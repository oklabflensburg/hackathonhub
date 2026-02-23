"""
User-related Pydantic schemas.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None


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


# Import after User is defined to avoid circular imports
from .team import TeamMember
from .project import Project, Vote, Comment
from .hackathon import HackathonRegistration


class UserWithDetails(User):
    teams: Optional[List[TeamMember]] = None
    projects: Optional[List[Project]] = None
    votes: Optional[List[Vote]] = None
    comments: Optional[List[Comment]] = None
    hackathon_registrations: Optional[List[HackathonRegistration]] = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None


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