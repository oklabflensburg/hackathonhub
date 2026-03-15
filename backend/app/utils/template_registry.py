"""
Template Registry with Type Safety.
Provides type-safe template definitions and validation.
"""
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict
from dataclasses import dataclass, field
from enum import Enum


class TemplateCategory(str, Enum):
    """Categories of email templates."""
    VERIFICATION = "verification"
    PASSWORD_RESET = "password_reset"
    NEWSLETTER = "newsletter"
    TEAM = "team"
    PROJECT = "project"
    HACKATHON = "hackathon"
    NOTIFICATION = "notification"
    SECURITY = "security"
    SETTINGS = "settings"


class TemplateVariable(TypedDict):
    """Type definition for template variables."""
    name: str
    description: str
    required: bool
    example: str


@dataclass
class TemplateDefinition:
    """Definition of an email template with type safety."""
    name: str
    category: TemplateCategory
    description: str
    variables: List[TemplateVariable]
    languages: List[str] = field(default_factory=lambda: ["en", "de"])
    subject_key: Optional[str] = None
    title_key: Optional[str] = None

    def validate_variables(self, provided_vars: Dict[str, str]) -> List[str]:
        """Validate provided variables against template definition."""
        errors = []

        # Check required variables
        for var_def in self.variables:
            if var_def["required"] and var_def["name"] not in provided_vars:
                errors.append(
                    f"Missing required variable: {var_def['name']} "
                    f"({var_def['description']})"
                )

        # Check for extra variables (warn but don't fail)
        provided_names = set(provided_vars.keys())
        defined_names = {var_def["name"] for var_def in self.variables}
        extra_vars = provided_names - defined_names

        if extra_vars:
            # Log warning but don't fail
            print(f"Warning: Extra variables provided: {extra_vars}")

        return errors

    def get_variable_docs(self) -> str:
        """Generate documentation for template variables."""
        lines = [f"Template: {self.name}", f"Description: {self.description}"]
        lines.append("Variables:")

        for var_def in self.variables:
            required = "REQUIRED" if var_def["required"] else "optional"
            lines.append(
                f"  - {var_def['name']}: {var_def['description']} "
                f"({required})"
            )
            if var_def["example"]:
                lines.append(f"    Example: {var_def['example']}")

        return "\n".join(lines)


class TemplateRegistry:
    """Registry of all email templates with type-safe definitions."""

    TEMPLATE_ROOT = (
        Path(__file__).resolve().parents[2] / "templates" / "emails"
    )
    COMMON_TEMPLATE_VARIABLES = {
        "subject",
        "title",
        "content",
        "current_year",
        "lang",
        "notification_title",
        "notification_message",
    }
    TEMPLATE_LANGUAGES = ("en", "de")
    _JINJA_IDENTIFIER_RE = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b")
    _JINJA_EXPRESSION_RE = re.compile(r"(\{\{.*?\}\}|\{%.*?%\})", re.DOTALL)
    _JINJA_RESERVED_NAMES = {
        "true",
        "false",
        "none",
        "and",
        "or",
        "not",
        "in",
        "if",
        "else",
        "elif",
        "endif",
        "for",
        "endfor",
        "set",
        "with",
        "endwith",
    }

    # Template definitions
    TEMPLATES: Dict[str, TemplateDefinition] = {
        "verification": TemplateDefinition(
            name="verification",
            category=TemplateCategory.VERIFICATION,
            description="Email verification for new user registration",
            variables=[
                {
                    "name": "user_name",
                    "description": "Name of the user",
                    "required": True,
                    "example": "John Doe"
                },
                {
                    "name": "verification_url",
                    "description": "URL for email verification",
                    "required": True,
                    "example": "https://example.com/verify?token=abc123"
                },
                {
                    "name": "expiration_hours",
                    "description": "Hours until token expires",
                    "required": False,
                    "example": "24"
                }
            ],
            subject_key="email.verification_subject",
            title_key="email.verification_title"
        ),

        "password_reset": TemplateDefinition(
            name="password_reset",
            category=TemplateCategory.PASSWORD_RESET,
            description="Password reset request",
            variables=[
                {
                    "name": "user_name",
                    "description": "Name of the user",
                    "required": True,
                    "example": "Jane Smith"
                },
                {
                    "name": "reset_url",
                    "description": "URL for password reset",
                    "required": True,
                    "example": "https://example.com/reset?token=xyz789"
                },
                {
                    "name": "expiration_hours",
                    "description": "Hours until token expires",
                    "required": False,
                    "example": "1"
                }
            ],
            subject_key="email.password_reset_subject",
            title_key="email.password_reset_title"
        ),

        "team/invitation_sent": TemplateDefinition(
            name="team/invitation_sent",
            category=TemplateCategory.TEAM,
            description="Team invitation sent to user",
            variables=[
                {
                    "name": "team_name",
                    "description": "Name of the team",
                    "required": True,
                    "example": "Awesome Team"
                },
                {
                    "name": "inviter_name",
                    "description": "Name of the person who sent invitation",
                    "required": True,
                    "example": "Alice Johnson"
                },
                {
                    "name": "accept_url",
                    "description": "URL to accept the invitation",
                    "required": True,
                    "example": "https://example.com/team/accept?token=inv123"
                },
                {
                    "name": "recipient_name",
                    "description": "Display name of the recipient",
                    "required": False,
                    "example": "Bob Wilson"
                },
                {
                    "name": "actor_name",
                    "description": "Fallback actor display name",
                    "required": False,
                    "example": "Alice Johnson"
                },
                {
                    "name": "invitation_url",
                    "description": "Alias URL to view the invitation",
                    "required": False,
                    "example": "https://example.com/team/invitations/123"
                },
                {
                    "name": "team_description",
                    "description": "Optional description of the team",
                    "required": False,
                    "example": "We build a sustainability app."
                },
                {
                    "name": "hackathon_name",
                    "description": "Hackathon name for the team",
                    "required": False,
                    "example": "Global Hackathon 2026"
                },
                {
                    "name": "expiration_date",
                    "description": "Invitation expiration date",
                    "required": False,
                    "example": "2026-04-10 18:00"
                }
            ],
            subject_key="email.team_invitation_subject",
            title_key="email.team_invitation_title"
        ),

        "team/invitation_accepted": TemplateDefinition(
            name="team/invitation_accepted",
            category=TemplateCategory.TEAM,
            description="Notification that team invitation was accepted",
            variables=[
                {
                    "name": "team_name",
                    "description": "Name of the team",
                    "required": True,
                    "example": "Awesome Team"
                },
                {
                    "name": "user_name",
                    "description": "Name of the user who accepted",
                    "required": True,
                    "example": "Bob Wilson"
                },
                {
                    "name": "recipient_name",
                    "description": "Display name of the recipient",
                    "required": False,
                    "example": "Alice Johnson"
                },
                {
                    "name": "actor_name",
                    "description": "Fallback actor display name",
                    "required": False,
                    "example": "Bob Wilson"
                },
                {
                    "name": "team_description",
                    "description": "Optional description of the team",
                    "required": False,
                    "example": "We build a sustainability app."
                },
                {
                    "name": "hackathon_name",
                    "description": "Hackathon name for the team",
                    "required": False,
                    "example": "Global Hackathon 2026"
                },
                {
                    "name": "member_role",
                    "description": "Role of the newly accepted member",
                    "required": False,
                    "example": "Developer"
                },
                {
                    "name": "team_url",
                    "description": "URL to open the team",
                    "required": False,
                    "example": "https://example.com/teams/123"
                },
                {
                    "name": "team_dashboard_url",
                    "description": "Fallback dashboard URL for the team",
                    "required": False,
                    "example": "https://example.com/teams/123/dashboard"
                },
                {
                    "name": "member_count",
                    "description": "Current team member count",
                    "required": False,
                    "example": "4"
                }
            ],
            subject_key="email.team_invitation_accepted_subject",
            title_key="email.team_invitation_accepted_title"
        ),

        "team/member_added": TemplateDefinition(
            name="team/member_added",
            category=TemplateCategory.TEAM,
            description="Notification that member was added to team",
            variables=[
                {
                    "name": "team_name",
                    "description": "Name of the team",
                    "required": True,
                    "example": "Awesome Team"
                },
                {
                    "name": "added_by_name",
                    "description": "Name of the person who added the member",
                    "required": True,
                    "example": "Charlie Brown"
                },
                {
                    "name": "recipient_name",
                    "description": "Display name of the recipient",
                    "required": False,
                    "example": "Bob Wilson"
                },
                {
                    "name": "actor_name",
                    "description": "Fallback actor display name",
                    "required": False,
                    "example": "Charlie Brown"
                },
                {
                    "name": "team_description",
                    "description": "Optional description of the team",
                    "required": False,
                    "example": "We build a sustainability app."
                },
                {
                    "name": "hackathon_name",
                    "description": "Hackathon name for the team",
                    "required": False,
                    "example": "Global Hackathon 2026"
                },
                {
                    "name": "member_role",
                    "description": "Role assigned to the recipient",
                    "required": False,
                    "example": "Developer"
                },
                {
                    "name": "team_url",
                    "description": "URL to open the team",
                    "required": False,
                    "example": "https://example.com/teams/123"
                },
                {
                    "name": "team_dashboard_url",
                    "description": "Fallback dashboard URL for the team",
                    "required": False,
                    "example": "https://example.com/teams/123/dashboard"
                },
                {
                    "name": "member_count",
                    "description": "Current team member count",
                    "required": False,
                    "example": "4"
                }
            ],
            subject_key="email.team_member_added_subject",
            title_key="email.team_member_added_title"
        ),

        "team/created": TemplateDefinition(
            name="team/created",
            category=TemplateCategory.TEAM,
            description="Notification that team was created",
            variables=[
                {
                    "name": "team_name",
                    "description": "Name of the team",
                    "required": True,
                    "example": "Innovation Squad"
                },
                {
                    "name": "creator_name",
                    "description": "Name of the team creator",
                    "required": True,
                    "example": "Eva Garcia"
                },
                {
                    "name": "team_id",
                    "description": "ID of the team",
                    "required": False,
                    "example": "789"
                },
                {
                    "name": "user_name",
                    "description": "Display name of the recipient",
                    "required": False,
                    "example": "Eva Garcia"
                },
                {
                    "name": "creation_date",
                    "description": "Date when the team was created",
                    "required": False,
                    "example": "2026-04-01 09:00"
                },
                {
                    "name": "hackathon_name",
                    "description": "Associated hackathon name",
                    "required": False,
                    "example": "Global Hackathon 2026"
                },
                {
                    "name": "team_dashboard_url",
                    "description": "URL to open the team dashboard",
                    "required": False,
                    "example": "https://example.com/teams/789/dashboard"
                },
                {
                    "name": "team_url",
                    "description": "Fallback URL to the team",
                    "required": False,
                    "example": "https://example.com/teams/789"
                },
                {
                    "name": "invite_members_url",
                    "description": "URL to invite more members",
                    "required": False,
                    "example": "https://example.com/teams/789/invite"
                },
                {
                    "name": "help_center_url",
                    "description": "Help center URL",
                    "required": False,
                    "example": "https://example.com/help"
                }
            ],
            subject_key="email.team_created_subject",
            title_key="email.team_created_title"
        ),

        "project/created": TemplateDefinition(
            name="project/created",
            category=TemplateCategory.PROJECT,
            description="Notification that project was created",
            variables=[
                {
                    "name": "project_name",
                    "description": "Name of the project",
                    "required": True,
                    "example": "Hackathon Dashboard"
                },
                {
                    "name": "creator_name",
                    "description": "Name of the project creator",
                    "required": True,
                    "example": "Frank Miller"
                },
                {
                    "name": "project_url",
                    "description": "URL to view the project",
                    "required": True,
                    "example": "https://example.com/projects/123"
                },
                {
                    "name": "recipient_name",
                    "description": "Display name of the recipient",
                    "required": False,
                    "example": "Bob Wilson"
                },
                {
                    "name": "user_name",
                    "description": "Fallback recipient display name",
                    "required": False,
                    "example": "Bob Wilson"
                },
                {
                    "name": "actor_name",
                    "description": "Fallback creator display name",
                    "required": False,
                    "example": "Frank Miller"
                },
                {
                    "name": "project_title",
                    "description": "Alias project title",
                    "required": False,
                    "example": "Hackathon Dashboard"
                },
                {
                    "name": "project_description",
                    "description": "Optional project description",
                    "required": False,
                    "example": "A platform for hackathon coordination."
                },
                {
                    "name": "project_technologies",
                    "description": "Optional project technologies",
                    "required": False,
                    "example": "Vue, FastAPI, PostgreSQL"
                },
                {
                    "name": "hackathon_name",
                    "description": "Associated hackathon name",
                    "required": False,
                    "example": "Global Hackathon 2026"
                },
                {
                    "name": "team_name",
                    "description": "Associated team name",
                    "required": False,
                    "example": "Innovation Squad"
                }
            ],
            subject_key="email.project_created_subject",
            title_key="email.project_created_title"
        ),

        "project/commented": TemplateDefinition(
            name="project/commented",
            category=TemplateCategory.PROJECT,
            description="Notification that project received a comment",
            variables=[
                {
                    "name": "project_name",
                    "description": "Name of the project",
                    "required": True,
                    "example": "Hackathon Dashboard"
                },
                {
                    "name": "commenter_name",
                    "description": "Name of the person who commented",
                    "required": True,
                    "example": "Grace Lee"
                },
                {
                    "name": "comment_preview",
                    "description": "Preview of the comment",
                    "required": True,
                    "example": "Great project! I have some suggestions..."
                },
                {
                    "name": "project_url",
                    "description": "URL to view the project and comment",
                    "required": True,
                    "example": "https://example.com/projects/123"
                },
                {
                    "name": "user_name",
                    "description": "Display name of the recipient",
                    "required": False,
                    "example": "Bob Wilson"
                },
                {
                    "name": "hackathon_name",
                    "description": "Associated hackathon name",
                    "required": False,
                    "example": "Global Hackathon 2026"
                },
                {
                    "name": "comment_date",
                    "description": "Date of the comment",
                    "required": False,
                    "example": "2026-04-01 10:30"
                },
                {
                    "name": "reply_url",
                    "description": "URL to reply to the comment",
                    "required": False,
                    "example": "https://example.com/projects/123#reply"
                },
                {
                    "name": "unsubscribe_url",
                    "description": "URL to unsubscribe from comment notifications",
                    "required": False,
                    "example": "https://example.com/settings/notifications"
                },
                {
                    "name": "comment_is_truncated",
                    "description": "Whether the comment preview is truncated",
                    "required": False,
                    "example": "false"
                }
            ],
            subject_key="email.project_commented_subject",
            title_key="email.project_commented_title"
        ),

        "hackathon/registered": TemplateDefinition(
            name="hackathon/registered",
            category=TemplateCategory.HACKATHON,
            description="Confirmation of hackathon registration",
            variables=[
                {
                    "name": "hackathon_name",
                    "description": "Name of the hackathon",
                    "required": True,
                    "example": "Global Hackathon 2026"
                },
                {
                    "name": "user_name",
                    "description": "Name of the registered user",
                    "required": True,
                    "example": "Henry Ford"
                },
                {
                    "name": "hackathon_date",
                    "description": "Date of the hackathon",
                    "required": True,
                    "example": "2026-04-15"
                },
                {
                    "name": "hackathon_url",
                    "description": "URL to hackathon details",
                    "required": True,
                    "example": "https://example.com/hackathons/456"
                },
                {
                    "name": "hackathon_location",
                    "description": "Hackathon location",
                    "required": False,
                    "example": "Berlin"
                },
                {
                    "name": "registration_id",
                    "description": "Registration identifier",
                    "required": False,
                    "example": "REG-2026-001"
                },
                {
                    "name": "organizer_email",
                    "description": "Organizer contact email",
                    "required": False,
                    "example": "team@example.com"
                }
            ],
            subject_key="email.hackathon_registered_subject",
            title_key="email.hackathon_registered_title"
        ),

        "hackathon/started": TemplateDefinition(
            name="hackathon/started",
            category=TemplateCategory.HACKATHON,
            description="Notification that hackathon has started",
            variables=[
                {
                    "name": "hackathon_name",
                    "description": "Name of the hackathon",
                    "required": True,
                    "example": "Global Hackathon 2026"
                },
                {
                    "name": "user_name",
                    "description": "Name of the registered user",
                    "required": True,
                    "example": "Henry Ford"
                },
                {
                    "name": "start_time",
                    "description": "Start time of the hackathon",
                    "required": True,
                    "example": "2026-04-15 09:00:00"
                },
                {
                    "name": "hackathon_dashboard_url",
                    "description": "URL to hackathon dashboard",
                    "required": True,
                    "example": "https://example.com/hackathons/456/dashboard"
                },
                {
                    "name": "end_time",
                    "description": "Hackathon end time",
                    "required": False,
                    "example": "2026-04-02 18:00"
                },
                {
                    "name": "duration_hours",
                    "description": "Hackathon duration in hours",
                    "required": False,
                    "example": "36"
                },
                {
                    "name": "current_phase",
                    "description": "Current hackathon phase",
                    "required": False,
                    "example": "Build phase"
                },
                {
                    "name": "submission_portal_url",
                    "description": "Submission portal URL",
                    "required": False,
                    "example": "https://example.com/submissions"
                },
                {
                    "name": "slack_channel_url",
                    "description": "Slack/community URL",
                    "required": False,
                    "example": "https://example.slack.com"
                },
                {
                    "name": "resources_url",
                    "description": "Resources and docs URL",
                    "required": False,
                    "example": "https://example.com/resources"
                },
                {
                    "name": "mentor_schedule_url",
                    "description": "Mentor schedule URL",
                    "required": False,
                    "example": "https://example.com/mentors"
                }
            ],
            subject_key="email.hackathon_started_subject",
            title_key="email.hackathon_started_title"
        ),

        "newsletter_welcome": TemplateDefinition(
            name="newsletter_welcome",
            category=TemplateCategory.NEWSLETTER,
            description="Welcome email for newsletter subscribers",
            variables=[
                {
                    "name": "unsubscribe_url",
                    "description": "URL to unsubscribe from newsletter",
                    "required": True,
                    "example": "https://example.com/unsubscribe"
                }
            ],
            subject_key="email.newsletter_welcome_subject",
            title_key="email.newsletter_welcome_title"
        ),

        # New confirmation templates
        "verification_confirmed": TemplateDefinition(
            name="verification_confirmed",
            category=TemplateCategory.VERIFICATION,
            description="Confirmation email after successful email verification",  # noqa: E501
            variables=[
                {
                    "name": "user_name",
                    "description": "Name of the user",
                    "required": True,
                    "example": "John Doe"
                },
                {
                    "name": "verification_date",
                    "description": "Date when email was verified",
                    "required": False,
                    "example": "2026-03-13 11:30:00"
                }
            ],
            subject_key="email.verification_confirmed_subject",
            title_key="email.verification_confirmed_title"
        ),

        "password_reset_confirmed": TemplateDefinition(
            name="password_reset_confirmed",
            category=TemplateCategory.SECURITY,
            description="Confirmation email after successful password reset",
            variables=[
                {
                    "name": "user_name",
                    "description": "Name of the user",
                    "required": True,
                    "example": "Jane Smith"
                },
                {
                    "name": "reset_date",
                    "description": "Date when password was reset",
                    "required": False,
                    "example": "2026-03-13 11:45:00"
                },
                {
                    "name": "ip_address",
                    "description": "IP address used for reset",
                    "required": False,
                    "example": "192.168.1.100"
                }
            ],
            subject_key="email.password_reset_confirmed_subject",
            title_key="email.password_reset_confirmed_title"
        ),

        "password_changed": TemplateDefinition(
            name="password_changed",
            category=TemplateCategory.SECURITY,
            description="Security notification when password is changed",
            variables=[
                {
                    "name": "user_name",
                    "description": "Name of the user",
                    "required": True,
                    "example": "John Doe"
                },
                {
                    "name": "change_date",
                    "description": "Date when password was changed",
                    "required": True,
                    "example": "2026-03-13 12:00:00"
                },
                {
                    "name": "ip_address",
                    "description": "IP address used for change",
                    "required": False,
                    "example": "192.168.1.100"
                },
                {
                    "name": "device_info",
                    "description": "Device/browser information",
                    "required": False,
                    "example": "Chrome on Windows 10"
                }
            ],
            subject_key="email.password_changed_subject",
            title_key="email.password_changed_title"
        ),

        "newsletter_unsubscribed": TemplateDefinition(
            name="newsletter_unsubscribed",
            category=TemplateCategory.NEWSLETTER,
            description="Confirmation email after unsubscribing from newsletter",  # noqa: E501
            variables=[
                {
                    "name": "email",
                    "description": "Email address that was unsubscribed",
                    "required": True,
                    "example": "user@example.com"
                },
                {
                    "name": "unsubscribe_date",
                    "description": "Date when unsubscribed",
                    "required": False,
                    "example": "2026-03-13 12:15:00"
                }
            ],
            subject_key="email.newsletter_unsubscribed_subject",
            title_key="email.newsletter_unsubscribed_title"
        ),

        "security_login_new_device": TemplateDefinition(
            name="security_login_new_device",
            category=TemplateCategory.SECURITY,
            description="Security alert for login from new device/location",
            variables=[
                {
                    "name": "user_name",
                    "description": "Name of the user",
                    "required": True,
                    "example": "John Doe"
                },
                {
                    "name": "login_time",
                    "description": "Time of login",
                    "required": True,
                    "example": "2026-03-13 12:30:00"
                },
                {
                    "name": "device_info",
                    "description": "Device/browser information",
                    "required": True,
                    "example": "Chrome on Windows 10"
                },
                {
                    "name": "location",
                    "description": "Approximate location",
                    "required": True,
                    "example": "Berlin, Germany"
                },
                {
                    "name": "ip_address",
                    "description": "IP address used for login",
                    "required": False,
                    "example": "192.168.1.100"
                },
                {
                    "name": "browser_info",
                    "description": "Detailed browser information",
                    "required": False,
                    "example": "Chrome 122.0.0.0"
                }
            ],
            subject_key="email.security_login_new_device_subject",
            title_key="email.security_login_new_device_title"
        ),

        "settings_changed": TemplateDefinition(
            name="settings_changed",
            category=TemplateCategory.SETTINGS,
            description="Notification when sensitive account settings are changed",  # noqa: E501
            variables=[
                {
                    "name": "user_name",
                    "description": "Name of the user",
                    "required": True,
                    "example": "Jane Smith"
                },
                {
                    "name": "changed_setting",
                    "description": "Setting that was changed",
                    "required": True,
                    "example": "Two-factor authentication"
                },
                {
                    "name": "change_time",
                    "description": "Time when setting was changed",
                    "required": True,
                    "example": "2026-03-13 12:45:00"
                },
                {
                    "name": "ip_address",
                    "description": "IP address used for change",
                    "required": False,
                    "example": "192.168.1.100"
                },
                {
                    "name": "device_info",
                    "description": "Device/browser information",
                    "required": False,
                    "example": "Firefox on macOS"
                }
            ],
            subject_key="email.settings_changed_subject",
            title_key="email.settings_changed_title"
        ),

        "hackathon/start_reminder": TemplateDefinition(
            name="hackathon/start_reminder",
            category=TemplateCategory.HACKATHON,
            description="Reminder before hackathon starts",
            variables=[
                {
                    "name": "hackathon_name",
                    "description": "Name of the hackathon",
                    "required": True,
                    "example": "Global Hackathon 2026"
                },
                {
                    "name": "user_name",
                    "description": "Name of the registered user",
                    "required": True,
                    "example": "Henry Ford"
                },
                {
                    "name": "start_time",
                    "description": "Start time of the hackathon",
                    "required": True,
                    "example": "2026-04-15 09:00:00"
                },
                {
                    "name": "days_until_start",
                    "description": "Days until hackathon starts",
                    "required": True,
                    "example": "3"
                },
                {
                    "name": "hackathon_dashboard_url",
                    "description": "URL to hackathon dashboard",
                    "required": True,
                    "example": "https://example.com/hackathons/456/dashboard"
                }
            ],
            subject_key="email.hackathon_start_reminder_subject",
            title_key="email.hackathon_start_reminder_title"
        )
    }

    @classmethod
    def get_template(cls, template_name: str) -> Optional[TemplateDefinition]:
        """Get template definition by name."""
        return cls.TEMPLATES.get(template_name)

    @classmethod
    def validate_template(
        cls,
        template_name: str,
        variables: Dict[str, str]
    ) -> List[str]:
        """Validate variables for a template."""
        template = cls.get_template(template_name)
        if not template:
            return [f"Template not found: {template_name}"]

        return template.validate_variables(variables)

    @classmethod
    def get_all_templates(cls) -> Dict[str, TemplateDefinition]:
        """Get all template definitions."""
        return cls.TEMPLATES.copy()

    @classmethod
    def get_templates_by_category(
        cls,
        category: TemplateCategory
    ) -> Dict[str, TemplateDefinition]:
        """Get templates filtered by category."""
        return {
            name: template
            for name, template in cls.TEMPLATES.items()
            if template.category == category
        }

    @classmethod
    def generate_documentation(cls) -> str:
        """Generate comprehensive documentation for all templates."""
        lines = ["Email Template Documentation", "=" * 40]

        # Group by category
        for category in TemplateCategory:
            category_templates = cls.get_templates_by_category(category)
            if not category_templates:
                continue

            lines.append(f"\n{category.value.upper()} TEMPLATES")
            lines.append("-" * 30)

            for template_name, template in category_templates.items():
                lines.append(f"\n{template.get_variable_docs()}")

        # Add usage example
        lines.append("\n\nUSAGE EXAMPLE")
        lines.append("-" * 30)
        lines.append("""
from app.utils.template_registry import TemplateRegistry

# Validate template variables
errors = TemplateRegistry.validate_template(
    "verification",
    {"user_name": "John Doe", "verification_url": "https://..."}
)

if errors:
    print(f"Validation errors: {errors}")
else:
    print("Template variables are valid!")

# Get template documentation
template = TemplateRegistry.get_template("verification")
if template:
    print(template.get_variable_docs())
""")

        return "\n".join(lines)

    @classmethod
    def get_required_variables(cls, template_name: str) -> List[str]:
        """Get list of required variable names for a template."""
        template = cls.get_template(template_name)
        if not template:
            return []

        return [
            var_def["name"]
            for var_def in template.variables
            if var_def["required"]
        ]

    @classmethod
    def get_optional_variables(cls, template_name: str) -> List[str]:
        """Get list of optional variable names for a template."""
        template = cls.get_template(template_name)
        if not template:
            return []

        return [
            var_def["name"]
            for var_def in template.variables
            if not var_def["required"]
        ]

    @classmethod
    def extract_template_variables(cls, template_path: Path) -> List[str]:
        """Extract variable names referenced by a Jinja template file."""
        source = template_path.read_text(encoding="utf-8")
        names = set()
        for expression in cls._JINJA_EXPRESSION_RE.findall(source):
            inner = expression[2:-2]
            for identifier in cls._JINJA_IDENTIFIER_RE.findall(inner):
                if identifier in cls._JINJA_RESERVED_NAMES:
                    continue
                names.add(identifier)
        return sorted(names)

    @classmethod
    def validate_template_files(cls) -> Dict[str, Any]:
        """Validate registered templates against on-disk placeholders."""
        report: Dict[str, Any] = {
            "missing_templates": [],
            "missing_languages": [],
            "unknown_templates": [],
            "issues": [],
        }

        known_templates = set(cls.TEMPLATES.keys())
        disk_templates = set()
        for template_path in cls.TEMPLATE_ROOT.rglob("*.html"):
            relative = template_path.relative_to(cls.TEMPLATE_ROOT)
            if len(relative.parts) != 2:
                continue
            template_name = relative.parent.as_posix()
            language = relative.stem
            disk_templates.add(template_name)
            if template_name not in known_templates:
                report["unknown_templates"].append(
                    {"template": template_name, "language": language}
                )
                continue

            allowed = (
                set(cls.COMMON_TEMPLATE_VARIABLES)
                | set(cls.get_required_variables(template_name))
                | set(cls.get_optional_variables(template_name))
            )
            used = set(cls.extract_template_variables(template_path))
            undocumented = sorted(used - allowed)
            if undocumented:
                report["issues"].append(
                    {
                        "template": template_name,
                        "language": language,
                        "undocumented_variables": undocumented,
                    }
                )

        for template_name, definition in cls.TEMPLATES.items():
            template_dir = cls.TEMPLATE_ROOT / template_name
            if not template_dir.exists():
                report["missing_templates"].append(template_name)
                continue
            for language in definition.languages or list(
                cls.TEMPLATE_LANGUAGES
            ):
                if not (template_dir / f"{language}.html").exists():
                    report["missing_languages"].append(
                        {"template": template_name, "language": language}
                    )

        report["valid"] = not any(
            report[key]
            for key in (
                "missing_templates",
                "missing_languages",
                "unknown_templates",
                "issues",
            )
        )
        return report


# Convenience functions
def validate_email_template(
    template_name: str,
    variables: Dict[str, str]
) -> bool:
    """Validate email template variables (convenience function)."""
    errors = TemplateRegistry.validate_template(template_name, variables)
    return len(errors) == 0


def get_template_docs(template_name: str) -> Optional[str]:
    """Get documentation for a template (convenience function)."""
    template = TemplateRegistry.get_template(template_name)
    if template:
        return template.get_variable_docs()
    return None


# Export the registry instance
template_registry = TemplateRegistry()
