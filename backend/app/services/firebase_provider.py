"""
Firebase Cloud Messaging (FCM) provider for push notifications.
"""
import json
import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import httpx
from google.oauth2 import service_account
import google.auth.transport.requests

logger = logging.getLogger(__name__)


class FirebaseProvider:
    """Firebase Cloud Messaging provider for mobile push notifications."""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Firebase provider.

        Args:
            credentials_path: Path to Firebase service account JSON file.
                If not provided, loads from environment variables.
        """
        self.credentials = None
        self.project_id = None
        self.access_token = None
        self.token_expiry = None

        self._initialize_firebase(credentials_path)

    def _initialize_firebase(self, credentials_path: Optional[str] = None):
        """Initialize Firebase credentials."""
        try:
            # Try to load from environment variables first
            firebase_config = self._load_from_env()

            if firebase_config:
                self.credentials = (
                    service_account.Credentials.from_service_account_info(
                        firebase_config
                    )
                )
                self.project_id = firebase_config.get('project_id')
                logger.info(
                    f"Firebase initialized from environment for project: "
                    f"{self.project_id}"
                )
            elif credentials_path and os.path.exists(credentials_path):
                # Load from JSON file
                with open(credentials_path, 'r') as f:
                    firebase_config = json.load(f)
                self.credentials = (
                    service_account.Credentials.from_service_account_file(
                        credentials_path
                    )
                )
                self.project_id = firebase_config.get('project_id')
                logger.info(
                    f"Firebase initialized from file for project: "
                    f"{self.project_id}"
                )
            else:
                logger.warning(
                    "Firebase credentials not configured. "
                    "FCM push notifications will not work."
                )
                return

            # Refresh access token
            self._refresh_access_token()

        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")

    def _load_from_env(self) -> Optional[Dict[str, Any]]:
        """Load Firebase configuration from environment variables."""
        try:
            project_id = os.environ.get("FIREBASE_PROJECT_ID")
            private_key_id = os.environ.get("FIREBASE_PRIVATE_KEY_ID")
            private_key = os.environ.get("FIREBASE_PRIVATE_KEY")
            client_email = os.environ.get("FIREBASE_CLIENT_EMAIL")
            client_id = os.environ.get("FIREBASE_CLIENT_ID")
            client_x509_cert_url = os.environ.get(
                "FIREBASE_CLIENT_X509_CERT_URL"
            )

            if not all([project_id, private_key, client_email]):
                return None

            # Clean up private key (replace escaped newlines)
            if private_key:
                private_key = private_key.replace('\\n', '\n')

            return {
                "type": "service_account",
                "project_id": project_id,
                "private_key_id": private_key_id,
                "private_key": private_key,
                "client_email": client_email,
                "client_id": client_id,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": (
                    "https://www.googleapis.com/oauth2/v1/certs"
                ),
                "client_x509_cert_url": client_x509_cert_url
            }
        except Exception as e:
            logger.error(f"Failed to load Firebase config from env: {e}")
            return None

    def _refresh_access_token(self):
        """Refresh Firebase access token."""
        if not self.credentials:
            return

        try:
            request = google.auth.transport.requests.Request()
            self.credentials.refresh(request)
            self.access_token = self.credentials.token
            self.token_expiry = self.credentials.expiry
            logger.debug("Firebase access token refreshed")
        except Exception as e:
            logger.error(f"Failed to refresh Firebase access token: {e}")

    def _ensure_valid_token(self):
        """Ensure we have a valid access token."""
        if not self.access_token or not self.token_expiry:
            self._refresh_access_token()
            return

        # Refresh if token expires in less than 5 minutes
        if (self.token_expiry - datetime.utcnow()).total_seconds() < 300:
            self._refresh_access_token()

    def send_notification(
        self,
        device_tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
        image_url: Optional[str] = None,
        priority: str = "high",
        ttl: int = 2419200  # 28 days in seconds
    ) -> Dict[str, Any]:
        """
        Send push notification via Firebase Cloud Messaging.

        Args:
            device_tokens: List of FCM device tokens
            title: Notification title
            body: Notification body
            data: Optional data payload
            image_url: Optional image URL for notification
            priority: Notification priority (high/normal)
            ttl: Time to live in seconds

        Returns:
            Dict with success count, failure count, and results
        """
        if not self.credentials or not self.project_id:
            logger.warning(
                "Firebase not initialized, skipping FCM notification"
            )
            return {
                "success_count": 0,
                "failure_count": len(device_tokens),
                "results": []
            }

        if not device_tokens:
            return {"success_count": 0, "failure_count": 0, "results": []}

        self._ensure_valid_token()

        # Prepare notification payload
        notification_payload = {
            "title": title,
            "body": body,
        }

        if image_url:
            notification_payload["image"] = image_url

        # Prepare message payload
        message = {
            "notification": notification_payload,
            "android": {
                "priority": priority.upper(),
                "ttl": f"{ttl}s",
                "notification": {
                    "sound": "default",
                    "channel_id": "default"
                }
            },
            "apns": {
                "payload": {
                    "aps": {
                        "sound": "default",
                        "badge": 1
                    }
                },
                "headers": {
                    "apns-priority": "10" if priority == "high" else "5"
                }
            },
            "webpush": {
                "headers": {
                    "Urgency": priority
                }
            }
        }

        if data:
            message["data"] = data

        results = []
        success_count = 0
        failure_count = 0

        # Send to each device token
        for token in device_tokens:
            try:
                # Add token to message
                token_message = message.copy()
                token_message["token"] = token

                # Send request to FCM
                response = self._send_fcm_request(token_message)

                if response.get("success", False):
                    success_count += 1
                    results.append({
                        "token": token,
                        "success": True,
                        "message_id": response.get("message_id"),
                        "error": None
                    })
                    logger.debug(
                        f"FCM notification sent successfully to token: "
                        f"{token[:20]}..."
                    )
                else:
                    failure_count += 1
                    results.append({
                        "token": token,
                        "success": False,
                        "message_id": None,
                        "error": response.get("error")
                    })
                    logger.warning(
                        f"FCM notification failed for token {token[:20]}...: "
                        f"{response.get('error')}"
                    )

                    # Handle specific error cases
                    error = response.get("error", "")
                    if ("InvalidRegistration" in error or
                            "NotRegistered" in error):
                        logger.info(
                            f"Device token is invalid or unregistered: "
                            f"{token[:20]}..."
                        )

            except Exception as e:
                failure_count += 1
                results.append({
                    "token": token,
                    "success": False,
                    "message_id": None,
                    "error": str(e)
                })
                logger.error(
                    f"Exception sending FCM notification to {token[:20]}...: "
                    f"{e}"
                )

        logger.info(
            f"FCM notification sent: {success_count} successful, "
            f"{failure_count} failed out of {len(device_tokens)} devices"
        )

        return {
            "success_count": success_count,
            "failure_count": failure_count,
            "results": results
        }

    def _send_fcm_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send HTTP request to FCM API."""
        url = (
            f"https://fcm.googleapis.com/v1/projects/{self.project_id}/"
            f"messages:send"
        )

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {"message": message}

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()

                response_data = response.json()

                # Check for errors in response
                if "error" in response_data:
                    return {
                        "success": False,
                        "error": response_data["error"].get(
                            "message", "Unknown error"
                        )
                    }

                # Extract message ID from response
                message_id = response_data.get("name", "").split("/")[-1]

                return {
                    "success": True,
                    "message_id": message_id
                }

        except httpx.HTTPError as e:
            error_msg = f"HTTP error: {e}"
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get("error", {}).get(
                        "message", str(e)
                    )
                except Exception:
                    error_msg = (
                        f"HTTP {e.response.status_code}: "
                        f"{e.response.text}"
                    )

            return {
                "success": False,
                "error": error_msg
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

    def send_to_topic(
        self,
        topic: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
        image_url: Optional[str] = None
    ) -> bool:
        """
        Send notification to a Firebase topic.

        Args:
            topic: Firebase topic name
            title: Notification title
            body: Notification body
            data: Optional data payload
            image_url: Optional image URL

        Returns:
            bool: True if successful
        """
        if not self.credentials or not self.project_id:
            logger.warning(
                "Firebase not initialized, skipping topic notification"
            )
            return False

        self._ensure_valid_token()

        # Prepare notification payload
        notification_payload = {
            "title": title,
            "body": body,
        }

        if image_url:
            notification_payload["image"] = image_url

        # Prepare message payload
        message = {
            "notification": notification_payload,
            "topic": topic,
        }

        if data:
            message["data"] = data

        try:
            response = self._send_fcm_request(message)
            success = response.get("success", False)

            if success:
                logger.info(
                    f"FCM topic notification sent successfully to topic: "
                    f"{topic}"
                )
            else:
                logger.error(
                    f"FCM topic notification failed for topic {topic}: "
                    f"{response.get('error')}"
                )

            return success

        except Exception as e:
            logger.error(
                f"Exception sending FCM topic notification to {topic}: {e}"
            )
            return False

    def subscribe_to_topic(
        self,
        device_tokens: List[str],
        topic: str
    ) -> bool:
        """
        Subscribe devices to a Firebase topic.

        Args:
            device_tokens: List of FCM device tokens
            topic: Firebase topic name

        Returns:
            bool: True if successful
        """
        return self._manage_topic_subscription(
            device_tokens, topic, "subscribe"
        )

    def unsubscribe_from_topic(
        self,
        device_tokens: List[str],
        topic: str
    ) -> bool:
        """
        Unsubscribe devices from a Firebase topic.

        Args:
            device_tokens: List of FCM device tokens
            topic: Firebase topic name

        Returns:
            bool: True if successful
        """
        return self._manage_topic_subscription(
            device_tokens, topic, "unsubscribe"
        )

    def _manage_topic_subscription(
        self,
        device_tokens: List[str],
        topic: str,
        operation: str
    ) -> bool:
        """Manage topic subscriptions (subscribe/unsubscribe)."""
        if not self.credentials or not self.project_id:
            logger.warning(
                "Firebase not initialized, skipping topic management"
            )
            return False

        if not device_tokens:
            return True

        self._ensure_valid_token()

        url = (
            "https://iid.googleapis.com/iid/v1:batchAdd"
            if operation == "subscribe"
            else "https://iid.googleapis.com/iid/v1:batchRemove"
        )

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "to": f"/topics/{topic}",
            "registration_tokens": device_tokens
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()

                response_data = response.json()

                # Check for errors
                if "error" in response_data:
                    logger.error(
                        f"FCM topic {operation} failed: "
                        f"{response_data['error']}"
                    )
                    return False

                # Check results
                results = response_data.get("results", [])
                success_count = sum(1 for r in results if "error" not in r)
                error_count = len(results) - success_count

                if error_count > 0:
                    logger.warning(
                        f"FCM topic {operation}: {success_count} successful, "
                        f"{error_count} failed out of {len(device_tokens)} "
                        f"devices"
                    )
                else:
                    logger.info(
                        f"FCM topic {operation} successful for all "
                        f"{len(device_tokens)} devices"
                    )

                return success_count > 0

        except Exception as e:
            logger.error(f"Exception during FCM topic {operation}: {e}")
            return False


# Global Firebase provider instance
firebase_provider = FirebaseProvider()
