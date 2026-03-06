<template>
  <span
    class="project-tag inline-flex items-center rounded-full font-medium transition-all duration-150"
    :class="[sizeClasses, interactiveClasses, colorClasses]"
    :aria-label="ariaLabel"
    :tabindex="clickable ? 0 : -1"
    @click="handleClick"
    @keydown.enter="handleClick"
    @keydown.space="handleClick"
  >
    <!-- Tag-Inhalt -->
    <span class="tag-content flex items-center gap-1.5">
      <!-- Optionales Icon -->
      <span
        v-if="$slots.icon"
        class="tag-icon"
        :class="iconClasses"
        aria-hidden="true"
      >
        <slot name="icon" />
      </span>

      <!-- Tag-Text -->
      <span class="tag-text" :class="textClasses">
        <slot>
          {{ tag.name }}
        </slot>
      </span>

      <!-- Entfernen-Button (wenn removable) -->
      <button
        v-if="removable"
        type="button"
        class="tag-remove"
        :class="removeButtonClasses"
        :aria-label="removeAriaLabel"
        @click.stop="handleRemove"
        @keydown.enter.stop="handleRemove"
        @keydown.space.stop="handleRemove"
      >
        <span class="remove-icon" aria-hidden="true">
          <slot name="remove-icon">
            <svg
              class="w-3 h-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </slot>
        </span>
      </button>
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
import type { ProjectTagProps } from '~/types/project-types'

interface Props extends ProjectTagProps {
  /** Tooltip-Text für zusätzliche Informationen */
  tooltip?: string
  /** Hover-Effekt aktivieren */
  hoverable?: boolean
  /** Fokus-Styling aktivieren */
  focusable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  removable: false,
  clickable: false,
  hoverable: true,
  focusable: true,
})

const emit = defineEmits<{
  'click': [tag: any]
  'remove': [tag: any]
}>()

// ARIA-Labels für Accessibility
const ariaLabel = computed(() => {
  return `Tag: ${props.tag.name}${props.tag.description ? ` - ${props.tag.description}` : ''}`
})

const removeAriaLabel = computed(() => {
  return `Tag "${props.tag.name}" entfernen`
})

// Größen-Klassen
const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'px-2 py-0.5 text-xs'
    case 'lg':
      return 'px-4 py-1.5 text-sm'
    case 'md':
    default:
      return 'px-3 py-1 text-sm'
  }
})

// Interaktive Klassen
const interactiveClasses = computed(() => {
  const classes: string[] = []
  
  if (props.clickable) {
    classes.push('cursor-pointer select-none')
    
    if (props.hoverable) {
      classes.push('hover:scale-105 hover:shadow-sm')
    }
    
    if (props.focusable) {
      classes.push('focus:outline-none focus:ring-2 focus:ring-offset-1')
    }
  }
  
  if (props.removable) {
    classes.push('pr-1') // Extra Platz für Remove-Button
  }
  
  return classes.join(' ')
})

// Farb-Klassen basierend auf Tag-Farbe
const colorClasses = computed(() => {
  const color = props.tag.color || 'gray'
  
  return `bg-${color}-100 dark:bg-${color}-900/30 text-${color}-700 dark:text-${color}-300 border border-${color}-200 dark:border-${color}-800`
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

// Text-Klassen
const textClasses = computed(() => {
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

// Remove-Button Klassen
const removeButtonClasses = computed(() => {
  const color = props.tag.color || 'gray'
  
  return `ml-1 p-0.5 rounded-full hover:bg-${color}-200 dark:hover:bg-${color}-800 focus:outline-none focus:ring-1 focus:ring-${color}-300 dark:focus:ring-${color}-700 transition-colors`
})

// Event-Handler
const handleClick = (event: Event) => {
  if (props.clickable) {
    emit('click', props.tag)
  }
}

const handleRemove = (event: Event) => {
  event.stopPropagation()
  emit('remove', props.tag)
}
</script>

<style scoped>
.project-tag {
  transition-property: color, background-color, border-color, transform, box-shadow;
  transition-duration: 150ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}

/* Entfernen-Button Animation */
.tag-remove {
  transition: all 100ms ease;
}

.tag-remove:hover {
  transform: scale(1.1);
}

.tag-remove:active {
  transform: scale(0.95);
}

/* Responsive Anpassungen */
@media (max-width: 640px) {
  .project-tag {
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
  }
  
  .project-tag.size-lg {
    font-size: 0.875rem;
    padding: 0.375rem 0.75rem;
  }
  
  .tag-remove {
    padding: 0.125rem;
  }
}

/* Dark Mode Optimierungen */
@media (prefers-color-scheme: dark) {
  .project-tag {
    border-opacity: 0.3;
  }
  
  .tag-remove:hover {
    background-opacity: 0.4;
  }
}

/* Accessibility: Fokus-Styling */
.project-tag:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 2px;
}

/* Disabled State (für zukünftige Erweiterungen) */
.project-tag.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}
</style>