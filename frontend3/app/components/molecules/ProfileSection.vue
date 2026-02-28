<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6 mb-6">
    <div v-if="title" class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-semibold text-gray-900 dark:text-white">{{ title }}</h2>
      <div v-if="showAction" class="flex items-center space-x-3">
        <slot name="action" />
      </div>
    </div>
    
    <div v-if="loading" class="flex justify-center py-8">
      <LoadingSpinner size="md" />
    </div>
    
    <div v-else-if="error" class="text-center py-8">
      <p class="text-red-600 dark:text-red-400 mb-3">{{ error }}</p>
      <Button v-if="showRetry" variant="secondary" size="sm" @click="$emit('retry')">
        Retry
      </Button>
    </div>
    
    <div v-else-if="empty && showEmptyState" class="text-center py-8 text-gray-500 dark:text-gray-400">
      <slot name="empty">
        <p>{{ emptyText }}</p>
      </slot>
    </div>
    
    <div v-else>
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from '../atoms/Button.vue'
import LoadingSpinner from '../atoms/LoadingSpinner.vue'

interface Props {
  title?: string
  loading?: boolean
  error?: string
  empty?: boolean
  showEmptyState?: boolean
  emptyText?: string
  showAction?: boolean
  showRetry?: boolean
}

withDefaults(defineProps<Props>(), {
  title: '',
  loading: false,
  error: '',
  empty: false,
  showEmptyState: true,
  emptyText: 'No data available',
  showAction: false,
  showRetry: false,
})

defineEmits<{
  retry: []
}>()
</script>