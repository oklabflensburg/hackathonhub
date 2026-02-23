"""
Authentication API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os

from app.core.database import get_db
from app.domain.schemas.user import (
    TokenWithRefresh, UserRegister, UserLogin, EmailResendRequest
)
from app.core.auth import refresh_tokens, verify_refresh_token
from app.services.auth_service import auth_service
from app.services.google_oauth_service import google_oauth
from app.services.github_oauth_service import github_oauth

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/login", response_model=TokenWithRefresh)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login endpoint that accepts JSON.
    
    JSON format: {"email": "...", "password": "..."}
    """
    try:
        # Use the consolidated auth service for email/password authentication
        auth_result = auth_service.login_with_email(
            db, email=login_data.email, password=login_data.password
        )
    except ValueError as e:
        # Convert ValueError from auth service to HTTPException
        error_message = str(e)
        if "Email not verified" in error_message:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_message,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_message,
                headers={"WWW-Authenticate": "Bearer"},
            )

    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract tokens from auth result
    tokens = auth_result.get("tokens", {})

    return TokenWithRefresh(
        access_token=tokens.get("access_token", ""),
        refresh_token=tokens.get("refresh_token", ""),
        token_type="bearer"
    )


@router.post("/login/json", response_model=TokenWithRefresh)
async def login_json(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    JSON-based login endpoint (alias for /login).
    
    Accepts email and password in JSON format.
    """
    try:
        # Use the consolidated auth service for email/password authentication
        auth_result = auth_service.login_with_email(
            db, email=login_data.email, password=login_data.password
        )
    except ValueError as e:
        # Convert ValueError from auth service to HTTPException
        error_message = str(e)
        if "Email not verified" in error_message:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_message,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_message,
                headers={"WWW-Authenticate": "Bearer"},
            )

    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract tokens from auth result
    tokens = auth_result.get("tokens", {})

    return TokenWithRefresh(
        access_token=tokens.get("access_token", ""),
        refresh_token=tokens.get("refresh_token", ""),
        token_type="bearer"
    )


@router.post("/refresh", response_model=TokenWithRefresh)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using a valid refresh token.
    """
    token_data = refresh_tokens(refresh_token, db)
    return TokenWithRefresh(
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        token_type=token_data["token_type"]
    )


@router.post("/logout")
async def logout(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Logout by revoking a refresh token.
    """
    token_info = verify_refresh_token(refresh_token, db)
    success = auth_service.revoke_refresh_token(db, token_info["token_id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token"
        )

    return {"message": "Successfully logged out"}


@router.get("/google")
async def google_auth(redirect_url: str = Query(None)):
    """Initiate Google OAuth flow"""
    try:
        auth_url = google_oauth.get_google_auth_url(redirect_url)
        return {"authorization_url": auth_url}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate Google OAuth URL: {str(e)}"
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

        # Redirect to frontend with token in query parameter
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        import urllib.parse
        token = urllib.parse.quote(result["access_token"])

        # Use state (redirect URL) if provided, otherwise redirect to home
        if state:
            decoded_state = urllib.parse.unquote(state)
            if decoded_state.startswith('/'):
                redirect_url = (
                    f"{frontend_url}{decoded_state}"
                    f"?token={token}&source=google"
                )
            else:
                redirect_url = f"{frontend_url}/?token={token}&source=google"
        else:
            redirect_url = f"{frontend_url}/?token={token}&source=google"

        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=redirect_url)
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

        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=redirect_url)


@router.post("/register")
async def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user with email and password."""
    try:
        result = auth_service.register_with_email(db, user_data)

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )

        # Return user info and tokens
        return {
            "message": "User registered successfully",
            "user": result.get("user"),
            "tokens": result.get("tokens", {})
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/forgot-password")
async def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):
    """Request password reset for a user."""
    try:
        success = auth_service.request_password_reset(db, email)

        if not success:
            # For security reasons, don't reveal if email exists or not
            # Just return success message regardless
            pass

        return {
            "message": "If an account with that email exists, a password reset link has been sent."
        }
    except Exception as e:
        # Log the error but don't reveal details to user
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to process password reset request"
        )


@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """Reset password using a valid reset token."""
    try:
        success = auth_service.reset_password(db, token, new_password)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        return {
            "message": "Password has been reset successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to reset password"
        )


@router.get("/github")
async def github_auth(
    redirect_url: str = Query(None),
    authorization: str = Query(None),
    db: Session = Depends(get_db)
):
    """Initiate GitHub OAuth flow"""
    client_id = os.getenv("GITHUB_CLIENT_ID")
    scope = "user:email"

    # Validate that we're using a GitHub client ID, not a Google client ID
    if not client_id:
        raise HTTPException(
            status_code=500,
            detail="GitHub OAuth is not configured. Please set GITHUB_CLIENT_ID in .env file."
        )

    # Check if client_id looks like a Google client ID (common mistake)
    if "apps.googleusercontent.com" in client_id:
        raise HTTPException(
            status_code=500,
            detail="Configuration error: GitHub client ID appears to be a Google client ID. "
                   "Please check your .env file and ensure GITHUB_CLIENT_ID is set to a "
                   "valid GitHub OAuth client ID."
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
            from app.core.auth import get_current_user
            token = authorization.replace("Bearer ", "")
            current_user = await get_current_user(token, db)
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

        # Redirect to frontend with token in query parameter
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        import urllib.parse
        token = urllib.parse.quote(result["access_token"])

        # Use redirect URL from state if provided, otherwise redirect to home
        if redirect_url_from_state:
            # Ensure redirect URL is within our frontend domain for security
            if redirect_url_from_state.startswith('/'):
                # It's a path within our frontend
                redirect_url = (
                    f"{frontend_url}{redirect_url_from_state}"
                    f"?token={token}&source=github"
                )
            else:
                # Fallback to home if state is malformed
                redirect_url = f"{frontend_url}/?token={token}&source=github"
        else:
            redirect_url = f"{frontend_url}/?token={token}&source=github"

        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=redirect_url)
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

        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=redirect_url)


@router.post("/verify-email")
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """Verify email address using verification token"""
    try:
        from app.services.email_verification_service import verify_email_token
        user = verify_email_token(db, token)
        return {
            "message": "Email verified successfully",
            "user": user
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Email verification failed: {str(e)}"
        )


@router.post("/resend-verification")
async def resend_verification(
    request: EmailResendRequest,
    db: Session = Depends(get_db)
):
    """Resend verification email to user"""
    try:
        from app.services.email_verification_service import (
            resend_verification_email
        )
        success = resend_verification_email(db, request.email)
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
