<template>
  <button
    type="button"
    class="project-vote-button inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
    :class="[sizeClasses, variantClasses, stateClasses, animationClasses]"
    :aria-label="ariaLabel"
    :aria-pressed="isVoted"
    :disabled="disabled || loading"
    @click="handleClick"
    @keydown.enter="handleClick"
    @keydown.space="handleClick"
  >
    <!-- Loading State -->
    <span
      v-if="loading"
      class="loading-spinner"
      :class="spinnerClasses"
      aria-hidden="true"
    >
      <svg
        class="animate-spin"
        :class="spinnerSizeClasses"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        />
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
    </span>

    <!-- Vote Icon -->
    <span
      v-else
      class="vote-icon"
      :class="iconClasses"
      aria-hidden="true"
    >
      <slot name="icon">
        <svg
          :class="iconSizeClasses"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            v-if="isVoted"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 15l7-7 7 7"
          />
          <path
            v-else
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </slot>
    </span>

    <!-- Vote Count -->
    <span
      v-if="showCount"
      class="vote-count"
      :class="countClasses"
    >
      {{ formattedCount }}
    </span>

    <!-- Optional: Vote Text -->
    <span
      v-if="showText"
      class="vote-text"
      :class="textClasses"
    >
      {{ voteText }}
    </span>

    <!-- Tooltip (optional) -->
    <span
      v-if="tooltip"
      class="sr-only"
    >
      {{ tooltip }}
    </span>
  </button>
</template>

<script setup lang="ts">
import type { ProjectVoteButtonProps } from '~/types/project-types'

interface Props extends ProjectVoteButtonProps {
  /** Tooltip-Text für zusätzliche Informationen */
  tooltip?: string
  /** Vote-Text anzeigen */
  showText?: boolean
  /** Animation beim Klicken aktivieren */
  animate?: boolean
  /** Loading State */
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  variant: 'primary',
  showCount: true,
  showText: false,
  animate: true,
  loading: false,
})

const emit = defineEmits<{
  'vote': [projectId: string, voteType: 'up' | 'down']
  'unvote': [projectId: string]
}>()

// Computed Properties
const isVoted = computed(() => props.hasVoted)
const voteText = computed(() => {
  if (props.showText) {
    return isVoted.value ? 'Voted' : 'Vote'
  }
  return ''
})

const formattedCount = computed(() => {
  if (props.voteCount >= 1000) {
    return `${(props.voteCount / 1000).toFixed(1)}k`
  }
  return props.voteCount.toString()
})

// ARIA-Label für Accessibility
const ariaLabel = computed(() => {
  const action = isVoted.value ? 'Remove vote from' : 'Vote for'
  return `${action} project ${props.projectId}`
})

// Größen-Klassen
const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'px-2 py-1 text-xs'
    case 'lg':
      return 'px-4 py-2.5 text-base'
    case 'xl':
      return 'px-6 py-3 text-lg'
    case 'md':
    default:
      return 'px-3 py-1.5 text-sm'
  }
})

// Variant-Klassen
const variantClasses = computed(() => {
  const base = 'border'
  
  if (isVoted.value) {
    switch (props.variant) {
      case 'primary':
        return `${base} bg-blue-600 dark:bg-blue-700 text-white border-blue-700 dark:border-blue-800 hover:bg-blue-700 dark:hover:bg-blue-800`
      case 'secondary':
        return `${base} bg-gray-200 dark:bg-gray-800 text-gray-800 dark:text-gray-200 border-gray-300 dark:border-gray-700 hover:bg-gray-300 dark:hover:bg-gray-700`
      case 'success':
        return `${base} bg-green-600 dark:bg-green-700 text-white border-green-700 dark:border-green-800 hover:bg-green-700 dark:hover:bg-green-800`
      case 'danger':
        return `${base} bg-red-600 dark:bg-red-700 text-white border-red-700 dark:border-red-800 hover:bg-red-700 dark:hover:bg-red-800`
      default:
        return `${base} bg-blue-600 dark:bg-blue-700 text-white border-blue-700 dark:border-blue-800 hover:bg-blue-700 dark:hover:bg-blue-800`
    }
  } else {
    switch (props.variant) {
      case 'primary':
        return `${base} bg-white dark:bg-gray-900 text-blue-600 dark:text-blue-400 border-blue-300 dark:border-blue-700 hover:bg-blue-50 dark:hover:bg-blue-900/30`
      case 'secondary':
        return `${base} bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800`
      case 'success':
        return `${base} bg-white dark:bg-gray-900 text-green-600 dark:text-green-400 border-green-300 dark:border-green-700 hover:bg-green-50 dark:hover:bg-green-900/30`
      case 'danger':
        return `${base} bg-white dark:bg-gray-900 text-red-600 dark:text-red-400 border-red-300 dark:border-red-700 hover:bg-red-50 dark:hover:bg-red-900/30`
      default:
        return `${base} bg-white dark:bg-gray-900 text-blue-600 dark:text-blue-400 border-blue-300 dark:border-blue-700 hover:bg-blue-50 dark:hover:bg-blue-900/30`
    }
  }
})

// State-Klassen
const stateClasses = computed(() => {
  const classes: string[] = []
  
  if (props.disabled) {
    classes.push('opacity-50 cursor-not-allowed')
  }
  
  if (props.loading) {
    classes.push('cursor-wait')
  }
  
  return classes.join(' ')
})

// Animation-Klassen
const animationClasses = computed(() => {
  if (!props.animate) return ''
  
  return 'active:scale-95 transition-transform duration-100'
})

// Icon-Klassen
const iconClasses = computed(() => {
  return isVoted.value ? 'text-current' : 'text-current'
})

const iconSizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'w-3 h-3'
    case 'lg':
      return 'w-5 h-5'
    case 'xl':
      return 'w-6 h-6'
    case 'md':
    default:
      return 'w-4 h-4'
  }
})

// Spinner-Klassen
const spinnerClasses = computed(() => {
  return isVoted.value ? 'text-white' : 'text-current'
})

const spinnerSizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'w-3 h-3'
    case 'lg':
      return 'w-5 h-5'
    case 'xl':
      return 'w-6 h-6'
    case 'md':
    default:
      return 'w-4 h-4'
  }
})

// Count-Klassen
const countClasses = computed(() => {
  const classes: string[] = ['font-semibold']
  
  if (isVoted.value) {
    classes.push('text-white dark:text-white')
  } else {
    switch (props.variant) {
      case 'primary':
        classes.push('text-blue-700 dark:text-blue-300')
      case 'secondary':
        classes.push('text-gray-800 dark:text-gray-300')
      case 'success':
        classes.push('text-green-700 dark:text-green-300')
      case 'danger':
        classes.push('text-red-700 dark:text-red-300')
      default:
        classes.push('text-blue-700 dark:text-blue-300')
    }
  }
  
  return classes.join(' ')
})

// Text-Klassen
const textClasses = computed(() => {
  const classes: string[] = ['ml-1']
  
  if (isVoted.value) {
    classes.push('text-white dark:text-white')
  } else {
    switch (props.variant) {
      case 'primary':
        classes.push('text-blue-700 dark:text-blue-300')
      case 'secondary':
        classes.push('text-gray-800 dark:text-gray-300')
      case 'success':
        classes.push('text-green-700 dark:text-green-300')
      case 'danger':
        classes.push('text-red-700 dark:text-red-300')
      default:
        classes.push('text-blue-700 dark:text-blue-300')
    }
  }
  
  return classes.join(' ')
})

// Event-Handler
const handleClick = (event: Event) => {
  if (props.disabled || props.loading) return
  
  if (isVoted.value) {
    emit('unvote', props.projectId)
  } else {
    emit('vote', props.projectId, 'up')
  }
}
</script>

<style scoped>
.project-vote-button {
  transition-property: color, background-color, border-color, transform, box-shadow;
  transition-duration: 200ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
  min-width: fit-content;
}

/* Loading Animation */
.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Hover Effects */
.project-vote-button:not(:disabled):not(.loading):hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Active State */
.project-vote-button:not(:disabled):active {
  transform: translateY(0);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

/* Focus Styles */
.project-vote-button:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 2px;
}

/* Dark Mode Optimierungen */
@media (prefers-color-scheme: dark) {
  .project-vote-button {
    border-opacity: 0.5;
  }
  
  .project-vote-button:not(:disabled):not(.loading):hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
  }
}

/* Responsive Anpassungen */
@media (max-width: 640px) {
  .project-vote-button.size-lg {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }
  
  .project-vote-button.size-xl {
    padding: 0.75rem 1.25rem;
    font-size: 1rem;
  }
  
  .vote-text {
    display: none;
  }
}

/* Accessibility: Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  .project-vote-button {
    transition: none;
  }
  
  .loading-spinner {
    animation: none;
  }
  
  .project-vote-button:not(:disabled):not(.loading):hover {
    transform: none;
  }
}
</style>