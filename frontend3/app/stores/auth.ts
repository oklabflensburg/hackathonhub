import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Stores
import { useUIStore } from './ui'
import { usePreferencesStore } from './preferences'
import { useTeamStore } from './team'

// Utils
import { useApiClient } from '~/utils/api-client'

// Types
import type { User } from '~/types/user-types'
import type { LoginCredentials, RegisterCredentials } from '~/types/auth-types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Stores und Services
  const uiStore = useUIStore()
  const preferences = usePreferencesStore()
  const teamStore = useTeamStore()
  const apiClient = useApiClient()
  const config = useRuntimeConfig()
  const translate = (key: string, fallback?: string) => {
    try {
      const nuxtApp = useNuxtApp()
      const i18n = (nuxtApp as any).$i18n
      const result = i18n?.t ? i18n.t(key) : null
      if (typeof result === 'string') return result
      if (result && typeof result.toString === 'function') return result.toString()
    } catch {
      // Ignore and fall back below
    }
    return fallback ?? key
  }

  const isAuthenticated = computed(() => !!user.value && !!token.value)
  const isSuperuser = computed(() => user.value?.roles?.includes('superuser') || user.value?.role === 'superuser')
  const hasPermission = (code: string) => !!user.value?.permissions?.includes(code)

  const userInitials = computed(() => {
    if (!user.value) return ''
    return user.value.username.charAt(0).toUpperCase()
  })

  async function loginWithGitHub(redirectUrl?: string) {
    isLoading.value = true
    error.value = null

    try {
      // Use Nuxt runtime config
      const backendUrl = config.public.apiUrl

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
        throw new Error(translate('errors.failed_to_get_github_authorization_url'))
      }

      const data = await response.json()
      window.location.href = data.authorization_url
    } catch (err) {
      error.value = translate('errors.failed_to_initiate_github_login')
      console.error('GitHub login error:', err)
    } finally {
      isLoading.value = false
    }
  }

  async function loginWithGoogle(redirectUrl?: string) {
    isLoading.value = true
    error.value = null

    try {
      const backendUrl = config.public.apiUrl

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
        throw new Error(translate('errors.failed_to_get_google_authorization_url'))
      }

      const data = await response.json()
      window.location.href = data.authorization_url
    } catch (err) {
      error.value = translate('errors.failed_to_initiate_google_login')
      console.error('Google login error:', err)
    } finally {
      isLoading.value = false
    }
  }

  async function loginWithEmail(credentials: LoginCredentials): Promise<boolean> {
    isLoading.value = true
    error.value = null

    try {
      // Use apiClient statt fetch
      const response = await apiClient.post<{
        requires_2fa: boolean
        temp_token?: string
        user_id?: number
        access_token?: string
        refresh_token?: string
        user?: User
      }>('/api/auth/login', {
        email: credentials.email,
        password: credentials.password,
        remember_me: credentials.rememberMe ?? false
      }, {
        skipAuth: true,
        skipErrorNotification: true
      })

      console.log('Login API response:', response)
      
      // Check if 2FA is required
      if (response.requires_2fa && response.temp_token) {
        console.log('2FA required, temp_token:', response.temp_token ? 'present' : 'missing')
        // Store temporary token and user info for 2FA verification
        const tempToken = response.temp_token
        const userId = response.user_id
        
        // Navigate to 2FA verification page
        if (typeof window !== 'undefined') {
          // Store temp token in session storage for the verify-2fa page
          sessionStorage.setItem('2fa_temp_token', tempToken)
          sessionStorage.setItem('2fa_user_id', userId?.toString() || '')
          console.log('Stored temp token in sessionStorage, navigating to /verify-2fa')
          
          // Navigate to verify-2fa page
          window.location.href = '/verify-2fa'
        }
        
        // Return false to indicate 2FA is required and navigation happened
        return false
      } else {
        console.log('No 2FA required, proceeding with normal login')
        // No 2FA required, proceed with normal login
        if (response.access_token && response.refresh_token) {
          await handleAuthResponse({
            access_token: response.access_token,
            refresh_token: response.refresh_token,
            user: response.user
          })
          return true
        } else {
          throw new Error('Invalid login response')
        }
      }
    } catch (err: any) {
      const errorMessage = err instanceof Error ? err.message : translate('errors.login_failed')
      error.value = errorMessage

      // Keine UI-Notification hier - die aufrufende Komponente ist dafür verantwortlich
      // uiStore.showError(errorMessage, 'Login Error')

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
      // Use apiClient statt fetch
      const response = await apiClient.post('/api/auth/register', {
        email: credentials.email,
        username: credentials.username,
        password: credentials.password
      }, {
        skipAuth: true,
        skipErrorNotification: true
      })

      // Registration successful, but email needs verification
      // Show success message and redirect to login
      return response
    } catch (err: any) {
      const errorMessage = err instanceof Error ? err.message : translate('errors.registration_failed')
      error.value = errorMessage

      // Keine UI-Notification hier - die aufrufende Komponente ist dafür verantwortlich
      // uiStore.showError(errorMessage, 'Registration Error')

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
      // Use apiClient statt fetch
      const response = await apiClient.post('/api/auth/resend-verification', {
        email: userEmail
      }, {
        skipAuth: true,
        skipErrorNotification: true
      })

      // Show success notification
      uiStore.showSuccess(response.message || 'Verification email sent', 'Verification Email Sent')
      return response
    } catch (err: any) {
      const errorMessage = err instanceof Error ? err.message : translate('errors.failed_to_resend_verification_email')
      error.value = errorMessage

      // Keine UI-Notification hier - die aufrufende Komponente ist dafür verantwortlich
      // uiStore.showError(errorMessage, 'Resend Failed')

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

  async function refreshAccessToken(options: { silent?: boolean } = {}): Promise<boolean> {
    console.log('[Auth] Attempting token refresh')

    try {
      console.log('[Auth] Sending refresh request')
      const response = await apiClient.post<{
        access_token: string
        refresh_token: string
        user?: User
      }>('/api/auth/refresh', {}, {
        headers: refreshToken.value
          ? { 'Authorization': `Bearer ${refreshToken.value}` }
          : undefined,
        skipAuth: true,
        skipErrorNotification: true
      })

      console.log('[Auth] Token refresh successful')
      token.value = response.access_token
      refreshToken.value = response.refresh_token

      // Save to preferences store
      preferences.auth.setTokens(response.access_token, response.refresh_token)

      // Also update user data if returned
      if (response.user) {
        user.value = response.user
        preferences.auth.setUser(response.user)
      }
      return true
    } catch (err) {
      console.error('[Auth] Token refresh error:', err)
      if (!options.silent) {
        await logout()
      }
      return false
    }
  }

  async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
    // Only run on client side (matching plugin behavior)
    if (!process.client) {
      // During SSR, return a mock response or throw error
      // For simplicity, we'll use regular fetch during SSR (won't have auth headers)
      const backendUrl = config.public.apiUrl
      const fullUrl = url.startsWith('http') ? url : `${backendUrl}${url}`
      return fetch(fullUrl, {
        credentials: 'include',
        ...options
      })
    }

    const backendUrl = config.public.apiUrl
    const fullUrl = url.startsWith('http') ? url : `${backendUrl}${url}`

    // Check if this is an API call to our backend (similar to plugin logic)
    const isApiCall = fullUrl.startsWith(backendUrl) || url.startsWith('/api/')

    // Prepare headers
    const headers = new Headers(options.headers || {})

    // Add auth header if token exists AND this is an API call
    if (token.value && isApiCall && !headers.has('Authorization')) {
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

    const requestOptions = {
      credentials: 'include' as RequestCredentials,
      ...options,
      headers,
      body: requestBody
    }
    let response
    try {
      response = await fetch(fullUrl, requestOptions)
    } catch (error) {
      // Handle network errors (e.g., offline, CORS, etc.)
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // This is a network error from fetch()
        throw new Error(translate('errors.networkErrorFetchResource'))
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

        const retryOptions = {
          credentials: 'include' as RequestCredentials,
          ...options,
          headers,
          body: retryBody
        }
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
        await apiClient.post('/api/auth/logout', {}, {
          headers: {
            'Authorization': `Bearer ${refreshToken.value}`
          },
          skipErrorNotification: true
        })
        console.log('[Auth] Backend logout successful')
      } catch (err: any) {
        // 401 Unauthorized is expected if token is already revoked/expired
        if (err.status === 401) {
          console.log('[Auth] Backend logout: token already invalid (expected)')
        } else {
          console.warn('[Auth] Backend logout failed:', err)
        }
        // Continue with client-side logout anyway
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

  let initializePromise: Promise<void> | null = null

  async function initializeAuth() {
    if (initializePromise) {
      return initializePromise
    }

    initializePromise = (async () => {
      // Try to use cookies for SSR compatibility
      if (typeof window === 'undefined') {
        // Server-side: try to read cookies using useCookie
        // Note: useCookie is a Nuxt composable that works in middleware and plugins
        // but not directly in stores. We'll handle server-side auth in middleware instead.
        // For now, we'll leave token as null on server to avoid hydration mismatches.
        // The middleware will handle server-side redirects based on cookies.
        return
      }

      // Client-side: check for tokens in URL (from OAuth callback)
      preferences.auth.cleanupLegacyCookies()

      const urlParams = new URLSearchParams(window.location.search)
      const accessToken = urlParams.get('access_token')
      const refreshTokenParam = urlParams.get('refresh_token')
      const source = urlParams.get('source')

      if (accessToken && (source === 'github' || source === 'google')) {
        await handleAuthResponse({
          access_token: accessToken,
          refresh_token: refreshTokenParam || '',
          user: null
        })

        // Clear URL parameters
        const newUrl = window.location.pathname
        window.history.replaceState({}, '', newUrl)

        // Start background token refresh timer
        startBackgroundTokenRefresh()

        // If user is on login or register page, redirect to home
        if (window.location.pathname === '/login' || window.location.pathname === '/register') {
          window.location.href = '/'
        }
        return
      }

      const storedTokens = preferences.auth.tokens
      const storedUser = preferences.auth.user

      if (storedUser) {
        user.value = storedUser
      }

      if (storedTokens.access) {
        token.value = storedTokens.access
      }

      if (storedTokens.refresh) {
        refreshToken.value = storedTokens.refresh
      }

      const refreshed = await refreshAccessToken({ silent: true })
      if (refreshed) {
        startBackgroundTokenRefresh()
        return
      }

      if (storedTokens.access) {
        try {
          await fetchUserWithToken(storedTokens.access)
          startBackgroundTokenRefresh()
          return
        } catch (err) {
          console.error('Failed to restore auth from stored access token:', err)
        }
      }

      user.value = null
      token.value = null
      refreshToken.value = null
      preferences.auth.clearAuth()
    })()

    try {
      await initializePromise
    } finally {
      initializePromise = null
    }
  }

  async function fetchUserWithToken(tokenValue: string) {
    try {
      const userData = await apiClient.get<User>('/api/me', {
        headers: {
          'Authorization': `Bearer ${tokenValue}`
        }
      })

      user.value = userData
      preferences.auth.setUser(userData)

      // Initialize team store with user's teams
      try {
        teamStore.initializeFromUser(userData)
      } catch (err) {
        console.error('Failed to initialize team store:', err)
      }
      return userData
    } catch (err) {
      console.error('Failed to fetch user with token:', err)
      preferences.auth.clearAuth()
      throw err
    }
  }

  async function refreshUser() {
    if (!token.value) return

    try {
      const userData = await apiClient.get<User>('/api/me', {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })

      user.value = userData
      preferences.auth.setUser(userData)

      // Initialize team store with user's teams
      try {
        teamStore.initializeFromUser(userData)
      } catch (err) {
        console.error('Failed to initialize team store:', err)
      }
    } catch (err: any) {
      if (err.status === 401) {
        // Token expired, clear auth
        logout()
      } else {
        console.error('Failed to refresh user:', err)
      }
    }
  }

  // Helper function for authenticated API calls with token expiration handling
  async function authenticatedFetch(url: string, options: RequestInit = {}) {
    if (!token.value) {
      throw new Error(translate('errors.not_authenticated'))
    }

    const backendUrl = config.public.apiUrl
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
        throw new Error(translate('errors.networkErrorFetchResource'))
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
            throw new Error(translate('errors.networkErrorFetchResource'))
          }
          throw error // Re-throw other errors
        }

        // If still 401 after refresh, token is invalid
        if (response.status === 401) {
          logout()
          throw new Error(translate('errors.session_expired'))
        }
      } else {
        // Refresh failed, logout
        logout()
        throw new Error(translate('errors.session_expired'))
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

  // 2FA Methods
  async function verifyTwoFactor(params: {
    code: string
    temp_token: string
    remember_device?: boolean
  }): Promise<boolean> {
    isLoading.value = true
    error.value = null

    try {
      const backendUrl = config.public.apiUrl

      const response = await fetch(`${backendUrl}/api/auth/verify-2fa`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || translate('errors.2fa_verification_failed'))
      }

      const data = await response.json()
      await handleAuthResponse(data)
      return true
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : translate('errors.2fa_verification_failed')
      error.value = errorMessage

      // Keine UI-Notification hier - die aufrufende Komponente ist dafür verantwortlich
      // uiStore.showError(errorMessage, '2FA Verification Error')

      console.error('2FA verification error:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function verifyTwoFactorBackup(params: {
    backup_code: string
    temp_token: string
  }): Promise<boolean> {
    isLoading.value = true
    error.value = null

    try {
      const backendUrl = config.public.apiUrl

      const response = await fetch(`${backendUrl}/api/auth/verify-2fa-backup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || translate('errors.backup_code_invalid'))
      }

      const data = await response.json()
      await handleAuthResponse(data)
      return true
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : translate('errors.backup_code_invalid')
      error.value = errorMessage

      // Keine UI-Notification hier - die aufrufende Komponente ist dafür verantwortlich
      // uiStore.showError(errorMessage, 'Backup Code Error')

      console.error('Backup code verification error:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function loginWithEmail2FA(credentials: LoginCredentials): Promise<{
    requires_2fa: boolean
    temp_token?: string
    user?: User
  }> {
    isLoading.value = true
    error.value = null

    try {
      const backendUrl = config.public.apiUrl

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
        throw new Error(errorData.detail || translate('errors.login_failed'))
      }

      const data = await response.json()
      
      // Check if 2FA is required
      if (data.requires_2fa) {
        return {
          requires_2fa: true,
          temp_token: data.temp_token,
          user: data.user
        }
      } else {
        // No 2FA required, proceed with normal login
        await handleAuthResponse(data)
        return {
          requires_2fa: false,
          user: data.user
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : translate('errors.login_failed')
      error.value = errorMessage

      // Keine UI-Notification hier - die aufrufende Komponente ist dafür verantwortlich
      // const uiStore = useUIStore()
      // uiStore.showError(errorMessage, 'Login Error')

      console.error('Email login with 2FA error:', err)
      throw err
    } finally {
      isLoading.value = false
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
    isSuperuser,
    hasPermission,
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
    stopBackgroundTokenRefresh,
    verifyTwoFactor,
    verifyTwoFactorBackup,
    loginWithEmail2FA
  }
})
