"""
Hackathon Pydantic schemas.
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from app.domain.schemas.user import User


class HackathonBase(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    website: Optional[str] = None
    image_url: Optional[str] = None
    banner_path: Optional[str] = None
    participant_count: int = 0
    project_count: int = 0
    is_active: bool = True
    max_participants: Optional[int] = None
    registration_open: bool = True
    prizes: Optional[str] = None
    rules: Optional[str] = None
    organizers: Optional[str] = None
    prize_pool: Optional[str] = None


class HackathonCreate(HackathonBase):
    pass


class HackathonUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    website: Optional[str] = None
    image_url: Optional[str] = None
    banner_path: Optional[str] = None
    participant_count: Optional[int] = None
    project_count: Optional[int] = None
    is_active: Optional[bool] = None
    max_participants: Optional[int] = None
    registration_open: Optional[bool] = None
    prizes: Optional[str] = None
    rules: Optional[str] = None
    organizers: Optional[str] = None
    prize_pool: Optional[str] = None


class Hackathon(HackathonBase):
    id: int
    owner_id: Optional[int] = None
    created_at: datetime
    owner: Optional["User"] = None

    model_config = ConfigDict(from_attributes=True)


class HackathonRegistrationBase(BaseModel):
    user_id: int
    hackathon_id: int
    status: str = "registered"


class HackathonRegistrationCreate(HackathonRegistrationBase):
    pass


class HackathonRegistration(HackathonRegistrationBase):
    id: int
    registered_at: datetime
    user: Optional["User"] = None
    hackathon: Optional[Hackathon] = None

    model_config = ConfigDict(from_attributes=True)


class HackathonRegistrationStatus(BaseModel):
    """Response schema for checking if user is registered for a hackathon."""
    is_registered: bool
    hackathon_id: int
    user_id: Optional[int] = None
    registration_id: Optional[int] = None
    status: Optional[str] = None
    registered_at: Optional[datetime] = None
