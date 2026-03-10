"""
Settings service for managing user settings in the Hackathon Hub Platform.
"""
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
    DataManagement, UserSession, PasswordChangeRequest,
    TwoFactorSetupResponse, TwoFactorVerifyRequest, TwoFactorDisableRequest,
    SessionRevokeRequest, DataExportRequest, AccountDeletionRequest,
    SettingsResponse
)
from app.services.user_service import UserService
from app.services.notification_preference_service import (
    NotificationPreferenceService
)
from app.services.email_auth_service import EmailAuthService
from app.i18n.helpers import raise_not_found, raise_bad_request


class SettingsService:
    """Service for managing user settings."""

    def __init__(self):
        self.user_service = UserService()
        self.notification_service = NotificationPreferenceService()

    def get_user_settings(self, db: Session, user_id: int) -> SettingsResponse:
        """
        Get all settings for a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            SettingsResponse object with settings and metadata
        """
        user = self.user_service.get_user(db, user_id)
        if not user:
            raise_not_found("en", "user")

        # Get notification preferences
        notification_prefs = self.notification_service.get_user_preferences(
            db, user_id
        )

        # Build settings from user data
        settings = self._build_settings_from_user(user, notification_prefs)

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

    def get_active_sessions(
        self, db: Session, user_id: int
    ) -> List[UserSession]:
        """
        Get active sessions for a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            List of active user sessions
        """
        # In a real implementation, this would query a sessions table
        # For now, return a mock session
        return [
            UserSession(
                id="current_session_123",
                device="Chrome on Windows",
                location="Berlin, DE",
                ip_address="192.168.1.1",
                last_active=datetime.utcnow(),
                created_at=datetime.utcnow() - timedelta(days=7),
                expires_at=datetime.utcnow() + timedelta(days=30),
                current=True
            )
        ]

    def revoke_session(
        self,
        db: Session,
        user_id: int,
        revoke_request: SessionRevokeRequest
    ) -> bool:
        """
        Revoke a user session.

        Args:
            db: Database session
            user_id: User ID
            revoke_request: Session revoke request

        Returns:
            True if session revoked
        """
        # In a real implementation, this would invalidate the session
        # For now, just return success
        return True

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

    # Private helper methods

    def _build_settings_from_user(
        self,
        user: User,
        notification_prefs: Any
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
        security = SecuritySettings(
            two_factor_enabled=user.two_factor_enabled or False,
            active_sessions=self._get_mock_sessions()
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
        # This is a simplified version
        # In a real implementation, you would map the preferences
        return NotificationSettings()

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

    def _get_mock_sessions(self) -> List[UserSession]:
        """Get mock sessions for development."""
        return [
            UserSession(
                id="session_1",
                device="Chrome on Windows",
                location="Berlin, Germany",
                ip_address="192.168.1.100",
                last_active=datetime.utcnow() - timedelta(hours=2),
                created_at=datetime.utcnow() - timedelta(days=7),
                expires_at=datetime.utcnow() + timedelta(days=23),
                current=True
            ),
            UserSession(
                id="session_2",
                device="Safari on iPhone",
                location="Hamburg, Germany",
                ip_address="192.168.1.101",
                last_active=datetime.utcnow() - timedelta(days=1),
                created_at=datetime.utcnow() - timedelta(days=3),
                expires_at=datetime.utcnow() + timedelta(days=27),
                current=False
            )
        ]

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
