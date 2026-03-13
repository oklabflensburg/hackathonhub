/**
 * Notification TypeScript Types for Atomic Design Components
 * 
 * This file defines all TypeScript interfaces and enums for notification components
 * Used across atoms, molecules, organisms, templates, and composables
 */

// ==================== ENUMS ====================

/**
 * Notification type enum
 */
export enum NotificationType {
  SYSTEM = 'system',
  TEAM_INVITATION = 'team_invitation',
  TEAM_JOIN_REQUEST = 'team_join_request',
  TEAM_MEMBER_ADDED = 'team_member_added',
  TEAM_MEMBER_REMOVED = 'team_member_removed',
  TEAM_ROLE_UPDATED = 'team_role_updated',
  PROJECT_COMMENT = 'project_comment',
  PROJECT_VOTE = 'project_vote',
  PROJECT_SHARE = 'project_share',
  HACKATHON_REGISTRATION = 'hackathon_registration',
  HACKATHON_STARTING_SOON = 'hackathon_starting_soon',
  HACKATHON_COMPLETED = 'hackathon_completed',
  COMMENT_REPLY = 'comment_reply',
  COMMENT_VOTE = 'comment_vote',
  USER_FOLLOW = 'user_follow',
  USER_MENTION = 'user_mention',
  NEWSLETTER = 'newsletter',
  PASSWORD_RESET = 'password_reset',
  EMAIL_VERIFICATION = 'email_verification',
  TWO_FACTOR_AUTH = 'two_factor_auth'
}

/**
 * Notification status enum
 */
export enum NotificationStatus {
  UNREAD = 'unread',
  READ = 'read',
  ARCHIVED = 'archived',
  DELETED = 'deleted'
}

/**
 * Notification priority enum
 */
export enum NotificationPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

/**
 * Notification channel enum
 */
export enum NotificationChannel {
  IN_APP = 'in_app',
  EMAIL = 'email',
  PUSH = 'push',
  SMS = 'sms',
  ALL = 'all'
}

// ==================== INTERFACES ====================

/**
 * Base notification interface
 */
export interface Notification {
  id: string
  type: NotificationType
  title: string
  message: string
  status: NotificationStatus
  priority: NotificationPriority
  channels: NotificationChannel[]
  userId: string
  senderId: string | null
  senderName: string | null
  senderAvatarUrl: string | null
  entityType: 'project' | 'hackathon' | 'team' | 'user' | 'comment' | null
  entityId: string | null
  metadata: Record<string, any>
  actionUrl: string | null
  actionLabel: string | null
  expiresAt: string | null
  createdAt: string
  updatedAt: string
  readAt: string | null
  archivedAt: string | null
  deletedAt: string | null
}

/**
 * UI notification interface for toast-style notifications
 * Used by uiStore and GlobalNotifications component
 */
export interface UiNotification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number  // ms, optional (default 5000)
  action?: {
    label: string
    onClick: () => void
  }
  timestamp?: Date   // optional for future extensions
  read?: boolean     // optional for future extensions
}

/**
 * Notification creation data
 */
export interface NotificationCreateData {
  type: NotificationType
  title: string
  message: string
  userId: string
  priority?: NotificationPriority
  channels?: NotificationChannel[]
  senderId?: string | null
  senderName?: string | null
  senderAvatarUrl?: string | null
  entityType?: 'project' | 'hackathon' | 'team' | 'user' | 'comment' | null
  entityId?: string | null
  metadata?: Record<string, any>
  actionUrl?: string | null
  actionLabel?: string | null
  expiresAt?: string | null
}

/**
 * Notification update data
 */
export interface NotificationUpdateData {
  status?: NotificationStatus
  readAt?: string | null
  archivedAt?: string | null
  deletedAt?: string | null
}

/**
 * Notification filter options
 */
export interface NotificationFilterOptions {
  userId?: string
  type?: NotificationType[]
  status?: NotificationStatus[]
  priority?: NotificationPriority[]
  channel?: NotificationChannel[]
  entityType?: 'project' | 'hackathon' | 'team' | 'user' | 'comment' | null
  entityId?: string | null
  startDate?: string
  endDate?: string
  unreadOnly?: boolean
  page?: number
  pageSize?: number
  sortBy?: 'newest' | 'oldest' | 'priority'
}

/**
 * Notification pagination response
 */
export interface NotificationPaginationResponse {
  notifications: Notification[]
  totalCount: number
  page: number
  pageSize: number
  totalPages: number
  unreadCount: number
  hasMore: boolean
}

/**
 * Notification preferences
 */
export interface NotificationPreferences {
  userId: string
  channels: Record<NotificationType, NotificationChannel[]>
  emailEnabled: boolean
  pushEnabled: boolean
  inAppEnabled: boolean
  quietHours?: {
    enabled: boolean
    startTime: string
    endTime: string
    timezone: string
  }
  mutedTypes: NotificationType[]
  createdAt: string
  updatedAt: string
}

/**
 * Notification preferences update data
 */
export interface NotificationPreferencesUpdateData {
  channels?: Record<NotificationType, NotificationChannel[]>
  emailEnabled?: boolean
  pushEnabled?: boolean
  inAppEnabled?: boolean
  quietHours?: {
    enabled: boolean
    startTime: string
    endTime: string
    timezone: string
  } | null
  mutedTypes?: NotificationType[]
}

// ==================== COMPONENT PROPS ====================

/**
 * Notification item props
 */
export interface NotificationItemProps {
  notification: Notification
  showActions?: boolean
  showTimestamp?: boolean
  showSender?: boolean
  compact?: boolean
  onMarkAsRead?: (notificationId: string) => void
  onArchive?: (notificationId: string) => void
  onDelete?: (notificationId: string) => void
  onClick?: (notification: Notification) => void
}

/**
 * Notification list props
 */
export interface NotificationListProps {
  notifications: Notification[]
  loading?: boolean
  error?: string | null
  emptyMessage?: string
  showLoadMore?: boolean
  showFilters?: boolean
  currentUserId?: string | null
  onMarkAllAsRead?: () => void
  onArchiveAll?: () => void
  onDeleteAll?: () => void
  onLoadMore?: () => void
  onNotificationClick?: (notification: Notification) => void
  onNotificationAction?: (notificationId: string, action: string) => void
}

/**
 * Notification badge props
 */
export interface NotificationBadgeProps {
  count: number
  maxCount?: number
  showZero?: boolean
  size?: 'sm' | 'md' | 'lg'
  variant?: 'dot' | 'count' | 'both'
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left'
  color?: 'primary' | 'danger' | 'warning' | 'success' | 'info'
}

/**
 * Notification dropdown props
 */
export interface NotificationDropdownProps {
  notifications: Notification[]
  loading?: boolean
  error?: string | null
  maxItems?: number
  showBadge?: boolean
  showMarkAllAsRead?: boolean
  showEmptyState?: boolean
  onMarkAllAsRead?: () => void
  onNotificationClick?: (notification: Notification) => void
  onViewAll?: () => void
}

/**
 * Notification preferences form props
 */
export interface NotificationPreferencesFormProps {
  preferences: NotificationPreferences
  loading?: boolean
  saving?: boolean
  onSubmit: (data: NotificationPreferencesUpdateData) => Promise<void> | void
  onReset?: () => void
  disabled?: boolean
}

// ==================== COMPOSABLE RETURN TYPES ====================

/**
 * UseNotifications composable return type
 */
export interface UseNotificationsReturn {
  notifications: Ref<Notification[]>
  loading: Ref<boolean>
  error: Ref<string | null>
  totalCount: Ref<number>
  unreadCount: Ref<number>
  page: Ref<number>
  pageSize: Ref<number>
  filters: Ref<Partial<NotificationFilterOptions>>
  
  fetchNotifications: (options?: NotificationFilterOptions) => Promise<void>
  fetchNotification: (notificationId: string) => Promise<Notification | null>
  markAsRead: (notificationId: string) => Promise<boolean>
  markAllAsRead: () => Promise<boolean>
  archiveNotification: (notificationId: string) => Promise<boolean>
  deleteNotification: (notificationId: string) => Promise<boolean>
  createNotification: (data: NotificationCreateData) => Promise<Notification | null>
  resetNotifications: () => void
  refreshUnreadCount: () => Promise<void>
}

/**
 * UseNotificationPreferences composable return type
 */
export interface UseNotificationPreferencesReturn {
  preferences: Ref<NotificationPreferences | null>
  loading: Ref<boolean>
  error: Ref<string | null>
  saving: Ref<boolean>
  
  fetchPreferences: (userId: string) => Promise<void>
  updatePreferences: (data: NotificationPreferencesUpdateData) => Promise<boolean>
  resetPreferences: () => void
  getChannelPreferences: (type: NotificationType) => NotificationChannel[]
  isTypeMuted: (type: NotificationType) => boolean
}

// ==================== UTILITY TYPES ====================

/**
 * Notification filter panel props
 */
export interface NotificationFilterPanelProps {
  filters: Partial<NotificationFilterOptions>
  onChange: (filters: Partial<NotificationFilterOptions>) => void
  onReset?: () => void
  disabled?: boolean
}

/**
 * Notification empty state props
 */
export interface NotificationEmptyStateProps {
  title?: string
  message?: string
  icon?: string
  showAction?: boolean
  actionLabel?: string
  onAction?: () => void
}

// ==================== UTILITY CONSTANTS ====================

/**
 * Notification type labels
 */
export const NOTIFICATION_TYPE_LABELS: Record<NotificationType, string> = {
  [NotificationType.SYSTEM]: 'System',
  [NotificationType.TEAM_INVITATION]: 'Team-Einladung',
  [NotificationType.TEAM_JOIN_REQUEST]: 'Team-Beitrittsanfrage',
  [NotificationType.TEAM_MEMBER_ADDED]: 'Team-Mitglied hinzugefügt',
  [NotificationType.TEAM_MEMBER_REMOVED]: 'Team-Mitglied entfernt',
  [NotificationType.TEAM_ROLE_UPDATED]: 'Team-Rolle aktualisiert',
  [NotificationType.PROJECT_COMMENT]: 'Projekt-Kommentar',
  [NotificationType.PROJECT_VOTE]: 'Projekt-Vote',
  [NotificationType.PROJECT_SHARE]: 'Projekt-Geteilt',
  [NotificationType.HACKATHON_REGISTRATION]: 'Hackathon-Registrierung',
  [NotificationType.HACKATHON_STARTING_SOON]: 'Hackathon startet bald',
  [NotificationType.HACKATHON_COMPLETED]: 'Hackathon abgeschlossen',
  [NotificationType.COMMENT_REPLY]: 'Kommentar-Antwort',
  [NotificationType.COMMENT_VOTE]: 'Kommentar-Vote',
  [NotificationType.USER_FOLLOW]: 'Benutzer folgt dir',
  [NotificationType.USER_MENTION]: 'Erwähnung',
  [NotificationType.NEWSLETTER]: 'Newsletter',
  [NotificationType.PASSWORD_RESET]: 'Passwort zurücksetzen',
  [NotificationType.EMAIL_VERIFICATION]: 'E-Mail-Verifizierung',
  [NotificationType.TWO_FACTOR_AUTH]: 'Zwei-Faktor-Authentifizierung'
}

/**
 * Notification type icons
 */
export const NOTIFICATION_TYPE_ICONS: Record<NotificationType, string> = {
  [NotificationType.SYSTEM]: 'i-heroicons-cog',
  [NotificationType.TEAM_INVITATION]: 'i-heroicons-user-group',
  [NotificationType.TEAM_JOIN_REQUEST]: 'i-heroicons-user-plus',
  [NotificationType.TEAM_MEMBER_ADDED]: 'i-heroicons-user-add',
  [NotificationType.TEAM_MEMBER_REMOVED]: 'i-heroicons-user-remove',
  [NotificationType.TEAM_ROLE_UPDATED]: 'i-heroicons-badge',
  [NotificationType.PROJECT_COMMENT]: 'i-heroicons-chat-bubble-left',
  [NotificationType.PROJECT_VOTE]: 'i-heroicons-hand-thumb-up',
  [NotificationType.PROJECT_SHARE]: 'i-heroicons-share',
  [NotificationType.HACKATHON_REGISTRATION]: 'i-heroicons-calendar',
  [NotificationType.HACKATHON_STARTING_SOON]: 'i-heroicons-clock',
  [NotificationType.HACKATHON_COMPLETED]: 'i-heroicons-check-circle',
  [NotificationType.COMMENT_REPLY]: 'i-heroicons-chat-bubble-left-right',
  [NotificationType.COMMENT_VOTE]: 'i-heroicons-hand-thumb-up',
  [NotificationType.USER_FOLLOW]: 'i-heroicons-user',
  [NotificationType.USER_MENTION]: 'i-heroicons-at-symbol',
  [NotificationType.NEWSLETTER]: 'i-heroicons-envelope',
  [NotificationType.PASSWORD_RESET]: 'i-heroicons-key',
  [NotificationType.EMAIL_VERIFICATION]: 'i-heroicons-envelope-open',
  [NotificationType.TWO_FACTOR_AUTH]: 'i-heroicons-shield-check'
}

/**
 * Notification status labels
 */
export const NOTIFICATION_STATUS_LABELS: Record<NotificationStatus, string> = {
  [NotificationStatus.UNREAD]: 'Ungelesen',
  [NotificationStatus.READ]: 'Gelesen',
  [NotificationStatus.ARCHIVED]: 'Archiviert',
  [NotificationStatus.DELETED]: 'Gelöscht'
}

/**
 * Notification status colors
 */
export const NOTIFICATION_STATUS_COLORS: Record<NotificationStatus, string> = {
  [NotificationStatus.UNREAD]: 'blue',
  [NotificationStatus.READ]: 'gray',
  [NotificationStatus.ARCHIVED]: 'yellow',
  [NotificationStatus.DELETED]: 'red'
}

/**
 * Notification priority labels
 */
export const NOTIFICATION_PRIORITY_LABELS: Record<NotificationPriority, string> = {
  [NotificationPriority.LOW]: 'Niedrig',
  [NotificationPriority.MEDIUM]: 'Mittel',
  [NotificationPriority.HIGH]: 'Hoch',
  [NotificationPriority.CRITICAL]: 'Kritisch'
}

/**
 * Notification priority colors
 */
export const NOTIFICATION_PRIORITY_COLORS: Record<NotificationPriority, string> = {
  [NotificationPriority.LOW]: 'gray',
  [NotificationPriority.MEDIUM]: 'blue',
  [NotificationPriority.HIGH]: 'orange',
  [NotificationPriority.CRITICAL]: 'red'
}

/**
 * Notification channel labels
 */
export const NOTIFICATION_CHANNEL_LABELS: Record<NotificationChannel, string> = {
  [NotificationChannel.IN_APP]: 'In-App',
  [NotificationChannel.EMAIL]: 'E-Mail',
  [NotificationChannel.PUSH]: 'Push',
  [NotificationChannel.SMS]: 'SMS',
  [NotificationChannel.ALL]: 'Alle'
}