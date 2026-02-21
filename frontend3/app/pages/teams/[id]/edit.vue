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
    <button @click="loadTeam" class="btn btn-outline">Try Again</button>
  </div>

  <div v-else-if="team" class="container mx-auto px-4 py-8 max-w-2xl">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Edit Team: {{ team.name }}</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        Update your team details and settings
      </p>
    </div>

    <!-- Form -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <form @submit.prevent="updateTeam">
        <!-- Team Name -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Team Name *
          </label>
          <input
            v-model="form.name"
            type="text"
            placeholder="Enter team name"
            class="w-full input"
            required
            :disabled="teamStore.isLoading"
          />
        </div>

        <!-- Description -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Description
          </label>
          <textarea
            v-model="form.description"
            placeholder="Describe your team goals, skills, or project ideas"
            rows="4"
            class="w-full input"
            :disabled="teamStore.isLoading"
          ></textarea>
        </div>

        <!-- Hackathon -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Hackathon *
          </label>
          <select
            v-model="form.hackathon_id"
            class="w-full input"
            required
            :disabled="teamStore.isLoading || loadingHackathons"
          >
            <option value="" disabled>Select a hackathon</option>
            <option v-for="hackathon in hackathons" :key="hackathon.id" :value="hackathon.id">
              {{ hackathon.name }}
            </option>
          </select>
          <p v-if="loadingHackathons" class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Loading hackathons...
          </p>
        </div>

        <!-- Max Members -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Maximum Members
          </label>
          <div class="flex items-center space-x-4">
            <input
              v-model="form.max_members"
              type="range"
              min="1"
              max="10"
              class="w-full"
              :disabled="teamStore.isLoading"
            />
            <span class="text-lg font-medium text-gray-700 dark:text-gray-300 min-w-[3rem]">
              {{ form.max_members }}
            </span>
          </div>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Current members: {{ members.length }}. You cannot set max members below current count.
          </p>
        </div>

        <!-- Team Openness -->
        <div class="mb-6">
          <div class="flex items-center">
            <input
              v-model="form.is_open"
              type="checkbox"
              id="is_open"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              :disabled="teamStore.isLoading"
            />
            <label for="is_open" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
              Open Team
            </label>
          </div>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Open teams can be joined by other users. Closed teams require invitations.
          </p>
        </div>

        <!-- Error Message -->
        <div v-if="teamStore.error" class="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-red-600 dark:text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="text-red-600 dark:text-red-400">{{ teamStore.error }}</span>
          </div>
        </div>

        <!-- Form Actions -->
        <div class="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
          <button
            type="button"
            @click="cancel"
            class="btn btn-outline"
            :disabled="teamStore.isLoading"
          >
            Cancel
          </button>
          <div class="flex space-x-3">
            <button
              type="button"
              @click="deleteTeam"
              class="btn btn-outline text-red-600 dark:text-red-400 border-red-300 dark:border-red-700 hover:bg-red-50 dark:hover:bg-red-900/20"
              :disabled="teamStore.isLoading"
            >
              Delete Team
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="teamStore.isLoading || !formValid"
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