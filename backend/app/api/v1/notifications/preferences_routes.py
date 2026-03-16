"""Notification preference endpoints backed by the mask-based settings service."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.domain.models.user import User
from app.services.notification_preference_service import (
    notification_preference_service,
)
from app.api.openapi_responses import UNAUTHORIZED_RESPONSE

router = APIRouter(prefix="/preferences", tags=["notification-preferences"])


@router.get("", responses=UNAUTHORIZED_RESPONSE)
async def get_notification_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_preference_service.get_user_preferences(db, current_user.id)


@router.put("", responses=UNAUTHORIZED_RESPONSE)
async def update_notification_preferences(
    preferences: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_preference_service.update_user_preferences(
        db, current_user.id, preferences
    )


@router.get("/channels", responses=UNAUTHORIZED_RESPONSE)
async def get_channel_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_preference_service.get_channel_preferences(
        db, current_user.id
    )


@router.put("/channels", responses=UNAUTHORIZED_RESPONSE)
async def update_channel_preferences(
    channel_preferences: Dict[str, Dict[str, Any]] = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_preference_service.update_channel_preferences(
        db, current_user.id, channel_preferences
    )


@router.get("/types", responses=UNAUTHORIZED_RESPONSE)
async def get_notification_type_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_preference_service.get_notification_type_preferences(
        db, current_user.id
    )


@router.put("/types", responses=UNAUTHORIZED_RESPONSE)
async def update_notification_type_preferences(
    type_preferences: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_preference_service.update_notification_type_preferences(
        db, current_user.id, type_preferences
    )


@router.get("/quiet-hours", responses=UNAUTHORIZED_RESPONSE)
async def get_quiet_hours(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_preference_service.get_quiet_hours(db, current_user.id)


@router.put("/quiet-hours", responses=UNAUTHORIZED_RESPONSE)
async def update_quiet_hours(
    quiet_hours: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_preference_service.update_quiet_hours(
        db, current_user.id, quiet_hours
    )


@router.post("/quiet-hours/disable", responses=UNAUTHORIZED_RESPONSE)
async def disable_quiet_hours(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_preference_service.disable_quiet_hours(
        db, current_user.id
    )


@router.post("/quiet-hours/enable", responses=UNAUTHORIZED_RESPONSE)
async def enable_quiet_hours(
    start_hour: int = Body(22, embed=True),
    end_hour: int = Body(8, embed=True),
    days: Optional[List[int]] = Body(None, embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload: Dict[str, Any] = {
        "start_hour": start_hour,
        "end_hour": end_hour,
    }
    if days is not None:
        payload["days"] = days
    return notification_preference_service.enable_quiet_hours(
        db, current_user.id, payload
    )


@router.get("/defaults")
async def get_default_preferences():
    return notification_preference_service.get_default_preferences()


@router.post("/reset", responses=UNAUTHORIZED_RESPONSE)
async def reset_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_preference_service.update_user_preferences(
        db,
        current_user.id,
        {"global_enabled": True, "channels": {"email": True, "push": True, "in_app": True}},
    )
