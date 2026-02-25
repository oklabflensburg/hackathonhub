"""
User repository for user-related database operations.
"""
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.domain.models.user import (
    User, RefreshToken, PasswordResetToken, EmailVerificationToken
)
from app.domain.schemas.user import UserCreate, UserUpdate
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model operations."""

    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get a user by email address."""
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get a user by username."""
        return db.query(User).filter(User.username == username).first()

    def get_by_github_id(self, db: Session, github_id: int) -> Optional[User]:
        """Get a user by GitHub ID."""
        return db.query(User).filter(User.github_id == github_id).first()

    def get_by_google_id(self, db: Session, google_id: str) -> Optional[User]:
        """Get a user by Google ID."""
        return db.query(User).filter(User.google_id == google_id).first()

    def search_by_username(
        self, db: Session, username_query: str, limit: int = 10
    ) -> List[User]:
        """Search users by username (case-insensitive partial match)."""
        query = db.query(User)
        if username_query:
            query = query.filter(User.username.ilike(f"%{username_query}%"))
        return query.limit(limit).all()

    def create_from_schema(self, db: Session, user_create: UserCreate) -> User:
        """Create a user from a UserCreate schema."""
        user_data = user_create.model_dump()
        return self.create(db, obj_in=user_data)

    def update_from_schema(
        self, db: Session, user_id: int, user_update: UserUpdate
    ) -> Optional[User]:
        """Update a user from a UserUpdate schema."""
        user = self.get(db, user_id)
        if not user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    def update_last_login(self, db: Session, user_id: int) -> Optional[User]:
        """Update user's last login timestamp."""
        user = self.get(db, user_id)
        if user:
            user.last_login = datetime.now(timezone.utc)
            db.commit()
            db.refresh(user)
        return user

    def update_password(
        self, db: Session, user_id: int, password_hash: str
    ) -> Optional[User]:
        """Update user's password hash."""
        user = self.get(db, user_id)
        if user:
            user.password_hash = password_hash
            user.auth_method = "email"
            db.commit()
            db.refresh(user)
        return user

    def update_avatar(
        self, db: Session, user_id: int, avatar_url: str
    ) -> Optional[User]:
        """Update user's avatar URL."""
        user = self.get(db, user_id)
        if user:
            user.avatar_url = avatar_url
            db.commit()
            db.refresh(user)
        return user

    def verify_email(self, db: Session, user_id: int) -> Optional[User]:
        """Mark user's email as verified."""
        user = self.get(db, user_id)
        if user:
            user.email_verified = True
            db.commit()
            db.refresh(user)
        return user

    def update_google_id(
        self, db: Session, user_id: int, google_id: str
    ) -> Optional[User]:
        """Update user's Google ID."""
        user = self.get(db, user_id)
        if user:
            user.google_id = google_id
            user.auth_method = "google"
            db.commit()
            db.refresh(user)
        return user


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """Repository for RefreshToken model operations."""

    def __init__(self):
        super().__init__(RefreshToken)

    def get_by_token_id(
        self, db: Session, token_id: str
    ) -> Optional[RefreshToken]:
        """Get a refresh token by token ID."""
        return db.query(RefreshToken).filter(
            RefreshToken.token_id == token_id
        ).first()

    def get_by_user_id(self, db: Session, user_id: int) -> List[RefreshToken]:
        """Get all refresh tokens for a user."""
        return db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id
        ).all()

    def revoke_by_token_id(self, db: Session, token_id: str) -> bool:
        """Revoke a refresh token by token ID."""
        token = self.get_by_token_id(db, token_id)
        if token:
            db.delete(token)
            db.commit()
            return True
        return False

    def revoke_all_for_user(self, db: Session, user_id: int) -> int:
        """Revoke all refresh tokens for a user."""
        tokens = self.get_by_user_id(db, user_id)
        count = len(tokens)
        for token in tokens:
            db.delete(token)
        db.commit()
        return count

    def get_valid_by_token_id(
        self, db: Session, token_id: str
    ) -> Optional[RefreshToken]:
        """Get a valid (non-expired) refresh token by token ID."""
        token = self.get_by_token_id(db, token_id)
        if token and token.expires_at > datetime.now(timezone.utc):
            return token
        return None

    def create_token(
        self,
        db: Session,
        user_id: int,
        token_id: str,
        expires_at: datetime,
        device_info: str = None,
        ip_address: str = None
    ) -> RefreshToken:
        """Create a new refresh token with all required fields."""
        token_data = {
            "user_id": user_id,
            "token_id": token_id,
            "expires_at": expires_at,
            "device_info": device_info,
            "ip_address": ip_address
        }
        return self.create(db, obj_in=token_data)


class PasswordResetTokenRepository(BaseRepository[PasswordResetToken]):
    """Repository for PasswordResetToken model operations."""

    def __init__(self):
        super().__init__(PasswordResetToken)

    def get_by_token(
        self, db: Session, token: str
    ) -> Optional[PasswordResetToken]:
        """Get a password reset token by token string."""
        return db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token
        ).first()

    def mark_as_used(self, db: Session, token_id: int) -> bool:
        """Mark a password reset token as used."""
        token = self.get(db, token_id)
        if token:
            token.used = True
            db.commit()
            return True
        return False


class EmailVerificationTokenRepository(BaseRepository[EmailVerificationToken]):
    """Repository for EmailVerificationToken model operations."""

    def __init__(self):
        super().__init__(EmailVerificationToken)

    def get_by_token(
        self, db: Session, token: str
    ) -> Optional[EmailVerificationToken]:
        """Get an email verification token by token string."""
        return db.query(EmailVerificationToken).filter(
            EmailVerificationToken.token == token
        ).first()

    def mark_as_used(self, db: Session, token_id: int) -> bool:
        """Mark an email verification token as used."""
        token = self.get(db, token_id)
        if token:
            token.used = True
            db.commit()
            return True
        return False
