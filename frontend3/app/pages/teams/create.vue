<template>
  <div class="container mx-auto px-4 py-8 max-w-2xl">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ $t('teams.createTeam') }}</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        {{ $t('teams.createTeamDescription', 'Create a new team for a hackathon') }}
      </p>
    </div>

    <!-- Form -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <form @submit.prevent="createTeam">
        <!-- Team Name -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ $t('teams.teamName') }} *
          </label>
          <input
            v-model="form.name"
            type="text"
            :placeholder="$t('teams.teamNamePlaceholder')"
            class="w-full input"
            required
            :disabled="teamStore.isLoading"
          />
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {{ $t('teams.teamNameHelp', 'Choose a descriptive name for your team') }}
          </p>
        </div>

        <!-- Description -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ $t('teams.teamDescription') }}
          </label>
          <textarea
            v-model="form.description"
            :placeholder="$t('teams.teamDescriptionPlaceholder')"
            rows="4"
            class="w-full input"
            :disabled="teamStore.isLoading"
          ></textarea>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {{ $t('teams.teamDescriptionHelp', 'Describe your team goals, skills, or project ideas') }}
          </p>
        </div>

        <!-- Hackathon Selection -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ $t('teams.hackathon') }} *
          </label>
          <select
            v-model="form.hackathon_id"
            class="w-full input"
            required
            :disabled="teamStore.isLoading || hackathons.length === 0"
          >
            <option value="">{{ $t('teams.selectHackathon') }}</option>
            <option v-for="hackathon in hackathons" :key="hackathon.id" :value="hackathon.id">
              {{ hackathon.name }} ({{ formatDate(hackathon.start_date) }} - {{ formatDate(hackathon.end_date) }})
            </option>
          </select>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {{ $t('teams.hackathonHelp', 'Select the hackathon this team will participate in') }}
          </p>
        </div>

        <!-- Max Members -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ $t('teams.maxMembers') }}
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
            {{ $t('teams.maxMembersHelp', 'Maximum number of team members (1-10)') }}
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
              {{ $t('teams.openTeam') }}
            </label>
          </div>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {{ $t('teams.openTeamHelp', 'Open teams can be joined by other users. Closed teams require invitations.') }}
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
            {{ $t('teams.cancel') }}
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