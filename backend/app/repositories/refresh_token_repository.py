"""
Refresh Token Repository.

This repository handles all database operations for RefreshToken entities.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.domain.models.user import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """
    Repository for RefreshToken operations.
    """

    def __init__(self):
        super().__init__(RefreshToken)

    def get_by_token_id(self, db: Session,
                        token_id: str) -> Optional[RefreshToken]:
        """
        Get a refresh token by its token ID.

        Args:
            db: Database session
            token_id: The token ID to look up

        Returns:
            RefreshToken if found, None otherwise
        """
        return db.query(self.model).filter(
            self.model.token_id == token_id
        ).first()

    def get_active_by_user(self, db: Session,
                           user_id: int) -> List[RefreshToken]:
        """
        Get all active refresh tokens for a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            List of active refresh tokens
        """
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.revoked.is_(False),
            self.model.expires_at > datetime.now(timezone.utc)
        ).all()

    def revoke_by_token_id(self, db: Session, token_id: str) -> bool:
        """
        Revoke a refresh token by its token ID.

        Args:
            db: Database session
            token_id: The token ID to revoke

        Returns:
            True if token was found and revoked, False otherwise
        """
        token = self.get_by_token_id(db, token_id)
        if not token:
            return False

        token.revoked = True
        db.commit()
        db.refresh(token)
        return True

    def revoke_all_for_user(self, db: Session, user_id: int) -> int:
        """
        Revoke all refresh tokens for a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Number of tokens revoked
        """
        tokens = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.revoked.is_(False)
        ).all()

        for token in tokens:
            token.revoked = True

        db.commit()
        return len(tokens)

    def create_with_details(
        self,
        db: Session,
        user_id: int,
        token_id: str,
        expires_at: datetime,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> RefreshToken:
        """
        Create a new refresh token with additional details.

        Args:
            db: Database session
            user_id: User ID
            token_id: Token ID
            expires_at: Expiration datetime
            device_info: Device information (optional)
            ip_address: IP address (optional)
            user_agent: User agent string (optional)

        Returns:
            Created RefreshToken
        """
        refresh_token = RefreshToken(
            user_id=user_id,
            token_id=token_id,
            expires_at=expires_at,
            device_info=device_info,
            ip_address=ip_address,
            user_agent=user_agent,
            revoked=False
        )

        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return refresh_token
