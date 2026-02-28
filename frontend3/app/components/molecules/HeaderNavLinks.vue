<template>
  <nav class="hidden lg:flex items-center space-x-8">
    <NuxtLink
      v-for="link in links"
      :key="link.to"
      :to="link.to"
      class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors"
      :class="{ 'text-primary-600 dark:text-primary-400': isActive(link.to) }"
    >
      {{ link.label }}
    </NuxtLink>
  </nav>
</template>

<script setup lang="ts">
interface NavLink {
  to: string
  label: string
}

interface Props {
  links: NavLink[]
  currentPath: string
}

const props = defineProps<Props>()

const isActive = (to: string) => props.currentPath === to
</script>
