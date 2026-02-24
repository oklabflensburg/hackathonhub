"""
Pydantic schemas for the domain models.
"""
from typing import List, Optional
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
    TeamMember, TeamMemberCreate, TeamMemberCreateRequest, TeamMemberUpdate,
    TeamInvitation, TeamInvitationCreate, TeamInvitationCreateRequest,
    TeamWithMembers, TeamWithProjects
)
from .notification import (
    NotificationType, NotificationTypeCreate,
    UserNotification, UserNotificationCreate,
    UserNotificationPreference, UserNotificationPreferenceCreate,
    PushSubscription, PushSubscriptionCreate
)
from .newsletter import (
    NewsletterSubscription, NewsletterSubscriptionCreate,
    NewsletterSubscribeRequest, NewsletterUnsubscribeRequest
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
    "TeamMemberCreateRequest",
    "TeamMemberUpdate",
    "TeamInvitation",
    "TeamInvitationCreate",
    "TeamInvitationCreateRequest",
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
    "NewsletterSubscription",
    "NewsletterSubscriptionCreate",
    "NewsletterSubscribeRequest",
    "NewsletterUnsubscribeRequest",
]

# Rebuild models with forward refs once all schemas are imported.
_types_namespace = {
    "Comment": Comment,
    "Hackathon": Hackathon,
    "HackathonRegistration": HackathonRegistration,
    "List": List,
    "Optional": Optional,
    "Project": Project,
    "Team": Team,
    "TeamMember": TeamMember,
    "User": User,
    "Vote": Vote,
}
Project.model_rebuild(_types_namespace=_types_namespace)
Hackathon.model_rebuild(_types_namespace=_types_namespace)
HackathonRegistration.model_rebuild(_types_namespace=_types_namespace)
Team.model_rebuild(_types_namespace=_types_namespace)
TeamMember.model_rebuild(_types_namespace=_types_namespace)
TeamInvitation.model_rebuild(_types_namespace=_types_namespace)
TeamWithMembers.model_rebuild(_types_namespace=_types_namespace)
TeamWithProjects.model_rebuild(_types_namespace=_types_namespace)
UserNotificationPreference.model_rebuild(_types_namespace=_types_namespace)
UserNotification.model_rebuild(_types_namespace=_types_namespace)
PushSubscription.model_rebuild(_types_namespace=_types_namespace)
UserWithDetails.model_rebuild(_types_namespace=_types_namespace)
