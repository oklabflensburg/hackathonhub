<template>
  <Badge
    :variant="variant"
    :class="[
      'capitalize font-semibold transition-all duration-200',
      sizeClasses,
      rounded ? 'rounded-full' : 'rounded-md',
      shadow ? 'shadow-sm' : ''
    ]"
    :title="tooltip"
  >
    <slot>
      <span class="flex items-center">
        <svg v-if="showIcon" :class="iconClasses" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path v-if="status === 'active'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
          <path v-if="status === 'upcoming'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          <path v-if="status === 'completed'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          <path v-if="!['active', 'upcoming', 'completed'].includes(status)" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
        <span :class="[showIcon ? 'ml-2' : '']">{{ displayText }}</span>
      </span>
    </slot>
  </Badge>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Badge from './Badge.vue'

interface Props {
  /** Hackathon status: 'upcoming', 'active', 'completed', or custom string */
  status?: 'upcoming' | 'active' | 'completed' | string
  /** Custom text to display (overrides status-based text) */
  text?: string
  /** Size of the badge: 'sm', 'md', 'lg' */
  size?: 'sm' | 'md' | 'lg'
  /** Show icon next to text */
  showIcon?: boolean
  /** Fully rounded badge (pill shape) */
  rounded?: boolean
  /** Add shadow to badge */
  shadow?: boolean
  /** Tooltip text on hover */
  tooltip?: string
}

const props = withDefaults(defineProps<Props>(), {
  status: 'upcoming',
  text: undefined,
  size: 'md',
  showIcon: true,
  rounded: true,
  shadow: true,
  tooltip: undefined
})

// Determine variant based on status
const variant = computed(() => {
  if (props.status === 'active') return 'success'
  if (props.status === 'upcoming') return 'warning'
  if (props.status === 'completed') return 'gray'
  return 'primary'
})

// Determine display text
const displayText = computed(() => {
  if (props.text) return props.text
  return props.status.charAt(0).toUpperCase() + props.status.slice(1)
})

// Size-based classes
const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm': return 'px-2 py-1 text-xs'
    case 'lg': return 'px-4 py-2 text-base'
    default: return 'px-3 py-1.5 text-sm'
  }
})

// Icon size classes
const iconClasses = computed(() => {
  switch (props.size) {
    case 'sm': return 'w-3 h-3'
    case 'lg': return 'w-5 h-5'
    default: return 'w-4 h-4'
  }
})
</script>

<style scoped>
/* Custom animations for status changes */
.badge-success {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}
</style>