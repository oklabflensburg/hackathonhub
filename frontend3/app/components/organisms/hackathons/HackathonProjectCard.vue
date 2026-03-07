<template>
  <div class="card-hover group">
    <div class="relative h-48 mb-4 rounded-xl overflow-hidden">
      <img :src="project.image" :alt="project.name" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
      <div class="absolute top-4 right-4">
        <Badge :variant="statusBadgeVariant" size="sm">
          {{ project.status }}
        </Badge>
      </div>
    </div>

    <div class="space-y-4">
      <div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">{{ project.name }}</h3>
        <p class="text-gray-600 dark:text-gray-400 text-sm">{{ project.description }}</p>
      </div>

      <ProjectCardStats
        :votes="project.votes"
        :votes-label="labels.votes"
        :comments="project.comments"
        :comments-label="labels.comments"
        :views="project.views"
        :views-label="labels.views"
      />

      <div class="flex items-center justify-between gap-2">
        <button @click="$emit('view', project.id)" class="btn btn-outline btn-sm">{{ labels.view }}</button>
        <VoteButtons :project-id="project.id" :initial-upvotes="project.votes" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Badge from '~/components/atoms/Badge.vue'
import ProjectCardStats from '~/components/molecules/ProjectCardStats.vue'
import VoteButtons from '~/components/molecules/VoteButtons.vue'

const props = defineProps<{ project: any; canEdit: boolean; labels: Record<string, string> }>()
defineEmits<{ (e: 'view', id: number): void }>()

const statusBadgeVariant = computed(() => {
  if (props.project.status === 'Winner') return 'success'
  if (props.project.status === 'Finalist') return 'warning'
  return 'primary'
})
</script>