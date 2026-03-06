<template>
  <div v-if="loading" class="container mx-auto px-4 py-8 text-center">
    <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    <p class="mt-4 text-gray-600 dark:text-gray-400">Loading team...</p>
  </div>

  <div v-else-if="error" class="container mx-auto px-4 py-8 text-center">
    <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400 mb-4">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </div>
    <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Error Loading Team</h3>
    <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
    <button @click="loadTeam" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700">
      Try Again
    </button>
  </div>

  <div v-else-if="team" class="container mx-auto px-4 py-8 max-w-2xl">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Edit Team: {{ team.name }}</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">Update your team details and settings</p>
    </div>

    <!-- Simple Edit Form -->
    <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <form @submit.prevent="updateTeam">
        <!-- Team Name -->
        <div class="mb-6">
          <label for="team-name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Team Name *
          </label>
          <input
            id="team-name"
            v-model="form.name"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
            placeholder="Enter team name"
          />
        </div>

        <!-- Description -->
        <div class="mb-6">
          <label for="team-description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Description
          </label>
          <textarea
            id="team-description"
            v-model="form.description"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
            placeholder="Describe your team goals, skills, or project ideas"
          />
        </div>

        <!-- Hackathon -->
        <div class="mb-6">
          <label for="hackathon" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Hackathon *
          </label>
          <select
            id="hackathon"
            v-model="form.hackathon_id"
            required
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
          >
            <option value="" disabled>Select a hackathon</option>
            <option v-for="hackathon in hackathons" :key="hackathon.id" :value="hackathon.id">
              {{ hackathon.name }}
            </option>
          </select>
        </div>

        <!-- Max Members -->
        <div class="mb-6">
          <label for="max-members" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Maximum Members (Current: {{ members.length }})
          </label>
          <div class="flex items-center space-x-4">
            <input
              id="max-members"
              v-model="form.max_members"
              type="range"
              :min="members.length"
              max="10"
              class="flex-1"
            />
            <span class="text-lg font-medium text-gray-700 dark:text-gray-300">{{ form.max_members }}</span>
          </div>
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
            You cannot set max members below current count.
          </p>
        </div>

        <!-- Open Team -->
        <div class="mb-8">
          <div class="flex items-center">
            <input
              id="open-team"
              v-model="form.is_open"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600 rounded"
            />
            <label for="open-team" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
              Open Team
            </label>
          </div>
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
            Open teams can be joined by other users. Closed teams require invitations.
          </p>
        </div>

        <!-- Error Message -->
        <div v-if="teamStore.error" class="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
          <p class="text-sm text-red-600 dark:text-red-400">{{ teamStore.error }}</p>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
          <div>
            <button
              type="button"
              @click="deleteTeam"
              class="px-4 py-2 border border-red-300 dark:border-red-700 rounded-md shadow-sm text-sm font-medium text-red-700 dark:text-red-300 bg-white dark:bg-gray-800 hover:bg-red-50 dark:hover:bg-red-900/30"
            >
              Delete Team
            </button>
          </div>
          <div class="flex space-x-4">
            <button
              type="button"
              class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
              @click="cancel"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="teamStore.isLoading || !formValid"
              class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="teamStore.isLoading" class="flex items-center">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Saving...
              </span>
              <span v-else>
                Save Changes
              </span>
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from '#app'
import { useTeamStore } from '~/stores/team'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

const route = useRoute()
const router = useRouter()
const teamStore = useTeamStore()
const authStore = useAuthStore()
const uiStore = useUIStore()

// State
const loading = ref(true)
const error = ref<string | null>(null)
const team = ref<any>(null)
const members = ref<any[]>([])
const hackathons = ref<any[]>([])
const loadingHackathons = ref(false)

const form = ref({
  name: '',
  description: '',
  hackathon_id: 0,
  max_members: 5,
  is_open: true
})

// Computed
const teamId = computed(() => Number(route.params.id))
const formValid = computed(() => {
  return form.value.name.trim() !== '' && 
         form.value.hackathon_id > 0 && 
         form.value.max_members >= members.value.length
})

// Methods
async function fetchHackathons() {
  loadingHackathons.value = true
  try {
    const response = await authStore.fetchWithAuth('/api/hackathons?limit=100')
    if (!response.ok) {
      throw new Error(`Failed to fetch hackathons: ${response.status}`)
    }
    const data = await response.json()
    hackathons.value = data
  } catch (err) {
    console.error('Failed to fetch hackathons:', err)
  } finally {
    loadingHackathons.value = false
  }
}

async function loadTeam() {
  loading.value = true
  error.value = null
  
  try {
    // Fetch hackathons and team in parallel
    const [_, teamData] = await Promise.all([fetchHackathons(), teamStore.fetchTeam(teamId.value)])
    
    team.value = teamData
    members.value = teamStore.teamMembers.get(teamId.value) || []
    
    // Initialize form
    form.value = {
      name: team.value.name,
      description: team.value.description || '',
      hackathon_id: team.value.hackathon_id,
      max_members: team.value.max_members,
      is_open: team.value.is_open
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load team'
    console.error('Failed to load team:', err)
  } finally {
    loading.value = false
  }
}

async function updateTeam() {
  if (!formValid.value) return

  try {
    const teamData = {
      name: form.value.name.trim(),
      description: form.value.description.trim(),
      hackathon_id: form.value.hackathon_id,
      max_members: form.value.max_members,
      is_open: form.value.is_open
    }

    const updatedTeam = await teamStore.updateTeam(teamId.value, teamData)
    
    // Redirect to team page
    router.push(`/teams/${updatedTeam.id}`)
  } catch (err) {
    // Error is already handled by team store
    console.error('Failed to update team:', err)
  }
}

async function deleteTeam() {
  try {
    const confirmed = confirm('Are you sure you want to delete this team? This action cannot be undone.')
    if (!confirmed) return

    await teamStore.deleteTeam(teamId.value)
    uiStore.showSuccess('Team deleted successfully')
    router.push('/teams')
  } catch (err) {
    console.error('Failed to delete team:', err)
  }
}

function cancel() {
  router.push(`/teams/${teamId.value}`)
}

// Lifecycle
onMounted(() => {
  loadTeam()
})
</script>

<style scoped>
.container {
  max-width: 42rem;
}

input[type="range"] {
  -webkit-appearance: none;
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  outline: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: #3b82f6;
  border-radius: 50%;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #3b82f6;
  border-radius: 50%;
  cursor: pointer;
  border: none;
}

.dark input[type="range"] {
  background: #4b5563;
}

.dark input[type="range"]::-webkit-slider-thumb {
  background: #60a5fa;
}

.dark input[type="range"]::-moz-range-thumb {
  background: #60a5fa;
}
</style>