"""
Canonical notification type registry.
"""
from dataclasses import dataclass
from typing import Dict, Iterable, Optional, Tuple


@dataclass(frozen=True)
class NotificationDefinition:
    type_key: str
    category: str
    default_channels: Tuple[str, ...]
    description: str
    email_template: Optional[str] = None


NOTIFICATION_DEFINITIONS = (
    NotificationDefinition(
        type_key="team_invitation",
        category="team",
        default_channels=("email", "push", "in_app"),
        description="When you're invited to join a team",
        email_template="team/invitation_sent",
    ),
    NotificationDefinition(
        type_key="team_invitation_accepted",
        category="team",
        default_channels=("email", "in_app"),
        description="When someone accepts your team invitation",
        email_template="team/invitation_accepted",
    ),
    NotificationDefinition(
        type_key="team_invitation_declined",
        category="team",
        default_channels=("email", "in_app"),
        description="When someone declines your team invitation",
    ),
    NotificationDefinition(
        type_key="team_member_added",
        category="team",
        default_channels=("email", "push", "in_app"),
        description="When you're added to a team",
        email_template="team/member_added",
    ),
    NotificationDefinition(
        type_key="team_created",
        category="team",
        default_channels=("email", "in_app"),
        description="When a team is created",
        email_template="team/created",
    ),
    NotificationDefinition(
        type_key="project_created",
        category="project",
        default_channels=("email", "push", "in_app"),
        description="When a project is created in your team",
        email_template="project/created",
    ),
    NotificationDefinition(
        type_key="project_commented",
        category="project",
        default_channels=("email", "push", "in_app"),
        description="When someone comments on your project",
        email_template="project/commented",
    ),
    NotificationDefinition(
        type_key="hackathon_registered",
        category="hackathon",
        default_channels=("email", "in_app"),
        description="When you register for a hackathon",
        email_template="hackathon/registered",
    ),
    NotificationDefinition(
        type_key="hackathon_started",
        category="hackathon",
        default_channels=("email", "push", "in_app"),
        description="When a hackathon starts",
        email_template="hackathon/started",
    ),
    NotificationDefinition(
        type_key="hackathon_start_reminder",
        category="hackathon",
        default_channels=("email", "push"),
        description="When a hackathon starts soon",
    ),
    NotificationDefinition(
        type_key="comment_reply",
        category="system",
        default_channels=("email", "push", "in_app"),
        description="When someone replies to your comment",
    ),
    NotificationDefinition(
        type_key="vote_received",
        category="system",
        default_channels=("in_app",),
        description="When your project receives a vote",
    ),
    NotificationDefinition(
        type_key="system_announcement",
        category="system",
        default_channels=("email", "in_app"),
        description="System announcements and updates",
    ),
    NotificationDefinition(
        type_key="security_alert",
        category="system",
        default_channels=("email", "push"),
        description="Security alerts and account notifications",
    ),
    NotificationDefinition(
        type_key="verification_confirmed",
        category="system",
        default_channels=("email", "in_app"),
        description="When email verification succeeds",
        email_template="verification_confirmed",
    ),
    NotificationDefinition(
        type_key="password_reset_confirmed",
        category="system",
        default_channels=("email",),
        description="When a password reset is confirmed",
        email_template="password_reset_confirmed",
    ),
    NotificationDefinition(
        type_key="password_changed",
        category="system",
        default_channels=("email",),
        description="When a password changes",
        email_template="password_changed",
    ),
    NotificationDefinition(
        type_key="newsletter_unsubscribed",
        category="system",
        default_channels=("email",),
        description="When newsletter preferences change",
        email_template="newsletter_unsubscribed",
    ),
    NotificationDefinition(
        type_key="security_login_new_device",
        category="system",
        default_channels=("email", "push"),
        description="When a new device logs in",
        email_template="security_login_new_device",
    ),
    NotificationDefinition(
        type_key="settings_changed",
        category="system",
        default_channels=("email",),
        description="When account settings change",
        email_template="settings_changed",
    ),
)

NOTIFICATION_DEFINITION_MAP: Dict[str, NotificationDefinition] = {
    definition.type_key: definition for definition in NOTIFICATION_DEFINITIONS
}


def get_definition(type_key: str) -> Optional[NotificationDefinition]:
    return NOTIFICATION_DEFINITION_MAP.get(type_key)


def is_known_type(type_key: str) -> bool:
    return type_key in NOTIFICATION_DEFINITION_MAP


def iter_definitions() -> Iterable[NotificationDefinition]:
    return NOTIFICATION_DEFINITIONS
