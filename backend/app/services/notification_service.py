"""
Canonical notification orchestration service.
"""
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.domain.models.notification import UserNotification
from app.repositories.notification_repository import (
    NotificationDeliveryRepository,
    NotificationRepository,
)
from app.repositories.project_repository import ProjectRepository
from app.repositories.team_repository import TeamRepository
from app.repositories.user_repository import UserRepository
from app.services.email_orchestrator import EmailContext, EmailOrchestrator
from app.services.in_app_notification_service import (
    DeliveryResult,
    InAppNotificationService,
)
from app.services.notification_eligibility_service import (
    notification_eligibility_service,
)
from app.services.notification_registry import get_definition, is_known_type
from app.services.push_notification_service import push_notification_service

logger = logging.getLogger(__name__)


@dataclass
class NotificationDispatchResult:
    notification: Optional[UserNotification]
    deliveries: Dict[str, DeliveryResult]


class NotificationService:
    """Service for sending notifications for important user actions."""

    def __init__(self):
        self.email_orchestrator = EmailOrchestrator()
        self.notification_repo = NotificationRepository()
        self.delivery_repo = NotificationDeliveryRepository()
        self.user_repo = UserRepository()
        self.team_repo = TeamRepository()
        self.project_repo = ProjectRepository()
        self.in_app_service = InAppNotificationService()

    def send_multi_channel_notification(
        self,
        db: Session,
        notification_type: str,
        user_id: int,
        title: str,
        message: str,
        language: str = "en",
        variables: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        channels: Optional[List[str]] = None,
    ) -> Dict[str, bool]:
        dispatch = self.dispatch_notification(
            db=db,
            notification_type=notification_type,
            user_id=user_id,
            title=title,
            message=message,
            language=language,
            variables=variables,
            data=data,
            requested_channels=channels,
        )
        return {
            channel: result.success
            for channel, result in dispatch.deliveries.items()
        }

    def dispatch_notification(
        self,
        db: Session,
        notification_type: str,
        user_id: int,
        title: str,
        message: str,
        language: str = "en",
        variables: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        requested_channels: Optional[List[str]] = None,
    ) -> NotificationDispatchResult:
        if not is_known_type(notification_type):
            raise ValueError(f"Unknown notification type: {notification_type}")

        allowed_channels = notification_eligibility_service.get_allowed_channels(
            db,
            user_id,
            notification_type,
            requested_channels=requested_channels,
        )
        if not allowed_channels:
            return NotificationDispatchResult(
                notification=None, deliveries={}
            )

        notification = self.notification_repo.create_notification(
            db,
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            message=message,
            data=data or {},
        )
        deliveries = self.delivery_repo.create_deliveries(
            db, notification.id, allowed_channels
        )

        results: Dict[str, DeliveryResult] = {}
        delivery_map = {delivery.channel: delivery for delivery in deliveries}
        for channel in allowed_channels:
            delivery = delivery_map[channel]
            try:
                result = self._send_via_channel(
                    db=db,
                    channel=channel,
                    notification=notification,
                    delivery=delivery,
                    language=language,
                    variables=variables or {},
                )
            except Exception as exc:
                logger.error(
                    "Failed to send notification %s via %s: %s",
                    notification.id,
                    channel,
                    exc,
                )
                result = DeliveryResult(
                    success=False,
                    status="failed",
                    error=str(exc),
                )
            self.delivery_repo.update_status(
                db,
                delivery,
                status=result.status,
                error=result.error,
                provider_message_id=result.provider_message_id,
                delivered_at=datetime.utcnow() if result.success else None,
            )
            results[channel] = result

        hydrated = self.notification_repo.get(db, notification.id)
        return NotificationDispatchResult(
            notification=hydrated, deliveries=results
        )

    def send_notification(
        self,
        db: Session,
        notification_type: str,
        user_id: int,
        language: str = "en",
        variables: Optional[Dict[str, Any]] = None,
    ) -> bool:
        title = f"Notification: {notification_type}"
        message = f"You have a new {notification_type} notification"
        results = self.send_multi_channel_notification(
            db=db,
            notification_type=notification_type,
            user_id=user_id,
            title=title,
            message=message,
            language=language,
            variables=variables,
        )
        return any(results.values())

    def send_team_invitation_notification(
        self,
        db: Session,
        team_id: int,
        invited_user_id: int,
        inviter_id: int,
        language: str = "en",
    ) -> bool:
        team = self.team_repo.get(db, team_id)
        inviter = self.user_repo.get(db, inviter_id)
        invited_user = self.user_repo.get(db, invited_user_id)
        if not team or not inviter or not invited_user:
            return False

        variables = {
            "team_name": team.name,
            "inviter_name": inviter.name or inviter.username or inviter.email,
            "accept_url": f"/teams/invitations/{team_id}/accept",
        }
        results = self.send_multi_channel_notification(
            db=db,
            notification_type="team_invitation",
            user_id=invited_user_id,
            title=f"Invitation to join {team.name}",
            message=(
                f"{inviter.name or inviter.username or inviter.email} invited "
                f"you to join {team.name}"
            ),
            language=language,
            variables=variables,
            data={
                "team_id": team.id,
                "inviter_id": inviter.id,
                "metadata": {
                    "team_name": team.name,
                    "inviter_name": inviter.name or inviter.username
                    or inviter.email,
                },
            },
        )
        return any(results.values())

    def send_team_member_added_notification(
        self,
        db: Session,
        team_id: int,
        user_id: int,
        added_by_id: int,
        language: str = "en",
    ) -> bool:
        team = self.team_repo.get(db, team_id)
        added_by = self.user_repo.get(db, added_by_id)
        recipient = self.user_repo.get(db, user_id)
        if not team or not added_by or not recipient:
            return False

        added_by_display_name = (
            added_by.name or added_by.username or added_by.email
        )
        variables = {
            "team_name": team.name,
            "added_by_name": added_by_display_name,
        }
        results = self.send_multi_channel_notification(
            db=db,
            notification_type="team_member_added",
            user_id=user_id,
            title=f"You joined {team.name}",
            message=(
                f"{added_by_display_name} added you to {team.name}"
            ),
            language=language,
            variables=variables,
            data={
                "team_id": team.id,
                "added_by_id": added_by.id,
                "metadata": {"team_name": team.name},
            },
        )
        return any(results.values())

    def send_team_invitation_declined_notification(
        self,
        db: Session,
        team_id: int,
        invited_user_id: int,
        inviter_id: int,
        language: str = "en",
    ) -> bool:
        team = self.team_repo.get(db, team_id)
        invited_user = self.user_repo.get(db, invited_user_id)
        inviter = self.user_repo.get(db, inviter_id)
        if not team or not invited_user or not inviter:
            return False
        user_display = (
            invited_user.name or invited_user.username or invited_user.email
        )
        results = self.send_multi_channel_notification(
            db=db,
            notification_type="team_invitation_declined",
            user_id=inviter_id,
            title=f"{team.name} invitation declined",
            message=(
                f"{user_display} declined the invitation to join {team.name}"
            ),
            language=language,
            data={
                "team_id": team.id,
                "invited_user_id": invited_user.id,
                "metadata": {"team_name": team.name},
            },
        )
        return any(results.values())

    def send_project_created_notification(
        self,
        db: Session,
        project_id: int,
        creator_id: int,
        hackathon_id: Optional[int] = None,
        language: str = "en",
    ) -> bool:
        project = self.project_repo.get(db, project_id)
        creator = self.user_repo.get(db, creator_id)
        if not project or not creator or not project.owner_id:
            return False
        results = self.send_multi_channel_notification(
            db=db,
            notification_type="project_created",
            user_id=project.owner_id,
            title=f"Project created: {project.title}",
            message=f"Your project {project.title} was created successfully",
            language=language,
            variables={
                "project_name": project.title,
                "creator_name": creator.name or creator.username
                or creator.email,
                "project_url": f"/projects/{project.id}",
            },
            data={
                "project_id": project.id,
                "hackathon_id": hackathon_id,
                "metadata": {"project_name": project.title},
            },
        )
        return any(results.values())

    def get_user_notifications(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        unread_only: bool = False,
    ) -> List[UserNotification]:
        return self.notification_repo.get_user_notifications(
            db,
            user_id=user_id,
            skip=skip,
            limit=limit,
            unread_only=unread_only,
        )

    def mark_notification_as_read(
        self, db: Session, notification_id: int, user_id: int
    ) -> bool:
        return self.notification_repo.mark_as_read(
            db, notification_id, user_id
        )

    def mark_all_notifications_as_read(self, db: Session, user_id: int) -> int:
        return self.notification_repo.mark_all_as_read(db, user_id)

    def _send_via_channel(
        self,
        db: Session,
        channel: str,
        notification: UserNotification,
        delivery,
        language: str,
        variables: Dict[str, Any],
    ) -> DeliveryResult:
        if channel == "in_app":
            return self.in_app_service.deliver(db, notification, delivery)
        if channel == "email":
            return self._deliver_email(
                db, notification, language=language, variables=variables
            )
        if channel == "push":
            return push_notification_service.deliver(
                db,
                user_id=notification.user_id,
                notification_type=notification.notification_type,
                title=notification.title,
                body=notification.message,
                delivery=delivery,
                data=notification.data,
            )
        raise ValueError(f"Unsupported channel: {channel}")

    def _deliver_email(
        self,
        db: Session,
        notification: UserNotification,
        *,
        language: str,
        variables: Dict[str, Any],
    ) -> DeliveryResult:
        definition = get_definition(notification.notification_type)
        user = self.user_repo.get(db, notification.user_id)
        if not definition or not definition.email_template:
            return DeliveryResult(
                success=False,
                status="failed",
                error="No email template configured",
            )
        if not user or not user.email:
            return DeliveryResult(
                success=False,
                status="failed",
                error="User not found or has no email",
            )

        payload = dict(variables)
        payload.setdefault("notification_title", notification.title)
        payload.setdefault("notification_message", notification.message)
        payload.setdefault(
            "user_name", user.name or user.username or user.email
        )

        context = EmailContext(
            user_id=notification.user_id,
            user_email=user.email,
            language=language,
            category="notification",
        )
        result = self.email_orchestrator.send_template(
            db=db,
            template_name=definition.email_template,
            context=context,
            variables=payload,
        )
        return DeliveryResult(
            success=result.success,
            status="delivered" if result.success else "failed",
            error=result.error,
            provider_message_id=result.message_id,
        )


notification_service = NotificationService()
