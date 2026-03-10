<template>
  <div
    v-if="message"
    :class="[
      'error-message',
      'text-sm rounded-lg p-3 border',
      type === 'error' ? 'bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300 border-red-200 dark:border-red-800' :
      type === 'warning' ? 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800' :
      type === 'success' ? 'bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-300 border-green-200 dark:border-green-800' :
      'bg-gray-50 dark:bg-gray-800 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-700'
    ]"
    role="alert"
    :aria-live="ariaLive"
  >
    <div class="flex items-start">
      <div class="flex-shrink-0">
        <svg
          v-if="type === 'error'"
          class="w-5 h-5 text-red-500 dark:text-red-400"
          fill="currentColor"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
            clip-rule="evenodd"
          />
        </svg>
        <svg
          v-else-if="type === 'warning'"
          class="w-5 h-5 text-yellow-500 dark:text-yellow-400"
          fill="currentColor"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
            clip-rule="evenodd"
          />
        </svg>
        <svg
          v-else-if="type === 'success'"
          class="w-5 h-5 text-green-500 dark:text-green-400"
          fill="currentColor"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
            clip-rule="evenodd"
          />
        </svg>
        <svg
          v-else
          class="w-5 h-5 text-gray-500 dark:text-gray-400"
          fill="currentColor"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
      <div class="ml-3 flex-1">
        <p class="font-medium">{{ title || defaultTitle }}</p>
        <p class="mt-1">{{ message }}</p>
        <div v-if="details" class="mt-2 text-xs opacity-80">
          {{ details }}
        </div>
      </div>
      <button
        v-if="dismissible"
        type="button"
        class="ml-auto -mx-1.5 -my-1.5 rounded-lg p-1.5 inline-flex h-8 w-8"
        :class="[
          type === 'error' ? 'text-red-500 hover:bg-red-100 dark:hover:bg-red-900/30' :
          type === 'warning' ? 'text-yellow-500 hover:bg-yellow-100 dark:hover:bg-yellow-900/30' :
          type === 'success' ? 'text-green-500 hover:bg-green-100 dark:hover:bg-green-900/30' :
          'text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'
        ]"
        @click="$emit('dismiss')"
        aria-label="Close"
      >
        <span class="sr-only">Schließen</span>
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
          <path
            fill-rule="evenodd"
            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  message?: string
  type?: 'error' | 'warning' | 'success' | 'info'
  title?: string
  details?: string
  dismissible?: boolean
  ariaLive?: 'polite' | 'assertive' | 'off'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'error',
  dismissible: false,
  ariaLive: 'polite'
})

defineEmits<{
  dismiss: []
}>()

const defaultTitle = {
  error: 'Fehler',
  warning: 'Warnung',
  success: 'Erfolg',
  info: 'Information'
}[props.type]
</script>

<style scoped>
.error-message {
  transition: opacity 0.2s ease;
}
</style>