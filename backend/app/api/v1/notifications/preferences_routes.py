"""
Notification Preferences API Routes

Provides endpoints for users to manage their notification preferences,
including channel preferences, quiet hours, and notification types.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.domain.models.user import User
from app.services.notification_preference_service import (
    NotificationPreferenceService
)

router = APIRouter(prefix="/preferences", tags=["notification-preferences"])


@router.get("")
async def get_notification_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's notification preferences.
    """
    service = NotificationPreferenceService(db)
    preferences = service.get_user_preferences(current_user.id)

    return preferences


@router.put("")
async def update_notification_preferences(
    preferences: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update current user's notification preferences.

    Expected structure:
    {
        "notifications_enabled": true,
        "quiet_hours": {
            "enabled": true,
            "start_hour": 22,
            "end_hour": 8
        },
        "channels": {
            "in_app": {
                "enabled": true,
                "priority": "normal"
            },
            "email": {
                "enabled": true,
                "priority": "normal"
            },
            "push": {
                "enabled": true,
                "priority": "normal"
            }
        },
        "notification_types": {
            "system": ["in_app", "email"],
            "user": ["in_app", "push"],
            "team": ["in_app", "email", "push"],
            "project": ["in_app", "push"],
            "hackathon": ["in_app", "email", "push"],
            "comment": ["in_app"],
            "invitation": ["in_app", "email"],
            "reminder": ["in_app", "push"],
            "alert": ["in_app", "email", "push"]
        }
    }
    """
    service = NotificationPreferenceService(db)

    try:
        updated = service.update_user_preferences(
            current_user.id, preferences
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/channels")
async def get_channel_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's channel preferences.
    """
    service = NotificationPreferenceService(db)
    channels = service.get_channel_preferences(current_user.id)

    return channels


@router.put("/channels")
async def update_channel_preferences(
    channel_preferences: Dict[str, Dict[str, Any]] = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update current user's channel preferences.

    Example:
    {
        "in_app": {
            "enabled": true,
            "priority": "normal"
        },
        "email": {
            "enabled": false,
            "priority": "low"
        },
        "push": {
            "enabled": true,
            "priority": "high"
        }
    }
    """
    service = NotificationPreferenceService(db)

    try:
        updated = service.update_channel_preferences(
            current_user.id, channel_preferences
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/types")
async def get_notification_type_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's notification type preferences.
    """
    service = NotificationPreferenceService(db)
    type_prefs = service.get_notification_type_preferences(current_user.id)

    return type_prefs


@router.put("/types")
async def update_notification_type_preferences(
    type_preferences: Dict[str, List[str]] = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update current user's notification type preferences.

    Example:
    {
        "system": ["in_app", "email"],
        "user": ["in_app", "push"],
        "team": ["in_app", "email", "push"],
        "project": ["in_app", "push"],
        "hackathon": ["in_app", "email", "push"],
        "comment": ["in_app"],
        "invitation": ["in_app", "email"],
        "reminder": ["in_app", "push"],
        "alert": ["in_app", "email", "push"]
    }
    """
    service = NotificationPreferenceService(db)

    try:
        updated = service.update_notification_type_preferences(
            current_user.id, type_preferences
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/quiet-hours")
async def get_quiet_hours(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's quiet hours settings.
    """
    service = NotificationPreferenceService(db)
    quiet_hours = service.get_quiet_hours(current_user.id)

    return quiet_hours


@router.put("/quiet-hours")
async def update_quiet_hours(
    quiet_hours: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update current user's quiet hours settings.

    Example:
    {
        "enabled": true,
        "start_hour": 22,
        "end_hour": 8,
        "days": [0, 1, 2, 3, 4, 5, 6]  # 0=Sunday, 6=Saturday
    }
    """
    service = NotificationPreferenceService(db)

    try:
        updated = service.update_quiet_hours(
            current_user.id, quiet_hours
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quiet-hours/disable")
async def disable_quiet_hours(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Disable quiet hours for current user.
    """
    service = NotificationPreferenceService(db)
    updated = service.disable_quiet_hours(current_user.id)

    return updated


@router.post("/quiet-hours/enable")
async def enable_quiet_hours(
    start_hour: int = Body(22, embed=True),
    end_hour: int = Body(8, embed=True),
    days: Optional[List[int]] = Body(None, embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Enable quiet hours for current user.
    """
    service = NotificationPreferenceService(db)

    quiet_hours = {
        "enabled": True,
        "start_hour": start_hour,
        "end_hour": end_hour
    }

    if days is not None:
        quiet_hours["days"] = days

    updated = service.update_quiet_hours(current_user.id, quiet_hours)

    return updated


@router.post("/enable")
async def enable_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Enable all notifications for current user.
    """
    service = NotificationPreferenceService(db)
    updated = service.enable_notifications(current_user.id)

    return updated


@router.post("/disable")
async def disable_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Disable all notifications for current user.
    """
    service = NotificationPreferenceService(db)
    updated = service.disable_notifications(current_user.id)

    return updated


@router.get("/status")
async def get_notification_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's notification status summary.
    """
    service = NotificationPreferenceService(db)
    status = service.get_notification_status(current_user.id)

    return status


@router.get("/defaults")
async def get_default_preferences():
    """
    Get default notification preferences.
    """
    service = NotificationPreferenceService(None)  # No db needed for defaults
    defaults = service.get_default_preferences()

    return defaults


@router.post("/reset")
async def reset_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Reset current user's preferences to defaults.
    """
    service = NotificationPreferenceService(db)
    reset = service.reset_to_defaults(current_user.id)

    return reset


@router.get("/available-channels")
async def get_available_channels():
    """
    Get available notification channels with descriptions.
    """
    return {
        "channels": [
            {
                "id": "in_app",
                "name": "In-App Notifications",
                "description": "Notifications within the application",
                "default_enabled": True,
                "requires_permission": False
            },
            {
                "id": "email",
                "name": "Email Notifications",
                "description": "Notifications sent via email",
                "default_enabled": True,
                "requires_permission": True
            },
            {
                "id": "push",
                "name": "Push Notifications",
                "description": "Mobile and web push notifications",
                "default_enabled": True,
                "requires_permission": True
            }
        ]
    }


@router.get("/available-types")
async def get_available_notification_types():
    """
    Get available notification types with descriptions.
    """
    return {
        "types": [
            {
                "id": "system",
                "name": "System Notification",
                "description": "System-wide announcements and updates",
                "default_channels": ["in_app", "email"]
            },
            {
                "id": "user",
                "name": "User Notification",
                "description": "Notifications related to user account",
                "default_channels": ["in_app", "push"]
            },
            {
                "id": "team",
                "name": "Team Notification",
                "description": "Notifications related to teams",
                "default_channels": ["in_app", "email", "push"]
            },
            {
                "id": "project",
                "name": "Project Notification",
                "description": "Notifications related to projects",
                "default_channels": ["in_app", "push"]
            },
            {
                "id": "hackathon",
                "name": "Hackathon Notification",
                "description": "Notifications related to hackathons",
                "default_channels": ["in_app", "email", "push"]
            },
            {
                "id": "comment",
                "name": "Comment Notification",
                "description": "Notifications about comments",
                "default_channels": ["in_app"]
            },
            {
                "id": "invitation",
                "name": "Invitation Notification",
                "description": "Notifications about invitations",
                "default_channels": ["in_app", "email"]
            },
            {
                "id": "reminder",
                "name": "Reminder Notification",
                "description": "Reminder notifications",
                "default_channels": ["in_app", "push"]
            },
            {
                "id": "alert",
                "name": "Alert Notification",
                "description": "Important alerts and warnings",
                "default_channels": ["in_app", "email", "push"]
            }
        ]
    }
