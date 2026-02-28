<template>
  <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-gray-500 dark:text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
        </svg>
        <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ title }}</span>
      </div>
      <button
        v-if="showClear"
        @click="$emit('clear')"
        class="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 flex items-center"
      >
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        {{ clearLabel }}
      </button>
    </div>
    <div class="flex flex-wrap gap-2">
      <span
        v-for="tag in tags"
        :key="tag"
        class="px-3 py-1.5 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 text-sm rounded-full flex items-center"
      >
        {{ tag }}
        <button
          @click="$emit('remove', tag)"
          class="ml-2 text-primary-500 hover:text-primary-700 dark:hover:text-primary-200"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  tags: string[]
  clearLabel?: string
  showClear?: boolean
}

withDefaults(defineProps<Props>(), {
  clearLabel: 'Clear all',
  showClear: true,
})

defineEmits<{
  remove: [tag: string]
  clear: []
}>()
</script>