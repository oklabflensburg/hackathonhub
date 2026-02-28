<template>
  <Card v-if="technologies.length > 0">
    <template #header>
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ title }}</h2>
    </template>
    <div class="flex flex-wrap gap-3">
      <NuxtLink
        v-for="tech in technologies"
        :key="tech"
        :to="`/projects?technology=${encodeURIComponent(tech)}`"
        class="px-4 py-2 bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-300 rounded-lg text-sm font-medium hover:bg-primary-200 dark:hover:bg-primary-800 transition-colors"
      >
        {{ tech }}
      </NuxtLink>
    </div>
  </Card>
</template>

<script setup lang="ts">
import Card from '~/components/atoms/Card.vue'

defineProps<{
  technologies: string[]
  title: string
}>()
</script>