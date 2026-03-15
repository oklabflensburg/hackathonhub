"""
Email Orchestrator - Central facade for all email operations.
Provides a unified interface for sending emails with template validation,
variable resolution, and language handling.
"""
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from sqlalchemy.orm import Session

from app.services.email_service import email_service
from app.utils.jinja2_engine import jinja2_template_engine as template_engine
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


@dataclass
class EmailContext:
    """Context for email sending."""
    user_id: Optional[int] = None
    user_email: str = ""
    language: str = "en"
    priority: str = "normal"  # "low", "normal", "high"
    category: str = "transactional"  # "transactional", "notification"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SendResult:
    """Result of email sending operation."""
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
    template_used: Optional[str] = None


class EmailTemplateValidator:
    """Validate template variables and requirements."""

    # Template requirements mapping
    TEMPLATE_REQUIREMENTS = {
        "verification": ["user_name", "verification_url"],
        "password_reset": ["user_name", "reset_url"],
        "newsletter_welcome": ["unsubscribe_url"],
        "team/invitation_sent": ["team_name", "inviter_name", "accept_url"],
        "team/invitation_accepted": ["team_name", "user_name"],
        "team/member_added": ["team_name", "added_by_name"],
        "team/created": ["team_name", "creator_name", "team_id"],
        "project/created": ["project_name", "creator_name", "project_url"],
        "project/commented": ["project_name", "commenter_name",
                              "comment_preview", "project_url"],
        "hackathon/registered": ["hackathon_name", "user_name",
                                 "hackathon_date", "hackathon_url"],
        "hackathon/started": ["hackathon_name", "user_name",
                              "start_time", "hackathon_dashboard_url"]
    }

    @classmethod
    def validate(cls, template_name: str, variables: Dict[str, Any]) -> bool:
        """Validate variables for template."""
        if template_name not in cls.TEMPLATE_REQUIREMENTS:
            logger.warning(
                f"No validation rules for template: {template_name}")
            return True

        required_vars = cls.TEMPLATE_REQUIREMENTS[template_name]
        missing_vars = [var for var in required_vars if var not in variables]

        if missing_vars:
            logger.error(
                f"Template {template_name} missing required "
                f"variables: {missing_vars}"
            )
            return False

        return True


class LanguageResolver:
    """Resolve language for email based on user preferences."""

    def __init__(self):
        self.user_repo = UserRepository()

    def resolve_for_user(self, db: Session, user_id: int) -> str:
        """Get user's preferred language from database."""
        try:
            user = self.user_repo.get(db, user_id)
            if user and user.language:
                return user.language
        except Exception as e:
            logger.error(f"Failed to resolve language for user {user_id}: {e}")

        return "en"  # Default to English

    def resolve(self, db: Session, context: EmailContext) -> str:
        """Resolve language from context."""
        if context.language and context.language != "auto":
            return context.language

        if context.user_id:
            return self.resolve_for_user(db, context.user_id)

        return "en"  # Default


class EmailOrchestrator:
    """Central facade for all email operations."""

    def __init__(self):
        self.email_service = email_service
        self.template_engine = template_engine
        self.validator = EmailTemplateValidator()
        self.language_resolver = LanguageResolver()
        self.user_repo = UserRepository()

    def send_template(
        self,
        db: Session,
        template_name: str,
        context: EmailContext,
        variables: Optional[Dict[str, Any]] = None
    ) -> SendResult:
        """
        Send email using a template with validation.

        Args:
            db: Database session
            template_name: Name of template (e.g., "verification",
                           "team/invitation_sent")
            context: Email context including recipient
            variables: Template variables

        Returns:
            SendResult with status and message ID
        """
        try:
            # Resolve language
            language = self.language_resolver.resolve(db, context)

            # Get user email from context or user_id
            to_email = context.user_email
            if not to_email and context.user_id:
                user = self.user_repo.get(db, context.user_id)
                if user and user.email:
                    to_email = user.email
                else:
                    return SendResult(
                        success=False,
                        error=(f"User {context.user_id} not found "
                               f"or has no email")
                    )

            if not to_email:
                return SendResult(
                    success=False,
                    error="No email address provided"
                )

            # Prepare variables
            if variables is None:
                variables = {}

            # Add common variables
            # Will be dynamic in production
            variables.setdefault("current_year", 2026)

            # Validate template variables
            if not self.validator.validate(template_name, variables):
                return SendResult(
                    success=False,
                    error=f"Template validation failed for {template_name}"
                )

            # Render email using template engine
            email_content = self.template_engine.render_email(
                template_name=template_name,
                language=language,
                variables=variables
            )

            # Send email
            success = self.email_service.send_email(
                to_email=to_email,
                subject=email_content["subject"],
                body=email_content["text"],
                html_body=email_content["html"]
            )

            if success:
                logger.info(
                    f"Email sent successfully: template={template_name}, "
                    f"to={to_email}, language={language}"
                )
                return SendResult(
                    success=True,
                    template_used=template_name
                )
            else:
                logger.error(
                    f"Failed to send email: template={template_name}, "
                    f"to={to_email}"
                )
                return SendResult(
                    success=False,
                    error="Email service failed to send",
                    template_used=template_name
                )

        except Exception as e:
            logger.error(f"Error in send_template: {e}")
            return SendResult(
                success=False,
                error=str(e)
            )

    def send_notification(
        self,
        db: Session,
        notification_type: str,
        user_id: int,
        variables: Optional[Dict[str, Any]] = None,
        language: str = "en"
    ) -> SendResult:
        """
        Send notification email based on type.

        Args:
            db: Database session
            notification_type: Type of notification
            user_id: Recipient user ID
            variables: Template variables
            language: Language code

        Returns:
            SendResult with status
        """
        # Map notification type to template
        template_map = {
            "team_invitation": "team/invitation_sent",
            "team_invitation_accepted": "team/invitation_accepted",
            "team_member_added": "team/member_added",
            "project_created": "project/created",
            "project_commented": "project/commented",
            "hackathon_registered": "hackathon/registered",
            "hackathon_started": "hackathon/started",
            "team_created": "team/created"
        }

        template_name = template_map.get(notification_type)
        if not template_name:
            return SendResult(
                success=False,
                error=(f"No template mapping for notification "
                       f"type: {notification_type}")
            )

        context = EmailContext(
            user_id=user_id,
            language=language,
            category="notification"
        )

        return self.send_template(db, template_name, context, variables)

    def send_verification_email(
        self,
        db: Session,
        user_id: int,
        verification_url: str,
        language: str = "en"
    ) -> SendResult:
        """Send email verification email."""
        user = self.user_repo.get(db, user_id)
        if not user:
            return SendResult(success=False, error="User not found")

        variables = {
            "user_name": user.name or user.username,
            "verification_url": verification_url,
            "expiration_hours": 24
        }

        context = EmailContext(
            user_id=user_id,
            user_email=user.email,
            language=language,
            category="auth"
        )

        return self.send_template(db, "verification", context, variables)

    def send_password_reset_email(
        self,
        db: Session,
        user_id: int,
        reset_url: str,
        language: str = "en"
    ) -> SendResult:
        """Send password reset email."""
        user = self.user_repo.get(db, user_id)
        if not user:
            return SendResult(success=False, error="User not found")

        variables = {
            "user_name": user.name or user.username,
            "reset_url": reset_url,
            "expiration_hours": 1
        }

        context = EmailContext(
            user_id=user_id,
            user_email=user.email,
            language=language,
            category="auth"
        )

        return self.send_template(db, "password_reset", context, variables)

    def send_team_invitation_email(
        self,
        db: Session,
        team_id: int,
        team_name: str,
        inviter_id: int,
        invitee_id: int,
        accept_url: str,
        language: str = "en"
    ) -> SendResult:
        """Send team invitation email."""
        inviter = self.user_repo.get(db, inviter_id)
        if not inviter:
            return SendResult(success=False, error="Inviter not found")

        variables = {
            "team_name": team_name,
            "inviter_name": inviter.name or inviter.username,
            "accept_url": accept_url,
            "team_id": team_id
        }

        context = EmailContext(
            user_id=invitee_id,
            language=language,
            category="notification"
        )

        return self.send_template(
            db, "team/invitation_sent", context, variables
        )


# Global email orchestrator instance
email_orchestrator = EmailOrchestrator()
