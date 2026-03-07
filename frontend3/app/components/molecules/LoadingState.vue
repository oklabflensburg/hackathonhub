<template>
  <div class="flex flex-col items-center justify-center py-12 text-center">
    <LoadingSpinner v-if="showSpinner" :size="size" class="mb-4" />
    <div v-else class="mb-4">
      <Icon name="loader" :size="size === 'lg' ? 48 : size === 'md' ? 32 : 24" class="animate-spin text-gray-400" />
    </div>
    <h3 v-if="title" class="text-lg font-medium text-gray-900 mb-2">{{ title }}</h3>
    <p v-if="message" class="text-gray-600 max-w-md">{{ message }}</p>
    <slot />
  </div>
</template>

<script setup lang="ts">
import LoadingSpinner from '~/components/atoms/LoadingSpinner.vue'
import Icon from '~/components/atoms/Icon.vue'

interface Props {
  title?: string
  message?: string
  showSpinner?: boolean
  size?: 'sm' | 'md' | 'lg'
}

withDefaults(defineProps<Props>(), {
  showSpinner: true,
  size: 'md'
})
</script>