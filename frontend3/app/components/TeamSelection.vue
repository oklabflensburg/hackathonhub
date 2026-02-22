<template>
  <div class="team-selection">
    <!-- Loading state -->
    <div v-if="loading" class="mb-4">
      <div class="flex items-center">
        <div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary-600 mr-2"></div>
        <span class="text-gray-600 dark:text-gray-400 text-sm">
          {{ $t('teams.loadingTeams') || 'Loading teams...' }}
        </span>
      </div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
      <p class="text-red-700 dark:text-red-300 text-sm">{{ error }}</p>
      <button 
        @click="fetchTeams" 
        class="mt-2 text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300"
      >
        {{ $t('common.retry') || 'Retry' }}
      </button>
    </div>

    <!-- Team selection -->
    <div v-else class="space-y-4">
      <!-- Team selection dropdown -->
      <div v-if="teams.length > 0">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          {{ $t('teams.selectTeamForProject') || 'Select Team for Project' }}
          <span class="text-gray-500 dark:text-gray-400 text-xs ml-1">({{ $t('common.optional') || 'Optional' }})</span>
        </label>
        
        <select
          v-model="selectedTeamId"
          class="w-full input"
          :disabled="disabled"
          @change="onTeamSelected"
        >
          <option :value="null">
            {{ $t('teams.noTeamIndividualProject') || 'No team - Individual project' }}
          </option>
          <option 
            v-for="team in teams" 
            :key="team.id" 
            :value="team.id"
          >
            {{ team.name }}
            <template v-if="team.member_count !== undefined">
              ({{ team.member_count }} {{ $t('teams.members') || 'members' }})
            </template>
          </option>
        </select>
        
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          {{ $t('teams.teamSelectionHelp') || 'Select a team to create a team project, or leave empty for an individual project' }}
        </p>
      </div>

      <!-- No teams message -->
      <div v-else class="mb-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
        <div class="flex items-start">
          <svg class="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <p class="text-blue-800 dark:text-blue-300 text-sm font-medium mb-1">
              {{ $t('teams.noTeamsForHackathon') || 'No teams for this hackathon' }}
            </p>
            <p class="text-blue-700 dark:text-blue-400 text-sm">
              {{ $t('teams.createTeamToCollaborate') || 'Create a team to collaborate with others on projects' }}
            </p>
            <div class="mt-3">
              <NuxtLink
                :to="`/teams/create?hackathon_id=${hackathonId}`"
                class="inline-flex items-center text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium"
              >
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                {{ $t('teams.createNewTeam') || 'Create New Team' }}
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>

      <!-- Selected team info -->
      <div v-if="selectedTeam && selectedTeamId" class="mt-4 p-4 bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-lg">
        <div class="flex items-center justify-between">
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white">
              {{ selectedTeam.name }}
            </h4>
            <p v-if="selectedTeam.description" class="text-sm text-gray-600 dark:text-gray-400 mt-1">
              {{ selectedTeam.description }}
            </p>
            <div class="flex items-center mt-2 text-sm text-gray-500 dark:text-gray-400">
              <span class="flex items-center mr-4">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                {{ selectedTeam.member_count || 0 }} {{ $t('teams.members') || 'members' }}
              </span>
              <NuxtLink 
                :to="`/teams/${selectedTeam.id}`"
                class="text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300 hover:underline"
              >
                {{ $t('teams.viewTeamDetails') || 'View team details' }}
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue'
import { useTeamStore } from '~/stores/team'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

const props = defineProps<{
  hackathonId: number | string
  modelValue?: number | null
  disabled?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number | null]
  'team-selected': [teamId: number | null]
}>()

const teamStore = useTeamStore()
const authStore = useAuthStore()
const uiStore = useUIStore()

const loading = ref(false)
const error = ref<string | null>(null)
const teams = ref<any[]>([])
const selectedTeamId = ref<number | null>(props.modelValue || null)

const selectedTeam = computed(() => {
  if (!selectedTeamId.value) return null
  return teams.value.find(team => team.id === selectedTeamId.value)
})

// Fetch teams for the hackathon
async function fetchTeams() {
  if (!props.hackathonId) return
  
  loading.value = true
  error.value = null
  
  try {
    // Convert hackathonId to number if it's a string
    const hackathonIdNum = typeof props.hackathonId === 'string' 
      ? parseInt(props.hackathonId) 
      : props.hackathonId
    
    if (isNaN(hackathonIdNum)) {
      throw new Error('Invalid hackathon ID')
    }
    
    const userTeams = await teamStore.fetchUserTeamsForHackathon(hackathonIdNum as number)
    teams.value = userTeams
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load teams'
    uiStore.showError(error.value, 'Team Error')
  } finally {
    loading.value = false
  }
}

function onTeamSelected() {
  emit('update:modelValue', selectedTeamId.value)
  emit('team-selected', selectedTeamId.value)
}

// Watch for hackathonId changes
watch(() => props.hackathonId, (newHackathonId) => {
  if (newHackathonId) {
    fetchTeams()
    // Reset selection when hackathon changes
    selectedTeamId.value = null
    emit('update:modelValue', null)
    emit('team-selected', null)
  }
})

// Watch for modelValue changes from parent
watch(() => props.modelValue, (newValue) => {
  selectedTeamId.value = newValue || null
})

onMounted(() => {
  if (props.hackathonId) {
    fetchTeams()
  }
})
</script>

<style scoped>
.team-selection {
  transition: all 0.2s ease;
}

.input {
  @apply w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg 
         bg-white dark:bg-gray-800 text-gray-900 dark:text-white 
         focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
         disabled:opacity-50 disabled:cursor-not-allowed;
}
</style>