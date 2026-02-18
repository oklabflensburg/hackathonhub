from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


# User schemas
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


# Project schemas
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    repository_url: Optional[str] = None
    live_url: Optional[str] = None
    technologies: Optional[str] = None
    status: Optional[str] = "active"
    is_public: Optional[bool] = True
    hackathon_id: Optional[int] = None
    image_path: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    title: Optional[str] = None
    description: Optional[str] = None
    repository_url: Optional[str] = None
    live_url: Optional[str] = None
    technologies: Optional[str] = None
    status: Optional[str] = None
    is_public: Optional[bool] = None
    hackathon_id: Optional[int] = None
    image_path: Optional[str] = None


class Project(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    upvote_count: int = 0
    downvote_count: int = 0
    vote_score: int = 0
    comment_count: int = 0
    view_count: int = 0
    owner: Optional[User] = None
    hackathon: Optional["Hackathon"] = None

    model_config = ConfigDict(from_attributes=True)

# Hackathon schemas


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


class HackathonUpdate(HackathonBase):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    banner_path: Optional[str] = None
    website: Optional[str] = None
    prizes: Optional[str] = None
    rules: Optional[str] = None
    organizers: Optional[str] = None
    prize_pool: Optional[str] = None
    max_participants: Optional[int] = None
    registration_open: Optional[bool] = None


class Hackathon(HackathonBase):
    id: int
    created_at: datetime
    owner_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

# Hackathon Registration schemas


class HackathonRegistrationBase(BaseModel):
    hackathon_id: int
    status: Optional[str] = "registered"


class HackathonRegistrationCreate(HackathonRegistrationBase):
    pass


class HackathonRegistration(HackathonRegistrationBase):
    id: int
    user_id: int
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Vote schemas


class VoteBase(BaseModel):
    project_id: int
    vote_type: str  # 'upvote' or 'downvote'


class VoteCreate(VoteBase):
    pass


class Vote(VoteBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# File schemas


class FileBase(BaseModel):
    filename: str
    filetype: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None


class FileCreate(FileBase):
    pass


class File(FileBase):
    id: int
    filepath: str
    uploaded_by: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Team schemas


class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    hackathon_id: int
    max_members: int = 5
    is_open: bool = True


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int
    created_by: int
    created_at: datetime
    creator: Optional[User] = None
    member_count: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class TeamMemberBase(BaseModel):
    team_id: int
    user_id: int
    role: str = "member"  # 'owner' or 'member'


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMember(TeamMemberBase):
    id: int
    joined_at: datetime
    user: Optional[User] = None

    model_config = ConfigDict(from_attributes=True)


class TeamInvitationBase(BaseModel):
    team_id: int
    invited_user_id: int


class TeamInvitationCreate(TeamInvitationBase):
    pass


class TeamInvitation(TeamInvitationBase):
    id: int
    invited_by: int
    status: str = "pending"  # 'pending', 'accepted', 'declined'
    created_at: datetime
    expires_at: Optional[datetime] = None
    invited_user: Optional[User] = None
    inviter: Optional[User] = None
    team: Optional[Team] = None

    model_config = ConfigDict(from_attributes=True)

# Comment schemas


class CommentBase(BaseModel):
    content: str
    parent_comment_id: Optional[int] = None


class CommentCreate(CommentBase):
    pass


class CommentCreateWithProject(CommentBase):
    project_id: int


class Comment(CommentBase):
    id: int
    project_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    upvote_count: int = 0
    downvote_count: int = 0
    user: Optional[User] = None
    replies: List["Comment"] = []

    model_config = ConfigDict(from_attributes=True)


class CommentVoteBase(BaseModel):
    vote_type: str  # 'upvote' or 'downvote'


class CommentVoteCreate(CommentVoteBase):
    pass


class CommentVoteCreateWithComment(CommentVoteBase):
    comment_id: int


class CommentVote(CommentVoteBase):
    id: int
    comment_id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Chat schemas


class ChatRoomBase(BaseModel):
    name: str
    hackathon_id: Optional[int] = None
    team_id: Optional[int] = None
    is_private: bool = False


class ChatRoomCreate(ChatRoomBase):
    pass


class ChatRoom(ChatRoomBase):
    id: int
    created_by: int
    created_at: datetime
    creator: Optional[User] = None
    participant_count: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ChatMessageBase(BaseModel):
    content: str
    room_id: int
    message_type: str = "text"  # 'text', 'image', 'file'
    file_path: Optional[str] = None


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessage(ChatMessageBase):
    id: int
    user_id: int
    created_at: datetime
    user: Optional[User] = None

    model_config = ConfigDict(from_attributes=True)


class ChatParticipantBase(BaseModel):
    room_id: int
    user_id: int


class ChatParticipantCreate(ChatParticipantBase):
    pass


class ChatParticipant(ChatParticipantBase):
    id: int
    joined_at: datetime
    last_read_at: Optional[datetime] = None
    user: Optional[User] = None

    model_config = ConfigDict(from_attributes=True)

# Token schemas


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenWithRefresh(Token):
    refresh_token: str
    user: Optional["User"] = None


class TokenData(BaseModel):
    username: Optional[str] = None


# Email/Password authentication schemas

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    name: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class EmailVerificationRequest(BaseModel):
    token: str


# Participant schemas


class HackathonParticipant(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Vote statistics


class VoteStats(BaseModel):
    upvote_count: int
    downvote_count: int
    vote_score: int
    user_vote: Optional[str] = None  # 'upvote', 'downvote', or None

# File upload response


class FileUploadResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    filetype: str
    uploaded_at: datetime
    url: str

# Team with members


class TeamWithMembers(Team):
    members: List[TeamMember] = []

# Project with details


class ProjectWithDetails(Project):
    votes: List[Vote] = []
    comments: List[Comment] = []
    team: Optional[Team] = None

# Hackathon with details


class HackathonWithDetails(Hackathon):
    projects: List[Project] = []
    teams: List[Team] = []
    registrations: List[HackathonRegistration] = []
    chat_rooms: List[ChatRoom] = []

# User with details


class UserWithDetails(User):
    projects: List[Project] = []
    teams: List[TeamMember] = []
    votes: List[Vote] = []
    comments: List[Comment] = []
    hackathon_registrations: List[HackathonRegistration] = []

# Chat room with messages


class ChatRoomWithMessages(ChatRoom):
    messages: List[ChatMessage] = []
    participants: List[ChatParticipant] = []

# Newsletter Subscription schemas
class NewsletterSubscriptionBase(BaseModel):
    email: str
    source: Optional[str] = "website_footer"


class NewsletterSubscriptionCreate(NewsletterSubscriptionBase):
    pass


class NewsletterSubscription(NewsletterSubscriptionBase):
    id: int
    subscribed_at: datetime
    is_active: bool
    unsubscribed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Update Comment to handle recursive references


Comment.model_rebuild()
