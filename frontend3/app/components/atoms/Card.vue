<template>
  <div :class="cardClasses">
    <div v-if="$slots.header" class="mb-4">
      <slot name="header" />
    </div>
    <slot />
    <div v-if="$slots.footer" class="mt-4">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  padding?: 'none' | 'sm' | 'md' | 'lg'
  rounded?: 'none' | 'md' | 'lg' | 'xl'
  shadow?: 'none' | 'sm' | 'md' | 'lg'
  background?: 'default' | 'subtle'
  border?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  padding: 'md',
  rounded: 'xl',
  shadow: 'lg',
  background: 'default',
  border: false,
})

const cardClasses = computed(() => {
  const paddingMap = {
    none: '',
    sm: 'p-3',
    md: 'p-6',
    lg: 'p-8',
  }

  const roundedMap = {
    none: '',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
  }

  const shadowMap = {
    none: '',
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
  }

  const backgroundMap = {
    default: 'bg-white dark:bg-gray-800',
    subtle: 'bg-gray-50 dark:bg-gray-900/40',
  }

  return [
    backgroundMap[props.background],
    paddingMap[props.padding],
    roundedMap[props.rounded],
    shadowMap[props.shadow],
    props.border ? 'border border-gray-200 dark:border-gray-700' : '',
  ]
})
</script>
