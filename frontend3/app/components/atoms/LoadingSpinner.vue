<template>
  <svg :class="spinnerClasses" viewBox="0 0 24 24" fill="none" role="status" aria-label="Loading">
    <circle
      class="opacity-25"
      cx="12"
      cy="12"
      r="10"
      stroke="currentColor"
      :stroke-width="thickness"
    />
    <path
      class="opacity-75"
      fill="currentColor"
      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
    />
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'sm' | 'md' | 'lg'
  color?: 'primary' | 'current'
  thickness?: number
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  color: 'primary',
  thickness: 3,
})

const sizeClasses = {
  sm: 'w-4 h-4',
  md: 'w-8 h-8',
  lg: 'w-12 h-12',
}

const colorClasses = {
  primary: 'text-primary-600',
  current: 'text-current',
}

const spinnerClasses = computed(() => [
  'animate-spin',
  sizeClasses[props.size],
  colorClasses[props.color],
])
</script>
