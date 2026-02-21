<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ $t('teams.title') }}</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">
          {{ $t('teams.subtitle', 'Browse and join teams for hackathons') }}
        </p>
      </div>
      <div class="mt-4 md:mt-0">
        <button
          @click="handleCreateTeamClick"
          class="btn btn-primary"
          :disabled="authStore.isLoading"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          {{ $t('teams.createTeam') }}
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ $t('teams.filter.hackathon') }}
          </label>
          <select
            v-model="filters.hackathon_id"
            class="w-full input"
            @change="loadTeams"
          >
            <option value="">{{ $t('teams.filter.allHackathons') }}</option>
            <option v-for="hackathon in hackathons" :key="hackathon.id" :value="hackathon.id">
              {{ hackathon.name }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ $t('teams.filter.status') }}
          </label>
          <select
            v-model="filters.is_open"
            class="w-full input"
            @change="loadTeams"
          >
            <option value="">{{ $t('teams.filter.allTeams') }}</option>
            <option :value="true">{{ $t('teams.filter.openTeams') }}</option>
            <option :value="false">{{ $t('teams.filter.closedTeams') }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ $t('teams.filter.search') }}
          </label>
          <div class="relative">
            <input
              v-model="filters.search"
              type="text"
              :placeholder="$t('teams.filter.searchPlaceholder')"
              class="w-full input pl-10"
              @input="debouncedLoadTeams"
            />
            <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="teamStore.isLoading && teams.length === 0" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">{{ $t('teams.loading') }}</p>
    </div>

    <!-- Error State -->
    <div v-else-if="teamStore.error && teams.length === 0" class="text-center py-12">
      <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400 mb-4">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <p class="text-gray-600 dark:text-gray-400">{{ teamStore.error }}</p>
      <button @click="loadTeams" class="mt-4 btn btn-outline">
        {{ $t('teams.retry') }}
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="teams.length === 0" class="text-center py-12">
      <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 mb-4">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
        {{ $t('teams.noTeamsFound') }}
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        {{ $t('teams.noTeamsDescription') }}
      </p>
      <button
        v-if="isAuthenticated"
        @click="navigateTo('/teams/create')"
        class="btn btn-primary"
      >
        {{ $t('teams.createFirstTeam') }}
      </button>
      <button
        v-else
        @click="navigateTo('/login')"
        class="btn btn-primary"
      >
        {{ $t('teams.loginToCreate') }}
      </button>
    </div>

    <!-- Teams Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="team in filteredTeams"
        :key="team.id"
        class="bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-lg transition-shadow duration-200"
      >
        <div class="p-6">
          <!-- Team Header -->
          <div class="flex items-start justify-between mb-4">
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                {{ team.name }}
              </h3>
              <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                {{ $t('teams.inHackathon') }}: {{ team.hackathon?.name || 'Unknown' }}
              </p>
            </div>
            <span
              :class="[
                'px-2 py-1 text-xs font-medium rounded-full',
                team.is_open
                  ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                  : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
              ]"
            >
              {{ team.is_open ? $t('teams.open') : $t('teams.closed') }}
            </span>
          </div>

          <!-- Team Description -->
          <p class="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
            {{ team.description || $t('teams.noDescription') }}
          </p>

          <!-- Team Stats -->
          <div class="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mb-4">
            <div class="flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{{ team.member_count || 0 }} / {{ team.max_members }} {{ $t('teams.members') }}</span>
            </div>
            <div class="flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>{{ formatDate(team.created_at) }}</span>
            </div>
          </div>

          <!-- Team Members Preview -->
          <div v-if="getTeamMembers(team.id)?.length > 0" class="mb-4">
            <div class="flex items-center mb-2">
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
                {{ $t('teams.teamMembers') }}
              </span>
            </div>
            <div class="flex -space-x-2">
               <div
                v-for="member in getTeamMembers(team.id).slice(0, 5)"
                :key="member.id"
                class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 border-2 border-white dark:border-gray-800 flex items-center justify-center overflow-hidden"
                :title="member.user?.name || member.user?.username"
              >
                <img
                  v-if="member.user?.avatar_url"
                  :src="member.user.avatar_url"
                  :alt="member.user?.name || member.user?.username"
                  class="w-full h-full object-cover"
                  @error="handleAvatarError"
                />
                <span
                  v-else
                  class="text-xs font-medium text-primary-600 dark:text-primary-400"
                >
                  {{ (member.user?.name || member.user?.username || '?').charAt(0).toUpperCase() }}
                </span>
              </div>
              <div
                v-if="getTeamMembers(team.id).length > 5"
                class="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-800 border-2 border-white dark:border-gray-800 flex items-center justify-center"
              >
                <span class="text-xs font-medium text-gray-600 dark:text-gray-400">
                  +{{ getTeamMembers(team.id).length - 5 }}
                </span>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-700">
            <button
              @click="navigateTo(`/teams/${team.id}`)"
              class="text-sm font-medium text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300"
            >
              {{ $t('teams.viewDetails') }}
            </button>
            
            <div class="flex items-center space-x-2">
              <button
                v-if="isTeamMember(team.id)"
                @click="leaveTeam(team.id)"
                class="text-sm px-3 py-1.5 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                {{ $t('teams.leaveTeam') }}
              </button>
              <button
                v-else-if="team.is_open && !isTeamFull(team)"
                @click="joinTeam(team.id)"
                class="text-sm px-3 py-1.5 rounded-lg bg-primary-600 text-white hover:bg-primary-700"
              >
                {{ $t('teams.joinTeam') }}
              </button>
              <span
                v-else-if="isTeamFull(team)"
                class="text-sm px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400"
              >
                {{ $t('teams.teamFull') }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="teams.length > 0" class="mt-8 flex items-center justify-between">
      <button
        @click="prevPage"
        :disabled="currentPage === 1"
        class="btn btn-outline"
        :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
      >
        {{ $t('teams.previous') }}
      </button>
      <span class="text-gray-600 dark:text-gray-400">
        {{ $t('teams.page', { page: currentPage }) }}
      </span>
      <button
        @click="nextPage"
        :disabled="teams.length < pageSize"
        class="btn btn-outline"
        :class="{ 'opacity-50 cursor-not-allowed': teams.length < pageSize }"
      >
        {{ $t('teams.next') }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from '#app'
import { useAuthStore } from '~/stores/auth'
import { useTeamStore } from '~/stores/team'
import { useUIStore } from '~/stores/ui'

const router = useRouter()
const authStore = useAuthStore()
const teamStore = useTeamStore()
const uiStore = useUIStore()

// State
const teams = ref<any[]>([])
const hackathons = ref<any[]>([])
const filters = ref({
  hackathon_id: '' as string | number,
  is_open: '' as string | boolean,
  search: ''
})
const currentPage = ref(1)
const pageSize = ref(12)
const debounceTimer = ref<NodeJS.Timeout>()

// Computed
const isAuthenticated = computed(() => authStore.isAuthenticated)
const teamMembers = computed(() => teamStore.teamMembers)
const filteredTeams = computed(() => {
  let filtered = teams.value

  // Apply search filter
  if (filters.value.search) {
    const searchLower = filters.value.search.toLowerCase()
    filtered = filtered.filter(team =>
      team.name.toLowerCase().includes(searchLower) ||
      team.description?.toLowerCase().includes(searchLower)
    )
  }

  // Apply hackathon filter
  if (filters.value.hackathon_id) {
    filtered = filtered.filter(team => team.hackathon_id === Number(filters.value.hackathon_id))
  }

  // Apply open/closed filter
  if (filters.value.is_open !== '') {
    filtered = filtered.filter(team => team.is_open === (filters.value.is_open === 'true' || filters.value.is_open === true))
  }

  // Apply pagination
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filtered.slice(start, end)
})

// Methods
function navigateTo(path: string) {
  router.push(path)
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}

function handleCreateTeamClick() {
  if (!isAuthenticated) {
    uiStore.showError('You must be logged in to create a team', 'Authentication Required')
    navigateTo('/login')
    return
  }
  navigateTo('/teams/create')
}

function handleAvatarError(event: Event) {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  // The parent div will show the fallback initials automatically
  // because we're using v-if/v-else
}

function isTeamMember(teamId: number) {
  const members = teamStore.teamMembers.get(teamId) || []
  return members.some(member => member.user_id === authStore.user?.id)
}

function isTeamFull(team: any) {
  return (team.member_count || 0) >= team.max_members
}

function getTeamMembers(teamId: number) {
  return teamStore.teamMembers.get(teamId) || []
}

async function loadTeams() {
  try {
    const params: any = {}
    if (filters.value.hackathon_id) params.hackathon_id = Number(filters.value.hackathon_id)
    if (filters.value.is_open !== '') params.is_open = filters.value.is_open === 'true' || filters.value.is_open === true
    
    const data = await teamStore.fetchTeams(params)
    teams.value = data
  } catch (err) {
    console.error('Failed to load teams:', err)
  }
}

async function loadHackathons() {
  try {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    const response = await authStore.fetchWithAuth(`/api/hackathons?limit=50`)
    
    if (response.ok) {
      hackathons.value = await response.json()
    }
    } catch (err) {
    console.error('Failed to load hackathons:', err)
  }
}

function debouncedLoadTeams() {
  if (debounceTimer.value) {
    clearTimeout(debounceTimer.value)
  }
  debounceTimer.value = setTimeout(() => {
    loadTeams()
  }, 300)
}

async function joinTeam(teamId: number) {
  if (!authStore.user?.id) {
    uiStore.showError('You must be logged in to join a team', 'Authentication Required')
    navigateTo('/login')
    return
  }

  try {
    // For now, we'll just show a message since we need invitation system
    // In a real implementation, this would send a join request or use invitations
    uiStore.showInfo('Open teams can be joined by requesting an invitation from the team owner.', 'Join Team')
    navigateTo(`/teams/${teamId}`)
  } catch (err) {
    console.error('Failed to join team:', err)
  }
}

async function leaveTeam(teamId: number) {
  if (!authStore.user?.id) return

  try {
    const confirmed = confirm('Are you sure you want to leave this team?')
    if (!confirmed) return

    await teamStore.removeTeamMember(teamId, authStore.user.id)
    uiStore.showSuccess('You have left the team')
    await loadTeams()
  } catch (err) {
    console.error('Failed to leave team:', err)
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

function nextPage() {
  if (filteredTeams.value.length === pageSize.value) {
    currentPage.value++
  }
}

// Lifecycle
onMounted(() => {
  loadTeams()
  loadHackathons()
})

// Watch for auth changes
watch(() => authStore.isAuthenticated, (isAuthenticated) => {
  if (isAuthenticated) {
    loadTeams()
  }
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