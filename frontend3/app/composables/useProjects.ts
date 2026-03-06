import { ref, computed, watch } from 'vue'
import type { Project, ProjectFilterOptions } from '../types/project-types'
import { ProjectSortOption } from '../types/project-types'

/**
 * Composable für Projekt-bezogene Daten und Logik
 * Bietet Funktionen zum Laden, Filtern, Sortieren und Verwalten von Projekten
 */
export function useProjects() {
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
      
      // Hier würde normalerweise ein API-Call stehen
      // Für jetzt simulieren wir eine leere Liste
      projects.value = []
      totalItems.value = 0
      
      // In einer echten Implementierung:
      // const response = await api.getProjects(options)
      // projects.value = response.data
      // totalItems.value = response.total
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load projects'
      console.error('Error loading projects:', err)
    } finally {
      loading.value = false
    }
  }
  
  const loadProject = async (projectId: string) => {
    try {
      loading.value = true
      error.value = null
      
      // Hier würde normalerweise ein API-Call stehen
      // Für jetzt simulieren wir ein leeres Projekt
      const project = null // await api.getProject(projectId)
      
      if (!project) {
        throw new Error('Project not found')
      }
      
      return project
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load project'
      console.error('Error loading project:', err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const createProject = async (projectData: Partial<Project>) => {
    try {
      loading.value = true
      error.value = null
      
      // Hier würde normalerweise ein API-Call stehen
      // const newProject = await api.createProject(projectData)
      // projects.value.unshift(newProject)
      // return newProject
      
      return {} as Project
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create project'
      console.error('Error creating project:', err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const updateProject = async (projectId: string, updates: Partial<Project>) => {
    try {
      loading.value = true
      error.value = null
      
      // Hier würde normalerweise ein API-Call stehen
      // const updatedProject = await api.updateProject(projectId, updates)
      
      // Update im lokalen State
      const index = projects.value.findIndex(p => p.id === projectId)
      if (index !== -1) {
        // Type-safe merge of partial updates with existing project
        const existingProject = projects.value[index]
        const updatedProject = {
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
        projects.value[index] = updatedProject
      }
      
      // return updatedProject
      return {} as Project
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update project'
      console.error('Error updating project:', err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const deleteProject = async (projectId: string) => {
    try {
      loading.value = true
      error.value = null
      
      // Hier würde normalerweise ein API-Call stehen
      // await api.deleteProject(projectId)
      
      // Remove from local state
      projects.value = projects.value.filter(p => p.id !== projectId)
      totalItems.value = Math.max(0, totalItems.value - 1)
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete project'
      console.error('Error deleting project:', err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const voteProject = async (projectId: string, voteValue: 1 | -1 | null) => {
    try {
      // Hier würde normalerweise ein API-Call stehen
      // await api.voteProject(projectId, voteValue)
      
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
      
    } catch (err) {
      console.error('Error voting on project:', err)
      throw err
    }
  }
  
  const bookmarkProject = async (projectId: string, isBookmarked: boolean) => {
    try {
      // Hier würde normalerweise ein API-Call stehen
      // await api.bookmarkProject(projectId, isBookmarked)
      
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
      
    } catch (err) {
      console.error('Error bookmarking project:', err)
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