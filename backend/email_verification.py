import os
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import crud
import models
from email_service import EmailService

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


def send_verification_email(user_email: str, user_name: str, token: str):
    """Send verification email to user"""
    # Create verification URL
    verification_url = f"{FRONTEND_URL}/verify-email?token={token}"
    
    # Email content
    subject = "Verify Your Email Address - Hackathon Dashboard"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verify Your Email</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
            .container {{ background-color: #f9f9f9; padding: 30px; border-radius: 10px; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .logo {{ font-size: 24px; font-weight: bold; color: #4F46E5; }}
            .button {{ display: inline-block; padding: 12px 24px; background-color: #4F46E5; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">Hackathon Dashboard</div>
                <h1>Verify Your Email Address</h1>
            </div>
            
            <p>Hello {user_name},</p>
            
            <p>Thank you for registering with Hackathon Dashboard! To complete your registration and start using your account, please verify your email address by clicking the button below:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_url}" class="button">Verify Email Address</a>
            </div>
            
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; background-color: #f0f0f0; padding: 10px; border-radius: 5px; font-size: 12px;">
                {verification_url}
            </p>
            
            <p>This verification link will expire in 24 hours.</p>
            
            <p>If you didn't create an account with Hackathon Dashboard, you can safely ignore this email.</p>
            
            <div class="footer">
                <p>This email was sent by Hackathon Dashboard</p>
                <p>© {datetime.now().year} Hackathon Dashboard. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Verify Your Email Address - Hackathon Dashboard
    
    Hello {user_name},
    
    Thank you for registering with Hackathon Dashboard! To complete your registration and start using your account, please verify your email address by clicking the link below:
    
    {verification_url}
    
    This verification link will expire in 24 hours.
    
    If you didn't create an account with Hackathon Dashboard, you can safely ignore this email.
    
    © {datetime.now().year} Hackathon Dashboard. All rights reserved.
    """
    
    # Send email
    email_service = EmailService()
    email_service.send_email(
        to_email=user_email,
        subject=subject,
        html_content=html_content,
        text_content=text_content
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


def resend_verification_email(db: Session, user_email: str):
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
    send_verification_email(user.email, user.name or user.username, token)
    
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