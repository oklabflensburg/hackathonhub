<template>
  <div>
    <h3 class="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4">{{ title }}</h3>
    <ul class="space-y-3">
      <li v-for="link in links" :key="link.label">
        <NuxtLink :to="link.to" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
          {{ link.label }}
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
interface FooterLink {
  label: string
  to: string
}

defineProps<{
  title: string
  links: FooterLink[]
}>()
</script>
