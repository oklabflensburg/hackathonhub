<template>
  <div class="mb-8">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ title }}</h1>
    <p class="text-gray-600 dark:text-gray-400 mt-2">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description: string
}>()
</script>
