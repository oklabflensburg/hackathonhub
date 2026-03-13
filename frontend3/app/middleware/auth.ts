// Main middleware function
const authMiddlewareFunction = defineNuxtRouteMiddleware(async (to, from) => {
  // With cookie-based authentication, we can now check auth state on server
  // without causing hydration mismatches
  
  // Define routes that should be inaccessible when authenticated
  const authRoutes = ['/login', '/register']
  
  // Protect authenticated routes (redirect unauthenticated users to login)
  const protectedRoutes = [
    '/profile',
    '/my-projects', 
    '/my-votes',
    '/create',
    '/teams/create',
    '/teams/invitations',
    '/teams/*/edit',
    '/projects/create',
    '/projects/*/edit',
    '/projects/*/vote',
    '/hackathons/*/register'
  ]

  // Check if the route is protected (exact match or starts with protected route)
  const isProtected = protectedRoutes.some(route => {
    if (route.includes('*')) {
      // Convert wildcard route to regex pattern
      const pattern = route.replace(/\*/g, '[^/]+')
      const regex = new RegExp(`^${pattern}$`)
      return regex.test(to.path)
    }
    return to.path === route || to.path.startsWith(route + '/')
  })

  // Server-side: check cookies for authentication
  if (process.server) {
    // Use useCookie to check for auth token
    const authToken = useCookie('auth_token')
    const hasAuthToken = !!authToken.value
    
    // If user is authenticated and trying to access auth routes, redirect to home
    if (hasAuthToken && authRoutes.includes(to.path)) {
      return navigateTo('/')
    }
    
    // Protect authenticated routes (redirect unauthenticated users to login)
    if (!hasAuthToken && isProtected) {
      return navigateTo('/login')
    }
    
    // If we have auth token but not authenticated in store yet, 
    // let client-side handle initialization
    return
  }
  
  // Client-side: use auth store to check authentication
  const authStore = useAuthStore()
  await authStore.initializeAuth()
  
  const isAuthenticated = authStore.isAuthenticated

  // If user is authenticated and trying to access auth routes, redirect to home
  if (isAuthenticated && authRoutes.includes(to.path)) {
    return navigateTo('/')
  }
  
  // Protect authenticated routes (redirect unauthenticated users to login)
  if (!isAuthenticated && isProtected) {
    return navigateTo('/login')
  }
})

// Default export for named middleware (can be referenced as 'auth' in definePageMeta)
export default authMiddlewareFunction

// Named export for direct import
export const authMiddleware = authMiddlewareFunction
