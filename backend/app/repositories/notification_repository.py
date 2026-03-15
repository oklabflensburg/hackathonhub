"""
Notification repository for database operations.
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional, Sequence

from sqlalchemy.orm import Session, joinedload

from app.repositories.base import BaseRepository
from app.domain.models.notification import (
    NotificationDelivery,
    NotificationType,
    PushSubscription,
    UserNotification,
    UserNotificationPreference,
)


class NotificationRepository(BaseRepository[UserNotification]):
    """Repository for user notifications."""

    def __init__(self):
        super().__init__(UserNotification)

    def get_user_notifications(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        unread_only: bool = False,
    ) -> List[UserNotification]:
        query = db.query(self.model).options(
            joinedload(self.model.deliveries)
        ).filter(self.model.user_id == user_id)

        if unread_only:
            query = query.filter(self.model.read_at.is_(None))

        return query.order_by(
            self.model.created_at.desc()
        ).offset(skip).limit(limit).all()

    def create_notification(
        self,
        db: Session,
        *,
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        data: Optional[Dict] = None,
    ) -> UserNotification:
        return self.create(
            db,
            obj_in={
                "user_id": user_id,
                "notification_type": notification_type,
                "title": title,
                "message": message,
                "data": data,
            },
        )

    def mark_as_read(
        self, db: Session, notification_id: int, user_id: int
    ) -> bool:
        notification = db.query(self.model).filter(
            self.model.id == notification_id,
            self.model.user_id == user_id,
        ).first()

        if notification and not notification.read_at:
            notification.read_at = datetime.utcnow()
            db.commit()
            return True
        return notification is not None

    def mark_all_as_read(self, db: Session, user_id: int) -> int:
        result = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.read_at.is_(None),
        ).update(
            {"read_at": datetime.utcnow()},
            synchronize_session=False,
        )
        db.commit()
        return result

    def count_unread(self, db: Session, user_id: int) -> int:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.read_at.is_(None),
        ).count()


class NotificationDeliveryRepository(BaseRepository[NotificationDelivery]):
    """Repository for notification delivery records."""

    def __init__(self):
        super().__init__(NotificationDelivery)

    def create_deliveries(
        self,
        db: Session,
        notification_id: int,
        channels: Sequence[str],
    ) -> List[NotificationDelivery]:
        deliveries = [
            NotificationDelivery(
                notification_id=notification_id,
                channel=channel,
                status="pending",
            )
            for channel in channels
        ]
        db.add_all(deliveries)
        db.commit()
        for delivery in deliveries:
            db.refresh(delivery)
        return deliveries

    def get_by_notification(
        self, db: Session, notification_id: int
    ) -> List[NotificationDelivery]:
        return db.query(self.model).filter(
            self.model.notification_id == notification_id
        ).order_by(self.model.id.asc()).all()

    def get_for_channel(
        self, db: Session, notification_id: int, channel: str
    ) -> Optional[NotificationDelivery]:
        return db.query(self.model).filter(
            self.model.notification_id == notification_id,
            self.model.channel == channel,
        ).first()

    def update_status(
        self,
        db: Session,
        delivery: NotificationDelivery,
        *,
        status: str,
        error: Optional[str] = None,
        provider_message_id: Optional[str] = None,
        delivered_at: Optional[datetime] = None,
    ) -> NotificationDelivery:
        delivery.status = status
        delivery.error = error
        delivery.provider_message_id = provider_message_id
        delivery.delivered_at = delivered_at
        delivery.last_attempt_at = datetime.utcnow()
        delivery.attempt_count = (delivery.attempt_count or 0) + 1
        db.add(delivery)
        db.commit()
        db.refresh(delivery)
        return delivery


class NotificationPreferenceRepository(
    BaseRepository[UserNotificationPreference]
):
    """Repository for user notification settings masks."""

    def __init__(self):
        super().__init__(UserNotificationPreference)

    def get_by_user_id(
        self, db: Session, user_id: int
    ) -> Optional[UserNotificationPreference]:
        return db.query(self.model).filter(
            self.model.user_id == user_id
        ).first()

    def get_user_preferences(
        self, db: Session, user_id: int
    ) -> List[UserNotificationPreference]:
        preference = self.get_by_user_id(db, user_id)
        return [preference] if preference else []

    def get_or_create_settings(
        self,
        db: Session,
        user_id: int,
        *,
        default_types_mask: int = 0,
        default_channels_mask: int = 0,
    ) -> UserNotificationPreference:
        preference = self.get_by_user_id(db, user_id)
        if preference:
            return preference
        return self.create(
            db,
            obj_in={
                "user_id": user_id,
                "types_mask": str(default_types_mask),
                "channels_mask": str(default_channels_mask),
                "quiet_hours": {},
                "updated_at": datetime.now(timezone.utc),
            },
        )

    def update_settings_masks(
        self,
        db: Session,
        *,
        preference: UserNotificationPreference,
        types_mask: int,
        channels_mask: int,
        quiet_hours: Optional[Dict] = None,
    ) -> UserNotificationPreference:
        preference.types_mask = str(types_mask)
        preference.channels_mask = str(channels_mask)
        preference.quiet_hours = quiet_hours or {}
        preference.updated_at = datetime.now(timezone.utc)
        db.add(preference)
        db.commit()
        db.refresh(preference)
        return preference


class PushSubscriptionRepository(BaseRepository[PushSubscription]):
    """Repository for push subscriptions."""

    def __init__(self):
        super().__init__(PushSubscription)

    def get_user_subscriptions(
        self, db: Session, user_id: int
    ) -> List[PushSubscription]:
        return db.query(self.model).filter(
            self.model.user_id == user_id
        ).all()

    def get_by_endpoint(
        self, db: Session, endpoint: str
    ) -> Optional[PushSubscription]:
        return db.query(self.model).filter(
            self.model.endpoint == endpoint
        ).first()

    def delete_by_endpoints(
        self, db: Session, user_id: int, endpoints: Sequence[str]
    ) -> int:
        if not endpoints:
            return 0
        deleted = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.endpoint.in_(list(endpoints)),
        ).delete(synchronize_session=False)
        db.commit()
        return deleted


class NotificationTypeRepository(BaseRepository[NotificationType]):
    """Repository for notification types."""

    def __init__(self):
        super().__init__(NotificationType)

    def get_by_type_key(
        self, db: Session, type_key: str
    ) -> Optional[NotificationType]:
        return db.query(self.model).filter(
            self.model.type_key == type_key
        ).first()

    def get_by_category(
        self, db: Session, category: str
    ) -> List[NotificationType]:
        return db.query(self.model).filter(
            self.model.category == category
        ).order_by(self.model.sort_order.asc(), self.model.id.asc()).all()
