<template>
  <div :class="cardClasses">
    <!-- Header -->
    <div class="flex items-start justify-between mb-3">
        <!-- Inviter Info -->
        <div class="flex items-center space-x-3">
          <!-- Avatar -->
          <div class="flex-shrink-0">
            <img
              v-if="invitation.invitedByUser?.avatarUrl"
              :src="invitation.invitedByUser.avatarUrl"
              :alt="invitation.invitedByUser.displayName || invitation.invitedByUser.username"
              class="h-10 w-10 rounded-full"
            />
            <div v-else class="h-10 w-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
              <span class="text-gray-500 dark:text-gray-400 font-medium">
                {{ getInitials(invitation.invitedByUser?.displayName || invitation.invitedByUser?.username || '?') }}
              </span>
            </div>
          </div>

          <!-- Inviter Details -->
          <div>
            <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">
              {{ invitation.invitedByUser?.displayName || invitation.invitedByUser?.username || 'Unknown User' }}
            </h4>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              {{ $t('teams.invitations.invitedYou') }}
            </p>
          </div>
        </div>

      <!-- Status Badge -->
      <TeamInvitationStatus
        :status="invitation.status"
        size="sm"
        :show-label="!compact"
        @click="handleStatusClick"
      />
    </div>

    <!-- Team Info -->
    <div class="mb-4">
      <div class="flex items-center space-x-2 mb-2">
        <div v-if="team.avatarUrl" class="flex-shrink-0">
          <img :src="team.avatarUrl" :alt="team.name" class="h-8 w-8 rounded-full" />
        </div>
        <div>
          <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100">
            {{ team.name }}
          </h3>
          <p v-if="team.description && !compact" class="text-xs text-gray-600 dark:text-gray-400 line-clamp-2">
            {{ team.description }}
          </p>
        </div>
      </div>

      <!-- Team Stats (only in non-compact mode) -->
      <div v-if="!compact && team.stats" class="flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400">
        <span class="flex items-center">
          <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {{ team.stats.memberCount || 0 }} members
        </span>
        <span v-if="team.maxMembers" class="flex items-center">
          <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {{ team.maxMembers }} max
        </span>
        <span class="flex items-center">
          <TeamBadge :status="team.status" size="xs" />
        </span>
      </div>
    </div>

    <!-- Actions -->
    <div v-if="showActions && invitation.status === 'pending'" class="flex items-center justify-between pt-3 border-t border-gray-200 dark:border-gray-700">
      <!-- Action Buttons -->
      <div class="flex space-x-2">
        <!-- Accept Button -->
        <button
          @click="handleAccept"
          class="px-3 py-1.5 bg-green-600 text-white text-xs font-medium rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-200"
        >
          {{ $t('teams.actions.accept') }}
        </button>

        <!-- Reject Button -->
        <button
          @click="handleReject"
          class="px-3 py-1.5 bg-red-600 text-white text-xs font-medium rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors duration-200"
        >
          {{ $t('teams.actions.reject') }}
        </button>
      </div>

      <!-- Additional Actions (for inviter) -->
      <div v-if="canManageTeam" class="flex space-x-2">
        <!-- Resend Button -->
        <button
          v-if="invitation.status === 'pending'"
          @click="handleResend"
          class="p-1.5 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
          :title="$t('teams.actions.resend')"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>

        <!-- Cancel Button -->
        <button
          @click="handleCancel"
          class="p-1.5 text-gray-600 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 rounded-full hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors duration-200"
          :title="$t('teams.actions.cancel')"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- View Profile Button -->
      <button
        v-else
        @click="handleViewProfile"
        class="text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300 text-xs font-medium"
      >
        {{ $t('teams.actions.viewProfile') }}
      </button>
    </div>

    <!-- Footer (only in non-compact mode) -->
    <div v-if="!compact" class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
        <span>
          {{ $t('teams.invitations.sent') }}: {{ formatDate(invitation.createdAt) }}
        </span>
        <span v-if="invitation.expiresAt">
          {{ $t('teams.invitations.expires') }}: {{ formatDate(invitation.expiresAt) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { TeamInvitationStatus } from '~/types/team-types'
import { canUserManageTeam } from '~/types/team-types'
import type { TeamInvitationCardProps, TeamInvitationCardEmits } from '~/types/team-types'

const props = withDefaults(defineProps<TeamInvitationCardProps>(), {
  showActions: true,
  compact: false,
})

const emit = defineEmits<TeamInvitationCardEmits>()

// Check if current user can manage the team
const canManageTeam = computed(() => {
  // In a real implementation, we would need team members
  // For now, we'll assume the inviter can manage
  return props.currentUserId === props.invitation.invitedByUserId
})

// Card classes based on props
const cardClasses = computed(() => {
  const baseClasses = [
    'p-4 bg-white dark:bg-gray-800 rounded-lg border transition-all duration-200',
    'hover:shadow-md hover:border-gray-300 dark:hover:border-gray-600',
  ]

  if (props.compact) {
    baseClasses.push('p-3')
  }

  // Status-based border color
  switch (props.invitation.status) {
    case TeamInvitationStatus.PENDING:
      baseClasses.push('border-yellow-200 dark:border-yellow-800')
      break
    case TeamInvitationStatus.ACCEPTED:
      baseClasses.push('border-green-200 dark:border-green-800')
      break
    case TeamInvitationStatus.REJECTED:
      baseClasses.push('border-red-200 dark:border-red-800')
      break
    case TeamInvitationStatus.EXPIRED:
      baseClasses.push('border-gray-200 dark:border-gray-700')
      break
    default:
      baseClasses.push('border-gray-200 dark:border-gray-700')
  }

  return baseClasses.join(' ')
})

// Get initials for avatar placeholder
const getInitials = (name: string): string => {
  if (!name) return '?'
  return name
    .split(' ')
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2)
}

// Format date for display
const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

// Event handlers
const handleAccept = () => {
  emit('accept', props.invitation.id)
}

const handleReject = () => {
  emit('reject', props.invitation.id)
}

const handleResend = () => {
  emit('resend', props.invitation.id)
}

const handleCancel = () => {
  if (confirm('Are you sure you want to cancel this invitation?')) {
    emit('cancel', props.invitation.id)
  }
}

const handleViewProfile = () => {
  if (props.invitation.invitedUserId) {
    emit('view-profile', props.invitation.invitedUserId)
  }
}

const handleStatusClick = (event: MouseEvent) => {
  // Status badge was clicked - could be used to show more details
  console.log('Status clicked:', props.invitation.status)
}
</script>

<style scoped>
/* Line clamp for description */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Smooth transitions */
.card-enter-active,
.card-leave-active {
  transition: all 0.3s ease;
}

.card-enter-from,
.card-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* Hover effects */
div[class*="bg-white"]:hover,
div[class*="bg-gray-800"]:hover {
  @apply transform transition-transform duration-200;
}
</style>