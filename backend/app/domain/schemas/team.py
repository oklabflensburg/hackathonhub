"""
Team Pydantic schemas.
"""
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from .user import User
    from .hackathon import Hackathon
    from .project import Project


class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    hackathon_id: int
    max_members: int = 5
    is_open: bool = True


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    max_members: Optional[int] = None
    is_open: Optional[bool] = None


class Team(TeamBase):
    id: int
    created_by: int
    created_at: datetime
    creator: Optional["User"] = None
    hackathon: Optional["Hackathon"] = None

    model_config = ConfigDict(from_attributes=True)


class TeamMemberBase(BaseModel):
    team_id: int
    user_id: int
    role: str = "member"


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMemberUpdate(BaseModel):
    role: Optional[str] = None


class TeamMember(TeamMemberBase):
    id: int
    joined_at: datetime
    user: Optional["User"] = None
    team: Optional["Team"] = None

    model_config = ConfigDict(from_attributes=True)


class TeamInvitationBase(BaseModel):
    team_id: int
    invited_user_id: int


class TeamInvitationCreate(TeamInvitationBase):
    pass


class TeamInvitation(TeamInvitationBase):
    id: int
    invited_by: int
    status: str = "pending"
    created_at: datetime
    expires_at: Optional[datetime] = None
    invited_user: Optional["User"] = None
    inviter: Optional["User"] = None
    team: Optional["Team"] = None

    model_config = ConfigDict(from_attributes=True)


class TeamWithMembers(Team):
    members: List[TeamMember] = []


class TeamWithProjects(TeamWithMembers):
    projects: List["Project"] = []
