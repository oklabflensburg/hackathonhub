// Main middleware function
const authMiddlewareFunction = defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()
  
  // On server, we can't check localStorage, but we can check cookies
  // For now, we'll initialize auth on both server and client
  // The auth store will handle SSR appropriately
  authStore.initializeAuth()
  
  // Check if user is authenticated
  const isAuthenticated = authStore.isAuthenticated
  
  // Define routes that should be inaccessible when authenticated
  const authRoutes = ['/login', '/register']
  
  // If user is authenticated and trying to access auth routes, redirect to home
  if (isAuthenticated && authRoutes.includes(to.path)) {
    return navigateTo('/')
  }
  
  // Protect authenticated routes (redirect unauthenticated users to login)
  const protectedRoutes = ['/profile', '/my-projects', '/my-votes', '/create']
  
  if (!isAuthenticated && protectedRoutes.includes(to.path)) {
    return navigateTo('/login')
  }
})

// Default export for named middleware (can be referenced as 'auth' in definePageMeta)
export default authMiddlewareFunction

// Named export for direct import
export const authMiddleware = authMiddlewareFunction