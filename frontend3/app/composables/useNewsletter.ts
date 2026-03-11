/**
 * Newsletter Composable
 * Bietet eine konsistente Schnittstelle für Newsletter-Abonnements
 */

import { ref, computed } from 'vue'
import { useApiClient } from '~/utils/api-client'
import { useUIStore } from '~/stores/ui'
import { usePreferencesStore } from '~/stores/preferences'

export interface NewsletterSubscription {
  email: string
  source?: string
  preferences?: {
    marketing?: boolean
    updates?: boolean
    events?: boolean
  }
}

export interface UseNewsletterOptions {
  /** Automatisches Error-Handling (Notifications) */
  autoErrorHandling?: boolean
  /** Automatisches Success-Handling (Notifications) */
  autoSuccessHandling?: boolean
  /** Standard-Quelle für Abonnements */
  defaultSource?: string
}

/**
 * Newsletter Composable
 */
export function useNewsletter(options: UseNewsletterOptions = {}) {
  const {
    autoErrorHandling = true,
    autoSuccessHandling = true,
    defaultSource = 'website'
  } = options

  // Stores
  const uiStore = useUIStore()
  const preferencesStore = usePreferencesStore()
  const apiClient = useApiClient()

  // State
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Computed Properties
  const subscribedEmails = computed(() => preferencesStore.newsletter.getSubscribedEmails())
  const isSubscribed = computed(() => (email: string) => subscribedEmails.value.includes(email))

  /**
   * Newsletter abonnieren
   */
  async function subscribe(email: string, source?: string, subscriptionPreferences?: NewsletterSubscription['preferences']): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      // Idempotency-Key generieren (verhindert doppelte Abonnements)
      const idempotencyKey = `newsletter-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`

      // API-Aufruf
      await apiClient.post('/api/newsletter/subscribe', {
        email,
        source: source || defaultSource,
        preferences: subscriptionPreferences
      }, {
        skipAuth: true,
        headers: {
          'Idempotency-Key': idempotencyKey
        },
        skipErrorNotification: true // Wir behandeln Errors selbst
      })

      // Lokalen State aktualisieren
      preferencesStore.newsletter.subscribe(email)

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Erfolgreich für den Newsletter angemeldet', 'Newsletter')
      }

    } catch (err: any) {
      error.value = err.message || 'Newsletter-Abonnement fehlgeschlagen'
      
      // Error Notification
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Newsletter Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Newsletter abbestellen
   */
  async function unsubscribe(email: string): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      // API-Aufruf
      await apiClient.post('/api/newsletter/unsubscribe', {
        email
      }, {
        skipAuth: true,
        skipErrorNotification: true
      })

      // Lokalen State aktualisieren
      preferencesStore.newsletter.unsubscribe(email)

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Newsletter-Abonnement erfolgreich beendet', 'Newsletter')
      }

    } catch (err: any) {
      error.value = err.message || 'Newsletter-Abbestellung fehlgeschlagen'
      
      // Error Notification
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Newsletter Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Abonnement-Status überprüfen
   */
  async function checkSubscription(email: string): Promise<boolean> {
    try {
      // Aktuell gibt es keinen API-Endpunkt zum Überprüfen des Status
      // Wir verwenden den lokalen State als Cache
      return isSubscribed.value(email)
    } catch (err: any) {
      console.error('Fehler beim Überprüfen des Newsletter-Abonnements:', err)
      return false
    }
  }

  /**
   * E-Mail-Validierung
   */
  function validateEmail(email: string): { isValid: boolean; message?: string } {
    if (!email || email.trim() === '') {
      return { isValid: false, message: 'E-Mail-Adresse ist erforderlich' }
    }

    // Einfache E-Mail-Validierung
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      return { isValid: false, message: 'Ungültige E-Mail-Adresse' }
    }

    return { isValid: true }
  }

  /**
   * Error zurücksetzen
   */
  function clearError(): void {
    error.value = null
  }

  /**
   * Loading-State zurücksetzen
   */
  function clearLoading(): void {
    isLoading.value = false
  }

  /**
   * Composable zurücksetzen
   */
  function reset(): void {
    isLoading.value = false
    error.value = null
  }

  return {
    // State
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    
    // Computed
    subscribedEmails,
    isSubscribed,
    
    // Methods
    subscribe,
    unsubscribe,
    checkSubscription,
    validateEmail,
    
    // Utilities
    clearError,
    clearLoading,
    reset
  }
}