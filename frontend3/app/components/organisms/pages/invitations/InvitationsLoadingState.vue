<template>
  <div class="text-center py-12">
    <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
    <p class="mt-4 text-gray-600 dark:text-gray-400">{{ text }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>
