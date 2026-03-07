<template>
  <div
    :class="alertClasses"
    :style="alertStyles"
    :role="role"
    :aria-live="ariaLive"
    v-bind="$attrs"
  >
      <!-- Icon (optional) -->
    <div v-if="showIcon" class="flex-shrink-0">
      <slot name="icon">
        <Icon
          :name="iconName"
          :size="iconSize"
          :class="iconClass"
          :aria-label="iconAriaLabel"
        />
      </slot>
    </div>

    <!-- Content -->
    <div class="flex-1">
      <!-- Title (optional) -->
      <h3 v-if="title" :class="titleClasses">
        {{ title }}
      </h3>

      <!-- Message -->
      <div :class="messageClasses">
        <slot>
          {{ message }}
        </slot>
      </div>

      <!-- Actions (optional slot) -->
      <div v-if="$slots.actions" :class="actionsClasses">
        <slot name="actions" />
      </div>
    </div>

    <!-- Dismiss button (optional) -->
    <button
      v-if="dismissible"
      :class="dismissButtonClasses"
      @click="handleDismiss"
      :aria-label="dismissAriaLabel"
    >
      <Icon
        name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M6 18L18 6M6 6l12 12' /></svg>"
        :size="16"
        is-svg
      />
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Icon from './Icon.vue'

export interface AlertProps {
  /** Type of alert */
  type?: 'success' | 'error' | 'warning' | 'info' | 'neutral'
  /** Title of the alert */
  title?: string
  /** Message content (can be overridden by slot) */
  message?: string
  /** Whether the alert can be dismissed */
  dismissible?: boolean
  /** Whether to show an icon */
  showIcon?: boolean
  /** Size of the alert */
  size?: 'sm' | 'md' | 'lg'
  /** Additional CSS classes */
  class?: string
  /** ARIA live attribute for accessibility */
  ariaLive?: 'polite' | 'assertive' | 'off'
  /** Role for accessibility */
  role?: string
}

const props = withDefaults(defineProps<AlertProps>(), {
  type: 'info',
  dismissible: false,
  showIcon: true,
  size: 'md',
  ariaLive: 'polite',
  role: 'alert',
})

const emit = defineEmits<{
  /** Emitted when the alert is dismissed */
  dismiss: []
}>()

// Icon configuration based on alert type
const iconConfig = computed(() => {
  const configs = {
    success: {
      name: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>',
      ariaLabel: 'Success',
    },
    error: {
      name: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>',
      ariaLabel: 'Error',
    },
    warning: {
      name: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.732 16.5c-.77.833.192 2.5 1.732 2.5z" /></svg>',
      ariaLabel: 'Warning',
    },
    info: {
      name: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
      ariaLabel: 'Information',
    },
    neutral: {
      name: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
      ariaLabel: 'Notice',
    },
  }
  
  return configs[props.type] || configs.info
})

const iconName = computed(() => iconConfig.value.name)
const iconAriaLabel = computed(() => iconConfig.value.ariaLabel)
const iconSize = computed(() => (props.size === 'sm' ? 16 : props.size === 'lg' ? 24 : 20))

// Color classes based on alert type
const colorClasses = computed(() => {
  const classes = {
    success: {
      bg: 'bg-green-50 dark:bg-green-900/20',
      border: 'border-green-200 dark:border-green-800',
      text: 'text-green-800 dark:text-green-300',
      icon: 'text-green-600 dark:text-green-400',
    },
    error: {
      bg: 'bg-red-50 dark:bg-red-900/20',
      border: 'border-red-200 dark:border-red-800',
      text: 'text-red-800 dark:text-red-300',
      icon: 'text-red-600 dark:text-red-400',
    },
    warning: {
      bg: 'bg-yellow-50 dark:bg-yellow-900/20',
      border: 'border-yellow-200 dark:border-yellow-800',
      text: 'text-yellow-800 dark:text-yellow-300',
      icon: 'text-yellow-600 dark:text-yellow-400',
    },
    info: {
      bg: 'bg-blue-50 dark:bg-blue-900/20',
      border: 'border-blue-200 dark:border-blue-800',
      text: 'text-blue-800 dark:text-blue-300',
      icon: 'text-blue-600 dark:text-blue-400',
    },
    neutral: {
      bg: 'bg-gray-50 dark:bg-gray-800/50',
      border: 'border-gray-200 dark:border-gray-700',
      text: 'text-gray-800 dark:text-gray-300',
      icon: 'text-gray-600 dark:text-gray-400',
    },
  }
  
  return classes[props.type] || classes.info
})

// Size classes
const sizeClasses = computed(() => {
  return {
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-3',
    lg: 'px-6 py-4 text-lg',
  }[props.size]
})

// Generate alert classes
const alertClasses = computed(() => {
  const classes = [
    'alert',
    'rounded-lg',
    'border',
    'flex',
    'items-start',
    'gap-3',
    colorClasses.value.bg,
    colorClasses.value.border,
    sizeClasses.value,
  ]
  
  if (props.class) {
    classes.push(props.class)
  }
  
  return classes.join(' ')
})

// Icon classes
const iconClass = computed(() => [
  colorClasses.value.icon,
  'mt-0.5',
].join(' '))

// Title classes
const titleClasses = computed(() => [
  'font-semibold',
  'mb-1',
  colorClasses.value.text,
])

// Message classes
const messageClasses = computed(() => [
  colorClasses.value.text,
  props.size === 'sm' ? 'text-sm' : '',
])

// Actions classes
const actionsClasses = computed(() => [
  'mt-3',
  'flex',
  'gap-2',
])

// Dismiss button classes
const dismissButtonClasses = computed(() => [
  'flex-shrink-0',
  'p-1',
  'rounded',
  'hover:bg-black/5',
  'dark:hover:bg-white/10',
  'transition-colors',
  'focus:outline-none',
  'focus:ring-2',
  'focus:ring-offset-2',
  'focus:ring-current',
  colorClasses.value.icon,
])

// Dismiss ARIA label
const dismissAriaLabel = computed(() => `Dismiss ${props.type} alert`)

// Inline styles (if needed)
const alertStyles = computed(() => ({})) // Can be extended for custom styles

// Handle dismiss
const handleDismiss = () => {
  emit('dismiss')
}
</script>

<style scoped>
.alert {
  position: relative;
}

/* Animation for appearing alerts */
.alert-enter-active,
.alert-leave-active {
  transition: all 0.3s ease;
}

.alert-enter-from,
.alert-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>