"""Settings API routes."""

from typing import Optional

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user, verify_refresh_token
from app.domain.schemas.settings import (
    SecuritySettings,
    TwoFactorSetupResponse,
    TwoFactorVerifyRequest,
    TwoFactorDisableRequest,
    SessionRevokeRequest,
    AccountImpactResponse,
    AccountClosureRequest,
    SettingsUpdateRequest,
    SettingsResponse
)
from app.services.settings_service import SettingsService
from app.i18n.dependencies import get_locale
from app.utils.cookies import get_refresh_token_from_cookies
from app.api.openapi_responses import UNAUTHORIZED_RESPONSE

router = APIRouter(responses=UNAUTHORIZED_RESPONSE)
settings_service = SettingsService()


def _get_current_refresh_token_id(
    request: Request,
    db: Session
) -> Optional[str]:
    refresh_token = get_refresh_token_from_cookies(request)
    if not refresh_token:
        return None

    try:
        token_info = verify_refresh_token(refresh_token, db)
        return token_info.get("token_id")
    except Exception:
        return None


@router.get("/security", response_model=SecuritySettings)
async def get_security_settings(
    request: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Get security settings for the current user.
    """
    current_token_id = _get_current_refresh_token_id(request, db)
    return settings_service.get_security_settings(
        db,
        current_user.id,
        current_token_id=current_token_id
    )


@router.get("/account/impact", response_model=AccountImpactResponse)
async def get_account_impact(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    return settings_service.get_account_impact(db, current_user.id)


@router.post("/account/deactivate")
async def deactivate_account(
    request_data: AccountClosureRequest,
    response: Response,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    from app.utils.cookies import clear_auth_cookies

    settings_service.deactivate_account(db, current_user.id, request_data)
    clear_auth_cookies(response)
    return {"message": "Account deactivated successfully"}


@router.post("/account/delete")
async def delete_account(
    request_data: AccountClosureRequest,
    response: Response,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    from app.utils.cookies import clear_auth_cookies

    impact = settings_service.delete_account(db, current_user.id, request_data)
    clear_auth_cookies(response)
    return {
        "message": "Account permanently deleted successfully",
        "impact": impact.model_dump()
    }


@router.delete("/security/sessions/{session_id}")
async def revoke_session(
    session_id: str,
    request: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    current_token_id = _get_current_refresh_token_id(request, db)
    settings_service.revoke_session(
        db,
        current_user.id,
        SessionRevokeRequest(session_id=session_id),
        current_token_id=current_token_id
    )
    return {"message": "Session revoked successfully"}


@router.delete("/security/trusted-devices/{device_id}")
async def revoke_trusted_device(
    device_id: str,
    request: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    current_token_id = _get_current_refresh_token_id(request, db)
    settings_service.revoke_trusted_device(
        db,
        current_user.id,
        device_id,
        current_token_id=current_token_id
    )
    return {"message": "Trusted device revoked successfully"}


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
    request: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Get all settings for the current user.
    """
    current_token_id = _get_current_refresh_token_id(request, db)
    return settings_service.get_user_settings(
        db,
        current_user.id,
        current_token_id=current_token_id
    )


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
