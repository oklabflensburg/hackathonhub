<template>
  <div class="container mx-auto px-4 py-8 max-w-2xl">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ $t('teams.createTeam') }}</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        {{ $t('teams.createTeamDescription', 'Create a new team for a hackathon') }}
      </p>
    </div>

    <!-- Simple Team Creation Form -->
    <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <form @submit.prevent="createTeam">
        <!-- Team Name -->
        <div class="mb-6">
          <label for="team-name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ $t('teams.teamName') }} *
          </label>
          <input
            id="team-name"
            v-model="form.name"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
            :placeholder="$t('teams.teamNamePlaceholder')"
          />
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
            {{ $t('teams.teamNameHelp', 'Choose a descriptive name for your team') }}
          </p>
        </div>

        <!-- Description -->
        <div class="mb-6">
          <label for="team-description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ $t('teams.teamDescription') }}
          </label>
          <textarea
            id="team-description"
            v-model="form.description"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
            :placeholder="$t('teams.teamDescriptionPlaceholder')"
          />
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
            {{ $t('teams.teamDescriptionHelp', 'Describe your team goals, skills, or project ideas') }}
          </p>
        </div>

        <!-- Hackathon -->
        <div class="mb-6">
          <label for="hackathon" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ $t('teams.hackathon') }} *
          </label>
          <select
            id="hackathon"
            v-model="form.hackathon_id"
            required
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
          >
            <option value="" disabled>{{ $t('teams.selectHackathon') }}</option>
            <option v-for="hackathon in hackathons" :key="hackathon.id" :value="hackathon.id">
              {{ hackathon.name }} ({{ formatDate(hackathon.start_date) }} - {{ formatDate(hackathon.end_date) }})
            </option>
          </select>
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
            {{ $t('teams.hackathonHelp', 'Select the hackathon this team will participate in') }}
          </p>
        </div>

        <!-- Max Members -->
        <div class="mb-6">
          <label for="max-members" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ $t('teams.maxMembers') }}
          </label>
          <div class="flex items-center space-x-4">
            <input
              id="max-members"
              v-model="form.max_members"
              type="range"
              min="1"
              max="10"
              class="flex-1"
            />
            <span class="text-lg font-medium text-gray-700 dark:text-gray-300">{{ form.max_members }}</span>
          </div>
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
            {{ $t('teams.maxMembersHelp', 'Maximum number of team members (1-10)') }}
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
              {{ $t('teams.openTeam') }}
            </label>
          </div>
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
            {{ $t('teams.openTeamHelp', 'Open teams can be joined by other users. Closed teams require invitations.') }}
          </p>
        </div>

        <!-- Error Message -->
        <div v-if="teamStore.error" class="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
          <p class="text-sm text-red-600 dark:text-red-400">{{ teamStore.error }}</p>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
          <button
            type="button"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
            @click="cancel"
          >
            {{ $t('teams.cancel') }}
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
              {{ $t('teams.creating') }}
            </span>
            <span v-else>
              {{ $t('teams.createTeam') }}
            </span>
          </button>
        </div>
      </form>
    </div>

    <!-- Loading hackathons -->
    <div v-if="loadingHackathons" class="mt-8 text-center">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      <p class="mt-2 text-gray-600 dark:text-gray-400">{{ $t('teams.loadingHackathons') }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from '#app'
import { useTeamStore } from '~/stores/team'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

const router = useRouter()
const teamStore = useTeamStore()
const authStore = useAuthStore()
const uiStore = useUIStore()

// State
const form = ref({
  name: '',
  description: '',
  hackathon_id: '' as string | number,
  max_members: 5,
  is_open: true
})

const hackathons = ref<any[]>([])
const loadingHackathons = ref(false)

// Computed
const formValid = computed(() => {
  return form.value.name.trim() !== '' && form.value.hackathon_id !== ''
})

// Methods
function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}

async function loadHackathons() {
  loadingHackathons.value = true
  try {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    const response = await authStore.fetchWithAuth(`/api/hackathons?limit=50&is_active=true`)
    
    if (response.ok) {
      hackathons.value = await response.json()
    }
  } catch (err) {
    console.error('Failed to load hackathons:', err)
    uiStore.showError('Failed to load hackathons', 'Error')
  } finally {
    loadingHackathons.value = false
  }
}

async function createTeam() {
  if (!formValid.value) return

  try {
    const teamData = {
      name: form.value.name.trim(),
      description: form.value.description.trim(),
      hackathon_id: Number(form.value.hackathon_id),
      max_members: form.value.max_members,
      is_open: form.value.is_open
    }

    const team = await teamStore.createTeam(teamData)
    
    // Redirect to team page
    router.push(`/teams/${team.id}`)
  } catch (err) {
    // Error is already handled by team store
    console.error('Failed to create team:', err)
  }
}

function cancel() {
  router.push('/teams')
}

// Lifecycle
onMounted(() => {
  loadHackathons()
  
  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    uiStore.showError('You must be logged in to create a team', 'Authentication Required')
    router.push('/login')
  }
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