"""Compatibility wrapper for mask-based notification settings service."""
from __future__ import annotations

from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.services.notification_settings_service import (
    notification_settings_service,
)


class NotificationPreferenceService:
    """Backward-compatible entrypoint used by existing services and routes."""

    def initialize_notification_types(self, db: Session) -> bool:
        return notification_settings_service.initialize_notification_types(db)

    def get_user_preferences(
        self, db: Session, user_id: int
    ) -> Dict[str, Any]:
        return notification_settings_service.get_settings(db, user_id)

    def update_user_preferences(
        self, db: Session, user_id: int, preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        return notification_settings_service.update_settings(
            db, user_id, preferences
        )

    def get_notification_types_with_preferences(
        self, db: Session, user_id: int
    ) -> List[Dict[str, Any]]:
        return (
            notification_settings_service
            .get_notification_types_with_preferences(db, user_id)
        )

    def should_send_notification(
        self, db: Session, user_id: int, notification_type: str, channel: str
    ) -> bool:
        return channel in notification_settings_service.get_allowed_channels(
            db, user_id, notification_type
        )

    def get_allowed_channels(
        self, db: Session, user_id: int, notification_type: str
    ) -> List[str]:
        return notification_settings_service.get_allowed_channels(
            db, user_id, notification_type
        )

    def get_channel_preferences(
        self, db: Session, user_id: int
    ) -> Dict[str, bool]:
        return notification_settings_service.get_channel_preferences(
            db, user_id
        )

    def update_channel_preferences(
        self, db: Session, user_id: int, channel_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        normalized = {
            "channels": {
                channel: bool(
                    value.get("enabled") if isinstance(value, dict) else value
                )
                for channel, value in channel_preferences.items()
            }
        }
        return notification_settings_service.update_settings(
            db, user_id, normalized
        )

    def get_notification_type_preferences(
        self, db: Session, user_id: int
    ) -> Dict[str, Dict[str, Any]]:
        return notification_settings_service.get_notification_type_preferences(
            db, user_id
        )

    def update_notification_type_preferences(
        self, db: Session, user_id: int, type_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        normalized = {
            "types": {
                type_key: {"enabled": bool(value)}
                for type_key, value in type_preferences.items()
            }
        }
        return notification_settings_service.update_settings(
            db, user_id, normalized
        )

    def get_quiet_hours(self, db: Session, user_id: int) -> Dict[str, Any]:
        return notification_settings_service.get_quiet_hours(db, user_id)

    def update_quiet_hours(
        self, db: Session, user_id: int, quiet_hours: Dict[str, Any]
    ) -> Dict[str, Any]:
        return notification_settings_service.update_quiet_hours(
            db, user_id, quiet_hours
        )

    def disable_quiet_hours(self, db: Session, user_id: int) -> Dict[str, Any]:
        return notification_settings_service.disable_quiet_hours(db, user_id)

    def enable_quiet_hours(
        self, db: Session, user_id: int, quiet_hours: Dict[str, Any]
    ) -> Dict[str, Any]:
        return notification_settings_service.enable_quiet_hours(
            db, user_id, quiet_hours
        )

    def get_default_preferences(self) -> Dict[str, Any]:
        return notification_settings_service.get_defaults()


notification_preference_service = NotificationPreferenceService()
