<template>
  <section class="text-center py-12">
    <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">{{ title }}</h2>
    <p class="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">{{ description }}</p>
    <div class="flex flex-wrap justify-center gap-4">
      <NuxtLink to="/create" class="btn btn-primary px-8 py-3 text-lg">{{ createLabel }}</NuxtLink>
      <button v-if="!isAuthenticated" @click="$emit('signup')" class="btn btn-outline px-8 py-3 text-lg">{{ signupLabel }}</button>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{ title: string; description: string; createLabel: string; signupLabel: string; isAuthenticated: boolean }>()
defineEmits<{ (e: 'signup'): void }>()
</script>
