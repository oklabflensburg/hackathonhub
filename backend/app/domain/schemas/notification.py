"""
Notification Pydantic schemas.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, computed_field

if TYPE_CHECKING:
    from app.domain.schemas.user import User


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
    enabled: bool = True


class UserNotificationPreferenceCreate(UserNotificationPreferenceBase):
    pass


class UserNotificationPreference(UserNotificationPreferenceBase):
    id: int
    user_id: int
    types_mask: str
    channels_mask: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional["User"] = None

    model_config = ConfigDict(from_attributes=True)


class NotificationDeliveryBase(BaseModel):
    channel: str
    status: str
    error: Optional[str] = None
    provider_message_id: Optional[str] = None
    attempt_count: int = 0
    last_attempt_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None


class NotificationDelivery(NotificationDeliveryBase):
    id: int
    notification_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserNotificationBase(BaseModel):
    notification_type: str
    title: str
    message: str
    data: Optional[Dict[str, Any]] = None


class UserNotificationCreate(UserNotificationBase):
    pass


class UserNotification(UserNotificationBase):
    id: int
    user_id: int
    read_at: Optional[datetime] = None
    created_at: datetime
    deliveries: List[NotificationDelivery] = Field(default_factory=list)
    user: Optional["User"] = None

    model_config = ConfigDict(from_attributes=True)

    @computed_field(return_type=Optional[str])
    @property
    def channels_sent(self) -> Optional[str]:
        if not self.deliveries:
            return None
        return ",".join(delivery.channel for delivery in self.deliveries)

    @computed_field(return_type=str)
    @property
    def type(self) -> str:
        return self.notification_type

    @computed_field(return_type=Optional[str])
    @property
    def priority(self) -> Optional[str]:
        return (self.data or {}).get("priority")

    @computed_field(return_type=Optional[str])
    @property
    def action_url(self) -> Optional[str]:
        return (self.data or {}).get("action_url")

    @computed_field(return_type=Optional[Dict[str, Any]])
    @property
    def metadata(self) -> Optional[Dict[str, Any]]:
        return (self.data or {}).get("metadata")

    @computed_field(return_type=Optional[str])
    @property
    def status(self) -> Optional[str]:
        for delivery in self.deliveries:
            if delivery.channel == "in_app":
                return delivery.status
        if self.deliveries:
            return self.deliveries[0].status
        return None

    @computed_field(return_type=Optional[datetime])
    @property
    def expires_at(self) -> Optional[datetime]:
        value = (self.data or {}).get("expires_at")
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return None
        return value


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
    user: Optional["User"] = None

    model_config = ConfigDict(from_attributes=True)
