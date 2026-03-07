<template>
  <div
    :class="skeletonClasses"
    :style="skeletonStyles"
    :aria-label="ariaLabel"
    role="status"
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue'

export interface SkeletonProps {
  /** Type of skeleton element */
  type?: 'text' | 'circle' | 'rectangle' | 'card'
  /** Width of the skeleton (CSS value or Tailwind class) */
  width?: string
  /** Height of the skeleton (CSS value or Tailwind class) */
  height?: string
  /** Number of skeleton elements to render (for text lines) */
  count?: number
  /** Animation type */
  animation?: 'pulse' | 'wave' | 'none'
  /** Border radius (CSS value) */
  borderRadius?: string
  /** Additional CSS classes */
  class?: string
  /** ARIA label for accessibility */
  ariaLabel?: string
}

const props = withDefaults(defineProps<SkeletonProps>(), {
  type: 'text',
  width: '100%',
  height: '1rem',
  count: 1,
  animation: 'pulse',
  borderRadius: '0.25rem',
  ariaLabel: 'Loading content',
})

// Generate skeleton classes based on props
const skeletonClasses = computed(() => {
  const classes = ['skeleton', 'bg-gray-200', 'dark:bg-gray-700']
  
  // Add animation class
  if (props.animation === 'pulse') {
    classes.push('animate-pulse')
  } else if (props.animation === 'wave') {
    classes.push('skeleton-wave')
  }
  
  // Add type-specific classes
  if (props.type === 'circle') {
    classes.push('rounded-full')
  } else if (props.type === 'card') {
    classes.push('rounded-lg', 'shadow-sm')
  } else if (props.type === 'rectangle') {
    classes.push('rounded')
  } else {
    // text type
    classes.push('rounded')
  }
  
  // Handle width/height as Tailwind classes
  if (props.width && props.width.startsWith('w-')) {
    classes.push(props.width)
  }
  if (props.height && props.height.startsWith('h-')) {
    classes.push(props.height)
  }
  
  // Add custom classes
  if (props.class) {
    classes.push(props.class)
  }
  
  return classes.join(' ')
})

// Generate inline styles for width, height, and borderRadius
const skeletonStyles = computed(() => {
  const styles: Record<string, string> = {}
  
  // Set width if it's not a Tailwind class
  if (props.width && !props.width.startsWith('w-')) {
    styles.width = props.width
  }
  
  // Set height if it's not a Tailwind class
  if (props.height && !props.height.startsWith('h-')) {
    styles.height = props.height
  }
  
  // Set border radius
  if (props.borderRadius) {
    styles.borderRadius = props.borderRadius
  }
  
  return styles
})
</script>

<style scoped>
.skeleton {
  display: inline-block;
  position: relative;
  overflow: hidden;
}

/* Pulse animation (using Tailwind's animate-pulse) */

/* Wave animation */
.skeleton-wave {
  position: relative;
  overflow: hidden;
}

.skeleton-wave::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  animation: skeleton-wave 1.5s ease-in-out infinite;
}

@keyframes skeleton-wave {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Dark mode adjustments */
.dark .skeleton-wave::after {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.05),
    transparent
  );
}

/* Text skeleton specific styles */
.skeleton.text {
  margin-bottom: 0.5rem;
}

.skeleton.text:last-child {
  margin-bottom: 0;
}

/* Circle skeleton */
.skeleton.circle {
  aspect-ratio: 1 / 1;
}

/* Card skeleton */
.skeleton.card {
  padding: 1rem;
}
</style>