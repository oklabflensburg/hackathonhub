<template>
  <span
    class="project-status-badge inline-flex items-center rounded-full font-medium transition-colors"
    :class="[sizeClasses, variantClasses, colorClasses]"
    :aria-label="ariaLabel"
  >
    <!-- Icon (wenn aktiviert) -->
    <span
      v-if="showIcon"
      class="status-icon"
      :class="iconClasses"
      aria-hidden="true"
    >
      <slot name="icon">
        <span :class="statusIcon" />
      </slot>
    </span>

    <!-- Label (wenn aktiviert) -->
    <span
      v-if="showLabel"
      class="status-label"
      :class="labelClasses"
    >
      <slot>
        {{ statusLabel }}
      </slot>
    </span>

    <!-- Tooltip (optional) -->
    <span
      v-if="tooltip"
      class="sr-only"
    >
      {{ tooltip }}
    </span>
  </span>
</template>

<script setup lang="ts">
import type { ProjectStatusBadgeProps } from '~/types/project-types'
import { PROJECT_STATUS_COLORS, PROJECT_STATUS_LABELS, PROJECT_STATUS_ICONS } from '~/types/project-types'

interface Props extends ProjectStatusBadgeProps {
  /** Tooltip-Text für zusätzliche Informationen */
  tooltip?: string
  /** Animation bei Status-Änderung */
  animate?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  variant: 'solid',
  showLabel: true,
  showIcon: false,
  animate: false,
})

// Status-Label und Icon
const statusLabel = computed(() => PROJECT_STATUS_LABELS[props.status])
const statusIcon = computed(() => PROJECT_STATUS_ICONS[props.status])

// ARIA-Label für Accessibility
const ariaLabel = computed(() => {
  return `Projekt-Status: ${statusLabel.value}`
})

// Größen-Klassen
const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'px-2 py-0.5 text-xs gap-1'
    case 'lg':
      return 'px-4 py-1.5 text-sm gap-2'
    case 'md':
    default:
      return 'px-3 py-1 text-sm gap-1.5'
  }
})

// Varianten-Klassen
const variantClasses = computed(() => {
  switch (props.variant) {
    case 'outline':
      return 'border'
    case 'soft':
      return 'bg-opacity-10'
    case 'solid':
    default:
      return ''
  }
})

// Farb-Klassen basierend auf Status
const colorClasses = computed(() => {
  const color = PROJECT_STATUS_COLORS[props.status]
  
  switch (props.variant) {
    case 'outline':
      return `border-${color}-300 dark:border-${color}-400 text-${color}-700 dark:text-${color}-300`
    case 'soft':
      return `bg-${color}-100 dark:bg-${color}-900/30 text-${color}-700 dark:text-${color}-300`
    case 'solid':
    default:
      return `bg-${color}-500 dark:bg-${color}-600 text-white`
  }
})

// Icon-Klassen
const iconClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'w-3 h-3'
    case 'lg':
      return 'w-4 h-4'
    case 'md':
    default:
      return 'w-3.5 h-3.5'
  }
})

// Label-Klassen
const labelClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'font-medium'
    case 'lg':
      return 'font-semibold'
    case 'md':
    default:
      return 'font-medium'
  }
})
</script>

<style scoped>
.project-status-badge {
  transition-property: color, background-color, border-color, transform;
  transition-duration: 150ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Animation für Status-Änderungen */
.project-status-badge.animate {
  animation: statusPulse 0.5s ease-in-out;
}

@keyframes statusPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

/* Responsive Anpassungen */
@media (max-width: 640px) {
  .project-status-badge {
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
  }
  
  .project-status-badge.size-lg {
    font-size: 0.875rem;
    padding: 0.375rem 0.75rem;
  }
}

/* Dark Mode Optimierungen */
@media (prefers-color-scheme: dark) {
  .project-status-badge.variant-outline {
    border-opacity: 0.3;
  }
  
  .project-status-badge.variant-soft {
    background-opacity: 0.15;
  }
}
</style>