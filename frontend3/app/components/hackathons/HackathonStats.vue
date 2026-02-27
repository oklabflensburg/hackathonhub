<template>
  <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4 sm:p-5 lg:p-6 mb-6">
    <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">{{ title }}</h3>
    <div class="space-y-4">
      <div class="flex justify-between items-center">
        <span class="text-gray-600 dark:text-gray-400">{{ labels.status }}</span>
        <span :class="statusClass" class="px-3 py-1 rounded-full text-sm font-medium capitalize">{{ hackathon.status }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-600 dark:text-gray-400">{{ labels.participants }}</span>
        <span class="font-bold text-gray-900 dark:text-white">{{ hackathon.participant_count || 0 }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-600 dark:text-gray-400">{{ labels.views }}</span>
        <span class="font-bold text-gray-900 dark:text-white">{{ hackathon.view_count || 0 }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-600 dark:text-gray-400">{{ labels.projects }}</span>
        <span class="font-bold text-gray-900 dark:text-white">{{ hackathon.project_count || 0 }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-600 dark:text-gray-400">{{ labels.registrationDeadline }}</span>
        <span class="font-bold text-gray-900 dark:text-white">{{ formatDateTime(hackathon.registration_deadline) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  hackathon: any
  title: string
  formatDateTime: (v: string) => string
  labels: Record<string, string>
}>()

const statusClass = computed(() => {
  if (props.hackathon.status === 'active') return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
  if (props.hackathon.status === 'upcoming') return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
  return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
})
</script>
