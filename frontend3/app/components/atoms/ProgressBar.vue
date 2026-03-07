<template>
  <div
    :class="containerClasses"
    :style="containerStyles"
    :role="role"
    :aria-valuemin="0"
    :aria-valuemax="100"
    :aria-valuenow="computedValue"
    :aria-valuetext="ariaValueText"
    :aria-label="ariaLabel"
    v-bind="$attrs"
  >
    <!-- Background track -->
    <div :class="trackClasses" :style="trackStyles">
      <!-- Progress fill -->
      <div
        ref="fillRef"
        :class="fillClasses"
        :style="fillStyles"
        :data-value="computedValue"
      >
        <!-- Label inside progress bar (optional) -->
        <div v-if="showLabel && labelPosition === 'inside'" :class="labelClasses">
          <slot name="label">
            {{ labelText }}
          </slot>
        </div>
      </div>
      
      <!-- Stripes animation (optional) -->
      <div
        v-if="striped"
        :class="stripesClasses"
        :style="stripesStyles"
      />
    </div>
    
    <!-- Label outside progress bar (optional) -->
    <div
      v-if="showLabel && labelPosition === 'outside'"
      :class="outsideLabelClasses"
    >
      <slot name="label">
        {{ labelText }}
      </slot>
    </div>
    
    <!-- Additional info (optional slot) -->
    <div v-if="$slots.info" :class="infoClasses">
      <slot name="info" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'

export interface ProgressBarProps {
  /** Current progress value (0-100) */
  value?: number
  /** Minimum value */
  min?: number
  /** Maximum value */
  max?: number
  /** Size of the progress bar */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  /** Color variant */
  variant?: 'primary' | 'success' | 'warning' | 'error' | 'info' | 'neutral'
  /** Whether to show striped animation */
  striped?: boolean
  /** Whether the stripes should be animated */
  animated?: boolean
  /** Whether to show a label */
  showLabel?: boolean
  /** Position of the label */
  labelPosition?: 'inside' | 'outside' | 'none'
  /** Custom label text (overrides default percentage) */
  label?: string
  /** Whether to show additional info slot */
  showInfo?: boolean
  /** Border radius */
  borderRadius?: string
  /** Height of the progress bar (overrides size) */
  height?: string
  /** Width of the container */
  width?: string
  /** Additional CSS classes */
  class?: string
  /** ARIA label for accessibility */
  ariaLabel?: string
  /** Role for accessibility */
  role?: string
}

const props = withDefaults(defineProps<ProgressBarProps>(), {
  value: 0,
  min: 0,
  max: 100,
  size: 'md',
  variant: 'primary',
  striped: false,
  animated: false,
  showLabel: false,
  labelPosition: 'inside',
  showInfo: false,
  borderRadius: '9999px',
  role: 'progressbar',
})

// Refs
const fillRef = ref<HTMLElement>()

// Computed value (clamped between min and max)
const computedValue = computed(() => {
  const clamped = Math.max(props.min, Math.min(props.max, props.value))
  return Math.round(clamped)
})

// Percentage for display and styling
const percentage = computed(() => {
  const range = props.max - props.min
  if (range === 0) return 0
  return ((computedValue.value - props.min) / range) * 100
})

// Label text
const labelText = computed(() => {
  if (props.label) return props.label
  return `${computedValue.value}%`
})

// ARIA value text
const ariaValueText = computed(() => {
  if (props.label) return props.label
  return `${computedValue.value} percent`
})

// Size classes
const sizeClasses = computed(() => {
  const sizes = {
    xs: 'h-1',
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4',
    xl: 'h-6',
  }
  return sizes[props.size]
})

// Variant color classes
const variantClasses = computed(() => {
  const variants = {
    primary: {
      bg: 'bg-blue-600 dark:bg-blue-500',
      text: 'text-blue-600 dark:text-blue-500',
      track: 'bg-blue-100 dark:bg-blue-900/30',
    },
    success: {
      bg: 'bg-green-600 dark:bg-green-500',
      text: 'text-green-600 dark:text-green-500',
      track: 'bg-green-100 dark:bg-green-900/30',
    },
    warning: {
      bg: 'bg-yellow-600 dark:bg-yellow-500',
      text: 'text-yellow-600 dark:text-yellow-500',
      track: 'bg-yellow-100 dark:bg-yellow-900/30',
    },
    error: {
      bg: 'bg-red-600 dark:bg-red-500',
      text: 'text-red-600 dark:text-red-500',
      track: 'bg-red-100 dark:bg-red-900/30',
    },
    info: {
      bg: 'bg-blue-600 dark:bg-blue-500',
      text: 'text-blue-600 dark:text-blue-500',
      track: 'bg-blue-100 dark:bg-blue-900/30',
    },
    neutral: {
      bg: 'bg-gray-600 dark:bg-gray-500',
      text: 'text-gray-600 dark:text-gray-500',
      track: 'bg-gray-100 dark:bg-gray-900/30',
    },
  }
  return variants[props.variant] || variants.primary
})

// Container classes
const containerClasses = computed(() => {
  const classes = ['progress-bar-container', 'w-full']
  
  if (props.class) {
    classes.push(props.class)
  }
  
  return classes.join(' ')
})

// Container styles
const containerStyles = computed(() => {
  const styles: Record<string, string> = {}
  
  if (props.width) {
    styles.width = props.width
  }
  
  return styles
})

// Track classes
const trackClasses = computed(() => {
  const classes = [
    'progress-track',
    'w-full',
    'overflow-hidden',
    variantClasses.value.track,
    sizeClasses.value,
  ]
  
  // Use custom height if provided
  if (props.height && !props.height.startsWith('h-')) {
    // Height will be set via inline style
  } else if (props.height) {
    classes.push(props.height)
  }
  
  return classes.join(' ')
})

// Track styles
const trackStyles = computed(() => {
  const styles: Record<string, string> = {
    borderRadius: props.borderRadius,
  }
  
  // Set custom height if provided as CSS value
  if (props.height && !props.height.startsWith('h-')) {
    styles.height = props.height
  }
  
  return styles
})

// Fill classes
const fillClasses = computed(() => {
  const classes = [
    'progress-fill',
    'h-full',
    'transition-all',
    'duration-300',
    'ease-out',
    variantClasses.value.bg,
  ]
  
  if (props.striped) {
    classes.push('progress-striped')
  }
  
  if (props.striped && props.animated) {
    classes.push('progress-animated')
  }
  
  return classes.join(' ')
})

// Fill styles
const fillStyles = computed(() => {
  const styles: Record<string, string> = {
    width: `${percentage.value}%`,
    borderRadius: props.borderRadius,
  }
  
  return styles
})

// Stripes classes
const stripesClasses = computed(() => {
  const classes = [
    'progress-stripes',
    'absolute',
    'inset-0',
    'opacity-30',
  ]
  
  if (props.animated) {
    classes.push('progress-stripes-animated')
  }
  
  return classes.join(' ')
})

// Stripes styles
const stripesStyles = computed(() => ({
  backgroundImage: `linear-gradient(
    45deg,
    rgba(255, 255, 255, 0.15) 25%,
    transparent 25%,
    transparent 50%,
    rgba(255, 255, 255, 0.15) 50%,
    rgba(255, 255, 255, 0.15) 75%,
    transparent 75%,
    transparent
  )`,
  backgroundSize: '1rem 1rem',
}))

// Label classes
const labelClasses = computed(() => {
  const classes = [
    'progress-label',
    'absolute',
    'inset-0',
    'flex',
    'items-center',
    'justify-center',
    'text-xs',
    'font-medium',
    'text-white',
    'dark:text-gray-100',
  ]
  
  // Adjust text size based on progress bar size
  if (props.size === 'xs' || props.size === 'sm') {
    classes.push('text-[10px]')
  }
  
  return classes.join(' ')
})

// Outside label classes
const outsideLabelClasses = computed(() => {
  const classes = [
    'progress-outside-label',
    'mt-1',
    'text-sm',
    'font-medium',
    variantClasses.value.text,
    'flex',
    'justify-between',
  ]
  
  return classes.join(' ')
})

// Info classes
const infoClasses = computed(() => [
  'progress-info',
  'mt-2',
  'text-sm',
  'text-gray-600',
  'dark:text-gray-400',
])

// Watch for value changes to trigger animations
watch(() => props.value, () => {
  // If we need to do anything when value changes
  nextTick(() => {
    // Could trigger custom events or animations here
  })
})

// Expose methods if needed
defineExpose({
  getValue: () => computedValue.value,
  getPercentage: () => percentage.value,
})
</script>

<style scoped>
.progress-bar-container {
  position: relative;
}

.progress-track {
  position: relative;
}

.progress-fill {
  position: relative;
  z-index: 1;
}

/* Striped background */
.progress-striped {
  background-image: linear-gradient(
    45deg,
    rgba(255, 255, 255, 0.15) 25%,
    transparent 25%,
    transparent 50%,
    rgba(255, 255, 255, 0.15) 50%,
    rgba(255, 255, 255, 0.15) 75%,
    transparent 75%,
    transparent
  );
  background-size: 1rem 1rem;
}

/* Animated stripes */
.progress-animated .progress-stripes {
  animation: progress-stripes 1s linear infinite;
}

@keyframes progress-stripes {
  0% {
    background-position: 1rem 0;
  }
  100% {
    background-position: 0 0;
  }
}

/* Smooth width transition */
.progress-fill {
  transition: width 0.3s ease-out;
}

/* For very small progress bars, adjust label visibility */
.progress-track.xs .progress-label,
.progress-track.sm .progress-label {
  display: none;
}

/* Dark mode adjustments */
.dark .progress-striped {
  background-image: linear-gradient(
    45deg,
    rgba(255, 255, 255, 0.1) 25%,
    transparent 25%,
    transparent 50%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.1) 75%,
    transparent 75%,
    transparent
  );
}

/* Accessibility focus styles */
.progress-bar-container:focus-within {
  outline: 2px solid currentColor;
  outline-offset: 2px;
  border-radius: 0.25rem;
}
</style>