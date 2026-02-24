"""
Newsletter-related Pydantic schemas.
"""
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


class NewsletterSubscriptionBase(BaseModel):
    email: EmailStr
    source: str = "website"


class NewsletterSubscriptionCreate(NewsletterSubscriptionBase):
    pass


class NewsletterSubscription(NewsletterSubscriptionBase):
    id: int
    subscribed_at: datetime
    unsubscribed_at: Optional[datetime] = None
    last_notified_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class NewsletterSubscribeRequest(BaseModel):
    email: EmailStr
    source: Optional[str] = "website"


class NewsletterUnsubscribeRequest(BaseModel):
    email: EmailStr