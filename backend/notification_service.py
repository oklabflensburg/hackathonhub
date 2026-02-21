"""
Enhanced notification service for sending multi-channel notifications.
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from sqlalchemy.orm import Session

from template_engine import template_engine
from email_service import EmailService
from notification_preference_service import notification_preference_service
from push_notification_service import push_notification_service
import crud
import models

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending notifications for important user actions."""
    
    def __init__(self):
        self.email_service = EmailService()
        self.template_engine = template_engine
    
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
        Send a notification through multiple channels based on user preferences.
        
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
            Dict with success status for each channel
        """
        if variables is None:
            variables = {}
        
        # Get user details
        user = crud.get_user(db, user_id)
        if not user:
            logger.error(f"User not found: {user_id}")
            return {"email": False, "push": False, "in_app": False}
        
        # Add user info to variables
        if "recipient_name" not in variables:
            variables["recipient_name"] = user.name or user.username
        
        if "current_year" not in variables:
            variables["current_year"] = datetime.now().year
        
        results = {
            "email": False,
            "push": False,
            "in_app": False
        }
        
        try:
            # Send email notification if enabled
            if notification_preference_service.should_send_notification(
                db, user_id, notification_type, "email"
            ):
                results["email"] = self._send_email_notification(
                    notification_type, user.email, user.name or user.username,
                    language, variables
                )
            
            # Send push notification if enabled
            if notification_preference_service.should_send_notification(
                db, user_id, notification_type, "push"
            ):
                results["push"] = push_notification_service.send_push_notification(
                    db, user_id, notification_type, title, message, data
                )
            
            # Send in-app notification if enabled
            if notification_preference_service.should_send_notification(
                db, user_id, notification_type, "in_app"
            ):
                results["in_app"] = self._send_in_app_notification(
                    db, user_id, notification_type, title, message, data
                )
            
            logger.info(f"Multi-channel notification sent for user {user_id}, type {notification_type}: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error sending multi-channel notification: {e}")
            return results
    
    def send_notification(
        self,
        notification_type: str,
        recipient_email: str,
        recipient_name: str,
        language: str = "en",
        variables: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send a notification email (legacy method for backward compatibility).
        
        Args:
            notification_type: Type of notification
            recipient_email: Email address of recipient
            recipient_name: Name of recipient
            language: Language code (default: "en")
            variables: Template variables
            
        Returns:
            bool: True if email was sent successfully
        """
        if variables is None:
            variables = {}
        
        # Add recipient name to variables if not already present
        if "recipient_name" not in variables:
            variables["recipient_name"] = recipient_name
        
        # Add current year for copyright
        if "current_year" not in variables:
            variables["current_year"] = datetime.now().year
        
        try:
            # Map notification type to template path
            template_map = {
                "team_invitation_sent": "team/invitation_sent",
                "team_invitation_accepted": "team/invitation_accepted",
                "team_member_added": "team/member_added",
                "team_created": "team/created",
                "project_created": "project/created",
                "project_commented": "project/commented",
                "hackathon_registered": "hackathon/registered",
                "hackathon_started": "hackathon/started",
            }
            
            template_name = template_map.get(notification_type)
            if not template_name:
                logger.error(f"Unknown notification type: {notification_type}")
                return False
            
            # Render email using template engine
            email_content = self.template_engine.render_email(
                template_name=template_name,
                language=language,
                variables=variables
            )
            
            # Send email
            success = self.email_service.send_email(
                to_email=recipient_email,
                subject=email_content["subject"],
                body=email_content["text"],
                html_body=email_content["html"]
            )
            
            if success:
                msg = f"Notification sent: {notification_type}"
                msg += f" to {recipient_email}"
                logger.info(msg)
            else:
                msg = f"Failed to send notification: {notification_type}"
                msg += f" to {recipient_email}"
                logger.error(msg)
            
            return success
            
        except Exception as e:
            msg = f"Error sending notification {notification_type}: {e}"
            logger.error(msg)
            return False
    
    def _send_email_notification(
        self,
        notification_type: str,
        recipient_email: str,
        recipient_name: str,
        language: str = "en",
        variables: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send an email notification."""
        if variables is None:
            variables = {}
        
        try:
            # Map notification type to template path
            template_map = {
                "team_invitation_sent": "team/invitation_sent",
                "team_invitation_accepted": "team/invitation_accepted",
                "team_member_added": "team/member_added",
                "team_created": "team/created",
                "project_created": "project/created",
                "project_commented": "project/commented",
                "hackathon_registered": "hackathon/registered",
                "hackathon_started": "hackathon/started",
                "comment_reply": "system/comment_reply",
                "vote_received": "system/vote_received",
                "system_announcement": "system/announcement",
                "security_alert": "system/security_alert",
            }
            
            template_name = template_map.get(notification_type)
            if not template_name:
                logger.error(f"Unknown notification type for email: {notification_type}")
                return False
            
            # Render email using template engine
            email_content = self.template_engine.render_email(
                template_name=template_name,
                language=language,
                variables=variables
            )
            
            # Send email
            success = self.email_service.send_email(
                to_email=recipient_email,
                subject=email_content["subject"],
                body=email_content["text"],
                html_body=email_content["html"]
            )
            
            if success:
                logger.debug(f"Email notification sent: {notification_type} to {recipient_email}")
            else:
                logger.warning(f"Failed to send email notification: {notification_type} to {recipient_email}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending email notification {notification_type}: {e}")
            return False
    
    def _send_in_app_notification(
        self,
        db: Session,
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send an in-app notification."""
        try:
            # Create notification in database
            notification = crud.create_user_notification(
                db=db,
                user_id=user_id,
                notification_type=notification_type,
                title=title,
                message=message,
                data=data,
                channel="in_app"
            )
            
            if notification:
                logger.debug(f"In-app notification created for user {user_id}: {notification_type}")
                return True
            else:
                logger.warning(f"Failed to create in-app notification for user {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error creating in-app notification: {e}")
            return False
    
    def send_team_invitation_notification(
        self,
        db: Session,
        invitation_id: int,
        language: str = "en"
    ) -> Dict[str, bool]:
        """
        Send notification for team invitation.
        
        Args:
            db: Database session
            invitation_id: ID of the team invitation
            language: Language code (default: "en")
            
        Returns:
            Dict with success status for each channel
        """
        # Get invitation details
        invitation = crud.get_team_invitation(db, invitation_id)
        if not invitation:
            logger.error(f"Team invitation not found: {invitation_id}")
            return {"email": False, "push": False, "in_app": False}
        
        team = invitation.team
        invited_user = invitation.invited_user
        inviter = invitation.inviter
        hackathon = team.hackathon
        
        # Prepare template variables
        frontend_url = self._get_frontend_url()
        invitation_url = f"{frontend_url}/teams/{team.id}/invitations"
        
        expiration_date = "Never"
        if invitation.expires_at:
            expiration_date = invitation.expires_at.strftime("%B %d, %Y")
        
        variables = {
            "team_name": team.name,
            "team_description": team.description or "No description",
            "hackathon_name": hackathon.name,
            "actor_name": inviter.name or inviter.username,
            "invitation_url": invitation_url,
            "expiration_date": expiration_date
        }
        
        # Prepare notification data
        data = {
            "team_id": team.id,
            "team_name": team.name,
            "invitation_id": invitation_id,
            "inviter_id": inviter.id,
            "inviter_name": inviter.name or inviter.username,
            "hackathon_id": hackathon.id,
            "hackathon_name": hackathon.name,
            "invitation_url": invitation_url
        }
        
        # Send multi-channel notification
        return self.send_multi_channel_notification(
            db=db,
            notification_type="team_invitation_sent",
            user_id=invited_user.id,
            title=f"You've been invited to join {team.name}",
            message=f"{inviter.name or inviter.username} has invited you to join team {team.name} for {hackathon.name}",
            language=language,
            variables=variables,
            data=data
        )
    
    def send_team_invitation_accepted_notification(
        self,
        db: Session,
        invitation_id: int,
        language: str = "en"
    ) -> bool:
        """
        Send notification when team invitation is accepted.
        
        Args:
            db: Database session
            invitation_id: ID of the accepted invitation
            language: Language code (default: "en")
            
        Returns:
            bool: True if notification was sent successfully
        """
        # Get invitation details
        invitation = crud.get_team_invitation(db, invitation_id)
        if not invitation:
            logger.error(f"Team invitation not found: {invitation_id}")
            return False
        
        team = invitation.team
        invited_user = invitation.invited_user
        inviter = invitation.inviter
        hackathon = team.hackathon
        
        # Get team member count
        member_count = db.query(models.TeamMember).filter(
            models.TeamMember.team_id == team.id
        ).count()
        
        # Get member role
        team_member = crud.get_team_member(
            db, team_id=team.id, user_id=invited_user.id
        )
        member_role = team_member.role if team_member else "member"
        
        # Prepare template variables
        frontend_url = self._get_frontend_url()
        team_url = f"{frontend_url}/teams/{team.id}"
        
        variables = {
            "team_name": team.name,
            "team_description": team.description or "No description",
            "hackathon_name": hackathon.name,
            "actor_name": invited_user.name or invited_user.username,
            "member_role": member_role,
            "member_count": member_count,
            "team_url": team_url
        }
        
        # Send notification to inviter
        return self.send_notification(
            notification_type="team_invitation_accepted",
            recipient_email=inviter.email,
            recipient_name=inviter.name or inviter.username,
            language=language,
            variables=variables
        )
    
    def send_team_member_added_notification(
        self,
        db: Session,
        team_id: int,
        user_id: int,
        added_by_id: int,
        language: str = "en"
    ) -> bool:
        """
        Send notification when a user is added to a team.
        
        Args:
            db: Database session
            team_id: ID of the team
            user_id: ID of the user who was added
            added_by_id: ID of the user who added the member
            language: Language code (default: "en")
            
        Returns:
            bool: True if notification was sent successfully
        """
        # Get team details
        team = crud.get_team(db, team_id)
        if not team:
            logger.error(f"Team not found: {team_id}")
            return False
        
        # Get user details
        user = crud.get_user(db, user_id)
        if not user:
            logger.error(f"User not found: {user_id}")
            return False
        
        # Get adder details
        added_by = crud.get_user(db, added_by_id)
        if not added_by:
            logger.error(f"User not found: {added_by_id}")
            return False
        
        hackathon = team.hackathon
        
        # Get team member count
        member_count = db.query(models.TeamMember).filter(
            models.TeamMember.team_id == team.id
        ).count()
        
        # Get member role
        team_member = crud.get_team_member(
            db, team_id=team.id, user_id=user.id
        )
        member_role = team_member.role if team_member else "member"
        
        # Prepare template variables
        frontend_url = self._get_frontend_url()
        team_url = f"{frontend_url}/teams/{team.id}"
        
        variables = {
            "team_name": team.name,
            "team_description": team.description or "No description",
            "hackathon_name": hackathon.name,
            "actor_name": added_by.name or added_by.username,
            "member_role": member_role,
            "member_count": member_count,
            "team_url": team_url
        }
        
        # Send notification to added user
        return self.send_notification(
            notification_type="team_member_added",
            recipient_email=user.email,
            recipient_name=user.name or user.username,
            language=language,
            variables=variables
        )
    
    def send_project_created_notification(
        self,
        db: Session,
        project_id: int,
        language: str = "en",
        recipient_ids: Optional[List[int]] = None
    ) -> bool:
        """
        Send notification when a project is created.
        
        Args:
            db: Database session
            project_id: ID of the created project
            language: Language code (default: "en")
            recipient_ids: List of user IDs to notify
            
        Returns:
            bool: True if all notifications were sent successfully
        """
        # Get project details
        project = crud.get_project(db, project_id)
        if not project:
            logger.error(f"Project not found: {project_id}")
            return False
        
        owner = project.owner
        
        # Prepare template variables
        frontend_url = self._get_frontend_url()
        project_url = f"{frontend_url}/projects/{project.id}"
        
        variables = {
            "project_title": project.title,
            "project_description": project.description or "No description",
            "project_technologies": project.technologies or "Not specified",
            "actor_name": owner.name or owner.username,
            "project_url": project_url
        }
        
        # Add hackathon info if available
        if project.hackathon:
            variables["hackathon_name"] = project.hackathon.name
        
        # Add team info if available
        if project.team:
            variables["team_name"] = project.team.name
        
        # Determine recipients
        if recipient_ids is None:
            # For now, just notify the owner (future: notify followers)
            recipients = [owner]
        else:
            recipients = [
                crud.get_user(db, user_id) for user_id in recipient_ids
            ]
            recipients = [r for r in recipients if r is not None]
        
        # Send notifications to all recipients
        success = True
        for recipient in recipients:
            if recipient.id == owner.id:
                continue  # Don't notify the owner about their own project
            
            recipient_success = self.send_notification(
                notification_type="project_created",
                recipient_email=recipient.email,
                recipient_name=recipient.name or recipient.username,
                language=language,
                variables=variables
            )
            
            if not recipient_success:
                success = False
        
        return success
    
    def _get_frontend_url(self) -> str:
        """Get frontend URL from environment."""
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv("FRONTEND_URL", "http://localhost:3001")


# Global notification service instance
notification_service = NotificationService()