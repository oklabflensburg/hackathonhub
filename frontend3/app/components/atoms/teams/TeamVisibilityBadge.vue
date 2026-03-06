<template>
  <span
    :class="badgeClasses"
    :title="tooltipText"
    aria-label="Team visibility badge"
  >
    <span v-if="showLabel" class="mr-1">{{ visibilityLabel }}</span>
    <span v-else class="sr-only">{{ visibilityLabel }}</span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { TeamVisibilityBadgeProps } from '~/types/team-types'
import { TeamVisibility } from '~/types/team-types'

const props = withDefaults(defineProps<TeamVisibilityBadgeProps & {
  showLabel?: boolean
}>(), {
  size: 'md',
  showLabel: true
})

// Visibility label mapping
const visibilityLabels = {
  [TeamVisibility.PUBLIC]: 'Public',
  [TeamVisibility.PRIVATE]: 'Private'
} as const

// Size classes mapping
const sizeClasses = {
  sm: 'px-1.5 py-0.5 text-xs',
  md: 'px-2 py-1 text-sm',
  lg: 'px-3 py-1.5 text-base'
} as const

// Color classes mapping based on visibility
const colorClasses = {
  [TeamVisibility.PUBLIC]: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  [TeamVisibility.PRIVATE]: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
} as const

// Icon mapping
const visibilityIcons = {
  [TeamVisibility.PUBLIC]: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z',
  [TeamVisibility.PRIVATE]: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z'
} as const

// Computed properties
const visibilityLabel = computed(() => visibilityLabels[props.visibility] || 'Unknown')
const tooltipText = computed(() => `Team visibility: ${visibilityLabel.value}`)

const badgeClasses = computed(() => [
  'inline-flex items-center rounded-full font-medium transition-colors duration-200',
  sizeClasses[props.size],
  colorClasses[props.visibility],
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