/**
 * Settings-related TypeScript types and interfaces
 * Based on the comprehensive data models defined in the implementation plan
 */

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
export interface UserSession {
  id: string;
  device: string;
  device_name?: string;
  device_type?: 'desktop' | 'mobile' | 'tablet' | 'unknown';
  location?: string;
  ip_address?: string;
  last_active: string; // ISO date string
  last_activity?: string; // ISO date string - alias for last_active
  created_at: string; // ISO date string
  expires_at?: string; // ISO date string
  current: boolean;
  is_current?: boolean; // alias for current
}

export interface TrustedDevice {
  id: string;
  device: string;
  device_name?: string;
  device_type?: 'desktop' | 'mobile' | 'tablet' | 'unknown';
  location?: string;
  ip_address?: string;
  last_active: string;
  last_activity?: string;
  created_at: string;
  expires_at?: string;
  current: boolean;
  is_current?: boolean;
}

export interface SecuritySettings {
  two_factor_enabled: boolean;
  two_factor_last_enabled?: string; // ISO date string
  two_factor_last_used?: string; // ISO date string
  trusted_devices_count?: number;
  remaining_backup_codes?: number;
  active_sessions: UserSession[];
  trusted_devices: TrustedDevice[];
}

export interface OwnedResourceSummary {
  id: number;
  name: string;
  resource_type: 'hackathon' | 'team' | 'project';
}

export interface AccountImpactResponse {
  can_delete: boolean;
  can_deactivate: boolean;
  requires_transfer: boolean;
  hackathons: OwnedResourceSummary[];
  teams: OwnedResourceSummary[];
  projects: OwnedResourceSummary[];
  message?: string;
}

export interface AccountClosureRequest {
  password?: string;
  confirmation: string;
}

// Privacy Settings
export type VisibilityLevel = 'public' | 'friends_only' | 'private';
export type MessagePermission = 'all_users' | 'friends_only' | 'none';

export interface DataSharingSettings {
  analytics: boolean;
  marketing: boolean;
  third_parties: boolean;
}

export interface PrivacySettings {
  profile_visibility: VisibilityLevel;
  email_visibility: VisibilityLevel;
  show_online_status: boolean;
  allow_messages_from: MessagePermission;
  show_activity: boolean;
  allow_tagging: boolean;
  data_sharing: DataSharingSettings;
}

// Platform Preferences
export type ThemePreference = 'light' | 'dark' | 'system';
export type DateFormat = 'YYYY-MM-DD' | 'DD/MM/YYYY' | 'MM/DD/YYYY';
export type TimeFormat = '12h' | '24h';

export interface DefaultViewSettings {
  hackathons: 'grid' | 'list';
  projects: 'grid' | 'list';
  notifications: 'grouped' | 'chronological';
}

export interface PlatformPreferences {
  theme: ThemePreference;
  language: string; // ISO language code
  timezone: string; // IANA timezone
  date_format: DateFormat;
  time_format: TimeFormat;
  notifications_sound: boolean;
  reduce_animations: boolean;
  compact_mode: boolean;
  default_view: DefaultViewSettings;
}

// Notification Settings
export interface QuietHours {
  enabled: boolean;
  start: string; // "22:00"
  end: string;   // "08:00"
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

export interface NotificationSettings {
  email_enabled: boolean;
  push_enabled: boolean;
  in_app_enabled: boolean;
  categories: NotificationCategories;
  quiet_hours?: QuietHours;
}

// OAuth Connections
export interface OAuthConnection {
  connected: boolean;
  username?: string;
  avatar_url?: string;
  email?: string;
  connected_at?: string; // ISO date string
  scopes?: string[];
}

export interface OAuthConnections {
  github?: OAuthConnection;
  google?: OAuthConnection;
}

// Data Management
export interface ExportStatus {
  requested_at: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  download_url?: string;
  expires_at?: string;
}

export interface DeletionStatus {
  requested_at: string;
  scheduled_for: string;
  status: 'pending' | 'scheduled' | 'cancelled';
}

export interface DataManagement {
  export_status?: ExportStatus;
  deletion_status?: DeletionStatus;
}

// Main Settings Interface
export interface UserSettings {
  profile: ProfileSettings;
  security: SecuritySettings;
  privacy: PrivacySettings;
  platform: PlatformPreferences;
  notifications: NotificationSettings;
  connections: OAuthConnections;
  data: DataManagement;
}

// Update Payloads
export type SettingsUpdate = Partial<UserSettings>;
export type ProfileSettingsUpdate = Partial<ProfileSettings>;
export type SecuritySettingsUpdate = Partial<SecuritySettings>;
export type PrivacySettingsUpdate = Partial<PrivacySettings>;
export type PlatformPreferencesUpdate = Partial<PlatformPreferences>;
export type NotificationSettingsUpdate = Partial<NotificationSettings>;
export type OAuthConnectionsUpdate = Partial<OAuthConnections>;
export type DataManagementUpdate = Partial<DataManagement>;

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

// Tab Navigation
export interface SettingsTab {
  id: string;
  label: string;
  icon: string;
  description?: string;
  component?: string;
}

// Default values for initialization
export const DEFAULT_PROFILE_SETTINGS: ProfileSettings = {
  username: '',
  email: '',
  name: '',
  avatar_url: '',
  bio: '',
  location: '',
  company: ''
};

export const DEFAULT_SECURITY_SETTINGS: SecuritySettings = {
  two_factor_enabled: false,
  active_sessions: [],
  trusted_devices: []
};

export const DEFAULT_PRIVACY_SETTINGS: PrivacySettings = {
  profile_visibility: 'public',
  email_visibility: 'private',
  show_online_status: true,
  allow_messages_from: 'all_users',
  show_activity: true,
  allow_tagging: true,
  data_sharing: {
    analytics: true,
    marketing: false,
    third_parties: false
  }
};

export const DEFAULT_PLATFORM_PREFERENCES: PlatformPreferences = {
  theme: 'system',
  language: 'en',
  timezone: 'UTC',
  date_format: 'YYYY-MM-DD',
  time_format: '24h',
  notifications_sound: true,
  reduce_animations: false,
  compact_mode: false,
  default_view: {
    hackathons: 'grid',
    projects: 'grid',
    notifications: 'grouped'
  }
};

export const DEFAULT_NOTIFICATION_SETTINGS: NotificationSettings = {
  email_enabled: true,
  push_enabled: true,
  in_app_enabled: true,
  categories: {
    project_updates: true,
    team_invitations: true,
    hackathon_announcements: true,
    comment_replies: true,
    vote_notifications: true,
    mention_notifications: true,
    system_announcements: true,
    newsletter: false
  }
};

export const DEFAULT_OAUTH_CONNECTIONS: OAuthConnections = {
  github: undefined,
  google: undefined
};

export const DEFAULT_DATA_MANAGEMENT: DataManagement = {
  export_status: undefined,
  deletion_status: undefined
};

export const DEFAULT_USER_SETTINGS: UserSettings = {
  profile: DEFAULT_PROFILE_SETTINGS,
  security: DEFAULT_SECURITY_SETTINGS,
  privacy: DEFAULT_PRIVACY_SETTINGS,
  platform: DEFAULT_PLATFORM_PREFERENCES,
  notifications: DEFAULT_NOTIFICATION_SETTINGS,
  connections: DEFAULT_OAUTH_CONNECTIONS,
  data: DEFAULT_DATA_MANAGEMENT
};

// Tab definitions
export const SETTINGS_TABS: SettingsTab[] = [
  {
    id: 'profile',
    label: 'Profile',
    icon: 'user',
    description: 'Manage your personal information and profile settings'
  },
  {
    id: 'security',
    label: 'Security',
    icon: 'shield',
    description: 'Password, two-factor authentication, and session management'
  },
  {
    id: 'notifications',
    label: 'Notifications',
    icon: 'bell',
    description: 'Configure how and when you receive notifications'
  },
  {
    id: 'privacy',
    label: 'Privacy',
    icon: 'lock',
    description: 'Control your privacy settings and data sharing preferences'
  },
  {
    id: 'preferences',
    label: 'Preferences',
    icon: 'settings',
    description: 'Customize your platform experience and appearance'
  },
  {
    id: 'connections',
    label: 'Connections',
    icon: 'link',
    description: 'Manage connected accounts and OAuth integrations'
  },
  {
    id: 'data',
    label: 'Data',
    icon: 'database',
    description: 'Export your data or manage account deletion'
  }
];

// Helper functions
export function createEmptySettings(): UserSettings {
  return {
    profile: { ...DEFAULT_PROFILE_SETTINGS },
    security: { ...DEFAULT_SECURITY_SETTINGS },
    privacy: { ...DEFAULT_PRIVACY_SETTINGS },
    platform: { ...DEFAULT_PLATFORM_PREFERENCES },
    notifications: { ...DEFAULT_NOTIFICATION_SETTINGS },
    connections: { ...DEFAULT_OAUTH_CONNECTIONS },
    data: { ...DEFAULT_DATA_MANAGEMENT }
  };
}

export function mergeSettings(
  base: UserSettings,
  updates: SettingsUpdate
): UserSettings {
  return {
    profile: { ...base.profile, ...updates.profile },
    security: { ...base.security, ...updates.security },
    privacy: { ...base.privacy, ...updates.privacy },
    platform: { ...base.platform, ...updates.platform },
    notifications: { ...base.notifications, ...updates.notifications },
    connections: { ...base.connections, ...updates.connections },
    data: { ...base.data, ...updates.data }
  };
}

export function hasUnsavedChanges(
  original: UserSettings,
  current: UserSettings
): boolean {
  return JSON.stringify(original) !== JSON.stringify(current);
}

export function getChangedFields(
  original: UserSettings,
  current: UserSettings
): Record<string, any> {
  const changes: Record<string, any> = {};
  
  // Compare each section
  const sections: (keyof UserSettings)[] = [
    'profile', 'security', 'privacy', 'platform', 'notifications', 'connections', 'data'
  ];
  
  for (const section of sections) {
    const originalSection = original[section];
    const currentSection = current[section];
    
    if (JSON.stringify(originalSection) !== JSON.stringify(currentSection)) {
      changes[section] = currentSection;
    }
  }
  
  return changes;
}
