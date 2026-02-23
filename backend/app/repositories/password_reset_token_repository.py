"""
Password Reset Token Repository.

This repository handles all database operations for
PasswordResetToken entities.
"""
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.domain.models.user import PasswordResetToken
from app.repositories.base import BaseRepository


class PasswordResetTokenRepository(BaseRepository[PasswordResetToken]):
    """
    Repository for PasswordResetToken operations.
    """
    
    def __init__(self):
        super().__init__(PasswordResetToken)
    
    def get_by_token(self, db: Session,
                     token: str) -> Optional[PasswordResetToken]:
        """
        Get a password reset token by its token string.
        
        Args:
            db: Database session
            token: The token string to look up
            
        Returns:
            PasswordResetToken if found, None otherwise
        """
        return db.query(self.model).filter(
            self.model.token == token
        ).first()
    
    def get_active_by_user(self, db: Session,
                           user_id: int) -> Optional[PasswordResetToken]:
        """
        Get active password reset token for a user.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Active PasswordResetToken if found, None otherwise
        """
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.used.is_(False),
            self.model.expires_at > datetime.utcnow()
        ).first()
    
    def mark_as_used(self, db: Session, token_id: int) -> bool:
        """
        Mark a password reset token as used.
        
        Args:
            db: Database session
            token_id: Token ID
            
        Returns:
            True if token was found and marked, False otherwise
        """
        token = self.get(db, token_id)
        if not token:
            return False
        
        token.used = True
        db.commit()
        db.refresh(token)
        return True
    
    def create_token(
        self,
        db: Session,
        user_id: int,
        token: str,
        expires_at: datetime
    ) -> PasswordResetToken:
        """
        Create a new password reset token.
        
        Args:
            db: Database session
            user_id: User ID
            token: Token string
            expires_at: Expiration datetime
            
        Returns:
            Created PasswordResetToken
        """
        password_reset_token = PasswordResetToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            used=False
        )
        
        db.add(password_reset_token)
        db.commit()
        db.refresh(password_reset_token)
        return password_reset_token