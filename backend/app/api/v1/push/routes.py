"""
Push notification API routes.
"""
from fastapi import APIRouter, HTTPException
from app.core.config import settings

router = APIRouter()


@router.get("/vapid-public-key")
async def get_vapid_public_key():
    """Get VAPID public key for web push notifications."""
    vapid_public_key = settings.VAPID_PUBLIC_KEY

    if not vapid_public_key:
        raise HTTPException(
            status_code=501,
            detail=(
                "Push notifications not configured. "
                "VAPID public key not set."
            )
        )

    return {"public_key": vapid_public_key}