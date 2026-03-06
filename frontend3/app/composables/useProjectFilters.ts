import { ref, computed, watch } from 'vue'
import type { ProjectFilterOptions } from '../types/project-types'
import { ProjectSortOption, ProjectStatus, ProjectVisibility } from '../types/project-types'

/**
 * Composable für erweiterte Projekt-Filterlogik
 * Bietet Funktionen zum Verwalten, Validieren und Anwenden von Filtern
 */
export function useProjectFilters() {
  // Filter State
  const filters = ref<ProjectFilterOptions>({})
  const sortOption = ref<ProjectSortOption>(ProjectSortOption.NEWEST)
  const searchQuery = ref('')
  
  // UI State
  const isFiltersOpen = ref(false)
  const activeFilterPanel = ref<string | null>(null)
  
  // Computed Properties
  const hasActiveFilters = computed(() => {
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
  
  const filterSummary = computed(() => {
    const summary: string[] = []
    
    if (searchQuery.value.trim()) {
      summary.push(`Suche: "${searchQuery.value}"`)
    }
    
    if (filters.value.status && filters.value.status.length > 0) {
      summary.push(`${filters.value.status.length} Status-Filter`)
    }
    
    if (filters.value.technologies && filters.value.technologies.length > 0) {
      summary.push(`${filters.value.technologies.length} Technologien`)
    }
    
    if (filters.value.tags && filters.value.tags.length > 0) {
      summary.push(`${filters.value.tags.length} Tags`)
    }
    
    if (filters.value.hackathonId) {
      summary.push('Hackathon-Filter')
    }
    
    if (filters.value.visibility && filters.value.visibility.length > 0) {
      summary.push(`${filters.value.visibility.length} Sichtbarkeits-Filter`)
    }
    
    if (filters.value.bookmarked !== undefined) {
      summary.push(filters.value.bookmarked ? 'Nur Lesezeichen' : 'Ohne Lesezeichen')
    }
    
    if (filters.value.voted) {
      summary.push(filters.value.voted === 'upvoted' ? 'Nur Upvotes' : 'Nur Downvotes')
    }
    
    if (filters.value.teamSize) {
      const { min, max } = filters.value.teamSize
      if (min && max) {
        summary.push(`Teamgröße: ${min}-${max}`)
      } else if (min) {
        summary.push(`Teamgröße: ≥${min}`)
      } else if (max) {
        summary.push(`Teamgröße: ≤${max}`)
      }
    }
    
    if (filters.value.createdAt) {
      const { from, to } = filters.value.createdAt
      if (from && to) {
        summary.push(`Zeitraum: ${formatDate(from)} - ${formatDate(to)}`)
      } else if (from) {
        summary.push(`Ab: ${formatDate(from)}`)
      } else if (to) {
        summary.push(`Bis: ${formatDate(to)}`)
      }
    }
    
    return summary
  })
  
  const sortOptions = computed(() => [
    {
      value: ProjectSortOption.NEWEST,
      label: 'Neueste zuerst',
      icon: 'i-heroicons-clock',
      description: 'Nach Erstellungsdatum (neueste zuerst)'
    },
    {
      value: ProjectSortOption.OLDEST,
      label: 'Älteste zuerst',
      icon: 'i-heroicons-clock',
      description: 'Nach Erstellungsdatum (älteste zuerst)'
    },
    {
      value: ProjectSortOption.MOST_VIEWED,
      label: 'Meist gesehen',
      icon: 'i-heroicons-eye',
      description: 'Nach Anzahl der Aufrufe'
    },
    {
      value: ProjectSortOption.MOST_VOTED,
      label: 'Meist gevotet',
      icon: 'i-heroicons-hand-thumb-up',
      description: 'Nach Anzahl der Votes'
    },
    {
      value: ProjectSortOption.MOST_COMMENTED,
      label: 'Meist kommentiert',
      icon: 'i-heroicons-chat-bubble-left-right',
      description: 'Nach Anzahl der Kommentare'
    },
    {
      value: ProjectSortOption.TRENDING,
      label: 'Trending',
      icon: 'i-heroicons-fire',
      description: 'Nach aktueller Popularität'
    },
    {
      value: ProjectSortOption.DEADLINE,
      label: 'Deadline',
      icon: 'i-heroicons-calendar',
      description: 'Nach Deadline (nächste zuerst)'
    },
    {
      value: ProjectSortOption.ALPHABETICAL,
      label: 'Alphabetisch',
      icon: 'i-heroicons-bars-arrow-down',
      description: 'Nach Titel (A-Z)'
    }
  ])
  
  const currentSortOption = computed(() => {
    return sortOptions.value.find(option => option.value === sortOption.value)
  })
  
  // Methods
  const setFilters = (newFilters: ProjectFilterOptions) => {
    filters.value = { ...filters.value, ...newFilters }
  }
  
  const clearFilters = () => {
    filters.value = {}
    searchQuery.value = ''
  }
  
  const clearFilter = (filterKey: keyof ProjectFilterOptions) => {
    if (filterKey in filters.value) {
      const newFilters = { ...filters.value }
      delete newFilters[filterKey]
      filters.value = newFilters
    }
  }
  
  const setSearchQuery = (query: string) => {
    searchQuery.value = query
  }
  
  const setSortOption = (option: ProjectSortOption) => {
    sortOption.value = option
  }
  
  const toggleFiltersOpen = () => {
    isFiltersOpen.value = !isFiltersOpen.value
  }
  
  const openFilterPanel = (panelId: string) => {
    activeFilterPanel.value = panelId
    isFiltersOpen.value = true
  }
  
  const closeFilterPanel = () => {
    activeFilterPanel.value = null
  }
  
  const toggleStatusFilter = (status: ProjectStatus) => {
    const currentStatuses = filters.value.status || []
    
    if (currentStatuses.includes(status)) {
      filters.value = {
        ...filters.value,
        status: currentStatuses.filter(s => s !== status)
      }
    } else {
      filters.value = {
        ...filters.value,
        status: [...currentStatuses, status]
      }
    }
  }
  
  const toggleTechnologyFilter = (technologyId: string) => {
    const currentTechnologies = filters.value.technologies || []
    
    if (currentTechnologies.includes(technologyId)) {
      filters.value = {
        ...filters.value,
        technologies: currentTechnologies.filter(id => id !== technologyId)
      }
    } else {
      filters.value = {
        ...filters.value,
        technologies: [...currentTechnologies, technologyId]
      }
    }
  }
  
  const toggleTagFilter = (tagId: string) => {
    const currentTags = filters.value.tags || []
    
    if (currentTags.includes(tagId)) {
      filters.value = {
        ...filters.value,
        tags: currentTags.filter(id => id !== tagId)
      }
    } else {
      filters.value = {
        ...filters.value,
        tags: [...currentTags, tagId]
      }
    }
  }
  
  const toggleVisibilityFilter = (visibility: ProjectVisibility) => {
    const currentVisibilities = filters.value.visibility || []
    
    if (currentVisibilities.includes(visibility)) {
      filters.value = {
        ...filters.value,
        visibility: currentVisibilities.filter(v => v !== visibility)
      }
    } else {
      filters.value = {
        ...filters.value,
        visibility: [...currentVisibilities, visibility]
      }
    }
  }
  
  const setHackathonFilter = (hackathonId: string | null) => {
    if (hackathonId) {
      filters.value = {
        ...filters.value,
        hackathonId
      }
    } else {
      const newFilters = { ...filters.value }
      delete newFilters.hackathonId
      filters.value = newFilters
    }
  }
  
  const setBookmarkedFilter = (bookmarked: boolean | null) => {
    if (bookmarked !== null) {
      filters.value = {
        ...filters.value,
        bookmarked
      }
    } else {
      const newFilters = { ...filters.value }
      delete newFilters.bookmarked
      filters.value = newFilters
    }
  }
  
  const setVotedFilter = (voted: 'upvoted' | 'downvoted' | null) => {
    if (voted) {
      filters.value = {
        ...filters.value,
        voted
      }
    } else {
      const newFilters = { ...filters.value }
      delete newFilters.voted
      filters.value = newFilters
    }
  }
  
  const setTeamSizeFilter = (min?: number, max?: number) => {
    if (min !== undefined || max !== undefined) {
      filters.value = {
        ...filters.value,
        teamSize: {
          min: min ?? filters.value.teamSize?.min,
          max: max ?? filters.value.teamSize?.max
        }
      }
    } else {
      const newFilters = { ...filters.value }
      delete newFilters.teamSize
      filters.value = newFilters
    }
  }
  
  const setDateRangeFilter = (from?: string, to?: string) => {
    if (from || to) {
      filters.value = {
        ...filters.value,
        createdAt: {
          from: from ?? filters.value.createdAt?.from,
          to: to ?? filters.value.createdAt?.to
        }
      }
    } else {
      const newFilters = { ...filters.value }
      delete newFilters.createdAt
      filters.value = newFilters
    }
  }
  
  const validateFilters = (): { valid: boolean; errors: string[] } => {
    const errors: string[] = []
    
    // Team Size Validation
    if (filters.value.teamSize) {
      const { min, max } = filters.value.teamSize
      if (min !== undefined && max !== undefined && min > max) {
        errors.push('Minimale Teamgröße darf nicht größer als maximale Teamgröße sein')
      }
      if (min !== undefined && min < 0) {
        errors.push('Teamgröße darf nicht negativ sein')
      }
      if (max !== undefined && max < 0) {
        errors.push('Maximale Teamgröße darf nicht negativ sein')
      }
    }
    
    // Date Range Validation
    if (filters.value.createdAt) {
      const { from, to } = filters.value.createdAt
      if (from && to) {
        const fromDate = new Date(from)
        const toDate = new Date(to)
        
        if (fromDate > toDate) {
          errors.push('Startdatum darf nicht nach Enddatum liegen')
        }
        
        if (fromDate > new Date()) {
          errors.push('Startdatum darf nicht in der Zukunft liegen')
        }
        
        if (toDate > new Date()) {
          errors.push('Enddatum darf nicht in der Zukunft liegen')
        }
      }
    }
    
    return {
      valid: errors.length === 0,
      errors
    }
  }
  
  const exportFilters = (): string => {
    const filterData = {
      filters: filters.value,
      searchQuery: searchQuery.value,
      sortOption: sortOption.value,
      timestamp: new Date().toISOString()
    }
    
    return JSON.stringify(filterData, null, 2)
  }
  
  const importFilters = (filterJson: string): boolean => {
    try {
      const filterData = JSON.parse(filterJson)
      
      if (filterData.filters) {
        filters.value = filterData.filters
      }
      
      if (filterData.searchQuery !== undefined) {
        searchQuery.value = filterData.searchQuery
      }
      
      if (filterData.sortOption) {
        sortOption.value = filterData.sortOption
      }
      
      return true
    } catch (error) {
      console.error('Failed to import filters:', error)
      return false
    }
  }
  
  const resetToDefaults = () => {
    filters.value = {}
    searchQuery.value = ''
    sortOption.value = ProjectSortOption.NEWEST
    isFiltersOpen.value = false
    activeFilterPanel.value = null
  }
  
  const getFilterPreset = (presetName: string): ProjectFilterOptions => {
    const presets: Record<string, ProjectFilterOptions> = {
      'recent': {
        createdAt: {
          from: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString() // Last 30 days
        }
      },
      'popular': {
        // Popular projects have high engagement
      },
      'bookmarked': {
        bookmarked: true
      },
      'my-votes': {
        voted: 'upvoted'
      },
      'team-projects': {
        teamSize: {
          min: 2
        }
      },
      'solo-projects': {
        teamSize: {
          max: 1
        }
      },
      'public-only': {
        visibility: [ProjectVisibility.PUBLIC]
      },
      'active': {
        status: [ProjectStatus.ACTIVE, ProjectStatus.UNDER_REVIEW]
      },
      'completed': {
        status: [ProjectStatus.COMPLETED]
      }
    }
    
    return presets[presetName] || {}
  }
  
  const applyPreset = (presetName: string) => {
    const presetFilters = getFilterPreset(presetName)
    filters.value = { ...filters.value, ...presetFilters }
  }
  
  // Helper Functions
  const formatDate = (dateString: string): string => {
    const date = new Date(dateString)
    return date.toLocaleDateString('de-DE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }
  
  // Watch for filter changes and validate
  watch(filters, () => {
    const validation = validateFilters()
    if (!validation.valid) {
      console.warn('Filter validation errors:', validation.errors)
    }
  }, { deep: true })
  
  return {
    // State
    filters,
    sortOption,
    searchQuery,
    isFiltersOpen,
    activeFilterPanel,
    
    // Computed
    hasActiveFilters,
    activeFilterCount,
    filterSummary,
    sortOptions,
    currentSortOption,
    
    // Methods
    setFilters,
    clearFilters,
    clearFilter,
    setSearchQuery,
    setSortOption,
    toggleFiltersOpen,
    openFilterPanel,
    closeFilterPanel,
    toggleStatusFilter,
    toggleTechnologyFilter,
    toggleTagFilter,
    toggleVisibilityFilter,
    setHackathonFilter,
    setBookmarkedFilter,
    setVotedFilter,
    setTeamSizeFilter,
    setDateRangeFilter,
    validateFilters,
    exportFilters,
    importFilters,
    resetToDefaults,
    getFilterPreset,
    applyPreset,
  }
}

export type UseProjectFiltersReturn = ReturnType<typeof useProjectFilters>