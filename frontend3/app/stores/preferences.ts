import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from './auth'

// SSR-safe localStorage wrapper
class SSRStorage {
  private isClient = typeof window !== 'undefined'

  getItem<T>(key: string, defaultValue: T | null = null): T | null {
    if (!this.isClient) return defaultValue
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : defaultValue
    } catch (error) {
      console.error(`[Preferences] Failed to get item "${key}":`, error)
      return defaultValue
    }
  }

  setItem<T>(key: string, value: T): void {
    if (!this.isClient) return
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error(`[Preferences] Failed to set item "${key}":`, error)
    }
  }

  removeItem(key: string): void {
    if (!this.isClient) return
    try {
      localStorage.removeItem(key)
    } catch (error) {
      console.error(`[Preferences] Failed to remove item "${key}":`, error)
    }
  }

  clear(): void {
    if (!this.isClient) return
    try {
      localStorage.clear()
    } catch (error) {
      console.error('[Preferences] Failed to clear storage:', error)
    }
  }
}

export const usePreferencesStore = defineStore('preferences', () => {
  const storage = new SSRStorage()

  // Auth module
  const auth = {
    // Keys
    AUTH_TOKEN_KEY: 'auth_token',
    REFRESH_TOKEN_KEY: 'refresh_token',
    USER_KEY: 'user',

    // Getters
    get tokens() {
      return {
        access: storage.getItem<string>(this.AUTH_TOKEN_KEY),
        refresh: storage.getItem<string>(this.REFRESH_TOKEN_KEY),
      }
    },

    get user(): User | null {
      return storage.getItem<User>(this.USER_KEY)
    },

    // Setters
    setTokens(access: string, refresh: string) {
      storage.setItem(this.AUTH_TOKEN_KEY, access)
      storage.setItem(this.REFRESH_TOKEN_KEY, refresh)
    },

    setUser(user: User) {
      storage.setItem(this.USER_KEY, user)
    },

    clearAuth() {
      storage.removeItem(this.AUTH_TOKEN_KEY)
      storage.removeItem(this.REFRESH_TOKEN_KEY)
      storage.removeItem(this.USER_KEY)
    },

    // Helper methods
    hasTokens(): boolean {
      const tokens = this.tokens
      return !!(tokens.access && tokens.refresh)
    },

    getUserData(): User | null {
      return this.user
    }
  }

  // Theme module
  const themeCurrent = ref<'light' | 'dark'>('light')
  const themeIsDark = computed(() => themeCurrent.value === 'dark')
  
  const theme = {
    // Key
    THEME_KEY: 'theme',

    // State
    currentTheme: themeCurrent,

    // Computed
    isDark: themeIsDark,

    // Initialize from storage
    initialize() {
      const savedTheme = storage.getItem<'light' | 'dark'>(this.THEME_KEY)
      if (savedTheme) {
        themeCurrent.value = savedTheme
      } else {
        // Check system preference
        if (typeof window !== 'undefined') {
          const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
          themeCurrent.value = prefersDark ? 'dark' : 'light'
        }
      }
      return themeCurrent.value
    },

    // Actions
    setTheme(themeValue: 'light' | 'dark') {
      themeCurrent.value = themeValue
      storage.setItem(this.THEME_KEY, themeValue)
      updateDocumentClass()
    },

    toggleTheme() {
      const newTheme = themeCurrent.value === 'light' ? 'dark' : 'light'
      theme.setTheme(newTheme)
    }
  }

  // Language module
  const languagePreferred = ref<string>('en')
  const language = {
    // Key
    LANGUAGE_KEY: 'preferred-language',

    // State
    preferredLanguage: languagePreferred,

    // Initialize from storage
    initialize() {
      const savedLanguage = storage.getItem<string>(this.LANGUAGE_KEY, 'en')
      languagePreferred.value = savedLanguage || 'en'
      return languagePreferred.value
    },

    // Actions
    setLanguage(lang: string) {
      languagePreferred.value = lang
      storage.setItem(this.LANGUAGE_KEY, lang)
    },

    getLanguage(): string {
      return languagePreferred.value
    }
  }

  // Newsletter module
  const newsletterEmails = ref<Set<string>>(new Set())
  
  // Private helper function for newsletter
  const saveNewsletterToStorage = () => {
    const emailsArray = Array.from(newsletterEmails.value)
    storage.setItem('subscribed-emails', emailsArray)
  }
  
  const newsletter = {
    // Key
    SUBSCRIBED_EMAILS_KEY: 'subscribed-emails',

    // State
    subscribedEmails: newsletterEmails,

    // Initialize from storage
    initialize() {
      const savedEmails = storage.getItem<string[]>(this.SUBSCRIBED_EMAILS_KEY, [])
      newsletterEmails.value = new Set(savedEmails)
      return newsletterEmails.value
    },

    // Computed
    isSubscribed(email: string): boolean {
      return newsletterEmails.value.has(email.toLowerCase())
    },

    // Actions
    subscribe(email: string) {
      const normalizedEmail = email.toLowerCase()
      newsletterEmails.value.add(normalizedEmail)
      saveNewsletterToStorage()
    },

    unsubscribe(email: string) {
      const normalizedEmail = email.toLowerCase()
      newsletterEmails.value.delete(normalizedEmail)
      saveNewsletterToStorage()
    },

    getSubscribedEmails(): string[] {
      return Array.from(newsletterEmails.value)
    },

    clearSubscriptions() {
      newsletterEmails.value.clear()
      storage.removeItem(this.SUBSCRIBED_EMAILS_KEY)
    }
  }

  // Initialize all modules
  function initializeAll() {
    theme.initialize()
    language.initialize()
    newsletter.initialize()
  }

  // Initialize on store creation if client-side
  if (typeof window !== 'undefined') {
    initializeAll()
  }

  // Helper function to update document class for theme
  function updateDocumentClass() {
    if (typeof window === 'undefined') return
    if (theme.currentTheme.value === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // Update document class when theme changes
  theme.currentTheme.value = theme.initialize()
  updateDocumentClass()

  return {
    // Modules
    auth,
    theme,
    language,
    newsletter,

    // Core storage methods (for advanced use cases)
    storage: {
      getItem: <T>(key: string, defaultValue?: T) => storage.getItem(key, defaultValue),
      setItem: <T>(key: string, value: T) => storage.setItem(key, value),
      removeItem: (key: string) => storage.removeItem(key),
      clear: () => storage.clear(),
    },

    // Initialization
    initializeAll,
  }
})

// Export types
export type PreferencesStore = ReturnType<typeof usePreferencesStore>