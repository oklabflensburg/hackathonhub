// Service Worker for Hackathon Dashboard Push Notifications

const CACHE_NAME = 'hackathon-dashboard-v1'
const urlsToCache = [
  '/',
  '/manifest.json',
  '/icon-192x192.png',
  '/icon-512x512.png',
  '/badge-72x72.png'
]

// Install event - cache static assets
self.addEventListener('install', event => {
  console.log('[Service Worker] Installing...')
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Caching app shell')
        return cache.addAll(urlsToCache)
      })
      .then(() => {
        console.log('[Service Worker] Install completed')
        return self.skipWaiting()
      })
  )
})

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('[Service Worker] Activating...')
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Deleting old cache:', cacheName)
            return caches.delete(cacheName)
          }
        })
      )
    }).then(() => {
      console.log('[Service Worker] Activation completed')
      return self.clients.claim()
    })
  )
})

// Fetch event - serve from cache or network
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return

  // Skip API requests
  if (event.request.url.includes('/api/')) return

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached response if found
        if (response) {
          return response
        }

        // Otherwise fetch from network
        return fetch(event.request).then(response => {
          // Don't cache if not a valid response
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response
          }

          // Clone the response
          const responseToCache = response.clone()

          // Cache the new response
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache)
            })

          return response
        })
      })
  )
})

// Push event - handle incoming push notifications
self.addEventListener('push', event => {
  console.log('[Service Worker] Push received:', event)

  let notificationData = {
    title: 'New Notification',
    body: 'You have a new notification',
    icon: '/icon-192x192.png',
    badge: '/badge-72x72.png',
    data: {},
    tag: 'hackathon-notification'
  }

  try {
    if (event.data) {
      const data = event.data.json()
      notificationData = {
        title: data.title || 'New Notification',
        body: data.body || 'You have a new notification',
        icon: data.icon || '/icon-192x192.png',
        badge: data.badge || '/badge-72x72.png',
        data: data.data || {},
        tag: data.tag || 'hackathon-notification'
      }
    }
  } catch (error) {
    console.error('[Service Worker] Failed to parse push data:', error)
  }

  const options = {
    body: notificationData.body,
    icon: notificationData.icon,
    badge: notificationData.badge,
    data: notificationData.data,
    tag: notificationData.tag,
    requireInteraction: false,
    actions: [
      {
        action: 'open',
        title: 'Open'
      },
      {
        action: 'dismiss',
        title: 'Dismiss'
      }
    ]
  }

  event.waitUntil(
    self.registration.showNotification(notificationData.title, options)
  )
})

// Notification click event - handle user interaction
self.addEventListener('notificationclick', event => {
  console.log('[Service Worker] Notification click:', event)

  event.notification.close()

  const notificationData = event.notification.data || {}
  let urlToOpen = '/notifications'

  // Determine URL based on notification data
  if (notificationData.project_id) {
    urlToOpen = `/projects/${notificationData.project_id}`
  } else if (notificationData.team_id) {
    urlToOpen = `/teams/${notificationData.team_id}`
  } else if (notificationData.hackathon_id) {
    urlToOpen = `/hackathons/${notificationData.hackathon_id}`
  } else if (notificationData.invitation_id) {
    urlToOpen = `/teams/${notificationData.team_id}/invitations`
  }

  // Handle action buttons
  if (event.action === 'open') {
    // Open the relevant page
    event.waitUntil(
      clients.matchAll({ type: 'window', includeUncontrolled: true })
        .then(windowClients => {
          // Check if there's already a window/tab open with the target URL
          for (const client of windowClients) {
            if (client.url.includes(urlToOpen) && 'focus' in client) {
              return client.focus()
            }
          }
          // If no matching window is found, open a new one
          if (clients.openWindow) {
            return clients.openWindow(urlToOpen)
          }
        })
    )
  } else if (event.action === 'dismiss') {
    // Notification was dismissed, do nothing
    console.log('[Service Worker] Notification dismissed')
  } else {
    // Default click behavior (no action button clicked)
    event.waitUntil(
      clients.matchAll({ type: 'window', includeUncontrolled: true })
        .then(windowClients => {
          // Check if there's already a window/tab open
          if (windowClients.length > 0) {
            const client = windowClients[0]
            if ('focus' in client) {
              return client.focus()
            }
          }
          // If no window is open, open the notifications page
          if (clients.openWindow) {
            return clients.openWindow(urlToOpen)
          }
        })
    )
  }
})

// Notification close event
self.addEventListener('notificationclose', event => {
  console.log('[Service Worker] Notification closed:', event)
})

// Push subscription change event
self.addEventListener('pushsubscriptionchange', event => {
  console.log('[Service Worker] Push subscription changed:', event)

  event.waitUntil(
    self.registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: event.oldSubscription ? 
        event.oldSubscription.options.applicationServerKey : null
    })
    .then(subscription => {
      // Send new subscription to server
      return fetch('/api/push-subscriptions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          endpoint: subscription.endpoint,
          keys: subscription.keys
        })
      })
    })
    .catch(error => {
      console.error('[Service Worker] Failed to renew push subscription:', error)
    })
  )
})

// Background sync for offline support
self.addEventListener('sync', event => {
  console.log('[Service Worker] Background sync:', event.tag)

  if (event.tag === 'sync-notifications') {
    event.waitUntil(
      syncNotifications()
    )
  }
})

async function syncNotifications() {
  try {
    // Get stored offline notifications
    const cache = await caches.open('offline-notifications')
    const requests = await cache.keys()
    
    for (const request of requests) {
      const response = await cache.match(request)
      if (response) {
        const notification = await response.json()
        
        // Try to send notification to server
        const result = await sendNotificationToServer(notification)
        
        if (result) {
          // Remove from cache if successful
          await cache.delete(request)
        }
      }
    }
  } catch (error) {
    console.error('[Service Worker] Failed to sync notifications:', error)
  }
}

async function sendNotificationToServer(notification) {
  try {
    const response = await fetch('/api/notifications/offline', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(notification)
    })
    
    return response.ok
  } catch (error) {
    console.error('[Service Worker] Failed to send notification to server:', error)
    return false
  }
}

// Message event - handle messages from the main thread
self.addEventListener('message', event => {
  console.log('[Service Worker] Message received:', event.data)

  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting()
  }
})