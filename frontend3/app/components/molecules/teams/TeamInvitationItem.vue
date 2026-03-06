<template>
  <div class="team-invitation-item" :class="itemClasses">
    <!-- Invitation Info -->
    <div class="invitation-info">
      <!-- Invited User Avatar & Info -->
      <div class="invited-user-info">
        <div v-if="invitation.invitedUser" class="flex items-center space-x-3">
          <TeamMemberAvatar
            :member="invitation.invitedUser"
            size="md"
            :show-name="true"
          />
          <div class="user-details">
            <div class="user-name-role">
              <span class="user-name">
                {{ invitation.invitedUser.displayName || invitation.invitedUser.username }}
              </span>
              <TeamRoleBadge
                :role="invitation.role"
                size="sm"
                class="ml-2"
              />
            </div>
            <div class="invitation-details">
              <span class="invited-by text-sm text-gray-600 dark:text-gray-400">
                Invited by {{ invitation.invitedByUser?.displayName || 'unknown' }}
              </span>
              <span class="invitation-date text-xs text-gray-500 dark:text-gray-400 ml-3">
                {{ formatDate(invitation.createdAt) }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- Email Invitation -->
        <div v-else-if="invitation.invitedEmail" class="email-invitation">
          <div class="flex items-center space-x-3">
            <div class="avatar-placeholder">
              <div class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <div class="email-details">
              <div class="email-address font-medium text-gray-900 dark:text-gray-100">
                {{ invitation.invitedEmail }}
              </div>
              <div class="invitation-status">
                <TeamInvitationStatus
                  :status="invitation.status"
                  size="sm"
                  :show-label="true"
                />
                <span class="invited-by text-sm text-gray-600 dark:text-gray-400 ml-3">
                  Invited by {{ invitation.invitedByUser?.displayName || 'unknown' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Invitation Message -->
      <div v-if="invitation.message" class="invitation-message mt-2">
        <div class="text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
          <span class="font-medium">Message:</span> {{ invitation.message }}
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div v-if="showActions" class="invitation-actions">
      <!-- Status-based actions -->
      <div v-if="invitation.status === 'pending'" class="pending-actions">
        <!-- For invited user (current user is the invitee) -->
        <div v-if="isInvitedToCurrentUser" class="accept-reject-buttons">
          <button
            type="button"
            class="accept-button inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            :disabled="processing"
            @click="handleAccept"
          >
            <span v-if="processingAccept" class="flex items-center">
              <svg class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Accepting...
            </span>
            <span v-else class="flex items-center">
              <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              Accept
            </span>
          </button>
          <button
            type="button"
            class="reject-button ml-2 inline-flex items-center px-3 py-1.5 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
            :disabled="processing"
            @click="handleReject"
          >
            <span v-if="processingReject" class="flex items-center">
              <svg class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Rejecting...
            </span>
            <span v-else class="flex items-center">
              <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Reject
            </span>
          </button>
        </div>
        
        <!-- For inviter (current user sent the invitation) -->
        <div v-else-if="canManageInvitation" class="inviter-actions">
          <button
            type="button"
            class="resend-button inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            :disabled="processing"
            @click="handleResend"
          >
            <span v-if="processingResend" class="flex items-center">
              <svg class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Resending...
            </span>
            <span v-else class="flex items-center">
              <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Resend
            </span>
          </button>
          <button
            type="button"
            class="cancel-button ml-2 inline-flex items-center px-3 py-1.5 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
            :disabled="processing"
            @click="handleCancel"
          >
            <span v-if="processingCancel" class="flex items-center">
              <svg class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Cancelling...
            </span>
            <span v-else class="flex items-center">
              <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Cancel
            </span>
          </button>
        </div>
      </div>
      
      <!-- Status display for non-pending invitations -->
      <div v-else class="status-display">
        <TeamInvitationStatus
          :status="invitation.status"
          size="md"
          :show-label="true"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { TeamInvitationItemProps } from '~/types/team-types'
import TeamMemberAvatar from '~/components/atoms/teams/TeamMemberAvatar.vue'
import TeamRoleBadge from '~/components/atoms/teams/TeamRoleBadge.vue'
import TeamInvitationStatus from '~/components/atoms/teams/TeamInvitationStatus.vue'

const props = withDefaults(defineProps<TeamInvitationItemProps>(), {
  currentUserId: null,
  showActions: true,
})

const emit = defineEmits<{
  accept: [invitationId: string]
  reject: [invitationId: string]
  resend: [invitationId: string]
  cancel: [invitationId: string]
}>()

const processing = ref(false)
const processingAccept = ref(false)
const processingReject = ref(false)
const processingResend = ref(false)
const processingCancel = ref(false)

// Berechne Berechtigungen
const isInvitedToCurrentUser = computed(() => {
  return props.invitation.invitedUser?.id === props.currentUserId
})

const isInviter = computed(() => {
  return props.invitation.invitedByUserId === props.currentUserId
})

const isTeamOwner = computed(() => {
  return props.currentUserId === props.team.createdBy
})

const canManageInvitation = computed(() => {
  return isInviter.value || isTeamOwner.value
})

// CSS-Klassen
const itemClasses = computed(() => ({
  'pending': props.invitation.status === 'pending',
  'accepted': props.invitation.status === 'accepted',
  'rejected': props.invitation.status === 'rejected',
  'expired': props.invitation.status === 'expired',
  'has-actions': props.showActions,
}))

// Formatierungsfunktionen
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

// Event-Handler
const handleAccept = () => {
  if (confirm('Accept this team invitation?')) {
    processing.value = true
    processingAccept.value = true
    emit('accept', props.invitation.id)
    // Reset processing state after a delay
    setTimeout(() => {
      processing.value = false
      processingAccept.value = false
    }, 3000)
  }
}

const handleReject = () => {
  if (confirm('Reject this team invitation?')) {
    processing.value = true
    processingReject.value = true
    emit('reject', props.invitation.id)
    setTimeout(() => {
      processing.value = false
      processingReject.value = false
    }, 3000)
  }
}

const handleResend = () => {
  if (confirm('Resend this invitation?')) {
    processing.value = true
    processingResend.value = true
    emit('resend', props.invitation.id)
    setTimeout(() => {
      processing.value = false
      processingResend.value = false
    }, 3000)
  }
}

const handleCancel = () => {
  if (confirm('Cancel this invitation?')) {
    processing.value = true
    processingCancel.value = true
    emit('cancel', props.invitation.id)
    setTimeout(() => {
      processing.value = false
      processingCancel.value = false
    }, 3000)
  }
}
</script>

<style scoped>
.team-invitation-item {
  @apply p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200;
}

.invitation-info {
  @apply flex-1;
}

.invited-user-info {
  @apply mb-2;
}

.user-details {
  @apply flex-1 min-w-0;
}

.user-name-role {
  @apply flex items-center mb-1;
}

.user-name {
  @apply text-sm font-medium text-gray-900 dark:text-gray-100;
}

.invitation-details {
  @apply flex items-center text-sm;
}

.email-invitation {
  @apply mb-2;
}

.email-details {
  @apply flex-1;
}

.email-address {
  @apply text-sm font-medium mb-1;
}

.invitation-status {
  @apply flex items-center;
}

.invitation-message {
  @apply mt-2;
}

.invitation-actions {
  @apply mt-3 flex items-center justify-end;
}

.pending-actions {
  @apply flex items-center;
}

.accept-reject-buttons {
  @apply flex items-center;
}

.inviter-actions {
  @apply flex items-center;
}

.status-display {
  @apply flex items-center;
}

/* Status-based styling */
.team-invitation-item.pending {
  @apply border-l-4 border-l-yellow-500;
}

.team-invitation-item.accepted {
  @apply border-l-4 border-l-green-500;
}

.team-invitation-item.rejected {
  @apply border-l-4 border-l-red-500;
}

.team-invitation-item.expired {
  @apply border-l-4 border-l-gray-500;
}
</style>