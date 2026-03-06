<template>
  <div
    :class="containerClasses"
    :title="tooltipText"
    @click="handleClick"
  >
    <!-- Icon -->
    <svg v-if="showIcon" :class="iconClasses" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path v-if="status === TeamInvitationStatus.PENDING" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      <path v-if="status === TeamInvitationStatus.ACCEPTED" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      <path v-if="status === TeamInvitationStatus.REJECTED" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      <path v-if="status === TeamInvitationStatus.EXPIRED" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>

    <!-- Label -->
    <span v-if="showLabel" :class="labelClasses">
      {{ statusText }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { TeamInvitationStatus } from '~/types/team-types'
import type { TeamInvitationStatusAtomProps, TeamInvitationStatusAtomEmits } from '~/types/team-types'

const props = withDefaults(defineProps<TeamInvitationStatusAtomProps>(), {
  size: 'md',
  showLabel: true,
  showIcon: true,
})

const emit = defineEmits<TeamInvitationStatusAtomEmits>()

// Status text based on invitation status
const statusText = computed(() => {
  switch (props.status) {
    case TeamInvitationStatus.PENDING:
      return 'Pending'
    case TeamInvitationStatus.ACCEPTED:
      return 'Accepted'
    case TeamInvitationStatus.REJECTED:
      return 'Rejected'
    case TeamInvitationStatus.EXPIRED:
      return 'Expired'
    default:
      return 'Unknown'
  }
})

// Tooltip text
const tooltipText = computed(() => {
  switch (props.status) {
    case TeamInvitationStatus.PENDING:
      return 'Invitation is pending acceptance'
    case TeamInvitationStatus.ACCEPTED:
      return 'Invitation has been accepted'
    case TeamInvitationStatus.REJECTED:
      return 'Invitation has been rejected'
    case TeamInvitationStatus.EXPIRED:
      return 'Invitation has expired'
    default:
      return 'Unknown invitation status'
  }
})

// Status color based on invitation status
const statusColor = computed(() => {
  switch (props.status) {
    case TeamInvitationStatus.PENDING:
      return 'yellow'
    case TeamInvitationStatus.ACCEPTED:
      return 'green'
    case TeamInvitationStatus.REJECTED:
      return 'red'
    case TeamInvitationStatus.EXPIRED:
      return 'gray'
    default:
      return 'gray'
  }
})

// Container classes
const containerClasses = computed(() => {
  const baseClasses = [
    'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors duration-200 cursor-pointer',
    'hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2',
  ]

  // Size classes
  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-0.5 text-xs',
    lg: 'px-3 py-1 text-sm',
  }

  // Color classes
  const colorClasses = {
    yellow: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200 focus:ring-yellow-500',
    green: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 focus:ring-green-500',
    red: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 focus:ring-red-500',
    gray: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200 focus:ring-gray-500',
  }

  return [
    ...baseClasses,
    sizeClasses[props.size],
    colorClasses[statusColor.value],
  ].join(' ')
})

// Icon classes
const iconClasses = computed(() => {
  const sizeClasses = {
    sm: 'h-3 w-3 mr-1',
    md: 'h-3.5 w-3.5 mr-1.5',
    lg: 'h-4 w-4 mr-2',
  }
  
  return sizeClasses[props.size]
})

// Label classes
const labelClasses = computed(() => {
  const sizeClasses = {
    sm: 'text-xs',
    md: 'text-xs',
    lg: 'text-sm',
  }
  
  return sizeClasses[props.size]
})

// Handle click
const handleClick = (event: MouseEvent) => {
  emit('click', event)
}
</script>

<style scoped>
/* Custom focus styles */
div:focus {
  outline: 2px solid transparent;
  outline-offset: 2px;
}

/* Animation for pending status */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

/* Apply pulse animation to pending status */
div[title*="pending"] {
  animation: pulse 2s infinite;
}
</style>