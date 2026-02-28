<template>
  <div class="flex items-start space-x-4">
    <NuxtLink to="/profile">
      <Avatar :src="comment.user?.avatar_url" :fallback-text="comment.user?.name || 'U'" size="md" />
    </NuxtLink>

    <div class="flex-1">
      <div class="flex items-center justify-between mb-2">
        <div>
          <NuxtLink to="/profile" class="font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400">
            {{ comment.user?.name || 'Anonymous' }}
          </NuxtLink>
          <span class="text-sm text-gray-500 dark:text-gray-400 ml-3">{{ formatDate(comment.created_at) }}</span>
        </div>

        <div v-if="currentUserId === comment.user_id" class="flex items-center space-x-2">
          <button class="text-sm text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400" @click="$emit('edit', comment)">Edit</button>
          <button class="text-sm text-red-500 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300" @click="$emit('delete', comment.id)">Delete</button>
        </div>
      </div>

      <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line">{{ comment.content }}</p>

      <div class="flex items-center space-x-4 mt-3">
        <button class="flex items-center space-x-1 text-sm text-gray-500 dark:text-gray-400 hover:text-green-600 dark:hover:text-green-400" @click="$emit('vote', comment.id, 'upvote')">
          <span>↑</span>
          <span>{{ comment.upvote_count || 0 }}</span>
        </button>
        <button class="flex items-center space-x-1 text-sm text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400" @click="$emit('vote', comment.id, 'downvote')">
          <span>↓</span>
          <span>{{ comment.downvote_count || 0 }}</span>
        </button>
        <button v-if="isAuthenticated" class="text-sm text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400" @click="$emit('reply', comment.id)">
          Reply
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Avatar from '~/components/atoms/Avatar.vue'
import type { ProjectComment } from '~/composables/useComments'

interface Props {
  comment: ProjectComment
  currentUserId?: number
  isAuthenticated?: boolean
  formatDate: (value: string) => string
}

withDefaults(defineProps<Props>(), {
  currentUserId: undefined,
  isAuthenticated: false,
})

defineEmits<{
  edit: [comment: ProjectComment]
  delete: [id: number]
  reply: [id: number]
  vote: [id: number, voteType: 'upvote' | 'downvote']
}>()
</script>
