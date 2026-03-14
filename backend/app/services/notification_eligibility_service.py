"""
Centralized eligibility checks for notification dispatching.
"""
from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.repositories.notification_repository import PushSubscriptionRepository
from app.services.notification_settings_service import (
    notification_settings_service
)


class NotificationEligibilityService:
    def __init__(self):
        self.push_repository = PushSubscriptionRepository()

    def is_event_enabled(
        self, db: Session, user_id: int, notification_type: str
    ) -> bool:
        return notification_settings_service.is_type_enabled(
            db, user_id, notification_type
        )

    def get_allowed_channels(
        self,
        db: Session,
        user_id: int,
        notification_type: str,
        requested_channels: Optional[List[str]] = None,
    ) -> List[str]:
        push_runtime_enabled = bool(
            self.push_repository.get_user_subscriptions(db, user_id)
        )
        allowed = notification_settings_service.get_allowed_channels(
            db,
            user_id,
            notification_type,
            push_runtime_enabled=push_runtime_enabled,
        )
        if requested_channels is None:
            return allowed
        requested = set(requested_channels)
        return [channel for channel in allowed if channel in requested]


notification_eligibility_service = NotificationEligibilityService()
