import { ref, computed, watch } from 'vue'
import {
  NotificationType,
  NotificationStatus,
  NotificationPriority
} from '~/types/notification-types'
import type {
  Notification,
  NotificationFilterOptions,
  NotificationSortField,
  NotificationSortDirection
} from '~/types/notification-types'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

interface UseNotificationsOptions {
  userId?: string | number
  autoFetch?: boolean
  initialFilters?: Partial<NotificationFilterOptions>
  pageSize?: number
}

const mapApiNotificationType = (apiType: string): NotificationType => {
  const typeMap: Record<string, NotificationType> = {
    system: NotificationType.SYSTEM,
    system_announcement: NotificationType.SYSTEM,
    team: NotificationType.TEAM_INVITATION,
    team_invitation: NotificationType.TEAM_INVITATION,
    team_invitation_accepted: NotificationType.TEAM_MEMBER_ADDED,
    team_invitation_declined: NotificationType.TEAM_INVITATION,
    team_member_added: NotificationType.TEAM_MEMBER_ADDED,
    project: NotificationType.PROJECT_COMMENT,
    project_created: NotificationType.PROJECT_COMMENT,
    project_commented: NotificationType.PROJECT_COMMENT,
    hackathon: NotificationType.HACKATHON_REGISTRATION,
    hackathon_registered: NotificationType.HACKATHON_REGISTRATION,
    hackathon_started: NotificationType.HACKATHON_STARTING_SOON,
    hackathon_start_reminder: NotificationType.HACKATHON_STARTING_SOON,
    comment: NotificationType.COMMENT_REPLY,
    comment_reply: NotificationType.COMMENT_REPLY,
    vote_received: NotificationType.PROJECT_VOTE,
    security_alert: NotificationType.SYSTEM,
    verification_confirmed: NotificationType.EMAIL_VERIFICATION,
    password_reset_confirmed: NotificationType.PASSWORD_RESET,
    password_changed: NotificationType.PASSWORD_RESET,
    newsletter_unsubscribed: NotificationType.NEWSLETTER,
    security_login_new_device: NotificationType.TWO_FACTOR_AUTH,
    settings_changed: NotificationType.SYSTEM
  }
  return typeMap[apiType.toLowerCase()] || NotificationType.SYSTEM
}

const mapApiPriority = (apiPriority: string): NotificationPriority => {
  const priorityMap: Record<string, NotificationPriority> = {
    low: NotificationPriority.LOW,
    medium: NotificationPriority.MEDIUM,
    high: NotificationPriority.HIGH,
    critical: NotificationPriority.CRITICAL,
    '1': NotificationPriority.LOW,
    '2': NotificationPriority.MEDIUM,
    '3': NotificationPriority.HIGH,
    '4': NotificationPriority.CRITICAL
  }
  return priorityMap[apiPriority?.toString().toLowerCase()] || NotificationPriority.LOW
}

/**
 * Composable für die Verwaltung von Benachrichtigungen
 *
 * @example
 * ```typescript
 * const {
 *   notifications,
 *   loading,
 *   error,
 *   filters,
 *   unreadCount,
 *   fetchNotifications,
 *   markAsRead,
 *   markAllAsRead
 * } = useNotifications({ userId: 123 })
 * ```
 */
export function useNotifications(options: UseNotificationsOptions = {}) {
  const {
    userId,
    autoFetch = true,
    initialFilters = {},
    pageSize = 20
  } = options

  // Stores
  const authStore = useAuthStore()
  const uiStore = useUIStore()

  // State
  const notifications = ref<Notification[]>([])
  const loading = ref(false)
  const error = ref<Error | null>(null)
  const total = ref(0)
  const page = ref(1)
  const hasMore = ref(true)

  // Filters
  const filters = ref<NotificationFilterOptions>({
    search: '',
    type: undefined,
    status: undefined,
    sortBy: 'createdAt',
    sortDirection: 'desc',
    ...initialFilters
  })

  // Sort
  const sortField = ref<NotificationSortField>('createdAt')
  const sortDirection = ref<NotificationSortDirection>('desc')

  // Computed properties
  const unreadCount = computed(() => {
    return notifications.value.filter(n => n.status === NotificationStatus.UNREAD).length
  })

  const unreadNotifications = computed(() => {
    return notifications.value.filter(n => n.status === NotificationStatus.UNREAD)
  })

  const readNotifications = computed(() => {
    return notifications.value.filter(n => n.status === NotificationStatus.READ)
  })

  const sortedNotifications = computed(() => {
    const sorted = [...notifications.value]

    sorted.sort((a, b) => {
      let aValue: any, bValue: any

      switch (sortField.value) {
        case 'createdAt':
          aValue = new Date(a.createdAt).getTime()
          bValue = new Date(b.createdAt).getTime()
          break
        case 'priority':
          const priorityOrder = { low: 0, medium: 1, high: 2, critical: 3 }
          aValue = priorityOrder[a.priority || 'low'] || 0
          bValue = priorityOrder[b.priority || 'low'] || 0
          break
        case 'type':
          aValue = a.type
          bValue = b.type
          break
        default:
          aValue = 0
          bValue = 0
      }

      if (sortDirection.value === 'asc') {
        return aValue > bValue ? 1 : -1
      } else {
        return aValue < bValue ? 1 : -1
      }
    })

    return sorted
  })

  const filteredNotifications = computed(() => {
    return sortedNotifications.value.filter(notification => {
      // Search filter
      if (filters.value.search) {
        const searchLower = filters.value.search.toLowerCase()
        const matchesSearch =
          notification.title.toLowerCase().includes(searchLower) ||
          notification.message.toLowerCase().includes(searchLower) ||
          notification.userName?.toLowerCase().includes(searchLower) ||
          false

        if (!matchesSearch) return false
      }

      // Type filter
      if (filters.value.type) {
        if (!filters.value.type.includes(notification.type)) return false
      }

      // Status filter
      if (filters.value.status) {
        if (!filters.value.status.includes(notification.status)) return false
      }

      // Date range filter
      if (filters.value.startDate && filters.value.endDate) {
        const notificationDate = new Date(notification.createdAt)
        const fromDate = new Date(filters.value.startDate)
        const toDate = new Date(filters.value.endDate)

        if (notificationDate < fromDate || notificationDate > toDate) {
          return false
        }
      }

      return true
    })
  })

  const notificationTypes = computed(() => {
    const types = new Set<NotificationType>()
    notifications.value.forEach(n => types.add(n.type))
    return Array.from(types)
  })

  // Methods
  const normalizeApiNotification = (apiNotif: any): Notification => {
    const notificationType = mapApiNotificationType(apiNotif.notification_type || apiNotif.type || 'system')
    const metadata = apiNotif.metadata ?? apiNotif.data?.metadata ?? {}
    const payload = apiNotif.data ?? {}
    const channels = Array.isArray(apiNotif.deliveries)
      ? apiNotif.deliveries.map((delivery: any) => delivery.channel)
      : String(apiNotif.channels_sent || 'in_app')
          .split(',')
          .map((channel) => channel.trim())
          .filter(Boolean)

    return {
      id: String(apiNotif.id),
      type: notificationType,
      title: apiNotif.title || 'Benachrichtigung',
      message: apiNotif.message || '',
      status: apiNotif.read_at ? NotificationStatus.READ : NotificationStatus.UNREAD,
      priority: mapApiPriority(apiNotif.priority),
      channels: channels as any,
      userId: String(apiNotif.user_id ?? userId ?? ''),
      senderId: metadata.sender_id?.toString?.() || null,
      senderName: metadata.sender_name || metadata.inviter_name || null,
      senderAvatarUrl: metadata.sender_avatar_url || null,
      entityType: metadata.entity_type || null,
      entityId: metadata.entity_id?.toString?.() || null,
      metadata,
      actionUrl: apiNotif.action_url || payload.action_url || null,
      actionLabel: metadata.action_label || null,
      expiresAt: apiNotif.expires_at || payload.expires_at || null,
      createdAt: apiNotif.created_at || new Date().toISOString(),
      updatedAt: apiNotif.created_at || new Date().toISOString(),
      readAt: apiNotif.read_at || null,
      archivedAt: null,
      deletedAt: null,
      userName: metadata.sender_name || metadata.inviter_name || null,
      avatarUrl: metadata.sender_avatar_url || null,
      userAvatar: metadata.sender_avatar_url || null,
      timestamp: apiNotif.created_at || new Date().toISOString()
    }
  }

  const fetchNotifications = async (reset = false) => {
    const authStore = useAuthStore()

    if (reset) {
      page.value = 1
      notifications.value = []
      hasMore.value = true
    }

    if (!hasMore.value && !reset) return

    loading.value = true
    error.value = null

    try {
      // Build query parameters - map to backend API parameters
      const params = new URLSearchParams()

      // Map page/pageSize to skip/limit
      const skip = (page.value - 1) * pageSize
      params.append('skip', skip.toString())
      params.append('limit', pageSize.toString())

      // Map status filter to unread_only parameter
      if (filters.value.status?.includes(NotificationStatus.UNREAD)) {
        params.append('unread_only', 'true')
      }

      const response = await authStore.fetchWithAuth(`/api/notifications?${params.toString()}`)

      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()

      // Check if response has the expected structure
      if (!data || typeof data !== 'object') {
        throw new Error('Ungültige API-Antwort: Keine Daten erhalten')
      }

      // Handle authentication error
      if (data.detail === 'Not authenticated') {
        throw new Error('401: Nicht authentifiziert')
      }

      const rawNotifications = Array.isArray(data)
        ? data
        : Array.isArray(data.notifications)
          ? data.notifications
          : []

      const apiNotifications: Notification[] = rawNotifications.map(
        (apiNotif: any) => normalizeApiNotification(apiNotif)
      )

      notifications.value = [...notifications.value, ...apiNotifications]
      total.value = data.total || rawNotifications.length
      hasMore.value = page.value * pageSize < total.value
      page.value++
    } catch (err) {
      // Spezifische Fehlerbehandlung basierend auf Fehlertyp
      if (err instanceof Error && err.message.includes('401')) {
        const errorMsg = 'Nicht authentifiziert. Bitte melden Sie sich an, um Benachrichtigungen zu sehen.'
        error.value = new Error(errorMsg)
        uiStore.showError('Authentifizierungsfehler', errorMsg)
      } else if (err instanceof Error && err.message.includes('403')) {
        const errorMsg = 'Zugriff verweigert. Sie haben keine Berechtigung, Benachrichtigungen abzurufen.'
        error.value = new Error(errorMsg)
        uiStore.showError('Zugriffsfehler', errorMsg)
      } else if (err instanceof Error && err.message.includes('404')) {
        const errorMsg = 'API-Endpoint nicht gefunden. Bitte überprüfen Sie die Serverkonfiguration.'
        error.value = new Error(errorMsg)
        uiStore.showError('API-Fehler', errorMsg)
      } else if (err instanceof Error && err.message.includes('500')) {
        const errorMsg = 'Serverfehler. Bitte versuchen Sie es später erneut.'
        error.value = new Error(errorMsg)
        uiStore.showError('Serverfehler', errorMsg)
      } else {
        const errorMsg = err instanceof Error ? err.message : 'Fehler beim Abrufen der Benachrichtigungen'
        error.value = err instanceof Error ? err : new Error(errorMsg)
        uiStore.showError('Fehler beim Laden', errorMsg)
      }
    } finally {
      loading.value = false
    }
  }

  const loadMore = () => {
    if (!loading.value && hasMore.value) {
      fetchNotifications(false)
    }
  }

  const markAsRead = async (notificationId: string) => {
    try {
      const authStore = useAuthStore()

      // API-Aufruf mit fetchWithAuth
      const response = await authStore.fetchWithAuth(`/api/notifications/${notificationId}/read`, {
        method: 'POST'
      })

      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      // Lokales Update
      const notification = notifications.value.find(n => n.id === notificationId)
      if (notification) {
        notification.status = NotificationStatus.READ
        notification.readAt = new Date().toISOString()
      }

      return true
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unbekannter Fehler beim Markieren als gelesen'
      uiStore.showError('Fehler beim Markieren als gelesen', errorMsg)
      return false
    }
  }

  const markAllAsRead = async () => {
    try {
      const authStore = useAuthStore()

      // API-Aufruf mit fetchWithAuth - korrekter Endpoint: /api/notifications/read-all
      const response = await authStore.fetchWithAuth(`/api/notifications/read-all`, {
        method: 'POST'
      })

      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      // Lokales Update
      notifications.value.forEach(notification => {
        if (notification.status === NotificationStatus.UNREAD) {
          notification.status = NotificationStatus.READ
          notification.readAt = new Date().toISOString()
        }
      })

      return true
    } catch (err) {
      console.error('Fehler beim Markieren aller als gelesen:', err)
      return false
    }
  }

  const archive = async (notificationId: string) => {
    try {
      const authStore = useAuthStore()

      // API-Aufruf mit fetchWithAuth
      const response = await authStore.fetchWithAuth(`/api/notifications/${notificationId}/archive`, {
        method: 'POST'
      })

      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      // Lokales Update
      const notification = notifications.value.find(n => n.id === notificationId)
      if (notification) {
        notification.status = NotificationStatus.ARCHIVED
      }

      return true
    } catch (err) {
      console.error('Fehler beim Archivieren:', err)
      return false
    }
  }

  const deleteNotification = async (notificationId: string) => {
    try {
      const authStore = useAuthStore()

      // API-Aufruf mit fetchWithAuth
      const response = await authStore.fetchWithAuth(`/api/notifications/${notificationId}`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      // Lokales Update
      notifications.value = notifications.value.filter(n => n.id !== notificationId)
      total.value--

      return true
    } catch (err) {
      console.error('Fehler beim Löschen:', err)
      return false
    }
  }

  const updateFilters = (newFilters: Partial<NotificationFilterOptions>) => {
    filters.value = { ...filters.value, ...newFilters }
    fetchNotifications(true)
  }

  const updateSort = (field: NotificationSortField, direction: NotificationSortDirection) => {
    sortField.value = field
    sortDirection.value = direction
    fetchNotifications(true)
  }

  const resetFilters = () => {
    filters.value = {
      search: '',
      type: undefined,
      status: undefined,
      sortBy: 'createdAt',
      sortDirection: 'desc'
    }
    fetchNotifications(true)
  }

  const getNotificationIcon = (type: NotificationType): string => {
    const icons: Record<NotificationType, string> = {
      [NotificationType.SYSTEM]: 'i-heroicons-cog',
      [NotificationType.TEAM_JOIN_REQUEST]: 'i-heroicons-user-plus',
      [NotificationType.PROJECT_COMMENT]: 'i-heroicons-document-text',
      [NotificationType.TEAM_INVITATION]: 'i-heroicons-user-group',
      [NotificationType.TEAM_MEMBER_ADDED]: 'i-heroicons-user-plus',
      [NotificationType.TEAM_MEMBER_REMOVED]: 'i-heroicons-user-minus',
      [NotificationType.TEAM_ROLE_UPDATED]: 'i-heroicons-shield-check',
      [NotificationType.HACKATHON_REGISTRATION]: 'i-heroicons-calendar',
      [NotificationType.HACKATHON_STARTING_SOON]: 'i-heroicons-bell-alert',
      [NotificationType.HACKATHON_COMPLETED]: 'i-heroicons-flag',
      [NotificationType.COMMENT_REPLY]: 'i-heroicons-chat-bubble-left-right',
      [NotificationType.COMMENT_VOTE]: 'i-heroicons-hand-thumb-up',
      [NotificationType.PROJECT_VOTE]: 'i-heroicons-hand-thumb-up',
      [NotificationType.PROJECT_SHARE]: 'i-heroicons-share',
      [NotificationType.USER_FOLLOW]: 'i-heroicons-user-circle',
      [NotificationType.USER_MENTION]: 'i-heroicons-at-symbol',
      [NotificationType.EMAIL_VERIFICATION]: 'i-heroicons-envelope',
      [NotificationType.PASSWORD_RESET]: 'i-heroicons-key',
      [NotificationType.NEWSLETTER]: 'i-heroicons-megaphone',
      [NotificationType.TWO_FACTOR_AUTH]: 'i-heroicons-shield-check'
    }
    return icons[type] || 'i-heroicons-bell'
  }

  const getNotificationColor = (type: NotificationType): string => {
    const colors: Record<NotificationType, string> = {
      [NotificationType.SYSTEM]: 'gray',
      [NotificationType.TEAM_JOIN_REQUEST]: 'purple',
      [NotificationType.PROJECT_COMMENT]: 'green',
      [NotificationType.TEAM_INVITATION]: 'purple',
      [NotificationType.TEAM_MEMBER_ADDED]: 'purple',
      [NotificationType.TEAM_MEMBER_REMOVED]: 'red',
      [NotificationType.TEAM_ROLE_UPDATED]: 'blue',
      [NotificationType.HACKATHON_REGISTRATION]: 'orange',
      [NotificationType.HACKATHON_STARTING_SOON]: 'amber',
      [NotificationType.HACKATHON_COMPLETED]: 'emerald',
      [NotificationType.COMMENT_REPLY]: 'yellow',
      [NotificationType.COMMENT_VOTE]: 'indigo',
      [NotificationType.PROJECT_VOTE]: 'indigo',
      [NotificationType.PROJECT_SHARE]: 'sky',
      [NotificationType.USER_FOLLOW]: 'pink',
      [NotificationType.USER_MENTION]: 'pink',
      [NotificationType.EMAIL_VERIFICATION]: 'pink',
      [NotificationType.PASSWORD_RESET]: 'red',
      [NotificationType.NEWSLETTER]: 'red',
      [NotificationType.TWO_FACTOR_AUTH]: 'blue'
    }
    return colors[type] || 'gray'
  }
  const getActionUrlForApiNotification = (apiNotif: any): string => {
    // Map API notification data to appropriate URLs
    if (apiNotif.action_url) return apiNotif.action_url
    if (apiNotif.data?.action_url) return apiNotif.data.action_url
    if (apiNotif.data?.url) return apiNotif.data.url

    // Fallback to notifications page if no URL is provided
    return '/notifications'
  }

  // Auto-fetch wenn gewünscht
  if (autoFetch && userId !== undefined) {
    fetchNotifications(true)
  }

  // Watch filters for auto-refresh
  watch(filters, () => {
    if (autoFetch) {
      fetchNotifications(true)
    }
  }, { deep: true })

  // Enhanced In-App Notification Methods
  const createInAppNotification = async (notificationData: {
    title: string
    message: string
    type?: string
    priority?: string
    action_url?: string
    metadata?: Record<string, any>
    expires_at?: string
  }) => {
    try {
      const authStore = useAuthStore()

      const response = await authStore.fetchWithAuth('/api/notifications/in-app', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(notificationData)
      })

      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      uiStore.showSuccess('Benachrichtigung erstellt', 'Die Benachrichtigung wurde erfolgreich erstellt.')

      // Refresh notifications
      if (autoFetch) {
        fetchNotifications(true)
      }

      return {
        ...data,
        notifications: Array.isArray(data.notifications)
          ? data.notifications.map((notification: any) => normalizeApiNotification(notification))
          : []
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unbekannter Fehler beim Erstellen der Benachrichtigung'
      uiStore.showError('Fehler beim Erstellen der Benachrichtigung', errorMsg)
      return null
    }
  }

  const fetchInAppNotifications = async (options: {
    skip?: number
    limit?: number
    unread_only?: boolean
    include_expired?: boolean
  } = {}) => {
    try {
      const authStore = useAuthStore()

      const params = new URLSearchParams()
      if (options.skip !== undefined) params.append('skip', options.skip.toString())
      if (options.limit !== undefined) params.append('limit', options.limit.toString())
      if (options.unread_only !== undefined) params.append('unread_only', options.unread_only.toString())
      if (options.include_expired !== undefined) params.append('include_expired', options.include_expired.toString())

      const queryString = params.toString()
      const url = `/api/notifications/in-app/list${queryString ? `?${queryString}` : ''}`

      const response = await authStore.fetchWithAuth(url)

      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      return data
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unbekannter Fehler beim Abrufen der Benachrichtigungen'
      uiStore.showError('Fehler beim Abrufen der Benachrichtigungen', errorMsg)
      return { notifications: [], total: 0, skip: 0, limit: 0 }
    }
  }

  const getInAppUnreadCount = async () => {
    try {
      const authStore = useAuthStore()

      const response = await authStore.fetchWithAuth('/api/notifications/in-app/unread-count')

      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      return data.count || 0
    } catch (err) {
      console.error('Fehler beim Abrufen der ungelesenen Anzahl:', err)
      return 0
    }
  }

  const markInAppAsRead = async (notificationId: string) => {
    try {
      const authStore = useAuthStore()

      const response = await authStore.fetchWithAuth(`/api/notifications/in-app/${notificationId}/read`, {
        method: 'POST'
      })

      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      // Update local state
      const notification = notifications.value.find(n => n.id === notificationId)
      if (notification) {
        notification.status = NotificationStatus.READ
        notification.readAt = new Date().toISOString()
      }

      return true
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unbekannter Fehler beim Markieren als gelesen'
      uiStore.showError('Fehler beim Markieren als gelesen', errorMsg)
      return false
    }
  }

  const markAllInAppAsRead = async () => {
    try {
      const authStore = useAuthStore()

      const response = await authStore.fetchWithAuth('/api/notifications/in-app/mark-all-read', {
        method: 'POST'
      })

      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()

      // Update all local notifications
      notifications.value.forEach(notification => {
        if (notification.status === NotificationStatus.UNREAD) {
          notification.status = NotificationStatus.READ
          notification.readAt = new Date().toISOString()
        }
      })

      uiStore.showSuccess('Alle als gelesen markiert', data.message || `${data.count} Benachrichtigungen wurden als gelesen markiert.`)
      return data
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unbekannter Fehler beim Markieren aller als gelesen'
      uiStore.showError('Fehler beim Markieren aller als gelesen', errorMsg)
      return null
    }
  }

  const deleteInAppNotification = async (notificationId: string) => {
    try {
      const authStore = useAuthStore()

      const response = await authStore.fetchWithAuth(`/api/notifications/in-app/${notificationId}`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      // Remove from local state
      const index = notifications.value.findIndex(n => n.id === notificationId)
      if (index !== -1) {
        notifications.value.splice(index, 1)
      }

      uiStore.showSuccess('Benachrichtigung gelöscht', 'Die Benachrichtigung wurde erfolgreich gelöscht.')
      return true
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unbekannter Fehler beim Löschen der Benachrichtigung'
      uiStore.showError('Fehler beim Löschen der Benachrichtigung', errorMsg)
      return false
    }
  }

  const cleanupExpiredNotifications = async () => {
    try {
      const authStore = useAuthStore()

      const response = await authStore.fetchWithAuth('/api/notifications/in-app/cleanup', {
        method: 'POST'
      })

      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      uiStore.showSuccess('Bereinigung abgeschlossen', data.message || `${data.count} abgelaufene Benachrichtigungen wurden bereinigt.`)
      return data
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unbekannter Fehler bei der Bereinigung'
      uiStore.showError('Fehler bei der Bereinigung', errorMsg)
      return null
    }
  }

  return {
    // State
    notifications: filteredNotifications,
    loading,
    error,
    total,
    page,
    hasMore,

    // Filters & Sort
    filters,
    sortField,
    sortDirection,

    // Computed
    unreadCount,
    unreadNotifications,
    readNotifications,
    notificationTypes,

    // Methods
    fetchNotifications,
    loadMore,
    markAsRead,
    markAllAsRead,
    archive,
    deleteNotification,
    updateFilters,
    updateSort,
    resetFilters,
    getNotificationIcon,
    getNotificationColor,

    // Enhanced In-App Notification Methods
    createInAppNotification,
    fetchInAppNotifications,
    getInAppUnreadCount,
    markInAppAsRead,
    markAllInAppAsRead,
    deleteInAppNotification,
    cleanupExpiredNotifications
  }
}

/**
 * Composable für die Verwaltung von Benachrichtigungs-Einstellungen
 */
export function useNotificationPreferences(userId?: string | number) {
  const preferences = ref<Record<NotificationType, boolean>>({
    [NotificationType.SYSTEM]: true,
    [NotificationType.TEAM_INVITATION]: true,
    [NotificationType.TEAM_JOIN_REQUEST]: true,
    [NotificationType.TEAM_MEMBER_ADDED]: true,
    [NotificationType.TEAM_MEMBER_REMOVED]: true,
    [NotificationType.TEAM_ROLE_UPDATED]: true,
    [NotificationType.PROJECT_COMMENT]: true,
    [NotificationType.PROJECT_VOTE]: true,
    [NotificationType.PROJECT_SHARE]: true,
    [NotificationType.HACKATHON_REGISTRATION]: true,
    [NotificationType.HACKATHON_STARTING_SOON]: true,
    [NotificationType.HACKATHON_COMPLETED]: true,
    [NotificationType.COMMENT_REPLY]: true,
    [NotificationType.COMMENT_VOTE]: true,
    [NotificationType.USER_FOLLOW]: true,
    [NotificationType.USER_MENTION]: true,
    [NotificationType.NEWSLETTER]: true,
    [NotificationType.PASSWORD_RESET]: true,
    [NotificationType.EMAIL_VERIFICATION]: true,
    [NotificationType.TWO_FACTOR_AUTH]: true
  })

  const loading = ref(false)
  const error = ref<Error | null>(null)

  const fetchPreferences = async () => {
    if (userId === undefined) return

    loading.value = true
    error.value = null

    try {
      // API-Aufruf für Benachrichtigungspräferenzen
      const authStore = useAuthStore()
      const uiStore = useUIStore()
      const response = await authStore.fetchWithAuth('/api/notifications/preferences')

      // Response parsen
      const data = await response.json()

      if (data && data.categories) {
        const updatedPreferences = { ...preferences.value }

        Object.values<any>(data.categories).forEach((category) => {
          Object.entries<any>(category.types || {}).forEach(([typeKey, typeValue]) => {
            const mappedType = mapApiNotificationType(typeKey)
            updatedPreferences[mappedType] = Object.values(typeValue.channels || {}).some(Boolean)
          })
        })

        preferences.value = updatedPreferences
      }
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Laden der Einstellungen')
      const uiStore = useUIStore()
      uiStore.showError('Fehler beim Laden der Benachrichtigungs-Einstellungen')
    } finally {
      loading.value = false
    }
  }

  const updatePreference = async (type: NotificationType, enabled: boolean) => {
    if (userId === undefined) return false

    loading.value = true
    error.value = null

    try {
      // API-Aufruf für einzelne Präferenz
      const authStore = useAuthStore()
      const uiStore = useUIStore()
      await authStore.fetchWithAuth(`/api/notifications/preferences/${type}/email`, {
        method: 'POST',
        body: JSON.stringify({ enabled }),
        headers: {
          'Content-Type': 'application/json'
        }
      })

      preferences.value[type] = enabled
      uiStore.showSuccess('Benachrichtigungs-Einstellung aktualisiert')
      return true
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Aktualisieren der Einstellung')
      const uiStore = useUIStore()
      uiStore.showError('Fehler beim Aktualisieren der Benachrichtigungs-Einstellung')
      return false
    } finally {
      loading.value = false
    }
  }

  const updateAllPreferences = async (enabled: boolean) => {
    if (userId === undefined) return false

    loading.value = true
    error.value = null

    try {
      // Für alle Präferenztypen einzeln aktualisieren
      const preferenceTypes = Object.keys(preferences.value) as NotificationType[]
      const updatePromises = preferenceTypes.map(type =>
        updatePreference(type, enabled)
      )

      // Warten, bis alle Updates abgeschlossen sind
      const results = await Promise.all(updatePromises)
      const allSuccessful = results.every(result => result === true)

      if (allSuccessful) {
        const uiStore = useUIStore()
        uiStore.showSuccess('Alle Benachrichtigungs-Einstellungen aktualisiert')
        return true
      } else {
        const uiStore = useUIStore()
        uiStore.showWarning('Einige Einstellungen konnten nicht aktualisiert werden')
        return false
      }
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Aktualisieren aller Einstellungen')
      const uiStore = useUIStore()
      uiStore.showError('Fehler beim Aktualisieren aller Benachrichtigungs-Einstellungen')
      return false
    } finally {
      loading.value = false
    }
  }

  if (userId !== undefined) {
    fetchPreferences()
  }

  return {
    preferences,
    loading,
    error,
    fetchPreferences,
    updatePreference,
    updateAllPreferences
  }
}
