"""
Compatibility API routes for frontend that expects certain endpoints at root level.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.domain.schemas.notification import (
    UserNotificationPreference, PushSubscription, UserNotificationPreferenceCreate
)
from app.repositories.notification_repository import (
    NotificationPreferenceRepository,
    PushSubscriptionRepository
)

router = APIRouter()
preference_repository = NotificationPreferenceRepository()
push_subscription_repository = PushSubscriptionRepository()


@router.get(
    "/notification-preferences",
    response_model=List[UserNotificationPreference]
)
async def get_notification_preferences(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get user notification preferences (compatibility endpoint)."""
    try:
        preferences = preference_repository.get_user_preferences(
            db, current_user.id
        )
        return preferences
    except Exception:
        # If user is not authenticated, return empty array for compatibility
        return []


@router.put(
    "/notification-preferences",
    response_model=List[UserNotificationPreference]
)
async def update_notification_preferences(
    preferences: List[UserNotificationPreferenceCreate],
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update user notification preferences (compatibility endpoint)."""
    try:
        updated = []
        for pref in preferences:
            # Update or create each preference
            updated_pref = preference_repository.update_or_create_preference(
                db,
                user_id=current_user.id,
                notification_type=pref.notification_type,
                channel=pref.channel,
                enabled=pref.enabled
            )
            updated.append(updated_pref)
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update notification preferences: {str(e)}"
        )


@router.get("/push-subscriptions", response_model=List[PushSubscription])
async def get_push_subscriptions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
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