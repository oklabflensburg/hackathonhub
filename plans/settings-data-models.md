# Datenmodelle und Validierungsschemata für /settings Seite

## Übersicht
Dieses Dokument definiert die vollständigen Datenmodelle, TypeScript-Typen und Validierungsschemata für die /settings Seite.

## TypeScript Typen

### Haupt-Typen (`frontend3/app/types/settings-types.ts`)

```typescript
// Profile Settings
export interface ProfileSettings {
  username: string;
  email: string;
  name?: string;
  avatar_url?: string;
  bio?: string;
  location?: string;
  company?: string;
}

// Security Settings
export interface SecuritySettings {
  two_factor_enabled: boolean;
  active_sessions: UserSession[];
}

export interface UserSession {
  id: string;
  device: string;
  location?: string;
  ip_address?: string;
  last_active: string; // ISO date string
  created_at: string; // ISO date string
  expires_at?: string; // ISO date string
  current: boolean;
}

// Privacy Settings
export type VisibilityLevel = 'public' | 'friends_only' | 'private';
export type MessagePermission = 'all_users' | 'friends_only' | 'none';

export interface PrivacySettings {
  profile_visibility: VisibilityLevel;
  email_visibility: VisibilityLevel;
  show_online_status: boolean;
  allow_messages_from: MessagePermission;
  show_activity: boolean;
  allow_tagging: boolean;
  data_sharing: {
    analytics: boolean;
    marketing: boolean;
    third_parties: boolean;
  };
}

// Platform Preferences
export type ThemePreference = 'light' | 'dark' | 'system';
export type DateFormat = 'YYYY-MM-DD' | 'DD/MM/YYYY' | 'MM/DD/YYYY';
export type TimeFormat = '12h' | '24h';

export interface PlatformPreferences {
  theme: ThemePreference;
  language: string; // ISO language code
  timezone: string; // IANA timezone
  date_format: DateFormat;
  time_format: TimeFormat;
  notifications_sound: boolean;
  reduce_animations: boolean;
  compact_mode: boolean;
  default_view: {
    hackathons: 'grid' | 'list';
    projects: 'grid' | 'list';
    notifications: 'grouped' | 'chronological';
  };
}

// Notification Settings
export interface NotificationSettings {
  email_enabled: boolean;
  push_enabled: boolean;
  in_app_enabled: boolean;
  categories: NotificationCategories;
  quiet_hours?: {
    enabled: boolean;
    start: string; // "22:00"
    end: string;   // "08:00"
  };
}

export interface NotificationCategories {
  project_updates: boolean;
  team_invitations: boolean;
  hackathon_announcements: boolean;
  comment_replies: boolean;
  vote_notifications: boolean;
  mention_notifications: boolean;
  system_announcements: boolean;
  newsletter: boolean;
}

// OAuth Connections
export interface OAuthConnections {
  github?: OAuthConnection;
  google?: OAuthConnection;
  // Weitere Provider können hinzugefügt werden
}

export interface OAuthConnection {
  connected: boolean;
  username?: string;
  avatar_url?: string;
  email?: string;
  connected_at?: string; // ISO date string
  scopes?: string[];
}

// Data Management
export interface DataManagement {
  export_status?: {
    requested_at: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    download_url?: string;
    expires_at?: string;
  };
  deletion_status?: {
    requested_at: string;
    scheduled_for: string;
    status: 'pending' | 'scheduled' | 'cancelled';
  };
}

// Haupt-Settings Interface
export interface UserSettings {
  profile: ProfileSettings;
  security: SecuritySettings;
  privacy: PrivacySettings;
  platform: PlatformPreferences;
  notifications: NotificationSettings;
  connections: OAuthConnections;
  data: DataManagement;
}

// Update-Payloads
export type SettingsUpdate = Partial<UserSettings>;
export type ProfileSettingsUpdate = Partial<ProfileSettings>;
export type SecuritySettingsUpdate = Partial<SecuritySettings>;
export type PrivacySettingsUpdate = Partial<PrivacySettings>;
export type PlatformPreferencesUpdate = Partial<PlatformPreferences>;
export type NotificationSettingsUpdate = Partial<NotificationSettings>;

// API Responses
export interface SettingsResponse {
  settings: UserSettings;
  last_updated: string;
  version: string;
}

export interface ValidationError {
  field: string;
  message: string;
  code: string;
}

export interface SettingsValidationResult {
  valid: boolean;
  errors: ValidationError[];
}
```

## Backend Pydantic Schemas

### Haupt-Schemas (`backend/app/domain/schemas/settings.py`)

```python
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
    username: str = Field(..., min_length=3, max_length=50, regex=r'^[a-zA-Z0-9_]+$')
    email: EmailStr
    name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    bio: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, max_length=100)
    company: Optional[str] = Field(None, max_length=100)

    @validator('avatar_url')
    def validate_avatar_url(cls, v):
        if v and v.startswith('data:'):
            raise ValueError('Base64 data URLs are not allowed')
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
    data_sharing: DataSharingSettings = Field(default_factory=DataSharingSettings)

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
    default_view: DefaultViewSettings = Field(default_factory=DefaultViewSettings)

    @validator('language')
    def validate_language(cls, v):
        # Einfache Validierung für ISO language codes
        if len(v) not in [2, 5]:  # 'en' oder 'en-US'
            raise ValueError('Invalid language code')
        return v

    @validator('timezone')
    def validate_timezone(cls, v):
        # In der Praxis: pytz oder zoneinfo verwenden
        common_timezones = ['UTC', 'Europe/Berlin', 'America/New_York', 'Asia/Tokyo']
        if v not in common_timezones:
            # Log warning aber erlauben
            pass
        return v

# Notification Settings
class QuietHours(BaseModel):
    enabled: bool = False
    start: str = "22:00"  # HH:MM format
    end: str = "08:00"    # HH:MM format

    @validator('start', 'end')
    def validate_time_format(cls, v):
        from datetime import datetime
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
    categories: NotificationCategories = Field(default_factory=NotificationCategories)
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

# Haupt-Settings Schema
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

# Update-Schemas
class UserSettingsUpdate(BaseModel):
    profile: Optional[ProfileSettings] = None
    security: Optional[SecuritySettings] = None
    privacy: Optional[PrivacySettings] = None
    platform: Optional[PlatformPreferences] = None
    notifications: Optional[NotificationSettings] = None
    connections: Optional[OAuthConnections] = None
    data: Optional[DataManagement] = None

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
```

## Validierungsregeln

### Frontend-Validierung (Client-side)

```typescript
// frontend3/app/utils/settings-validation.ts
export const validateProfileSettings = (data: ProfileSettingsUpdate): ValidationError[] => {
  const errors: ValidationError[] = [];
  
  if (data.username !== undefined) {
    if (data.username.length < 3) {
      errors.push({
        field: 'username',
        message: 'Username must be at least 3 characters',
        code: 'TOO_SHORT'
      });
    }
    
    if (data.username.length > 50) {
      errors.push({
        field: 'username',
        message: 'Username must be at most 50 characters',
        code: 'TOO_LONG'
      });
    }
    
    if (!/^[a-zA-Z0-9_]+$/.test(data.username)) {
      errors.push({
        field: 'username',
        message: 'Username can only contain letters, numbers and underscores',
        code: 'INVALID_CHARACTERS'
      });
    }
  }
  
  if (data.email !== undefined) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.email)) {
      errors.push({
        field: 'email',
        message: 'Please enter a valid email address',
        code: 'INVALID_EMAIL'
      });
    }
  }
  
  if (data.bio !== undefined && data.bio.length > 500) {
    errors.push({
      field: 'bio',
      message: 'Bio must be at most 500 characters',
      code: 'TOO_LONG'
    });
  }
  
  return errors;
};

export const validatePasswordChange = (
  currentPassword: string,
  newPassword: string,
  confirmPassword: string
): ValidationError[] => {
  const errors: ValidationError[] = [];
  
  if (!currentPassword) {
    errors.push({
      field: 'currentPassword',
      message: 'Current password is required',
      code: 'REQUIRED'
    });
  }
  
  if (newPassword.length < 8) {
    errors.push({
      field: 'newPassword',
      message: 'Password must be at least 8 characters',
      code: 'TOO_SHORT'
    });
  }
  
  if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(newPassword)) {
    errors.push({
      field: 'newPassword',
      message: 'Password must contain uppercase, lowercase and numbers',
      code: 'WEAK_PASSWORD'
    });
  }
  
  if (newPassword !== confirmPassword) {
    errors.push({
      field: 'confirmPassword',
      message: 'Passwords do not match',
      code: 'MISMATCH'
    });
  }
  
  return errors;
};

export const validatePrivacySettings = (data: PrivacySettingsUpdate): ValidationError[] => {
  const errors: ValidationError[] = [];
  
  const validVisibility = ['public', 'friends_only', 'private'];
  const validMessagePermissions = ['all_users', 'friends_only', 'none'];
  
  if (data.profile_visibility && !validVisibility.includes(data.profile_visibility)) {
    errors.push({
      field: 'profile_visibility',
      message: 'Invalid visibility setting',
      code: 'INVALID_VALUE'
    });
  }
  
  if (data.allow_messages_from && !validMessagePermissions.includes(data.allow_messages_from)) {
    errors.push({
      field: 'allow_messages_from',
      message: 'Invalid message permission setting',
      code: 'INVALID_VALUE'
    });
  }
  
  return errors;
};
```

### Backend-Validierung (Server-side)

```python
# backend/app/services/settings_service.py
class SettingsService:
    def validate_settings_update(self, update: UserSettingsUpdate) -> SettingsValidationResult:
        """Komplette Validierung aller Einstellungsupdates"""
        errors = []
        
        if update.profile:
            errors.extend(self._validate_profile(update.profile))
        
        if update.security:
            errors.extend(self._validate_security(update.security))
        
        if update.privacy:
            errors.extend(self._validate_privacy(update.privacy))
        
        if update.platform:
            errors.extend(self._validate_platform(update.platform))
        
        if update.notifications:
            errors.extend(self._validate_notifications(update.notifications))
        
        return SettingsValidationResult(
            valid=len(errors) == 0,
            errors=errors
        )
    
    def _validate_profile(self, profile: ProfileSettings) -> List[ValidationError]:
        errors = []
        
        # Username uniqueness check (wenn geändert)
        if profile.username:
            existing_user = self._check_username_exists(profile.username)
            if existing_user and existing_user.id != current_user.id:
                errors.append(ValidationError(
                    field="username",
                    message="Username already taken",
                    code="USERNAME_EXISTS"
                ))
        
        # Email uniqueness check (wenn geändert)
        if profile.email:
            existing_user = self._check_email_exists(profile.email)
            if existing_user and existing_user.id != current_user.id:
                errors.append(ValidationError(
                    field="email",
                    message="Email already registered",
                    code="EMAIL_EXISTS"
                ))
        
        return errors
    
    def _validate_security(self, security: SecuritySettings) -> List[ValidationError]:
        # Sicherheitsvalidierung
        errors = []
        
        if security.two_factor_enabled and not current_user.email_verified:
            errors.append(ValidationError(
                field="two_factor_enabled",
                message="Email must be verified to enable two-factor authentication",
                code="EMAIL_NOT_VERIFIED"
            ))
        
        return errors
```

## Datenbank-Migration

### SQL Migration Script

```sql
-- Migration: Add user_settings columns to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS theme VARCHAR(20) DEFAULT 'system',
ADD COLUMN IF NOT EXISTS language VARCHAR(10) DEFAULT 'en',
ADD COLUMN IF NOT EXISTS timezone VARCHAR(50) DEFAULT 'UTC',
ADD COLUMN IF NOT EXISTS date_format VARCHAR(20) DEFAULT 'YYYY-MM-DD',
ADD COLUMN IF NOT EXISTS time_format VARCHAR(10