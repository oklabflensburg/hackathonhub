"""
Authentication API routes.
"""

from typing import Optional

from fastapi import APIRouter, Depends, status, Query, Response, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os

from app.core.database import get_db
from app.domain.schemas.user import (
    TokenWithRefresh, UserRegister, UserLogin, EmailResendRequest,
    EmailVerificationRequest, PasswordResetRequest, PasswordResetConfirm
)
from app.domain.schemas.settings import (
    TwoFactorLoginVerifyRequest, TwoFactorBackupVerifyRequest,
    TwoFactorLoginResponse
)
from app.core.auth import refresh_tokens, verify_refresh_token
from app.core.permissions import apply_access_context
from app.services.auth_service import auth_service
from app.services.google_oauth_service import google_oauth
from app.services.github_oauth_service import github_oauth
from app.i18n.dependencies import get_locale
from app.i18n.helpers import (
    raise_unauthorized,
    raise_forbidden,
    raise_bad_request,
    raise_i18n_http_exception
)
from app.utils.cookies import (
    set_auth_cookies,
    clear_auth_cookies,
    get_refresh_token_from_cookies,
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login", auto_error=False
)


def _serialize_auth_user(db: Session, user):
    if not user:
        return None
    return apply_access_context(db, user)


@router.post("/login")
async def login(
    login_data: UserLogin,
    response: Response,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Login endpoint that accepts JSON.

    JSON format: {"email": "...", "password": "..."}

    Returns:
        - If 2FA is required: {"requires_2fa": True, "temp_token": "...",
          "user_id": ...}
        - If 2FA is not required: {"access_token": "...",
          "refresh_token": "...", "token_type": "bearer",
          "requires_2fa": False}
    """
    try:
        # Use the consolidated auth service for email/password authentication
        auth_result = auth_service.login_with_email(
            db,
            email=login_data.email,
            password=login_data.password,
            remember_me=login_data.remember_me
        )
    except ValueError as e:
        # Convert ValueError from auth service to HTTPException
        error_message = str(e)
        if "Email not verified" in error_message:
            raise_forbidden(locale, "email_verification")
        else:
            raise_unauthorized(locale, "credentials")

    if not auth_result:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_401_UNAUTHORIZED,
            translation_key="errors.incorrect_email_or_password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Check if 2FA is required
    if auth_result.get("requires_2fa", False):
        # Return 2FA required response
        return {
            "requires_2fa": True,
            "temp_token": auth_result.get("temp_token", ""),
            "user_id": auth_result.get("user_id", 0),
            "message": auth_result.get(
                "message", "Two-factor authentication required"
            )
        }

    # Extract tokens from auth result
    access_token = auth_result.get("access_token", "")
    refresh_token = auth_result.get("refresh_token", "")

    # Set HTTP-Only cookies for SSR compatibility
    set_auth_cookies(
        response=response,
        auth_token=access_token,
        refresh_token=refresh_token,
        persistent=login_data.remember_me,
        secure=False  # In development, set to False for local testing
    )

    # Return full auth result including requires_2fa field
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": auth_result.get("token_type", "bearer"),
        "requires_2fa": False,
        "user": _serialize_auth_user(db, auth_result.get("user"))
    }


@router.post("/login/json")
async def login_json(
    login_data: UserLogin,
    response: Response,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    JSON-based login endpoint (alias for /login).

    Accepts email and password in JSON format.

    Returns:
        - If 2FA is required: {"requires_2fa": True, "temp_token": "...",
          "user_id": ...}
        - If 2FA is not required: {"access_token": "...",
          "refresh_token": "...", "token_type": "bearer",
          "requires_2fa": False}
    """
    # Simply call the main login function
    return await login(login_data, response, db, locale)


@router.post("/refresh", response_model=TokenWithRefresh)
async def refresh_token(
    request: Request,
    response: Response,
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Refresh access token using a valid refresh token.
    """
    refresh_token_value = token or get_refresh_token_from_cookies(request)
    if not refresh_token_value:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_401_UNAUTHORIZED,
            translation_key="errors.invalid_refresh_token"
        )

    token_data = refresh_tokens(refresh_token_value, db)
    set_auth_cookies(
        response=response,
        auth_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        persistent=token_data.get("is_persistent", False)
    )
    return TokenWithRefresh(
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        token_type=token_data["token_type"]
    )


@router.post("/logout")
async def logout(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    response: Response = None,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Logout by revoking a refresh token and clearing auth cookies.
    """
    refresh_token_value = token or get_refresh_token_from_cookies(request)
    if not refresh_token_value:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_401_UNAUTHORIZED,
            translation_key="errors.invalid_refresh_token"
        )

    token_info = verify_refresh_token(refresh_token_value, db)
    success = auth_service.revoke_refresh_token(db, token_info["token_id"])
    if not success:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_400_BAD_REQUEST,
            translation_key="errors.invalid_refresh_token"
        )

    # Clear auth cookies if response is available
    if response:
        clear_auth_cookies(response)

    return {"message": "Successfully logged out"}


@router.get("/google")
async def google_auth(
    redirect_url: str = Query(None),
    locale: str = Depends(get_locale)
):
    """Initiate Google OAuth flow"""
    try:
        auth_url = google_oauth.get_google_auth_url(redirect_url)
        return {"authorization_url": auth_url}
    except Exception as e:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            translation_key="errors.failed_to_generate_oauth_url",
            error=str(e)
        )


@router.get("/google/callback")
async def google_callback(
    code: str,
    state: str = Query(None),
    db: Session = Depends(get_db)
):
    """Handle Google OAuth callback and redirect to frontend"""
    try:
        result = await google_oauth.authenticate_with_google(code, db)

        # Redirect to frontend with tokens in query parameters
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        import urllib.parse
        access_token = urllib.parse.quote(result["access_token"])
        refresh_token = urllib.parse.quote(result.get("refresh_token", ""))

        # Use state (redirect URL) if provided, otherwise redirect to home
        if state:
            decoded_state = urllib.parse.unquote(state)
            if decoded_state.startswith('/'):
                redirect_url = (
                    f"{frontend_url}{decoded_state}"
                    f"?access_token={access_token}"
                    f"&refresh_token={refresh_token}&source=google"
                )
            else:
                redirect_url = (
                    f"{frontend_url}/?access_token={access_token}"
                    f"&refresh_token={refresh_token}&source=google"
                )
        else:
            redirect_url = (
                f"{frontend_url}/?access_token={access_token}"
                f"&refresh_token={refresh_token}&source=google"
            )

        response = RedirectResponse(url=redirect_url)
        set_auth_cookies(
            response=response,
            auth_token=result["access_token"],
            refresh_token=result.get("refresh_token", ""),
            persistent=True,
            secure=False
        )
        return response
    except Exception as e:
        # On error, redirect to frontend with error
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        import urllib.parse
        error_msg = urllib.parse.quote(str(e))

        if state:
            decoded_state = urllib.parse.unquote(state)
            if decoded_state.startswith('/'):
                redirect_url = (
                    f"{frontend_url}{decoded_state}"
                    f"?error={error_msg}&source=google"
                )
            else:
                redirect_url = (
                    f"{frontend_url}/?error={error_msg}&source=google"
                )
        else:
            redirect_url = f"{frontend_url}/?error={error_msg}&source=google"

        return RedirectResponse(url=redirect_url)


@router.post("/register")
async def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Register a new user with email and password."""
    try:
        result = auth_service.register_with_email(db, user_data)

        if "error" in result:
            raise_bad_request(locale, "registration")

        # Return user info and tokens
        return {
            "message": "User registered successfully",
            "user": result.get("user"),
            "tokens": result.get("tokens", {})
        }
    except Exception:
        raise_bad_request(locale, "registration")


@router.post("/forgot-password")
async def forgot_password(
    request: PasswordResetRequest,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Request password reset for a user."""
    try:
        success = auth_service.request_password_reset(db, request.email)

        if not success:
            # For security reasons, don't reveal if email exists or not
            # Just return success message regardless
            pass

        return {
            "message": "If an account with that email exists, "
                       "a password reset link has been sent."
        }
    except Exception:
        # Log the error but don't reveal details to user
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_400_BAD_REQUEST,
            translation_key="errors.failed_to_process_password_reset"
        )


@router.post("/reset-password")
async def reset_password(
    request: PasswordResetConfirm,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Reset password using a valid reset token."""
    try:
        success = auth_service.reset_password(
            db, request.token, request.new_password
        )

        if not success:
            raise_i18n_http_exception(
                locale=locale,
                status_code=status.HTTP_400_BAD_REQUEST,
                translation_key="errors.invalid_or_expired_reset_token"
            )

        return {
            "message": "Password has been reset successfully"
        }
    except Exception:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_400_BAD_REQUEST,
            translation_key="errors.failed_to_reset_password"
        )


@router.get("/github")
async def github_auth(
    redirect_url: str = Query(None),
    authorization: str = Query(None),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Initiate GitHub OAuth flow"""
    client_id = os.getenv("GITHUB_CLIENT_ID")
    scope = "user:email"

    # Validate that we're using a GitHub client ID, not a Google client ID
    if not client_id:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            translation_key="errors.oauth_not_configured",
            provider="GitHub"
        )

    # Check if client_id looks like a Google client ID (common mistake)
    if "apps.googleusercontent.com" in client_id:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            translation_key="errors.configuration_error",
            details=(
                "GitHub client ID appears to be a Google client ID. "
                "Please check your .env file and ensure GITHUB_CLIENT_ID "
                "is set to a valid GitHub OAuth client ID."
            )
        )

    # Build authorization URL with state parameter
    authorization_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={client_id}&scope={scope}"
    )

    # Create state object with redirect_url and user_id
    state_data = {}
    if redirect_url:
        state_data["redirect_url"] = redirect_url

    # Get current user from Authorization header
    if authorization and authorization.startswith("Bearer "):
        try:
            current_user = auth_service.get_current_user(
                db, authorization.replace("Bearer ", "")
            )
            if current_user:
                state_data["user_id"] = current_user.id
        except Exception:
            # If token is invalid, proceed without user ID
            # (normal login/registration)
            pass

    # Add state parameter if we have any state data
    if state_data:
        import json
        import urllib.parse
        state_json = json.dumps(state_data)
        encoded_state = urllib.parse.quote(state_json)
        authorization_url += f"&state={encoded_state}"

    return {"authorization_url": authorization_url}


@router.get("/github/callback")
async def github_callback(
    code: str,
    state: str = Query(None),
    db: Session = Depends(get_db)
):
    """Handle GitHub OAuth callback and redirect to frontend"""
    try:
        # Parse state if provided
        current_user_id = None
        redirect_url_from_state = None

        if state:
            import json
            import urllib.parse
            try:
                decoded_state = urllib.parse.unquote(state)
                state_data = json.loads(decoded_state)

                # Extract redirect_url and user_id from state
                redirect_url_from_state = state_data.get("redirect_url")
                current_user_id = state_data.get("user_id")
            except (json.JSONDecodeError, TypeError):
                # If state is not JSON, treat it as plain redirect URL
                # (backward compatibility)
                redirect_url_from_state = urllib.parse.unquote(state)

        result = await github_oauth.authenticate_with_github(
            code, db, current_user_id)

        # Redirect to frontend with tokens in query parameters
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        import urllib.parse
        access_token = urllib.parse.quote(result["access_token"])
        refresh_token = urllib.parse.quote(result.get("refresh_token", ""))

        # Use redirect URL from state if provided, otherwise redirect to home
        if redirect_url_from_state:
            # Ensure redirect URL is within our frontend domain for security
            if redirect_url_from_state.startswith('/'):
                # It's a path within our frontend
                redirect_url = (
                    f"{frontend_url}{redirect_url_from_state}"
                    f"?access_token={access_token}"
                    f"&refresh_token={refresh_token}&source=github"
                )
            else:
                # Fallback to home if state is malformed
                redirect_url = (
                    f"{frontend_url}/?access_token={access_token}"
                    f"&refresh_token={refresh_token}&source=github"
                )
        else:
            redirect_url = (
                f"{frontend_url}/?access_token={access_token}"
                f"&refresh_token={refresh_token}&source=github"
            )

        response = RedirectResponse(url=redirect_url)
        set_auth_cookies(
            response=response,
            auth_token=result["access_token"],
            refresh_token=result.get("refresh_token", ""),
            persistent=True,
            secure=False
        )
        return response
    except Exception as e:
        # On error, redirect to frontend with error
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        import urllib.parse
        error_msg = urllib.parse.quote(str(e))

        if state:
            decoded_state = urllib.parse.unquote(state)
            if decoded_state.startswith('/'):
                redirect_url = (
                    f"{frontend_url}{decoded_state}"
                    f"?error={error_msg}&source=github"
                )
            else:
                redirect_url = (
                    f"{frontend_url}/?error={error_msg}&source=github"
                )
        else:
            redirect_url = f"{frontend_url}/?error={error_msg}&source=github"

        return RedirectResponse(url=redirect_url)


@router.post("/verify-email")
async def verify_email(
    request: EmailVerificationRequest,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Verify email address using verification token"""
    try:
        from app.services.email_verification_service import (
            EmailVerificationService
        )
        verification_service = EmailVerificationService()
        user = verification_service.verify_email_token(db, request.token)
        return {
            "message": "Email verified successfully",
            "user": user
        }
    except ValueError as ve:
        # Extract error code from ValueError
        error_code = str(ve)
        # Map error codes to translation keys
        if error_code == "invalid_token":
            translation_key = "errors.invalid_token"
        elif error_code == "token_expired":
            translation_key = "errors.token_expired"
        elif error_code == "token_already_used":
            translation_key = "errors.token_already_used"
        else:
            translation_key = "errors.validation_email_verification"
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_400_BAD_REQUEST,
            translation_key=translation_key
        )
    except Exception as e:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            translation_key="errors.email_verification_failed",
            error=str(e)
        )


@router.post("/resend-verification")
async def resend_verification(
    request: EmailResendRequest,
    db: Session = Depends(get_db)
):
    """Resend verification email to user"""
    try:
        from app.services.email_verification_service import (
            EmailVerificationService
        )
        verification_service = EmailVerificationService()
        success = verification_service.resend_verification_email(
            db, request.email
        )
        if success:
            return {
                "message": "Verification email has been resent. "
                           "Please check your inbox."
            }
        else:
            # User not found or already verified
            # Return success anyway to avoid email enumeration
            return {
                "message": "If an account with that email exists "
                           "and is not verified, a verification "
                           "email has been sent."
            }
    except Exception:
        # Still return success to avoid email enumeration
        return {
            "message": "If an account with that email exists "
                       "and is not verified, a verification "
                       "email has been sent."
        }


@router.post("/verify-2fa", response_model=TwoFactorLoginResponse)
async def verify_2fa_login(
    request: TwoFactorLoginVerifyRequest,
    response: Response,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Verify 2FA code after initial login.

    This endpoint is called when a user has entered their email/password
    and 2FA is enabled. It verifies the 2FA code and completes the login.
    """
    try:
        # Use the consolidated auth service for 2FA verification
        auth_result = auth_service.verify_2fa_and_login(
            db,
            temp_token=request.temp_token,
            code=request.code,
            remember_device=request.remember_device
        )
    except ValueError as e:
        error_message = str(e)
        if "Invalid verification code" in error_message:
            raise_unauthorized(locale, "invalid_2fa_code")
        elif "Temporary token has expired" in error_message:
            raise_unauthorized(locale, "temp_token_expired")
        elif "Invalid temporary token" in error_message:
            raise_unauthorized(locale, "invalid_temp_token")
        else:
            raise_unauthorized(locale, "2fa_verification_failed")

    if not auth_result:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_401_UNAUTHORIZED,
            translation_key="errors.2fa_verification_failed",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Extract tokens from auth result
    access_token = auth_result.get("access_token", "")
    refresh_token = auth_result.get("refresh_token", "")

    # Set HTTP-Only cookies for SSR compatibility
    set_auth_cookies(
        response=response,
        auth_token=access_token,
        refresh_token=refresh_token,
        persistent=True,  # Default for 2FA and OAuth
        secure=False  # In development, set to False for local testing
    )

    # Return tokens in JSON response
    return TwoFactorLoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=auth_result.get("token_type", "bearer"),
        user_id=auth_result.get("user", {}).id,
        requires_2fa=False
    )


@router.post("/verify-2fa-backup", response_model=TwoFactorLoginResponse)
async def verify_2fa_backup(
    request: TwoFactorBackupVerifyRequest,
    response: Response,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """
    Verify 2FA backup code after initial login.

    This endpoint is called when a user has entered their email/password
    and 2FA is enabled, but they want to use a backup code instead.
    """
    try:
        # Use the consolidated auth service for backup code verification
        auth_result = auth_service.verify_2fa_backup_code(
            db,
            temp_token=request.temp_token,
            backup_code=request.backup_code
        )
    except ValueError as e:
        error_message = str(e)
        if "Invalid backup code" in error_message:
            raise_unauthorized(locale, "invalid_backup_code")
        elif "Temporary token has expired" in error_message:
            raise_unauthorized(locale, "temp_token_expired")
        elif "Invalid temporary token" in error_message:
            raise_unauthorized(locale, "invalid_temp_token")
        else:
            raise_unauthorized(locale, "backup_code_verification_failed")

    if not auth_result:
        raise_i18n_http_exception(
            locale=locale,
            status_code=status.HTTP_401_UNAUTHORIZED,
            translation_key="errors.backup_code_verification_failed",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Extract tokens from auth result
    access_token = auth_result.get("access_token", "")
    refresh_token = auth_result.get("refresh_token", "")

    # Set HTTP-Only cookies for SSR compatibility
    set_auth_cookies(
        response=response,
        auth_token=access_token,
        refresh_token=refresh_token,
        persistent=True,  # Default for 2FA and OAuth
        secure=False  # In development, set to False for local testing
    )

    # Return tokens in JSON response
    return TwoFactorLoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=auth_result.get("token_type", "bearer"),
        user_id=auth_result.get("user", {}).id,
        requires_2fa=False
    )
