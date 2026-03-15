/**
 * Firebase composable for FCM push notifications.
 * 
 * This composable provides methods for:
 * - Initializing Firebase
 * - Requesting notification permission
 * - Getting FCM device token
 * - Subscribing/unsubscribing from topics
 * - Handling foreground/background messages
 */
import { ref, onMounted, onUnmounted } from 'vue'
import { getFirebaseConfig, isFirebaseConfigured } from '~/config/firebase.config'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

// Firebase types (we'll use dynamic imports to avoid bundle size issues)
interface FirebaseMessaging {
  getToken(options?: { vapidKey?: string }): Promise<string>
  onMessage(callback: (payload: any) => void): () => void
  onBackgroundMessage(callback: (payload: any) => void): () => void
  deleteToken(): Promise<boolean>
}

export function useFirebase() {
  const authStore = useAuthStore()
  const uiStore = useUIStore()

  // State
  const isInitialized = ref(false)
  const messaging = ref<FirebaseMessaging | null>(null)
  const fcmToken = ref<string | null>(null)
  const isSubscribed = ref(false)
  const error = ref<string | null>(null)

  // Check if Firebase is supported
  const isSupported = () => {
    if (typeof window === 'undefined') return false
    if (!isFirebaseConfigured()) return false
    return true
  }

  /**
   * Initialize Firebase app and messaging.
   * Uses CDN-based Firebase for service worker compatibility.
   */
  const initialize = async (): Promise<boolean> => {
    if (!isSupported()) {
      error.value = 'Firebase is not configured or not supported'
      return false
    }

    if (isInitialized.value) {
      return true
    }

    try {
      // Register service worker for Firebase Cloud Messaging
      await registerServiceWorker()

      // For web-based Firebase (using CDN), we don't need to initialize
      // the main Firebase app in the composable since the service worker
      // handles background messages.
      
      // Check if service worker is registered
      const registration = await navigator.serviceWorker.ready
      if (!registration) {
        error.value = 'Failed to register service worker'
        return false
      }

      isInitialized.value = true
      console.log('Firebase service worker initialized successfully')
      return true

    } catch (err) {
      error.value = `Failed to initialize Firebase: ${err}`
      console.error('Firebase initialization error:', err)
      return false
    }
  }

  /**
   * Register Firebase service worker.
   */
  const registerServiceWorker = async (): Promise<ServiceWorkerRegistration> => {
    if (!('serviceWorker' in navigator)) {
      throw new Error('Service workers are not supported in this browser')
    }

    try {
      // Register the Firebase messaging service worker
      const registration = await navigator.serviceWorker.register(
        '/firebase-messaging-sw.js',
        {
          scope: '/',
          type: 'classic'
        }
      )

      console.log('Firebase service worker registered:', registration)
      return registration

    } catch (err) {
      console.error('Failed to register service worker:', err)
      throw err
    }
  }

  /**
   * Request notification permission from the user.
   */
  const requestPermission = async (): Promise<boolean> => {
    if (!isInitialized.value || !messaging.value) {
      await initialize()
    }

    if (!messaging.value) {
      error.value = 'Firebase Messaging not initialized'
      return false
    }

    try {
      // Request permission using Notification API
      const permission = await Notification.requestPermission()
      
      if (permission === 'granted') {
        console.log('Notification permission granted')
        return true
      } else if (permission === 'denied') {
        error.value = 'Notification permission denied by user'
        console.warn('Notification permission denied')
        return false
      } else {
        error.value = 'Notification permission dismissed'
        console.warn('Notification permission dismissed')
        return false
      }
    } catch (err) {
      error.value = `Failed to request notification permission: ${err}`
      console.error('Permission request error:', err)
      return false
    }
  }

  /**
   * Get FCM device token for the current device.
   * Uses service worker to get token via CDN-based Firebase.
   */
  const getDeviceToken = async (): Promise<string | null> => {
    if (!isInitialized.value) {
      const initialized = await initialize()
      if (!initialized) return null
    }

    try {
      // Get VAPID key from config
      const { VAPID_PUBLIC_KEY } = await import('~/config/firebase.config')
      
      // Get service worker registration
      const registration = await navigator.serviceWorker.ready
      
      // Create a message channel to communicate with service worker
      const channel = new MessageChannel()
      
      return new Promise((resolve, reject) => {
        // Set up message handler
        channel.port1.onmessage = (event) => {
          if (event.data.token) {
            const token = event.data.token
            fcmToken.value = token
            isSubscribed.value = true
            console.log('FCM token obtained:', token.substring(0, 20) + '...')
            resolve(token)
          } else if (event.data.error) {
            error.value = `Failed to get device token: ${event.data.error}`
            console.error('Get token error:', event.data.error)
            reject(new Error(event.data.error))
          } else {
            error.value = 'Unknown error getting device token'
            reject(new Error('Unknown error'))
          }
        }
        
        // Send message to service worker to get FCM token
        registration.active?.postMessage(
          {
            type: 'GET_FCM_TOKEN',
            vapidKey: VAPID_PUBLIC_KEY
          },
          [channel.port2]
        )
        
        // Set timeout in case service worker doesn't respond
        setTimeout(() => {
          error.value = 'Timeout getting device token from service worker'
          reject(new Error('Timeout'))
        }, 10000)
      })

    } catch (err) {
      error.value = `Failed to get device token: ${err}`
      console.error('Get token error:', err)
      return null
    }
  }

  /**
   * Register device with backend for push notifications.
   */
  const registerDevice = async (): Promise<boolean> => {
    try {
      // Get device token
      const token = await getDeviceToken()
      if (!token) {
        return false
      }

      // Check if user is authenticated
      if (!authStore.isAuthenticated) {
        error.value = 'User must be authenticated to register device'
        return false
      }

      // Send token to backend
      const response = await authStore.fetchWithAuth('/api/notifications/push-subscriptions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          endpoint: token, // For FCM, token is the endpoint
          keys: {
            p256dh: 'fcm-token', // Placeholder for FCM
            auth: 'fcm-token'    // Placeholder for FCM
          },
          platform: getPlatform(),
          user_agent: navigator.userAgent
        })
      })

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      console.log('Device registered successfully:', data)
      
      uiStore.showSuccess(
        'Push Notifications Enabled',
        'You will now receive push notifications on this device.'
      )
      
      return true

    } catch (err) {
      error.value = `Failed to register device: ${err}`
      console.error('Device registration error:', err)
      uiStore.showError(
        'Failed to Enable Push Notifications',
        error.value || 'Unknown error'
      )
      return false
    }
  }

  /**
   * Unregister device from push notifications.
   */
  const unregisterDevice = async (): Promise<boolean> => {
    try {
      if (!fcmToken.value) {
        // No token to unregister
        return true
      }

      // Delete FCM token
      if (messaging.value) {
        await messaging.value.deleteToken()
      }

      // Notify backend to delete subscription
      if (authStore.isAuthenticated) {
        try {
          await authStore.fetchWithAuth(
            `/api/notifications/push-subscriptions/fcm/${fcmToken.value}`,
            { method: 'DELETE' }
          )
        } catch (err) {
          console.warn('Failed to delete subscription from backend:', err)
        }
      }

      fcmToken.value = null
      isSubscribed.value = false
      
      console.log('Device unregistered successfully')
      return true

    } catch (err) {
      error.value = `Failed to unregister device: ${err}`
      console.error('Device unregistration error:', err)
      return false
    }
  }

  /**
   * Subscribe to a Firebase topic.
   */
  const subscribeToTopic = async (topic: string): Promise<boolean> => {
    try {
      if (!fcmToken.value) {
        error.value = 'No device token available'
        return false
      }

      if (!authStore.isAuthenticated) {
        error.value = 'User must be authenticated to subscribe to topics'
        return false
      }

      const response = await authStore.fetchWithAuth(
        `/api/notifications/topics/${topic}/subscribe`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            device_tokens: [fcmToken.value]
          })
        }
      )

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`)
      }

      console.log(`Subscribed to topic: ${topic}`)
      return true

    } catch (err) {
      error.value = `Failed to subscribe to topic: ${err}`
      console.error('Topic subscription error:', err)
      return false
    }
  }

  /**
   * Unsubscribe from a Firebase topic.
   */
  const unsubscribeFromTopic = async (topic: string): Promise<boolean> => {
    try {
      if (!fcmToken.value) {
        error.value = 'No device token available'
        return false
      }

      if (!authStore.isAuthenticated) {
        error.value = 'User must be authenticated to unsubscribe from topics'
        return false
      }

      const response = await authStore.fetchWithAuth(
        `/api/notifications/topics/${topic}/unsubscribe`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            device_tokens: [fcmToken.value]
          })
        }
      )

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`)
      }

      console.log(`Unsubscribed from topic: ${topic}`)
      return true

    } catch (err) {
      error.value = `Failed to unsubscribe from topic: ${err}`
      console.error('Topic unsubscription error:', err)
      return false
    }
  }

  /**
   * Set up foreground message handler.
   * For CDN-based Firebase, foreground messages are handled by the service worker.
   * We can listen for messages from the service worker.
   */
  const setupForegroundHandler = (): (() => void) | null => {
    if (!isInitialized.value) {
      return null
    }

    try {
      // Listen for messages from service worker
      const messageHandler = (event: MessageEvent) => {
        if (event.data && event.data.type === 'FOREGROUND_MESSAGE') {
          const payload = event.data.payload
          console.log('Foreground message received via service worker:', payload)
          
          // Show notification to user
          if (payload.notification) {
            const { title, body } = payload.notification
            
            // Use browser notification API
            if ('Notification' in window && Notification.permission === 'granted') {
              new Notification(title, {
                body,
                icon: payload.notification.icon || '/icon-192x192.png'
              })
            }
            
            // Also show in-app notification
            uiStore.showNotification({
              title,
              message: body,
              type: 'info',
              duration: 5000
            })
          }
        }
      }

      // Add event listener
      navigator.serviceWorker.addEventListener('message', messageHandler)

      // Return cleanup function
      return () => {
        navigator.serviceWorker.removeEventListener('message', messageHandler)
      }
    } catch (err) {
      console.error('Failed to setup foreground handler:', err)
      return null
    }
  }

  /**
   * Get current platform (web, android, ios).
   */
  const getPlatform = (): string => {
    const userAgent = navigator.userAgent.toLowerCase()
    
    if (userAgent.includes('android')) {
      return 'android'
    } else if (
      userAgent.includes('iphone') || 
      userAgent.includes('ipad') || 
      userAgent.includes('ipod')
    ) {
      return 'ios'
    } else {
      return 'web'
    }
  }

  /**
   * Check if push notifications are enabled and registered.
   */
  const checkPushStatus = async (): Promise<{
    hasPermission: boolean
    isRegistered: boolean
    token: string | null
  }> => {
    const hasPermission = Notification.permission === 'granted'
    const token = fcmToken.value || await getDeviceToken()
    
    return {
      hasPermission,
      isRegistered: !!token,
      token
    }
  }

  /**
   * Enable push notifications (request permission + register device).
   */
  const enablePushNotifications = async (): Promise<boolean> => {
    // Request permission
    const hasPermission = await requestPermission()
    if (!hasPermission) {
      return false
    }

    // Register device
    const registered = await registerDevice()
    return registered
  }

  /**
   * Disable push notifications (unregister device).
   */
  const disablePushNotifications = async (): Promise<boolean> => {
    const disabled = await unregisterDevice()
    if (disabled) {
      uiStore.showSuccess(
        'Push Notifications Disabled',
        'You will no longer receive push notifications on this device.'
      )
    }
    return disabled
  }

  // Auto-initialize on mount if supported
  onMounted(async () => {
    if (isSupported()) {
      await initialize()
    }
  })

  // Cleanup on unmount
  onUnmounted(() => {
    // Note: Firebase doesn't need explicit cleanup, but we can reset state
    isInitialized.value = false
    messaging.value = null
  })

  return {
    // State
    isInitialized,
    fcmToken,
    isSubscribed,
    error,
    
    // Methods
    isSupported,
    initialize,
    requestPermission,
    getDeviceToken,
    registerDevice,
    unregisterDevice,
    subscribeToTopic,
    unsubscribeFromTopic,
    setupForegroundHandler,
    checkPushStatus,
    enablePushNotifications,
    disablePushNotifications,
    getPlatform
  }
}
