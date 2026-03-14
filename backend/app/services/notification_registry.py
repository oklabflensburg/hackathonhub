"""Canonical notification type registry."""
import logging
from dataclasses import dataclass
from typing import Dict, Iterable, Optional, Tuple, List

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.models.notification import NotificationType
from app.utils.cache import cache_manager, cached

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class NotificationDefinition:
    type_key: str
    category: str
    default_channels: Tuple[str, ...]
    description: str
    help_text: str
    help_text_key: str
    email_template: Optional[str] = None


# Cache TTL in seconds (5 minutes)
CACHE_TTL = 300


def _convert_db_to_definition(
    db_type: NotificationType
) -> NotificationDefinition:
    """Convert database NotificationType to NotificationDefinition."""
    # Parse default_channels from comma-separated string to tuple
    channels_str = db_type.default_channels or ""
    channels = tuple(
        channel.strip() for channel in channels_str.split(",")
        if channel.strip()
    ) if channels_str else ()

    return NotificationDefinition(
        type_key=db_type.type_key,
        category=db_type.category,
        default_channels=channels,
        description=db_type.description or "",
        help_text=db_type.help_text or "",
        help_text_key=db_type.help_text_key or "",
        email_template=db_type.email_template
    )


def _load_definitions_from_db(db: Session) -> List[NotificationDefinition]:
    """Load notification definitions from database."""
    try:
        db_types = db.query(NotificationType).order_by(
            NotificationType.sort_order,
            NotificationType.id
        ).all()

        if not db_types:
            logger.warning(
                "No notification types found in database, "
                "using embedded definitions"
            )
            return _load_embedded_definitions()

        return [_convert_db_to_definition(db_type) for db_type in db_types]
    except Exception as e:
        logger.error(f"Error querying database: {e}")
        # Fallback to embedded definitions
        return _load_embedded_definitions()


def _load_embedded_definitions() -> List[NotificationDefinition]:
    """Load notification definitions from embedded data."""
    # Embedded definitions as tuples (same as seed script)
    embedded_defs = [
        ("team_invitation", "team", "email,push,in_app",
         "When you're invited to join a team",
         "Alerts you when another participant invites you to a team.",
         "notifications.help_text.team_invitation", "team/invitation_sent"),
        ("team_invitation_accepted", "team", "email,in_app",
         "When someone accepts your team invitation",
         "Lets you know that an invited member has joined your team.",
         "notifications.help_text.team_invitation_accepted",
         "team/invitation_accepted"),
        ("team_invitation_declined", "team", "email,in_app",
         "When someone declines your team invitation",
         "Informs you when an invitation is declined.",
         "notifications.help_text.team_invitation_declined", None),
        ("team_member_added", "team", "email,push,in_app",
         "When you're added to a team",
         "Notifies you that you were added to a team.",
         "notifications.help_text.team_member_added", "team/member_added"),
        ("team_created", "team", "email,in_app",
         "When a team is created",
         "Confirms team creation and keeps new collaboration spaces visible.",
         "notifications.help_text.team_created", "team/created"),
        ("project_created", "project", "email,push,in_app",
         "When a project is created in your team",
         "Tells you when a new project appears in your team.",
         "notifications.help_text.project_created", "project/created"),
        ("project_commented", "project", "email,push,in_app",
         "When someone comments on your project",
         "Highlights new project discussion and feedback.",
         "notifications.help_text.project_commented", "project/commented"),
        ("hackathon_registered", "hackathon", "email,in_app",
         "When you register for a hackathon",
         "Confirms successful registration for a hackathon.",
         "notifications.help_text.hackathon_registered",
         "hackathon/registered"),
        ("hackathon_started", "hackathon", "email,push,in_app",
         "When a hackathon starts",
         "Signals the official start of a hackathon.",
         "notifications.help_text.hackathon_started", "hackathon/started"),
        ("hackathon_start_reminder", "hackathon", "email,push",
         "When a hackathon starts soon",
         "Sends a reminder shortly before hackathon kickoff.",
         "notifications.help_text.hackathon_start_reminder", None),
        ("comment_reply", "system", "email,push,in_app",
         "When someone replies to your comment",
         "Keeps threaded conversations visible when someone replies.",
         "notifications.help_text.comment_reply", None),
        ("vote_received", "system", "in_app",
         "When your project receives a vote",
         "Shows engagement with your project inside the app.",
         "notifications.help_text.vote_received", None),
        ("system_announcement", "system", "email,in_app",
         "System announcements and updates",
         "Covers platform-wide announcements and operational updates.",
         "notifications.help_text.system_announcement", None),
        ("security_alert", "system", "email,push",
         "Security alerts and account notifications",
         "Reserved for security-sensitive events that may need action.",
         "notifications.help_text.security_alert", None),
        ("verification_confirmed", "system", "email,in_app",
         "When email verification succeeds",
         "Confirms that your email address was verified.",
         "notifications.help_text.verification_confirmed",
         "verification_confirmed"),
        ("password_reset_confirmed", "system", "email",
         "When a password reset is confirmed",
         "Confirms that a password reset request was completed.",
         "notifications.help_text.password_reset_confirmed",
         "password_reset_confirmed"),
        ("password_changed", "system", "email",
         "When a password changes",
         "Warns you whenever the account password changes.",
         "notifications.help_text.password_changed", "password_changed"),
        ("newsletter_unsubscribed", "system", "email",
         "When newsletter preferences change",
         "Records changes to newsletter communication preferences.",
         "notifications.help_text.newsletter_unsubscribed",
         "newsletter_unsubscribed"),
        ("security_login_new_device", "system", "email,push",
         "When a new device logs in",
         "Notifies you about sign-ins from new devices.",
         "notifications.help_text.security_login_new_device",
         "security_login_new_device"),
        ("settings_changed", "system", "email",
         "When account settings change",
         "Confirms sensitive account setting changes.",
         "notifications.help_text.settings_changed", "settings_changed"),
    ]

    definitions = []
    for (type_key, category, channels_str, description,
         help_text, help_text_key, email_template) in embedded_defs:
        channels = tuple(
            channel.strip() for channel in channels_str.split(",")
            if channel.strip()
        ) if channels_str else ()

        definitions.append(NotificationDefinition(
            type_key=type_key,
            category=category,
            default_channels=channels,
            description=description,
            help_text=help_text,
            help_text_key=help_text_key,
            email_template=email_template
        ))

    logger.info(f"Loaded {len(definitions)} embedded notification definitions")
    return definitions


@cached(ttl=CACHE_TTL)
def get_all_definitions() -> List[NotificationDefinition]:
    """Get all notification definitions with caching."""
    db = next(get_db())
    try:
        return _load_definitions_from_db(db)
    except Exception as e:
        logger.error(f"Failed to load notification definitions: {e}")
        # Re-raise the exception - let the caller handle it
        raise
    finally:
        db.close()


@cached(ttl=CACHE_TTL)
def get_definition_map() -> Dict[str, NotificationDefinition]:
    """Get notification definition map with caching."""
    definitions = get_all_definitions()
    return {definition.type_key: definition for definition in definitions}


def get_definition(type_key: str) -> Optional[NotificationDefinition]:
    """Get a notification definition by type key."""
    try:
        definition_map = get_definition_map()
        return definition_map.get(type_key)
    except Exception:
        # If we can't load definitions, return None
        logger.error(f"Failed to get definition for type_key: {type_key}")
        return None


def is_known_type(type_key: str) -> bool:
    """Check if a notification type is known."""
    try:
        definition_map = get_definition_map()
        return type_key in definition_map
    except Exception:
        # If we can't load definitions, assume type is not known
        logger.error(f"Failed to check if type is known: {type_key}")
        return False


def iter_definitions() -> Iterable[NotificationDefinition]:
    """Iterate over all notification definitions."""
    try:
        return get_all_definitions()
    except Exception:
        # Return empty iterable if we can't load definitions
        logger.error("Failed to iterate definitions")
        return []


def refresh_cache() -> None:
    """Refresh the notification definitions cache."""
    cache_manager.clear()
    # Trigger reload on next access
    try:
        get_all_definitions()
        get_definition_map()
    except Exception as e:
        logger.error(f"Failed to refresh cache: {e}")


# Initialize on module import (will fail if database is not ready)
try:
    NOTIFICATION_DEFINITIONS = tuple(get_all_definitions())
    NOTIFICATION_DEFINITION_MAP = get_definition_map()
except Exception as e:
    logger.error(f"Failed to initialize notification registry: {e}")
    # Initialize with empty values - will be populated on first access
    NOTIFICATION_DEFINITIONS = ()
    NOTIFICATION_DEFINITION_MAP = {}
