"""
Push notification service for sending web push notifications.
"""
import json
import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import base64
from urllib.parse import urlparse
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import jwt
import httpx

from sqlalchemy.orm import Session

from app.repositories.notification_repository import (
    PushSubscriptionRepository,
    NotificationRepository
)
from app.services.notification_preference_service import (
    notification_preference_service
)

logger = logging.getLogger(__name__)


class PushNotificationService:
    """Service for managing and sending push notifications."""

    def __init__(
        self,
        vapid_private_key: Optional[str] = None,
        vapid_public_key: Optional[str] = None
    ):
        """
        Initialize the push notification service.

        Args:
            vapid_private_key: VAPID private key (base64 encoded)
            vapid_public_key: VAPID public key (base64 encoded)
        """
        self.vapid_private_key = vapid_private_key
        self.vapid_public_key = vapid_public_key
        self.subscription_repo = PushSubscriptionRepository()
        self.notification_repo = NotificationRepository()

        # Load VAPID keys from environment if not provided
        if not self.vapid_private_key or not self.vapid_public_key:
            self._load_vapid_keys_from_env()

    def _load_vapid_keys_from_env(self):
        """Load VAPID keys from environment variables."""
        self.vapid_private_key = os.environ.get("VAPID_PRIVATE_KEY")
        self.vapid_public_key = os.environ.get("VAPID_PUBLIC_KEY")

        if not self.vapid_private_key or not self.vapid_public_key:
            logger.warning(
                "VAPID keys not configured. Push notifications will not work."
            )

    def send_push_notification(
        self,
        db: Session,
        user_id: int,
        notification_type: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
        ttl: int = 86400  # 24 hours
    ) -> bool:
        """
        Send a push notification to a user.

        Args:
            db: Database session
            user_id: User ID to send notification to
            notification_type: Type of notification
            title: Notification title
            body: Notification body
            data: Optional data payload
            ttl: Time to live in seconds

        Returns:
            bool: True if notification was sent successfully
            to at least one device
        """
        try:
            # Check if user has push notifications enabled for this type
            if not self._should_send_push_notification(
                db, user_id, notification_type
            ):
                logger.debug(
                    f"Push notifications disabled for user {user_id}, "
                    f"type {notification_type}"
                )
                return False

            # Get user's push subscriptions
            subscriptions = self.subscription_repo.get_user_subscriptions(
                db, user_id
            )
            if not subscriptions:
                logger.debug(f"No push subscriptions found for user {user_id}")
                return False

            # Prepare notification payload
            payload = self._create_notification_payload(title, body, data)

            # Send to each subscription
            success_count = 0
            failed_subscriptions = []

            for subscription in subscriptions:
                try:
                    if self._send_to_subscription(subscription, payload, ttl):
                        success_count += 1
                    else:
                        failed_subscriptions.append(subscription.endpoint)
                except Exception as e:
                    logger.error(
                        f"Failed to send to subscription "
                        f"{subscription.endpoint}: {e}"
                    )
                    failed_subscriptions.append(subscription.endpoint)

            # Clean up failed subscriptions
            if failed_subscriptions:
                self._cleanup_failed_subscriptions(
                    db, user_id, failed_subscriptions
                )

            # Log the notification
            if success_count > 0:
                self._log_notification(
                    db, user_id, notification_type,
                    title, body, data, "push"
                )
                logger.info(
                    f"Sent push notification to {success_count} "
                    f"device(s) for user {user_id}"
                )
                return True
            else:
                logger.warning(
                    f"Failed to send push notification to any "
                    f"device for user {user_id}"
                )
                return False

        except Exception as e:
            logger.error(f"Failed to send push notification: {e}")
            return False

    def _should_send_push_notification(
        self, db: Session, user_id: int, notification_type: str
    ) -> bool:
        """Check if push notification should be sent."""
        return notification_preference_service.should_send_notification(
            db, user_id, notification_type, "push"
        )

    def _create_notification_payload(
        self, title: str, body: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a web push notification payload."""
        payload = {
            "title": title,
            "body": body,
            "icon": "/icon-192x192.png",  # Default icon path
            "badge": "/badge-72x72.png",  # Default badge path
            # Milliseconds
            "timestamp": int(datetime.utcnow().timestamp() * 1000),
        }

        if data:
            payload["data"] = data

        return payload

    def _send_to_subscription(
        self,
        subscription: Any,
        payload: Dict[str, Any],
        ttl: int
    ) -> bool:
        """Send a notification to a specific subscription."""
        try:
            # Get subscription details
            endpoint = subscription.endpoint

            if (not endpoint or not subscription.p256dh
                    or not subscription.auth):
                logger.error("Invalid subscription: missing endpoint or keys")
                return False

            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "TTL": str(ttl),
            }

            # Add VAPID authorization if keys are configured
            if self.vapid_private_key and self.vapid_public_key:
                vapid_auth_header = self._generate_vapid_auth_header(endpoint)
                if vapid_auth_header:
                    headers["Authorization"] = vapid_auth_header

            # Send the request
            with httpx.Client(timeout=10) as client:
                response = client.post(
                    endpoint,
                    headers=headers,
                    content=json.dumps(payload)
                )

            # Check response
            if response.status_code == 201:
                logger.debug(
                    f"Push notification sent successfully to {endpoint}"
                )
                return True
            elif response.status_code in [404, 410]:
                # Subscription expired or invalid
                logger.info(
                    f"Push subscription expired or invalid: {endpoint}"
                )
                return False
            else:
                logger.warning(
                    f"Failed to send push notification to {endpoint}: "
                    f"{response.status_code}"
                )
                return False

        except httpx.RequestError as e:
            logger.error(f"Network error sending push notification: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending push notification: {e}")
            return False

    def _generate_vapid_auth_header(
        self, endpoint: str
    ) -> Optional[str]:
        """Generate VAPID authorization header."""
        try:
            if not self.vapid_private_key or not self.vapid_public_key:
                return None

            # Decode base64 private key
            private_key_bytes = base64.urlsafe_b64decode(
                self.vapid_private_key + "=="
            )

            # Create JWT token
            token = jwt.encode(
                {
                    "aud": self._get_audience_from_endpoint(endpoint),
                    "exp": datetime.utcnow() + timedelta(hours=12),
                    "sub": "mailto:admin@hackathonhub.oklabflensburg.de"
                },
                private_key_bytes,
                algorithm="ES256",
                headers={"typ": "JWT"}
            )

            # Create Crypto-Key header
            crypto_key = f"p256ecdsa={self.vapid_public_key}"

            # Return Authorization header
            return f"vapid t={token}, k={crypto_key}"

        except Exception as e:
            logger.error(f"Failed to generate VAPID auth header: {e}")
            return None

    def _get_audience_from_endpoint(self, endpoint: str) -> str:
        """Extract audience from push endpoint URL."""
        try:
            parsed = urlparse(endpoint)
            return f"{parsed.scheme}://{parsed.netloc}"
        except Exception:
            # Fallback to the endpoint itself
            return endpoint

    def _cleanup_failed_subscriptions(
        self, db: Session, user_id: int, failed_endpoints: List[str]
    ):
        """Remove failed push subscriptions from database."""
        for endpoint in failed_endpoints:
            try:
                subscription = self.subscription_repo.get_by_endpoint(
                    db, endpoint
                )
                if subscription and subscription.user_id == user_id:
                    db.delete(subscription)
                    db.commit()
                    logger.info(
                        f"Removed failed push subscription: {endpoint}"
                    )
            except Exception as e:
                logger.error(
                    f"Failed to remove push subscription {endpoint}: {e}"
                )

    def _log_notification(
        self,
        db: Session,
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]],
        channel: str
    ):
        """Log the notification in the database."""
        try:
            self.notification_repo.create(db, obj_in={
                "user_id": user_id,
                "type": notification_type,
                "title": title,
                "message": message,
                "data": data or {},
                "channel": channel,
                "read": False,
                "created_at": datetime.utcnow()
            })
        except Exception as e:
            logger.error(f"Failed to log notification: {e}")

    def send_bulk_push_notifications(
        self,
        db: Session,
        user_ids: List[int],
        notification_type: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, int]:
        """
        Send push notifications to multiple users.

        Args:
            db: Database session
            user_ids: List of user IDs
            notification_type: Type of notification
            title: Notification title
            body: Notification body
            data: Optional data payload

        Returns:
            Dict with success and failure counts
        """
        results = {
            "total": len(user_ids),
            "success": 0,
            "failed": 0
        }

        for user_id in user_ids:
            try:
                if self.send_push_notification(
                    db, user_id, notification_type, title, body, data
                ):
                    results["success"] += 1
                else:
                    results["failed"] += 1
            except Exception as e:
                logger.error(
                    f"Failed to send push notification to user {user_id}: {e}"
                )
                results["failed"] += 1

        return results

    def generate_vapid_keys(self) -> Dict[str, str]:
        """
        Generate new VAPID keys for web push.

        Returns:
            Dict with base64 encoded private and public keys
        """
        try:
            # Generate EC key pair
            private_key = ec.generate_private_key(
                ec.SECP256R1(), default_backend()
            )
            public_key = private_key.public_key()

            # Serialize keys
            private_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            public_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.X962,
                format=serialization.PublicFormat.UncompressedPoint
            )

            # Convert to base64 URL-safe strings
            private_b64 = base64.urlsafe_b64encode(
                private_bytes
            ).decode('utf-8').rstrip('=')
            public_b64 = base64.urlsafe_b64encode(
                public_bytes
            ).decode('utf-8').rstrip('=')

            return {
                "private_key": private_b64,
                "public_key": public_b64
            }

        except Exception as e:
            logger.error(f"Failed to generate VAPID keys: {e}")
            raise


# Global service instance
push_notification_service = PushNotificationService()