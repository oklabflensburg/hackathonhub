<template>
  <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-5 border border-gray-200 dark:border-gray-600">
    <div class="flex items-start justify-between mb-2">
      <h3 class="font-semibold text-gray-900 dark:text-white">{{ team.name }}</h3>
      <Badge
        :variant="team.is_open ? 'success' : 'gray'"
        size="sm"
      >
        {{ team.is_open ? openLabel : closedLabel }}
      </Badge>
    </div>
    
    <p class="text-gray-600 dark:text-gray-400 text-sm mb-3 line-clamp-2">
      {{ team.description || noDescriptionLabel }}
    </p>
    
    <div class="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
      <span>{{ team.member_count || 0 }} / {{ team.max_members }} {{ membersLabel }}</span>
      <span class="text-xs">{{ createdPrefix }} {{ formatDate(team.created_at) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import Badge from '~/components/atoms/Badge.vue'

interface Team {
  id: number | string
  name: string
  description?: string
  is_open: boolean
  member_count: number
  max_members: number
  created_at: string
}

interface Props {
  team: Team
  openLabel: string
  closedLabel: string
  noDescriptionLabel: string
  membersLabel: string
  createdPrefix: string
  formatDate: (dateString: string) => string
}

defineProps<Props>()
</script>