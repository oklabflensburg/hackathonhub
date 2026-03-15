<template>
  <div class="p-4 rounded-lg border border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
    <div class="flex items-center justify-between">
      <!-- Left side: User info -->
      <div class="flex items-center">
        <!-- Avatar -->
        <slot name="avatar" :user="invitedUser">
          <NuxtLink
            v-if="invitedUser"
            :to="`/users/${invitedUser.id}`"
            class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center mr-4 overflow-hidden hover:opacity-90 transition-opacity"
            :title="invitedUser.username"
          >
            <img
              v-if="invitedUser?.avatar_url"
              :src="invitedUser.avatar_url"
              :alt="invitedUser?.username || labels.unknownUser"
              class="w-full h-full object-cover"
              @error="handleAvatarError"
            />
            <span v-else class="text-sm font-medium text-primary-600 dark:text-primary-400">
              {{ (invitedUser?.username || unknownUserInitial).charAt(0).toUpperCase() }}
            </span>
          </NuxtLink>
          <div
            v-else
            class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center mr-4 overflow-hidden"
          >
            <span class="text-sm font-medium text-primary-600 dark:text-primary-400">
              {{ unknownUserInitial }}
            </span>
          </div>
        </slot>

        <!-- User details -->
        <div>
          <div class="font-medium text-gray-900 dark:text-white">
            <NuxtLink
              v-if="invitedUser"
              :to="`/users/${invitedUser.id}`"
              class="hover:text-primary-600 dark:hover:text-primary-400"
            >
              {{ invitedUser.username }}
            </NuxtLink>
            <span v-else>
              {{ labels.unknownUser }}
            </span>
          </div>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            {{ labels.invited }} {{ formattedDate }}
            <span v-if="invitation.inviter && showInviter">
              {{ labels.by }}
              <NuxtLink
                :to="`/users/${invitation.inviter.id}`"
                class="hover:text-primary-600 dark:hover:text-primary-400"
              >
                {{ invitation.inviter.username }}
              </NuxtLink>
            </span>
          </p>
        </div>
      </div>

      <!-- Right side: Status and actions -->
      <div class="flex items-center space-x-3">
        <!-- Status badge -->
        <slot name="status" :status="invitation.status">
          <span
            v-if="showStatus"
            class="text-sm px-2 py-1 rounded-full"
            :class="statusClasses"
          >
            {{ statusLabel }}
          </span>
        </slot>

        <!-- Cancel button -->
        <slot
          name="actions"
          :invitation="invitation"
          :cancel="handleCancel"
        >
          <button
            v-if="showCancelButton"
            @click="handleCancel"
            class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 transition-colors"
            :title="labels.cancel"
            :disabled="cancelling"
          >
            <span v-if="cancelling">
              <svg class="animate-spin h-4 w-4 inline-block mr-1" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              {{ labels.cancelling }}
            </span>
            <span v-else>
              {{ labels.cancel }}
            </span>
          </button>
        </slot>
      </div>
    </div>

    <!-- Team info (optional) -->
    <div v-if="showTeamInfo && invitation.team" class="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700">
      <p class="text-sm text-gray-600 dark:text-gray-400">
        {{ labels.teamLabel }}:
        <NuxtLink
          :to="`/teams/${invitation.team.id}`"
          class="font-medium hover:text-primary-600 dark:hover:text-primary-400"
        >
          {{ invitation.team.name }}
        </NuxtLink>
        <span v-if="invitation.team.hackathon" class="ml-2">
          ({{ invitation.team.hackathon.name }})
        </span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { InvitationItemProps } from '~/types/team-invitations'

const props = withDefaults(defineProps<InvitationItemProps>(), {
  showCancelButton: false,
  showInviter: true,
  showTeamInfo: false,
  showStatus: true,
  formatDate: (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString()
    } catch {
      return dateString
    }
  },
  labels: () => ({
    pending: 'Pending',
    invited: 'Invited',
    by: 'by',
    cancel: 'Cancel',
    cancelling: 'Cancelling...',
    unknownUser: 'Unknown User',
    unknownUserInitial: '?',
    teamLabel: 'Team'
  })
})

const emit = defineEmits<{
  cancel: [invitationId: number]
  click: [invitation: any]
}>()

const cancelling = ref(false)
const invitedUser = computed(() => props.invitation.invited_user ?? null)
const unknownUserInitial = computed(() => (props.labels?.unknownUserInitial ?? '?').charAt(0).toUpperCase())

// Computed
const formattedDate = computed(() => {
  return props.formatDate(props.invitation.created_at)
})

const statusLabel = computed(() => {
  if (props.invitation.status === 'pending') return props.labels?.pending || 'Pending'
  if (props.invitation.status === 'accepted') return 'Accepted'
  if (props.invitation.status === 'declined') return 'Declined'
  return 'Cancelled'
})

const statusClasses = computed(() => {
  switch (props.invitation.status) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
    case 'accepted':
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
    case 'declined':
    case 'cancelled':
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
  }
})

// Methods
function handleAvatarError(event: Event) {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  // The parent div will show the fallback initials automatically
}

async function handleCancel() {
  if (cancelling.value) return
  
  cancelling.value = true
  try {
    emit('cancel', props.invitation.id)
  } finally {
    // Note: We don't reset cancelling here because the parent component
    // should handle the actual cancellation and update the UI
    // If cancellation fails, the parent should handle the error
  }
}

function handleClick() {
  emit('click', props.invitation)
}
</script>

<style scoped>
/* Custom styles if needed */
</style>
