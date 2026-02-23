"""
Email authentication service for user registration,
login, and password management.
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
import bcrypt
import uuid
import os

from app.domain.schemas.user import UserRegister, UserCreate, User
from app.repositories.user_repository import (
    UserRepository, RefreshTokenRepository, PasswordResetTokenRepository
)
from app.core.auth import create_tokens
from app.services.email_service import EmailService
from app.services.email_verification_service import EmailVerificationService
from app.utils.template_engine import template_engine


class EmailAuthService:
    """Service for email-based authentication operations."""

    def __init__(self):
        self.user_repository = UserRepository()
        self.refresh_token_repository = RefreshTokenRepository()
        self.password_reset_repository = PasswordResetTokenRepository()
        self.email_service = EmailService()
        self.email_verification_service = EmailVerificationService()

    @staticmethod
    def _truncate_to_72_bytes(password: str) -> bytes:
        """Truncate password to 72 bytes in UTF-8 safe way."""
        password_bytes = password.encode('utf-8')
        if len(password_bytes) <= 72:
            return password_bytes

        # Take first 72 bytes and remove any incomplete UTF-8 sequence at end
        truncated = password_bytes[:72]
        while truncated:
            try:
                truncated.decode('utf-8')
                return truncated
            except UnicodeDecodeError:
                truncated = truncated[:-1]
        return b''  # Should never happen

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        password_bytes = EmailAuthService._truncate_to_72_bytes(plain_password)

        # Convert hashed_password from string to bytes if needed
        if isinstance(hashed_password, str):
            hashed_password_bytes = hashed_password.encode('utf-8')
        else:
            hashed_password_bytes = hashed_password

        return bcrypt.checkpw(password_bytes, hashed_password_bytes)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password."""
        password_bytes = EmailAuthService._truncate_to_72_bytes(password)

        # Hash password with bcrypt
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')  # Return as string for storage

    @staticmethod
    def validate_email_address(email: str) -> str:
        """Validate email address format and return normalized email."""
        try:
            # Validate email
            valid = validate_email(email, check_deliverability=False)
            # Normalize email
            return valid.email
        except EmailNotValidError:
            raise ValueError("Invalid email address")

    def register_user(
        self,
        db: Session,
        user_data: UserRegister,
        language: str = "en"
    ) -> User:
        """Register a new user with email/password."""
        # Validate email
        normalized_email = self.validate_email_address(user_data.email)

        # Check if user already exists
        existing_user = self.user_repository.get_by_email(db, normalized_email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # Check if username is taken
        existing_username = self.user_repository.get_by_username(
            db, user_data.username)
        if existing_username:
            raise ValueError("Username already taken")

        # Hash password
        password_hash = self.get_password_hash(user_data.password)

        # Create user
        user_create = UserCreate(
            username=user_data.username,
            email=normalized_email,
            name=user_data.username,  # Use username as name
            password_hash=password_hash,
            auth_method="email",
            email_verified=False
        )

        user = self.user_repository.create_from_schema(db, user_create)

        # Create verification token and send email
        self.email_verification_service.create_and_send_verification_email(
            db, user.id, user.email, user.name or user.username, language
        )

        return user

    def login_user(
        self,
        db: Session,
        email: str,
        password: str
    ) -> dict:
        """Authenticate user with email/password."""
        # Find user by email
        user = self.user_repository.get_by_email(db, email)
        if not user:
            raise ValueError("Invalid email or password")

        # Check if user has password hash (email/password user)
        if not user.password_hash:
            raise ValueError("Invalid email or password")

        # Verify password
        if not self.verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        # Check if email is verified
        if not user.email_verified:
            raise ValueError("Email not verified. Please check your email.")

        # Update last login
        self.user_repository.update_last_login(db, user.id)

        # Create tokens
        tokens = create_tokens(user.id, user.username)

        # Store refresh token
        self.refresh_token_repository.create_token(
            db,
            user_id=user.id,
            token_id=tokens["refresh_token_id"],
            expires_at=datetime.utcnow() + tokens["refresh_token_expires"]
        )

        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer",
            "user": user
        }

    def change_password(
        self,
        db: Session,
        user_id: int,
        current_password: str,
        new_password: str
    ) -> bool:
        """Change user password."""
        user = self.user_repository.get(db, user_id)
        if not user or not user.password_hash:
            return False

        # Verify current password
        if not self.verify_password(current_password, user.password_hash):
            return False

        # Hash new password
        new_password_hash = self.get_password_hash(new_password)

        # Update password
        self.user_repository.update_password(db, user_id, new_password_hash)

        # Revoke all refresh tokens (security measure)
        self.refresh_token_repository.revoke_all_for_user(db, user_id)

        return True

    def forgot_password(
        self,
        db: Session,
        email: str,
        language: str = "en"
    ) -> bool:
        """Initiate password reset process by sending reset email."""
        # Find user by email
        user = self.user_repository.get_by_email(db, email)
        if not user:
            # Don't reveal that user doesn't exist (security best practice)
            return True

        # Generate reset token
        token = str(uuid.uuid4())

        # Set expiration (1 hour)
        expires_at = datetime.utcnow() + timedelta(hours=1)

        # Create password reset token in database
        token_data = {
            "user_id": user.id,
            "token": token,
            "expires_at": expires_at,
            "used": False
        }
        self.password_reset_repository.create(db, obj_in=token_data)

        # Get FRONTEND_URL from environment
        FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3001")

        reset_url = f"{FRONTEND_URL}/reset-password?token={token}"

        # Prepare template variables
        variables = {
            "user_name": user.name or user.username,
            "reset_url": reset_url,
            "expiration_hours": 1
        }

        # Render email using template engine
        email_content = template_engine.render_email(
            template_name="password_reset",
            language=language,
            variables=variables
        )

        # Send email
        self.email_service.send_email(
            to_email=user.email,
            subject=email_content["subject"],
            body=email_content["text"],
            html_body=email_content["html"]
        )

        return True

    def reset_password(
        self,
        db: Session,
        token: str,
        new_password: str
    ) -> bool:
        """Reset password using reset token."""
        # Find valid reset token
        reset_token = self.password_reset_repository.get_by_token(db, token)
        if not reset_token or reset_token.used:
            return False

        # Check expiration - use naive UTC for comparison
        now = datetime.utcnow()
        expires_at = reset_token.expires_at

        # If expires_at is aware (has timezone), convert to naive UTC
        if expires_at.tzinfo is not None:
            expires_at = expires_at.replace(tzinfo=None)

        if expires_at < now:
            return False

        # Hash new password
        new_password_hash = self.get_password_hash(new_password)

        # Update user password
        self.user_repository.update_password(
            db, reset_token.user_id, new_password_hash)

        # Mark token as used
        self.password_reset_repository.mark_as_used(db, reset_token.id)

        # Revoke all refresh tokens (security measure)
        self.refresh_token_repository.revoke_all_for_user(
            db, reset_token.user_id)

        return True


# Global email auth service instance
email_auth = EmailAuthService()