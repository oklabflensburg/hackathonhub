// Main middleware function
const authMiddlewareFunction = defineNuxtRouteMiddleware((to, from) => {
  // Skip middleware on server-side
  if (process.server) {
    return
  }
  
  const authStore = useAuthStore()
  
  // Initialize auth store if not already initialized
  // This ensures we check localStorage for existing tokens
  authStore.initializeAuth()
  
  // Check if user is authenticated
  const isAuthenticated = authStore.isAuthenticated
  
  // Define routes that should be inaccessible when authenticated
  const authRoutes = ['/login', '/register']
  
  // If user is authenticated and trying to access auth routes, redirect to home
  if (isAuthenticated && authRoutes.includes(to.path)) {
    return navigateTo('/')
  }
  
  // Optional: If user is not authenticated and trying to access protected routes
  // This can be expanded later for other protected routes
  const protectedRoutes = ['/profile', '/my-projects', '/my-votes', '/create']
  
  if (!isAuthenticated && protectedRoutes.includes(to.path)) {
    return navigateTo('/login')
  }
})

// Default export for named middleware (can be referenced as 'auth' in definePageMeta)
export default authMiddlewareFunction

// Named export for direct import
export const authMiddleware = authMiddlewareFunction