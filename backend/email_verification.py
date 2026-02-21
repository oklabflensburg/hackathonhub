import os
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import crud
import models
from email_service import EmailService
from template_engine import template_engine

load_dotenv()

# Email verification settings
VERIFICATION_TOKEN_EXPIRE_HOURS = 24
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3001")


def generate_verification_token():
    """Generate a unique verification token"""
    return str(uuid.uuid4())


def create_verification_token(db: Session, user_id: int):
    """Create and store email verification token"""
    # Generate token
    token = generate_verification_token()

    # Set expiration (24 hours)
    expires_at = datetime.utcnow() + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)

    # Store token in database
    db_token = models.EmailVerificationToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )

    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return token


def send_verification_email(
    user_email: str,
    user_name: str,
    token: str,
    language: str = "en"
):
    """Send verification email to user using templates."""
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
    email_service = EmailService()
    email_service.send_email(
        to_email=user_email,
        subject=email_content["subject"],
        body=email_content["text"],
        html_body=email_content["html"]
    )


def verify_email_token(db: Session, token: str):
    """Verify email verification token"""
    # Find token in database
    db_token = db.query(models.EmailVerificationToken).filter(
        models.EmailVerificationToken.token == token,
        models.EmailVerificationToken.used.is_(False),
        models.EmailVerificationToken.expires_at > datetime.utcnow()
    ).first()

    if not db_token:
        return None

    # Mark token as used
    db_token.used = True
    db.commit()

    # Verify user's email
    user = crud.verify_user_email(db, db_token.user_id)

    return user


def resend_verification_email(
    db: Session,
    user_email: str,
    language: str = "en"
):
    """Resend verification email to user"""
    # Find user by email
    user = crud.get_user_by_email(db, user_email)

    if not user:
        return False

    # Check if email is already verified
    if user.email_verified:
        return False

    # Create new verification token
    token = create_verification_token(db, user.id)

    # Send verification email
    send_verification_email(
        user.email,
        user.name or user.username,
        token,
        language
    )

    return True


def cleanup_expired_tokens(db: Session):
    """Clean up expired verification tokens"""
    expired_tokens = db.query(models.EmailVerificationToken).filter(
        models.EmailVerificationToken.expires_at <= datetime.utcnow()
    ).all()

    for token in expired_tokens:
        db.delete(token)

    db.commit()

    return len(expired_tokens)
