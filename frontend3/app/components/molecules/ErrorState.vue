<template>
  <div class="text-center py-12">
    <div class="w-24 h-24 mx-auto mb-6 text-red-400">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.342 16.5c-.77.833.192 2.5 1.732 2.5z" />
      </svg>
    </div>
    <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
      {{ title }}
    </h3>
    <p class="text-gray-600 dark:text-gray-400 mb-6">{{ message }}</p>
    <button v-if="showRetry" @click="$emit('retry')" class="btn btn-primary">
      {{ retryLabel }}
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  message: string
  retryLabel?: string
  showRetry?: boolean
}

withDefaults(defineProps<Props>(), {
  retryLabel: 'Try again',
  showRetry: true,
})

defineEmits<{
  retry: []
}>()
</script>