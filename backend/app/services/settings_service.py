"""Settings service for managing user settings in the Hackathon Hub Platform."""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import pyotp
import qrcode
import io
import base64
import secrets
import hashlib

from app.domain.models.user import User
from app.domain.schemas.settings import (
    UserSettings, UserSettingsUpdate, SettingsValidationResult,
    ValidationError, ProfileSettings, SecuritySettings, PrivacySettings,
    PlatformPreferences, NotificationSettings, OAuthConnections,
    DataManagement, UserSession, TrustedDevice, PasswordChangeRequest,
    TwoFactorSetupResponse, TwoFactorVerifyRequest, TwoFactorDisableRequest,
    SessionRevokeRequest, DataExportRequest, AccountDeletionRequest,
    SettingsResponse, AccountImpactResponse, OwnedResourceSummary,
    AccountClosureRequest
)
from app.services.user_service import UserService
from app.services.notification_preference_service import (
    NotificationPreferenceService
)
from app.services.email_auth_service import EmailAuthService
from app.i18n.helpers import raise_not_found, raise_bad_request
from app.repositories.user_repository import RefreshTokenRepository
from app.domain.models.hackathon import Hackathon
from app.domain.models.team import Team
from app.domain.models.project import Project


class SettingsService:
    """Service for managing user settings."""

    def __init__(self):
        self.user_service = UserService()
        self.notification_service = NotificationPreferenceService()
        self.refresh_token_repository = RefreshTokenRepository()

    def get_user_settings(
        self,
        db: Session,
        user_id: int,
        current_token_id: Optional[str] = None
    ) -> SettingsResponse:
        """
        Get all settings for a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            SettingsResponse object with settings and metadata
        """
        user = self.user_service.user_repo.get(db, user_id)
        if not user:
            raise_not_found("en", "user")

        # Get notification preferences
        notification_prefs = self.notification_service.get_user_preferences(
            db, user_id
        )

        # Build settings from user data
        settings = self._build_settings_from_user(
            db,
            user,
            notification_prefs,
            current_token_id=current_token_id
        )

        # Return as SettingsResponse
        return SettingsResponse(
            settings=settings,
            last_updated=datetime.utcnow(),
            version="1.0.0"
        )

    def update_user_settings(
        self,
        db: Session,
        user_id: int,
        settings_update: UserSettingsUpdate
    ) -> SettingsResponse:
        """
        Update user settings.

        Args:
            db: Database session
            user_id: User ID
            settings_update: Settings to update

        Returns:
            Updated UserSettings object
        """
        # Validate the update
        validation_result = self._validate_settings_update(
            db, user_id, settings_update
        )
        if not validation_result.valid:
            raise_bad_request(
                "en",
                "Invalid settings update",
                {"errors": [err.dict() for err in validation_result.errors]}
            )

        # Apply updates
        if settings_update.profile:
            self._update_profile_settings(db, user_id, settings_update.profile)

        if settings_update.security:
            self._update_security_settings(
                db, user_id, settings_update.security
            )

        if settings_update.privacy:
            self._update_privacy_settings(
                db, user_id, settings_update.privacy
            )

        if settings_update.platform:
            self._update_platform_preferences(
                db, user_id, settings_update.platform
            )

        if settings_update.notifications:
            self._update_notification_settings(
                db, user_id, settings_update.notifications
            )

        if settings_update.connections:
            self._update_oauth_connections(
                db, user_id, settings_update.connections
            )

        if settings_update.data:
            self._update_data_management(
                db, user_id, settings_update.data
            )

        # Get updated settings
        return self.get_user_settings(db, user_id)

    def _get_user_or_raise(self, db: Session, user_id: int) -> User:
        user = self.user_service.user_repo.get(db, user_id)
        if not user:
            raise_not_found("en", "user")
        return user

    def _update_profile_settings(
        self,
        db: Session,
        user_id: int,
        profile: ProfileSettings
    ) -> None:
        user = self._get_user_or_raise(db, user_id)
        user.username = profile.username
        user.email = profile.email
        user.name = profile.name
        user.avatar_url = profile.avatar_url
        user.bio = profile.bio
        user.location = profile.location
        user.company = profile.company
        db.add(user)
        db.commit()
        db.refresh(user)

    def _update_security_settings(
        self,
        db: Session,
        user_id: int,
        security: SecuritySettings
    ) -> None:
        user = self._get_user_or_raise(db, user_id)
        user.two_factor_enabled = bool(security.two_factor_enabled)
        db.add(user)
        db.commit()

    def _update_privacy_settings(
        self,
        db: Session,
        user_id: int,
        privacy: PrivacySettings
    ) -> None:
        user = self._get_user_or_raise(db, user_id)
        # These columns do not exist in older schemas; ignore safely there.
        for field, value in (
            ("profile_visibility", privacy.profile_visibility),
            ("email_visibility", privacy.email_visibility),
            ("show_online_status", privacy.show_online_status),
            ("allow_messages_from", privacy.allow_messages_from),
            ("show_activity", privacy.show_activity),
            ("allow_tagging", privacy.allow_tagging),
            ("data_sharing_analytics", privacy.data_sharing.analytics),
            ("data_sharing_marketing", privacy.data_sharing.marketing),
            ("data_sharing_third_parties", privacy.data_sharing.third_parties),
        ):
            if hasattr(user, field):
                setattr(user, field, value)
        db.add(user)
        db.commit()

    def _update_platform_preferences(
        self,
        db: Session,
        user_id: int,
        platform: PlatformPreferences
    ) -> None:
        user = self._get_user_or_raise(db, user_id)
        user.theme = platform.theme.value
        user.language = platform.language
        user.timezone = platform.timezone
        user.date_format = platform.date_format.value
        user.time_format = platform.time_format.value
        user.notifications_sound = bool(platform.notifications_sound)
        user.reduce_animations = bool(platform.reduce_animations)
        user.compact_mode = bool(platform.compact_mode)
        user.default_view_hackathons = platform.default_view.hackathons
        user.default_view_projects = platform.default_view.projects
        user.default_view_notifications = platform.default_view.notifications
        db.add(user)
        db.commit()
        db.refresh(user)

    def _update_notification_settings(
        self,
        db: Session,
        user_id: int,
        notifications: NotificationSettings
    ) -> None:
        quiet_hours = notifications.quiet_hours
        normalized_quiet_hours = None
        if quiet_hours is not None:
            normalized_quiet_hours = {
                "enabled": quiet_hours.enabled,
                "start": quiet_hours.start,
                "end": quiet_hours.end,
            }

        normalized = {
            "channels": {
                "email": notifications.email_enabled,
                "push": notifications.push_enabled,
                "in_app": True,
            },
        }
        if normalized_quiet_hours is not None:
            normalized["quiet_hours"] = normalized_quiet_hours
        self.notification_service.update_user_preferences(
            db, user_id, normalized
        )

    def _update_oauth_connections(
        self,
        db: Session,
        user_id: int,
        connections: OAuthConnections
    ) -> None:
        return None

    def _update_data_management(
        self,
        db: Session,
        user_id: int,
        data: DataManagement
    ) -> None:
        return None

    def change_password(
        self,
        db: Session,
        user_id: int,
        password_change: PasswordChangeRequest
    ) -> bool:
        """
        Change user password.

        Args:
            db: Database session
            user_id: User ID
            password_change: Password change request

        Returns:
            True if successful
        """
        user = self.user_service.get_user(db, user_id)
        if not user:
            raise_not_found("en", "user")

        # Verify current password
        if not EmailAuthService.verify_password(
            password_change.current_password, user.password_hash
        ):
            raise_bad_request("en", "Current password is incorrect")

        # Update password
        new_password_hash = EmailAuthService.get_password_hash(
            password_change.new_password
        )
        user.password_hash = new_password_hash
        db.commit()

        return True

    def enable_two_factor(
        self, db: Session, user_id: int
    ) -> TwoFactorSetupResponse:
        """
        Enable two-factor authentication for a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            TwoFactorSetupResponse with QR code and backup codes
        """
        # Get the SQLAlchemy User model directly from repository
        from app.repositories.user_repository import UserRepository
        user_repo = UserRepository()
        user = user_repo.get(db, user_id)
        if not user:
            raise_not_found("en", "user")

        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Enabling 2FA for user {user_id}")

        # Generate TOTP secret
        secret = pyotp.random_base32()
        logger.info(f"Generated secret for user {user_id}: {secret}")

        # Generate backup codes
        backup_codes = [
            secrets.token_hex(4).upper() for _ in range(10)
        ]

        # Store backup codes hash (for verification)
        backup_codes_hash = hashlib.sha256(
            "|".join(backup_codes).encode()
        ).hexdigest()

        # Update user
        user.two_factor_secret = secret
        user.two_factor_backup_codes = backup_codes_hash
        user.two_factor_enabled = False  # Not enabled until verified
        db.commit()
        logger.info(
            f"2FA secret saved for user {user_id}. "
            f"Secret: {secret[:10]}..., "
            f"Backup codes hash: {backup_codes_hash[:10]}..."
        )

        # Generate QR code
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user.email,
            issuer_name="Hackathon Hub"
        )
        logger.debug(f"Generated provisioning URI: {provisioning_uri}")

        qr = qrcode.make(provisioning_uri)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

        return TwoFactorSetupResponse(
            qr_code=f"data:image/png;base64,{qr_code_base64}",
            secret=secret,
            backup_codes=backup_codes
        )

    def verify_two_factor(
        self,
        db: Session,
        user_id: int,
        verify_request: TwoFactorVerifyRequest
    ) -> bool:
        """
        Verify two-factor authentication setup.

        Args:
            db: Database session
            user_id: User ID
            verify_request: Verification request

        Returns:
            True if verification successful
        """
        # Get the SQLAlchemy User model directly from repository
        from app.repositories.user_repository import UserRepository
        user_repo = UserRepository()
        user = user_repo.get(db, user_id)
        if not user:
            raise_not_found("en", "user")

        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        secret_preview = (
            f"{user.two_factor_secret[:10]}..."
            if user.two_factor_secret else "None"
        )
        logger.debug(
            f"2FA verification for user {user_id}: "
            f"secret={secret_preview}, enabled={user.two_factor_enabled}"
        )

        if not user.two_factor_secret:
            logger.warning(
                f"User {user_id} attempted 2FA verification without secret"
            )
            raise_bad_request("en", "Two-factor authentication not set up")

        # Verify TOTP code
        import time
        totp = pyotp.TOTP(user.two_factor_secret)
        current_time = time.time()
        logger.debug(
            f"Verifying code: {verify_request.code}, "
            f"secret: {user.two_factor_secret[:10]}..., "
            f"current time: {current_time}"
        )

        # Try verification with default window (current +/- 30 seconds)
        current_code = totp.now()
        logger.debug(f"Current TOTP code for secret: {current_code}")

        if totp.verify(verify_request.code):
            user.two_factor_enabled = True
            db.commit()
            logger.info(f"2FA successfully verified for user {user_id}")
            return True

        # Try with extended windows in case of time drift
        for window in [2, 3, 5]:  # Try up to 2.5 minutes drift
            if totp.verify(verify_request.code, valid_window=window):
                user.two_factor_enabled = True
                db.commit()
                logger.info(
                    f"2FA verified with window={window} for user {user_id}"
                )
                return True

        # Check backup codes
        if user.two_factor_backup_codes:
            # In a real implementation, you would check against stored hashes
            pass

        logger.warning(
            f"Invalid verification code for user {user_id}: "
            f"code={verify_request.code}, "
            f"secret={user.two_factor_secret[:10]}..."
        )
        raise_bad_request("en", "Invalid verification code")

    def disable_two_factor(
        self,
        db: Session,
        user_id: int,
        disable_request: TwoFactorDisableRequest
    ) -> bool:
        """
        Disable two-factor authentication.

        Args:
            db: Database session
            user_id: User ID
            disable_request: Disable request with password

        Returns:
            True if disabled successfully
        """
        # Get the SQLAlchemy User model directly from repository
        from app.repositories.user_repository import UserRepository
        user_repo = UserRepository()
        user = user_repo.get(db, user_id)
        if not user:
            raise_not_found("en", "user")

        # Verify password
        if not EmailAuthService.verify_password(
            disable_request.password, user.password_hash
        ):
            raise_bad_request("en", "Password is incorrect")

        # Disable 2FA
        user.two_factor_secret = None
        user.two_factor_backup_codes = None
        user.two_factor_enabled = False
        db.commit()

        return True

    def get_security_settings(
        self,
        db: Session,
        user_id: int,
        current_token_id: Optional[str] = None
    ) -> SecuritySettings:
        user = self.user_service.get_user(db, user_id)
        if not user:
            raise_not_found("en", "user")

        return self._build_security_settings(
            db,
            user,
            current_token_id=current_token_id
        )

    def get_active_sessions(
        self,
        db: Session,
        user_id: int,
        current_token_id: Optional[str] = None
    ) -> List[UserSession]:
        return self._build_active_sessions(
            db,
            user_id,
            current_token_id=current_token_id
        )

    def revoke_session(
        self,
        db: Session,
        user_id: int,
        revoke_request: SessionRevokeRequest,
        current_token_id: Optional[str] = None
    ) -> bool:
        if revoke_request.session_id is None:
            raise_bad_request("en", "Session ID is required")

        return self._revoke_refresh_token(
            db,
            user_id,
            revoke_request.session_id,
            current_token_id=current_token_id
        )

    def revoke_trusted_device(
        self,
        db: Session,
        user_id: int,
        device_id: str,
        current_token_id: Optional[str] = None
    ) -> bool:
        return self._revoke_refresh_token(
            db,
            user_id,
            device_id,
            current_token_id=current_token_id
        )

    def get_account_impact(
        self,
        db: Session,
        user_id: int
    ) -> AccountImpactResponse:
        user = self.user_service.user_repo.get(db, user_id)
        if not user:
            raise_not_found("en", "user")

        hackathons = db.query(Hackathon).filter(
            Hackathon.owner_id == user_id).all()
        teams = db.query(Team).filter(
            Team.created_by == user_id).all()
        projects = db.query(Project).filter(
            Project.owner_id == user_id).all()

        hackathon_items = [
            OwnedResourceSummary(
                id=item.id,
                name=item.name or f"Hackathon #{item.id}",
                resource_type="hackathon"
            )
            for item in hackathons
        ]
        team_items = [
            OwnedResourceSummary(
                id=item.id,
                name=item.name or f"Team #{item.id}",
                resource_type="team"
            )
            for item in teams
        ]
        project_items = [
            OwnedResourceSummary(
                id=item.id,
                name=item.title or f"Project #{item.id}",
                resource_type="project"
            )
            for item in projects
        ]

        has_owned_resources = bool(
            hackathon_items or team_items or project_items
        )
        return AccountImpactResponse(
            can_delete=not has_owned_resources,
            can_deactivate=True,
            requires_transfer=has_owned_resources,
            hackathons=hackathon_items,
            teams=team_items,
            projects=project_items,
            message=(
                "Permanent deletion is blocked while you still "
                "own hackathons, teams, or projects."
                if has_owned_resources else
                "Your account can be permanently deleted."
            )
        )

    def deactivate_account(
        self,
        db: Session,
        user_id: int,
        request: AccountClosureRequest
    ) -> None:
        user = self._validate_account_closure_request(
            db,
            user_id,
            request,
            expected_confirmation="DEACTIVATE ACCOUNT"
        )
        user.is_active = False
        user.deactivated_at = datetime.utcnow()
        self.refresh_token_repository.revoke_all_for_user(db, user_id)
        db.add(user)
        db.commit()

    def delete_account(
        self,
        db: Session,
        user_id: int,
        request: AccountClosureRequest
    ) -> AccountImpactResponse:
        user = self._validate_account_closure_request(
            db,
            user_id,
            request,
            expected_confirmation="DELETE MY ACCOUNT"
        )
        impact = self.get_account_impact(db, user_id)
        if not impact.can_delete:
            raise_bad_request(
                "en",
                "Account cannot be permanently deleted while owned resources still exist."
            )

        user.is_active = False
        user.deactivated_at = datetime.utcnow()
        user.email = f"deleted-user-{user.id}@deleted.local"
        user.username = f"deleted-user-{user.id}"
        user.name = "Deleted User"
        user.avatar_url = None
        user.bio = None
        user.location = None
        user.company = None
        user.blog = None
        user.twitter_username = None
        user.password_hash = None
        user.google_id = None
        user.github_id = None
        user.two_factor_secret = None
        user.two_factor_backup_codes = None
        user.two_factor_enabled = False
        user.email_verified = False
        self.refresh_token_repository.revoke_all_for_user(db, user_id)
        db.add(user)
        db.commit()
        return impact

    def request_data_export(
        self,
        db: Session,
        user_id: int,
        export_request: DataExportRequest
    ) -> Dict[str, Any]:
        """
        Request data export for a user.

        Args:
            db: Database session
            user_id: User ID
            export_request: Export request

        Returns:
            Export status information
        """
        user = self.user_service.get_user(db, user_id)
        if not user:
            raise_not_found("en", "user")

        # In a real implementation, this would queue an export job
        # For now, just update the user record
        user.data_export_requested_at = datetime.utcnow()
        db.commit()

        return {
            "request_id": (
                f"export_{user_id}_{int(datetime.utcnow().timestamp())}"
            ),
            "status": "pending",
            "estimated_completion": (
                datetime.utcnow() + timedelta(hours=24)
            ).isoformat()
        }

    def request_account_deletion(
        self,
        db: Session,
        user_id: int,
        deletion_request: AccountDeletionRequest
    ) -> bool:
        """
        Request account deletion.

        Args:
            db: Database session
            user_id: User ID
            deletion_request: Deletion request

        Returns:
            True if deletion requested successfully
        """
        user = self.user_service.get_user(db, user_id)
        if not user:
            raise_not_found("en", "user")

        # Verify password
        if not EmailAuthService.verify_password(
            deletion_request.password, user.password_hash
        ):
            raise_bad_request("en", "Password is incorrect")

        # Schedule deletion (in a real implementation, this would be async)
        user.account_deletion_requested_at = datetime.utcnow()
        db.commit()

        return True

    def _validate_account_closure_request(
        self,
        db: Session,
        user_id: int,
        request: AccountClosureRequest,
        expected_confirmation: str
    ):
        user = self.user_service.user_repo.get(db, user_id)
        if not user:
            raise_not_found("en", "user")

        if user.auth_method == "email":
            if not request.password or not user.password_hash:
                raise_bad_request("en", "Password is required")
            if not EmailAuthService.verify_password(request.password, user.password_hash):
                raise_bad_request("en", "Password is incorrect")
            if request.confirmation != expected_confirmation:
                raise_bad_request("en", "Confirmation text is invalid")
        else:
            if request.confirmation != expected_confirmation:
                raise_bad_request("en", "Confirmation text is invalid")

        return user

    # Private helper methods

    def _build_settings_from_user(
        self,
        db: Session,
        user: User,
        notification_prefs: Any,
        current_token_id: Optional[str] = None
    ) -> UserSettings:
        """Build UserSettings from User model."""
        # Build profile settings
        profile = ProfileSettings(
            username=user.username,
            email=user.email,
            name=user.name,
            avatar_url=user.avatar_url,
            bio=user.bio,
            location=user.location,
            company=user.company
        )

        # Build security settings
        security = self._build_security_settings(
            db,
            user,
            current_token_id=current_token_id
        )

        # Build privacy settings
        privacy = PrivacySettings(
            profile_visibility=getattr(user, 'profile_visibility', 'public'),
            email_visibility=getattr(user, 'email_visibility', 'private'),
            show_online_status=getattr(user, 'show_online_status', True),
            allow_messages_from=getattr(
                user, 'allow_messages_from', 'all_users'
            ),
            show_activity=getattr(user, 'show_activity', True),
            allow_tagging=getattr(user, 'allow_tagging', True),
            data_sharing={
                "analytics": getattr(user, 'data_sharing_analytics', True),
                "marketing": getattr(user, 'data_sharing_marketing', False),
                "third_parties": getattr(
                    user, 'data_sharing_third_parties', False
                )
            }
        )

        # Build platform preferences
        platform = PlatformPreferences(
            theme=getattr(user, 'theme', 'system'),
            language=getattr(user, 'language', 'en'),
            timezone=getattr(user, 'timezone', 'UTC'),
            date_format=getattr(user, 'date_format', 'YYYY-MM-DD'),
            time_format=getattr(user, 'time_format', '24h'),
            notifications_sound=getattr(user, 'notifications_sound', True),
            reduce_animations=getattr(user, 'reduce_animations', False),
            compact_mode=getattr(user, 'compact_mode', False),
            default_view={
                "hackathons": getattr(user, 'default_view_hackathons', 'grid'),
                "projects": getattr(user, 'default_view_projects', 'grid'),
                "notifications": getattr(
                    user, 'default_view_notifications', 'grouped'
                )
            }
        )

        # Build notification settings from notification preferences
        notifications = self._build_notification_settings(notification_prefs)

        # Build OAuth connections
        connections = OAuthConnections(
            github=self._build_github_connection(user),
            google=self._build_google_connection(user)
        )

        # Build data management
        data = DataManagement(
            export_status=self._build_export_status(user),
            deletion_status=self._build_deletion_status(user)
        )

        return UserSettings(
            profile=profile,
            security=security,
            privacy=privacy,
            platform=platform,
            notifications=notifications,
            connections=connections,
            data=data
        )

    def _build_notification_settings(self, prefs: Any) -> NotificationSettings:
        """Build NotificationSettings from notification preferences."""
        channels = prefs.get("channels", {}) if isinstance(prefs, dict) else {}
        quiet_hours = (
            prefs.get("quiet_hours", {}) if isinstance(prefs, dict) else {}
        ) or {}

        categories = {
            "project_updates": True,
            "team_invitations": True,
            "hackathon_announcements": True,
            "comment_replies": True,
            "vote_notifications": True,
            "mention_notifications": True,
            "system_announcements": True,
            "newsletter": False,
        }

        if isinstance(prefs, dict):
            category_map = prefs.get("categories", {})
            if isinstance(category_map, dict):
                for key, value in category_map.items():
                    if key in categories and isinstance(value, dict):
                        categories[key] = bool(value.get("enabled", True))
                    elif key in categories:
                        categories[key] = bool(value)

        return NotificationSettings(
            email_enabled=bool(channels.get("email", True)),
            push_enabled=bool(channels.get("push", True)),
            in_app_enabled=bool(channels.get("in_app", True)),
            categories=categories,
            quiet_hours={
                "enabled": bool(quiet_hours.get("enabled", False)),
                "start": quiet_hours.get("start", "22:00"),
                "end": quiet_hours.get("end", "08:00"),
            },
        )

    def _build_github_connection(self, user: User) -> Optional[Dict[str, Any]]:
        """Build GitHub OAuth connection info."""
        if user.github_id:
            return {
                "connected": True,
                "username": user.username,
                "avatar_url": user.avatar_url,
                "connected_at": user.created_at
            }
        return None

    def _build_google_connection(self, user: User) -> Optional[Dict[str, Any]]:
        """Build Google OAuth connection info."""
        if user.google_id:
            return {
                "connected": True,
                "email": user.email,
                "connected_at": user.created_at
            }
        return None

    def _build_export_status(self, user: User) -> Optional[Dict[str, Any]]:
        """Build export status from user data."""
        # Check if attribute exists (for backward compatibility)
        if (hasattr(user, 'data_export_requested_at') and
                user.data_export_requested_at):
            return {
                "requested_at": user.data_export_requested_at,
                "status": "completed",  # Simplified
                "download_url": "/api/v1/users/me/exports/latest",
                "expires_at": user.data_export_requested_at + timedelta(days=7)
            }
        return None

    def _build_deletion_status(self, user: User) -> Optional[Dict[str, Any]]:
        """Build deletion status from user data."""
        # Check if attribute exists (for backward compatibility)
        if (hasattr(user, 'account_deletion_requested_at') and
                user.account_deletion_requested_at):
            return {
                "requested_at": user.account_deletion_requested_at,
                "scheduled_for": (
                    user.account_deletion_requested_at + timedelta(days=30)
                ),
                "status": "scheduled"
            }
        return None

    def _build_security_settings(
        self,
        db: Session,
        user: User,
        current_token_id: Optional[str] = None
    ) -> SecuritySettings:
        active_sessions = self._build_active_sessions(
            db,
            user.id,
            current_token_id=current_token_id
        )
        trusted_devices = self._build_trusted_devices(
            db,
            user.id,
            current_token_id=current_token_id
        )
        remaining_backup_codes = 10 if user.two_factor_backup_codes else 0

        return SecuritySettings(
            two_factor_enabled=user.two_factor_enabled or False,
            trusted_devices_count=len(trusted_devices),
            remaining_backup_codes=remaining_backup_codes,
            active_sessions=active_sessions,
            trusted_devices=trusted_devices
        )

    def _build_active_sessions(
        self,
        db: Session,
        user_id: int,
        current_token_id: Optional[str] = None
    ) -> List[UserSession]:
        tokens = self.refresh_token_repository.get_by_user_id(db, user_id)
        active_tokens = [
            token for token in tokens
            if self._is_token_active(token)
        ]
        active_tokens.sort(
            key=lambda token: token.created_at or datetime.utcnow(),
            reverse=True
        )
        return [
            self._serialize_refresh_token(token, current_token_id, UserSession)
            for token in active_tokens
        ]

    def _build_trusted_devices(
        self,
        db: Session,
        user_id: int,
        current_token_id: Optional[str] = None
    ) -> List[TrustedDevice]:
        tokens = self.refresh_token_repository.get_by_user_id(db, user_id)
        persistent_tokens = [
            token for token in tokens
            if token.is_persistent and self._is_token_active(token)
        ]
        persistent_tokens.sort(
            key=lambda token: token.created_at or datetime.utcnow(),
            reverse=True
        )
        return [
            self._serialize_refresh_token(token, current_token_id, TrustedDevice)
            for token in persistent_tokens
        ]

    def _serialize_refresh_token(
        self,
        token,
        current_token_id: Optional[str],
        schema_cls
    ):
        device_name = token.device_info or "Unbekanntes Gerät"
        device_type = self._infer_device_type(device_name)
        is_current = bool(current_token_id and token.token_id == current_token_id)
        last_active = token.created_at or datetime.utcnow()

        return schema_cls(
            id=str(token.id),
            device=device_name,
            device_name=device_name,
            device_type=device_type,
            location=None,
            ip_address=token.ip_address,
            last_active=last_active,
            last_activity=last_active,
            created_at=token.created_at or datetime.utcnow(),
            expires_at=token.expires_at,
            current=is_current,
            is_current=is_current
        )

    def _revoke_refresh_token(
        self,
        db: Session,
        user_id: int,
        token_row_id: str,
        current_token_id: Optional[str] = None
    ) -> bool:
        try:
            row_id = int(token_row_id)
        except (TypeError, ValueError):
            raise_bad_request("en", "Invalid session identifier")

        token = self.refresh_token_repository.get(db, row_id)
        if not token or token.user_id != user_id:
            raise_not_found("en", "session")

        if current_token_id and token.token_id == current_token_id:
            raise_bad_request("en", "Current session cannot be revoked here")

        db.delete(token)
        db.commit()
        return True

    def _infer_device_type(
        self,
        device_info: Optional[str]
    ) -> str:
        value = (device_info or "").lower()
        if any(keyword in value for keyword in ("iphone", "android", "mobile", "phone")):
            return "mobile"
        if any(keyword in value for keyword in ("ipad", "tablet")):
            return "tablet"
        if any(keyword in value for keyword in ("windows", "mac", "linux", "chrome", "firefox", "safari", "desktop")):
            return "desktop"
        return "unknown"

    def _is_token_active(self, token) -> bool:
        if not token.expires_at:
            return False
        now = datetime.now(token.expires_at.tzinfo) if token.expires_at.tzinfo else datetime.utcnow()
        return token.expires_at > now

    def _validate_settings_update(
        self,
        db: Session,
        user_id: int,
        settings_update: UserSettingsUpdate
    ) -> SettingsValidationResult:
        """Validate settings update."""
        errors = []

        if settings_update.profile:
            errors.extend(
                self._validate_profile_update(
                    db, user_id, settings_update.profile
                )
            )

        # Add validation for other sections as needed

        return SettingsValidationResult(
            valid=len(errors) == 0,
            errors=errors
        )

    def _validate_profile_update(
        self,
        db: Session,
        user_id: int,
        profile_update: ProfileSettings
    ) -> List[ValidationError]:
        """Validate profile update."""
        errors = []

        # Check username uniqueness
        if profile_update.username:
            existing_user = self.user_service.get_user_by_username(
                db, profile_update.username
            )
            if existing_user and existing_user.id != user_id:
                errors.append(ValidationError(
                    field="username",
                    message="Username already taken",
                    code="USERNAME_EXISTS"
                ))

        # Check email uniqueness
        if profile_update.email:
            existing_user = self.user_service.get_user_by_email(
                db, profile_update.email
            )
            if existing_user and existing_user.id != user_id:
                errors.append(ValidationError(
                    field="email",
                    message="Email already in use",
                    code="EMAIL_EXISTS"
                ))

        return errors
