<template>
  <div v-if="replies.length" class="mt-4 ml-6 space-y-4 border-l-2 border-gray-200 dark:border-gray-700 pl-4">
    <div v-for="reply in replies" :key="reply.id" class="pt-4 first:pt-0">
      <div v-if="editingCommentId !== reply.id">
        <CommentItem
          :comment="reply"
          :current-user-id="currentUserId"
          :is-authenticated="isAuthenticated"
          :format-date="formatDate"
          @edit="startEdit"
          @delete="emit('remove', $event)"
          @reply="startReply"
          @vote="onVote"
        />
      </div>

      <div v-else>
        <CommentForm
          v-model="editingContent"
          :loading="submitting"
          :show-cancel="true"
          :submit-label="saveLabel"
          @cancel="cancelEdit"
          @submit="handleSaveEdit"
        />
      </div>

      <div v-if="replyingToCommentId === reply.id" class="mt-4">
        <CommentForm
          v-model="replyContent"
          :loading="submitting"
          :show-cancel="true"
          :placeholder="replyPlaceholder"
          :submit-label="postReplyLabel"
          @cancel="cancelReply"
          @submit="() => handleSubmitReply(reply.id)"
        />
      </div>

      <ReplyThread
        :replies="reply.replies || []"
        :current-user-id="currentUserId"
        :is-authenticated="isAuthenticated"
        :format-date="formatDate"
        :submitting="submitting"
        :save-label="saveLabel"
        :post-reply-label="postReplyLabel"
        :reply-placeholder="replyPlaceholder"
        @update="forwardUpdate"
        @remove="emit('remove', $event)"
        @reply="forwardReply"
        @vote="onVote"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CommentItem from './CommentItem.vue'
import CommentForm from './CommentForm.vue'
import type { ProjectComment } from '~/composables/useComments'

interface Props {
  replies: ProjectComment[]
  currentUserId?: number
  isAuthenticated?: boolean
  formatDate: (value: string) => string
  submitting?: boolean
  saveLabel?: string
  postReplyLabel?: string
  replyPlaceholder?: string
}

withDefaults(defineProps<Props>(), {
  currentUserId: undefined,
  isAuthenticated: false,
  submitting: false,
  saveLabel: 'Save',
  postReplyLabel: 'Post reply',
  replyPlaceholder: 'Write a reply...',
})

const emit = defineEmits<{
  update: [id: number, content: string]
  remove: [id: number]
  reply: [parentId: number, content: string]
  vote: [id: number, voteType: 'upvote' | 'downvote']
}>()

const onVote = (id: number, voteType: 'upvote' | 'downvote') => emit('vote', id, voteType)

const editingCommentId = ref<number | null>(null)
const editingContent = ref('')
const replyingToCommentId = ref<number | null>(null)
const replyContent = ref('')

const startEdit = (comment: ProjectComment) => {
  editingCommentId.value = comment.id
  editingContent.value = comment.content
  replyingToCommentId.value = null
}

const cancelEdit = () => {
  editingCommentId.value = null
  editingContent.value = ''
}

const handleSaveEdit = () => {
  if (!editingCommentId.value || !editingContent.value.trim()) return
  emit('update', editingCommentId.value, editingContent.value)
  cancelEdit()
}

const startReply = (commentId: number) => {
  replyingToCommentId.value = commentId
  replyContent.value = ''
  editingCommentId.value = null
}

const cancelReply = () => {
  replyingToCommentId.value = null
  replyContent.value = ''
}

const handleSubmitReply = (commentId: number) => {
  if (!replyContent.value.trim()) return
  emit('reply', commentId, replyContent.value)
  cancelReply()
}

const forwardUpdate = (id: number, content: string) => {
  emit('update', id, content)
}

const forwardReply = (parentId: number, content: string) => {
  emit('reply', parentId, content)
}
</script>
