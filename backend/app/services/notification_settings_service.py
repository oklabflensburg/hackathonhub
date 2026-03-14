"""
Central notification settings service backed by bitmasks.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.i18n.translations import get_translation
from app.repositories.notification_repository import (
    NotificationPreferenceRepository,
    NotificationTypeRepository,
)
from app.utils.notification_flags import (
    ALL_CHANNEL_FLAGS_MASK,
    ALL_TYPE_FLAGS_MASK,
    CHANNEL_FLAGS,
    TYPE_FLAGS,
)
from app.utils.notification_mask_utils import (
    are_all_flags_enabled,
    disable_flag,
    enable_flag,
    has_flag
)
from app.services.notification_registry import (
    get_definition,
    is_known_type,
    iter_definitions
)


class NotificationSettingsService:
    """Reads and writes notification settings via type/channel bitmasks."""

    def __init__(self):
        self.preference_repository = NotificationPreferenceRepository()
        self.type_repository = NotificationTypeRepository()

    def initialize_notification_types(self, db: Session) -> bool:
        for index, definition in enumerate(iter_definitions()):
            payload = {
                "type_key": definition.type_key,
                "category": definition.category,
                "default_channels": ",".join(definition.default_channels),
                "description": definition.description,
                "help_text": definition.help_text,
                "type_flag": str(TYPE_FLAGS[definition.type_key]),
                "sort_order": index,
            }
            existing = self.type_repository.get_by_type_key(
                db, definition.type_key)
            if existing:
                self.type_repository.update(
                    db, db_obj=existing, obj_in=payload)
            else:
                self.type_repository.create(db, obj_in=payload)
        return True

    def get_settings(self, db: Session, user_id: int) -> Dict[str, Any]:
        return self.get_settings_for_locale(db, user_id, locale="en")

    def get_settings_for_locale(
        self, db: Session, user_id: int, locale: str = "en"
    ) -> Dict[str, Any]:
        preference = self.preference_repository.get_or_create_settings(
            db,
            user_id,
            default_types_mask=ALL_TYPE_FLAGS_MASK,
            default_channels_mask=ALL_CHANNEL_FLAGS_MASK,
        )
        type_mask = preference.types_mask_int
        channel_mask = preference.channels_mask_int
        quiet_hours = self._normalize_quiet_hours(preference.quiet_hours)

        categories: Dict[str, Dict[str, Any]] = {}
        for definition in iter_definitions():
            type_flag = TYPE_FLAGS[definition.type_key]
            type_enabled = has_flag(type_mask, type_flag)
            type_channels = {
                channel: (
                    type_enabled
                    and channel in definition.default_channels
                    and has_flag(channel_mask, flag)
                )
                for channel, flag in CHANNEL_FLAGS.items()
            }
            category_entry = categories.setdefault(
                definition.category,
                {
                    "enabled": True,
                    "channels": {channel: True for channel in CHANNEL_FLAGS},
                    "types": {},
                },
            )
            category_entry["types"][definition.type_key] = {
                "enabled": type_enabled,
                "channels": type_channels,
                "description": definition.description,
                "help_text": self._get_help_text(
                    definition.help_text_key,
                    locale,
                    definition.help_text,
                ),
                "help_text_key": definition.help_text_key,
                "category": definition.category,
                "default_channels": list(definition.default_channels),
            }

        for category_name, category_entry in categories.items():
            type_flags = [
                TYPE_FLAGS[type_key]
                for type_key, type_data in category_entry["types"].items()
                if type_data["category"] == category_name
            ]
            category_entry["enabled"] = are_all_flags_enabled(
                type_mask, type_flags)
            category_entry["channels"] = {
                channel: all(
                    type_data["channels"][channel]
                    or channel not in type_data["default_channels"]
                    for type_data in category_entry["types"].values()
                )
                for channel in CHANNEL_FLAGS
            }

        return {
            "global_enabled": are_all_flags_enabled(
                type_mask, TYPE_FLAGS.values()
            ),
            "channels": {
                channel: has_flag(channel_mask, flag)
                for channel, flag in CHANNEL_FLAGS.items()
            },
            "categories": categories,
            "types": {
                definition.type_key: categories[definition.category]["types"][
                    definition.type_key
                ]
                for definition in iter_definitions()
            },
            "masks": {
                "channels": str(channel_mask),
                "types": str(type_mask),
            },
            "quiet_hours": quiet_hours,
        }

    def get_notification_types_with_preferences(
        self, db: Session, user_id: int, locale: str = "en"
    ) -> List[Dict[str, Any]]:
        settings = self.get_settings_for_locale(db, user_id, locale=locale)
        result: List[Dict[str, Any]] = []
        for definition in iter_definitions():
            type_settings = settings["types"][definition.type_key]
            result.append(
                {
                    "type_key": definition.type_key,
                    "category": definition.category,
                    "description": definition.description,
                    "help_text": type_settings["help_text"],
                    "help_text_key": definition.help_text_key,
                    "default_channels": list(definition.default_channels),
                    "type_flag": str(TYPE_FLAGS[definition.type_key]),
                    "user_preferences": type_settings["channels"],
                    "enabled": type_settings["enabled"],
                }
            )
        return result

    def update_settings(
        self, db: Session, user_id: int, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        preference = self.preference_repository.get_or_create_settings(
            db,
            user_id,
            default_types_mask=ALL_TYPE_FLAGS_MASK,
            default_channels_mask=ALL_CHANNEL_FLAGS_MASK,
        )
        type_mask = preference.types_mask_int
        channel_mask = preference.channels_mask_int
        quiet_hours = self._normalize_quiet_hours(preference.quiet_hours)

        if "global_enabled" in payload:
            type_mask = ALL_TYPE_FLAGS_MASK if payload["global_enabled"] else 0

        if "quiet_hours" in payload:
            quiet_hours = self._merge_quiet_hours(
                quiet_hours,
                payload.get("quiet_hours") or {},
            )

        for channel, enabled in (payload.get("channels") or {}).items():
            if channel in CHANNEL_FLAGS:
                channel_mask = self._set_mask_flag(
                    channel_mask, CHANNEL_FLAGS[channel], bool(enabled)
                )

        direct_types = payload.get("types") or {}
        for type_key, value in direct_types.items():
            type_mask = self._apply_type_update(type_mask, type_key, value)

        for category_name, category_data in (
            payload.get("categories") or {}
        ).items():
            if "enabled" in category_data:
                type_mask = self._set_category_enabled(
                    type_mask, category_name, bool(category_data["enabled"])
                )
            for type_key, value in (category_data.get("types") or {}).items():
                type_mask = self._apply_type_update(type_mask, type_key, value)

        updated = self.preference_repository.update_settings_masks(
            db,
            preference=preference,
            types_mask=type_mask,
            channels_mask=channel_mask,
            quiet_hours=quiet_hours,
        )
        return self.get_settings_for_locale(db, updated.user_id)

    def update_type_channel_compatibility(
        self,
        db: Session,
        user_id: int,
        type_key: str,
        channel: str,
        enabled: bool,
    ) -> Dict[str, Any]:
        if not is_known_type(type_key) or channel not in CHANNEL_FLAGS:
            raise ValueError("Unknown notification type or channel")

        payload: Dict[str, Any] = {"types": {type_key: {"enabled": enabled}}}
        definition = get_definition(type_key)
        if enabled and definition and channel in definition.default_channels:
            payload["channels"] = {channel: True}
        return self.update_settings(db, user_id, payload)

    def is_type_enabled(
        self, db: Session, user_id: int, type_key: str
    ) -> bool:
        if type_key not in TYPE_FLAGS:
            return False
        preference = self.preference_repository.get_or_create_settings(
            db,
            user_id,
            default_types_mask=ALL_TYPE_FLAGS_MASK,
            default_channels_mask=ALL_CHANNEL_FLAGS_MASK,
        )
        return has_flag(preference.types_mask_int, TYPE_FLAGS[type_key])

    def get_allowed_channels(
        self,
        db: Session,
        user_id: int,
        type_key: str,
        *,
        push_runtime_enabled: bool = True,
    ) -> List[str]:
        if not is_known_type(type_key):
            return []
        preference = self.preference_repository.get_or_create_settings(
            db,
            user_id,
            default_types_mask=ALL_TYPE_FLAGS_MASK,
            default_channels_mask=ALL_CHANNEL_FLAGS_MASK,
        )
        if not has_flag(preference.types_mask_int, TYPE_FLAGS[type_key]):
            return []
        definition = get_definition(type_key)
        if not definition:
            return []
        allowed = [
            channel
            for channel in definition.default_channels
            if has_flag(preference.channels_mask_int, CHANNEL_FLAGS[channel])
        ]
        if not push_runtime_enabled:
            allowed = [channel for channel in allowed if channel != "push"]
        return allowed

    def get_channel_preferences(
        self, db: Session, user_id: int
    ) -> Dict[str, bool]:
        settings = self.get_settings(db, user_id)
        return settings["channels"]

    def get_notification_type_preferences(
        self, db: Session, user_id: int
    ) -> Dict[str, Dict[str, Any]]:
        settings = self.get_settings(db, user_id)
        return settings["types"]

    def get_defaults(self) -> Dict[str, Any]:
        return {
            "channels": {
                channel: True for channel in CHANNEL_FLAGS
            },
            "quiet_hours": self._normalize_quiet_hours(None),
            "masks": {
                "channels": str(ALL_CHANNEL_FLAGS_MASK),
                "types": str(ALL_TYPE_FLAGS_MASK),
            },
            "definitions": [
                asdict(definition) for definition in iter_definitions()
            ]
        }

    def get_quiet_hours(self, db: Session, user_id: int) -> Dict[str, Any]:
        return self.get_settings(db, user_id)["quiet_hours"]

    def update_quiet_hours(
        self, db: Session, user_id: int, quiet_hours: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.update_settings(
            db,
            user_id,
            {"quiet_hours": quiet_hours},
        )["quiet_hours"]

    def disable_quiet_hours(
        self, db: Session, user_id: int
    ) -> Dict[str, Any]:
        return self.update_quiet_hours(db, user_id, {"enabled": False})

    def enable_quiet_hours(
        self, db: Session, user_id: int, quiet_hours: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.update_quiet_hours(
            db,
            user_id,
            {"enabled": True, **quiet_hours},
        )

    def _get_help_text(
        self, translation_key: str, locale: str, fallback: str
    ) -> str:
        try:
            return get_translation(translation_key, locale)
        except KeyError:
            return fallback

    def _apply_type_update(
        self, type_mask: int, type_key: str, value: Any
    ) -> int:
        if type_key not in TYPE_FLAGS:
            return type_mask
        enabled = value.get("enabled") if isinstance(value, dict) else value
        if enabled is None:
            return type_mask
        return self._set_mask_flag(
            type_mask, TYPE_FLAGS[type_key], bool(enabled)
        )

    def _set_category_enabled(
        self, type_mask: int, category: str, enabled: bool
    ) -> int:
        for definition in iter_definitions():
            if definition.category != category:
                continue
            type_mask = self._set_mask_flag(
                type_mask,
                TYPE_FLAGS[definition.type_key],
                enabled,
            )
        return type_mask

    def _set_mask_flag(self, mask: int, flag: int, enabled: bool) -> int:
        if enabled:
            return enable_flag(mask, flag)
        return disable_flag(mask, flag)

    def _normalize_quiet_hours(
        self, quiet_hours: Dict[str, Any] | None
    ) -> Dict[str, Any]:
        source = quiet_hours or {}
        start = str(
            source.get("start")
            or f"{int(source.get('start_hour', 22)):02d}:00"
        )
        end = str(
            source.get("end")
            or f"{int(source.get('end_hour', 8)):02d}:00"
        )
        days = source.get("days")
        if not isinstance(days, list):
            days = []
        return {
            "enabled": bool(source.get("enabled", False)),
            "start": start,
            "end": end,
            "start_hour": self._time_to_hour(start, 22),
            "end_hour": self._time_to_hour(end, 8),
            "days": [int(day) for day in days],
        }

    def _merge_quiet_hours(
        self, current: Dict[str, Any], incoming: Dict[str, Any]
    ) -> Dict[str, Any]:
        merged = dict(current)
        merged.update(incoming)
        return self._normalize_quiet_hours(merged)

    def _time_to_hour(self, value: str, default: int) -> int:
        try:
            return int(str(value).split(":", 1)[0])
        except (ValueError, TypeError):
            return default


notification_settings_service = NotificationSettingsService()
