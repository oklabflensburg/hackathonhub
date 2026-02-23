"""
Notification Pydantic schemas.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Import at the top to avoid circular imports
from .user import User


class NotificationTypeBase(BaseModel):
    type_key: str
    category: str
    default_channels: str = "email,in_app"
    description: Optional[str] = None


class NotificationTypeCreate(NotificationTypeBase):
    pass


class NotificationType(NotificationTypeBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserNotificationPreferenceBase(BaseModel):
    notification_type: str
    channel: str
    enabled: bool = True


class UserNotificationPreferenceCreate(UserNotificationPreferenceBase):
    pass


class UserNotificationPreference(UserNotificationPreferenceBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[User] = None

    model_config = ConfigDict(from_attributes=True)


class UserNotificationBase(BaseModel):
    notification_type: str
    title: str
    message: str
    data: Optional[str] = None
    channels_sent: Optional[str] = None


class UserNotificationCreate(UserNotificationBase):
    pass


class UserNotification(UserNotificationBase):
    id: int
    user_id: int
    read_at: Optional[datetime] = None
    created_at: datetime
    user: Optional[User] = None

    model_config = ConfigDict(from_attributes=True)


class PushSubscriptionBase(BaseModel):
    endpoint: str
    p256dh: str
    auth: str
    user_agent: Optional[str] = None


class PushSubscriptionCreate(PushSubscriptionBase):
    pass


class PushSubscription(PushSubscriptionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[User] = None

    model_config = ConfigDict(from_attributes=True)