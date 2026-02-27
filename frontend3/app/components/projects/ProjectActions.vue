<template>
  <Card>
    <template #header>
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ title }}</h2>
    </template>

    <div class="space-y-3">
      <NuxtLink
        v-if="canEdit"
        :to="`/projects/${project.id}/edit`"
        class="w-full flex items-center justify-center px-4 py-3 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/30 transition-colors"
      >
        {{ editLabel }}
      </NuxtLink>

      <button
        v-if="canEdit"
        @click="$emit('delete')"
        class="w-full flex items-center justify-center px-4 py-3 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors"
      >
        {{ deleteLabel }}
      </button>

      <NuxtLink
        v-if="project.hackathon_id"
        :to="`/hackathons/${project.hackathon_id}`"
        class="w-full flex items-center justify-center px-4 py-3 bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-400 rounded-lg hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-colors"
      >
        {{ viewHackathonLabel }}
      </NuxtLink>

      <NuxtLink
        v-if="project.team_id"
        :to="`/teams/${project.team_id}`"
        class="w-full flex items-center justify-center px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        {{ viewTeamLabel }}
      </NuxtLink>

      <NuxtLink
        to="/projects"
        class="w-full flex items-center justify-center px-4 py-3 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
      >
        {{ backLabel }}
      </NuxtLink>
    </div>
  </Card>
</template>

<script setup lang="ts">
defineProps<{
  project: any
  canEdit: boolean
  title: string
  editLabel: string
  deleteLabel: string
  viewHackathonLabel: string
  viewTeamLabel: string
  backLabel: string
}>()

defineEmits<{ (e: 'delete'): void }>()
</script>
