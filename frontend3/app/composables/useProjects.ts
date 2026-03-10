import { ref, computed, watch } from 'vue'
import type { Project, ProjectFilterOptions } from '../types/project-types'
import { ProjectSortOption } from '../types/project-types'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

/**
 * Composable für Projekt-bezogene Daten und Logik
 * Bietet Funktionen zum Laden, Filtern, Sortieren und Verwalten von Projekten
 * Verwendet echte API-Aufrufe statt Mock-Daten
 */
export function useProjects() {
  // Stores
  const authStore = useAuthStore()
  const uiStore = useUIStore()

  // State
  const projects = ref<Project[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  // Filter und Sortierung
  const filters = ref<ProjectFilterOptions>({})
  const sortOption = ref<ProjectSortOption>(ProjectSortOption.NEWEST)
  const searchQuery = ref('')
  const currentPage = ref(1)
  const itemsPerPage = ref(12)
  const totalItems = ref(0)
  
  // Computed Properties
  const filteredProjects = computed(() => {
    let result = [...projects.value]
    
    // Search Filter
    if (searchQuery.value.trim()) {
      const query = searchQuery.value.toLowerCase().trim()
      result = result.filter(project =>
        project.title.toLowerCase().includes(query) ||
        project.description.toLowerCase().includes(query) ||
        project.tags?.some(tag => tag.name.toLowerCase().includes(query)) ||
        project.technologies?.some(tech => tech.name.toLowerCase().includes(query))
      )
    }
    
    // Status Filter
    if (filters.value.status && filters.value.status.length > 0) {
      result = result.filter(project =>
        filters.value.status!.includes(project.status)
      )
    }
    
    // Technology Filter
    if (filters.value.technologies && filters.value.technologies.length > 0) {
      result = result.filter(project =>
        project.technologies?.some(tech =>
          filters.value.technologies!.includes(tech.id)
        )
      )
    }
    
    // Tag Filter
    if (filters.value.tags && filters.value.tags.length > 0) {
      result = result.filter(project =>
        project.tags?.some(tag =>
          filters.value.tags!.includes(tag.id)
        )
      )
    }
    
    // Hackathon Filter
    if (filters.value.hackathonId) {
      result = result.filter(project =>
        project.hackathonId === filters.value.hackathonId
      )
    }
    
    // Visibility Filter
    if (filters.value.visibility && filters.value.visibility.length > 0) {
      result = result.filter(project =>
        filters.value.visibility!.includes(project.visibility)
      )
    }
    
    // Bookmarked Filter
    if (filters.value.bookmarked !== undefined) {
      result = result.filter(project =>
        filters.value.bookmarked ? project.isBookmarked : !project.isBookmarked
      )
    }
    
    // Voted Filter
    if (filters.value.voted) {
      result = result.filter(project => {
        if (filters.value.voted === 'upvoted') {
          return project.userVote === 1
        } else if (filters.value.voted === 'downvoted') {
          return project.userVote === -1
        }
        return true
      })
    }
    
    // Team Size Filter
    if (filters.value.teamSize) {
      result = result.filter(project => {
        const teamSize = project.team?.length || 0
        const min = filters.value.teamSize!.min || 0
        const max = filters.value.teamSize!.max || Infinity
        return teamSize >= min && teamSize <= max
      })
    }
    
    // Date Range Filter
    if (filters.value.createdAt) {
      result = result.filter(project => {
        const projectDate = new Date(project.createdAt).getTime()
        const from = filters.value.createdAt!.from
          ? new Date(filters.value.createdAt!.from).getTime()
          : -Infinity
        const to = filters.value.createdAt!.to
          ? new Date(filters.value.createdAt!.to).getTime()
          : Infinity
        return projectDate >= from && projectDate <= to
      })
    }
    
    return result
  })
  
  const sortedProjects = computed(() => {
    const projectsToSort = [...filteredProjects.value]
    
    switch (sortOption.value) {
      case ProjectSortOption.NEWEST:
        return projectsToSort.sort((a, b) =>
          new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
        )
      
      case ProjectSortOption.OLDEST:
        return projectsToSort.sort((a, b) =>
          new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
        )
      
      case ProjectSortOption.MOST_VIEWED:
        return projectsToSort.sort((a, b) =>
          b.stats.views - a.stats.views
        )
      
      case ProjectSortOption.MOST_VOTED:
        return projectsToSort.sort((a, b) =>
          b.stats.votes - a.stats.votes
        )
      
      case ProjectSortOption.MOST_COMMENTED:
        return projectsToSort.sort((a, b) =>
          b.stats.comments - a.stats.comments
        )
      
      case ProjectSortOption.TRENDING:
        // Simple trending algorithm based on recent activity
        return projectsToSort.sort((a, b) => {
          const aScore = calculateTrendingScore(a)
          const bScore = calculateTrendingScore(b)
          return bScore - aScore
        })
      
      case ProjectSortOption.DEADLINE:
        return projectsToSort.sort((a, b) => {
          if (!a.deadline && !b.deadline) return 0
          if (!a.deadline) return 1
          if (!b.deadline) return -1
          return new Date(a.deadline).getTime() - new Date(b.deadline).getTime()
        })
      
      case ProjectSortOption.ALPHABETICAL:
        return projectsToSort.sort((a, b) =>
          a.title.localeCompare(b.title)
        )
      
      default:
        return projectsToSort
    }
  })
  
  const paginatedProjects = computed(() => {
    const startIndex = (currentPage.value - 1) * itemsPerPage.value
    const endIndex = startIndex + itemsPerPage.value
    return sortedProjects.value.slice(startIndex, endIndex)
  })
  
  const totalPages = computed(() => {
    return Math.ceil(sortedProjects.value.length / itemsPerPage.value)
  })
  
  const hasFilters = computed(() => {
    return Object.keys(filters.value).length > 0 || searchQuery.value.trim() !== ''
  })
  
  const activeFilterCount = computed(() => {
    let count = 0
    
    if (searchQuery.value.trim()) count++
    
    if (filters.value.status && filters.value.status.length > 0) {
      count += filters.value.status.length
    }
    
    if (filters.value.technologies && filters.value.technologies.length > 0) {
      count += filters.value.technologies.length
    }
    
    if (filters.value.tags && filters.value.tags.length > 0) {
      count += filters.value.tags.length
    }
    
    if (filters.value.hackathonId) count++
    if (filters.value.visibility && filters.value.visibility.length > 0) count++
    if (filters.value.bookmarked !== undefined) count++
    if (filters.value.voted) count++
    if (filters.value.teamSize) count++
    if (filters.value.createdAt) count++
    
    return count
  })
  
  // Helper Functions
  const calculateTrendingScore = (project: Project): number => {
    // Simple trending score based on recent activity
    const now = new Date().getTime()
    const createdAt = new Date(project.createdAt).getTime()
    const ageInDays = (now - createdAt) / (1000 * 60 * 60 * 24)
    
    // Weight recent projects higher
    const recencyScore = Math.max(0, 30 - ageInDays) / 30
    
    // Weight engagement metrics
    const viewScore = Math.min(project.stats.views / 1000, 1)
    const voteScore = Math.min(project.stats.votes / 100, 1)
    const commentScore = Math.min(project.stats.comments / 50, 1)
    
    // Combined score
    return (
      recencyScore * 0.4 +
      viewScore * 0.3 +
      voteScore * 0.2 +
      commentScore * 0.1
    )
  }
  
  // Methods
  const loadProjects = async (options: {
    forceRefresh?: boolean
    userId?: string
    hackathonId?: string
  } = {}) => {
    if (loading.value && !options.forceRefresh) return
    
    try {
      loading.value = true
      error.value = null
      
      // Build query parameters
      const queryParams = new URLSearchParams()
      if (options.userId) queryParams.append('user', options.userId)
      if (options.hackathonId) queryParams.append('hackathon', options.hackathonId)
      if (searchQuery.value.trim()) queryParams.append('search', searchQuery.value)
      
      // Apply filters
      if (filters.value.status && filters.value.status.length > 0) {
        queryParams.append('status', filters.value.status.join(','))
      }
      
      const queryString = queryParams.toString()
      const url = `/api/v1/projects${queryString ? `?${queryString}` : ''}`
      
      const response = await authStore.fetchWithAuth(url)
      
      if (!response.ok) {
        throw new Error(`Failed to load projects: ${response.statusText}`)
      }
      
      const data = await response.json()
      projects.value = data
      totalItems.value = data.length
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load projects'
      console.error('Error loading projects:', err)
      uiStore.showNotification({
        title: 'Fehler',
        type: 'error',
        message: 'Projekte konnten nicht geladen werden'
      })
    } finally {
      loading.value = false
    }
  }
  
  const loadProject = async (projectId: string) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await authStore.fetchWithAuth(`/api/v1/projects/${projectId}`)
      
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Project not found')
        }
        throw new Error(`Failed to load project: ${response.statusText}`)
      }
      
      const project = await response.json()
      
      // Update local state if project exists in list
      const index = projects.value.findIndex(p => p.id === projectId)
      if (index !== -1) {
        projects.value[index] = project
      }
      
      return project
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load project'
      console.error('Error loading project:', err)
      uiStore.showNotification({
        title: 'Fehler',
        type: 'error',
        message: 'Projekt konnte nicht geladen werden'
      })
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const createProject = async (projectData: Partial<Project>) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await authStore.fetchWithAuth('/api/v1/projects', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(projectData)
      })
      
      if (!response.ok) {
        throw new Error(`Failed to create project: ${response.statusText}`)
      }
      
      const newProject = await response.json()
      projects.value.unshift(newProject)
      
      uiStore.showNotification({
        title: 'Erfolg',
        type: 'success',
        message: 'Projekt erfolgreich erstellt'
      })
      
      return newProject
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create project'
      console.error('Error creating project:', err)
      uiStore.showNotification({
        title: 'Fehler',
        type: 'error',
        message: 'Projekt konnte nicht erstellt werden'
      })
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const updateProject = async (projectId: string, updates: Partial<Project>) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await authStore.fetchWithAuth(`/api/v1/projects/${projectId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updates)
      })
      
      if (!response.ok) {
        throw new Error(`Failed to update project: ${response.statusText}`)
      }
      
      const updatedProject = await response.json()
      
      // Update im lokalen State
      const index = projects.value.findIndex(p => p.id === projectId)
      if (index !== -1) {
        const existingProject = projects.value[index]
        if (existingProject) {
          // Type-safe merge of partial updates with existing project
          const mergedProject = {
            ...existingProject,
            ...updates,
            // Ensure required fields are preserved
            id: existingProject.id,
            title: updates.title ?? existingProject.title,
            slug: updates.slug ?? existingProject.slug,
            description: updates.description ?? existingProject.description,
            status: updates.status ?? existingProject.status,
            visibility: updates.visibility ?? existingProject.visibility,
            createdAt: existingProject.createdAt,
            updatedAt: new Date().toISOString(),
          }
          projects.value[index] = mergedProject
        }
      }
      
      uiStore.showNotification({
        title: 'Erfolg',
        type: 'success',
        message: 'Projekt erfolgreich aktualisiert'
      })
      
      return updatedProject
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update project'
      console.error('Error updating project:', err)
      uiStore.showNotification({
        title: 'Fehler',
        type: 'error',
        message: 'Projekt konnte nicht aktualisiert werden'
      })
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const deleteProject = async (projectId: string) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await authStore.fetchWithAuth(`/api/v1/projects/${projectId}`, {
        method: 'DELETE'
      })
      
      if (!response.ok) {
        throw new Error(`Failed to delete project: ${response.statusText}`)
      }
      
      // Remove from local state
      projects.value = projects.value.filter(p => p.id !== projectId)
      totalItems.value = Math.max(0, totalItems.value - 1)
      
      uiStore.showNotification({
        title: 'Erfolg',
        type: 'success',
        message: 'Projekt erfolgreich gelöscht'
      })
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete project'
      console.error('Error deleting project:', err)
      uiStore.showNotification({
        title: 'Fehler',
        type: 'error',
        message: 'Projekt konnte nicht gelöscht werden'
      })
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const voteProject = async (projectId: string, voteValue: 1 | -1 | null) => {
    try {
      const voteType = voteValue === 1 ? 'upvote' : voteValue === -1 ? 'downvote' : 'remove'
      
      const response = await authStore.fetchWithAuth(`/api/v1/projects/${projectId}/vote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ vote_type: voteType })
      })
      
      if (!response.ok) {
        throw new Error(`Failed to vote on project: ${response.statusText}`)
      }
      
      // Update im lokalen State
      const project = projects.value.find(p => p.id === projectId)
      if (project) {
        const previousVote = project.userVote
        
        // Update vote count
        if (previousVote === 1 && voteValue !== 1) {
          project.stats.votes = Math.max(0, project.stats.votes - 1)
        } else if (previousVote === -1 && voteValue !== -1) {
          project.stats.votes = Math.max(0, project.stats.votes + 1)
        } else if (previousVote !== 1 && voteValue === 1) {
          project.stats.votes += 1
        } else if (previousVote !== -1 && voteValue === -1) {
          project.stats.votes = Math.max(0, project.stats.votes - 1)
        }
        
        project.userVote = voteValue
      }
      
      uiStore.showNotification({
        title: 'Erfolg',
        type: 'success',
        message: voteValue === 1 ? 'Projekt positiv bewertet' : 
                voteValue === -1 ? 'Projekt negativ bewertet' : 
                'Bewertung entfernt'
      })
      
    } catch (err) {
      console.error('Error voting on project:', err)
      uiStore.showNotification({
        title: 'Fehler',
        type: 'error',
        message: 'Bewertung konnte nicht gespeichert werden'
      })
      throw err
    }
  }
  
  const bookmarkProject = async (projectId: string, isBookmarked: boolean) => {
    try {
      const response = await authStore.fetchWithAuth(`/api/v1/projects/${projectId}/bookmark`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ bookmarked: isBookmarked })
      })
      
      if (!response.ok) {
        throw new Error(`Failed to bookmark project: ${response.statusText}`)
      }
      
      // Update im lokalen State
      const project = projects.value.find(p => p.id === projectId)
      if (project) {
        project.isBookmarked = isBookmarked
        
        // Update bookmark count
        if (isBookmarked) {
          project.stats.bookmarks += 1
        } else {
          project.stats.bookmarks = Math.max(0, project.stats.bookmarks - 1)
        }
      }
      
      uiStore.showNotification({
        title: 'Erfolg',
        type: 'success',
        message: isBookmarked ? 'Projekt als Lesezeichen gespeichert' : 'Lesezeichen entfernt'
      })
      
    } catch (err) {
      console.error('Error bookmarking project:', err)
      uiStore.showNotification({
        title: 'Fehler',
        type: 'error',
        message: 'Lesezeichen konnte nicht gespeichert werden'
      })
      throw err
    }
  }
  
  const setFilters = (newFilters: ProjectFilterOptions) => {
    filters.value = { ...filters.value, ...newFilters }
    currentPage.value = 1 // Reset to first page when filters change
  }
  
  const clearFilters = () => {
    filters.value = {}
    searchQuery.value = ''
    currentPage.value = 1
  }
  
  const setSortOption = (option: ProjectSortOption) => {
    sortOption.value = option
  }
  
  const setSearchQuery = (query: string) => {
    searchQuery.value = query
    currentPage.value = 1
  }
  
  const setPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }
  
  const setItemsPerPage = (count: number) => {
    itemsPerPage.value = Math.max(1, count)
    currentPage.value = 1
  }
  
  const getProjectById = (projectId: string) => {
    return projects.value.find(p => p.id === projectId)
  }
  
  const getRelatedProjects = (project: Project, limit: number = 3): Project[] => {
    if (!project) return []
    
    return projects.value
      .filter(p => p.id !== project.id)
      .filter(p => {
        // Find related projects by shared technologies
        const sharedTechnologies = project.technologies?.filter(tech =>
          p.technologies?.some(pTech => pTech.id === tech.id)
        ) || []
        
        // Find related projects by shared tags
        const sharedTags = project.tags?.filter(tag =>
          p.tags?.some(pTag => pTag.id === tag.id)
        ) || []
        
        // Find related projects by same hackathon
        const sameHackathon = project.hackathonId && p.hackathonId === project.hackathonId
        
        return sharedTechnologies.length > 0 || sharedTags.length > 0 || sameHackathon
      })
      .slice(0, limit)
  }
  
  // Watch for filter changes to update total items
  watch([filters, searchQuery], () => {
    totalItems.value = sortedProjects.value.length
  })
  
  // Initial load
  loadProjects()
  
  return {
    // State
    projects: paginatedProjects,
    allProjects: sortedProjects,
    loading,
    error,
    
    // Filter State
    filters,
    sortOption,
    searchQuery,
    currentPage,
    itemsPerPage,
    totalItems,
    totalPages,
    
    // Computed
    hasFilters,
    activeFilterCount,
    
    // Methods
    loadProjects,
    loadProject,
    createProject,
    updateProject,
    deleteProject,
    voteProject,
    bookmarkProject,
    setFilters,
    clearFilters,
    setSortOption,
    setSearchQuery,
    setPage,
    setItemsPerPage,
    getProjectById,
    getRelatedProjects,
  }
}

export type UseProjectsReturn = ReturnType<typeof useProjects>
