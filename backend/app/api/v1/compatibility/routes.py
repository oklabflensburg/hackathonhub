"""Compatibility API routes for frontend that expects certain endpoints at root level."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Any, Dict, List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.domain.schemas.notification import (
    PushSubscription,
)
from app.repositories.notification_repository import (
    PushSubscriptionRepository
)
from app.i18n.dependencies import get_locale
from app.i18n.helpers import raise_i18n_http_exception
from app.services.notification_settings_service import (
    notification_settings_service,
)

router = APIRouter()
push_subscription_repository = PushSubscriptionRepository()


@router.get("/notification-preferences")
async def get_notification_preferences(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Get user notification preferences (compatibility endpoint)."""
    try:
        return notification_settings_service.get_settings(
            db, current_user.id
        )
    except Exception:
        return {"global_enabled": False, "channels": {}, "categories": {}}


@router.put("/notification-preferences")
async def update_notification_preferences(
    preferences: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Update user notification preferences (compatibility endpoint)."""
    try:
        return notification_settings_service.update_settings(
            db, current_user.id, preferences
        )
    except Exception as e:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            translation_key="errors.server_error",
            error=str(e)
        )


@router.get("/push-subscriptions", response_model=List[PushSubscription])
async def get_push_subscriptions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Get user push subscriptions (compatibility endpoint)."""
    try:
        subscriptions = push_subscription_repository.get_user_subscriptions(
            db, current_user.id
        )
        return subscriptions
    except Exception:
        # If user is not authenticated, return empty array for compatibility
        return []
