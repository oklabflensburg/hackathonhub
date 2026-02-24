"""
Notification API routes.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.domain.schemas.notification import (
    UserNotification, UserNotificationCreate,
    UserNotificationPreference, UserNotificationPreferenceCreate,
    PushSubscription, PushSubscriptionCreate
)
from app.repositories.notification_repository import (
    NotificationRepository,
    NotificationPreferenceRepository,
    PushSubscriptionRepository
)
from app.i18n.dependencies import get_locale
from app.i18n.helpers import (
    raise_not_found,
    raise_internal_server_error
)

router = APIRouter()
notification_repository = NotificationRepository()
preference_repository = NotificationPreferenceRepository()
push_subscription_repository = PushSubscriptionRepository()


@router.get("/", response_model=List[UserNotification])
async def get_notifications(
    skip: int = 0,
    limit: int = 100,
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get user notifications."""
    notifications = notification_repository.get_user_notifications(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        unread_only=unread_only
    )
    return notifications


@router.get("/{notification_id}", response_model=UserNotification)
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Get a specific notification by ID."""
    notification = notification_repository.get(db, notification_id)
    if not notification or notification.user_id != current_user.id:
        raise_not_found(locale, "notification")
    return notification


@router.post("/", response_model=UserNotification)
async def create_notification(
    notification: UserNotificationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a new notification."""
    # Create notification data with user_id
    notification_data = notification.model_dump()
    notification_data["user_id"] = current_user.id

    # Create notification using repository
    db_notification = notification_repository.create(
        db, obj_in=notification_data)

    return db_notification


@router.post("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Mark a notification as read."""
    success = notification_repository.mark_as_read(
        db, notification_id, current_user.id
    )
    if not success:
        raise_not_found(locale, "notification")
    return {
        "message": "Notification marked as read",
        "notification_id": notification_id
    }


@router.post("/read-all")
async def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Mark all notifications as read."""
    count = notification_repository.mark_all_as_read(db, current_user.id)
    return {
        "message": "All notifications marked as read",
        "count": count
    }


@router.get("/preferences", response_model=List[UserNotificationPreference])
async def get_notification_preferences(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get user notification preferences."""
    preferences = preference_repository.get_user_preferences(
        db, current_user.id
    )
    return preferences


@router.put(
    "/preferences/{preference_id}",
    response_model=UserNotificationPreference
)
async def update_notification_preference(
    preference_id: int,
    preference_update: UserNotificationPreferenceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Update a notification preference."""
    preference = preference_repository.get(db, preference_id)
    if not preference or preference.user_id != current_user.id:
        raise_not_found(locale, "preference")

    updated_preference = preference_repository.update(
        db, db_obj=preference, obj_in=preference_update.dict()
    )
    return updated_preference


@router.post("/preferences/{notification_type}/{channel}")
async def update_notification_preference_by_type(
    notification_type: str,
    channel: str,
    preference_update: UserNotificationPreferenceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update or create a notification preference by type and channel."""
    # Use the repository's update_or_create_preference method
    updated_preference = preference_repository.update_or_create_preference(
        db=db,
        user_id=current_user.id,
        notification_type=notification_type,
        channel=channel,
        enabled=preference_update.enabled
    )

    return updated_preference


@router.get("/push-subscriptions", response_model=List[PushSubscription])
async def get_push_subscriptions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get user push subscriptions."""
    subscriptions = push_subscription_repository.get_user_subscriptions(
        db, current_user.id
    )
    return subscriptions


@router.post("/push-subscriptions", response_model=PushSubscription)
async def create_push_subscription(
    subscription: PushSubscriptionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a push subscription."""
    # Check if subscription with same endpoint already exists
    existing = push_subscription_repository.get_by_endpoint(
        db, subscription.endpoint
    )
    if existing:
        # Update existing subscription
        updated_subscription = push_subscription_repository.update(
            db, db_obj=existing, obj_in=subscription.dict()
        )
        return updated_subscription

    # Create new subscription
    subscription_data = subscription.dict()
    subscription_data["user_id"] = current_user.id
    new_subscription = push_subscription_repository.create(
        db, obj_in=subscription_data
    )
    return new_subscription


@router.delete("/push-subscriptions/{subscription_id}")
async def delete_push_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Delete a push subscription."""
    subscription = push_subscription_repository.get(db, subscription_id)
    if not subscription or subscription.user_id != current_user.id:
        raise_not_found(locale, "subscription")

    success = push_subscription_repository.delete(db, id=subscription_id)
    if not success:
        raise_internal_server_error(locale, "subscription_deletion")

    return {"message": "Subscription deleted successfully"}
