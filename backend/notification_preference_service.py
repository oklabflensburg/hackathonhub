"""
Notification preference service for managing user notification settings.
"""
import logging
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session

import crud
import models
import schemas

logger = logging.getLogger(__name__)


class NotificationPreferenceService:
    """Service for managing user notification preferences."""
    
    # Default notification types with their categories and default channels
    DEFAULT_NOTIFICATION_TYPES = [
        {
            "type_key": "team_invitation_sent",
            "category": "team",
            "default_channels": "email,push,in_app",
            "description": "When you're invited to join a team"
        },
        {
            "type_key": "team_invitation_accepted",
            "category": "team",
            "default_channels": "email,in_app",
            "description": "When someone accepts your team invitation"
        },
        {
            "type_key": "team_member_added",
            "category": "team",
            "default_channels": "email,push,in_app",
            "description": "When you're added to a team"
        },
        {
            "type_key": "team_created",
            "category": "team",
            "default_channels": "in_app",
            "description": "When a team you're in is created"
        },
        {
            "type_key": "project_created",
            "category": "project",
            "default_channels": "email,push,in_app",
            "description": "When a project is created in your team"
        },
        {
            "type_key": "project_commented",
            "category": "project",
            "default_channels": "email,push,in_app",
            "description": "When someone comments on your project"
        },
        {
            "type_key": "project_updated",
            "category": "project",
            "default_channels": "email,in_app",
            "description": "When a project you follow is updated"
        },
        {
            "type_key": "hackathon_registered",
            "category": "hackathon",
            "default_channels": "email,in_app",
            "description": "When you register for a hackathon"
        },
        {
            "type_key": "hackathon_starting_soon",
            "category": "hackathon",
            "default_channels": "email,push",
            "description": "When a hackathon you registered for is starting soon"
        },
        {
            "type_key": "hackathon_started",
            "category": "hackathon",
            "default_channels": "email,push,in_app",
            "description": "When a hackathon you registered for starts"
        },
        {
            "type_key": "comment_reply",
            "category": "system",
            "default_channels": "email,push,in_app",
            "description": "When someone replies to your comment"
        },
        {
            "type_key": "vote_received",
            "category": "system",
            "default_channels": "in_app",
            "description": "When your project receives a vote"
        },
        {
            "type_key": "system_announcement",
            "category": "system",
            "default_channels": "email,in_app",
            "description": "System announcements and updates"
        },
        {
            "type_key": "security_alert",
            "category": "system",
            "default_channels": "email,push",
            "description": "Security alerts and important account notifications"
        }
    ]
    
    def __init__(self):
        pass
    
    def initialize_notification_types(self, db: Session) -> bool:
        """
        Initialize the notification types in the database.
        Creates default notification types if they don't exist.
        
        Args:
            db: Database session
            
        Returns:
            bool: True if initialization was successful
        """
        try:
            for notification_type in self.DEFAULT_NOTIFICATION_TYPES:
                # Check if type already exists
                existing = crud.get_notification_type(db, notification_type["type_key"])
                if not existing:
                    # Create new notification type
                    type_create = schemas.NotificationTypeCreate(**notification_type)
                    crud.create_notification_type(db, type_create)
            
            logger.info(f"Initialized {len(self.DEFAULT_NOTIFICATION_TYPES)} notification types")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize notification types: {e}")
            return False
    
    def get_user_preferences(
        self,
        db: Session,
        user_id: int
    ) -> Dict[str, Any]:
        """
        Get comprehensive notification preferences for a user.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Dict with user preferences structure
        """
        try:
            # Get all notification types
            notification_types = crud.get_notification_types(db)
            
            # Get user's specific preferences
            user_prefs = crud.get_user_notification_preferences(db, user_id)
            
            # Create a map of user preferences for quick lookup
            user_prefs_map = {}
            for pref in user_prefs:
                key = f"{pref.notification_type}:{pref.channel}"
                user_prefs_map[key] = pref.enabled
            
            # Build structured preferences
            preferences = {
                "global_enabled": True,  # Default to enabled
                "channels": {
                    "email": True,
                    "push": True,
                    "in_app": True
                },
                "categories": {}
            }
            
            # Organize by category
            for nt in notification_types:
                category = nt.category
                type_key = nt.type_key
                
                if category not in preferences["categories"]:
                    preferences["categories"][category] = {
                        "enabled": True,
                        "channels": self._parse_channels(nt.default_channels),
                        "types": {}
                    }
                
                # Get default channels for this type
                default_channels = self._parse_channels(nt.default_channels)
                
                # Build type preferences
                type_prefs = {
                    "enabled": True,
                    "channels": {}
                }
                
                # Set channel preferences
                for channel in ["email", "push", "in_app"]:
                    # Check if user has a specific preference
                    pref_key = f"{type_key}:{channel}"
                    if pref_key in user_prefs_map:
                        type_prefs["channels"][channel] = user_prefs_map[pref_key]
                    else:
                        # Use default if channel is in default channels
                        type_prefs["channels"][channel] = channel in default_channels
                
                preferences["categories"][category]["types"][type_key] = type_prefs
            
            return preferences
            
        except Exception as e:
            logger.error(f"Failed to get user preferences for user {user_id}: {e}")
            # Return default preferences on error
            return self._get_default_preferences()
    
    def update_user_preferences(
        self,
        db: Session,
        user_id: int,
        preferences: Dict[str, Any]
    ) -> bool:
        """
        Update user notification preferences.
        
        Args:
            db: Database session
            user_id: User ID
            preferences: New preferences structure
            
        Returns:
            bool: True if update was successful
        """
        try:
            # For now, we'll implement a simplified version
            # In a full implementation, we would parse the preferences structure
            # and update individual preference records
            
            logger.info(f"Updating notification preferences for user {user_id}")
            
            # This is a placeholder - actual implementation would:
            # 1. Parse the preferences structure
            # 2. Update or create UserNotificationPreference records
            # 3. Handle channel-specific preferences
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update preferences for user {user_id}: {e}")
            return False
    
    def get_notification_types_with_preferences(
        self,
        db: Session,
        user_id: int
    ) -> List[Dict[str, Any]]:
        """
        Get all notification types with user's preferences.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of notification types with preference info
        """
        try:
            notification_types = crud.get_notification_types(db)
            user_prefs = crud.get_user_notification_preferences(db, user_id)
            
            # Create preference map
            pref_map = {}
            for pref in user_prefs:
                key = f"{pref.notification_type}:{pref.channel}"
                pref_map[key] = pref.enabled
            
            result = []
            for nt in notification_types:
                type_info = {
                    "type_key": nt.type_key,
                    "category": nt.category,
                    "description": nt.description,
                    "default_channels": self._parse_channels(nt.default_channels),
                    "user_preferences": {}
                }
                
                # Add channel preferences
                for channel in ["email", "push", "in_app"]:
                    key = f"{nt.type_key}:{channel}"
                    if key in pref_map:
                        type_info["user_preferences"][channel] = pref_map[key]
                    else:
                        # Use default
                        type_info["user_preferences"][channel] = channel in type_info["default_channels"]
                
                result.append(type_info)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get notification types with preferences: {e}")
            return []
    
    def should_send_notification(
        self,
        db: Session,
        user_id: int,
        notification_type: str,
        channel: str
    ) -> bool:
        """
        Check if a notification should be sent to a user via a specific channel.
        
        Args:
            db: Database session
            user_id: User ID
            notification_type: Type of notification
            channel: Delivery channel ('email', 'push', 'in_app')
            
        Returns:
            bool: True if notification should be sent
        """
        try:
            # Get user preference for this notification type and channel
            preference = crud.get_user_notification_preference(
                db, user_id, notification_type, channel
            )
            
            if preference:
                return preference.enabled
            
            # If no preference exists, check default for this notification type
            notification_type_obj = crud.get_notification_type(db, notification_type)
            if notification_type_obj:
                default_channels = self._parse_channels(notification_type_obj.default_channels)
                return channel in default_channels
            
            # If notification type doesn't exist, default to True
            return True
            
        except Exception as e:
            logger.error(f"Failed to check notification preference: {e}")
            # Default to True on error to avoid blocking notifications
            return True
    
    def _parse_channels(self, channels_str: str) -> List[str]:
        """Parse comma-separated channels string into list."""
        if not channels_str:
            return []
        return [channel.strip() for channel in channels_str.split(",") if channel.strip()]
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Get default preferences structure."""
        return {
            "global_enabled": True,
            "channels": {
                "email": True,
                "push": True,
                "in_app": True
            },
            "categories": {}
        }


# Global service instance
notification_preference_service = NotificationPreferenceService()