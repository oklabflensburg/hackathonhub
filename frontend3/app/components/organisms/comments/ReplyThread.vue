<template>
  <div v-if="replies.length" class="mt-4 ml-6 space-y-4 border-l-2 border-gray-200 dark:border-gray-700 pl-4">
    <div v-for="reply in replies" :key="reply.id" class="pt-4 first:pt-0">
      <CommentItem
        :comment="reply"
        :current-user-id="currentUserId"
        :is-authenticated="isAuthenticated"
        :format-date="formatDate"
        @edit="emit('edit', $event)"
        @delete="emit('delete', $event)"
        @reply="emit('reply', $event)"
        @vote="onVote"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import CommentItem from './CommentItem.vue'
import type { ProjectComment } from '~/composables/useComments'

interface Props {
  replies: ProjectComment[]
  currentUserId?: number
  isAuthenticated?: boolean
  formatDate: (value: string) => string
}

withDefaults(defineProps<Props>(), {
  currentUserId: undefined,
  isAuthenticated: false,
})

const emit = defineEmits<{
  edit: [comment: ProjectComment]
  delete: [id: number]
  reply: [id: number]
  vote: [id: number, voteType: 'upvote' | 'downvote']
}>()

const onVote = (id: number, voteType: 'upvote' | 'downvote') => emit('vote', id, voteType)
</script>
