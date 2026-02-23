"""
Notification domain models.
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Boolean, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class UserNotificationPreference(Base):
    __tablename__ = "user_notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    notification_type = Column(String(50), nullable=False)
    # 'email', 'push', 'in_app', 'all'
    channel = Column(String(20), nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'notification_type', 'channel',
            name='_user_notification_channel_uc'
        ),
    )

    # Relationships will be defined in __init__.py
    # user = relationship("User", back_populates="notification_preferences")


class NotificationType(Base):
    __tablename__ = "notification_types"

    id = Column(Integer, primary_key=True, index=True)
    type_key = Column(String(50), unique=True, nullable=False)
    # 'team', 'project', 'hackathon', 'system'
    category = Column(String(50), nullable=False)
    default_channels = Column(String(100), default='email,in_app')
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserNotification(Base):
    __tablename__ = "user_notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    notification_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(Text)  # JSON string for additional data
    # Comma-separated channels actually used
    channels_sent = Column(String(100))
    read_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships will be defined in __init__.py
    # user = relationship("User", back_populates="notifications")


class PushSubscription(Base):
    __tablename__ = "push_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    endpoint = Column(Text, nullable=False)
    p256dh = Column(Text, nullable=False)
    auth = Column(Text, nullable=False)
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('endpoint', name='_push_endpoint_uc'),
    )

    # Relationships will be defined in __init__.py
    # user = relationship("User", back_populates="push_subscriptions")