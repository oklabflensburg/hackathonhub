<template>
  <div class="tooltip-container" ref="containerRef">
    <!-- Trigger element -->
    <div
      ref="triggerRef"
      :class="triggerClasses"
      @mouseenter="handleMouseEnter"
      @mouseleave="handleMouseLeave"
      @focus="handleFocus"
      @blur="handleBlur"
      @click="handleClick"
      :tabindex="tabindex"
      :aria-describedby="tooltipId"
      v-bind="$attrs"
    >
      <slot name="trigger">
        <!-- Default trigger if no slot provided -->
        <Icon
          name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' /></svg>"
          :size="16"
          is-svg
          class="text-gray-500"
        />
      </slot>
    </div>

    <!-- Tooltip content -->
    <Teleport v-if="isMounted" to="body">
      <div
        v-if="isVisible"
        :id="tooltipId"
        ref="tooltipRef"
        :class="tooltipClasses"
        :style="tooltipStyles"
        role="tooltip"
        @mouseenter="handleTooltipMouseEnter"
        @mouseleave="handleTooltipMouseLeave"
      >
        <!-- Arrow -->
        <div v-if="showArrow" :class="arrowClasses" :style="arrowStyles" />

        <!-- Content -->
        <div :class="contentClasses">
          <slot>
            {{ content }}
          </slot>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import Icon from './Icon.vue'

export interface TooltipProps {
  /** Tooltip content (can be overridden by slot) */
  content?: string
  /** Position of the tooltip relative to the trigger */
  position?: 'top' | 'bottom' | 'left' | 'right' | 'top-start' | 'top-end' | 'bottom-start' | 'bottom-end'
  /** Delay before showing tooltip (ms) */
  delay?: number
  /** Whether to show an arrow */
  showArrow?: boolean
  /** Maximum width of the tooltip */
  maxWidth?: string
  /** Background color class */
  bgColor?: string
  /** Text color class */
  textColor?: string
  /** Whether the tooltip is disabled */
  disabled?: boolean
  /** Trigger behavior */
  trigger?: 'hover' | 'click' | 'focus' | 'manual'
  /** Tabindex for the trigger element */
  tabindex?: number
  /** Additional CSS classes for the tooltip */
  class?: string
}

const props = withDefaults(defineProps<TooltipProps>(), {
  position: 'top',
  delay: 100,
  showArrow: true,
  maxWidth: '16rem',
  bgColor: 'bg-gray-900 dark:bg-gray-700',
  textColor: 'text-white dark:text-gray-100',
  disabled: false,
  trigger: 'hover',
  tabindex: 0,
})

const emit = defineEmits<{
  /** Emitted when tooltip becomes visible */
  show: []
  /** Emitted when tooltip becomes hidden */
  hide: []
}>()

// Refs
const containerRef = ref<HTMLElement>()
const triggerRef = ref<HTMLElement>()
const tooltipRef = ref<HTMLElement>()
const isVisible = ref(false)
const isMounted = ref(false)
const showTimeout = ref<NodeJS.Timeout>()
const hideTimeout = ref<NodeJS.Timeout>()
const isHoveringTooltip = ref(false)

// Generate unique ID for accessibility
const tooltipId = computed(() => `tooltip-${Math.random().toString(36).substr(2, 9)}`)

// Position classes
const positionClasses = computed(() => {
  const base = 'absolute z-50'
  const positions = {
    'top': 'bottom-full left-1/2 transform -translate-x-1/2 mb-2',
    'bottom': 'top-full left-1/2 transform -translate-x-1/2 mt-2',
    'left': 'right-full top-1/2 transform -translate-y-1/2 mr-2',
    'right': 'left-full top-1/2 transform -translate-y-1/2 ml-2',
    'top-start': 'bottom-full left-0 mb-2',
    'top-end': 'bottom-full right-0 mb-2',
    'bottom-start': 'top-full left-0 mt-2',
    'bottom-end': 'top-full right-0 mt-2',
  }
  
  return `${base} ${positions[props.position]}`
})

// Arrow classes
const arrowClasses = computed(() => {
  const base = 'absolute w-2 h-2 transform rotate-45'
  const positions = {
    'top': 'bottom-[-4px] left-1/2 -translate-x-1/2',
    'bottom': 'top-[-4px] left-1/2 -translate-x-1/2',
    'left': 'right-[-4px] top-1/2 -translate-y-1/2',
    'right': 'left-[-4px] top-1/2 -translate-y-1/2',
    'top-start': 'bottom-[-4px] left-3',
    'top-end': 'bottom-[-4px] right-3',
    'bottom-start': 'top-[-4px] left-3',
    'bottom-end': 'top-[-4px] right-3',
  }
  
  return `${base} ${positions[props.position]} ${props.bgColor}`
})

// Tooltip classes
const tooltipClasses = computed(() => {
  const classes = [
    positionClasses.value,
    props.bgColor,
    props.textColor,
    'rounded-md',
    'px-3',
    'py-2',
    'text-sm',
    'font-normal',
    'shadow-lg',
    'whitespace-normal',
    'break-words',
  ]
  
  if (props.class) {
    classes.push(props.class)
  }
  
  return classes.join(' ')
})

// Content classes
const contentClasses = computed(() => [
  'relative',
  'z-10',
])

// Trigger classes
const triggerClasses = computed(() => [
  'inline-flex',
  'items-center',
  'justify-center',
  'cursor-help',
])

// Tooltip styles
const tooltipStyles = computed(() => ({
  maxWidth: props.maxWidth,
}))

// Arrow styles
const arrowStyles = computed(() => ({}))

// Show tooltip
const showTooltip = () => {
  if (props.disabled || isVisible.value) return
  
  clearTimeout(hideTimeout.value)
  
  showTimeout.value = setTimeout(() => {
    isVisible.value = true
    emit('show')
    nextTick(() => {
      updatePosition()
    })
  }, props.delay)
}

// Hide tooltip
const hideTooltip = () => {
  if (!isVisible.value) return
  
  clearTimeout(showTimeout.value)
  
  // If user is hovering over tooltip, don't hide immediately
  if (isHoveringTooltip.value && props.trigger === 'hover') {
    return
  }
  
  hideTimeout.value = setTimeout(() => {
    isVisible.value = false
    emit('hide')
    isHoveringTooltip.value = false
  }, 100)
}

// Update tooltip position
const updatePosition = () => {
  if (!triggerRef.value || !tooltipRef.value) return
  
  const triggerRect = triggerRef.value.getBoundingClientRect()
  const tooltipRect = tooltipRef.value.getBoundingClientRect()
  
  // For now, we rely on CSS positioning
  // In a more advanced implementation, we could adjust for viewport boundaries
}

// Event handlers
const handleMouseEnter = () => {
  if (props.trigger === 'hover' && !props.disabled) {
    showTooltip()
  }
}

const handleMouseLeave = () => {
  if (props.trigger === 'hover') {
    hideTooltip()
  }
}

const handleFocus = () => {
  if (props.trigger === 'focus' && !props.disabled) {
    showTooltip()
  }
}

const handleBlur = () => {
  if (props.trigger === 'focus') {
    hideTooltip()
  }
}

const handleClick = () => {
  if (props.trigger === 'click' && !props.disabled) {
    if (isVisible.value) {
      hideTooltip()
    } else {
      showTooltip()
    }
  }
}

const handleTooltipMouseEnter = () => {
  isHoveringTooltip.value = true
}

const handleTooltipMouseLeave = () => {
  isHoveringTooltip.value = false
  if (props.trigger === 'hover') {
    hideTooltip()
  }
}

// Manual control methods
const show = () => {
  if (!props.disabled) {
    showTooltip()
  }
}

const hide = () => {
  hideTooltip()
}

// Expose methods
defineExpose({
  show,
  hide,
})

// Lifecycle
onMounted(() => {
  isMounted.value = true
  
  // Add global click listener for click-away behavior
  if (props.trigger === 'click') {
    document.addEventListener('click', handleDocumentClick)
  }
})

onUnmounted(() => {
  clearTimeout(showTimeout.value)
  clearTimeout(hideTimeout.value)
  
  if (props.trigger === 'click') {
    document.removeEventListener('click', handleDocumentClick)
  }
})

// Handle click outside
const handleDocumentClick = (event: MouseEvent) => {
  if (
    isVisible.value &&
    triggerRef.value &&
    !triggerRef.value.contains(event.target as Node) &&
    tooltipRef.value &&
    !tooltipRef.value.contains(event.target as Node)
  ) {
    hideTooltip()
  }
}

// Watch for prop changes
watch(() => props.disabled, (disabled) => {
  if (disabled && isVisible.value) {
    hideTooltip()
  }
})

watch(() => props.position, () => {
  if (isVisible.value) {
    nextTick(() => {
      updatePosition()
    })
  }
})
</script>

<style scoped>
.tooltip-container {
  display: inline-block;
  position: relative;
}

/* Animation */
.tooltip-enter-active,
.tooltip-leave-active {
  transition: all 0.2s ease;
}

.tooltip-enter-from,
.tooltip-leave-to {
  opacity: 0;
  transform: translateY(-5px) scale(0.95);
}

.tooltip-enter-to,
.tooltip-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* For left/right positions */
.tooltip-enter-from[data-position^="left"],
.tooltip-leave-to[data-position^="left"] {
  transform: translateX(5px) scale(0.95);
}

.tooltip-enter-from[data-position^="right"],
.tooltip-leave-to[data-position^="right"] {
  transform: translateX(-5px) scale(0.95);
}
</style>