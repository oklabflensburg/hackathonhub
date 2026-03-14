"""Notification types API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.i18n.dependencies import get_locale
from app.repositories.notification_repository import NotificationTypeRepository
from app.services.notification_registry import iter_definitions
from app.utils.notification_flags import TYPE_FLAGS

from app.services.notification_settings_service import (
    notification_settings_service,
)

router = APIRouter()
type_repository = NotificationTypeRepository()


@router.get("")
async def get_notification_types(
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale),
):
    """Get all notification types."""
    try:
        notification_settings_service.initialize_notification_types(db)
        return [
            {
                "type_key": definition.type_key,
                "category": definition.category,
                "description": definition.description,
                "help_text": notification_settings_service._get_help_text(
                    definition.help_text_key,
                    locale,
                    definition.help_text,
                ),
                "help_text_key": definition.help_text_key,
                "default_channels": list(definition.default_channels),
                "type_flag": str(TYPE_FLAGS[definition.type_key]),
            }
            for definition in iter_definitions()
        ]
    except Exception:
        import logging
        logging.error("Error getting notification types")
        return []
