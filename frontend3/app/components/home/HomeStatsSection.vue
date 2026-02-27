<template>
  <section class="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
    <NuxtLink v-for="item in items" :key="item.label" :to="item.to" class="card text-center cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900" role="link" tabindex="0">
      <div :class="['text-3xl font-bold mb-2', item.valueClass]">{{ item.value }}</div>
      <div class="text-gray-600 dark:text-gray-400">{{ item.label }}</div>
    </NuxtLink>
  </section>
</template>

<script setup lang="ts">
defineProps<{ items: Array<{ to: string; value: number | string; label: string; valueClass: string }> }>()
</script>
