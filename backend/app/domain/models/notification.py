"""
Notification domain models.
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Boolean, UniqueConstraint, JSON, Index
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from .base import Base


notification_json_type = JSON().with_variant(JSONB, "postgresql")


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
    data = Column(notification_json_type)
    read_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships will be defined in __init__.py
    # user = relationship("User", back_populates="notifications")

    __table_args__ = (
        Index("ix_user_notifications_user_id", "user_id"),
        Index("ix_user_notifications_created_at", "created_at"),
        Index("ix_user_notifications_read_at", "read_at"),
    )


class NotificationDelivery(Base):
    __tablename__ = "notification_deliveries"

    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(
        Integer,
        ForeignKey("user_notifications.id", ondelete="CASCADE"),
        nullable=False,
    )
    channel = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    error = Column(Text)
    provider_message_id = Column(String(255))
    attempt_count = Column(Integer, nullable=False, default=0)
    last_attempt_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


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
