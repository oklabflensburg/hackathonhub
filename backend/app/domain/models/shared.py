"""
Shared domain models (File, NewsletterSubscription, Chat, etc.).
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Boolean, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    filetype = Column(String(50), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    file_size = Column(Integer)  # Size in bytes
    mime_type = Column(String(100))

    # Relationships will be defined in __init__.py
    # uploader = relationship("User", back_populates="uploaded_files")


class NewsletterSubscription(Base):
    __tablename__ = "newsletter_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    subscribed_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    unsubscribed_at = Column(DateTime(timezone=True), nullable=True)
    # website_footer, signup_page, etc.
    source = Column(String, default="website_footer")


class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    is_private = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships will be defined in __init__.py
    # hackathon = relationship("Hackathon", back_populates="chat_rooms")
    # team = relationship("Team", back_populates="chat_rooms")
    # creator = relationship("User", foreign_keys=[created_by])
    # messages = relationship("ChatMessage", back_populates="room")
    # participants = relationship("ChatParticipant", back_populates="room")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    # 'text', 'image', 'file'
    message_type = Column(String(20), default='text')
    file_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships will be defined in __init__.py
    # room = relationship("ChatRoom", back_populates="messages")
    # user = relationship("User", back_populates="chat_messages")


class ChatParticipant(Base):
    __tablename__ = "chat_participants"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    last_read_at = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint(
            'room_id', 'user_id',
            name='_room_user_participant_uc'
        ),
    )

    # Relationships will be defined in __init__.py
    # room = relationship("ChatRoom", back_populates="participants")
    # user = relationship("User", back_populates="chat_participants")