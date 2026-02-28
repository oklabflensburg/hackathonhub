<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
    <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">{{ title }}</h2>
    <div class="prose dark:prose-invert max-w-none">
      <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line">{{ description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  description: string
}

defineProps<Props>()
</script>
