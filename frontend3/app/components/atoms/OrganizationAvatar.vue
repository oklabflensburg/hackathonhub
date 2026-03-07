<template>
  <div :class="avatarClasses" class="inline-flex items-center justify-center rounded-full font-medium">
    <span v-if="!imageUrl" class="text-gray-600 dark:text-gray-400">{{ initial }}</span>
    <img v-else :src="imageUrl" :alt="organizationName" class="w-full h-full object-cover rounded-full" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  organizationName: string
  imageUrl?: string
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md'
})

const initial = computed(() => {
  if (!props.organizationName) return '?'
  return props.organizationName.charAt(0).toUpperCase()
})

const avatarClasses = computed(() => {
  const sizes = {
    sm: 'w-6 h-6 text-xs',
    md: 'w-8 h-8 text-sm',
    lg: 'w-10 h-10 text-base'
  }
  
  const base = 'bg-gray-100 dark:bg-gray-800'
  return `${base} ${sizes[props.size]}`
})
</script>