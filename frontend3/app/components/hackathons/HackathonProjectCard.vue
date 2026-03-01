<template>
  <div class="card-hover group">
    <div class="relative h-48 mb-4 rounded-xl overflow-hidden">
      <img :src="project.image" :alt="project.name" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
      <div class="absolute top-4 right-4">
        <span :class="['badge', project.status === 'Winner' ? 'badge-success' : project.status === 'Finalist' ? 'badge-warning' : 'badge-primary']">
          {{ project.status }}
        </span>
      </div>
    </div>

    <div class="space-y-4">
      <div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">{{ project.name }}</h3>
        <p class="text-gray-600 dark:text-gray-400 text-sm">{{ project.description }}</p>
      </div>

      <div class="grid grid-cols-3 gap-4 py-4 border-t border-gray-100 dark:border-gray-800">
        <div class="text-center">
          <div class="text-xl font-bold text-gray-900 dark:text-white">{{ project.votes }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">{{ labels.votes }}</div>
        </div>
        <div class="text-center">
          <div class="text-xl font-bold text-gray-900 dark:text-white">{{ project.comments }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">{{ labels.comments }}</div>
        </div>
        <div class="text-center">
          <div class="text-xl font-bold text-gray-900 dark:text-white">{{ project.views }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">{{ labels.views }}</div>
        </div>
      </div>

      <div class="flex items-center justify-between gap-2">
        <button @click="$emit('view', project.id)" class="btn btn-outline btn-sm">{{ labels.view }}</button>
        <VoteButtons :project-id="project.id" :initial-upvotes="project.votes" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import VoteButtons from '~/components/molecules/VoteButtons.vue'

defineProps<{ project: any; canEdit: boolean; labels: Record<string, string> }>()
defineEmits<{ (e: 'view', id: number): void }>()
</script>
