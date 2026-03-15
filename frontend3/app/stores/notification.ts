import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'
import { useUIStore } from './ui'
import { useI18n } from 'vue-i18n'

export interface UserNotification {
  id: number
  user_id: number
  notification_type: string
  title: string
  message: string
  data?: Record<string, any>
  deliveries?: Array<{
    channel: 'email' | 'push' | 'in_app'
    status: string
  }>
  channels_sent?: string | null
  read: boolean
  read_at?: string
  created_at: string
  type?: string
  priority?: string | null
  action_url?: string | null
  metadata?: Record<string, any> | null
  expires_at?: string | null
}

export interface NotificationPreference {
  notification_type: string
  channel: 'email' | 'push' | 'in_app'
  enabled: boolean
}

export interface NotificationType {
  type_key: string
  category: string
  description: string
  help_text?: string
  default_channels: string[]
  user_preferences: Record<'email' | 'push' | 'in_app', boolean>
  enabled?: boolean
}

export interface NotificationSettingsResponse {
  global_enabled: boolean
  channels: Record<'email' | 'push' | 'in_app', boolean>
  categories: Record<string, {
    enabled: boolean
    channels: Record<'email' | 'push' | 'in_app', boolean>
    types: Record<string, {
      enabled: boolean
      channels: Record<'email' | 'push' | 'in_app', boolean>
      description?: string
      help_text?: string
      category?: string
      default_channels?: string[]
    }>
  }>
  types?: Record<string, {
    enabled: boolean
    channels: Record<'email' | 'push' | 'in_app', boolean>
    description?: string
    help_text?: string
    category?: string
    default_channels?: string[]
  }>
  masks?: {
    channels: string
    types: string
  }
  quiet_hours?: {
    enabled: boolean
    start: string
    end: string
    start_hour?: number
    end_hour?: number
    days: number[]
  }
}

export interface PushSubscription {
  id: number
  user_id: number
  endpoint: string
  p256dh: string
  auth: string
  user_agent?: string | null
  created_at: string
  updated_at: string
}

function normalizeNotification(raw: any): UserNotification {
  const metadata = raw.metadata ?? raw.data?.metadata ?? null
  const deliveries = Array.isArray(raw.deliveries) ? raw.deliveries : []
  return {
    id: Number(raw.id),
    user_id: Number(raw.user_id),
    notification_type: raw.notification_type ?? raw.type ?? 'system_announcement',
    title: raw.title ?? 'Notification',
    message: raw.message ?? '',
    data: raw.data ?? {},
    deliveries,
    channels_sent: raw.channels_sent ?? (deliveries.map((delivery: any) => delivery.channel).join(',') || null),
    read: Boolean(raw.read_at),
    read_at: raw.read_at ?? undefined,
    created_at: raw.created_at ?? new Date().toISOString(),
    type: raw.type ?? raw.notification_type,
    priority: raw.priority ?? raw.data?.priority ?? null,
    action_url: raw.action_url ?? raw.data?.action_url ?? null,
    metadata,
    expires_at: raw.expires_at ?? raw.data?.expires_at ?? null
  }
}

export const useNotificationStore = defineStore('notification', () => {
  const authStore = useAuthStore()
  const uiStore = useUIStore()
  const { t } = useI18n()

  // State
  const notifications = ref<UserNotification[]>([])
  const unreadCount = ref(0)
  const notificationTypes = ref<NotificationType[]>([])
  const preferences = ref<NotificationSettingsResponse>({
    global_enabled: false,
    channels: {
      email: true,
      push: true,
      in_app: true
    },
    categories: {},
    types: {},
    masks: {
      channels: '0',
      types: '0'
    },
    quiet_hours: {
      enabled: false,
      start: '22:00',
      end: '08:00',
      start_hour: 22,
      end_hour: 8,
      days: []
    }
  })
  const pushSubscriptions = ref<PushSubscription[]>([])
  const vapidPublicKey = ref<string | null>(null)
  const serviceWorkerRegistration = ref<ServiceWorkerRegistration | null>(null)
  const isPushSupported = ref(false)
  const isLoading = ref(false)

  // Computed
  const hasUnreadNotifications = computed(() => unreadCount.value > 0)
  const sortedNotifications = computed(() => 
    [...notifications.value].sort((a, b) => 
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )
  )
  const unreadNotifications = computed(() => 
    sortedNotifications.value.filter(n => !n.read)
  )
  const readNotifications = computed(() => 
    sortedNotifications.value.filter(n => n.read)
  )

  // Actions
  async function fetchNotifications(options?: { 
    skip?: number, 
    limit?: number, 
    unreadOnly?: boolean 
  }) {
    if (!authStore.isAuthenticated) return

    try {
      isLoading.value = true
      const params = new URLSearchParams()
      if (options?.skip) params.append('skip', options.skip.toString())
      if (options?.limit) params.append('limit', options.limit.toString())
      if (options?.unreadOnly) params.append('unread_only', 'true')

      const response = await authStore.authenticatedFetch(`/api/notifications?${params}`)
      
      if (response.ok) {
        const data = await response.json()
        notifications.value = Array.isArray(data) ? data.map(normalizeNotification) : []
        updateUnreadCount()
      }
    } catch (error) {
      console.error('Failed to fetch notifications:', error)
      uiStore.showError('Failed to load notifications')
    } finally {
      isLoading.value = false
    }
  }

  async function fetchUnreadCount() {
    if (!authStore.isAuthenticated) return

    try {
      const response = await authStore.authenticatedFetch('/api/notifications/unread-count')
      
      if (response.ok) {
        const data = await response.json()
        unreadCount.value = data.count
      }
    } catch (error) {
      console.error('Failed to fetch unread count:', error)
    }
  }

  async function markAsRead(notificationId: number) {
    if (!authStore.isAuthenticated) return

    try {
      const response = await authStore.authenticatedFetch(`/api/notifications/${notificationId}/read`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        // Update local state
        const notification = notifications.value.find(n => n.id === notificationId)
        if (notification) {
          notification.read = true
          notification.read_at = new Date().toISOString()
          updateUnreadCount()
        }
      }
    } catch (error) {
      console.error('Failed to mark notification as read:', error)
      uiStore.showError('Failed to mark notification as read')
    }
  }

  async function markAllAsRead() {
    if (!authStore.isAuthenticated) return

    try {
      const response = await authStore.authenticatedFetch('/api/notifications/read-all', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        // Update all notifications as read
        notifications.value.forEach(notification => {
          notification.read = true
          notification.read_at = new Date().toISOString()
        })
        unreadCount.value = 0
        uiStore.showSuccess('All notifications marked as read')
      }
    } catch (error) {
      console.error('Failed to mark all notifications as read:', error)
      uiStore.showError('Failed to mark all notifications as read')
    }
  }

  async function fetchNotificationTypes() {
    if (!authStore.isAuthenticated) return

    try {
      const response = await authStore.authenticatedFetch('/api/notification-types')
      
      if (response.ok) {
        const data = await response.json()
        notificationTypes.value = (Array.isArray(data) ? data : []).map((type: any) => ({
          ...type,
          default_channels: Array.isArray(type.default_channels)
            ? type.default_channels
            : String(type.default_channels || '')
                .split(',')
                .map((channel: string) => channel.trim())
                .filter(Boolean),
          user_preferences: type.user_preferences || { email: false, push: false, in_app: false },
          enabled: type.enabled ?? Object.values(type.user_preferences || {}).some(Boolean)
        }))
      }
    } catch (error) {
      console.error('Failed to fetch notification types:', error)
    }
  }

  async function fetchPreferences() {
    if (!authStore.isAuthenticated) return

    try {
      const response = await authStore.authenticatedFetch('/api/notifications/preferences')
      
      if (response.ok) {
        const data = await response.json()
        preferences.value = {
          ...data,
          quiet_hours: {
            enabled: Boolean(data?.quiet_hours?.enabled),
            start: data?.quiet_hours?.start || '22:00',
            end: data?.quiet_hours?.end || '08:00',
            start_hour: data?.quiet_hours?.start_hour ?? 22,
            end_hour: data?.quiet_hours?.end_hour ?? 8,
            days: Array.isArray(data?.quiet_hours?.days) ? data.quiet_hours.days : []
          }
        }
        notificationTypes.value = Object.entries(data.types || {}).map(([typeKey, typeData]: [string, any]) => ({
          type_key: typeKey,
          category: typeData.category || 'system',
          description: typeData.description || typeKey,
          help_text: typeData.help_text || '',
          default_channels: Array.isArray(typeData.default_channels) ? typeData.default_channels : [],
          user_preferences: typeData.channels || { email: false, push: false, in_app: false },
          enabled: Boolean(typeData.enabled)
        }))
      }
    } catch (error) {
      console.error('Failed to fetch notification preferences:', error)
    }
  }

  async function updatePreference(
    notificationType: string,
    channel: 'email' | 'push' | 'in_app',
    enabled: boolean
  ) {
    if (!authStore.isAuthenticated) return

    try {
      const response = await authStore.authenticatedFetch(`/api/notifications/preferences/${notificationType}/${channel}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ enabled })
      })

      if (response.ok) {
        const data = await response.json()
        preferences.value = data
        await fetchPreferences()
        uiStore.showSuccess('Notification preference updated')
      }
    } catch (error) {
      console.error('Failed to update notification preference:', error)
      uiStore.showError(t('errors.failedToUpdateNotificationPreference'))
    }
  }

  async function updatePreferences(newPreferences: Record<string, any>) {
    if (!authStore.isAuthenticated) return

    try {
      const response = await authStore.authenticatedFetch('/api/notifications/preferences', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newPreferences)
      })

      if (response.ok) {
        const data = await response.json()
        preferences.value = {
          ...preferences.value,
          ...data
        }
        await fetchPreferences()
        uiStore.showSuccess('Notification preferences updated')
      }
    } catch (error) {
      console.error('Failed to update notification preferences:', error)
      uiStore.showError(t('errors.failedToUpdateNotificationPreferences'))
    }
  }

  async function fetchQuietHours() {
    if (!authStore.isAuthenticated) return

    try {
      const response = await authStore.authenticatedFetch('/api/notifications/preferences/quiet-hours')

      if (response.ok) {
        const data = await response.json()
        preferences.value = {
          ...preferences.value,
          quiet_hours: {
            enabled: Boolean(data?.enabled),
            start: data?.start || '22:00',
            end: data?.end || '08:00',
            start_hour: data?.start_hour ?? 22,
            end_hour: data?.end_hour ?? 8,
            days: Array.isArray(data?.days) ? data.days : []
          }
        }
      }
    } catch (error) {
      console.error('Failed to fetch quiet hours:', error)
    }
  }

  async function updateQuietHours(quietHours: Record<string, any>) {
    if (!authStore.isAuthenticated) return

    try {
      const isToggleOnly = Object.keys(quietHours).length === 1 && typeof quietHours.enabled === 'boolean'
      const endpoint = isToggleOnly
        ? `/api/notifications/preferences/quiet-hours/${quietHours.enabled ? 'enable' : 'disable'}`
        : '/api/notifications/preferences/quiet-hours'
      const method = isToggleOnly ? 'POST' : 'PUT'
      const body = isToggleOnly && quietHours.enabled
        ? JSON.stringify({
            start_hour: preferences.value.quiet_hours?.start_hour ?? 22,
            end_hour: preferences.value.quiet_hours?.end_hour ?? 8,
            days: preferences.value.quiet_hours?.days ?? []
          })
        : isToggleOnly
          ? undefined
          : JSON.stringify(quietHours)

      const response = await authStore.authenticatedFetch(endpoint, {
        method,
        headers: {
          'Content-Type': 'application/json'
        },
        body
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(errorText || `Quiet hours update failed with ${response.status}`)
      }

      const data = await response.json()
      preferences.value = {
        ...preferences.value,
        quiet_hours: {
          enabled: Boolean(data?.enabled),
          start: data?.start || `${String(data?.start_hour ?? preferences.value.quiet_hours?.start_hour ?? 22).padStart(2, '0')}:00`,
          end: data?.end || `${String(data?.end_hour ?? preferences.value.quiet_hours?.end_hour ?? 8).padStart(2, '0')}:00`,
          start_hour: data?.start_hour ?? preferences.value.quiet_hours?.start_hour ?? 22,
          end_hour: data?.end_hour ?? preferences.value.quiet_hours?.end_hour ?? 8,
          days: Array.isArray(data?.days) ? data.days : []
        }
      }
      await fetchPreferences()
      uiStore.showSuccess(t('notificationSettings.settingsSaved'))
    } catch (error) {
      console.error('Failed to update quiet hours:', error)
      uiStore.showError(t('notificationSettings.saveError'))
      throw error
    }
  }

  // Push notification methods
  async function checkPushSupport() {
    isPushSupported.value = 'serviceWorker' in navigator && 'PushManager' in window
    return isPushSupported.value
  }

  async function getVapidPublicKey() {
    try {
      const response = await fetch('/api/push/vapid-public-key')
      if (response.ok) {
        const data = await response.json()
        vapidPublicKey.value = data.public_key
        return data.public_key
      } else {
        console.warn('VAPID public key not available')
        return null
      }
    } catch (error) {
      console.error('Failed to get VAPID public key:', error)
      return null
    }
  }

  async function registerServiceWorker() {
    if (!('serviceWorker' in navigator)) {
      console.warn('Service workers are not supported')
      return null
    }

    try {
      const registration = await navigator.serviceWorker.register('/sw.js')
      serviceWorkerRegistration.value = registration
      console.log('Service Worker registered:', registration)
      return registration
    } catch (error) {
      console.error('Service Worker registration failed:', error)
      return null
    }
  }

  async function subscribeToPushNotifications() {
    if (!authStore.isAuthenticated) {
      console.warn('Cannot subscribe to push notifications: not authenticated')
      return null
    }

    if (!serviceWorkerRegistration.value) {
      console.warn('Service worker not registered')
      return null
    }

    const publicKey = await getVapidPublicKey()
    if (!publicKey) {
      console.warn('VAPID public key not available')
      return null
    }

    try {
      const subscription = await serviceWorkerRegistration.value.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(publicKey)
      })

      // Send subscription to server
      await savePushSubscription(subscription)
      return subscription
    } catch (error) {
      console.error('Failed to subscribe to push notifications:', error)
      if (error instanceof Error && error.name === 'NotAllowedError') {
        uiStore.showError('Push notifications permission denied')
      }
      return null
    }
  }

  async function unsubscribeFromPushNotifications() {
    if (!serviceWorkerRegistration.value) return

    try {
      const subscription = await serviceWorkerRegistration.value.pushManager.getSubscription()
      if (subscription) {
        await subscription.unsubscribe()
        await deletePushSubscription(subscription.endpoint)
        uiStore.showSuccess('Push notifications disabled')
      }
    } catch (error) {
      console.error('Failed to unsubscribe from push notifications:', error)
      uiStore.showError('Failed to disable push notifications')
    }
  }

  async function savePushSubscription(subscription: PushSubscriptionJSON) {
    if (!authStore.isAuthenticated) return false

    try {
      const body = {
        endpoint: subscription.endpoint,
        p256dh: subscription.keys?.p256dh || '',
        auth: subscription.keys?.auth || '',
        user_agent: navigator.userAgent
      }
      const response = await authStore.authenticatedFetch('/api/notifications/push-subscriptions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      })

      if (response.ok) {
        await fetchPushSubscriptions()
        console.log('Push subscription saved to server')
        return true
      } else {
        console.error('Failed to save push subscription to server')
        return false
      }
    } catch (error) {
      console.error('Failed to save push subscription:', error)
      return false
    }
  }

  async function deletePushSubscription(endpoint: string) {
    if (!authStore.isAuthenticated) return false

    try {
      const existing = pushSubscriptions.value.find(sub => sub.endpoint === endpoint)
      if (!existing) return true
      const response = await authStore.authenticatedFetch(
        `/api/notifications/push-subscriptions/${existing.id}`,
        { method: 'DELETE' }
      )

      if (response.ok) {
        pushSubscriptions.value = pushSubscriptions.value.filter(sub => sub.id !== existing.id)
        console.log('Push subscription deleted from server')
        return true
      } else {
        console.error('Failed to delete push subscription from server')
        return false
      }
    } catch (error) {
      console.error('Failed to delete push subscription:', error)
      return false
    }
  }

  async function fetchPushSubscriptions() {
    if (!authStore.isAuthenticated) return

    try {
      const response = await authStore.authenticatedFetch('/api/notifications/push-subscriptions')
      
      if (response.ok) {
        const data = await response.json()
        pushSubscriptions.value = Array.isArray(data) ? data : []
      }
    } catch (error) {
      console.error('Failed to fetch push subscriptions:', error)
    }
  }

  async function requestPushPermission() {
    if (!isPushSupported.value) {
      uiStore.showError('Push notifications are not supported in this browser')
      return false
    }

    try {
      const permission = await Notification.requestPermission()
      if (permission === 'granted') {
        uiStore.showSuccess('Push notifications enabled')
        return true
      } else {
        uiStore.showError('Push notifications permission denied')
        return false
      }
    } catch (error) {
      console.error('Failed to request push permission:', error)
      uiStore.showError('Failed to request push permission')
      return false
    }
  }

  // Helper methods
  function updateUnreadCount() {
    unreadCount.value = notifications.value.filter(n => !n.read).length
  }

  function urlBase64ToUint8Array(base64String: string) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4)
    const base64 = (base64String + padding)
      .replace(/-/g, '+')
      .replace(/_/g, '/')

    const rawData = window.atob(base64)
    const outputArray = new Uint8Array(rawData.length)

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i)
    }
    return outputArray
  }

  function clearNotifications() {
    notifications.value = []
    unreadCount.value = 0
    preferences.value = {
      global_enabled: false,
      channels: { email: true, push: true, in_app: true },
      categories: {},
      types: {},
      masks: { channels: '0', types: '0' },
      quiet_hours: {
        enabled: false,
        start: '22:00',
        end: '08:00',
        start_hour: 22,
        end_hour: 8,
        days: []
      }
    }
  }

  // Initialize
  async function initialize() {
    if (authStore.isAuthenticated) {
      await Promise.all([
        fetchNotifications(),
        fetchUnreadCount(),
        fetchNotificationTypes(),
        fetchPreferences(),
        checkPushSupport()
      ])
    }
  }

  // Watch for authentication changes
  authStore.$subscribe(() => {
    if (authStore.isAuthenticated) {
      initialize()
    } else {
      clearNotifications()
    }
  })

  return {
    // State
    notifications,
    unreadCount,
    notificationTypes,
    preferences,
    pushSubscriptions,
    vapidPublicKey,
    serviceWorkerRegistration,
    isPushSupported,
    isLoading,

    // Computed
    hasUnreadNotifications,
    sortedNotifications,
    unreadNotifications,
    readNotifications,

    // Actions
    fetchNotifications,
    fetchUnreadCount,
    markAsRead,
    markAllAsRead,
    fetchNotificationTypes,
    fetchPreferences,
    fetchQuietHours,
    updatePreference,
    updatePreferences,
    updateQuietHours,
    checkPushSupport,
    getVapidPublicKey,
    registerServiceWorker,
    subscribeToPushNotifications,
    unsubscribeFromPushNotifications,
    savePushSubscription,
    deletePushSubscription,
    fetchPushSubscriptions,
    requestPushPermission,
    initialize,
    clearNotifications
  }
})
