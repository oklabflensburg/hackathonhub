<template>
  <span
    :class="badgeClasses"
    :title="tooltipText"
    aria-label="Team role badge"
  >
    <span v-if="showLabel" class="mr-1">{{ roleLabel }}</span>
    <span v-else class="sr-only">{{ roleLabel }}</span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { TeamRoleBadgeProps } from '~/types/team-types'
import { TeamRole } from '~/types/team-types'

const props = withDefaults(defineProps<TeamRoleBadgeProps & {
  showLabel?: boolean
}>(), {
  size: 'md',
  showLabel: true
})

// Role label mapping
const roleLabels = {
  [TeamRole.OWNER]: 'Owner',
  [TeamRole.ADMIN]: 'Admin',
  [TeamRole.MEMBER]: 'Member',
  [TeamRole.PENDING]: 'Pending'
} as const

// Size classes mapping
const sizeClasses = {
  sm: 'px-1.5 py-0.5 text-xs',
  md: 'px-2 py-1 text-sm',
  lg: 'px-3 py-1.5 text-base'
} as const

// Color classes mapping based on role
const colorClasses = {
  [TeamRole.OWNER]: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
  [TeamRole.ADMIN]: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  [TeamRole.MEMBER]: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  [TeamRole.PENDING]: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
} as const

// Computed properties
const roleLabel = computed(() => roleLabels[props.role] || 'Unknown')
const tooltipText = computed(() => `Team role: ${roleLabel.value}`)

const badgeClasses = computed(() => [
  'inline-flex items-center rounded-full font-medium transition-colors duration-200',
  sizeClasses[props.size],
  colorClasses[props.role],
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