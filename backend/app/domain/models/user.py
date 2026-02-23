"""
User model and related authentication models.
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    avatar_url = Column(String)
    name = Column(String)
    bio = Column(Text)
    location = Column(String)
    company = Column(String)
    blog = Column(String)
    twitter_username = Column(String)
    password_hash = Column(String, nullable=True)
    google_id = Column(String, unique=True, index=True, nullable=True)
    email_verified = Column(Boolean, default=False)
    auth_method = Column(String, default="github")
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships will be defined in __init__.py to avoid circular imports
    # projects = relationship("Project", back_populates="owner")
    # refresh_tokens = relationship("RefreshToken", back_populates="user")
    # votes = relationship("Vote", back_populates="user")
    # comment_votes = relationship("CommentVote", back_populates="user")
    # comments = relationship("Comment", back_populates="user")
    # team_memberships = relationship("TeamMember", back_populates="user")
    # team_invitations = relationship(
    #     "TeamInvitation",
    #     foreign_keys="TeamInvitation.invited_user_id",
    #     back_populates="invited_user"
    # )
    # sent_invitations = relationship(
    #     "TeamInvitation",
    #     foreign_keys="TeamInvitation.invited_by",
    #     back_populates="inviter"
    # )
    # chat_messages = relationship("ChatMessage", back_populates="user")
    # chat_participants = relationship(
    #     "ChatParticipant", back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token_id = Column(String(64), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    device_info = Column(String(255))
    ip_address = Column(String(45))  # IPv6 max length
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="refresh_tokens")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(64), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")


class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(64), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")