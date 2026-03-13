"""
In-app notification adapter.
"""
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.domain.models.notification import (
    NotificationDelivery,
    UserNotification
)
from app.repositories.notification_repository import (
    NotificationDeliveryRepository,
    NotificationRepository,
)

logger = logging.getLogger(__name__)


@dataclass
class DeliveryResult:
    success: bool
    status: str
    error: Optional[str] = None
    provider_message_id: Optional[str] = None


class InAppNotificationService:
    """Service for managing in-app notifications."""

    def __init__(self):
        self.notification_repo = NotificationRepository()
        self.delivery_repo = NotificationDeliveryRepository()

    def store_notification(
        self,
        db: Session,
        user_id: int,
        title: str,
        body: str,
        notification_type: str,
        priority: str = "normal",
        data: Optional[Dict[str, Any]] = None,
        action_url: Optional[str] = None,
        icon_url: Optional[str] = None,
        image_url: Optional[str] = None,
        expires_in_days: int = 30,
    ) -> UserNotification:
        payload = dict(data or {})
        payload.setdefault("priority", priority)
        if action_url:
            payload["action_url"] = action_url
        if icon_url:
            payload["icon_url"] = icon_url
        if image_url:
            payload["image_url"] = image_url
        payload.setdefault(
            "expires_at",
            (datetime.utcnow() + timedelta(days=expires_in_days)).isoformat(),
        )

        notification = self.notification_repo.create_notification(
            db,
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            message=body,
            data=payload,
        )
        self.delivery_repo.create_deliveries(db, notification.id, ["in_app"])
        return self.notification_repo.get(db, notification.id)

    def deliver(
        self,
        db: Session,
        notification: UserNotification,
        delivery: NotificationDelivery,
    ) -> DeliveryResult:
        return DeliveryResult(success=True, status="delivered")

    def get_user_notifications(
        self,
        db: Session,
        user_id: int,
        limit: int = 50,
        offset: int = 0,
        unread_only: bool = False,
        include_expired: bool = False,
    ) -> List[UserNotification]:
        notifications = self.notification_repo.get_user_notifications(
            db,
            user_id=user_id,
            skip=offset,
            limit=limit,
            unread_only=unread_only,
        )
        if include_expired:
            return notifications

        result = []
        now = datetime.utcnow()
        for notification in notifications:
            expires_at = (notification.data or {}).get("expires_at")
            if isinstance(expires_at, str):
                try:
                    expires_at = datetime.fromisoformat(expires_at)
                except ValueError:
                    expires_at = None
            if expires_at and expires_at <= now:
                continue
            result.append(notification)
        return result

    def get_unread_count(self, db: Session, user_id: int) -> int:
        return self.notification_repo.count_unread(db, user_id)

    def mark_as_read(
        self, db: Session, notification_id: int, user_id: int
    ) -> bool:
        return self.notification_repo.mark_as_read(
            db, notification_id, user_id
        )

    def mark_all_as_read(self, db: Session, user_id: int) -> int:
        return self.notification_repo.mark_all_as_read(db, user_id)

    def cleanup_expired_notifications(self, db: Session) -> int:
        notifications = self.notification_repo.get_multi(
            db, skip=0, limit=10000
        )
        now = datetime.utcnow()
        expired_ids = []
        for notification in notifications:
            expires_at = (notification.data or {}).get("expires_at")
            if isinstance(expires_at, str):
                try:
                    expires_at = datetime.fromisoformat(expires_at)
                except ValueError:
                    expires_at = None
            if expires_at and expires_at <= now:
                expired_ids.append(notification.id)

        if not expired_ids:
            return 0

        deleted = db.query(UserNotification).filter(
            UserNotification.id.in_(expired_ids)
        ).delete(synchronize_session=False)

        db.commit()
        return deleted
