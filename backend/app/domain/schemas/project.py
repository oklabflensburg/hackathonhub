"""
Project Pydantic schemas.
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from .user import User
    from .team import Team
    from .hackathon import Hackathon


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