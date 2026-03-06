<template>
  <span
    :class="badgeClasses"
    :title="tooltipText"
    aria-label="Team status badge"
  >
    <span v-if="showLabel" class="mr-1">{{ statusLabel }}</span>
    <span v-else class="sr-only">{{ statusLabel }}</span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { TeamBadgeProps } from '~/types/team-types'
import { TeamStatus, getTeamStatusColor } from '~/types/team-types'

const props = withDefaults(defineProps<TeamBadgeProps>(), {
  status: TeamStatus.ACTIVE,
  size: 'md',
  showLabel: true
})

// Status label mapping
const statusLabels = {
  [TeamStatus.ACTIVE]: 'Active',
  [TeamStatus.INACTIVE]: 'Inactive',
  [TeamStatus.ARCHIVED]: 'Archived',
  [TeamStatus.DELETED]: 'Deleted'
} as const

// Size classes mapping
const sizeClasses = {
  sm: 'px-1.5 py-0.5 text-xs',
  md: 'px-2 py-1 text-sm',
  lg: 'px-3 py-1.5 text-base'
} as const

// Color classes mapping
const colorClasses = {
  green: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  gray: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300',
  orange: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
  red: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
} as const

// Computed properties
const statusLabel = computed(() => statusLabels[props.status] || 'Unknown')
const tooltipText = computed(() => `Team status: ${statusLabel.value}`)
const statusColor = computed(() => getTeamStatusColor(props.status))

const badgeClasses = computed(() => [
  'inline-flex items-center rounded-full font-medium transition-colors duration-200',
  sizeClasses[props.size],
  colorClasses[statusColor.value],
  props.showLabel ? '' : 'w-3 h-3 rounded-full p-0'
])
</script>

<style scoped>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>