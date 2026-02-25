"""
Project Pydantic schemas.
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict, field_validator

if TYPE_CHECKING:
    from .user import User
    from .team import Team
    from .hackathon import Hackathon


def is_base64_data_url(value: str) -> bool:
    """Check if a string is a base64 data URL (data:image/...;base64,...)."""
    return value.startswith('data:image/') and 'base64,' in value


class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    repository_url: Optional[str] = None
    live_url: Optional[str] = None
    technologies: Optional[str] = None
    status: Optional[str] = "active"
    is_public: Optional[bool] = True
    hackathon_id: Optional[int] = None
    team_id: Optional[int] = None
    image_path: Optional[str] = None

    @field_validator('image_path')
    @classmethod
    def validate_image_path(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if is_base64_data_url(v):
            raise ValueError(
                'Base64 data URLs are not allowed for image_path. '
                'Please upload the file via the upload endpoint.'
            )
        return v


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    repository_url: Optional[str] = None
    live_url: Optional[str] = None
    technologies: Optional[str] = None
    status: Optional[str] = None
    is_public: Optional[bool] = None
    hackathon_id: Optional[int] = None
    team_id: Optional[int] = None
    image_path: Optional[str] = None

    @field_validator('image_path')
    @classmethod
    def validate_image_path(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if is_base64_data_url(v):
            raise ValueError(
                'Base64 data URLs are not allowed for image_path. '
                'Please upload the file via the upload endpoint.'
            )
        return v


class Project(ProjectBase):
    id: int
    owner_id: Optional[int] = None
    team_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    upvote_count: int = 0
    downvote_count: int = 0
    vote_score: int = 0
    comment_count: int = 0
    view_count: int = 0
    owner: Optional["User"] = None
    hackathon: Optional["Hackathon"] = None
    team: Optional["Team"] = None

    model_config = ConfigDict(from_attributes=True)


class VoteBase(BaseModel):
    user_id: int
    project_id: int
    vote_type: str  # 'upvote' or 'downvote'


class VoteCreate(VoteBase):
    pass


class Vote(VoteBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentBase(BaseModel):
    content: str
    user_id: int
    project_id: int
    parent_id: Optional[int] = None


class CommentCreate(BaseModel):
    content: str
    parent_id: Optional[int] = None


class Comment(CommentBase):
    id: int
    upvote_count: int = 0
    downvote_count: int = 0
    vote_score: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)