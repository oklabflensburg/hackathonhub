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
    <div class="relative h-48 mb-4 rounded-xl overflow-hidden">
      <img :src="hackathon.image" :alt="hackathon.name" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
      <div class="absolute top-4 right-4">
        <span :class="['badge', statusBadgeClass]">{{ hackathon.status }}</span>
      </div>
      <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
        <h3 class="text-xl font-bold text-white">{{ hackathon.name }}</h3>
      </div>
    </div>

    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
            <span class="text-sm font-medium text-gray-600 dark:text-gray-400">{{ hackathon.organization.charAt(0) }}</span>
          </div>
          <span class="text-gray-600 dark:text-gray-400">{{ hackathon.organization }}</span>
        </div>
        <div v-if="hackathon.prize" class="text-right">
          <div class="text-lg font-bold text-gray-900 dark:text-white">{{ hackathon.prize }}</div>
          <div class="text-sm text-gray-500 dark:text-gray-400">{{ prizePoolLabel }}</div>
        </div>
      </div>

      <p class="text-gray-600 dark:text-gray-400 text-sm">{{ hackathon.description }}</p>

      <div class="grid grid-cols-3 gap-4 py-4 border-t border-gray-100 dark:border-gray-800">
        <div class="text-center">
          <div class="text-xl font-bold text-gray-900 dark:text-white">{{ hackathon.participants }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">{{ participantsLabel }}</div>
        </div>
        <div class="text-center">
          <div class="text-xl font-bold text-gray-900 dark:text-white">{{ hackathon.projects }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">{{ projectsLabel }}</div>
        </div>
        <div class="text-center">
          <div class="text-xl font-bold text-gray-900 dark:text-white">{{ hackathon.duration }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">{{ durationLabel }}</div>
        </div>
      </div>

      <div class="flex items-center justify-between text-sm">
        <div class="flex items-center text-gray-500 dark:text-gray-400">{{ hackathon.startDate }} - {{ hackathon.endDate }}</div>
        <span class="text-gray-500 dark:text-gray-400">{{ hackathon.location }}</span>
      </div>

      <div class="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-800">
        <div class="flex items-center space-x-2">
          <span v-for="tag in hackathon.tags.slice(0, 2)" :key="tag" class="badge badge-primary text-xs">{{ tag }}</span>
          <span v-if="hackathon.tags.length > 2" class="text-xs text-gray-500 dark:text-gray-400">+{{ hackathon.tags.length - 2 }}</span>
        </div>
        <NuxtLink :to="`/hackathons/${hackathon.id}`" class="btn btn-primary px-4 py-2 text-sm" @click.stop>
          {{ viewDetailsLabel }}
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  hackathon: any
  participantsLabel: string
  projectsLabel: string
  durationLabel: string
  prizePoolLabel: string
  viewDetailsLabel: string
}>()

defineEmits<{ (e: 'open', id: number): void }>()

const statusBadgeClass = computed(() => {
  if (props.hackathon.status === 'Active') return 'badge-success'
  if (props.hackathon.status === 'Upcoming') return 'badge-warning'
  if (props.hackathon.status === 'Completed') return 'badge-info'
  return 'badge-primary'
})
</script>