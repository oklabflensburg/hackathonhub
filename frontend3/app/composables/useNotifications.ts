import { ref, computed, watch } from 'vue'
import { 
  NotificationType, 
  NotificationStatus 
} from '~/types/notification-types'
import type { 
  Notification, 
  NotificationUIFilter,
  NotificationSortField,
  NotificationSortDirection
} from '~/types/notification-types'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

interface UseNotificationsOptions {
  userId?: string | number
  autoFetch?: boolean
  initialFilters?: Partial<NotificationUIFilter>
  pageSize?: number
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
  const filters = ref<NotificationUIFilter>({
    search: '',
    type: undefined,
    status: undefined,
    dateRange: undefined,
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
      if (filters.value.type && filters.value.type !== 'all') {
        if (notification.type !== filters.value.type) return false
      }
      
      // Status filter
      if (filters.value.status && filters.value.status !== 'all') {
        if (notification.status !== filters.value.status) return false
      }
      
      // Date range filter
      if (filters.value.dateRange?.from && filters.value.dateRange?.to) {
        const notificationDate = new Date(notification.createdAt)
        const fromDate = new Date(filters.value.dateRange.from)
        const toDate = new Date(filters.value.dateRange.to)
        
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
      if (filters.value.status === 'unread') {
        params.append('unread_only', 'true')
      }
      
      // Map type filter (notification_type in backend)
      if (filters.value.type && filters.value.type !== 'all') {
        params.append('notification_type', filters.value.type)
      }
      
      // Map search filter
      if (filters.value.search) {
        params.append('search', filters.value.search)
      }
      
      // Map date range filters
      if (filters.value.dateRange?.from) {
        params.append('date_from', filters.value.dateRange.from)
      }
      
      if (filters.value.dateRange?.to) {
        params.append('date_to', filters.value.dateRange.to)
      }
      
      // Map sort parameters
      if (sortField.value) {
        params.append('sort_field', sortField.value)
      }
      
      if (sortDirection.value) {
        params.append('sort_direction', sortDirection.value)
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
      
      // Check if notifications array exists
      if (!data.notifications || !Array.isArray(data.notifications)) {
        // Log to UI store for debugging
        uiStore.showWarning('API-Antwort-Struktur', 'Die API-Antwort hat keine notifications-Array. Es werden keine Benachrichtigungen angezeigt.')
        // Return empty array if no notifications
        notifications.value = [...notifications.value]
        total.value = 0
        hasMore.value = false
        page.value++
        return
      }
      
      // Transform API response to Notification interface
      const apiNotifications: Notification[] = data.notifications.map((apiNotif: any) => ({
        id: apiNotif.id.toString(),
        type: mapApiNotificationType(apiNotif.notification_type),
        status: apiNotif.read ? NotificationStatus.READ : NotificationStatus.UNREAD,
        title: apiNotif.title || 'Benachrichtigung',
        message: apiNotif.message || '',
        icon: getNotificationIcon(mapApiNotificationType(apiNotif.notification_type)),
        iconColor: getNotificationColor(mapApiNotificationType(apiNotif.notification_type)),
        userId: apiNotif.user_id?.toString() ?? (userId ? userId.toString() : undefined),
        userName: apiNotif.user?.username || 'Unbekannter Benutzer',
        userAvatar: apiNotif.user?.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${apiNotif.id}`,
        targetId: apiNotif.target_id?.toString(),
        targetType: apiNotif.target_type || 'general',
        targetName: apiNotif.target_name || 'Unbekannt',
        targetUrl: getActionUrlForApiNotification(apiNotif),
        createdAt: apiNotif.created_at || new Date().toISOString(),
        readAt: apiNotif.read_at || (apiNotif.read ? new Date().toISOString() : undefined),
        priority: mapApiPriority(apiNotif.priority),
        metadata: apiNotif.data || {}
      }))

      notifications.value = [...notifications.value, ...apiNotifications]
      total.value = data.total || data.notifications.length
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

  const updateFilters = (newFilters: Partial<NotificationUIFilter>) => {
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
      dateRange: undefined
    }
    fetchNotifications(true)
  }

  const getNotificationIcon = (type: NotificationType): string => {
    const icons: Record<NotificationType, string> = {
      [NotificationType.SYSTEM]: 'i-heroicons-cog',
      [NotificationType.USER]: 'i-heroicons-user',
      [NotificationType.PROJECT]: 'i-heroicons-document-text',
      [NotificationType.TEAM]: 'i-heroicons-user-group',
      [NotificationType.HACKATHON]: 'i-heroicons-calendar',
      [NotificationType.COMMENT]: 'i-heroicons-chat-bubble-left-right',
      [NotificationType.VOTE]: 'i-heroicons-hand-thumb-up',
      [NotificationType.INVITATION]: 'i-heroicons-envelope',
      [NotificationType.ANNOUNCEMENT]: 'i-heroicons-megaphone',
      [NotificationType.REMINDER]: 'i-heroicons-bell'
    }
    return icons[type] || 'i-heroicons-bell'
  }

  const getNotificationColor = (type: NotificationType): string => {
    const colors: Record<NotificationType, string> = {
      [NotificationType.SYSTEM]: 'gray',
      [NotificationType.USER]: 'blue',
      [NotificationType.PROJECT]: 'green',
      [NotificationType.TEAM]: 'purple',
      [NotificationType.HACKATHON]: 'orange',
      [NotificationType.COMMENT]: 'yellow',
      [NotificationType.VOTE]: 'indigo',
      [NotificationType.INVITATION]: 'pink',
      [NotificationType.ANNOUNCEMENT]: 'red',
      [NotificationType.REMINDER]: 'amber'
    }
    return colors[type] || 'gray'
  }



  // Helper functions for API data mapping
  const mapApiNotificationType = (apiType: string): NotificationType => {
    const typeMap: Record<string, NotificationType> = {
      'system': NotificationType.SYSTEM,
      'user': NotificationType.USER,
      'project': NotificationType.PROJECT,
      'team': NotificationType.TEAM,
      'hackathon': NotificationType.HACKATHON,
      'comment': NotificationType.COMMENT,
      'vote': NotificationType.VOTE,
      'invitation': NotificationType.INVITATION,
      'announcement': NotificationType.ANNOUNCEMENT,
      'reminder': NotificationType.REMINDER
    }
    return typeMap[apiType.toLowerCase()] || NotificationType.SYSTEM
  }

  const mapApiPriority = (apiPriority: string): 'low' | 'medium' | 'high' | 'critical' => {
    const priorityMap: Record<string, 'low' | 'medium' | 'high' | 'critical'> = {
      'low': 'low',
      'medium': 'medium',
      'high': 'high',
      'critical': 'critical',
      '1': 'low',
      '2': 'medium',
      '3': 'high',
      '4': 'critical'
    }
    return priorityMap[apiPriority?.toString().toLowerCase()] || 'low'
  }

  const getActionUrlForApiNotification = (apiNotif: any): string => {
    // Map API notification data to appropriate URLs
    if (apiNotif.target_url) return apiNotif.target_url
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
    getNotificationColor
  }
}

/**
 * Composable für die Verwaltung von Benachrichtigungs-Einstellungen
 */
export function useNotificationPreferences(userId?: string | number) {
  const preferences = ref<Record<NotificationType, boolean>>({
    [NotificationType.SYSTEM]: true,
    [NotificationType.USER]: true,
    [NotificationType.PROJECT]: true,
    [NotificationType.TEAM]: true,
    [NotificationType.HACKATHON]: true,
    [NotificationType.COMMENT]: true,
    [NotificationType.VOTE]: true,
    [NotificationType.INVITATION]: true,
    [NotificationType.ANNOUNCEMENT]: true,
    [NotificationType.REMINDER]: false
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
      
      if (data && data.preferences) {
        // Backend gibt ein Array von Präferenz-Objekten zurück
        // Wir müssen es in unser Map-Format konvertieren
        const updatedPreferences = { ...preferences.value }
        
        // Standardwerte mit API-Daten überschreiben
        data.preferences.forEach((pref: any) => {
          if (pref.notification_type in updatedPreferences) {
            updatedPreferences[pref.notification_type as NotificationType] = pref.enabled
          }
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