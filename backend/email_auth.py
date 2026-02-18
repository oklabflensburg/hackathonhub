import os
from datetime import datetime
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from email_validator import validate_email, EmailNotValidError

import crud
import schemas
import auth
from email_verification import send_verification_email, create_verification_token

# Password hashing
# Configure bcrypt to truncate passwords longer than 72 bytes
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=True  # This might help with long passwords
)


def verify_password(plain_password: str, hashed_password: str):
    """Verify a password against its hash"""
    # bcrypt has a 72-byte limit
    # Always truncate to 72 bytes in a UTF-8 safe way
    # (same as get_password_hash)
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes, but ensure we don't cut in
        # middle of multi-byte char
        # Find the last valid UTF-8 boundary
        for i in range(72, 0, -1):
            try:
                truncated = password_bytes[:i].decode('utf-8')
                break
            except UnicodeDecodeError:
                continue
        else:
            # If we can't decode any prefix, use empty string
            # (shouldn't happen)
            truncated = ""
        return pwd_context.verify(truncated, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """Hash a password"""
    # bcrypt has a 72-byte limit
    # Always truncate to 72 bytes in a UTF-8 safe way
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes, but ensure we don't cut in
        # middle of multi-byte char
        # Find the last valid UTF-8 boundary
        for i in range(72, 0, -1):
            try:
                truncated = password_bytes[:i].decode('utf-8')
                break
            except UnicodeDecodeError:
                continue
        else:
            # If we can't decode any prefix, use empty string
            # (shouldn't happen)
            truncated = ""
        return pwd_context.hash(truncated)
    return pwd_context.hash(password)


def validate_email_address(email: str):
    """Validate email address format"""
    try:
        # Validate email
        valid = validate_email(email)
        # Normalize email
        return valid.email
    except EmailNotValidError:
        return None


def register_user(db: Session, user_data: schemas.UserRegister):
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
        token
    )
    
    return user


def login_user(db: Session, email: str, password: str):
    """Authenticate user with email/password"""
    # Find user by email
    user = crud.get_user_by_email(db, email)
    if not user:
        return None
    
    # Check if user has password hash (email/password user)
    if not user.password_hash:
        return None
    
    # Verify password
    if not verify_password(password, user.password_hash):
        return None
    
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


def change_password(db: Session, user_id: int, current_password: str, new_password: str):
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


def reset_password(db: Session, token: str, new_password: str):
    """Reset password using reset token"""
    # Find valid reset token
    reset_token = crud.get_password_reset_token(db, token)
    if not reset_token or reset_token.used or reset_token.expires_at < datetime.utcnow():
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