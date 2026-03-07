<template>
  <component
    :is="to ? 'NuxtLink' : 'button'"
    :type="to ? undefined : type"
    :disabled="disabled"
    :to="to"
    :class="[
      'inline-flex items-center justify-center font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:opacity-50 disabled:cursor-not-allowed',
      sizeClasses,
      variantClasses,
      rounded && 'rounded-lg',
      fullWidth && 'w-full',
      className
    ]"
    @click="handleClick"
    @blur="$emit('blur', $event)"
    @focus="$emit('focus', $event)"
  >
    <slot name="icon-left" />
    <span v-if="$slots.default" :class="[iconLeft || iconRight ? (size === 'sm' ? 'ml-2' : 'ml-3') : '', size === 'sm' ? 'text-sm' : 'text-base']">
      <slot />
    </span>
    <slot name="icon-right" />
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  type?: 'button' | 'submit' | 'reset'
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size?: 'xs' | 'sm' | 'md' | 'lg'
  disabled?: boolean
  rounded?: boolean
  fullWidth?: boolean
  className?: string
  iconLeft?: boolean
  iconRight?: boolean
  to?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'button',
  variant: 'primary',
  size: 'md',
  disabled: false,
  rounded: true,
  fullWidth: false,
  className: '',
  iconLeft: false,
  iconRight: false,
  to: undefined
})

const emit = defineEmits<{
  click: [event: MouseEvent]
  blur: [event: FocusEvent]
  focus: [event: FocusEvent]
}>()

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'xs': return 'px-2 py-1 text-xs'
    case 'sm': return 'px-3 py-2 text-sm'
    case 'md': return 'px-4 py-3 text-base'
    case 'lg': return 'px-6 py-4 text-lg'
    default: return 'px-4 py-3 text-base'
  }
})

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'primary':
      return 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500/20'
    case 'secondary':
      return 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600 focus:ring-gray-500/20'
    case 'outline':
      return 'border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 focus:ring-gray-500/20'
    case 'ghost':
      return 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 focus:ring-gray-500/20'
    case 'danger':
      return 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500/20'
    default:
      return 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500/20'
  }
})

const handleClick = (event: MouseEvent) => {
  if (props.disabled) {
    event.preventDefault()
    return
  }
  emit('click', event)
}
</script>
