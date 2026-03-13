"""
Team Pydantic schemas.
"""
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from .user import PublicUser
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
    creator: Optional["PublicUser"] = None
    hackathon: Optional["Hackathon"] = None
    member_count: Optional[int] = None
    project_count: int = 0
    active_project_count: int = 0
    completed_project_count: int = 0
    total_votes: int = 0
    total_comments: int = 0
    last_activity_at: Optional[datetime] = None
    view_count: int = 0
    engagement_score: int = 0
    engagement_level: str = "low"

    model_config = ConfigDict(from_attributes=True)


class TeamMemberBase(BaseModel):
    team_id: int
    user_id: int
    role: str = "member"


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMemberCreateRequest(BaseModel):
    """Schema for creating a team member from API request."""
    user_id: int
    role: str = "member"


class TeamMemberUpdate(BaseModel):
    role: Optional[str] = None


class TeamMember(TeamMemberBase):
    id: int
    joined_at: datetime
    user: Optional["PublicUser"] = None
    team: Optional["Team"] = None

    model_config = ConfigDict(from_attributes=True)


class TeamInvitationBase(BaseModel):
    team_id: int
    invited_user_id: int


class TeamInvitationCreate(TeamInvitationBase):
    pass


class TeamInvitationCreateRequest(BaseModel):
    """Schema for creating a team invitation from API request."""
    invited_user_id: int


class TeamInvitation(TeamInvitationBase):
    id: int
    invited_by: int
    status: str = "pending"
    created_at: datetime
    expires_at: Optional[datetime] = None
    invited_user: Optional["PublicUser"] = None
    inviter: Optional["PublicUser"] = None
    team: Optional["Team"] = None

    model_config = ConfigDict(from_attributes=True)


class TeamReportBase(BaseModel):
    reason: str


class TeamReportCreateRequest(TeamReportBase):
    pass


class TeamReportUpdateRequest(BaseModel):
    status: str
    resolution_note: Optional[str] = None


class TeamReport(TeamReportBase):
    id: int
    team_id: int
    reporter_id: int
    status: str = "pending"
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    resolution_note: Optional[str] = None
    created_at: datetime
    team: Optional["Team"] = None
    reporter: Optional["PublicUser"] = None
    reviewer: Optional["PublicUser"] = None

    model_config = ConfigDict(from_attributes=True)


class TeamWithMembers(Team):
    members: List[TeamMember] = []


class TeamWithProjects(TeamWithMembers):
    projects: List["Project"] = []
