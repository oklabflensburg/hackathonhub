<template>
  <div
    class="card-hover group relative cursor-pointer focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
    role="link"
    :aria-label="`View details for ${hackathon.name}`"
    tabindex="0"
    @click="$emit('open', hackathon.id)"
    @keydown.enter="$emit('open', hackathon.id)"
    @keydown.space.prevent="$emit('open', hackathon.id)"
  >
    <div class="w-full overflow-hidden rounded-t-lg mb-4 aspect-ratio-16-9">
      <img :src="hackathon.imageUrl" :alt="hackathon.name" class="img-cover group-hover:scale-105 transition-transform duration-300" />
    </div>
    <div class="flex items-start justify-between mb-4">
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1 group-hover:text-primary-600 dark:group-hover:text-primary-400">{{ hackathon.name }}</h3>
        <p class="text-sm text-gray-600 dark:text-gray-400">{{ hackathon.organization }}</p>
      </div>
      <span class="badge badge-primary">{{ hackathon.status }}</span>
    </div>
    <p class="text-gray-600 dark:text-gray-400 mb-4 text-sm">{{ hackathon.description }}</p>
    <div class="flex items-center justify-between text-sm">
      <div class="flex items-center space-x-4">
        <span class="flex items-center text-gray-500 dark:text-gray-400">{{ hackathon.duration }}</span>
        <span class="flex items-center text-gray-500 dark:text-gray-400">{{ hackathon.participants }}</span>
      </div>
      <span class="text-primary-600 dark:text-primary-400 font-medium">{{ viewDetailsLabel }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ hackathon: any; viewDetailsLabel: string }>()
defineEmits<{ (e: 'open', id: number): void }>()
</script>
