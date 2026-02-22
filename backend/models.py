from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Boolean, UniqueConstraint, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Use String for SQLite compatibility, INET for PostgreSQL
# SQLite doesn't support INET type, so we use String as fallback
try:
    from sqlalchemy.dialects.postgresql import INET
    IPAddressType = INET
except ImportError:
    # Fallback to String for SQLite and other databases
    IPAddressType = String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    avatar_url = Column(String)
    name = Column(String)
    bio = Column(Text)
    location = Column(String)
    company = Column(String)
    blog = Column(String)
    twitter_username = Column(String)
    password_hash = Column(String, nullable=True)
    google_id = Column(String, unique=True, index=True, nullable=True)
    email_verified = Column(Boolean, default=False)
    auth_method = Column(String, default="github")
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    projects = relationship("Project", back_populates="owner")
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    votes = relationship("Vote", back_populates="user")
    comment_votes = relationship("CommentVote", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    team_memberships = relationship("TeamMember", back_populates="user")
    team_invitations = relationship(
        "TeamInvitation",
        foreign_keys="TeamInvitation.invited_user_id",
        back_populates="invited_user"
    )
    sent_invitations = relationship(
        "TeamInvitation",
        foreign_keys="TeamInvitation.invited_by",
        back_populates="inviter"
    )
    chat_messages = relationship("ChatMessage", back_populates="user")
    chat_participants = relationship("ChatParticipant", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    repository_url = Column(String)
    live_url = Column(String)
    technologies = Column(String)  # Comma-separated list
    status = Column(String, default="active")  # active, completed, archived
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String)  # Path to uploaded image file
    upvote_count = Column(Integer, default=0)
    downvote_count = Column(Integer, default=0)
    vote_score = Column(Integer, default=0)  # upvotes - downvotes
    comment_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)  # Project view count
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    owner = relationship("User", back_populates="projects")
    hackathon = relationship("Hackathon", back_populates="projects")
    team = relationship("Team")
    votes = relationship("Vote", back_populates="project")
    comments = relationship("Comment", back_populates="project")


class Hackathon(Base):
    __tablename__ = "hackathons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    location = Column(String)  # Physical or virtual
    latitude = Column(Float, nullable=True)  # Geographic coordinates
    longitude = Column(Float, nullable=True)
    website = Column(String)
    image_url = Column(String)  # URL to hackathon banner/image
    banner_path = Column(String)  # Path to uploaded banner file
    participant_count = Column(Integer, default=0)  # Registered participants
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    max_participants = Column(Integer, nullable=True)  # Optional limit
    registration_open = Column(Boolean, default=True)
    prizes = Column(Text, nullable=True)  # JSON or text description of prizes
    rules = Column(Text, nullable=True)  # Rules and guidelines
    organizers = Column(Text, nullable=True)  # JSON or text of organizers
    prize_pool = Column(String, nullable=True)  # Total prize amount
    owner_id = Column(Integer, ForeignKey("users.id"),
                      nullable=True)  # Creator

    registrations = relationship(
        "HackathonRegistration",
        back_populates="hackathon"
    )
    projects = relationship("Project", back_populates="hackathon")
    teams = relationship("Team", back_populates="hackathon")
    chat_rooms = relationship("ChatRoom", back_populates="hackathon")
    owner = relationship("User")


class HackathonRegistration(Base):
    __tablename__ = "hackathon_registrations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"))
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="registered")  # registered, attended

    # Unique constraint to prevent duplicate registrations
    __table_args__ = (
        UniqueConstraint(
            'user_id', 'hackathon_id',
            name='_user_hackathon_uc'
        ),
    )

    user = relationship("User")
    hackathon = relationship("Hackathon")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    vote_type = Column(String, nullable=False)  # 'upvote' or 'downvote'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'project_id',
            name='_user_project_vote_uc'
        ),
    )

    user = relationship("User", back_populates="votes")
    project = relationship("Project", back_populates="votes")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    filetype = Column(String(50), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    file_size = Column(Integer)  # Size in bytes
    mime_type = Column(String(100))

    uploader = relationship("User")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    max_members = Column(Integer, default=5)
    is_open = Column(Boolean, default=True)  # Open for new members

    hackathon = relationship("Hackathon", back_populates="teams")
    creator = relationship("User", foreign_keys=[created_by])
    members = relationship("TeamMember", back_populates="team")
    invitations = relationship("TeamInvitation", back_populates="team")


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(20), default='member')  # 'owner' or 'member'
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            'team_id', 'user_id',
            name='_team_user_member_uc'
        ),
    )

    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")


class TeamInvitation(Base):
    __tablename__ = "team_invitations"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    invited_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    # 'pending', 'accepted', 'declined'
    status = Column(String(20), default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint(
            'team_id', 'invited_user_id',
            name='_team_user_invitation_uc'
        ),
    )

    team = relationship("Team", back_populates="invitations")
    invited_user = relationship(
        "User",
        foreign_keys=[invited_user_id],
        back_populates="team_invitations"
    )
    inviter = relationship(
        "User",
        foreign_keys=[invited_by],
        back_populates="sent_invitations"
    )


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    parent_comment_id = Column(
        Integer, ForeignKey("comments.id"), nullable=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    upvote_count = Column(Integer, default=0)
    downvote_count = Column(Integer, default=0)

    user = relationship("User", back_populates="comments")
    project = relationship("Project", back_populates="comments")
    parent = relationship(
        "Comment", remote_side=[id], back_populates="replies"
    )
    replies = relationship("Comment", back_populates="parent")
    votes = relationship("CommentVote", back_populates="comment")


class CommentVote(Base):
    __tablename__ = "comment_votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_id = Column(
        Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    vote_type = Column(String(10), nullable=False)  # 'upvote' or 'downvote'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'comment_id',
            name='_user_comment_vote_uc'
        ),
    )

    user = relationship("User", back_populates="comment_votes")
    comment = relationship("Comment", back_populates="votes")


class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    is_private = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    hackathon = relationship("Hackathon", back_populates="chat_rooms")
    team = relationship("Team")
    creator = relationship("User", foreign_keys=[created_by])
    messages = relationship("ChatMessage", back_populates="room")
    participants = relationship("ChatParticipant", back_populates="room")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    # 'text', 'image', 'file'
    message_type = Column(String(20), default='text')
    file_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    room = relationship("ChatRoom", back_populates="messages")
    user = relationship("User", back_populates="chat_messages")


class ChatParticipant(Base):
    __tablename__ = "chat_participants"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    last_read_at = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint(
            'room_id', 'user_id',
            name='_room_user_participant_uc'
        ),
    )

    room = relationship("ChatRoom", back_populates="participants")
    user = relationship("User", back_populates="chat_participants")


class NewsletterSubscription(Base):
    __tablename__ = "newsletter_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    subscribed_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    unsubscribed_at = Column(DateTime(timezone=True), nullable=True)
    # website_footer, signup_page, etc.
    source = Column(String, default="website_footer")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token_id = Column(String(64), unique=True, nullable=False)  # jti from JWT
    device_info = Column(Text, nullable=True)
    ip_address = Column(IPAddressType, nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    replaced_by_token_id = Column(String(64), nullable=True)

    user = relationship("User", back_populates="refresh_tokens")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(64), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")


class UserNotificationPreference(Base):
    __tablename__ = "user_notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    notification_type = Column(String(50), nullable=False)
    # 'email', 'push', 'in_app', 'all'
    channel = Column(String(20), nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'notification_type', 'channel',
            name='_user_notification_channel_uc'
        ),
    )

    user = relationship("User")


class NotificationType(Base):
    __tablename__ = "notification_types"

    id = Column(Integer, primary_key=True, index=True)
    type_key = Column(String(50), unique=True, nullable=False)
    # 'team', 'project', 'hackathon', 'system'
    category = Column(String(50), nullable=False)
    default_channels = Column(String(100), default='email,in_app')
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserNotification(Base):
    __tablename__ = "user_notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    notification_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(Text)  # JSON string for additional data
    # Comma-separated channels actually used
    channels_sent = Column(String(100))
    read_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")


class PushSubscription(Base):
    __tablename__ = "push_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    endpoint = Column(Text, nullable=False)
    p256dh = Column(Text, nullable=False)
    auth = Column(Text, nullable=False)
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('endpoint', name='_push_endpoint_uc'),
    )

    user = relationship("User")


class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(64), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
