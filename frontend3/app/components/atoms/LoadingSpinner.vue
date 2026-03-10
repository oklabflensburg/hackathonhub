<template>
  <div
    :class="[
      'loading-spinner',
      'inline-flex items-center justify-center',
      size === 'sm' ? 'w-4 h-4' :
      size === 'md' ? 'w-6 h-6' :
      size === 'lg' ? 'w-8 h-8' :
      size === 'xl' ? 'w-12 h-12' :
      'w-6 h-6'
    ]"
    role="status"
    :aria-label="label"
  >
    <svg
      class="animate-spin"
      :class="[
        color === 'primary' ? 'text-primary-600 dark:text-primary-400' :
        color === 'white' ? 'text-white' :
        color === 'gray' ? 'text-gray-600 dark:text-gray-400' :
        'text-current'
      ]"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
    <span v-if="showText" class="ml-2 text-sm text-gray-600 dark:text-gray-400">
      {{ text || 'Lädt...' }}
    </span>
  </div>
</template>

<script setup lang="ts">
interface Props {
  size?: 'sm' | 'md' | 'lg' | 'xl'
  color?: 'primary' | 'white' | 'gray' | 'current'
  showText?: boolean
  text?: string
  label?: string
}

withDefaults(defineProps<Props>(), {
  size: 'md',
  color: 'primary',
  showText: false,
  label: 'Lädt'
})
</script>

<style scoped>
.loading-spinner {
  transition: opacity 0.2s ease;
}
</style>
