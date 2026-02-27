<template>
  <div class="h-48 relative">
    <div v-if="hackathon.image_url" class="absolute inset-0 bg-cover bg-center" :style="{ backgroundImage: `url(${hackathon.image_url})` }">
      <div class="absolute inset-0 bg-black/40"></div>
    </div>
    <div v-else class="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-600">
      <div class="absolute inset-0 bg-black/20"></div>
    </div>

    <div class="relative h-full flex items-center justify-center p-8">
      <div class="text-center">
        <h1 class="text-4xl font-bold text-white mb-2">{{ hackathon.name }}</h1>
        <div class="flex items-center justify-center space-x-4 text-white/90">
          <span class="flex items-center">
            {{ formatDateTime(hackathon.start_date) }} - {{ formatDateTime(hackathon.end_date) }}
          </span>
          <span class="flex items-center">
            {{ hackathon.location || virtualLabel }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  hackathon: any
  formatDateTime: (v: string) => string
  virtualLabel: string
}>()
</script>
