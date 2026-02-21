import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'
import { useUIStore } from './ui'

export interface UserNotification {
  id: number
  user_id: number
  notification_type: string
  title: string
  message: string
  data?: Record<string, any>
  channel: 'email' | 'push' | 'in_app'
  read: boolean
  read_at?: string
  created_at: string
  updated_at: string
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
  default_channels: string[]
  user_preferences: Record<'email' | 'push' | 'in_app', boolean>
}

export interface PushSubscription {
  id: number
  user_id: number
  endpoint: string
  keys: Record<string, string>
  created_at: string
  updated_at: string
}

export const useNotificationStore = defineStore('notification', () => {
  const authStore = useAuthStore()
  const uiStore = useUIStore()

  // State
  const notifications = ref<UserNotification[]>([])
  const unreadCount = ref(0)
  const notificationTypes = ref<NotificationType[]>([])
  const preferences = ref<Record<string, any>>({})
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
        notifications.value = data
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
        notificationTypes.value = data
      }
    } catch (error) {
      console.error('Failed to fetch notification types:', error)
    }
  }

  async function fetchPreferences() {
    if (!authStore.isAuthenticated) return

    try {
      const response = await authStore.authenticatedFetch('/api/notification-preferences')
      
      if (response.ok) {
        const data = await response.json()
        preferences.value = data
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
      const response = await authStore.authenticatedFetch(`/api/notification-preferences/${notificationType}/${channel}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ enabled })
      })

      if (response.ok) {
        // Update local state
        const type = notificationTypes.value.find(t => t.type_key === notificationType)
        if (type) {
          type.user_preferences[channel] = enabled
        }
        uiStore.showSuccess('Notification preference updated')
      }
    } catch (error) {
      console.error('Failed to update notification preference:', error)
      uiStore.showError('Failed to update notification preference')
    }
  }

  async function updatePreferences(newPreferences: Record<string, any>) {
    if (!authStore.isAuthenticated) return

    try {
      const response = await authStore.authenticatedFetch('/api/notification-preferences', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newPreferences)
      })

      if (response.ok) {
        preferences.value = newPreferences
        uiStore.showSuccess('Notification preferences updated')
      }
    } catch (error) {
      console.error('Failed to update notification preferences:', error)
      uiStore.showError('Failed to update notification preferences')
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
      const response = await authStore.authenticatedFetch('/api/push-subscriptions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          endpoint: subscription.endpoint,
          keys: subscription.keys
        })
      })

      if (response.ok) {
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
      const response = await authStore.authenticatedFetch(`/api/push-subscriptions/${encodeURIComponent(endpoint)}`, {
        method: 'DELETE'
      })

      if (response.ok) {
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
      const response = await authStore.authenticatedFetch('/api/push-subscriptions')
      
      if (response.ok) {
        const data = await response.json()
        pushSubscriptions.value = data
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
      .replace(/\-/g, '+')
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
    updatePreference,
    updatePreferences,
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