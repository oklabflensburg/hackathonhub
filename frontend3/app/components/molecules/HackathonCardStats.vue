<template>
  <div class="grid grid-cols-3 gap-4 py-4 border-t border-gray-100 dark:border-gray-800">
    <div class="text-center">
      <div class="text-xl font-bold text-gray-900 dark:text-white">{{ participants }}</div>
      <div class="text-xs text-gray-500 dark:text-gray-400">{{ participantsLabel }}</div>
    </div>
    <div class="text-center">
      <div class="text-xl font-bold text-gray-900 dark:text-white">{{ projects }}</div>
      <div class="text-xs text-gray-500 dark:text-gray-400">{{ projectsLabel }}</div>
    </div>
    <div class="text-center">
      <div class="text-xl font-bold text-gray-900 dark:text-white">{{ duration }}</div>
      <div class="text-xs text-gray-500 dark:text-gray-400">{{ durationLabel }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  participants: number | string
  participantsLabel: string
  projects: number | string
  projectsLabel: string
  duration: string
  durationLabel: string
}

defineProps<Props>()
</script>