import { ref, computed } from 'vue'
import type { Hackathon } from '~/types/hackathon-types'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

interface HackathonFilters {
  status?: 'upcoming' | 'active' | 'completed' | 'all'
  search?: string
  location?: string
  dateFrom?: string
  dateTo?: string
}

interface UseHackathonsListOptions {
  page?: number
  pageSize?: number
  filters?: HackathonFilters
}

/**
 * Composable für die Verwaltung mehrerer Hackathons (Liste, Filter, Suche)
 * 
 * @example
 * ```typescript
 * const { hackathons, loading, error, fetchHackathons, hasMore } = useHackathonsList({
 *   page: 1,
 *   pageSize: 20,
 *   filters: { status: 'upcoming' }
 * })
 * ```
 */
export function useHackathonsList(options: UseHackathonsListOptions = {}) {
  const { page = 1, pageSize = 20, filters = {} } = options

  const authStore = useAuthStore()
  const uiStore = useUIStore()

  const hackathons = ref<Hackathon[]>([])
  const loading = ref(false)
  const error = ref<Error | null>(null)
  const total = ref(0)
  const currentPage = ref(page)
  const hasMore = ref(true)

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

  const fetchHackathons = async (reset = false) => {
    if (reset) {
      currentPage.value = 1
      hackathons.value = []
      hasMore.value = true
    }

    if (!hasMore.value && !reset) return

    loading.value = true
    error.value = null

    try {
      // Build query parameters
      const params = new URLSearchParams()
      params.append('skip', ((currentPage.value - 1) * pageSize).toString())
      params.append('limit', pageSize.toString())
      if (filters.status && filters.status !== 'all') {
        params.append('status', filters.status)
      }
      if (filters.search) {
        params.append('search', filters.search)
      }
      if (filters.location) {
        params.append('location', filters.location)
      }
      if (filters.dateFrom) {
        params.append('date_from', filters.dateFrom)
      }
      if (filters.dateTo) {
        params.append('date_to', filters.dateTo)
      }

      const response = await authStore.fetchWithAuth(`/api/hackathons?${params.toString()}`)
      if (!response.ok) {
        throw new Error(`Failed to fetch hackathons: ${response.status}`)
      }
      const data = await response.json()
      
      const transformedHackathons = data.hackathons?.map(transformApiHackathon) || []
      
      if (reset) {
        hackathons.value = transformedHackathons
      } else {
        hackathons.value.push(...transformedHackathons)
      }
      
      total.value = data.total || 0
      hasMore.value = hackathons.value.length < total.value
      
      if (!reset && transformedHackathons.length > 0) {
        currentPage.value++
      }
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Laden der Hackathons')
      console.error('Fehler beim Laden der Hackathons:', err)
      uiStore.showError('Fehler beim Laden der Hackathons')
    } finally {
      loading.value = false
    }
  }

  const loadMore = async () => {
    if (loading.value || !hasMore.value) return
    await fetchHackathons(false)
  }

  const refresh = async () => {
    await fetchHackathons(true)
  }

  const applyFilters = async (newFilters: HackathonFilters) => {
    // Update filters and reset pagination
    Object.assign(filters, newFilters)
    await refresh()
  }

  const clearFilters = async () => {
    // Clear all filters
    Object.keys(filters).forEach(key => {
      delete (filters as any)[key]
    })
    await refresh()
  }

  const searchHackathons = async (searchTerm: string) => {
    filters.search = searchTerm
    await refresh()
  }

  const filterByStatus = async (status: HackathonFilters['status']) => {
    filters.status = status
    await refresh()
  }

  const filterByLocation = async (location: string) => {
    filters.location = location
    await refresh()
  }

  const filterByDateRange = async (dateFrom: string, dateTo: string) => {
    filters.dateFrom = dateFrom
    filters.dateTo = dateTo
    await refresh()
  }

  // Initial fetch
  fetchHackathons(true)

  return {
    // State
    hackathons,
    loading,
    error,
    total,
    currentPage,
    hasMore,
    
    // Computed
    isEmpty: computed(() => hackathons.value.length === 0),
    isFiltered: computed(() => 
      !!filters.status || 
      !!filters.search || 
      !!filters.location || 
      !!filters.dateFrom || 
      !!filters.dateTo
    ),
    
    // Methods
    fetchHackathons,
    loadMore,
    refresh,
    applyFilters,
    clearFilters,
    searchHackathons,
    filterByStatus,
    filterByLocation,
    filterByDateRange
  }
}