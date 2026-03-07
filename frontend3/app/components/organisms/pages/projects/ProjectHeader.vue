<template>
  <div class="mb-8">
    <div class="flex items-center justify-between mb-4 gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ project.title }}</h1>
        <div class="flex items-center space-x-4 mt-2">
          <div class="flex items-center space-x-2">
            <NuxtLink v-if="project.owner" :to="`/users/${project.owner.id}`" class="flex items-center space-x-2 hover:opacity-90 transition-opacity">
              <Avatar :src="project.owner?.avatar_url" :fallback-text="project.owner?.username || 'U'" size="sm" :alt="project.owner?.username || 'Unknown'" />
              <span class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400">{{ project.owner?.username || 'Unknown' }}</span>
            </NuxtLink>
            <div v-else class="flex items-center space-x-2">
              <Avatar fallback-text="U" size="sm" alt="Unknown user" />
              <span class="text-gray-600 dark:text-gray-400">Unknown</span>
            </div>
          </div>
          <span class="text-gray-500 dark:text-gray-500">•</span>
          <span class="text-gray-600 dark:text-gray-400">{{ formatDate(project.created_at) }}</span>
        </div>
      </div>
      <div v-if="showVoting">
        <VoteButtons :project-id="project.id" />
      </div>
    </div>

    <div class="flex items-center space-x-4">
      <Tag :text="project.status || 'active'" :color="statusColor" />
      <NuxtLink
        v-if="project.hackathon"
        :to="`/hackathons/${project.hackathon.id}`"
        class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300 hover:bg-purple-200 dark:hover:bg-purple-800 transition-colors"
      >
        {{ project.hackathon.name }}
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Avatar from '~/components/atoms/Avatar.vue'
import Tag from '~/components/atoms/Tag.vue'
import VoteButtons from '~/components/molecules/VoteButtons.vue'

interface Props {
  project: any
  showVoting?: boolean
  formatDate: (date: string) => string
}

const props = withDefaults(defineProps<Props>(), {
  showVoting: false,
})

const statusColor = computed(() => {
  if (props.project.status === 'active') return 'success'
  if (props.project.status === 'completed') return 'primary'
  if (props.project.status === 'archived') return 'neutral'
  return 'neutral'
})
</script>
