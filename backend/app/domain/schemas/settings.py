"""
Settings-related Pydantic schemas for the Hackathon Hub Platform.
"""
from __future__ import annotations

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum


# Enums
class VisibilityLevel(str, Enum):
    PUBLIC = "public"
    FRIENDS_ONLY = "friends_only"
    PRIVATE = "private"


class MessagePermission(str, Enum):
    ALL_USERS = "all_users"
    FRIENDS_ONLY = "friends_only"
    NONE = "none"


class ThemePreference(str, Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class DateFormat(str, Enum):
    YYYY_MM_DD = "YYYY-MM-DD"
    DD_MM_YYYY = "DD/MM/YYYY"
    MM_DD_YYYY = "MM/DD/YYYY"


class TimeFormat(str, Enum):
    HOUR_12 = "12h"
    HOUR_24 = "24h"


# Profile Settings
class ProfileSettings(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$'
    )
    email: EmailStr
    name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=2000)
    bio: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, max_length=100)
    company: Optional[str] = Field(None, max_length=100)

    @validator('avatar_url')
    def validate_avatar_url(cls, v):
        if v and v.startswith('data:'):
            raise ValueError(
                'Base64 data URLs are not allowed. '
                'Please upload the file via the upload endpoint.'
            )
        return v


# Security Settings
class UserSession(BaseModel):
    id: str
    device: str
    location: Optional[str] = None
    ip_address: Optional[str] = None
    last_active: datetime
    created_at: datetime
    expires_at: Optional[datetime] = None
    current: bool = False


class SecuritySettings(BaseModel):
    two_factor_enabled: bool = False
    active_sessions: List[UserSession] = []


# Privacy Settings
class DataSharingSettings(BaseModel):
    analytics: bool = True
    marketing: bool = False
    third_parties: bool = False


class PrivacySettings(BaseModel):
    profile_visibility: VisibilityLevel = VisibilityLevel.PUBLIC
    email_visibility: VisibilityLevel = VisibilityLevel.PRIVATE
    show_online_status: bool = True
    allow_messages_from: MessagePermission = MessagePermission.ALL_USERS
    show_activity: bool = True
    allow_tagging: bool = True
    data_sharing: DataSharingSettings = Field(
        default_factory=DataSharingSettings
    )


# Platform Preferences
class DefaultViewSettings(BaseModel):
    hackathons: Literal["grid", "list"] = "grid"
    projects: Literal["grid", "list"] = "grid"
    notifications: Literal["grouped", "chronological"] = "grouped"


class PlatformPreferences(BaseModel):
    theme: ThemePreference = ThemePreference.SYSTEM
    language: str = "en"
    timezone: str = "UTC"
    date_format: DateFormat = DateFormat.YYYY_MM_DD
    time_format: TimeFormat = TimeFormat.HOUR_24
    notifications_sound: bool = True
    reduce_animations: bool = False
    compact_mode: bool = False
    default_view: DefaultViewSettings = Field(
        default_factory=DefaultViewSettings
    )

    @validator('language')
    def validate_language(cls, v):
        # Simple validation for ISO language codes
        if len(v) not in [2, 5]:  # 'en' or 'en-US'
            raise ValueError(
                'Invalid language code format. '
                'Use ISO format like "en" or "en-US"'
            )
        return v

    @validator('timezone')
    def validate_timezone(cls, v):
        # In production, use pytz or zoneinfo for validation
        common_timezones = [
            'UTC', 'Europe/Berlin', 'America/New_York',
            'America/Los_Angeles', 'Asia/Tokyo',
            'Australia/Sydney', 'Europe/London'
        ]
        if v not in common_timezones:
            # Log warning but allow it
            pass
        return v


# Notification Settings
class QuietHours(BaseModel):
    enabled: bool = False
    start: str = "22:00"  # HH:MM format
    end: str = "08:00"    # HH:MM format

    @validator('start', 'end')
    def validate_time_format(cls, v):
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError('Time must be in HH:MM format')


class NotificationCategories(BaseModel):
    project_updates: bool = True
    team_invitations: bool = True
    hackathon_announcements: bool = True
    comment_replies: bool = True
    vote_notifications: bool = True
    mention_notifications: bool = True
    system_announcements: bool = True
    newsletter: bool = False


class NotificationSettings(BaseModel):
    email_enabled: bool = True
    push_enabled: bool = True
    in_app_enabled: bool = True
    categories: NotificationCategories = Field(
        default_factory=NotificationCategories
    )
    quiet_hours: Optional[QuietHours] = None


# OAuth Connections
class OAuthConnection(BaseModel):
    connected: bool = False
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    email: Optional[str] = None
    connected_at: Optional[datetime] = None
    scopes: List[str] = []


class OAuthConnections(BaseModel):
    github: Optional[OAuthConnection] = None
    google: Optional[OAuthConnection] = None


# Data Management
class ExportStatus(BaseModel):
    requested_at: datetime
    status: Literal["pending", "processing", "completed", "failed"]
    download_url: Optional[str] = None
    expires_at: Optional[datetime] = None


class DeletionStatus(BaseModel):
    requested_at: datetime
    scheduled_for: datetime
    status: Literal["pending", "scheduled", "cancelled"]


class DataManagement(BaseModel):
    export_status: Optional[ExportStatus] = None
    deletion_status: Optional[DeletionStatus] = None


# Main Settings Schema
class UserSettings(BaseModel):
    profile: ProfileSettings
    security: SecuritySettings
    privacy: PrivacySettings
    platform: PlatformPreferences
    notifications: NotificationSettings
    connections: OAuthConnections
    data: DataManagement

    class Config:
        from_attributes = True


# Update Schemas
class UserSettingsUpdate(BaseModel):
    profile: Optional[ProfileSettings] = None
    security: Optional[SecuritySettings] = None
    privacy: Optional[PrivacySettings] = None
    platform: Optional[PlatformPreferences] = None
    notifications: Optional[NotificationSettings] = None
    connections: Optional[OAuthConnections] = None
    data: Optional[DataManagement] = None


# Backwards-compatible alias used by API routes
class SettingsUpdateRequest(UserSettingsUpdate):
    pass


# API Request/Response Schemas
class SettingsResponse(BaseModel):
    settings: UserSettings
    last_updated: datetime
    version: str = "1.0.0"


class ValidationError(BaseModel):
    field: str
    message: str
    code: str


class SettingsValidationResult(BaseModel):
    valid: bool
    errors: List[ValidationError] = []


# Password Change Schema
class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str

    @validator('new_password')
    def validate_password_strength(cls, v):
        # At least one uppercase, one lowercase, one digit
        if not any(c.isupper() for c in v):
            raise ValueError(
                'Password must contain at least one uppercase letter'
            )
        if not any(c.islower() for c in v):
            raise ValueError(
                'Password must contain at least one lowercase letter'
            )
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


# Two-Factor Authentication Schemas
class TwoFactorSetupResponse(BaseModel):
    qr_code: str  # Base64 encoded QR code
    secret: str   # TOTP secret
    backup_codes: List[str]


class TwoFactorVerifyRequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=6, pattern=r'^\d+$')


class TwoFactorDisableRequest(BaseModel):
    password: str


# Two-Factor Authentication Login Schemas
class TwoFactorLoginVerifyRequest(BaseModel):
    """Request for verifying 2FA code during login"""
    code: str = Field(..., min_length=6, max_length=6, pattern=r'^\d+$')
    temp_token: str = Field(
        ..., description="Temporary token from initial login"
    )
    remember_device: bool = Field(
        default=False, description="Remember this device for 30 days"
    )


class TwoFactorBackupVerifyRequest(BaseModel):
    """Request for verifying backup code during login"""
    backup_code: str = Field(
        ..., min_length=8, max_length=12, pattern=r'^[A-Z0-9]+$'
    )
    temp_token: str = Field(
        ..., description="Temporary token from initial login"
    )


class TwoFactorLoginResponse(BaseModel):
    """Response for successful 2FA verification"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    requires_2fa: bool = False


# Session Management
class SessionRevokeRequest(BaseModel):
    session_id: Optional[str] = None  # If None, revoke all other sessions


# Data Export/Deletion
class DataExportRequest(BaseModel):
    format: Literal["json", "csv"] = "json"
    include: List[str] = Field(
        default_factory=lambda: ["profile", "projects", "teams"]
    )


class AccountDeletionRequest(BaseModel):
    password: str
    confirmation: str = Field(..., pattern=r'^DELETE MY ACCOUNT$')


# Helper functions
def create_default_settings() -> UserSettings:
    """Create default settings for a new user."""
    return UserSettings(
        profile=ProfileSettings(
            username="",
            email=""
        ),
        security=SecuritySettings(),
        privacy=PrivacySettings(),
        platform=PlatformPreferences(),
        notifications=NotificationSettings(),
        connections=OAuthConnections(),
        data=DataManagement()
    )
