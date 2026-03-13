/**
 * Firebase configuration for the Hackathon Dashboard.
 * 
 * This file contains Firebase configuration for:
 * - Firebase Cloud Messaging (FCM) for push notifications
 * - Firebase Analytics (optional)
 * - Firebase Performance Monitoring (optional)
 */

export interface FirebaseConfig {
  apiKey: string
  authDomain: string
  projectId: string
  storageBucket: string
  messagingSenderId: string
  appId: string
  measurementId?: string
}

/**
 * Get Firebase configuration from environment variables.
 * 
 * Environment variables should be set in .env file:
 * - VITE_FIREBASE_API_KEY
 * - VITE_FIREBASE_AUTH_DOMAIN
 * - VITE_FIREBASE_PROJECT_ID
 * - VITE_FIREBASE_STORAGE_BUCKET
 * - VITE_FIREBASE_MESSAGING_SENDER_ID
 * - VITE_FIREBASE_APP_ID
 * - VITE_FIREBASE_MEASUREMENT_ID (optional)
 */
export function getFirebaseConfig(): FirebaseConfig | null {
  const apiKey = import.meta.env.VITE_FIREBASE_API_KEY
  const authDomain = import.meta.env.VITE_FIREBASE_AUTH_DOMAIN
  const projectId = import.meta.env.VITE_FIREBASE_PROJECT_ID
  const storageBucket = import.meta.env.VITE_FIREBASE_STORAGE_BUCKET
  const messagingSenderId = import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID
  const appId = import.meta.env.VITE_FIREBASE_APP_ID
  const measurementId = import.meta.env.VITE_FIREBASE_MEASUREMENT_ID

  // Check if all required config values are present
  if (!apiKey || !authDomain || !projectId || !storageBucket || 
      !messagingSenderId || !appId) {
    console.warn(
      'Firebase configuration is incomplete. ' +
      'FCM push notifications will not work.'
    )
    return null
  }

  return {
    apiKey,
    authDomain,
    projectId,
    storageBucket,
    messagingSenderId,
    appId,
    ...(measurementId && { measurementId })
  }
}

/**
 * Default Firebase configuration (for development).
 * Replace with your own Firebase project configuration.
 */
export const defaultFirebaseConfig: FirebaseConfig = {
  apiKey: 'AIzaSyD-example-key-1234567890',
  authDomain: 'hackathon-dashboard-dev.firebaseapp.com',
  projectId: 'hackathon-dashboard-dev',
  storageBucket: 'hackathon-dashboard-dev.appspot.com',
  messagingSenderId: '123456789012',
  appId: '1:123456789012:web:abcdef1234567890',
  measurementId: 'G-EXAMPLE123'
}

/**
 * VAPID public key for web push notifications.
 * This should match the VAPID_PUBLIC_KEY in the backend.
 */
export const VAPID_PUBLIC_KEY = import.meta.env.VITE_VAPID_PUBLIC_KEY || 
  'BEl62iUYgUivxIkv69yViEuiBIa-Ib9-SkvMeAtA3LFgDzkrxZJjSgSnfckjBJuBkr3qBUYIHBQFLXYp5Nksh8U'

/**
 * Check if Firebase is configured.
 */
export function isFirebaseConfigured(): boolean {
  const config = getFirebaseConfig()
  return config !== null
}

/**
 * Check if the current platform supports Firebase FCM.
 * Firebase FCM works on:
 * - Web browsers with Firebase JS SDK
 * - Android apps
 * - iOS apps
 */
export function isFcmSupported(): boolean {
  // Check if we're in a browser environment
  if (typeof window === 'undefined') {
    return false
  }

  // Check if Firebase is configured
  if (!isFirebaseConfigured()) {
    return false
  }

  // Check if we're on a mobile device (better FCM support)
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i
    .test(navigator.userAgent)

  // FCM works better on mobile devices but also works on desktop
  return true
}

/**
 * Get the appropriate push notification service to use.
 * Returns 'fcm' for mobile devices with Firebase config,
 * 'web-push' for desktop browsers with VAPID support,
 * or null if push notifications are not supported.
 */
export function getPreferredPushService(): 'fcm' | 'web-push' | null {
  // Check if we're in a browser
  if (typeof window === 'undefined' || typeof navigator === 'undefined') {
    return null
  }

  // Check for service worker support (required for both)
  if (!('serviceWorker' in navigator)) {
    return null
  }

  // Check for Firebase FCM support
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i
    .test(navigator.userAgent)

  if (isMobile && isFirebaseConfigured()) {
    return 'fcm'
  }

  // Check for Web Push API support
  if ('PushManager' in window && VAPID_PUBLIC_KEY) {
    return 'web-push'
  }

  return null
}