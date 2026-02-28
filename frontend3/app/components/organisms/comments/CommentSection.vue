<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ title }}</h2>
      <span class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-sm">
        {{ commentCount }} {{ commentsCountLabel }}
      </span>
    </div>

    <div v-if="isAuthenticated" class="mb-8">
      <CommentForm
        v-model="newComment"
        :loading="submitting"
        :placeholder="addCommentPlaceholder"
        :submit-label="postCommentLabel"
        @submit="handleSubmitComment"
      />
    </div>
    <div v-else class="mb-8 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg text-center">
      <p class="text-gray-600 dark:text-gray-400">{{ signInToCommentLabel }}</p>
    </div>

    <div v-if="loading" class="text-center py-8">
      <LoadingSpinner />
      <p class="mt-2 text-gray-600 dark:text-gray-400">{{ loadingCommentsLabel }}</p>
    </div>

    <div v-else-if="error" class="text-center py-8">
      <p class="text-red-600 dark:text-red-400 mb-3">{{ errorCommentsLabel }}</p>
      <button
        type="button"
        class="px-4 py-2 rounded-lg bg-primary-600 text-white hover:bg-primary-700"
        @click="emit('retry')"
      >
        {{ retryLabel }}
      </button>
    </div>

    <div v-else-if="comments.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
      {{ emptyCommentsLabel }}
    </div>

    <div v-else class="space-y-6">
      <div v-for="comment in comments" :key="comment.id" class="border-b border-gray-200 dark:border-gray-700 pb-6 last:border-0">
        <div v-if="editingCommentId !== comment.id">
          <CommentItem
            :comment="comment"
            :current-user-id="currentUserId"
            :is-authenticated="isAuthenticated"
            :format-date="formatDate"
            @edit="startEdit"
            @delete="confirmDelete"
            @reply="startReply"
            @vote="handleVote"
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

        <div v-if="replyingToCommentId === comment.id" class="mt-4 ml-6">
          <CommentForm
            v-model="replyContent"
            :loading="submitting"
            :show-cancel="true"
            :placeholder="replyPlaceholder"
            :submit-label="postReplyLabel"
            @cancel="cancelReply"
            @submit="() => handleSubmitReply(comment.id)"
          />
        </div>

        <ReplyThread
          :replies="comment.replies || []"
          :current-user-id="currentUserId"
          :is-authenticated="isAuthenticated"
          :format-date="formatDate"
          @edit="startEdit"
          @delete="confirmDelete"
          @reply="startReply"
          @vote="handleVote"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import LoadingSpinner from '~/components/atoms/LoadingSpinner.vue'
import CommentForm from './CommentForm.vue'
import CommentItem from './CommentItem.vue'
import ReplyThread from './ReplyThread.vue'
import type { ProjectComment } from '~/composables/useComments'

interface Props {
  title?: string
  comments: ProjectComment[]
  loading?: boolean
  submitting?: boolean
  error?: string | null
  commentCount?: number
  currentUserId?: number
  isAuthenticated?: boolean
  formatDate: (value: string) => string
  addCommentPlaceholder?: string
  postCommentLabel?: string
  postReplyLabel?: string
  replyPlaceholder?: string
  signInToCommentLabel?: string
  emptyCommentsLabel?: string
  loadingCommentsLabel?: string
  errorCommentsLabel?: string
  retryLabel?: string
  saveLabel?: string
  commentsCountLabel?: string
  deleteConfirmLabel?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Comments',
  loading: false,
  submitting: false,
  error: null,
  commentCount: 0,
  currentUserId: undefined,
  isAuthenticated: false,
  addCommentPlaceholder: 'Add a comment...',
  postCommentLabel: 'Post comment',
  postReplyLabel: 'Post reply',
  replyPlaceholder: 'Write a reply...',
  signInToCommentLabel: 'Please sign in to comment.',
  emptyCommentsLabel: 'No comments yet.',
  loadingCommentsLabel: 'Loading comments...',
  errorCommentsLabel: 'Failed to load comments.',
  retryLabel: 'Retry',
  saveLabel: 'Save',
  commentsCountLabel: 'comments',
  deleteConfirmLabel: 'Are you sure you want to delete this comment?',
})

const emit = defineEmits<{
  add: [content: string]
  update: [id: number, content: string]
  remove: [id: number]
  vote: [id: number, voteType: 'upvote' | 'downvote']
  reply: [parentId: number, content: string]
  retry: []
}>()

const newComment = ref('')
const editingCommentId = ref<number | null>(null)
const editingContent = ref('')
const replyingToCommentId = ref<number | null>(null)
const replyContent = ref('')

const handleSubmitComment = () => {
  if (!newComment.value.trim()) return
  emit('add', newComment.value)
  newComment.value = ''
}

const startEdit = (comment: ProjectComment) => {
  editingCommentId.value = comment.id
  editingContent.value = comment.content
}

const handleSaveEdit = () => {
  if (!editingCommentId.value || !editingContent.value.trim()) return
  emit('update', editingCommentId.value, editingContent.value)
  cancelEdit()
}

const cancelEdit = () => {
  editingCommentId.value = null
  editingContent.value = ''
}

const startReply = (commentId: number) => {
  replyingToCommentId.value = commentId
  replyContent.value = ''
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

const confirmDelete = (commentId: number) => {
  emit('remove', commentId)
}

const handleVote = (commentId: number, voteType: 'upvote' | 'downvote') => {
  emit('vote', commentId, voteType)
}
</script>
