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

    <TeamForm
      :form="form"
      :hackathons="hackathons"
      :loading="teamStore.isLoading"
      :loading-hackathons="loadingHackathons"
      :error="teamStore.error"
      :form-valid="formValid"
      :show-delete="true"
      :labels="{
        teamName: 'Team Name',
        teamNamePlaceholder: 'Enter team name',
        teamNameHelp: '',
        description: 'Description',
        descriptionPlaceholder: 'Describe your team goals, skills, or project ideas',
        descriptionHelp: '',
        hackathon: 'Hackathon',
        selectHackathon: 'Select a hackathon',
        hackathonHelp: '',
        maxMembers: 'Maximum Members',
        maxMembersHelp: `Current members: ${members.length}. You cannot set max members below current count.`,
        openTeam: 'Open Team',
        openTeamHelp: 'Open teams can be joined by other users. Closed teams require invitations.',
        cancel: 'Cancel',
        delete: 'Delete Team',
        saving: 'Saving...',
        submit: 'Save Changes'
      }"
      @submit="updateTeam"
      @cancel="cancel"
      @delete="deleteTeam"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from '#app'
import { useTeamStore } from '~/stores/team'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import TeamForm from '~/components/teams/TeamForm.vue'

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