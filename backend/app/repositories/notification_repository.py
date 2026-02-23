"""
Notification repository for database operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.domain.models.notification import (
    UserNotification, UserNotificationPreference,
    NotificationType, PushSubscription
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
        unread_only: bool = False
    ) -> List[UserNotification]:
        """Get notifications for a specific user."""
        query = db.query(self.model).filter(self.model.user_id == user_id)

        if unread_only:
            query = query.filter(self.model.read_at.is_(None))

        return query.order_by(
            self.model.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def mark_as_read(
        self, db: Session, notification_id: int, user_id: int
    ) -> bool:
        """Mark a notification as read."""
        notification = db.query(self.model).filter(
            self.model.id == notification_id,
            self.model.user_id == user_id
        ).first()
        
        if notification and not notification.read_at:
            from datetime import datetime
            notification.read_at = datetime.utcnow()
            db.commit()
            return True
        return False
    
    def mark_all_as_read(self, db: Session, user_id: int) -> int:
        """Mark all notifications as read for a user."""
        from datetime import datetime
        result = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.read_at.is_(None)
        ).update(
            {"read_at": datetime.utcnow()},
            synchronize_session=False
        )
        db.commit()
        return result


class NotificationPreferenceRepository(
    BaseRepository[UserNotificationPreference]
):
    """Repository for user notification preferences."""
    
    def __init__(self):
        super().__init__(UserNotificationPreference)
    
    def get_user_preferences(
        self, db: Session, user_id: int
    ) -> List[UserNotificationPreference]:
        """Get all notification preferences for a user."""
        return db.query(self.model).filter(
            self.model.user_id == user_id
        ).all()
    
    def get_preference(
        self, db: Session, user_id: int, notification_type: str, channel: str
    ) -> Optional[UserNotificationPreference]:
        """Get a specific notification preference."""
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.notification_type == notification_type,
            self.model.channel == channel
        ).first()
    
    def update_or_create_preference(
        self,
        db: Session,
        user_id: int,
        notification_type: str,
        channel: str,
        enabled: bool
    ) -> UserNotificationPreference:
        """Update or create a notification preference."""
        preference = self.get_preference(
            db, user_id, notification_type, channel
        )
        
        if preference:
            preference.enabled = enabled
            db.commit()
            db.refresh(preference)
            return preference
        else:
            return self.create(db, obj_in={
                "user_id": user_id,
                "notification_type": notification_type,
                "channel": channel,
                "enabled": enabled
            })


class PushSubscriptionRepository(BaseRepository[PushSubscription]):
    """Repository for push subscriptions."""
    
    def __init__(self):
        super().__init__(PushSubscription)
    
    def get_user_subscriptions(
        self, db: Session, user_id: int
    ) -> List[PushSubscription]:
        """Get all push subscriptions for a user."""
        return db.query(self.model).filter(
            self.model.user_id == user_id
        ).all()
    
    def get_by_endpoint(
        self, db: Session, endpoint: str
    ) -> Optional[PushSubscription]:
        """Get a push subscription by endpoint."""
        return db.query(self.model).filter(
            self.model.endpoint == endpoint
        ).first()


class NotificationTypeRepository(BaseRepository[NotificationType]):
    """Repository for notification types."""
    
    def __init__(self):
        super().__init__(NotificationType)
    
    def get_by_type_key(
        self, db: Session, type_key: str
    ) -> Optional[NotificationType]:
        """Get a notification type by its key."""
        return db.query(self.model).filter(
            self.model.type_key == type_key
        ).first()
    
    def get_by_category(
        self, db: Session, category: str
    ) -> List[NotificationType]:
        """Get notification types by category."""
        return db.query(self.model).filter(
            self.model.category == category
        ).all()