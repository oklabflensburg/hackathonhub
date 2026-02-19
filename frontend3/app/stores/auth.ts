import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useUIStore } from './ui'

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
      }

      // First, get the GitHub authorization URL from backend
      const url = new URL(`${backendUrl}/api/auth/github`)
      if (redirectUrl) {
        url.searchParams.append('redirect_url', redirectUrl)
      }

      const response = await fetch(url.toString())
      if (!response.ok) {
        throw new Error('Failed to get GitHub authorization URL')
      }

      const data = await response.json()
      window.location.href = data.authorization_url
    } catch (err) {
      error.value = 'Failed to initiate GitHub login'
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
      }

      const url = new URL(`${backendUrl}/api/auth/google`)
      if (redirectUrl) {
        url.searchParams.append('redirect_url', redirectUrl)
      }

      const response = await fetch(url.toString())
      if (!response.ok) {
        throw new Error('Failed to get Google authorization URL')
      }

      const data = await response.json()
      window.location.href = data.authorization_url
    } catch (err) {
      error.value = 'Failed to initiate Google login'
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
        throw new Error(errorData.detail || 'Login failed')
      }

      const data = await response.json()
      await handleAuthResponse(data)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Login failed'
      error.value = errorMessage

      // Also show notification for better visibility
      const uiStore = useUIStore()
      uiStore.showError(errorMessage, 'Login Error')

      console.error('Email login error:', err)
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
        const errorDetail = errorData.detail || 'Registration failed'

        // Provide more user-friendly messages for common errors
        if (errorDetail.includes('email already exists')) {
          throw new Error(`An account with email ${credentials.email} already exists. Please try logging in or use a different email address.`)
        } else if (errorDetail.includes('Username already taken')) {
          throw new Error(`Username "${credentials.username}" is already taken. Please choose a different username.`)
        } else if (errorDetail.includes('Invalid email address')) {
          throw new Error('Please enter a valid email address.')
        } else if (errorDetail.includes('password cannot be longer than 72 bytes')) {
          // This error might be caused by bcrypt library issues
          // Provide a helpful message
          throw new Error('Password validation failed. Please try a different password or contact support if the issue persists.')
        } else if (errorDetail.includes('bcrypt') || errorDetail.includes('__about__')) {
          // Handle bcrypt library errors
          throw new Error('Authentication system error. Please try again later or contact support.')
        } else {
          throw new Error(errorDetail)
        }
      }

      const data = await response.json()
      // Registration successful, but email needs verification
      // Show success message and redirect to login
      return data
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Registration failed'
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

  async function handleAuthResponse(authData: any) {
    token.value = authData.access_token
    refreshToken.value = authData.refresh_token

    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', authData.access_token)
      localStorage.setItem('refresh_token', authData.refresh_token)
    }

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

        // Save to localStorage
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('auth_token', data.access_token)
          localStorage.setItem('refresh_token', data.refresh_token)

          // Also update user data if returned
          if (data.user) {
            user.value = data.user
            localStorage.setItem('user', JSON.stringify(data.user))
          }
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
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    const fullUrl = url.startsWith('http') ? url : `${backendUrl}${url}`

    // Add auth header if token exists
    const headers = {
      ...options.headers,
      ...(token.value ? { 'Authorization': `Bearer ${token.value}` } : {})
    }

    let response = await fetch(fullUrl, { ...options, headers })

    // If 401, try to refresh token and retry once
    if (response.status === 401 && token.value) {
      const refreshed = await refreshAccessToken()
      if (refreshed) {
        // Retry with new token
        const newHeaders = {
          ...options.headers,
          'Authorization': `Bearer ${token.value}`
        }
        response = await fetch(fullUrl, { ...options, headers: newHeaders })
      }
    }

    return response
  }

  function logout() {
    console.log('[Auth] Logging out user')
    user.value = null
    token.value = null
    refreshToken.value = null

    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      console.log('[Auth] LocalStorage cleared')
    }
    console.log('[Auth] Logout complete')
    
    // Also reset any UI state that might be showing user info
    // This helps ensure UI updates properly after logout
    const uiStore = useUIStore()
    // You could add a method to reset UI state if needed
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
        localStorage.setItem('auth_token', urlToken)

        // Clear URL parameters
        const newUrl = window.location.pathname
        window.history.replaceState({}, '', newUrl)

        // Fetch user info with the token
        fetchUserWithToken(urlToken)
        return
      } else {
        // Check localStorage for existing tokens
        const storedToken = localStorage.getItem('auth_token')
        const storedRefreshToken = localStorage.getItem('refresh_token')
        const storedUser = localStorage.getItem('user')

        if (storedToken && storedUser) {
          try {
            token.value = storedToken
            refreshToken.value = storedRefreshToken
            user.value = JSON.parse(storedUser)
          } catch (err) {
            console.error('Failed to parse stored user:', err)
            localStorage.removeItem('auth_token')
            localStorage.removeItem('refresh_token')
            localStorage.removeItem('user')
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
        localStorage.setItem('user', JSON.stringify(userData))
      } else {
        console.error('Failed to fetch user with token')
        localStorage.removeItem('auth_token')
      }
    } catch (err) {
      console.error('Error fetching user:', err)
      localStorage.removeItem('auth_token')
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
        user.value = await response.json()
        if (typeof window !== 'undefined') {
          localStorage.setItem('user', JSON.stringify(user.value))
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
      throw new Error('Not authenticated')
    }

    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    const fullUrl = url.startsWith('http') ? url : `${backendUrl}${url}`

    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token.value}`,
      ...options.headers
    }

    let response = await fetch(fullUrl, {
      ...options,
      headers
    })

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
        response = await fetch(fullUrl, {
          ...options,
          headers: newHeaders
        })

        // If still 401 after refresh, token is invalid
        if (response.status === 401) {
          logout()
          throw new Error('Session expired. Please login again.')
        }
      } else {
        // Refresh failed, logout
        logout()
        throw new Error('Session expired. Please login again.')
      }
    }

    return response
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
    logout,
    initializeAuth,
    refreshUser,
    authenticatedFetch,
    refreshAccessToken,
    fetchWithAuth,
    handleAuthResponse
  }
})