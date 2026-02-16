import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
  id: number
  github_id: string
  username: string
  avatar_url: string
  email?: string
  created_at: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
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

  async function refreshToken(): Promise<boolean> {
    if (!token.value) return false
    
    try {
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'
      
      const response = await fetch(`${backendUrl}/api/auth/refresh`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        token.value = data.access_token
        // Save to localStorage
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('auth_token', data.access_token)
        }
        return true
      } else {
        // Refresh failed, logout
        logout()
        return false
      }
    } catch (err) {
      console.error('Token refresh error:', err)
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
      const refreshed = await refreshToken()
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


  async function logout() {
    user.value = null
    token.value = null
    
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
    }
  }

  function initializeAuth() {
    if (typeof window === 'undefined') return
    
    // Check for token in URL (from OAuth callback)
    const urlParams = new URLSearchParams(window.location.search)
    const urlToken = urlParams.get('token')
    const source = urlParams.get('source')
    
    if (urlToken && source === 'github') {
      // Store token from URL
      token.value = urlToken
      localStorage.setItem('auth_token', urlToken)
      
      // Clear URL parameters
      const newUrl = window.location.pathname
      window.history.replaceState({}, '', newUrl)
      
      // Fetch user info with the token
      fetchUserWithToken(urlToken)
    } else {
      // Check localStorage for existing token
      const storedToken = localStorage.getItem('auth_token')
      const storedUser = localStorage.getItem('user')
      
      if (storedToken && storedUser) {
        try {
          token.value = storedToken
          user.value = JSON.parse(storedUser)
        } catch (err) {
          console.error('Failed to parse stored user:', err)
          localStorage.removeItem('auth_token')
          localStorage.removeItem('user')
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
    
    const response = await fetch(fullUrl, {
      ...options,
      headers
    })
    
    // Check for token expiration - MUST check before returning response
    if (response.status === 401) {
      // Clear auth and throw specific error
      logout()
      throw new Error('Session expired. Please login again.')
    }
    
    return response
  }

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    userInitials,
    loginWithGitHub,
    logout,
    initializeAuth,
    refreshUser,
    authenticatedFetch,
    refreshToken,
    fetchWithAuth
  }
})