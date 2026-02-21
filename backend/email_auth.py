from datetime import datetime
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
import bcrypt

import crud
import schemas
import auth
from email_verification import (
    send_verification_email, create_verification_token
)
from template_engine import template_engine


def _truncate_to_72_bytes(password: str) -> bytes:
    """Truncate password to 72 bytes in UTF-8 safe way"""
    password_bytes = password.encode('utf-8')
    if len(password_bytes) <= 72:
        return password_bytes

    # Take first 72 bytes and remove any incomplete UTF-8 sequence at the end
    truncated = password_bytes[:72]
    while truncated:
        try:
            truncated.decode('utf-8')
            return truncated
        except UnicodeDecodeError:
            truncated = truncated[:-1]
    return b''  # Should never happen


def verify_password(plain_password: str, hashed_password: str):
    """Verify a password against its hash"""
    password_bytes = _truncate_to_72_bytes(plain_password)

    # Convert hashed_password from string to bytes if needed
    if isinstance(hashed_password, str):
        hashed_password_bytes = hashed_password.encode('utf-8')
    else:
        hashed_password_bytes = hashed_password

    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


def get_password_hash(password: str):
    """Hash a password"""
    password_bytes = _truncate_to_72_bytes(password)

    # Hash password with bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')  # Return as string for storage


def validate_email_address(email: str):
    """Validate email address format"""
    try:
        # Validate email
        valid = validate_email(email)
        # Normalize email
        return valid.email
    except EmailNotValidError:
        raise ValueError("Invalid email address")


def register_user(
    db: Session,
    user_data: schemas.UserRegister,
    language: str = "en"
):
    """Register a new user with email/password"""
    # Validate email
    normalized_email = validate_email_address(user_data.email)
    if not normalized_email:
        raise ValueError("Invalid email address")

    # Check if user already exists
    existing_user = crud.get_user_by_email(db, normalized_email)
    if existing_user:
        raise ValueError("User with this email already exists")

    # Check if username is taken
    existing_username = crud.get_user_by_username(db, user_data.username)
    if existing_username:
        raise ValueError("Username already taken")

    # Hash password
    password_hash = get_password_hash(user_data.password)

    # Create user
    user_create = schemas.UserCreate(
        username=user_data.username,
        email=normalized_email,
        name=user_data.name or user_data.username,
        password_hash=password_hash,
        auth_method="email",
        email_verified=False
    )

    user = crud.create_user(db, user_create)

    # Create verification token
    token = create_verification_token(db, user.id)

    # Send verification email
    send_verification_email(
        user.email,
        user.name or user.username,
        token,
        language
    )

    return user


def login_user(db: Session, email: str, password: str):
    """Authenticate user with email/password"""
    # Find user by email
    user = crud.get_user_by_email(db, email)
    if not user:
        raise ValueError("Invalid email or password")

    # Check if user has password hash (email/password user)
    if not user.password_hash:
        raise ValueError("Invalid email or password")

    # Verify password
    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password")

    # Check if email is verified
    if not user.email_verified:
        raise ValueError("Email not verified. Please check your email.")

    # Update last login
    crud.update_user_last_login(db, user.id)

    # Create tokens
    tokens = auth.create_tokens(user.id, user.username)

    # Store refresh token
    crud.create_refresh_token(
        db,
        user_id=user.id,
        token_id=tokens["refresh_token_id"],
        expires_at=datetime.utcnow() + tokens["refresh_token_expires"]
    )

    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer",
        "user": schemas.User.from_orm(user)
    }


def change_password(db: Session, user_id: int,
                    current_password: str, new_password: str):
    """Change user password"""
    user = crud.get_user(db, user_id)
    if not user or not user.password_hash:
        return False

    # Verify current password
    if not verify_password(current_password, user.password_hash):
        return False

    # Hash new password
    new_password_hash = get_password_hash(new_password)

    # Update password
    crud.update_user_password(db, user_id, new_password_hash)

    # Revoke all refresh tokens (security measure)
    crud.revoke_all_user_refresh_tokens(db, user_id)

    return True


def forgot_password(
    db: Session,
    email: str,
    language: str = "en"
):
    """Initiate password reset process by sending reset email"""
    # Find user by email
    user = crud.get_user_by_email(db, email)
    if not user:
        # Don't reveal that user doesn't exist (security best practice)
        return True

    # Generate reset token
    import uuid
    token = str(uuid.uuid4())
    
    # Set expiration (1 hour)
    from datetime import timedelta
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    # Create password reset token in database
    crud.create_password_reset_token(db, user.id, token, expires_at)
    
    # Get FRONTEND_URL from environment
    import os
    from dotenv import load_dotenv
    load_dotenv()
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
    from email_service import EmailService
    email_service = EmailService()
    email_service.send_email(
        to_email=user.email,
        subject=email_content["subject"],
        body=email_content["text"],
        html_body=email_content["html"]
    )
    
    return True


def reset_password(db: Session, token: str, new_password: str):
    """Reset password using reset token"""
    # Find valid reset token
    reset_token = crud.get_password_reset_token(db, token)
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
    new_password_hash = get_password_hash(new_password)

    # Update user password
    crud.update_user_password(db, reset_token.user_id, new_password_hash)

    # Mark token as used
    crud.mark_password_reset_token_used(db, reset_token.id)

    # Revoke all refresh tokens (security measure)
    crud.revoke_all_user_refresh_tokens(db, reset_token.user_id)

    return True
