"""
Email verification service for sending and verifying email verification tokens.
"""
import os
import uuid
import logging
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.domain.models.user import EmailVerificationToken, User
from app.services.email_service import EmailService
from app.utils.template_engine import template_engine
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)

# Email verification settings
VERIFICATION_TOKEN_EXPIRE_HOURS = 24
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3001")


class EmailVerificationService:
    """Service for email verification functionality."""

    def __init__(self):
        self.user_repository = UserRepository()
        self.email_service = EmailService()

    def generate_verification_token(self) -> str:
        """Generate a unique verification token."""
        return str(uuid.uuid4())

    def create_verification_token(self, db: Session, user_id: int) -> str:
        """Create and store email verification token."""
        # Generate token
        token = self.generate_verification_token()

        # Set expiration (24 hours)
        expires_at = datetime.utcnow() + timedelta(
            hours=VERIFICATION_TOKEN_EXPIRE_HOURS
        )

        # Store token in database
        db_token = EmailVerificationToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            used=False
        )

        db.add(db_token)
        db.commit()
        db.refresh(db_token)

        return token

    def send_verification_email(
        self,
        user_email: str,
        user_name: str,
        token: str,
        language: str = "en"
    ) -> bool:
        """Send verification email to user using templates."""
        try:
            # Create verification URL
            verification_url = f"{FRONTEND_URL}/verify-email?token={token}"

            # Prepare template variables
            variables = {
                "user_name": user_name,
                "verification_url": verification_url,
                "expiration_hours": VERIFICATION_TOKEN_EXPIRE_HOURS
            }

            # Render email using template engine
            email_content = template_engine.render_email(
                template_name="verification",
                language=language,
                variables=variables
            )

            # Send email
            return self.email_service.send_email(
                to_email=user_email,
                subject=email_content["subject"],
                body=email_content["text"],
                html_body=email_content["html"]
            )
        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")
            return False

    def create_and_send_verification_email(
        self,
        db: Session,
        user_id: int,
        user_email: str,
        user_name: str,
        language: str = "en"
    ) -> bool:
        """Create verification token and send verification email."""
        try:
            # Create verification token
            token = self.create_verification_token(db, user_id)

            # Send verification email
            return self.send_verification_email(
                user_email, user_name, token, language
            )
        except Exception as e:
            logger.error(f"Failed to create and send verification email: {e}")
            return False

    def verify_email_token(self, db: Session, token: str) -> Optional[User]:
        """Verify email verification token."""
        try:
            # Find token in database without filtering by used/expired
            db_token = db.query(EmailVerificationToken).filter(
                EmailVerificationToken.token == token
            ).first()

            if not db_token:
                raise ValueError("invalid_token")

            # Check if token already used
            if db_token.used:
                raise ValueError("token_already_used")

            # Check if token expired
            if db_token.expires_at <= datetime.utcnow():
                raise ValueError("token_expired")

            # Mark token as used
            db_token.used = True
            db.commit()

            # Verify user's email
            user = self.user_repository.get(db, db_token.user_id)
            if not user:
                # Token references a non-existent user (data integrity issue)
                raise ValueError("invalid_token")

            # If user already verified, we still treat as success (no-op)
            if not user.email_verified:
                user.email_verified = True
                user.email_verified_at = datetime.utcnow()
                db.commit()
                db.refresh(user)
            else:
                # User already verified, log but continue
                logger.info(
                    f"User {user.id} already verified, token used"
                )

            return user
        except ValueError:
            # Re-raise ValueError with specific error code
            raise
        except Exception as e:
            logger.error(f"Failed to verify email token: {e}")
            raise ValueError("email_verification_failed")

    def resend_verification_email(
        self,
        db: Session,
        user_email: str,
        language: str = "en"
    ) -> bool:
        """Resend verification email to user."""
        try:
            # Find user by email
            user = self.user_repository.get_by_email(db, user_email)

            if not user:
                logger.warning(f"User not found for email: {user_email}")
                return False

            # Check if email is already verified
            if user.email_verified:
                logger.info(f"Email already verified for user: {user_email}")
                return False

            # Create new verification token
            token = self.create_verification_token(db, user.id)

            # Send verification email
            success = self.send_verification_email(
                user.email,
                user.name or user.username,
                token,
                language
            )

            if success:
                logger.info(f"Verification email resent to: {user_email}")
            else:
                logger.error(
                    f"Failed to resend verification email to: {user_email}"
                )

            return success
        except Exception as e:
            logger.error(f"Failed to resend verification email: {e}")
            return False

    def cleanup_expired_tokens(self, db: Session) -> int:
        """Clean up expired verification tokens."""
        try:
            expired_tokens = db.query(EmailVerificationToken).filter(
                EmailVerificationToken.expires_at <= datetime.utcnow()
            ).all()

            count = len(expired_tokens)
            for token in expired_tokens:
                db.delete(token)

            db.commit()
            logger.info(f"Cleaned up {count} expired verification tokens")
            return count
        except Exception as e:
            logger.error(f"Failed to cleanup expired tokens: {e}")
            return 0

    def get_verification_token(
        self, db: Session, token: str
    ) -> Optional[EmailVerificationToken]:
        """Get a verification token by token string."""
        return db.query(EmailVerificationToken).filter(
            EmailVerificationToken.token == token
        ).first()

    def get_user_verification_tokens(
        self, db: Session, user_id: int
    ) -> list[EmailVerificationToken]:
        """Get all verification tokens for a user."""
        return db.query(EmailVerificationToken).filter(
            EmailVerificationToken.user_id == user_id
        ).all()


# Global service instance
email_verification_service = EmailVerificationService()
