import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '~/types/user-types'

// SSR-safe cookie access using Nuxt's useCookie composable
// We need to import it dynamically to avoid SSR issues
let useCookie: (key: string, options?: any) => { value: any } = () => ({ value: null })

// Initialize useCookie only when needed to avoid SSR issues
const initUseCookie = () => {
  if (typeof window !== 'undefined') {
    // Client-side: use the actual useCookie from Nuxt
    try {
      // @ts-ignore - We'll import it dynamically
      const { useCookie: nuxtUseCookie } = require('#imports')
      useCookie = nuxtUseCookie
    } catch (error) {
      console.warn('Failed to import useCookie, falling back to document.cookie')
      // Fallback implementation using document.cookie
      useCookie = (key: string, options?: any) => {
        const cookies = document.cookie.split(';').reduce((acc, cookie) => {
          const [k, v] = cookie.trim().split('=')
          if (k) acc[k] = decodeURIComponent(v || '')
          return acc
        }, {} as Record<string, string>)
        
        const cookieValue = cookies[key] || null
        
        return {
          get value() {
            return cookieValue
          },
          set value(newValue: any) {
            if (newValue === null || newValue === undefined) {
              // Delete cookie
              document.cookie = `${key}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`
            } else {
              // Set cookie
              const maxAge = options?.maxAge || 60 * 60 * 24 * 7 // 7 days default
              const sameSite = options?.sameSite || 'lax'
              const secure = options?.secure || process.env.NODE_ENV === 'production'
              const path = options?.path || '/'
              
              let cookieStr = `${key}=${encodeURIComponent(newValue)}; max-age=${maxAge}; path=${path}; sameSite=${sameSite}`
              if (secure) {
                cookieStr += '; secure'
              }
              document.cookie = cookieStr
            }
          }
        }
      }
    }
  } else {
    // Server-side: we need to access cookies via headers
    // This is handled by Nuxt's useCookie automatically
    // We'll use a mock for now, actual implementation will be provided by Nuxt
    useCookie = (key: string, options?: any) => {
      // Server-side cookies are handled by Nuxt middleware
      return { value: null }
    }
  }
}

// Initialize on first use
let isInitialized = false
const getUseCookie = () => {
  if (!isInitialized) {
    initUseCookie()
    isInitialized = true
  }
  return useCookie
}

// SSR-safe storage wrapper that uses cookies for auth tokens and localStorage for other data
class SSRStorage {
  private isClient = typeof window !== 'undefined'
  private cleanedKeys = new Set<string>() // Track keys we've already cleaned up

  private getClientCookieValue(key: string): string | null {
    if (!this.isClient) return null
    const cookies = document.cookie.split(';').reduce((acc, cookie) => {
      const [k, v] = cookie.trim().split('=')
      if (k) acc[k] = decodeURIComponent(v || '')
      return acc
    }, {} as Record<string, string>)
    return cookies[key] || null
  }

  private setClientCookieValue(
    key: string,
    value: string | null,
    options?: { maxAge?: number; sameSite?: string; secure?: boolean; path?: string }
  ) {
    if (!this.isClient) return
    if (value === null || value === undefined) {
      document.cookie = `${key}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`
      return
    }
    const maxAge = options?.maxAge || 60 * 60 * 24 * 7
    const sameSite = options?.sameSite || 'lax'
    const secure = options?.secure ?? process.env.NODE_ENV === 'production'
    const path = options?.path || '/'
    let cookieStr = `${key}=${encodeURIComponent(value)}; max-age=${maxAge}; path=${path}; sameSite=${sameSite}`
    if (secure) cookieStr += '; secure'
    document.cookie = cookieStr
  }

  getItem<T>(key: string, defaultValue: T | null = null): T | null {
    // Special handling for auth tokens: use cookies for SSR compatibility
    if (key === 'auth_token' || key === 'refresh_token') {
      if (this.isClient) {
        const value = this.getClientCookieValue(key)
        if (!value || value === 'undefined' || value === 'null') return defaultValue
        return value as T
      }
      // Use useCookie for server-side reading (best effort)
      let value: any = null
      try {
        const cookie = getUseCookie()(key)
        value = cookie.value
      } catch {
        value = null
      }
      if (!value || value === 'undefined' || value === 'null') return defaultValue
      
      // Tokens are stored as plain strings, not JSON
      return value as T
    }
    
    // For other keys, use localStorage on client only
    if (!this.isClient) return defaultValue
    
    const item = localStorage.getItem(key)
    if (!item || item === 'undefined' || item === 'null') return defaultValue
    
    // Safe JSON parsing without throwing errors
    const parsed = this.safeJsonParse(item)
    if (parsed === undefined) {
      // Invalid JSON - clean it up
      if (!this.cleanedKeys.has(key)) {
        console.warn(`[Preferences] Removing corrupted data for key "${key}"`)
        this.cleanedKeys.add(key)
      }
      try {
        localStorage.removeItem(key)
      } catch (removeError) {
        // Ignore removal errors
      }
      return defaultValue
    }
    
    return parsed as T
  }

  // Helper method to parse JSON without throwing errors
  private safeJsonParse(str: string): any {
    // First, check if it looks like JSON (starts with {, [, ", true, false, null, or a number)
    const trimmed = str.trim()
    if (trimmed === '') return undefined
    
    try {
      // Use JSON.parse but wrap it to catch any errors
      return JSON.parse(str)
    } catch {
      return undefined
    }
  }

  setItem<T>(key: string, value: T): void {
    // Special handling for auth tokens: store in cookies for SSR compatibility
    if (key === 'auth_token' || key === 'refresh_token') {
      if (this.isClient) {
        this.setClientCookieValue(key, value as string, {
          maxAge: 60 * 60 * 24 * 7,
          sameSite: 'lax',
          secure: process.env.NODE_ENV === 'production'
        })
        return
      }
      try {
        const cookie = getUseCookie()(key, {
          maxAge: 60 * 60 * 24 * 7, // 7 days
          sameSite: 'lax',
          secure: process.env.NODE_ENV === 'production'
        })
        cookie.value = value as string
      } catch {
        // Server-side fallback: do nothing if composable is unavailable
      }
      return
    }
    
    // For other keys, use localStorage on client only
    if (!this.isClient) return
    try {
      // Handle undefined/null values by removing the item instead
      if (value === undefined || value === null) {
        localStorage.removeItem(key)
        return
      }
      
      const serialized = JSON.stringify(value)
      // JSON.stringify can return undefined for certain values (like undefined itself)
      if (serialized === undefined) {
        console.warn(`[Preferences] Cannot serialize value for key "${key}", removing item`)
        localStorage.removeItem(key)
        return
      }
      
      localStorage.setItem(key, serialized)
    } catch (error) {
      console.error(`[Preferences] Failed to set item "${key}":`, error)
    }
  }

  removeItem(key: string): void {
    // Special handling for auth tokens: remove cookies
    if (key === 'auth_token' || key === 'refresh_token') {
      if (this.isClient) {
        this.setClientCookieValue(key, null)
        return
      }
      try {
        const cookie = getUseCookie()(key)
        cookie.value = null
      } catch {
        // Server-side fallback: do nothing if composable is unavailable
      }
      return
    }
    
    // For other keys, use localStorage on client only
    if (!this.isClient) return
    try {
      localStorage.removeItem(key)
    } catch (error) {
      console.error(`[Preferences] Failed to remove item "${key}":`, error)
    }
  }

  clear(): void {
    // Clear auth tokens from cookies
    if (this.isClient) {
      this.setClientCookieValue('auth_token', null)
      this.setClientCookieValue('refresh_token', null)
    } else {
      try {
        const authTokenCookie = getUseCookie()('auth_token')
        const refreshTokenCookie = getUseCookie()('refresh_token')
        authTokenCookie.value = null
        refreshTokenCookie.value = null
      } catch {
        // Server-side fallback: do nothing if composable is unavailable
      }
    }
    
    // Clear localStorage on client only
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
