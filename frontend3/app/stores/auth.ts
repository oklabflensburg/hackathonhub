import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useUIStore } from './ui'
import { usePreferencesStore } from './preferences'
import { useTeamStore } from './team'

export interface User {
  id: number
  github_id?: string
  google_id?: string
  username: string
  avatar_url: string
  email?: string
  email_verified?: boolean
  auth_method?: 'github' | 'google' | 'email'
  created_at: string
  last_login?: string
  name?: string
  bio?: string
  location?: string
  company?: string
  updated_at?: string
  is_admin?: boolean
  // Extended fields from /api/me (UserWithDetails)
  teams?: Array<{
    id: number
    team_id: number
    user_id: number
    role: 'owner' | 'member'
    joined_at: string
    team?: {
      id: number
      name: string
      description: string
      hackathon_id: number
      max_members: number
      is_open: boolean
      created_by: number
      created_at: string
      member_count?: number
    }
  }>
  projects?: any[]
  votes?: any[]
  comments?: any[]
  hackathon_registrations?: any[]
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterCredentials {
  email: string
  username: string
  password: string
  confirmPassword: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!user.value && !!token.value)
  const userInitials = computed(() => {
    if (!user.value) return ''
    return user.value.username.charAt(0).toUpperCase()
  })

  async function loginWithGitHub(redirectUrl?: string) {
    isLoading.value = true
    error.value = null

    try {
      // Use Nuxt runtime config
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'

      // Get current URL if not provided
      if (!redirectUrl && typeof window !== 'undefined') {
        redirectUrl = window.location.pathname + window.location.search
        // If user is on login or register page, redirect to home after OAuth
        if (window.location.pathname === '/login' || window.location.pathname === '/register') {
          redirectUrl = '/'
        }
      }

      // First, get the GitHub authorization URL from backend
      const url = new URL(`${backendUrl}/api/auth/github`)
      if (redirectUrl) {
        url.searchParams.append('redirect_url', redirectUrl)
      }

      // Prepare headers with Authorization if user is authenticated
      const headers: HeadersInit = {}
      if (token.value) {
        headers['Authorization'] = `Bearer ${token.value}`
      }

      const response = await fetch(url.toString(), { headers })
      if (!response.ok) {
        const { t } = useI18n()
        throw new Error(t('errors.failed_to_get_github_authorization_url'))
      }

      const data = await response.json()
      window.location.href = data.authorization_url
    } catch (err) {
      const { t } = useI18n()
      error.value = t('errors.failed_to_initiate_github_login')
      console.error('GitHub login error:', err)
    } finally {
      isLoading.value = false
    }
  }

  async function loginWithGoogle(redirectUrl?: string) {
    isLoading.value = true
    error.value = null

    try {
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'

      if (!redirectUrl && typeof window !== 'undefined') {
        redirectUrl = window.location.pathname + window.location.search
        // If user is on login or register page, redirect to home after OAuth
        if (window.location.pathname === '/login' || window.location.pathname === '/register') {
          redirectUrl = '/'
        }
      }

      const url = new URL(`${backendUrl}/api/auth/google`)
      if (redirectUrl) {
        url.searchParams.append('redirect_url', redirectUrl)
      }

      const response = await fetch(url.toString())
      if (!response.ok) {
        const { t } = useI18n()
        throw new Error(t('errors.failed_to_get_google_authorization_url'))
      }

      const data = await response.json()
      window.location.href = data.authorization_url
    } catch (err) {
      const { t } = useI18n()
      error.value = t('errors.failed_to_initiate_google_login')
      console.error('Google login error:', err)
    } finally {
      isLoading.value = false
    }
  }

  async function loginWithEmail(credentials: LoginCredentials) {
    isLoading.value = true
    error.value = null

    try {
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'

      const response = await fetch(`${backendUrl}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: credentials.email,
          password: credentials.password
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        const { t } = useI18n()
        throw new Error(errorData.detail || t('errors.login_failed'))
      }

      const data = await response.json()
      await handleAuthResponse(data)
    } catch (err) {
      const { t } = useI18n()
      const errorMessage = err instanceof Error ? err.message : t('errors.login_failed')
      error.value = errorMessage

      // Also show notification for better visibility
      const uiStore = useUIStore()
      const authStore = useAuthStore()
      uiStore.showError(errorMessage, 'Login Error')

      console.error('Email login error:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function registerWithEmail(credentials: RegisterCredentials) {
    isLoading.value = true
    error.value = null

    try {
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'

      const response = await fetch(`${backendUrl}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: credentials.email,
          username: credentials.username,
          password: credentials.password
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        const { t } = useI18n()
        const errorDetail = errorData.detail || t('errors.registration_failed')

        // Provide more user-friendly messages for common errors
        if (errorDetail.includes('email already exists')) {
          throw new Error(t('errors.email_already_exists', { email: credentials.email }))
        } else if (errorDetail.includes('Username already taken')) {
          throw new Error(t('errors.username_already_taken', { username: credentials.username }))
        } else if (errorDetail.includes('Invalid email address')) {
          throw new Error(t('errors.invalid_email_address'))
        } else if (errorDetail.includes('password cannot be longer than 72 bytes')) {
          // This error might be caused by bcrypt library issues
          // Provide a helpful message
          throw new Error(t('errors.password_validation_failed'))
        } else if (errorDetail.includes('bcrypt') || errorDetail.includes('__about__')) {
          // Handle bcrypt library errors
          throw new Error(t('errors.authentication_system_error'))
        } else {
          throw new Error(errorDetail)
        }
      }

      const data = await response.json()
      // Registration successful, but email needs verification
      // Show success message and redirect to login
      return data
    } catch (err) {
      const { t } = useI18n()
      const errorMessage = err instanceof Error ? err.message : t('errors.registration_failed')
      error.value = errorMessage

      // Also show notification for better visibility
      const uiStore = useUIStore()
      uiStore.showError(errorMessage, 'Registration Error')

      console.error('Registration error:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function resendVerificationEmail(userEmail: string) {
    const previousError = error.value
    error.value = null

    try {
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'

      const response = await fetch(`${backendUrl}/api/auth/resend-verification`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: userEmail
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        const { t } = useI18n()
        throw new Error(errorData.detail || t('errors.failed_to_resend_verification_email'))
      }

      const data = await response.json()
      // Show success notification
      const uiStore = useUIStore()
      uiStore.showSuccess(data.message, 'Verification Email Sent')
      return data
    } catch (err) {
      const { t } = useI18n()
      const errorMessage = err instanceof Error ? err.message : t('errors.failed_to_resend_verification_email')
      error.value = errorMessage

      // Also show notification for better visibility
      const uiStore = useUIStore()
      uiStore.showError(errorMessage, 'Resend Failed')

      console.error('Resend verification error:', err)
      throw err
    }
  }

  async function handleAuthResponse(authData: any) {
    token.value = authData.access_token
    refreshToken.value = authData.refresh_token

    // Use preferences store for storage
    const preferences = usePreferencesStore()
    preferences.auth.setTokens(authData.access_token, authData.refresh_token)

    // Fetch user info
    await fetchUserWithToken(authData.access_token)
  }

  async function refreshAccessToken(): Promise<boolean> {
    console.log('[Auth] Attempting token refresh')
    if (!refreshToken.value) {
      console.log('[Auth] No refresh token available - logging out')
      logout()
      return false
    }

    try {
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'

      console.log('[Auth] Sending refresh request to:', `${backendUrl}/api/auth/refresh`)
      const response = await fetch(`${backendUrl}/api/auth/refresh`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${refreshToken.value}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        console.log('[Auth] Token refresh successful')
        const data = await response.json()
        token.value = data.access_token
        refreshToken.value = data.refresh_token

        // Save to preferences store
        const preferences = usePreferencesStore()
        preferences.auth.setTokens(data.access_token, data.refresh_token)

        // Also update user data if returned
        if (data.user) {
          user.value = data.user
          preferences.auth.setUser(data.user)
        }
        return true
      } else {
        // Refresh failed, logout
        console.error('[Auth] Token refresh failed with status:', response.status)
        logout()
        return false
      }
    } catch (err) {
      console.error('[Auth] Token refresh error:', err)
      logout()
      return false
    }
  }

  async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
    // Only run on client side (matching plugin behavior)
    if (!process.client) {
      // During SSR, return a mock response or throw error
      // For simplicity, we'll use regular fetch during SSR (won't have auth headers)
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'
      const fullUrl = url.startsWith('http') ? url : `${backendUrl}${url}`
      return fetch(fullUrl, options)
    }

    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    const fullUrl = url.startsWith('http') ? url : `${backendUrl}${url}`

    // Check if this is an API call to our backend (similar to plugin logic)
    const isApiCall = fullUrl.startsWith(backendUrl) || url.startsWith('/api/')

    // Prepare headers
    const headers = new Headers(options.headers || {})

    // Add auth header if token exists AND this is an API call
    if (token.value && isApiCall) {
      headers.set('Authorization', `Bearer ${token.value}`)
    }

    // Add Content-Type for JSON requests (POST/PUT/PATCH) if not FormData
    // Only for API calls (matching plugin behavior)
    if (isApiCall && !headers.has('Content-Type') && options.method && ['POST', 'PUT', 'PATCH'].includes(options.method)) {
      const isFormData = options.body instanceof FormData
      if (!isFormData) {
        headers.set('Content-Type', 'application/json')
      }
    }

    // Helper function to clone FormData
    const cloneFormData = (formData: FormData): FormData => {
      const newFormData = new FormData()
      for (const [key, value] of formData.entries()) {
        newFormData.append(key, value)
      }
      return newFormData
    }

    // For authenticated API calls with FormData, we need to handle potential retry
    // Clone FormData upfront so we have a fresh copy for retry if needed
    let requestBody = options.body
    let hasClonedFormData = false

    if (isApiCall && token.value && options.body instanceof FormData) {
      // Clone FormData to preserve it for potential retry
      requestBody = cloneFormData(options.body as FormData)
      hasClonedFormData = true
    }

    const requestOptions = { ...options, headers, body: requestBody }
    let response
    try {
      response = await fetch(fullUrl, requestOptions)
    } catch (error) {
      // Handle network errors (e.g., offline, CORS, etc.)
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // This is a network error from fetch()
        const { t } = useI18n()
        throw new Error(t('errors.networkErrorFetchResource'))
      }
      throw error // Re-throw other errors
    }

    // Handle token expiration (skip for refresh endpoint to avoid infinite loop)
    // Only handle 401 for API calls (matching plugin behavior)
    const isRefreshEndpoint = fullUrl.includes('/api/auth/refresh')
    if (response.status === 401 && token.value && !isRefreshEndpoint && isApiCall) {
      console.log('[fetchWithAuth] Token expired, attempting refresh for:', url)

      const refreshed = await refreshAccessToken()
      if (refreshed) {
        console.log('[fetchWithAuth] Token refresh successful, retrying request')
        // Update auth header with new token
        headers.set('Authorization', `Bearer ${token.value}`)

        // Prepare body for retry
        let retryBody = options.body
        if (options.body instanceof FormData) {
          if (hasClonedFormData) {
            // We already cloned the FormData for the first request
            // The clone was consumed, so we need to clone from the original again
            try {
              retryBody = cloneFormData(options.body as FormData)
            } catch (err) {
              console.error('[fetchWithAuth] Failed to clone FormData for retry:', err)
              // If original FormData is consumed, we can't retry
              return response
            }
          } else {
            // FormData wasn't cloned upfront (edge case: token existed but we didn't clone)
            // Try to clone now
            try {
              retryBody = cloneFormData(options.body as FormData)
            } catch (err) {
              console.error('[fetchWithAuth] Failed to clone FormData for retry:', err)
              return response
            }
          }
        }

        const retryOptions = { ...options, headers, body: retryBody }
        response = await fetch(fullUrl, retryOptions)

        // Check if retry also failed
        if (response.status === 401) {
          console.warn('[fetchWithAuth] Request still unauthorized after token refresh')
        }
      } else {
        console.warn('[fetchWithAuth] Token refresh failed')
      }
    }

    return response
  }

  async function logout() {
    console.log('[Auth] Logging out user')

    // Stop background token refresh timer
    stopBackgroundTokenRefresh()

    // Try to call backend logout endpoint with refresh token
    if (refreshToken.value) {
      try {
        const config = useRuntimeConfig()
        const backendUrl = config.public.apiUrl || 'http://localhost:8000'
        const response = await fetch(`${backendUrl}/api/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${refreshToken.value}`,
            'Content-Type': 'application/json'
          }
        })
        if (!response.ok) {
          // 401 Unauthorized is expected if token is already revoked/expired
          if (response.status === 401) {
            console.log('[Auth] Backend logout: token already invalid (expected)')
          } else {
            console.warn('[Auth] Backend logout failed:', response.status, response.statusText)
          }
          // Continue with client-side logout anyway
        } else {
          console.log('[Auth] Backend logout successful')
        }
      } catch (err) {
        console.error('[Auth] Error calling logout endpoint:', err)
        // Continue with client-side logout
      }
    }

    user.value = null
    token.value = null
    refreshToken.value = null

    // Clear auth data from preferences store
    const preferences = usePreferencesStore()
    preferences.auth.clearAuth()
    console.log('[Auth] Auth data cleared from preferences store')
    console.log('[Auth] Logout complete')

    // Also reset any UI state that might be showing user info
    // This helps ensure UI updates properly after logout
    const uiStore = useUIStore()
    // You could add a method to reset UI state if needed

    // Clear team store
    try {
      const teamStore = useTeamStore()
      teamStore.clear()
    } catch (err) {
      console.error('Failed to clear team store:', err)
    }
  }

  function initializeAuth() {
    // Try to use cookies for SSR compatibility
    let authToken: string | null = null
    let refreshTokenValue: string | null = null
    let userData: User | null = null

    if (typeof window === 'undefined') {
      // Server-side: we can't check localStorage, but we could check cookies
      // For now, we'll leave token as null on server
      // This means isAuthenticated will be false on server, true on client for logged-in users
      // This causes hydration mismatches but is the current limitation
      return
    } else {
      // Client-side: check for token in URL (from OAuth callback)
      const urlParams = new URLSearchParams(window.location.search)
      const urlToken = urlParams.get('token')
      const source = urlParams.get('source')

      if (urlToken && (source === 'github' || source === 'google')) {
        // Store token from URL
        token.value = urlToken
        const preferences = usePreferencesStore()
        preferences.auth.setTokens(urlToken, '') // Refresh token will be set later

        // Clear URL parameters
        const newUrl = window.location.pathname
        window.history.replaceState({}, '', newUrl)

        // Fetch user info with the token
        fetchUserWithToken(urlToken)

        // Start background token refresh timer
        startBackgroundTokenRefresh()

        // If user is on login or register page, redirect to home
        if (window.location.pathname === '/login' || window.location.pathname === '/register') {
          window.location.href = '/'
        }
        return
      } else {
        // Check preferences store for existing tokens
        const preferences = usePreferencesStore()
        const storedTokens = preferences.auth.tokens
        const storedUser = preferences.auth.user

        if (storedTokens.access && storedUser) {
          try {
            token.value = storedTokens.access
            refreshToken.value = storedTokens.refresh
            user.value = storedUser

            // Start background token refresh timer
            startBackgroundTokenRefresh()
          } catch (err) {
            console.error('Failed to load stored user:', err)
            preferences.auth.clearAuth()
          }
        }
      }
    }
  }

  async function fetchUserWithToken(tokenValue: string) {
    try {
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'

      const response = await fetch(`${backendUrl}/api/me`, {
        headers: {
          'Authorization': `Bearer ${tokenValue}`
        }
      })

      if (response.ok) {
        const userData = await response.json()
        user.value = userData
        const preferences = usePreferencesStore()
        preferences.auth.setUser(userData)

        // Initialize team store with user's teams
        try {
          const teamStore = useTeamStore()
          teamStore.initializeFromUser(userData)
        } catch (err) {
          console.error('Failed to initialize team store:', err)
        }
      } else {
        console.error('Failed to fetch user with token')
        const preferences = usePreferencesStore()
        preferences.auth.clearAuth()
      }
    } catch (err) {
      console.error('Error fetching user:', err)
      const preferences = usePreferencesStore()
      preferences.auth.clearAuth()
    }
  }

  async function refreshUser() {
    if (!token.value) return

    try {
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'
      const response = await fetch(`${backendUrl}/api/me`, {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })

      if (response.ok) {
        const userData = await response.json()
        user.value = userData
        const preferences = usePreferencesStore()
        preferences.auth.setUser(userData)

        // Initialize team store with user's teams
        try {
          const teamStore = useTeamStore()
          teamStore.initializeFromUser(userData)
        } catch (err) {
          console.error('Failed to initialize team store:', err)
        }
      } else if (response.status === 401) {
        // Token expired, clear auth
        logout()
      }
    } catch (err) {
      console.error('Failed to refresh user:', err)
    }
  }

  // Helper function for authenticated API calls with token expiration handling
  async function authenticatedFetch(url: string, options: RequestInit = {}) {
    if (!token.value) {
      const { t } = useI18n()
      throw new Error(t('errors.not_authenticated'))
    }

    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    const fullUrl = url.startsWith('http') ? url : `${backendUrl}${url}`

    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token.value}`,
      ...options.headers
    }

    let response
    try {
      response = await fetch(fullUrl, {
        ...options,
        headers
      })
    } catch (error) {
      // Handle network errors (e.g., offline, CORS, etc.)
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // This is a network error from fetch()
        const { t } = useI18n()
        throw new Error(t('errors.networkErrorFetchResource'))
      }
      throw error // Re-throw other errors
    }

    // Check for token expiration and try to refresh
    if (response.status === 401 && token.value) {
      const refreshed = await refreshAccessToken()
      if (refreshed) {
        // Retry with new token
        const newHeaders = {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token.value}`,
          ...options.headers
        }
        try {
          response = await fetch(fullUrl, {
            ...options,
            headers: newHeaders
          })
        } catch (error) {
          // Handle network errors (e.g., offline, CORS, etc.)
          if (error instanceof TypeError && error.message.includes('fetch')) {
            // This is a network error from fetch()
            const { t } = useI18n()
            throw new Error(t('errors.networkErrorFetchResource'))
          }
          throw error // Re-throw other errors
        }

        // If still 401 after refresh, token is invalid
        if (response.status === 401) {
          logout()
          const { t } = useI18n()
          throw new Error(t('errors.session_expired'))
        }
      } else {
        // Refresh failed, logout
        logout()
        const { t } = useI18n()
        throw new Error(t('errors.session_expired'))
      }
    }

    return response
  }

  // Background token refresh timer
  let refreshTimer: NodeJS.Timeout | null = null

  function startBackgroundTokenRefresh() {
    // Clear existing timer if any
    if (refreshTimer) {
      clearInterval(refreshTimer)
    }

    // Only start timer if we have a refresh token
    if (!refreshToken.value) {
      return
    }

    // Refresh token every 10 minutes (600000 ms)
    // This is proactive refresh to prevent token expiration during user session
    refreshTimer = setInterval(async () => {
      if (refreshToken.value && token.value) {
        try {
          console.log('[Auth] Background token refresh triggered')
          await refreshAccessToken()
        } catch (error) {
          console.error('[Auth] Background token refresh failed:', error)
          // Don't logout on background refresh failure - let next API call handle it
        }
      }
    }, 10 * 60 * 1000) // 10 minutes
  }

  function stopBackgroundTokenRefresh() {
    if (refreshTimer) {
      clearInterval(refreshTimer)
      refreshTimer = null
    }
  }

  return {
    user,
    token,
    refreshToken,
    isLoading,
    error,
    isAuthenticated,
    userInitials,
    loginWithGitHub,
    loginWithGoogle,
    loginWithEmail,
    registerWithEmail,
    resendVerificationEmail,
    logout,
    initializeAuth,
    refreshUser,
    authenticatedFetch,
    refreshAccessToken,
    fetchWithAuth,
    handleAuthResponse,
    startBackgroundTokenRefresh,
    stopBackgroundTokenRefresh
  }
})