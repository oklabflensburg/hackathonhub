"""
Settings API routes.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.domain.schemas.settings import (
    SecuritySettings,
    TwoFactorSetupResponse,
    TwoFactorVerifyRequest,
    TwoFactorDisableRequest,
    SettingsUpdateRequest,
    SettingsResponse
)
from app.services.settings_service import SettingsService
from app.i18n.dependencies import get_locale

router = APIRouter()
settings_service = SettingsService()


@router.get("/security", response_model=SecuritySettings)
async def get_security_settings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Get security settings for the current user.
    """
    return settings_service.get_security_settings(db, current_user.id)


@router.post("/security/2fa/enable", response_model=TwoFactorSetupResponse)
async def enable_two_factor(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Enable two-factor authentication for the current user.
    
    Returns QR code, secret, and backup codes for setup.
    """
    return settings_service.enable_two_factor(db, current_user.id)


@router.post("/security/2fa/verify")
async def verify_two_factor(
    verify_request: TwoFactorVerifyRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Verify two-factor authentication setup.
    
    Verifies the TOTP code and enables 2FA for the user.
    """
    success = settings_service.verify_two_factor(
        db, current_user.id, verify_request
    )
    
    if success:
        return {"message": "Two-factor authentication enabled successfully"}
    else:
        return {"message": "Invalid verification code"}


@router.post("/security/2fa/disable")
async def disable_two_factor(
    disable_request: TwoFactorDisableRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Disable two-factor authentication for the current user.
    
    Requires password verification for security.
    """
    success = settings_service.disable_two_factor(
        db, current_user.id, disable_request
    )
    
    if success:
        return {"message": "Two-factor authentication disabled successfully"}
    else:
        return {"message": "Password is incorrect"}


@router.get("/", response_model=SettingsResponse)
async def get_settings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Get all settings for the current user.
    """
    return settings_service.get_user_settings(db, current_user.id)


@router.put("/", response_model=SettingsResponse)
async def update_settings(
    settings_update: SettingsUpdateRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Update user settings.
    """
    return settings_service.update_user_settings(
        db, current_user.id, settings_update
    )