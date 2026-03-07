<template>
  <Card>
    <template #header>
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Project Stats</h3>
    </template>

    <div class="space-y-4">
      <!-- Main Stats -->
      <div class="grid grid-cols-2 gap-4">
        <div class="text-center p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
          <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">
            {{ stats.votes || 0 }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-300 mt-1">
            Votes
          </div>
          <div v-if="stats.voteChange" class="text-xs mt-1" :class="stats.voteChange > 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
            {{ stats.voteChange > 0 ? '+' : '' }}{{ stats.voteChange }} today
          </div>
        </div>
        
        <div class="text-center p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
          <div class="text-2xl font-bold text-green-600 dark:text-green-400">
            {{ stats.comments || 0 }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-300 mt-1">
            Comments
          </div>
        </div>
        
        <div class="text-center p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
          <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">
            {{ stats.views || 0 }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-300 mt-1">
            Views
          </div>
        </div>
        
        <div class="text-center p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
          <div class="text-2xl font-bold text-orange-600 dark:text-orange-400">
            {{ stats.shares || 0 }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-300 mt-1">
            Shares
          </div>
        </div>
      </div>

      <!-- Engagement Rate -->
      <div v-if="stats.engagementRate !== undefined" class="pt-3 border-t border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Engagement Rate</span>
          <span class="text-sm font-bold text-primary-600 dark:text-primary-400">
            {{ stats.engagementRate.toFixed(1) }}%
          </span>
        </div>
        <ProgressBar
          :value="stats.engagementRate"
          :max="100"
          size="sm"
          :show-label="false"
        />
      </div>

      <!-- Created Date -->
      <div class="pt-3 border-t border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-300">Created</span>
          <span class="text-sm font-medium text-gray-900 dark:text-white">
            {{ formatDate(stats.createdAt) }}
          </span>
        </div>
        <div v-if="stats.updatedAt" class="flex items-center justify-between mt-1">
          <span class="text-sm text-gray-600 dark:text-gray-300">Last Updated</span>
          <span class="text-sm font-medium text-gray-900 dark:text-white">
            {{ formatDate(stats.updatedAt) }}
          </span>
        </div>
      </div>

      <!-- Status Badge -->
      <div v-if="stats.status" class="pt-3 border-t border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-300">Status</span>
          <Badge :variant="getStatusVariant(stats.status)" size="sm">
            {{ stats.status }}
          </Badge>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { Card, Badge, ProgressBar } from '~/components/atoms'

interface ProjectStats {
  votes?: number
  voteChange?: number
  comments?: number
  views?: number
  shares?: number
  engagementRate?: number
  createdAt: string
  updatedAt?: string
  status?: 'draft' | 'published' | 'featured' | 'archived'
}

interface Props {
  stats: ProjectStats
}

const props = defineProps<Props>()

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric',
    year: 'numeric'
  })
}

const getStatusVariant = (status: string): 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info' | 'gray' => {
  const variantMap: Record<string, 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info' | 'gray'> = {
    draft: 'gray',
    published: 'success',
    featured: 'primary',
    archived: 'warning'
  }
  return variantMap[status] || 'gray'
}
</script>

<style scoped>
/* Add any custom styles if needed */
</style>