"""
Notification API routes.
"""
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.domain.schemas.notification import (
    PushSubscription,
    PushSubscriptionCreate,
    UserNotification,
    UserNotificationCreate,
    UserNotificationPreferenceCreate,
)
from app.i18n.dependencies import get_locale
from app.i18n.helpers import raise_internal_server_error, raise_not_found
from app.repositories.notification_repository import (
    NotificationRepository,
    PushSubscriptionRepository,
)
from app.services.in_app_notification_service import InAppNotificationService
from app.services.notification_settings_service import (
    notification_settings_service,
)
from app.services.notification_service import notification_service

router = APIRouter()
notification_repository = NotificationRepository()
push_subscription_repository = PushSubscriptionRepository()
in_app_service = InAppNotificationService()


@router.get("", response_model=List[UserNotification])
async def get_notifications(
    skip: int = 0,
    limit: int = 100,
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return notification_service.get_user_notifications(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        unread_only=unread_only,
    )


@router.post("", response_model=UserNotification)
async def create_notification(
    notification: UserNotificationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    dispatch = notification_service.dispatch_notification(
        db=db,
        notification_type=notification.notification_type,
        user_id=current_user.id,
        title=notification.title,
        message=notification.message,
        data=notification.data or {},
        requested_channels=["in_app"],
    )
    if dispatch.notification is None:
        raise HTTPException(
            status_code=409,
            detail="Notification disabled by current preferences",
        )
    return dispatch.notification


@router.post("/read-all")
async def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    count = notification_repository.mark_all_as_read(db, current_user.id)
    return {"message": "All notifications marked as read", "count": count}


@router.get("/preferences")
async def get_notification_preferences(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale),
):
    return notification_settings_service.get_settings_for_locale(
        db, current_user.id, locale=locale
    )


@router.post("/preferences/{notification_type}/{channel}")
async def update_notification_preference_by_type(
    notification_type: str,
    channel: str,
    preference_update: UserNotificationPreferenceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return notification_settings_service.update_type_channel_compatibility(
        db,
        current_user.id,
        notification_type,
        channel,
        preference_update.enabled,
    )


@router.put("/preferences")
async def bulk_update_notification_preferences(
    preferences: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale),
):
    notification_settings_service.update_settings(
        db, current_user.id, preferences
    )
    return {
        "success": True,
        "preferences": notification_settings_service.get_settings_for_locale(
            db, current_user.id, locale=locale
        ),
    }


@router.get("/push-subscriptions", response_model=List[PushSubscription])
async def get_push_subscriptions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return push_subscription_repository.get_user_subscriptions(
        db, current_user.id
    )


@router.post("/push-subscriptions", response_model=PushSubscription)
async def create_push_subscription(
    subscription: PushSubscriptionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    existing = push_subscription_repository.get_by_endpoint(
        db, subscription.endpoint
    )
    if existing:
        updated_subscription = push_subscription_repository.update(
            db, db_obj=existing, obj_in=subscription.model_dump()
        )
        return updated_subscription

    subscription_data = subscription.model_dump()
    subscription_data["user_id"] = current_user.id
    return push_subscription_repository.create(db, obj_in=subscription_data)


@router.get("/unread-count")
async def get_unread_count(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    count = notification_repository.count_unread(db, current_user.id)
    return {"count": count}


@router.get("/{notification_id}", response_model=UserNotification)
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale),
):
    notification = notification_repository.get(db, notification_id)
    if not notification or notification.user_id != current_user.id:
        raise_not_found(locale, "notification")
    return notification


@router.post("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale),
):
    success = notification_repository.mark_as_read(
        db, notification_id, current_user.id
    )
    if not success:
        raise_not_found(locale, "notification")
    return {
        "message": "Notification marked as read",
        "notification_id": notification_id,
    }


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale),
):
    notification = notification_repository.get(db, notification_id)
    if not notification or notification.user_id != current_user.id:
        raise_not_found(locale, "notification")

    success = notification_repository.delete(db, id=notification_id)
    if not success:
        raise_internal_server_error(locale, "notification_deletion")

    return {"message": "Notification deleted successfully"}


@router.delete("/push-subscriptions/{subscription_id}")
async def delete_push_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale),
):
    subscription = push_subscription_repository.get(db, subscription_id)
    if not subscription or subscription.user_id != current_user.id:
        raise_not_found(locale, "subscription")

    success = push_subscription_repository.delete(db, id=subscription_id)
    if not success:
        raise_internal_server_error(locale, "subscription_deletion")

    return {"message": "Subscription deleted successfully"}


@router.post("/in-app", response_model=UserNotification, status_code=201)
async def create_in_app_notification(
    notification_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    payload = dict(notification_data.get("metadata") or {})
    if notification_data.get("action_url"):
        payload["action_url"] = notification_data["action_url"]
    if notification_data.get("priority"):
        payload["priority"] = notification_data["priority"]
    if notification_data.get("expires_at"):
        payload["expires_at"] = notification_data["expires_at"]
    dispatch = notification_service.dispatch_notification(
        db=db,
        notification_type=notification_data.get("type", "system_announcement"),
        user_id=current_user.id,
        title=notification_data.get("title", ""),
        message=notification_data.get("message", ""),
        data={"metadata": payload} if payload else {},
        requested_channels=["in_app"],
    )
    if dispatch.notification is None:
        raise HTTPException(
            status_code=409,
            detail="Notification disabled by current preferences",
        )
    return dispatch.notification


@router.get("/in-app/list")
async def get_in_app_notifications(
    skip: int = 0,
    limit: int = 50,
    unread_only: bool = False,
    include_expired: bool = False,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    notifications = in_app_service.get_user_notifications(
        db=db,
        user_id=current_user.id,
        offset=skip,
        limit=limit,
        unread_only=unread_only,
        include_expired=include_expired,
    )
    return {
        "notifications": [
            UserNotification.model_validate(notification).model_dump()
            for notification in notifications
        ],
        "total": len(notifications),
        "skip": skip,
        "limit": limit,
    }


@router.get("/in-app/unread-count")
async def get_in_app_unread_count(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return {"count": in_app_service.get_unread_count(db, current_user.id)}


@router.post("/in-app/{notification_id}/read")
async def mark_in_app_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale),
):
    success = in_app_service.mark_as_read(db, notification_id, current_user.id)
    if not success:
        raise_not_found(locale, "notification")
    return {
        "message": "Notification marked as read",
        "notification_id": notification_id,
    }


@router.post("/in-app/mark-all-read")
async def mark_all_in_app_notifications_as_read(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    count = in_app_service.mark_all_as_read(db, current_user.id)
    return {"message": f"Marked {count} notifications as read", "count": count}


@router.delete("/in-app/{notification_id}")
async def delete_in_app_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale),
):
    notification = notification_repository.get(db, notification_id)
    if not notification or notification.user_id != current_user.id:
        raise_not_found(locale, "notification")

    success = notification_repository.delete(db, id=notification_id)
    if not success:
        raise_internal_server_error(locale, "notification_deletion")

    return {"message": "Notification deleted successfully"}


@router.post("/in-app/cleanup")
async def cleanup_expired_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    count = in_app_service.cleanup_expired_notifications(db)
    return {
        "message": f"Cleaned up {count} expired notifications", "count": count
    }
