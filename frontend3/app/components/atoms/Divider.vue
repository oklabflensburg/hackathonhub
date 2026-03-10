<template>
  <div
    :class="[
      'divider',
      orientation === 'horizontal' ? 'w-full' : 'h-full',
      orientation === 'horizontal' ? 'border-t' : 'border-l',
      dashed && 'border-dashed',
      thick && (orientation === 'horizontal' ? 'border-t-2' : 'border-l-2'),
      colorClass,
      className
    ]"
    :aria-orientation="orientation"
    role="separator"
  />
</template>

<script setup lang="ts">
interface Props {
  /** Orientation of the divider */
  orientation?: 'horizontal' | 'vertical'
  /** Whether to use dashed border */
  dashed?: boolean
  /** Whether to use thick border */
  thick?: boolean
  /** Color variant */
  color?: 'default' | 'light' | 'dark' | 'primary' | 'danger' | 'success' | 'warning'
  /** Additional CSS classes */
  className?: string
  /** Label for accessibility (optional) */
  label?: string
}

const props = withDefaults(defineProps<Props>(), {
  orientation: 'horizontal',
  dashed: false,
  thick: false,
  color: 'default',
  className: '',
  label: undefined
})

const colorClass = computed(() => {
  type ColorType = 'default' | 'light' | 'dark' | 'primary' | 'danger' | 'success' | 'warning'
  const map: Record<ColorType, string> = {
    default: 'border-gray-200 dark:border-gray-700',
    light: 'border-gray-100 dark:border-gray-800',
    dark: 'border-gray-300 dark:border-gray-600',
    primary: 'border-primary-500 dark:border-primary-400',
    danger: 'border-red-500 dark:border-red-400',
    success: 'border-green-500 dark:border-green-400',
    warning: 'border-yellow-500 dark:border-yellow-400'
  }
  return map[props.color as ColorType]
})
</script>

<style scoped>
.divider {
  box-sizing: border-box;
}

/* Ensure vertical divider has proper height when inside flex containers */
.divider[aria-orientation="vertical"] {
  align-self: stretch;
}
</style>