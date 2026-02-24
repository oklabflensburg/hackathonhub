"""
Push notification API routes.
"""
from fastapi import APIRouter, Depends, status
from app.core.config import settings
from app.i18n.dependencies import get_locale
from app.i18n.helpers import raise_i18n_http_exception

router = APIRouter()


@router.get("/vapid-public-key")
async def get_vapid_public_key(
    locale: str = Depends(get_locale)
):
    """Get VAPID public key for web push notifications."""
    vapid_public_key = settings.VAPID_PUBLIC_KEY

    if not vapid_public_key:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            translation_key="errors.server_error"
        )

    return {"public_key": vapid_public_key}