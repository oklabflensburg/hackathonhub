"""
Notification preference service for managing user notification settings.
"""
import logging
from typing import Any, Dict, List, Set

from sqlalchemy.orm import Session

from app.domain.schemas.notification import NotificationTypeCreate
from app.repositories.notification_repository import (
    NotificationPreferenceRepository,
    NotificationTypeRepository,
)
from app.services.notification_registry import (
    get_definition,
    is_known_type,
    iter_definitions,
)

logger = logging.getLogger(__name__)

VALID_CHANNELS = ("email", "push", "in_app")


class NotificationPreferenceService:
    """Service for managing user notification preferences."""

    def __init__(self):
        self.type_repository = NotificationTypeRepository()
        self.preference_repository = NotificationPreferenceRepository()

    def initialize_notification_types(self, db: Session) -> bool:
        try:
            for definition in iter_definitions():
                existing = self.type_repository.get_by_type_key(
                    db, definition.type_key
                )
                payload = NotificationTypeCreate(
                    type_key=definition.type_key,
                    category=definition.category,
                    default_channels=",".join(definition.default_channels),
                    description=definition.description,
                )
                if existing:
                    self.type_repository.update(
                        db, db_obj=existing, obj_in=payload.model_dump()
                    )
                else:
                    self.type_repository.create(
                        db, obj_in=payload.model_dump()
                    )

            logger.info(
                "Initialized %s notification types",
                len(tuple(iter_definitions()))
            )
            return True
        except Exception as exc:
            logger.error("Failed to initialize notification types: %s", exc)
            return False

    def get_user_preferences(
        self, db: Session, user_id: int
    ) -> Dict[str, Any]:
        notification_types = self.type_repository.get_all(db)
        user_prefs = self.preference_repository.get_user_preferences(
            db, user_id
        )
        user_prefs_map = {
            f"{pref.notification_type}:{pref.channel}": pref.enabled
            for pref in user_prefs
        }

        preferences = {
            "global_enabled": True,
            "channels": {channel: True for channel in VALID_CHANNELS},
            "categories": {},
        }

        for notification_type in notification_types:
            category = notification_type.category
            default_channels = self._parse_channels(
                notification_type.default_channels
            )
            category_entry = preferences["categories"].setdefault(
                category,
                {
                    "enabled": True,
                    "channels": {
                        channel: channel in default_channels
                        for channel in VALID_CHANNELS
                    },
                    "types": {},
                },
            )
            category_entry["types"][notification_type.type_key] = {
                "enabled": True,
                "channels": {
                    channel: user_prefs_map.get(
                        f"{notification_type.type_key}:{channel}",
                        channel in default_channels,
                    )
                    for channel in VALID_CHANNELS
                },
            }

        return preferences

    def update_user_preferences(
        self, db: Session, user_id: int, preferences: Dict[str, Any]
    ) -> bool:
        try:
            updates = self._flatten_preferences_payload(preferences)
            for notification_type, channel_map in updates.items():
                if not is_known_type(notification_type):
                    logger.warning(
                        "Ignoring unknown notification type during update: %s",
                        notification_type,
                    )
                    continue
                for channel, enabled in channel_map.items():
                    self.preference_repository.update_or_create_preference(
                        db,
                        user_id=user_id,
                        notification_type=notification_type,
                        channel=channel,
                        enabled=enabled,
                    )
            return True
        except Exception as exc:
            logger.error(
                "Failed to update preferences for user %s: %s",
                user_id,
                exc,
            )
            return False

    def get_notification_types_with_preferences(
        self, db: Session, user_id: int
    ) -> List[Dict[str, Any]]:
        prefs = self.get_user_preferences(db, user_id)
        result = []
        for category_data in prefs["categories"].values():
            for type_key, type_preferences in category_data["types"].items():
                definition = get_definition(type_key)
                category = definition.category if definition else "system"
                description = definition.description if definition else None
                default_channels = list(
                    definition.default_channels if definition else ()
                )
                result.append(
                    {
                        "type_key": type_key,
                        "category": category,
                        "description": description,
                        "default_channels": default_channels,
                        "user_preferences": type_preferences["channels"],
                    }
                )
        return result

    def should_send_notification(
        self, db: Session, user_id: int, notification_type: str, channel: str
    ) -> bool:
        if channel not in VALID_CHANNELS or not is_known_type(
            notification_type
        ):
            return False

        preference = self.preference_repository.get_preference(
            db, user_id, notification_type, channel
        )
        if preference is not None:
            return preference.enabled

        definition = get_definition(notification_type)
        return channel in (definition.default_channels if definition else ())

    def get_allowed_channels(
        self, db: Session, user_id: int, notification_type: str
    ) -> List[str]:
        if not is_known_type(notification_type):
            return []
        return [
            channel
            for channel in VALID_CHANNELS

            if self.should_send_notification(
                db, user_id, notification_type, channel
            )
        ]

    def _flatten_preferences_payload(
        self, preferences: Dict[str, Any]
    ) -> Dict[str, Dict[str, bool]]:
        flattened: Dict[str, Dict[str, bool]] = {}

        direct_types = preferences.get("types", {})
        for notification_type, channel_map in direct_types.items():
            flattened[notification_type] = self._normalize_channel_map(
                channel_map
            )

        categories = preferences.get("categories", {})
        for category_data in categories.values():
            for notification_type, type_data in category_data.get(
                "types", {}
            ).items():
                flattened[notification_type] = self._normalize_channel_map(
                    type_data
                )

        return flattened

    def _normalize_channel_map(
        self, payload: Dict[str, Any]
    ) -> Dict[str, bool]:
        if "channels" in payload and isinstance(payload["channels"], dict):
            candidate = payload["channels"]
        else:
            candidate = payload

        normalized: Dict[str, bool] = {}
        for channel in VALID_CHANNELS:
            if channel in candidate:
                normalized[channel] = bool(candidate[channel])
        return normalized

    def _parse_channels(self, channels_str: str) -> Set[str]:
        if not channels_str:
            return set()
        return {
            channel.strip()
            for channel in channels_str.split(",")
            if channel.strip()
        }


notification_preference_service = NotificationPreferenceService()
