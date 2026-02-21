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


def forgot_password(db: Session, email: str):
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
    
    # Send password reset email
    from email_service import EmailService
    from email_verification import FRONTEND_URL
    
    reset_url = f"{FRONTEND_URL}/reset-password?token={token}"
    
    subject = "Reset Your Password - Hackathon Dashboard"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reset Your Password</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                padding: 30px;
                border-radius: 10px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .logo {{
                font-size: 24px;
                font-weight: bold;
                color: #4F46E5;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #4F46E5;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                font-size: 12px;
                color: #666;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">Hackathon Dashboard</div>
                <h1>Reset Your Password</h1>
            </div>
            
            <p>Hello {user.name or user.username},</p>
            
            <p>We received a request to reset your password for your
            Hackathon Dashboard account. If you made this request,
            please click the button below to reset your password:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" class="button">Reset Password</a>
            </div>
            
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; background-color: #f0f0f0;
               padding: 10px; border-radius: 5px; font-size: 12px;">
                {reset_url}
            </p>
            
            <p>This password reset link will expire in 1 hour.</p>
            
            <p>If you didn't request a password reset, you can safely
            ignore this email. Your password will not be changed.</p>
            
            <div class="footer">
                <p>This email was sent by Hackathon Dashboard</p>
                <p>© {datetime.now().year} Hackathon Dashboard.
                All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Reset Your Password - Hackathon Dashboard
    
    Hello {user.name or user.username},
    
    We received a request to reset your password for your
    Hackathon Dashboard account. If you made this request,
    please click the link below to reset your password:
    
    {reset_url}
    
    This password reset link will expire in 1 hour.
    
    If you didn't request a password reset, you can safely
    ignore this email. Your password will not be changed.
    
    © {datetime.now().year} Hackathon Dashboard. All rights reserved.
    """
    
    # Send email
    email_service = EmailService()
    email_service.send_email(
        to_email=user.email,
        subject=subject,
        body=text_content,
        html_body=html_content
    )
    
    return True


def reset_password(db: Session, token: str, new_password: str):
    """Reset password using reset token"""
    # Find valid reset token
    reset_token = crud.get_password_reset_token(db, token)
    if (not reset_token or reset_token.used or 
            reset_token.expires_at < datetime.utcnow()):
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
