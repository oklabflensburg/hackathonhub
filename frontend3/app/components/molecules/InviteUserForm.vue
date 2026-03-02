<template>
  <div class="invite-user-form">
    <!-- Form header (optional) -->
    <div v-if="showTitle && title" class="mb-4">
      <h4 class="text-md font-medium text-gray-900 dark:text-white">{{ title }}</h4>
      <p v-if="helpText && showHelpText" class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ helpText }}</p>
    </div>

    <!-- Member count (optional) -->
    <div v-if="showMemberCount && maxMembers" class="mb-4">
      <p class="text-sm text-gray-600 dark:text-gray-400">
        {{ memberCountLabel }}
      </p>
      <div v-if="maxMembers" class="mt-1 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
        <div
          class="bg-primary-600 dark:bg-primary-500 h-2 rounded-full transition-all duration-300"
          :style="{ width: memberPercentage + '%' }"
        ></div>
      </div>
    </div>

    <!-- Team full message -->
    <div v-if="isTeamFull" class="mb-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
      <p class="text-sm text-yellow-800 dark:text-yellow-200">
        {{ teamFullMessage }}
      </p>
    </div>

    <!-- Search input and button -->
    <div class="relative" :class="{ 'opacity-50 pointer-events-none': disabled }">
      <div class="flex space-x-3">
        <!-- Search input -->
        <div class="flex-1 relative">
          <UserSearchInput
            v-model="searchQuery"
            :suggestions="searchResults"
            :loading="searchLoading"
            :placeholder="placeholder"
            :min-chars="2"
            :max-suggestions="5"
            :disabled="disabled || isTeamFull"
            @select="handleUserSelect"
            @search="handleSearch"
          />
        </div>

        <!-- Invite button -->
        <button
          @click="handleInvite"
          class="btn btn-primary whitespace-nowrap"
          :disabled="!canInvite || inviting || disabled || isTeamFull"
          :class="{ 'opacity-50 cursor-not-allowed': !canInvite || disabled || isTeamFull }"
        >
          <span v-if="inviting">
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 inline-block" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            {{ invitingLabel }}
          </span>
          <span v-else>
            {{ buttonLabel }}
          </span>
        </button>
      </div>

      <!-- Help text -->
      <p v-if="!isTeamFull && helpTextInline" class="text-sm text-gray-500 dark:text-gray-400 mt-2">
        {{ helpTextInline }}
      </p>

      <!-- Search error message -->
      <div v-if="searchError" class="mt-2 p-2 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
        <p class="text-sm text-red-600 dark:text-red-400">{{ searchError }}</p>
      </div>

      <!-- Invite error message -->
      <div v-if="inviteError" class="mt-2 p-2 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
        <p class="text-sm text-red-600 dark:text-red-400">{{ inviteError }}</p>
      </div>

      <!-- Success message -->
      <div v-if="success" class="mt-2 p-2 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
        <p class="text-sm text-green-600 dark:text-green-400">{{ success }}</p>
      </div>
    </div>

    <!-- Selected user preview -->
    <div v-if="selectedUser" class="mt-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <div class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center mr-3 overflow-hidden">
            <img
              v-if="selectedUser.avatar_url"
              :src="selectedUser.avatar_url"
              :alt="selectedUser.username"
              class="w-full h-full object-cover"
            />
            <span v-else class="text-xs font-medium text-primary-600 dark:text-primary-400">
              {{ selectedUser.username.charAt(0).toUpperCase() }}
            </span>
          </div>
          <div>
            <div class="font-medium text-gray-900 dark:text-white">{{ selectedUser.username }}</div>
            <div v-if="selectedUser.name" class="text-sm text-gray-500 dark:text-gray-400">{{ selectedUser.name }}</div>
          </div>
        </div>
        <button
          @click="clearSelection"
          class="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
        >
          {{ clearLabel }}
        </button>
      </div>
    </div>

    <!-- Slot for additional content -->
    <slot name="after-form"></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import UserSearchInput from './UserSearchInput.vue'
import { useUserSearch } from '~/composables/useUserSearch'
import { useTeamStore } from '~/stores/team'
import { useUIStore } from '~/stores/ui'
import type { InviteUserFormProps, UserSearchResult } from '~/types/team-invitations'

const props = withDefaults(defineProps<InviteUserFormProps>(), {
  maxMembers: 5,
  currentMemberCount: 0,
  disabled: false,
  placeholder: 'Enter username',
  buttonLabel: 'Invite',
  helpText: 'Invite members to your team',
  showMemberCount: true,
  showTitle: false,
  showHelpText: true,
  excludeUserIds: () => []
})

const emit = defineEmits<{
  'invite-sent': [{ userId: number, username: string }]
  'error': [{ message: string, code?: string }]
  'search': [{ query: string }]
  'user-select': [{ user: UserSearchResult }]
}>()

const { t } = useI18n()
const teamStore = useTeamStore()
const uiStore = useUIStore()

// Use the user search composable
const {
  query: searchQuery,
  results: searchResults,
  loading: searchLoading,
  error: searchError,
  selectedUser,
  search,
  selectUser,
  clear: clearSearch
} = useUserSearch({
  debounceMs: 300,
  minQueryLength: 2,
  excludeUserIds: props.excludeUserIds
})

// Local state
const inviting = ref(false)
const inviteError = ref<string | null>(null)
const success = ref<string | null>(null)

// Computed
const isTeamFull = computed(() => {
  return props.currentMemberCount >= props.maxMembers
})

const memberCountLabel = computed(() => {
  return t('teams.memberCount', {
    current: props.currentMemberCount,
    max: props.maxMembers
  }) || `${props.currentMemberCount}/${props.maxMembers} members`
})

const memberPercentage = computed(() => {
  if (!props.maxMembers) return 0
  return Math.min(100, (props.currentMemberCount / props.maxMembers) * 100)
})

const teamFullMessage = computed(() => {
  return t('teams.teamFull') || 'Team is full. Cannot invite more members.'
})

const canInvite = computed(() => {
  return !!selectedUser.value && !isTeamFull.value
})

const invitingLabel = computed(() => {
  return t('teams.inviting') || 'Inviting...'
})

const clearLabel = computed(() => {
  return t('common.clear') || 'Clear'
})

const helpTextInline = computed(() => {
  if (props.helpText) return props.helpText
  return t('teams.inviteHelp') || 'Enter a username to invite them to your team'
})

const title = computed(() => {
  return props.helpText // Can be overridden by parent component if needed
})

// Methods
function handleUserSelect(user: UserSearchResult) {
  selectUser(user)
  inviteError.value = null
  emit('user-select', { user })
}

async function handleSearch(query: string) {
  emit('search', { query })
  // Trigger API search through the composable
  await search(query)
}

async function handleInvite() {
  if (!selectedUser.value || inviting.value || isTeamFull.value) return

  inviting.value = true
  inviteError.value = null
  success.value = null

  try {
    // Send invitation directly via team store
    await teamStore.inviteToTeam(props.teamId, selectedUser.value.id)
    
    // Emit event to parent component
    emit('invite-sent', {
      userId: selectedUser.value.id,
      username: selectedUser.value.username
    })

    // Show success message
    success.value = t('teams.invitationSent') || 'Invitation sent successfully'

    // Clear selection after a delay
    setTimeout(() => {
      clearSelection()
      success.value = null
    }, 3000)
  } catch (err) {
    // Fehler vom Composable oder Store
    const errorMsg = err instanceof Error ? err.message : 'Failed to send invitation'
    inviteError.value = errorMsg
    emit('error', { message: errorMsg })
  } finally {
    inviting.value = false
  }
}

function clearSelection() {
  clearSearch()
  inviteError.value = null
  success.value = null
}

// Watch for teamId changes to reset form
watch(() => props.teamId, () => {
  clearSelection()
})

// Watch for disabled prop
watch(() => props.disabled, (newVal) => {
  if (newVal) {
    clearSelection()
  }
})
</script>

<style scoped>
/* Custom styles */
.invite-user-form .btn:disabled {
  @apply cursor-not-allowed;
}
</style>