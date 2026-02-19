/**
 * Global fetch wrapper with automatic token refresh
 * This plugin intercepts all fetch calls and adds authentication headers
 * with automatic token refresh on 401 responses
 */

// Plugin to install the auth fetch wrapper
export default defineNuxtPlugin((nuxtApp) => {
  // Only override fetch on client side
  if (process.client) {
    // Store the original fetch function
    const originalFetch = globalThis.fetch
    const authStore = useAuthStore()
    
    // Create a wrapper function that handles token refresh
    const authFetch = async function(input: RequestInfo | URL, init?: RequestInit): Promise<Response> {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'
      
      // Convert input to string for URL checking
      const url = typeof input === 'string' ? input : input instanceof URL ? input.toString() : input.url
      
      // Check if this is an API call to our backend
      const isApiCall = url.startsWith(backendUrl) || url.startsWith('/api/')
      
      if (!isApiCall) {
        // For non-API calls, use original fetch
        return originalFetch(input, init)
      }
      
      // Prepare headers
      const headers = new Headers(init?.headers || {})
      
      // Add auth header if we have a token
      if (authStore.token) {
        headers.set('Authorization', `Bearer ${authStore.token}`)
      }
      
      // Add content type if not present
      if (!headers.has('Content-Type') && init?.method && ['POST', 'PUT', 'PATCH'].includes(init.method)) {
        headers.set('Content-Type', 'application/json')
      }
      
      // Make the request
      const requestInit: RequestInit = {
        ...init,
        headers
      }
      
      let response = await originalFetch(input, requestInit)
      
      // Handle token expiration for authenticated requests
      if (response.status === 401 && authStore.token && isApiCall) {
        // Try to refresh the token
        const refreshed = await authStore.refreshAccessToken()
        
        if (refreshed) {
          // Update the auth header with new token
          headers.set('Authorization', `Bearer ${authStore.token}`)
          
          // Retry the request
          const retryInit: RequestInit = {
            ...init,
            headers
          }
          
          response = await originalFetch(input, retryInit)
        } else {
          // Refresh failed - the user will be logged out by refreshAccessToken
          console.warn('Token refresh failed, user logged out')
          
          // Log current auth state for debugging
          console.log('[AuthFetch] Current auth state after refresh failure:', {
            user: authStore.user,
            token: authStore.token ? 'present' : 'null',
            refreshToken: authStore.refreshToken ? 'present' : 'null',
            isAuthenticated: authStore.isAuthenticated
          })
        }
      }
      
      return response
    }
    
    // Override global fetch
    globalThis.fetch = authFetch
    
    // Provide a way to access the original fetch if needed
    return {
      provide: {
        originalFetch
      }
    }
  }
  
  return {
    provide: {
      originalFetch: globalThis.fetch
    }
  }
})