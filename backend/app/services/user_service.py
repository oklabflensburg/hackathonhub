"""
User service layer for business logic operations.
"""
from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.domain.models.user import User
from app.domain.schemas.user import UserCreate, UserUpdate, User as UserSchema
from app.repositories.user_repository import (
    UserRepository, RefreshTokenRepository,
    PasswordResetTokenRepository, EmailVerificationTokenRepository
)
from app.core.config import settings


class UserService:
    """Service for user-related business logic."""

    def __init__(self):
        self.user_repo = UserRepository()
        self.refresh_token_repo = RefreshTokenRepository()
        self.password_reset_repo = PasswordResetTokenRepository()
        self.email_verification_repo = EmailVerificationTokenRepository()

    def get_user(self, db: Session, user_id: int) -> Optional[UserSchema]:
        """Get a user by ID."""
        user = self.user_repo.get(db, user_id)
        if user:
            return UserSchema.model_validate(user)
        return None

    def get_user_by_email(self, db: Session, email: str) -> Optional[UserSchema]:
        """Get a user by email."""
        user = self.user_repo.get_by_email(db, email)
        if user:
            return UserSchema.model_validate(user)
        return None

    def get_user_by_username(self, db: Session, username: str) -> Optional[UserSchema]:
        """Get a user by username."""
        user = self.user_repo.get_by_username(db, username)
        if user:
            return UserSchema.model_validate(user)
        return None

    def create_user(self, db: Session, user_create: UserCreate) -> UserSchema:
        """Create a new user."""
        # Check if user already exists
        if self.user_repo.get_by_email(db, user_create.email):
            raise ValueError("User with this email already exists")

        if self.user_repo.get_by_username(db, user_create.username):
            raise ValueError("User with this username already exists")

        # Create user
        user = self.user_repo.create_from_schema(db, user_create)
        return UserSchema.model_validate(user)

    def update_user(
        self, db: Session, user_id: int, user_update: UserUpdate
    ) -> Optional[UserSchema]:
        """Update a user."""
        user = self.user_repo.update_from_schema(db, user_id, user_update)
        if user:
            return UserSchema.model_validate(user)
        return None

    def update_last_login(self, db: Session, user_id: int) -> Optional[UserSchema]:
        """Update user's last login timestamp."""
        user = self.user_repo.update_last_login(db, user_id)
        if user:
            return UserSchema.model_validate(user)
        return None

    def verify_email(self, db: Session, user_id: int) -> Optional[UserSchema]:
        """Mark user's email as verified."""
        user = self.user_repo.verify_email(db, user_id)
        if user:
            return UserSchema.model_validate(user)
        return None

    def search_users(
        self, db: Session, username_query: str, limit: int = 10
    ) -> List[UserSchema]:
        """Search users by username."""
        users = self.user_repo.search_by_username(db, username_query, limit)
        return [UserSchema.model_validate(user) for user in users]

    def get_users(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[UserSchema]:
        """Get multiple users with pagination."""
        users = self.user_repo.get_multi(db, skip=skip, limit=limit)
        return [UserSchema.model_validate(user) for user in users]

    def delete_user(self, db: Session, user_id: int) -> bool:
        """Delete a user by ID."""
        return self.user_repo.delete(db, id=user_id)


class AuthService:
    """Service for authentication-related business logic."""

    def __init__(self):
        self.user_repo = UserRepository()
        self.refresh_token_repo = RefreshTokenRepository()

    def authenticate_user(
        self, db: Session, email: str, password_hash: str
    ) -> Optional[UserSchema]:
        """Authenticate a user with email and password hash."""
        user = self.user_repo.get_by_email(db, email)
        if not user:
            return None

        # In a real implementation, you would verify the password hash
        # For now, we'll assume the password_hash is already verified
        if user.password_hash != password_hash:
            return None

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)

        return UserSchema.model_validate(user)

    def create_refresh_token(
        self, db: Session, user_id: int, token_id: str,
        device_info: str = None, ip_address: str = None
    ) -> bool:
        """Create a refresh token for a user."""
        expires_at = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

        token_data = {
            "user_id": user_id,
            "token_id": token_id,
            "expires_at": expires_at,
            "device_info": device_info,
            "ip_address": ip_address,
        }

        self.refresh_token_repo.create(db, obj_in=token_data)
        return True

    def revoke_refresh_token(self, db: Session, token_id: str) -> bool:
        """Revoke a refresh token."""
        return self.refresh_token_repo.revoke_by_token_id(db, token_id)

    def revoke_all_user_tokens(self, db: Session, user_id: int) -> int:
        """Revoke all refresh tokens for a user."""
        return self.refresh_token_repo.revoke_all_for_user(db, user_id)


# Create service instances for dependency injection
user_service = UserService()
auth_service = AuthService()
