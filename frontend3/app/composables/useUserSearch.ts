import { ref, computed, watch, type Ref } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n, useRuntimeConfig } from '#imports'
import type { UserSearchResult, UseUserSearchOptions } from '~/types/team-invitations'

/**
 * Composable für die Benutzersuche mit Autocomplete und Debouncing
 * 
 * @example
 * ```typescript
 * const { query, results, loading, search, selectUser } = useUserSearch({
 *   debounceMs: 300,
 *   minQueryLength: 2,
 *   excludeUserIds: [1, 2, 3]
 * })
 * ```
 */
export function useUserSearch(options: UseUserSearchOptions = {}) {
  const {
    debounceMs = 300,
    minQueryLength = 2,
    excludeUserIds = []
  } = options

  const authStore = useAuthStore()
  const uiStore = useUIStore()
  const { t } = useI18n()
  const config = useRuntimeConfig()

  // State
  const query = ref('')
  const results = ref<UserSearchResult[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const selectedUser = ref<UserSearchResult | null>(null)

  // Computed
  const hasResults = computed(() => results.value.length > 0)
  const isEmpty = computed(() => query.value.length >= minQueryLength && !loading.value && results.value.length === 0)
  const isValidQuery = computed(() => query.value.length >= minQueryLength)

  // Methods
  async function search(searchQuery: string): Promise<void> {
    if (searchQuery.length < minQueryLength) {
      results.value = []
      return
    }

    loading.value = true
    error.value = null

    try {
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'
      const response = await authStore.fetchWithAuth(
        `/api/users?username=${encodeURIComponent(searchQuery)}&limit=8`
      )

      if (!response.ok) {
        throw new Error(`Search failed with status: ${response.status}`)
      }

      const users = await response.json()
      
      // Filter out excluded users
      const filteredUsers = users.filter((user: UserSearchResult) => {
        return !excludeUserIds.includes(user.id)
      })

      // Mark users who are already team members (if is_member property is provided)
      const enhancedUsers = filteredUsers.map((user: UserSearchResult) => ({
        ...user,
        is_member: user.is_member || false
      }))

      results.value = enhancedUsers
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to search users'
      console.error('Failed to search users:', err)
      results.value = []
    } finally {
      loading.value = false
    }
  }

  function clear(): void {
    query.value = ''
    results.value = []
    selectedUser.value = null
    error.value = null
  }

  function selectUser(user: UserSearchResult): void {
    selectedUser.value = user
    query.value = user.username
    results.value = []
  }

  // Debounce timer
  let debounceTimer: NodeJS.Timeout | null = null

  // Debounced search function
  function debouncedSearch() {
    if (debounceTimer) {
      clearTimeout(debounceTimer)
    }
    
    debounceTimer = setTimeout(async () => {
      if (query.value.length >= minQueryLength) {
        await search(query.value)
      } else {
        results.value = []
      }
    }, debounceMs)
  }

  // Watch query changes and trigger debounced search
  watch(query, () => {
    if (selectedUser.value && query.value !== selectedUser.value.username) {
      selectedUser.value = null
    }
    debouncedSearch()
  })

  // Helper function to check if a user is excluded
  function isUserExcluded(userId: number): boolean {
    return excludeUserIds.includes(userId)
  }

  // Helper function to get user by ID
  function getUserById(userId: number): UserSearchResult | undefined {
    return results.value.find(user => user.id === userId)
  }

  return {
    // State
    query,
    results,
    loading,
    error,
    selectedUser,
    
    // Computed
    hasResults,
    isEmpty,
    isValidQuery,
    
    // Methods
    search,
    clear,
    selectUser,
    isUserExcluded,
    getUserById,
  }
}

export type UseUserSearchReturn = ReturnType<typeof useUserSearch>