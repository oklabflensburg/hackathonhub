"""
User-related Pydantic schemas.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.domain.schemas.team import TeamMember
    from app.domain.schemas.project import Project, Vote, Comment
    from app.domain.schemas.hackathon import HackathonRegistration


def is_base64_data_url(value: str) -> bool:
    """Check if a string is a base64 data URL (data:image/...;base64,...)."""
    return value.startswith('data:image/') and 'base64,' in value


class UserBase(BaseModel):
    username: str
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None

    @field_validator('avatar_url')
    @classmethod
    def validate_avatar_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if is_base64_data_url(v):
            raise ValueError(
                'Base64 data URLs are not allowed for avatar_url. '
                'Please upload the file via the upload endpoint.'
            )
        return v


class UserCreate(UserBase):
    github_id: Optional[int] = None
    google_id: Optional[str] = None
    password_hash: Optional[str] = None
    auth_method: str = "github"
    email_verified: bool = False
    access_token: Optional[str] = None


class User(UserBase):
    id: int
    github_id: Optional[int] = None
    google_id: Optional[str] = None
    email_verified: bool = False
    auth_method: str = "github"
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserWithDetails(User):
    teams: Optional[List["TeamMember"]] = None
    projects: Optional[List["Project"]] = None
    votes: Optional[List["Vote"]] = None
    comments: Optional[List["Comment"]] = None
    hackathon_registrations: Optional[List["HackathonRegistration"]] = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None

    @field_validator('avatar_url')
    @classmethod
    def validate_avatar_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if is_base64_data_url(v):
            raise ValueError(
                'Base64 data URLs are not allowed for avatar_url. '
                'Please upload the file via the upload endpoint.'
            )
        return v


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class PasswordResetRequest(BaseModel):
    email: str


class EmailResendRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class EmailVerificationRequest(BaseModel):
    token: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenWithRefresh(Token):
    refresh_token: str


class TokenData(BaseModel):
    username: Optional[str] = None
