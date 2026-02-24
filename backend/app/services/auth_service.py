"""
Consolidated authentication service facade.

This service provides a unified interface for all authentication methods:
- Email/password authentication
- GitHub OAuth
- Google OAuth
- Token management
- User session management
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.domain.schemas.user import User, UserRegister
from app.services.email_auth_service import EmailAuthService
from app.services.github_oauth_service import GitHubOAuthService
from app.services.google_oauth_service import GoogleOAuthService
from app.services.user_service import AuthService as TokenAuthService


class AuthService:
    """
    Facade service that consolidates all authentication methods.

    This provides a single entry point for authentication operations,
    abstracting away the details of different authentication providers.
    """

    def __init__(self):
        self.email_auth_service = EmailAuthService()
        self.github_auth_service = GitHubOAuthService()
        self.google_auth_service = GoogleOAuthService()
        self.token_auth_service = TokenAuthService()

    # Email Authentication Methods

    def register_with_email(
        self, db: Session, user_data: UserRegister
    ) -> Dict[str, Any]:
        """
        Register a new user with email and password.

        Args:
            db: Database session
            user_data: User registration data

        Returns:
            Dictionary with user and token information
        """
        user = self.email_auth_service.register_user(db, user_data)

        # Create tokens for the newly registered user
        from app.core.auth import create_tokens
        tokens = create_tokens(user.id, user.username)

        return {
            "user": user,
            "tokens": tokens
        }

    def login_with_email(
        self, db: Session, email: str, password: str
    ) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with email and password.

        Args:
            db: Database session
            email: User email
            password: Plain text password

        Returns:
            Dictionary with user and token information,
            or None if authentication fails
        """
        return self.email_auth_service.login_user(db, email, password)

    def verify_email_token(self, db: Session, token: str) -> Optional[User]:
        """
        Verify email using verification token.

        Args:
            db: Database session
            token: Email verification token

        Returns:
            Verified user or None if token is invalid
        """
        from app.services.email_verification_service import (
            EmailVerificationService
        )
        verification_service = EmailVerificationService()
        return verification_service.verify_email_token(db, token)

    def request_password_reset(self, db: Session, email: str) -> bool:
        """
        Request password reset for a user.

        Args:
            db: Database session
            email: User email

        Returns:
            True if reset email was sent, False otherwise
        """
        return self.email_auth_service.request_password_reset(db, email)

    def reset_password(
        self, db: Session, token: str, new_password: str
    ) -> Optional[User]:
        """
        Reset user password using reset token.

        Args:
            db: Database session
            token: Password reset token
            new_password: New password

        Returns:
            User with updated password or None if token is invalid
        """
        return self.email_auth_service.reset_password(db, token, new_password)

    # OAuth Authentication Methods

    def get_github_authorization_url(self) -> str:
        """
        Get GitHub OAuth authorization URL.

        Returns:
            Authorization URL for GitHub OAuth
        """
        return self.github_auth_service.get_authorization_url()

    def authenticate_with_github(
        self, db: Session, code: str
    ) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with GitHub OAuth.

        Args:
            db: Database session
            code: GitHub OAuth authorization code

        Returns:
            Dictionary with user and token information,
            or None if authentication fails
        """
        return self.github_auth_service.authenticate(db, code)

    def get_google_authorization_url(self) -> str:
        """
        Get Google OAuth authorization URL.

        Returns:
            Authorization URL for Google OAuth
        """
        return self.google_auth_service.get_authorization_url()

    def authenticate_with_google(
        self, db: Session, code: str
    ) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with Google OAuth.

        Args:
            db: Database session
            code: Google OAuth authorization code

        Returns:
            Dictionary with user and token information,
            or None if authentication fails
        """
        return self.google_auth_service.authenticate(db, code)

    # Token Management Methods

    def create_refresh_token(
        self, db: Session, user_id: int, token_id: str,
        device_info: str = None, ip_address: str = None
    ) -> bool:
        """
        Create a refresh token for a user.

        Args:
            db: Database session
            user_id: User ID
            token_id: Token identifier
            device_info: Optional device information
            ip_address: Optional IP address

        Returns:
            True if token was created successfully
        """
        return self.token_auth_service.create_refresh_token(
            db, user_id, token_id, device_info, ip_address
        )

    def revoke_refresh_token(self, db: Session, token_id: str) -> bool:
        """
        Revoke a refresh token.

        Args:
            db: Database session
            token_id: Token identifier

        Returns:
            True if token was revoked successfully
        """
        return self.token_auth_service.revoke_refresh_token(db, token_id)

    def revoke_all_user_tokens(self, db: Session, user_id: int) -> int:
        """
        Revoke all refresh tokens for a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Number of tokens revoked
        """
        return self.token_auth_service.revoke_all_user_tokens(db, user_id)

    # User Session Methods

    def get_current_user(self, db: Session, token: str) -> Optional[User]:
        """
        Get current user from access token.

        Args:
            db: Database session
            token: JWT access token

        Returns:
            User object or None if token is invalid
        """
        from app.core.auth import get_current_user_from_token
        return get_current_user_from_token(db, token)

    def update_last_login(self, db: Session, user_id: int) -> Optional[User]:
        """
        Update user's last login timestamp.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Updated user or None if user not found
        """
        from app.services.user_service import user_service
        return user_service.update_last_login(db, user_id)


# Create singleton instance for dependency injection
auth_service = AuthService()
