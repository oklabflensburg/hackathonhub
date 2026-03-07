<template>
  <div
    class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border p-4 animate-slide-in"
    :class="borderClasses"
  >
    <div class="flex items-start justify-between">
      <div class="flex items-start space-x-3">
        <NotificationIcon :type="type" />
        
        <!-- Content -->
        <div class="flex-1">
          <h4 class="font-semibold text-gray-900 dark:text-white mb-1">
            {{ title }}
          </h4>
          <p class="text-sm text-gray-600 dark:text-gray-300">
            {{ message }}
          </p>
          
          <!-- Action Button -->
          <div v-if="actionLabel" class="mt-3">
            <button
              @click="$emit('action')"
              class="text-sm font-medium text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors"
            >
              {{ actionLabel }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- Close Button -->
      <button
        v-if="dismissible"
        @click="$emit('dismiss')"
        class="flex-shrink-0 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
        aria-label="Dismiss notification"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    
    <!-- Progress Bar -->
    <div v-if="autoDismiss && progress" class="mt-3">
      <div class="h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        <div
          class="h-full transition-all duration-300"
          :class="progressBarClasses"
          :style="{ width: `${progress}%` }"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import NotificationIcon from '~/components/atoms/NotificationIcon.vue'

interface Props {
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  actionLabel?: string
  dismissible?: boolean
  autoDismiss?: boolean
  progress?: number
}

withDefaults(defineProps<Props>(), {
  dismissible: true,
  autoDismiss: false,
  progress: 0
})

const props = defineProps<Props>()
defineEmits<{
  action: []
  dismiss: []
}>()

const borderClasses = computed(() => {
  const classes = {
    'success': 'border-green-200 dark:border-green-800',
    'error': 'border-red-200 dark:border-red-800',
    'warning': 'border-yellow-200 dark:border-yellow-800',
    'info': 'border-blue-200 dark:border-blue-800'
  }
  return classes[props.type]
})

const progressBarClasses = computed(() => {
  const classes = {
    'success': 'bg-green-500',
    'error': 'bg-red-500',
    'warning': 'bg-yellow-500',
    'info': 'bg-blue-500'
  }
  return classes[props.type]
})
</script>