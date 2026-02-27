<template>
  <div
    class="card-hover group relative cursor-pointer focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
    role="link"
    :aria-label="`View details for ${project.name}`"
    tabindex="0"
    @click="$emit('open', project.id, $event)"
    @keydown.enter="$emit('open-direct', project.id)"
    @keydown.space.prevent="$emit('open-direct', project.id)"
  >
    <div class="relative w-full mb-4 overflow-hidden rounded-lg aspect-ratio-4-3">
      <img :src="project.imageUrl" :alt="project.name" class="img-cover transition-transform duration-300 group-hover:scale-105" />
      <div class="absolute top-2 right-2">
        <span class="badge badge-success">{{ project.hackathon }}</span>
      </div>
    </div>

    <div class="flex items-start justify-between mb-3">
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1 group-hover:text-primary-600 dark:group-hover:text-primary-400">{{ project.name }}</h3>
        <p class="text-sm text-gray-600 dark:text-gray-400">{{ byLabel }} {{ project.author }}</p>
      </div>
    </div>
    <p class="text-gray-600 dark:text-gray-400 mb-4 text-sm line-clamp-2">{{ project.description }}</p>

    <div class="flex items-center justify-between" @click.stop>
      <VoteButtons :project-id="project.id" :initial-upvotes="project.upvotes" :initial-downvotes="project.downvotes" :initial-user-vote="project.userVote" class="vote-button" />
      <span class="text-sm text-gray-500 dark:text-gray-400">{{ project.tech.join(', ') }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import VoteButtons from '~/components/VoteButtons.vue'

defineProps<{ project: any; byLabel: string }>()
defineEmits<{ (e: 'open', id: number, ev: MouseEvent): void; (e: 'open-direct', id: number): void }>()
</script>
