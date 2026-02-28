<template>
  <section class="mb-8">
    <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ title }}</h2>
    <div class="prose dark:prose-invert max-w-none">
      <p class="text-gray-700 dark:text-gray-300">{{ description }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title: string
  description: string
}>(), {
  description: ''
})
</script>
