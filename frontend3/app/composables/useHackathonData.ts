import { ref, computed } from 'vue'
import type { Hackathon } from '~/types/hackathon-types'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

interface UseHackathonDataOptions {
  hackathonId?: string | number
  autoFetch?: boolean
}

/**
 * Composable für die Verwaltung von Hackathon-Daten
 * 
 * @example
 * ```typescript
 * const { hackathon, loading, error, participants, projects } = useHackathonData({ hackathonId: 123 })
 * ```
 */
export function useHackathonData(options: UseHackathonDataOptions = {}) {
  const { hackathonId, autoFetch = true } = options

  // Stores
  const authStore = useAuthStore()
  const uiStore = useUIStore()

  // State
  const hackathon = ref<Hackathon | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)
  const participants = ref<any[]>([])
  const projects = ref<any[]>([])
  const teams = ref<any[]>([])

  // Computed properties
  const isUpcoming = computed(() => {
    if (!hackathon.value) return false
    return hackathon.value.status === 'upcoming'
  })

  const isActive = computed(() => {
    if (!hackathon.value) return false
    return hackathon.value.status === 'active'
  })

  const isCompleted = computed(() => {
    if (!hackathon.value) return false
    return hackathon.value.status === 'completed'
  })

  const daysRemaining = computed(() => {
    if (!hackathon.value || !isUpcoming.value) return 0
    
    const startDate = new Date(hackathon.value.start_date)
    const today = new Date()
    const diffTime = startDate.getTime() - today.getTime()
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  })

  const daysActive = computed(() => {
    if (!hackathon.value || !isActive.value) return 0
    
    const startDate = new Date(hackathon.value.start_date)
    const today = new Date()
    const diffTime = today.getTime() - startDate.getTime()
    return Math.floor(diffTime / (1000 * 60 * 60 * 24))
  })

  const totalDays = computed(() => {
    if (!hackathon.value) return 0
    
    const startDate = new Date(hackathon.value.start_date)
    const endDate = new Date(hackathon.value.end_date)
    const diffTime = endDate.getTime() - startDate.getTime()
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  })

  const progressPercentage = computed(() => {
    if (!hackathon.value) return 0
    
    if (isUpcoming.value) return 0
    if (isCompleted.value) return 100
    
    const startDate = new Date(hackathon.value.start_date)
    const endDate = new Date(hackathon.value.end_date)
    const today = new Date()
    
    const totalDuration = endDate.getTime() - startDate.getTime()
    const elapsedDuration = today.getTime() - startDate.getTime()
    
    return Math.min(100, Math.max(0, (elapsedDuration / totalDuration) * 100))
  })

  const registrationOpen = computed(() => {
    if (!hackathon.value) return false
    
    if (hackathon.value.registration_deadline) {
      const deadline = new Date(hackathon.value.registration_deadline)
      const today = new Date()
      return today < deadline
    }
    
    return isUpcoming.value
  })

  const prizePoolTotal = computed(() => {
    if (!hackathon.value?.prizes?.length) return '0'
    
    // Versuche, den Wert aus dem prize_pool Feld zu extrahieren
    if (hackathon.value.prize_pool) {
      return hackathon.value.prize_pool
    }
    
    // Fallback: Summiere alle Preise
    const total = hackathon.value.prizes.reduce((sum, prize) => {
      const value = parseFloat(prize.value.replace(/[^0-9.]/g, '')) || 0
      return sum + value
    }, 0)
    
    return `$${total.toLocaleString()}`
  })

  // Helper function to transform API response to Hackathon type
  const transformApiHackathon = (apiHackathon: any): Hackathon => {
    return {
      id: apiHackathon.id,
      name: apiHackathon.name,
      description: apiHackathon.description,
      start_date: apiHackathon.start_date,
      end_date: apiHackathon.end_date,
      location: apiHackathon.location,
      image_url: apiHackathon.image_url,
      status: apiHackathon.status,
      is_active: apiHackathon.is_active,
      participant_count: apiHackathon.participant_count,
      view_count: apiHackathon.view_count,
      project_count: apiHackathon.project_count,
      registration_deadline: apiHackathon.registration_deadline,
      prizes: apiHackathon.prizes || [],
      rules: apiHackathon.rules,
      organizers: apiHackathon.organizers || [],
      prize_pool: apiHackathon.prize_pool,
      created_at: apiHackathon.created_at,
      updated_at: apiHackathon.updated_at
    }
  }

  // Methods
  const fetchHackathon = async (id?: string | number) => {
    const targetId = id || hackathonId
    if (!targetId) {
      error.value = new Error('Keine Hackathon-ID angegeben')
      return
    }

    loading.value = true
    error.value = null

    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${targetId}`)
      if (!response.ok) {
        throw new Error(`Failed to fetch hackathon: ${response.status}`)
      }
      const data = await response.json()
      hackathon.value = transformApiHackathon(data)

      // Optionally fetch participants, projects, teams if needed
      // For now, we'll leave them empty or fetch separately
      participants.value = []
      projects.value = []
      teams.value = []
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Laden des Hackathons')
      console.error('Fehler beim Laden des Hackathons:', err)
      uiStore.showError('Fehler beim Laden des Hackathons')
    } finally {
      loading.value = false
    }
  }

  const fetchParticipants = async (page = 1, pageSize = 20) => {
    if (!hackathonId) return

    loading.value = true
    error.value = null

    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/participants?page=${page}&pageSize=${pageSize}`)
      if (!response.ok) {
        throw new Error(`Failed to fetch participants: ${response.status}`)
      }
      const data = await response.json()
      participants.value = data.participants || []
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Laden der Teilnehmer')
      console.error('Fehler beim Laden der Teilnehmer:', err)
      uiStore.showError('Fehler beim Laden der Teilnehmer')
    } finally {
      loading.value = false
    }
  }

  const fetchProjects = async (page = 1, pageSize = 20) => {
    if (!hackathonId) return

    loading.value = true
    error.value = null

    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/projects?page=${page}&pageSize=${pageSize}`)
      if (!response.ok) {
        throw new Error(`Failed to fetch projects: ${response.status}`)
      }
      const data = await response.json()
      projects.value = data.projects || []
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Laden der Projekte')
      console.error('Fehler beim Laden der Projekte:', err)
      uiStore.showError('Fehler beim Laden der Projekte')
    } finally {
      loading.value = false
    }
  }

  const fetchTeams = async (page = 1, pageSize = 20) => {
    if (!hackathonId) return

    loading.value = true
    error.value = null

    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/teams?page=${page}&pageSize=${pageSize}`)
      if (!response.ok) {
        throw new Error(`Failed to fetch teams: ${response.status}`)
      }
      const data = await response.json()
      teams.value = data.teams || []
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Laden der Teams')
      console.error('Fehler beim Laden der Teams:', err)
      uiStore.showError('Fehler beim Laden der Teams')
    } finally {
      loading.value = false
    }
  }

  const registerForHackathon = async (userId: string | number, teamId?: string | number) => {
    if (!hackathonId) return false

    loading.value = true
    error.value = null

    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, teamId })
      })
      if (!response.ok) {
        throw new Error(`Registration failed: ${response.status}`)
      }
      
      // Update participant count
      if (hackathon.value) {
        hackathon.value.participant_count++
      }
      
      uiStore.showSuccess('Erfolgreich für den Hackathon registriert')
      return true
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler bei der Registrierung')
      console.error('Fehler bei der Registrierung für den Hackathon:', err)
      uiStore.showError('Fehler bei der Registrierung')
      return false
    } finally {
      loading.value = false
    }
  }

  const createTeam = async (teamData: { name: string; description?: string; members?: string[] }) => {
    if (!hackathonId) return null

    loading.value = true
    error.value = null

    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/teams`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(teamData)
      })
      if (!response.ok) {
        throw new Error(`Team creation failed: ${response.status}`)
      }
      const data = await response.json()
      teams.value.push(data.team)
      uiStore.showSuccess('Team erfolgreich erstellt')
      return data.team
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Erstellen des Teams')
      console.error('Fehler beim Erstellen des Teams:', err)
      uiStore.showError('Fehler beim Erstellen des Teams')
      return null
    } finally {
      loading.value = false
    }
  }

  const submitProject = async (projectData: { 
    name: string; 
    description: string; 
    teamId?: string; 
    repositoryUrl?: string;
    demoUrl?: string;
  }) => {
    if (!hackathonId) return null

    loading.value = true
    error.value = null

    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(projectData)
      })
      if (!response.ok) {
        throw new Error(`Project submission failed: ${response.status}`)
      }
      const data = await response.json()
      projects.value.push(data.project)
      if (hackathon.value) {
        hackathon.value.project_count++
      }
      uiStore.showSuccess('Projekt erfolgreich eingereicht')
      return data.project
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Einreichen des Projekts')
      console.error('Fehler beim Einreichen des Projekts:', err)
      uiStore.showError('Fehler beim Einreichen des Projekts')
      return null
    } finally {
      loading.value = false
    }
  }

  const voteForProject = async (projectId: string, userId: string) => {
    if (!hackathonId) return false

    loading.value = true
    error.value = null

    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/projects/${projectId}/vote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId })
      })
      if (!response.ok) {
        throw new Error(`Voting failed: ${response.status}`)
      }
      
      // Update vote count locally
      const project = projects.value.find(p => p.id === projectId)
      if (project) {
        project.votes = (project.votes || 0) + 1
      }
      
      uiStore.showSuccess('Erfolgreich abgestimmt')
      return true
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Abstimmen')
      console.error('Fehler beim Abstimmen für das Projekt:', err)
      uiStore.showError('Fehler beim Abstimmen')
      return false
    } finally {
      loading.value = false
    }
  }

  // Auto-fetch wenn gewünscht
  if (autoFetch && hackathonId) {
    fetchHackathon()
  }

  return {
    // State
    hackathon,
    loading,
    error,
    participants,
    projects,
    teams,
    
    // Computed
    isUpcoming,
    isActive,
    isCompleted,
    daysRemaining,
    daysActive,
    totalDays,
    progressPercentage,
    registrationOpen,
    prizePoolTotal,
    
    // Methods
    fetchHackathon,
    fetchParticipants,
    fetchProjects,
    fetchTeams,
    registerForHackathon,
    createTeam,
    submitProject,
    voteForProject
  }
}