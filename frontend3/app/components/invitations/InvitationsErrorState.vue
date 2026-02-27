<template>
  <div class="text-center py-12">
    <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400 mb-4">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </div>
    <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">{{ title }}</h3>
    <p class="text-gray-600 dark:text-gray-400 mb-6">{{ message }}</p>
    <button class="btn btn-outline" @click="$emit('retry')">{{ retryLabel }}</button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  message: string
  retryLabel: string
}>()

defineEmits<{ (e: 'retry'): void }>()
</script>
