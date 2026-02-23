"""
Enhanced notification service for sending multi-channel notifications.
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from sqlalchemy.orm import Session

from app.utils.template_engine import template_engine
from app.services.email_service import EmailService
from app.services.notification_preference_service import (
    notification_preference_service
)
from app.services.push_notification_service import push_notification_service
from app.repositories.notification_repository import (
    NotificationRepository
)
from app.domain.models.notification import UserNotification

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending notifications for important user actions."""

    def __init__(self):
        self.email_service = EmailService()
        self.template_engine = template_engine
        self.notification_repo = NotificationRepository()

    def send_multi_channel_notification(
        self,
        db: Session,
        notification_type: str,
        user_id: int,
        title: str,
        message: str,
        language: str = "en",
        variables: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, bool]:
        """
        Send a notification through multiple channels
        based on user preferences.

        Args:
            db: Database session
            notification_type: Type of notification
            user_id: User ID to send notification to
            title: Notification title
            message: Notification message
            language: Language code (default: "en")
            variables: Template variables for email
            data: Additional data for push/in-app notifications

        Returns:
            Dictionary with channel success status
        """
        results = {
            "email": False,
            "push": False,
            "in_app": False
        }

        # Store in-app notification
        try:
            notification_data = {
                "user_id": user_id,
                "type": notification_type,
                "title": title,
                "message": message,
                "data": data or {},
                "read": False,
                "created_at": datetime.utcnow()
            }
            self.notification_repo.create(db, obj_in=notification_data)
            results["in_app"] = True
        except Exception as e:
            logger.error(f"Failed to store in-app notification: {e}")

        # Send email notification if enabled
        if notification_preference_service.should_send_notification(
            db, user_id, notification_type, "email"
        ):
            try:
                if variables is None:
                    variables = {}

                # Add common variables
                variables.update({
                    "notification_title": title,
                    "notification_message": message,
                    "user_id": user_id
                })

                # Get user email (would need user repository)
                # For now, this is a placeholder
                results["email"] = True
                logger.info(
                    f"Email notification would be sent to user {user_id} "
                    f"for {notification_type}"
                )
            except Exception as e:
                logger.error(f"Failed to send email notification: {e}")

        # Send push notification if enabled
        if notification_preference_service.should_send_notification(
            db, user_id, notification_type, "push"
        ):
            try:
                push_result = push_notification_service.send_push_notification(
                    db, user_id, notification_type, title, message, data
                )
                results["push"] = push_result
            except Exception as e:
                logger.error(f"Failed to send push notification: {e}")

        return results

    def send_notification(
        self,
        db: Session,
        notification_type: str,
        user_id: int,
        language: str = "en",
        variables: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send a notification based on type with automatic title/message.

        Args:
            db: Database session
            notification_type: Type of notification
            user_id: User ID to send notification to
            language: Language code
            variables: Template variables

        Returns:
            True if at least one channel succeeded
        """
        # This would use template engine to get title/message
        # For now, placeholder implementation
        title = f"Notification: {notification_type}"
        message = f"You have a new {notification_type} notification"

        results = self.send_multi_channel_notification(
            db=db,
            notification_type=notification_type,
            user_id=user_id,
            title=title,
            message=message,
            language=language,
            variables=variables
        )

        return any(results.values())

    def send_team_invitation_notification(
        self,
        db: Session,
        team_id: int,
        invited_user_id: int,
        inviter_id: int,
        language: str = "en"
    ) -> bool:
        """Send notification for team invitation."""
        # Placeholder implementation
        logger.info(
            f"Team invitation notification: team={team_id}, "
            f"invited_user={invited_user_id}, inviter={inviter_id}"
        )
        return True

    def send_team_member_added_notification(
        self,
        db: Session,
        team_id: int,
        user_id: int,
        added_by_id: int,
        language: str = "en"
    ) -> bool:
        """Send notification for team member addition."""
        # Placeholder implementation
        logger.info(
            f"Team member added notification: team={team_id}, "
            f"user={user_id}, added_by={added_by_id}"
        )
        return True

    def send_project_created_notification(
        self,
        db: Session,
        project_id: int,
        creator_id: int,
        hackathon_id: Optional[int] = None,
        language: str = "en"
    ) -> bool:
        """Send notification for project creation."""
        # Placeholder implementation
        logger.info(
            f"Project created notification: project={project_id}, "
            f"creator={creator_id}, hackathon={hackathon_id}"
        )
        return True

    def get_user_notifications(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        unread_only: bool = False
    ) -> List[UserNotification]:
        """Get notifications for a user."""
        filters = {"user_id": user_id}
        if unread_only:
            filters["read"] = False

        return self.notification_repo.filter(
            db, skip=skip, limit=limit, **filters
        )

    def mark_notification_as_read(
        self, db: Session, notification_id: int, user_id: int
    ) -> bool:
        """Mark a notification as read."""
        notification = self.notification_repo.get(db, notification_id)
        if notification and notification.user_id == user_id:
            notification.read = True
            db.commit()
            return True
        return False

    def mark_all_notifications_as_read(self, db: Session, user_id: int) -> int:
        """Mark all notifications as read for a user."""
        notifications = self.notification_repo.filter(
            db, user_id=user_id, read=False
        )
        count = 0
        for notification in notifications:
            notification.read = True
            count += 1
        if count > 0:
            db.commit()
        return count


# Global notification service instance
notification_service = NotificationService()
