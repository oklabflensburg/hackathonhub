<template>
  <div class="space-y-8">
    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Users</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">
          Browse all registered users on the platform
        </p>
      </div>
      <div class="flex items-center space-x-4">
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search users..."
            class="input pl-10"
          />
          <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <select v-model="sortBy" class="input">
          <option value="newest">Newest</option>
          <option value="name">Name</option>
          <option value="activity">Last Active</option>
        </select>
      </div>
    </div>

    <!-- Users Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div
        v-for="user in filteredUsers"
        :key="user.id"
        class="card-hover group cursor-pointer"
        @click="$router.push(`/users/${user.id}`)"
      >
        <!-- User Avatar and Info -->
        <div class="flex flex-col items-center text-center p-6">
          <div class="relative mb-4">
            <div class="w-24 h-24 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg">
              <img
                v-if="user.avatar_url"
                :src="user.avatar_url"
                :alt="user.name || user.username"
                class="w-full h-full object-cover"
              />
              <div v-else class="text-3xl font-bold text-gray-600 dark:text-gray-400">
                {{ userInitials(user) }}
              </div>
            </div>
            <div v-if="user.is_admin" class="absolute -bottom-2 left-1/2 transform -translate-x-1/2">
              <span class="badge badge-warning text-xs px-2 py-1">
                Admin
              </span>
            </div>
          </div>
          
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 mb-1">
            {{ user.name || user.username }}
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
            @{{ user.username }}
          </p>
          
          <!-- User Bio -->
          <p v-if="user.bio" class="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
            {{ user.bio }}
          </p>
          
          <!-- User Stats -->
          <div class="grid grid-cols-3 gap-4 w-full mt-4 pt-4 border-t border-gray-100 dark:border-gray-800">
            <div class="text-center">
              <div class="text-lg font-bold text-gray-900 dark:text-white">{{ user.project_count || 0 }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">Projects</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-bold text-gray-900 dark:text-white">{{ user.team_count || 0 }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">Teams</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-bold text-gray-900 dark:text-white">{{ user.hackathon_count || 0 }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">Hackathons</div>
            </div>
          </div>
          
          <!-- User Location/Company -->
          <div v-if="user.location || user.company" class="flex flex-col items-center gap-2 mt-4 pt-4 border-t border-gray-100 dark:border-gray-800 w-full">
            <div v-if="user.location" class="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {{ user.location }}
            </div>
            <div v-if="user.company" class="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              {{ user.company }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredUsers.length === 0 && !isLoading" class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-6 text-gray-300 dark:text-gray-600">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        No users found
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        Try adjusting your search or filter to find what you're looking for.
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">Loading users...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-6 text-red-400">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.342 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
      </div>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        Failed to load users
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
      <button @click="fetchUsers" class="btn btn-primary">
        Try Again
      </button>
    </div>

    <!-- Load More -->
    <div v-if="filteredUsers.length > 0 && hasMore" class="text-center pt-8">
      <button
        @click="loadMore"
        :disabled="isLoading"
        class="btn btn-outline px-8"
      >
        <svg v-if="isLoading" class="w-5 h-5 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
        Load More
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from '#imports'
import { useUIStore } from '~/stores/ui'

const route = useRoute()
const uiStore = useUIStore()
const searchQuery = ref('')
const sortBy = ref('newest')
const isLoading = ref(false)
const users = ref<any[]>([])
const error = ref<string | null>(null)
const hasMore = ref(true)
const limit = 20

const config = useRuntimeConfig()
const apiUrl = config.public.apiUrl

// Initialize search query from URL parameter
onMounted(() => {
  if (route.query.q) {
    searchQuery.value = route.query.q as string
  }
  fetchUsers()
})

// Fetch users from API with optional search
const fetchUsers = async () => {
  isLoading.value = true
  error.value = null
  try {
    // Build query parameters
    const params = new URLSearchParams()
    params.append('skip', '0')
    params.append('limit', limit.toString())
    
    const response = await fetch(`${apiUrl}/api/users?${params.toString()}`)
    if (!response.ok) {
      throw new Error(`Failed to fetch users: ${response.status}`)
    }
    const data = await response.json()
    
    // Check if we got fewer users than requested (end of data)
    if (data.length < limit) {
      hasMore.value = false
    }
    
    // Transform API data to match frontend structure
    users.value = data.map((user: any) => ({
      id: user.id,
      username: user.username,
      name: user.name,
      email: user.email,
      avatar_url: user.avatar_url,
      bio: user.bio,
      location: user.location,
      company: user.company,
      is_admin: user.is_admin || false,
      email_verified: user.email_verified || false,
      auth_method: user.auth_method || 'email',
      last_login: user.last_login,
      created_at: user.created_at,
      updated_at: user.updated_at,
      // These would need to come from user profile endpoint
      project_count: 0,
      team_count: 0,
      hackathon_count: 0
    }))
    
    // Fetch additional profile data for each user to get stats
    await fetchUserProfiles()
    
  } catch (err: any) {
    error.value = err.message || 'Failed to load users'
    console.error('Error fetching users:', err)
    uiStore.showError('Failed to load users', 'Unable to load users. Please try again later.')
    // Fallback to empty array
    users.value = []
  } finally {
    isLoading.value = false
  }
}

// Fetch user profiles to get stats (projects, teams, hackathons count)
const fetchUserProfiles = async () => {
  try {
    const promises = users.value.map(async (user) => {
      try {
        const response = await fetch(`${apiUrl}/api/users/${user.id}/profile`)
        if (response.ok) {
          const profile = await response.json()
          user.project_count = profile.stats?.project_count || 0
          user.team_count = profile.stats?.team_count || 0
          user.hackathon_count = profile.stats?.hackathon_count || 0
        }
      } catch (err) {
        console.error(`Error fetching profile for user ${user.id}:`, err)
      }
    })
    
    await Promise.all(promises)
  } catch (err) {
    console.error('Error fetching user profiles:', err)
  }
}

// Load more users
const loadMore = async () => {
  isLoading.value = true
  try {
    const skip = users.value.length
    const response = await fetch(`${apiUrl}/api/users?skip=${skip}&limit=${limit}`)
    if (!response.ok) {
      throw new Error(`Failed to load more users: ${response.status}`)
    }
    
    const data = await response.json()
    
    // Check if we got fewer users than requested (end of data)
    if (data.length < limit) {
      hasMore.value = false
    }
    
    // Transform API data
    const newUsers = data.map((user: any) => ({
      id: user.id,
      username: user.username,
      name: user.name,
      email: user.email,
      avatar_url: user.avatar_url,
      bio: user.bio,
      location: user.location,
      company: user.company,
      is_admin: user.is_admin || false,
      email_verified: user.email_verified || false,
      auth_method: user.auth_method || 'email',
      last_login: user.last_login,
      created_at: user.created_at,
      updated_at: user.updated_at,
      project_count: 0,
      team_count: 0,
      hackathon_count: 0
    }))
    
    // Add new users to existing list
    users.value = [...users.value, ...newUsers]
    
    // Fetch profiles for new users
    await fetchUserProfilesForNewUsers(newUsers)
    
  } catch (err: any) {
    console.error('Error loading more users:', err)
    uiStore.showError('Failed to load more users', 'Unable to load more users. Please try again.')
  } finally {
    isLoading.value = false
  }
}

// Fetch profiles for newly loaded users
const fetchUserProfilesForNewUsers = async (newUsers: any[]) => {
  try {
    const promises = newUsers.map(async (user) => {
      try {
        const response = await fetch(`${apiUrl}/api/users/${user.id}/profile`)
        if (response.ok) {
          const profile = await response.json()
          user.project_count = profile.stats?.project_count || 0
          user.team_count = profile.stats?.team_count || 0
          user.hackathon_count = profile.stats?.hackathon_count || 0
        }
      } catch (err) {
        console.error(`Error fetching profile for user ${user.id}:`, err)
      }
    })
    
    await Promise.all(promises)
  } catch (err) {
    console.error('Error fetching profiles for new users:', err)
  }
}

// Helper function to get user initials
const userInitials = (user: any) => {
  if (user.name) {
    return user.name.split(' ').map((n: string) => n[0]).join('').toUpperCase().substring(0, 2)
  }
  return user.username.substring(0, 2).toUpperCase()
}

// Filtered users based on search and sort
const filteredUsers = computed(() => {
  let filtered = [...users.value]

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(user =>
      user.username.toLowerCase().includes(query) ||
      (user.name && user.name.toLowerCase().includes(query)) ||
      (user.bio && user.bio.toLowerCase().includes(query)) ||
      (user.location && user.location.toLowerCase().includes(query)) ||
      (user.company && user.company.toLowerCase().includes(query))
    )
  }

  // Apply sorting
  if (sortBy.value === 'name') {
    filtered.sort((a, b) => {
      const nameA = (a.name || a.username).toLowerCase()
      const nameB = (b.name || b.username).toLowerCase()
      return nameA.localeCompare(nameB)
    })
  } else if (sortBy.value === 'activity') {
    // Sort by last login (most recent first)
    filtered.sort((a, b) => {
      const dateA = a.last_login ? new Date(a.last_login).getTime() : 0
      const dateB = b.last_login ? new Date(b.last_login).getTime() : 0
      return dateB - dateA // Most recent first
    })
  } else {
    // Default: newest (by created_at)
    filtered.sort((a, b) => {
      const dateA = new Date(a.created_at).getTime()
      const dateB = new Date(b.created_at).getTime()
      return dateB - dateA // Most recent first
    })
  }

  return filtered
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>