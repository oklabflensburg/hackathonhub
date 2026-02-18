// Main middleware function
const authMiddlewareFunction = defineNuxtRouteMiddleware((to, from) => {
  // Skip middleware on server-side for auth checks (to avoid hydration mismatches)
  // We'll handle authenticated → auth routes redirect in onMounted hooks
  // But we still need to protect authenticated routes for unauthenticated users
  if (process.server) {
    return
  }
  
  const authStore = useAuthStore()
  
  // Initialize auth store if not already initialized
  authStore.initializeAuth()
  
  // Check if user is authenticated
  const isAuthenticated = authStore.isAuthenticated
  
  // Protect authenticated routes (redirect unauthenticated users to login)
  const protectedRoutes = ['/profile', '/my-projects', '/my-votes', '/create']
  
  if (!isAuthenticated && protectedRoutes.includes(to.path)) {
    return navigateTo('/login')
  }
  
  // Note: We're NOT redirecting authenticated users away from auth routes here
  // to avoid hydration mismatches. This is handled in page components.
})

// Default export for named middleware (can be referenced as 'auth' in definePageMeta)
export default authMiddlewareFunction

// Named export for direct import
export const authMiddleware = authMiddlewareFunction