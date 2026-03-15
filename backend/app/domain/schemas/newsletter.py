"""
Newsletter-related Pydantic schemas.
"""
import json

from pydantic import BaseModel, ConfigDict, EmailStr, model_validator
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

    @model_validator(mode="before")
    @classmethod
    def parse_stringified_body(cls, data):
        if isinstance(data, str):
            return json.loads(data)
        return data


class NewsletterUnsubscribeRequest(BaseModel):
    email: EmailStr

    @model_validator(mode="before")
    @classmethod
    def parse_stringified_body(cls, data):
        if isinstance(data, str):
            return json.loads(data)
        return data
