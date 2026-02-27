<template>
  <section class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary-500 to-purple-600 p-8 md:p-12 text-white">
    <div class="relative z-10 max-w-3xl">
      <h1 class="text-4xl md:text-5xl font-bold mb-4">{{ title }}</h1>
      <p class="text-xl mb-8 opacity-90">{{ description }}</p>
      <div class="flex flex-wrap gap-4">
        <NuxtLink to="/hackathons" class="btn bg-white text-primary-600 hover:bg-gray-100">{{ exploreLabel }}</NuxtLink>
        <NuxtLink to="/create" class="btn bg-transparent border-2 border-white hover:bg-white/10">{{ createLabel }}</NuxtLink>
      </div>
    </div>
    <div class="absolute top-0 right-0 w-32 h-32 sm:w-48 sm:h-48 md:w-64 md:h-64 bg-white/10 rounded-full -translate-y-16 sm:-translate-y-24 md:-translate-y-32 translate-x-16 sm:translate-x-24 md:translate-x-32" />
    <div class="absolute bottom-0 left-0 w-48 h-48 sm:w-64 sm:h-64 md:w-96 md:h-96 bg-white/5 rounded-full translate-y-24 sm:translate-y-32 md:translate-y-48 -translate-x-24 sm:-translate-x-32 md:-translate-x-48" />
  </section>
</template>

<script setup lang="ts">
defineProps<{ title: string; description: string; exploreLabel: string; createLabel: string }>()
</script>
