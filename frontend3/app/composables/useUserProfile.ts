import { ref, computed } from 'vue'
import type { User, UserStats } from '~/types/user-types'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

interface UseUserProfileOptions {
  userId?: string | number
  autoFetch?: boolean
}

/**
 * Composable für die Verwaltung von Benutzerprofilen
 * 
 * @example
 * ```typescript
 * const { user, loading, error, fetchUser } = useUserProfile({ userId: 123 })
 * 
 * // Benutzer automatisch laden
 * onMounted(() => {
 *   fetchUser()
 * })
 * ```
 */
export function useUserProfile(options: UseUserProfileOptions = {}) {
  const { userId, autoFetch = true } = options

  // Stores
  const authStore = useAuthStore()
  const uiStore = useUIStore()

  // State
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)
  const stats = ref<UserStats | null>(null)

  // Computed properties
  const isCurrentUser = computed(() => {
    // Hier sollte die Logik zur Überprüfung des aktuellen Benutzers implementiert werden
    // Zum Beispiel: Vergleich mit dem aktuell eingeloggten Benutzer
    return false
  })

  const fullName = computed(() => {
    if (!user.value) return ''
    return user.value.name || user.value.username
  })

  const initials = computed(() => {
    if (!user.value) return ''
    const name = user.value.name || user.value.username
    return name.substring(0, 2).toUpperCase()
  })

  const profileCompletion = computed(() => {
    if (!user.value) return 0
    
    const fields = [
      user.value.name,
      user.value.email,
      user.value.avatar_url,
      user.value.bio,
      user.value.location,
      user.value.company
    ]
    
    const filledFields = fields.filter(field => field && field.trim().length > 0).length
    return Math.round((filledFields / fields.length) * 100)
  })

  // Helper: Transform API user to frontend User interface
  const transformApiUser = (apiUser: any): User => ({
    id: apiUser.id,
    username: apiUser.username,
    email: apiUser.email,
    name: apiUser.name,
    avatar_url: apiUser.avatar_url,
    bio: apiUser.bio,
    location: apiUser.location,
    company: apiUser.company,
    github_id: apiUser.github_id,
    google_id: apiUser.google_id,
    email_verified: apiUser.email_verified,
    auth_method: apiUser.auth_method,
    last_login: apiUser.last_login,
    created_at: apiUser.created_at,
    updated_at: apiUser.updated_at
  })

  // Helper: Transform API stats to frontend UserStats interface
  const transformApiStats = (apiStats: any): UserStats => ({
    hackathonsCreated: apiStats.hackathonsCreated || 0,
    projectsSubmitted: apiStats.projectsSubmitted || 0,
    totalVotes: apiStats.totalVotes || 0,
    // Optionale Felder können hier gemappt werden, falls vorhanden
    teamCount: apiStats.teamCount,
    commentCount: apiStats.commentCount,
    followerCount: apiStats.followerCount,
    followingCount: apiStats.followingCount,
    averageRating: apiStats.averageRating,
    totalPoints: apiStats.totalPoints
  })

  // Methods
  const fetchUser = async (id?: string | number) => {
    const targetId = id || userId
    if (!targetId) {
      error.value = new Error('Keine Benutzer-ID angegeben')
      return
    }

    loading.value = true
    error.value = null

    try {
      // API-Aufruf für Benutzerdaten
      const userResponse = await authStore.fetchWithAuth(`/api/users/${targetId}`)
      
      if (!userResponse.ok) {
        throw new Error(`API-Fehler: ${userResponse.status} ${userResponse.statusText}`)
      }

      const userData = await userResponse.json()
      
      // Check if response has the expected structure
      if (!userData || typeof userData !== 'object') {
        throw new Error('Ungültige API-Antwort: Keine Benutzerdaten erhalten')
      }
      
      // Handle authentication error
      if (userData.detail === 'Not authenticated') {
        throw new Error('401: Nicht authentifiziert')
      }

      // Transform API response to User interface
      user.value = transformApiUser(userData)

      // API-Aufruf für Statistiken (falls verfügbar)
      try {
        const statsResponse = await authStore.fetchWithAuth(`/api/users/${targetId}/stats`)
        if (statsResponse.ok) {
          const statsData = await statsResponse.json()
          stats.value = transformApiStats(statsData)
        } else {
          // Falls kein Stats-Endpoint, leere Stats verwenden
          stats.value = {
            hackathonsCreated: 0,
            projectsSubmitted: 0,
            totalVotes: 0
          }
        }
      } catch (statsErr) {
        // Stats sind optional, Fehler ignorieren
        console.warn('Stats konnten nicht geladen werden:', statsErr)
        stats.value = {
          hackathonsCreated: 0,
          projectsSubmitted: 0,
          totalVotes: 0
        }
      }
    } catch (err) {
      // Spezifische Fehlerbehandlung basierend auf Fehlertyp
      if (err instanceof Error && err.message.includes('401')) {
        const errorMsg = 'Nicht authentifiziert. Bitte melden Sie sich an, um Benutzerdaten zu sehen.'
        error.value = new Error(errorMsg)
        uiStore.showError('Authentifizierungsfehler', errorMsg)
      } else if (err instanceof Error && err.message.includes('403')) {
        const errorMsg = 'Zugriff verweigert. Sie haben keine Berechtigung, diesen Benutzer abzurufen.'
        error.value = new Error(errorMsg)
        uiStore.showError('Zugriffsfehler', errorMsg)
      } else if (err instanceof Error && err.message.includes('404')) {
        const errorMsg = 'Benutzer nicht gefunden.'
        error.value = new Error(errorMsg)
        uiStore.showError('Nicht gefunden', errorMsg)
      } else if (err instanceof Error && err.message.includes('500')) {
        const errorMsg = 'Serverfehler. Bitte versuchen Sie es später erneut.'
        error.value = new Error(errorMsg)
        uiStore.showError('Serverfehler', errorMsg)
      } else {
        const errorMsg = err instanceof Error ? err.message : 'Fehler beim Abrufen des Benutzers'
        error.value = err instanceof Error ? err : new Error(errorMsg)
        uiStore.showError('Fehler beim Laden', errorMsg)
      }
      console.error('Fehler beim Laden des Benutzers:', err)
    } finally {
      loading.value = false
    }
  }

  const updateUser = async (updates: Partial<User>) => {
    if (!user.value) {
      error.value = new Error('Kein Benutzer zum Aktualisieren')
      return false
    }

    loading.value = true
    error.value = null

    try {
      // API-Aufruf für Update
      const response = await authStore.fetchWithAuth(`/api/users/${user.value.id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updates)
      })
      
      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      const updatedData = await response.json()
      user.value = transformApiUser(updatedData)
      return true
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Aktualisieren des Benutzers')
      uiStore.showError('Fehler beim Aktualisieren', 'Das Profil konnte nicht aktualisiert werden.')
      console.error('Fehler beim Aktualisieren des Benutzers:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  const uploadAvatar = async (file: File) => {
    if (!user.value) {
      error.value = new Error('Kein Benutzer zum Aktualisieren')
      return false
    }

    loading.value = true
    error.value = null

    try {
      const formData = new FormData()
      formData.append('avatar', file)
      
      const response = await authStore.fetchWithAuth(`/api/users/${user.value.id}/avatar`, {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      user.value.avatar_url = data.avatar_url
      return true
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Hochladen des Avatars')
      uiStore.showError('Fehler beim Hochladen', 'Der Avatar konnte nicht hochgeladen werden.')
      console.error('Fehler beim Hochladen des Avatars:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    user.value = null
    stats.value = null
    loading.value = false
    error.value = null
  }

  // Auto-fetch wenn gewünscht
  if (autoFetch && userId) {
    fetchUser()
  }

  return {
    // State
    user,
    loading,
    error,
    stats,

    // Computed
    isCurrentUser,
    fullName,
    initials,
    profileCompletion,

    // Methods
    fetchUser,
    updateUser,
    uploadAvatar,
    reset
  }
}

/**
 * Composable für die Verwaltung der aktuellen Benutzer-Session
 * 
 * @example
 * ```typescript
 * const { currentUser, isAuthenticated, logout } = useCurrentUser()
 * ```
 */
export function useCurrentUser() {
  const authStore = useAuthStore()
  const uiStore = useUIStore()
  const currentUser = ref<User | null>(null)
  const isAuthenticated = computed(() => !!currentUser.value)

  const transformApiUser = (apiUser: any): User => ({
    id: apiUser.id,
    username: apiUser.username,
    email: apiUser.email,
    name: apiUser.name,
    avatar_url: apiUser.avatar_url,
    bio: apiUser.bio,
    location: apiUser.location,
    company: apiUser.company,
    github_id: apiUser.github_id,
    google_id: apiUser.google_id,
    email_verified: apiUser.email_verified,
    auth_method: apiUser.auth_method,
    last_login: apiUser.last_login,
    created_at: apiUser.created_at,
    updated_at: apiUser.updated_at
  })

  const fetchCurrentUser = async () => {
    try {
      const response = await authStore.fetchWithAuth('/api/users/me')
      
      if (!response.ok) {
        throw new Error(`API-Fehler: ${response.status} ${response.statusText}`)
      }

      const userData = await response.json()
      
      if (!userData || typeof userData !== 'object') {
        throw new Error('Ungültige API-Antwort: Keine Benutzerdaten erhalten')
      }
      
      if (userData.detail === 'Not authenticated') {
        throw new Error('401: Nicht authentifiziert')
      }

      currentUser.value = transformApiUser(userData)
    } catch (err) {
      console.error('Fehler beim Laden des aktuellen Benutzers:', err)
      currentUser.value = null
      
      if (err instanceof Error && err.message.includes('401')) {
        uiStore.showWarning('Nicht authentifiziert', 'Bitte melden Sie sich an, um auf Ihr Profil zuzugreifen.')
      }
    }
  }

  const logout = async () => {
    try {
      await authStore.fetchWithAuth('/api/auth/logout', { method: 'POST' })
      currentUser.value = null
      return true
    } catch (err) {
      console.error('Fehler beim Logout:', err)
      return false
    }
  }

  return {
    currentUser,
    isAuthenticated,
    fetchCurrentUser,
    logout
  }
}
