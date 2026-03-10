/**
 * TypeScript-Typen für Notification-Komponenten
 * Definiert alle Typen für Benachrichtigungs-bezogene Komponenten
 */

/**
 * Benachrichtigungstypen
 */
export enum NotificationType {
  SYSTEM = 'system',
  USER = 'user',
  PROJECT = 'project',
  TEAM = 'team',
  HACKATHON = 'hackathon',
  COMMENT = 'comment',
  VOTE = 'vote',
  INVITATION = 'invitation',
  ANNOUNCEMENT = 'announcement',
  REMINDER = 'reminder'
}

/**
 * Benachrichtigungsstatus
 */
export enum NotificationStatus {
  UNREAD = 'unread',
  READ = 'read',
  ARCHIVED = 'archived',
  DELETED = 'deleted'
}

/**
 * Benachrichtigungsaktion
 */
export interface NotificationAction {
  id: string
  label: string
  type: 'primary' | 'secondary' | 'danger' | 'success' | 'warning'
  url?: string
  onClick?: () => void
}

/**
 * Benachrichtigung
 */
export interface Notification {
  id: string
  type: NotificationType
  status: NotificationStatus
  title: string
  message: string
  icon?: string
  iconColor?: string
  avatarUrl?: string
  userId?: string
  userName?: string
  userAvatar?: string
  targetId?: string
  targetType?: string
  targetName?: string
  targetUrl?: string
  actions?: NotificationAction[]
  additionalContent?: string
  createdAt: string
  readAt?: string
  expiresAt?: string
  priority?: 'low' | 'medium' | 'high' | 'critical'
  metadata?: Record<string, any>
}

/**
 * Benachrichtigungsfilter
 */
export interface NotificationFilter {
  id: string
  label: string
  type?: NotificationType
  status?: NotificationStatus
  count?: number
}

/**
 * Benachrichtigungsfilter-Optionen
 */
export interface NotificationFilterOptions {
  type?: NotificationType[]
  status?: NotificationStatus[]
  priority?: ('low' | 'medium' | 'high' | 'critical')[]
  dateRange?: {
    start: string
    end: string
  }
  search?: string
  sortBy?: 'createdAt' | 'priority' | 'type'
  sortDirection?: 'asc' | 'desc'
}

/**
 * Benachrichtigungsfilter für UI-Komponenten
 */
export interface NotificationUIFilter {
  search?: string
  type?: NotificationType | 'all'
  status?: NotificationStatus | 'all'
  dateRange?: {
    from: string
    to: string
  }
}

/**
 * Sortierfelder für Benachrichtigungen
 */
export type NotificationSortField = 'createdAt' | 'priority' | 'type'

/**
 * Sortierrichtung für Benachrichtigungen
 */
export type NotificationSortDirection = 'asc' | 'desc'

/**
 * Benachrichtigungseinstellungen
 */
export interface NotificationSettings {
  email: {
    enabled: boolean
    frequency: 'instant' | 'daily' | 'weekly'
    types: NotificationType[]
  }
  push: {
    enabled: boolean
    types: NotificationType[]
  }
  inApp: {
    enabled: boolean
    sound: boolean
    desktop: boolean
    types: NotificationType[]
  }
  muteUntil?: string
  doNotDisturb?: {
    enabled: boolean
    startTime: string
    endTime: string
  }
}

/**
 * Benachrichtigungsstatistiken
 */
export interface NotificationStats {
  total: number
  unread: number
  read: number
  archived: number
  byType: Record<NotificationType, number>
  byPriority: Record<'low' | 'medium' | 'high' | 'critical', number>
  lastUpdated: string
}