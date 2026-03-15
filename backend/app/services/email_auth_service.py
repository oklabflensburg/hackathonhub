"""
Email authentication service for user registration,
login, and password management.
"""
import base64
import json
import logging
import os
import uuid
from datetime import datetime, timedelta

import bcrypt
from email_validator import EmailNotValidError, validate_email
from sqlalchemy.orm import Session

from app.core.auth import create_tokens
from app.domain.schemas.user import User, UserCreate, UserRegister
from app.repositories.user_repository import (
    PasswordResetTokenRepository,
    RefreshTokenRepository,
    UserRepository,
)
from app.services.email_orchestrator import EmailContext, EmailOrchestrator
from app.services.email_verification_service import EmailVerificationService

logger = logging.getLogger(__name__)


class EmailAuthService:
    """Service for email-based authentication operations."""

    def __init__(self):
        self.user_repository = UserRepository()
        self.refresh_token_repository = RefreshTokenRepository()
        self.password_reset_repository = PasswordResetTokenRepository()
        self.email_orchestrator = EmailOrchestrator()
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
        password: str,
        remember_me: bool = False
    ) -> dict:
        """Authenticate user with email/password."""
        # Find user by email
        user = self.user_repository.get_by_email(db, email)
        if not user:
            raise ValueError("Invalid email or password")
        if getattr(user, "is_active", True) is False:
            raise ValueError("Account is deactivated")

        # Check if user has password hash (email/password user)
        if not user.password_hash:
            raise ValueError("Invalid email or password")

        # Verify password
        if not self.verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        # Check if email is verified
        if not user.email_verified:
            raise ValueError("Email not verified. Please check your email.")

        # Check if 2FA is enabled
        if user.two_factor_enabled:
            # Create temporary token for 2FA verification
            # Create temporary token data
            expires_at = datetime.utcnow() + timedelta(minutes=10)
            temp_token_data = {
                "user_id": user.id,
                "email": user.email,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": expires_at.isoformat(),
                "purpose": "2fa_verification"
            }

            # Encode token data
            token_json = json.dumps(temp_token_data)
            temp_token = base64.urlsafe_b64encode(
                token_json.encode()
            ).decode()

            # Return partial authentication response
            # Frontend should prompt for 2FA code
            return {
                "requires_2fa": True,
                "user_id": user.id,
                "temp_token": temp_token,
                "message": "Two-factor authentication required"
            }

        # Update last login
        self.user_repository.update_last_login(db, user.id)

        # Create tokens with remember_me parameter
        tokens = create_tokens(user.id, user.username, remember_me)

        # Store refresh token with is_persistent flag
        self.refresh_token_repository.create_token(
            db,
            user_id=user.id,
            token_id=tokens["refresh_token_id"],
            expires_at=datetime.utcnow() + tokens["refresh_token_expires"],
            is_persistent=remember_me
        )

        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer",
            "user": user,
            "requires_2fa": False
        }

    def _decode_temp_token(self, temp_token: str) -> dict:
        """Decode and validate temporary token for 2FA verification."""
        import json
        import base64
        from datetime import datetime

        try:
            # Decode token
            token_json = base64.urlsafe_b64decode(temp_token).decode()
            token_data = json.loads(token_json)

            # Check expiration
            expires_at = datetime.fromisoformat(token_data["expires_at"])
            if datetime.utcnow() > expires_at:
                raise ValueError("Temporary token has expired")

            # Validate required fields
            required_fields = ["user_id", "email", "purpose"]
            for field in required_fields:
                if field not in token_data:
                    raise ValueError(f"Missing required field: {field}")

            if token_data["purpose"] != "2fa_verification":
                raise ValueError("Invalid token purpose")

            return token_data
        except (json.JSONDecodeError, base64.binascii.Error, KeyError) as e:
            raise ValueError(f"Invalid temporary token: {str(e)}")

    def verify_2fa_and_login(
        self,
        db: Session,
        temp_token: str,
        code: str,
        remember_device: bool = False
    ) -> dict:
        """Verify 2FA code using temporary token and complete login."""
        # Decode and validate temporary token
        token_data = self._decode_temp_token(temp_token)
        user_id = token_data["user_id"]

        user = self.user_repository.get(db, user_id)
        if not user:
            raise ValueError("User not found")

        if not user.two_factor_enabled or not user.two_factor_secret:
            raise ValueError("Two-factor authentication not enabled")

        # Import pyotp here to avoid dependency if not using 2FA
        import pyotp

        # Verify TOTP code
        totp = pyotp.TOTP(user.two_factor_secret)
        if not totp.verify(code):
            raise ValueError("Invalid verification code")

        # Update last login
        self.user_repository.update_last_login(db, user.id)

        # Create tokens
        from app.core.auth import create_tokens
        tokens = create_tokens(user.id, user.username)

        # Store refresh token
        self.refresh_token_repository.create_token(
            db,
            user_id=user.id,
            token_id=tokens["refresh_token_id"],
            expires_at=datetime.utcnow() + tokens["refresh_token_expires"]
        )

        # If remember device is enabled, create a device cookie
        if remember_device:
            # Create device token for 30 days
            import secrets
            device_token = secrets.token_urlsafe(32)
            # Store device token in user settings or separate table
            # For now, we'll just return it
            device_data = {
                "device_token": device_token,
                "expires_in_days": 30
            }
        else:
            device_data = None

        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer",
            "user": user,
            "device_data": device_data
        }

    def verify_2fa_backup_code(
        self,
        db: Session,
        temp_token: str,
        backup_code: str
    ) -> dict:
        """Verify 2FA backup code using temporary token and complete login."""
        # Decode and validate temporary token
        token_data = self._decode_temp_token(temp_token)
        user_id = token_data["user_id"]

        user = self.user_repository.get(db, user_id)
        if not user:
            raise ValueError("User not found")

        if not user.two_factor_enabled:
            raise ValueError("Two-factor authentication not enabled")

        # Check backup codes (assuming they're stored as JSON string)
        import json
        backup_codes = []
        if user.two_factor_backup_codes:
            try:
                backup_codes = json.loads(user.two_factor_backup_codes)
            except json.JSONDecodeError:
                backup_codes = []

        # Verify backup code
        if backup_code not in backup_codes:
            raise ValueError("Invalid backup code")

        # Remove used backup code
        backup_codes.remove(backup_code)
        user.two_factor_backup_codes = json.dumps(backup_codes)
        db.commit()

        # Update last login
        self.user_repository.update_last_login(db, user.id)

        # Create tokens
        from app.core.auth import create_tokens
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
            "user": user,
            "remaining_backup_codes": len(backup_codes)
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

        # Send password change notification email (fire and forget)
        try:
            if user and user.email:
                variables = {
                    "user_name": user.name or user.username,
                    "change_date": datetime.utcnow().isoformat()
                }
                context = EmailContext(
                    user_id=user_id,
                    user_email=user.email,
                    language="en",  # TODO: Get user's preferred language
                    category="security"
                )
                result = self.email_orchestrator.send_template(
                    db=db,
                    template_name="password_changed",
                    context=context,
                    variables=variables
                )
                if not result.success:
                    logger.warning(
                        f"Failed to send password change notification: "
                        f"{result.error}"
                    )
        except Exception as e:
            # Log but don't fail password change
            logger.warning(f"Failed to send password change notification: {e}")

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

        # Create email context
        context = EmailContext(
            user_id=user.id,
            user_email=user.email,
            language=language,
            category="password_reset"
        )

        # Send email using orchestrator
        result = self.email_orchestrator.send_template(
            db=db,
            template_name="password_reset",
            context=context,
            variables=variables
        )

        # Log result
        if not result.success:
            logger.error(
                f"Failed to send password reset email: {result.error}"
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

        # Send password reset confirmation email (fire and forget)
        try:
            user = self.user_repository.get(db, reset_token.user_id)
            if user and user.email:
                variables = {
                    "user_name": user.name or user.username,
                    "reset_date": datetime.utcnow().isoformat()
                }
                context = EmailContext(
                    user_id=reset_token.user_id,
                    user_email=user.email,
                    language="en",  # TODO: Get user's preferred language
                    category="security"
                )
                result = self.email_orchestrator.send_template(
                    db=db,
                    template_name="password_reset_confirmed",
                    context=context,
                    variables=variables
                )
                if not result.success:
                    logger.warning(
                        f"Failed to send password reset confirmation: "
                        f"{result.error}"
                    )
        except Exception as e:
            # Log but don't fail password reset
            logger.warning(f"Failed to send password reset confirmation: {e}")

        return True


# Global email auth service instance
email_auth = EmailAuthService()
