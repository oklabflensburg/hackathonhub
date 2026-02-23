"""
Pydantic schemas for the domain models.
"""
from .user import User, UserCreate, UserUpdate, UserWithDetails
from .project import (
    Project, ProjectCreate, ProjectUpdate,
    Vote, VoteCreate, Comment, CommentCreate
)
from .hackathon import (
    Hackathon, HackathonCreate, HackathonUpdate, HackathonRegistration
)
from .team import (
    Team, TeamCreate, TeamUpdate,
    TeamMember, TeamMemberCreate, TeamMemberUpdate,
    TeamInvitation, TeamInvitationCreate,
    TeamWithMembers, TeamWithProjects
)
from .notification import (
    NotificationType, NotificationTypeCreate,
    UserNotification, UserNotificationCreate,
    UserNotificationPreference, UserNotificationPreferenceCreate,
    PushSubscription, PushSubscriptionCreate
)

__all__ = [
    "User",
    "UserCreate",
    "UserUpdate",
    "UserWithDetails",
    "Project",
    "ProjectCreate",
    "ProjectUpdate",
    "Hackathon",
    "HackathonCreate",
    "HackathonUpdate",
    "HackathonRegistration",
    "Team",
    "TeamCreate",
    "TeamUpdate",
    "TeamMember",
    "TeamMemberCreate",
    "TeamMemberUpdate",
    "TeamInvitation",
    "TeamInvitationCreate",
    "TeamWithMembers",
    "TeamWithProjects",
    "NotificationType",
    "NotificationTypeCreate",
    "UserNotification",
    "UserNotificationCreate",
    "UserNotificationPreference",
    "UserNotificationPreferenceCreate",
    "PushSubscription",
    "PushSubscriptionCreate",
    "Vote",
    "VoteCreate",
    "Comment",
    "CommentCreate",
]

# Rebuild models with forward refs once all schemas are imported.
Project.model_rebuild(_types_namespace={"Team": Team})
TeamWithProjects.model_rebuild(_types_namespace={"Project": Project})