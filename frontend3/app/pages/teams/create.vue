<template>
  <div class="container mx-auto px-4 py-8 max-w-2xl">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ $t('teams.createTeam') }}</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        {{ $t('teams.createTeamDescription', 'Create a new team for a hackathon') }}
      </p>
    </div>

    <TeamForm
      :form="form"
      :hackathons="hackathons"
      :loading="teamStore.isLoading"
      :loading-hackathons="loadingHackathons"
      :error="teamStore.error"
      :form-valid="formValid"
      :labels="{
        teamName: $t('teams.teamName'),
        teamNamePlaceholder: $t('teams.teamNamePlaceholder'),
        teamNameHelp: $t('teams.teamNameHelp', 'Choose a descriptive name for your team'),
        description: $t('teams.teamDescription'),
        descriptionPlaceholder: $t('teams.teamDescriptionPlaceholder'),
        descriptionHelp: $t('teams.teamDescriptionHelp', 'Describe your team goals, skills, or project ideas'),
        hackathon: $t('teams.hackathon'),
        selectHackathon: $t('teams.selectHackathon'),
        hackathonHelp: $t('teams.hackathonHelp', 'Select the hackathon this team will participate in'),
        maxMembers: $t('teams.maxMembers'),
        maxMembersHelp: $t('teams.maxMembersHelp', 'Maximum number of team members (1-10)'),
        openTeam: $t('teams.openTeam'),
        openTeamHelp: $t('teams.openTeamHelp', 'Open teams can be joined by other users. Closed teams require invitations.'),
        cancel: $t('teams.cancel'),
        delete: $t('teams.deleteTeam'),
        saving: $t('teams.creating'),
        submit: $t('teams.createTeam')
      }"
      @submit="createTeam"
      @cancel="cancel"
    />

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
import TeamForm from '~/components/teams/TeamForm.vue'

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