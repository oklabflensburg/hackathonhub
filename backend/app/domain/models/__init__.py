"""
Domain models package initialization.

This file sets up all model relationships to avoid circular imports.
"""
from sqlalchemy.orm import relationship

from .base import Base
from .user import (
    User, RefreshToken, PasswordResetToken, EmailVerificationToken
)
from .rbac import Role, Permission, RolePermission, UserRole
from .report import Report
from .project import Project, Vote, Comment, CommentVote
from .hackathon import Hackathon, HackathonRegistration
from .team import Team, TeamMember, TeamInvitation, TeamReport
from .notification import (
    NotificationType, UserNotification, NotificationDelivery,
    UserNotificationPreference, PushSubscription
)
from .shared import (
    File, NewsletterSubscription, ChatRoom,
    ChatMessage, ChatParticipant
)

# Set up User relationships
User.projects = relationship("Project", back_populates="owner")
User.refresh_tokens = relationship("RefreshToken", back_populates="user")
User.votes = relationship("Vote", back_populates="user")
User.comment_votes = relationship("CommentVote", back_populates="user")
User.comments = relationship("Comment", back_populates="user")

# Set up Project relationships
Project.owner = relationship("User", back_populates="projects")
Project.hackathon = relationship("Hackathon", back_populates="projects")
Project.team = relationship("Team", back_populates="projects")
Project.votes = relationship("Vote", back_populates="project")
Project.comments = relationship("Comment", back_populates="project")

# Set up Vote relationships
Vote.user = relationship("User", back_populates="votes")
Vote.project = relationship("Project", back_populates="votes")

# Set up Comment relationships
Comment.user = relationship("User", back_populates="comments")
Comment.project = relationship("Project", back_populates="comments")
Comment.parent = relationship(
    "Comment",
    remote_side="Comment.id",
    back_populates="replies"
)
Comment.replies = relationship(
    "Comment",
    back_populates="parent",
    cascade="all, delete-orphan",
    single_parent=True,
)
Comment.votes = relationship(
    "CommentVote",
    back_populates="comment",
    cascade="all, delete-orphan",
    passive_deletes=True,
)

# Set up CommentVote relationships
CommentVote.user = relationship("User", back_populates="comment_votes")
CommentVote.comment = relationship("Comment", back_populates="votes")

# Set up Hackathon relationships
Hackathon.registrations = relationship(
    "HackathonRegistration",
    back_populates="hackathon"
)
Hackathon.projects = relationship("Project", back_populates="hackathon")
Hackathon.teams = relationship("Team", back_populates="hackathon")
Hackathon.chat_rooms = relationship("ChatRoom", back_populates="hackathon")
Hackathon.owner = relationship("User")

# Set up HackathonRegistration relationships
HackathonRegistration.user = relationship("User")
HackathonRegistration.hackathon = relationship("Hackathon")

# Set up Team relationships
Team.hackathon = relationship("Hackathon", back_populates="teams")
Team.creator = relationship("User", foreign_keys=[Team.created_by])
Team.members = relationship("TeamMember", back_populates="team")
Team.invitations = relationship("TeamInvitation", back_populates="team")
Team.reports = relationship("TeamReport", back_populates="team")
Team.projects = relationship("Project", back_populates="team")
Team.chat_rooms = relationship("ChatRoom", back_populates="team")

# Set up TeamMember relationships
TeamMember.team = relationship("Team", back_populates="members")
TeamMember.user = relationship("User", back_populates="team_memberships")

# Set up TeamInvitation relationships
TeamInvitation.team = relationship("Team", back_populates="invitations")
TeamInvitation.invited_user = relationship(
    "User",
    foreign_keys=[TeamInvitation.invited_user_id],
    back_populates="team_invitations"
)
TeamInvitation.inviter = relationship(
    "User",
    foreign_keys=[TeamInvitation.invited_by],
    back_populates="team_invitations_sent"
)
TeamReport.team = relationship("Team", back_populates="reports")
TeamReport.reporter = relationship(
    "User",
    foreign_keys=[TeamReport.reporter_id],
    back_populates="team_reports"
    )
TeamReport.reviewer = relationship(
    "User",
    foreign_keys=[TeamReport.reviewed_by],
    back_populates="reviewed_team_reports"
)

# Set up Notification relationships
UserNotificationPreference.user = relationship(
    "User",
    back_populates="notification_preferences"
)
UserNotification.user = relationship("User", back_populates="notifications")
UserNotification.deliveries = relationship(
    "NotificationDelivery",
    back_populates="notification",
    cascade="all, delete-orphan"
)
NotificationDelivery.notification = relationship(
    "UserNotification",
    back_populates="deliveries"
)
PushSubscription.user = relationship(
    "User",
    back_populates="push_subscriptions"
)

# Set up Shared model relationships
File.uploader = relationship("User", back_populates="uploaded_files")
ChatRoom.hackathon = relationship("Hackathon", back_populates="chat_rooms")
ChatRoom.team = relationship("Team", back_populates="chat_rooms")
ChatRoom.creator = relationship("User", foreign_keys=[ChatRoom.created_by])
ChatRoom.messages = relationship("ChatMessage", back_populates="room")
ChatRoom.participants = relationship("ChatParticipant", back_populates="room")
ChatMessage.room = relationship("ChatRoom", back_populates="messages")
ChatMessage.user = relationship("User", back_populates="chat_messages")
ChatParticipant.room = relationship("ChatRoom", back_populates="participants")
ChatParticipant.user = relationship("User", back_populates="chat_participants")

# Set up User relationships for new models
User.team_memberships = relationship("TeamMember", back_populates="user")
User.team_invitations = relationship(
    "TeamInvitation",
    foreign_keys=[TeamInvitation.invited_user_id],
    back_populates="invited_user"
)
User.team_invitations_sent = relationship(
    "TeamInvitation",
    foreign_keys=[TeamInvitation.invited_by],
    back_populates="inviter"
)
User.team_reports = relationship(
    "TeamReport",
    foreign_keys=[TeamReport.reporter_id],
    back_populates="reporter"
)
User.reviewed_team_reports = relationship(
    "TeamReport",
    foreign_keys=[TeamReport.reviewed_by],
    back_populates="reviewer"
)
User.reports = relationship(
    "Report",
    foreign_keys=[Report.reporter_id],
    back_populates="reporter"
)
User.reviewed_reports = relationship(
    "Report",
    foreign_keys=[Report.reviewed_by],
    back_populates="reviewer"
)
User.user_roles = relationship(
    "UserRole",
    back_populates="user",
    cascade="all, delete-orphan"
)
User.notification_preferences = relationship(
    "UserNotificationPreference",
    back_populates="user"
)
User.notifications = relationship("UserNotification", back_populates="user")
User.push_subscriptions = relationship(
    "PushSubscription",
    back_populates="user"
)
User.uploaded_files = relationship("File", back_populates="uploader")
User.chat_messages = relationship("ChatMessage", back_populates="user")
User.chat_participants = relationship("ChatParticipant", back_populates="user")

Report.reporter = relationship(
    "User",
    foreign_keys=[Report.reporter_id],
    back_populates="reports"
)
Report.reviewer = relationship(
    "User",
    foreign_keys=[Report.reviewed_by],
    back_populates="reviewed_reports"
)

# Set up RBAC relationships
Role.role_permissions = relationship(
    "RolePermission",
    back_populates="role",
    cascade="all, delete-orphan",
    overlaps="permissions,roles"
)
Role.permissions = relationship(
    "Permission",
    secondary="role_permissions",
    back_populates="roles",
    overlaps="role_permissions,permission"
)
Role.user_roles = relationship(
    "UserRole",
    back_populates="role",
    cascade="all, delete-orphan"
)
Permission.role_permissions = relationship(
    "RolePermission",
    back_populates="permission",
    cascade="all, delete-orphan",
    overlaps="permissions,roles"
)
Permission.roles = relationship(
    "Role",
    secondary="role_permissions",
    back_populates="permissions",
    overlaps="role_permissions,role"
)
RolePermission.role = relationship(
    "Role",
    back_populates="role_permissions",
    overlaps="permissions,roles"
)
RolePermission.permission = relationship(
    "Permission",
    back_populates="role_permissions",
    overlaps="permissions,roles"
)
UserRole.user = relationship(
    "User",
    back_populates="user_roles"
)
UserRole.role = relationship(
    "Role",
    back_populates="user_roles"
)

# Export all models
__all__ = [
    "Base",
    "User",
    "RefreshToken",
    "PasswordResetToken",
    "EmailVerificationToken",
    "Project",
    "Vote",
    "Comment",
    "CommentVote",
    "Hackathon",
    "HackathonRegistration",
    "Team",
    "TeamMember",
    "TeamInvitation",
    "TeamReport",
    "Report",
    "Role",
    "Permission",
    "RolePermission",
    "UserRole",
    "NotificationType",
    "UserNotification",
    "NotificationDelivery",
    "UserNotificationPreference",
    "PushSubscription",
    "File",
    "NewsletterSubscription",
    "ChatRoom",
    "ChatMessage",
    "ChatParticipant",
]
