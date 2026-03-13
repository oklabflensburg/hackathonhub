<template>
  <span class="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700 dark:bg-gray-700 dark:text-gray-200">
    {{ label }}
  </span>
</template>

<script setup lang="ts">
defineProps<{ label: string }>()
</script>
