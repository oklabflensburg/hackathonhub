"""
Push notification service for sending web push notifications.
"""
import base64
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import httpx
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from sqlalchemy.orm import Session

from app.domain.models.notification import (
    NotificationDelivery, PushSubscription
)
from app.repositories.notification_repository import PushSubscriptionRepository
from app.services.in_app_notification_service import DeliveryResult

try:
    from app.services.firebase_provider import firebase_provider
except Exception:  # pragma: no cover - optional dependency
    firebase_provider = None

logger = logging.getLogger(__name__)


class PushNotificationService:
    """Service for managing and sending push notifications."""

    def __init__(
        self,
        vapid_private_key: Optional[str] = None,
        vapid_public_key: Optional[str] = None,
    ):
        self.vapid_private_key = vapid_private_key
        self.vapid_public_key = vapid_public_key
        self.subscription_repo = PushSubscriptionRepository()
        if not self.vapid_private_key or not self.vapid_public_key:
            self._load_vapid_keys_from_env()

    def _load_vapid_keys_from_env(self):
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
        ttl: int = 86400,
    ) -> bool:
        result = self.deliver(
            db,
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            body=body,
            data=data,
            ttl=ttl,
        )
        return result.success

    def deliver(
        self,
        db: Session,
        *,
        user_id: int,
        notification_type: str,
        title: str,
        body: str,
        delivery: Optional[NotificationDelivery] = None,
        data: Optional[Dict[str, Any]] = None,
        ttl: int = 86400,
    ) -> DeliveryResult:
        subscriptions = self.subscription_repo.get_user_subscriptions(
            db, user_id
        )
        if not subscriptions:
            return DeliveryResult(
                success=False,
                status="failed",
                error="No push subscriptions found",
            )

        fcm_tokens = self._extract_fcm_tokens(subscriptions)
        web_push_subscriptions = [
            subscription
            for subscription in subscriptions
            if not self._is_fcm_token(subscription.endpoint)
        ]

        success_count = 0
        failed_endpoints: List[str] = []
        first_provider_id: Optional[str] = None

        if fcm_tokens:
            try:
                if firebase_provider is None:
                    failed_endpoints.extend(fcm_tokens)
                else:
                    fcm_result = firebase_provider.send_notification(
                        device_tokens=fcm_tokens,
                        title=title,
                        body=body,
                        data=data,
                        ttl=ttl,
                    )
                    success_count += fcm_result.get("success_count", 0)
                    for result in fcm_result.get("results", []):
                        if result.get("success", False):
                            first_provider_id = (
                                first_provider_id or result.get("message_id")
                            )
                        else:
                            failed_endpoints.append(result.get("token"))
            except Exception as exc:
                logger.error("Failed to send FCM notifications: %s", exc)
                failed_endpoints.extend(fcm_tokens)

        if web_push_subscriptions:
            payload = self._create_notification_payload(title, body, data)
            max_workers = min(8, len(web_push_subscriptions))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_map = {
                    executor.submit(
                        self._send_to_subscription, subscription, payload, ttl
                    ): subscription
                    for subscription in web_push_subscriptions
                }
                for future in as_completed(future_map):
                    subscription = future_map[future]
                    try:
                        if future.result():
                            success_count += 1
                        else:
                            failed_endpoints.append(subscription.endpoint)
                    except Exception as exc:
                        logger.error(
                            "Failed to send to subscription %s: %s",
                            subscription.endpoint,
                            exc,
                        )
                        failed_endpoints.append(subscription.endpoint)

        if failed_endpoints:
            removed = self.subscription_repo.delete_by_endpoints(
                db, user_id, failed_endpoints
            )
            if removed:
                logger.info(
                    "Removed %s failed push subscriptions for user %s",
                    removed,
                    user_id,
                )

        if success_count > 0:
            return DeliveryResult(
                success=True,
                status="delivered",
                provider_message_id=first_provider_id,
            )
        return DeliveryResult(
            success=False,
            status="failed",
            error="Failed to send push notification to any device",
        )

    def _is_fcm_token(self, endpoint: str) -> bool:
        fcm_patterns = [
            "https://fcm.googleapis.com/fcm/send/",
            "fcm.googleapis.com",
            "https://android.googleapis.com/gcm/send/",
            "android.googleapis.com",
        ]
        if endpoint and len(endpoint) > 100 and "http" not in endpoint:
            return True
        return any(pattern in endpoint for pattern in fcm_patterns)

    def _extract_fcm_tokens(
        self, subscriptions: List[PushSubscription]
    ) -> List[str]:
        fcm_tokens = []
        for subscription in subscriptions:
            endpoint = subscription.endpoint
            if not self._is_fcm_token(endpoint):
                continue
            if "http" in endpoint:
                token = endpoint.rsplit("/", 1)[-1]
                if token and len(token) > 50:
                    fcm_tokens.append(token)
            else:
                fcm_tokens.append(endpoint)
        return fcm_tokens

    def _create_notification_payload(
        self, title: str, body: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        payload = {
            "title": title,
            "body": body,
            "icon": "/icon-192x192.png",
            "badge": "/badge-72x72.png",
            "timestamp": int(datetime.utcnow().timestamp() * 1000),
        }
        if data:
            payload["data"] = data
        return payload

    def _send_to_subscription(
        self,
        subscription: PushSubscription,
        payload: Dict[str, Any],
        ttl: int,
    ) -> bool:
        endpoint = subscription.endpoint
        if not endpoint or not subscription.p256dh or not subscription.auth:
            logger.error("Invalid subscription: missing endpoint or keys")
            return False

        headers = {"Content-Type": "application/json", "TTL": str(ttl)}
        if self.vapid_private_key and self.vapid_public_key:
            vapid_auth_header = self._generate_vapid_auth_header(endpoint)
            if vapid_auth_header:
                headers["Authorization"] = vapid_auth_header

        try:
            with httpx.Client(timeout=10) as client:
                response = client.post(
                    endpoint,
                    headers=headers,
                    content=json.dumps(payload),
                )
            if response.status_code == 201:
                return True
            if response.status_code in {404, 410}:
                logger.info(
                    "Push subscription expired or invalid: %s", endpoint
                )
                return False
            logger.warning(
                "Failed to send push notification to %s: %s",
                endpoint,
                response.status_code,
            )
            return False
        except httpx.RequestError as exc:
            logger.error("Network error sending push notification: %s", exc)
            return False
        except Exception as exc:
            logger.error("Unexpected error sending push notification: %s", exc)
            return False

    def _generate_vapid_auth_header(self, endpoint: str) -> Optional[str]:
        try:
            if not self.vapid_private_key or not self.vapid_public_key:
                return None
            private_key_bytes = base64.urlsafe_b64decode(
                self.vapid_private_key + "=="
            )
            token = jwt.encode(
                {
                    "aud": self._get_audience_from_endpoint(endpoint),
                    "exp": datetime.utcnow() + timedelta(hours=12),
                    "sub": "mailto:admin@hackathonhub.oklabflensburg.de",
                },
                private_key_bytes,
                algorithm="ES256",
                headers={"typ": "JWT"},
            )
            crypto_key = f"p256ecdsa={self.vapid_public_key}"
            return f"vapid t={token}, k={crypto_key}"
        except Exception as exc:
            logger.error("Failed to generate VAPID auth header: %s", exc)
            return None

    def _get_audience_from_endpoint(self, endpoint: str) -> str:
        try:
            parsed = urlparse(endpoint)
            return f"{parsed.scheme}://{parsed.netloc}"
        except Exception:
            return endpoint

    def send_bulk_push_notifications(
        self,
        db: Session,
        user_ids: List[int],
        notification_type: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, int]:
        results = {"total": len(user_ids), "success": 0, "failed": 0}
        for user_id in user_ids:
            try:
                if self.send_push_notification(
                    db, user_id, notification_type, title, body, data
                ):
                    results["success"] += 1
                else:
                    results["failed"] += 1
            except Exception as exc:
                logger.error("Bulk push send failed: %s", exc)
                results["failed"] += 1
        return results

    def generate_vapid_keys(self) -> Dict[str, str]:
        private_key = ec.generate_private_key(
            ec.SECP256R1(), default_backend()
        )
        public_key = private_key.public_key()
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint,
        )
        return {
            "private_key": base64.urlsafe_b64encode(private_bytes)
            .decode("utf-8")
            .rstrip("="),
            "public_key": base64.urlsafe_b64encode(public_bytes)
            .decode("utf-8")
            .rstrip("="),
        }


push_notification_service = PushNotificationService()
