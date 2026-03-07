<template>
  <Card>
    <template #header>
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ title }}</h2>
    </template>
    <div class="space-y-4">
      <a
        v-if="repositoryUrl"
        :href="repositoryUrl"
        target="_blank"
        rel="noopener noreferrer"
        class="flex items-center space-x-3 p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
      >
        <div class="flex-1">
          <p class="font-medium text-gray-900 dark:text-white">{{ repositoryLabel }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 truncate">{{ repositoryUrl }}</p>
        </div>
      </a>

      <a
        v-if="liveUrl"
        :href="liveUrl"
        target="_blank"
        rel="noopener noreferrer"
        class="flex items-center space-x-3 p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
      >
        <div class="flex-1">
          <p class="font-medium text-gray-900 dark:text-white">{{ liveLabel }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 truncate">{{ liveUrl }}</p>
        </div>
      </a>

      <div v-if="!repositoryUrl && !liveUrl" class="text-center py-4">
        <p class="text-gray-500 dark:text-gray-400">{{ emptyLabel }}</p>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import Card from '~/components/atoms/Card.vue'

defineProps<{
  title: string
  repositoryLabel: string
  liveLabel: string
  emptyLabel: string
  repositoryUrl?: string | null
  liveUrl?: string | null
}>()
</script>
