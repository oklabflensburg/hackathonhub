/**
 * Projects Composable
 * Bietet eine konsistente Schnittstelle für alle Projekt-Operationen
 * Kapselt API-Aufrufe und bietet reaktiven State, Loading-States und Error-Handling
 * 
 * Migriert zur Verwendung zentraler Typ-Definitionen (project-types.ts)
 */

import { ref, computed } from 'vue'
import { useApiClient } from '~/utils/api-client'
import { useUIStore } from '~/stores/ui'
import type { 
  Project, 
  ProjectCreateData, 
  ProjectUpdateData,
  ProjectStatus,
  ProjectVisibility,
  ProjectFilterOptions,
  ProjectSortOption,
  ProjectListResponse,
  ProjectStats,
  ProjectVote,
  ProjectComment,
  VoteStats,
  VoteData,
  UseProjectsReturn
} from '~/types/project-types'
import { snakeToCamel, mapApiProjectToProject, mapPaginatedResponse, idToNumber, idToString } from '~/utils/api-mappers'

export interface UseProjectsOptions {
  /** Automatisches Error-Handling (Notifications) */
  autoErrorHandling?: boolean
  /** Automatisches Success-Handling (Notifications) */
  autoSuccessHandling?: boolean
  /** Initiale Projekt-ID für Single-Project-Operationen */
  initialProjectId?: string
}

/**
 * Projects Composable
 */
export function useProjects(options: UseProjectsOptions = {}): UseProjectsReturn {
  const {
    autoErrorHandling = true,
    autoSuccessHandling = true,
    initialProjectId
  } = options

  // Stores und Services
  const uiStore = useUIStore()
  const apiClient = useApiClient()

  // State
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const projectVoteStats = ref<Record<string, VoteStats>>({})

  // Computed Properties
  const hasProjects = computed(() => projects.value.length > 0)
  const projectCount = computed(() => projects.value.length)

  /**
   * Alle Projekte abrufen
   */
  async function fetchProjects(filters?: {
    hackathonId?: string
    teamId?: string
    userId?: string
    status?: string
    search?: string
    limit?: number
    offset?: number
  }): Promise<Project[]> {
    try {
      isLoading.value = true
      error.value = null

      const queryParams = new URLSearchParams()
      if (filters?.hackathonId) queryParams.append('hackathon_id', idToNumber(filters.hackathonId).toString())
      if (filters?.teamId) queryParams.append('team_id', idToNumber(filters.teamId).toString())
      if (filters?.userId) queryParams.append('user_id', idToNumber(filters.userId).toString())
      if (filters?.status) queryParams.append('status', filters.status)
      if (filters?.search) queryParams.append('search', filters.search)
      if (filters?.limit) queryParams.append('limit', filters.limit.toString())
      if (filters?.offset) queryParams.append('offset', filters.offset.toString())

      const url = `/api/projects${queryParams.toString() ? `?${queryParams.toString()}` : ''}`
      const response = await apiClient.get<any[]>(url)

      // API-Response zu Frontend-Typen mappen
      const mappedProjects = response.map(mapApiProjectToProject)
      projects.value = mappedProjects
      return mappedProjects
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Abrufen der Projekte'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Projekte Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Einzelnes Projekt abrufen
   */
  async function fetchProject(projectId: string): Promise<Project> {
    try {
      isLoading.value = true
      error.value = null

      const numericId = idToNumber(projectId)
      const response = await apiClient.get<any>(`/api/projects/${numericId}`)
      
      // API-Response zu Frontend-Typ mappen
      const mappedProject = mapApiProjectToProject(response)
      currentProject.value = mappedProject

      // View-Count inkrementieren
      await incrementViewCount(projectId)

      return mappedProject
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Abrufen des Projekts'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Projekt Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Projekt erstellen
   */
  async function createProject(projectData: ProjectCreateData): Promise<Project> {
    try {
      isLoading.value = true
      error.value = null

      // Frontend-Typ zu API-Payload mappen (camelCase → snake_case, string → number IDs)
      const apiPayload = {
        title: projectData.title,
        description: projectData.description,
        repository_url: projectData.repositoryUrl,
        live_url: projectData.liveUrl,
        technologies: projectData.technologies,
        status: projectData.status,
        is_public: projectData.isPublic,
        hackathon_id: projectData.hackathonId ? idToNumber(projectData.hackathonId) : undefined,
        team_id: projectData.teamId ? idToNumber(projectData.teamId) : undefined,
        image_path: projectData.imagePath
      }

      const response = await apiClient.post<any>('/api/projects', apiPayload, {
        skipErrorNotification: true // Wir behandeln Errors selbst
      })

      // API-Response zu Frontend-Typ mappen
      const mappedProject = mapApiProjectToProject(response)

      // Zum lokalen State hinzufügen
      projects.value = [mappedProject, ...projects.value]
      currentProject.value = mappedProject

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Projekt erfolgreich erstellt', 'Projekt')
      }

      return mappedProject
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Erstellen des Projekts'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Projekt Erstellung Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Projekt aktualisieren
   */
  async function updateProject(projectId: string, projectData: ProjectUpdateData): Promise<Project> {
    try {
      isLoading.value = true
      error.value = null

      const numericId = idToNumber(projectId)
      
      // Frontend-Typ zu API-Payload mappen
      const apiPayload = {
        title: projectData.title,
        description: projectData.description,
        repository_url: projectData.repositoryUrl,
        live_url: projectData.liveUrl,
        technologies: projectData.technologies,
        status: projectData.status,
        is_public: projectData.isPublic,
        hackathon_id: projectData.hackathonId ? idToNumber(projectData.hackathonId) : undefined,
        team_id: projectData.teamId ? idToNumber(projectData.teamId) : undefined,
        image_path: projectData.imagePath
      }

      const response = await apiClient.put<any>(`/api/projects/${numericId}`, apiPayload, {
        skipErrorNotification: true
      })

      // API-Response zu Frontend-Typ mappen
      const mappedProject = mapApiProjectToProject(response)

      // Lokalen State aktualisieren
      if (currentProject.value?.id === projectId) {
        currentProject.value = mappedProject
      }

      // In der Projekte-Liste aktualisieren
      const index = projects.value.findIndex(p => p.id === projectId)
      if (index !== -1) {
        projects.value[index] = mappedProject
      }

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Projekt erfolgreich aktualisiert', 'Projekt')
      }

      return mappedProject
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Aktualisieren des Projekts'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Projekt Update Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Projekt löschen
   */
  async function deleteProject(projectId: string): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      const numericId = idToNumber(projectId)
      await apiClient.delete(`/api/projects/${numericId}`, {
        skipErrorNotification: true
      })

      // Aus lokalem State entfernen
      projects.value = projects.value.filter(p => p.id !== projectId)
      if (currentProject.value?.id === projectId) {
        currentProject.value = null
      }

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Projekt erfolgreich gelöscht', 'Projekt')
      }
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Löschen des Projekts'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Projekt Löschung Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Für Projekt voten
   */
  async function voteForProject(projectId: string, voteType: 'upvote' | 'downvote'): Promise<void> {
    try {
      error.value = null

      const numericId = idToNumber(projectId)
      await apiClient.post(`/api/projects/${numericId}/vote`, {
        vote_type: voteType
      }, {
        skipErrorNotification: true
      })

      // Vote-Stats aktualisieren
      await fetchVoteStats(projectId)

      // Success Notification
      if (autoSuccessHandling) {
        const message = voteType === 'upvote' ? 'Upvote erfolgreich' : 'Downvote erfolgreich'
        uiStore.showSuccess(message, 'Vote')
      }
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Voten'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Vote Fehler')
      }
      
      throw err
    }
  }

  /**
   * Vote entfernen
   */
  async function removeVote(projectId: string): Promise<void> {
    try {
      error.value = null

      const numericId = idToNumber(projectId)
      await apiClient.delete(`/api/projects/${numericId}/vote`, {
        skipErrorNotification: true
      })

      // Vote-Stats aktualisieren
      await fetchVoteStats(projectId)

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Vote erfolgreich entfernt', 'Vote')
      }
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Entfernen des Votes'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Vote Entfernung Fehler')
      }
      
      throw err
    }
  }

  /**
   * Vote-Statistiken abrufen
   */
  async function fetchVoteStats(projectId: string): Promise<VoteStats> {
    try {
      const numericId = idToNumber(projectId)
      const response = await apiClient.get<any>(`/api/projects/${numericId}/vote-stats`)
      
      // API-Response zu Frontend-Typ mappen (snake_case → camelCase)
      const mappedStats = snakeToCamel(response) as VoteStats
      projectVoteStats.value[projectId] = mappedStats
      return mappedStats
    } catch (err: any) {
      console.error('Fehler beim Abrufen der Vote-Statistiken:', err)
      throw err
    }
  }

  /**
   * View-Count inkrementieren
   */
  async function incrementViewCount(projectId: string): Promise<void> {
    try {
      const numericId = idToNumber(projectId)
      await apiClient.post(`/api/projects/${numericId}/view`, {}, {
        skipErrorNotification: true
      })
    } catch (err: any) {
      // View-Count-Fehler sind nicht kritisch, nur loggen
      console.warn('Fehler beim Inkrementieren des View-Counts:', err)
    }
  }

  /**
   * Error zurücksetzen
   */
  function clearError(): void {
    error.value = null
  }

  /**
   * Loading-State zurücksetzen
   */
  function clearLoading(): void {
    isLoading.value = false
  }

  /**
   * Composable zurücksetzen
   */
  function reset(): void {
    isLoading.value = false
    error.value = null
    projects.value = []
    currentProject.value = null
    projectVoteStats.value = {}
  }

  return {
    // State
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    projects: computed(() => projects.value),
    currentProject: computed(() => currentProject.value),
    projectVoteStats: computed(() => projectVoteStats.value),
    
    // Computed
    hasProjects,
    projectCount,
    
    // Methods
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
    voteForProject,
    removeVote,
    fetchVoteStats,
    incrementViewCount,
    
    // Utilities
    clearError,
    clearLoading,
    reset
  }
}
