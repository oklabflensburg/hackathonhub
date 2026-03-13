/**
 * Firebase Cloud Messaging Service Worker
 * 
 * This service worker handles push notifications from Firebase FCM.
 * It receives messages and displays notifications to the user.
 */

// Import Firebase scripts (will be loaded from CDN)
importScripts('https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js')
importScripts('https://www.gstatic.com/firebasejs/10.8.0/firebase-messaging-compat.js')

// Firebase configuration (will be injected by the main app)
const firebaseConfig = {
  apiKey: 'AIzaSyD-example-key-1234567890',
  authDomain: 'hackathon-dashboard-dev.firebaseapp.com',
  projectId: 'hackathon-dashboard-dev',
  storageBucket: 'hackathon-dashboard-dev.appspot.com',
  messagingSenderId: '123456789012',
  appId: '1:123456789012:web:abcdef1234567890',
  measurementId: 'G-EXAMPLE123'
}

// Initialize Firebase
firebase.initializeApp(firebaseConfig)

// Initialize Firebase Cloud Messaging
const messaging = firebase.messaging()

/**
 * Handle background messages (when app is not in foreground).
 * This is called when a push notification is received while the app is closed
 * or in the background.
 */
messaging.onBackgroundMessage((payload) => {
  console.log('[firebase-messaging-sw.js] Received background message:', payload)
  
  const notificationTitle = payload.notification?.title || 'New Notification'
  const notificationOptions = {
    body: payload.notification?.body || 'You have a new notification',
    icon: payload.notification?.icon || '/icon-192x192.png',
    badge: '/badge-72x72.png',
    tag: payload.data?.tag || 'hackathon-notification',
    data: payload.data || {},
    actions: payload.data?.actions || [],
    requireInteraction: payload.data?.requireInteraction || false,
    silent: payload.data?.silent || false
  }

  // Show notification
  self.registration.showNotification(notificationTitle, notificationOptions)
  
  // Send analytics event if available
  if (payload.data?.analytics) {
    sendAnalyticsEvent('push_notification_received', {
      notification_id: payload.data.notification_id,
      type: payload.data.type,
      source: 'background'
    })
  }
})

/**
 * Handle notification click events.
 * When a user clicks on a notification, open the app to the relevant page.
 */
self.addEventListener('notificationclick', (event) => {
  console.log('[firebase-messaging-sw.js] Notification clicked:', event.notification)
  
  event.notification.close()

  const notificationData = event.notification.data || {}
  let urlToOpen = '/'
  
  // Determine URL based on notification data
  if (notificationData.url) {
    urlToOpen = notificationData.url
  } else if (notificationData.type === 'project_comment') {
    urlToOpen = `/projects/${notificationData.project_id}`
  } else if (notificationData.type === 'team_invitation') {
    urlToOpen = '/teams'
  } else if (notificationData.type === 'hackathon_started') {
    urlToOpen = `/hackathons/${notificationData.hackathon_id}`
  }

  // Open or focus the app
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((windowClients) => {
        // Check if there's already a window/tab open with the app
        for (const client of windowClients) {
          if (client.url.includes(self.location.origin) && 'focus' in client) {
            return client.focus()
          }
        }
        
        // If no window is open, open a new one
        if (clients.openWindow) {
          return clients.openWindow(urlToOpen)
        }
      })
  )

  // Send analytics event
  sendAnalyticsEvent('push_notification_clicked', {
    notification_id: notificationData.notification_id,
    type: notificationData.type,
    url: urlToOpen
  })
})

/**
 * Handle push subscription changes.
 */
self.addEventListener('pushsubscriptionchange', (event) => {
  console.log('[firebase-messaging-sw.js] Push subscription changed:', event)
  
  event.waitUntil(
    self.registration.pushManager.subscribe(event.oldSubscription.options)
      .then((newSubscription) => {
        // Send new subscription to server
        return fetch('/api/notifications/push-subscriptions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(newSubscription)
        })
      })
      .catch((error) => {
        console.error('Failed to update push subscription:', error)
      })
  )
})

/**
 * Send analytics event to server.
 */
function sendAnalyticsEvent(eventName, eventData) {
  try {
    // Send to backend analytics endpoint if available
    fetch('/api/analytics/events', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        event: eventName,
        data: eventData,
        timestamp: new Date().toISOString(),
        source: 'service_worker'
      })
    }).catch(() => {
      // Ignore errors for analytics
    })
  } catch (error) {
    // Ignore analytics errors
  }
}

/**
 * Handle service worker installation.
 */
self.addEventListener('install', (event) => {
  console.log('[firebase-messaging-sw.js] Service worker installed')
  self.skipWaiting() // Activate immediately
})

/**
 * Handle service worker activation.
 */
self.addEventListener('activate', (event) => {
  console.log('[firebase-messaging-sw.js] Service worker activated')
  event.waitUntil(clients.claim()) // Take control of all clients
})

/**
 * Handle messages from the main app.
 */
self.addEventListener('message', (event) => {
  console.log('[firebase-messaging-sw.js] Received message from app:', event.data)
  
  if (event.data && event.data.type === 'GET_FCM_TOKEN') {
    // Get FCM token and send back to app
    messaging.getToken({ vapidKey: event.data.vapidKey })
      .then((token) => {
        event.ports[0].postMessage({ token })
      })
      .catch((error) => {
        event.ports[0].postMessage({ error: error.message })
      })
  }
})

console.log('[firebase-messaging-sw.js] Service worker loaded successfully')