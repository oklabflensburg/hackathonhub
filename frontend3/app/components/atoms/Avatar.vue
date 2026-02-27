<template>
  <div :class="containerClasses">
    <img v-if="src" :src="src" :alt="alt" class="w-full h-full object-cover" />
    <span v-else :class="textClasses">{{ initials }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  src?: string | null
  alt?: string
  fallbackText?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

const props = withDefaults(defineProps<Props>(), {
  src: null,
  alt: 'Avatar',
  fallbackText: 'U',
  size: 'md',
})

const sizeClasses = {
  sm: 'w-8 h-8',
  md: 'w-10 h-10',
  lg: 'w-12 h-12',
  xl: 'w-16 h-16',
}

const textSizeClasses = {
  sm: 'text-xs',
  md: 'text-sm',
  lg: 'text-base',
  xl: 'text-xl',
}

const initials = computed(() => props.fallbackText?.charAt(0)?.toUpperCase() || 'U')

const containerClasses = computed(() => [
  sizeClasses[props.size],
  'rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center overflow-hidden',
])

const textClasses = computed(() => [
  textSizeClasses[props.size],
  'font-medium text-gray-700 dark:text-gray-300',
])
</script>
