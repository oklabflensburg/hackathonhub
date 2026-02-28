import { computed, ref, unref } from 'vue'
import type { MaybeRef } from 'vue'
import type { Ref } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

interface CommentUser {
  name: string
  avatar_url: string | null
}

export interface ProjectComment {
  id: number
  content: string
  created_at: string
  user_name?: string
  user_id?: number
  upvote_count?: number
  downvote_count?: number
  replies?: ProjectComment[]
  user?: CommentUser
}

export const useComments = (projectId: MaybeRef<number>, projectCommentCount?: Ref<number>) => {
  const authStore = useAuthStore()
  const uiStore = useUIStore()

  const comments = ref<ProjectComment[]>([])
  const loading = ref(false)
  const submitting = ref(false)
  const error = ref<string | null>(null)

  const resolvedProjectId = computed(() => Number(unref(projectId)))
  const getBackendUrl = () => useRuntimeConfig().public.apiUrl || 'http://localhost:8000'

  const fetchComments = async () => {
    try {
      loading.value = true
      error.value = null

      const response = await authStore.fetchWithAuth(`${getBackendUrl()}/api/projects/${resolvedProjectId.value}/comments`)

      if (!response.ok) {
        error.value = `Failed to load comments (${response.status})`
        return
      }

      const data = await response.json()
      comments.value = (data.comments || []).map((comment: ProjectComment) => ({
        ...comment,
        user: {
          name: comment.user_name || 'Anonymous',
          avatar_url: null,
        },
      }))
    } catch (fetchError) {
      console.error('Failed to fetch comments:', fetchError)
      error.value = 'Failed to load comments'
      uiStore.showError('Failed to load comments', 'Unable to load comments. Please try again later.')
    } finally {
      loading.value = false
    }
  }

  const postComment = async (content: string, parentCommentId?: number) => {
    if (!authStore.isAuthenticated) {
      uiStore.showError('Authentication required', 'Please log in to post a comment.')
      return false
    }

    if (!content.trim() || submitting.value) {
      return false
    }

    try {
      submitting.value = true
      const response = await authStore.fetchWithAuth(`${getBackendUrl()}/api/projects/${resolvedProjectId.value}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: content.trim(),
          ...(parentCommentId ? { parent_comment_id: parentCommentId } : {}),
        }),
      })

      if (!response.ok) {
        uiStore.showError('Failed to submit comment', `Unable to submit your comment. Please try again. (Error: ${response.status})`)
        return false
      }

      if (projectCommentCount) {
        projectCommentCount.value += 1
      }

      await fetchComments()
      return true
    } catch (postError) {
      console.error('Failed to post comment:', postError)
      uiStore.showError('Failed to submit comment', 'An unexpected error occurred while submitting your comment. Please try again.')
      return false
    } finally {
      submitting.value = false
    }
  }

  const updateComment = async (commentId: number, content: string) => {
    if (!authStore.isAuthenticated) {
      uiStore.showError('Authentication required', 'Please log in to edit a comment.')
      return false
    }

    const response = await authStore.fetchWithAuth(`${getBackendUrl()}/api/comments/${commentId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: content.trim() }),
    })

    if (!response.ok) {
      uiStore.showError('Failed to update comment', `Unable to update your comment. Please try again. (Error: ${response.status})`)
      return false
    }

    await fetchComments()
    return true
  }

  const deleteComment = async (commentId: number) => {
    if (!authStore.isAuthenticated) {
      uiStore.showError('Authentication required', 'Please log in to delete a comment.')
      return false
    }

    const response = await authStore.fetchWithAuth(`${getBackendUrl()}/api/comments/${commentId}`, {
      method: 'DELETE',
    })

    if (!response.ok) {
      uiStore.showError('Failed to delete comment', `Unable to delete your comment. Please try again. (Error: ${response.status})`)
      return false
    }

    if (projectCommentCount) {
      projectCommentCount.value = Math.max(0, projectCommentCount.value - 1)
    }

    await fetchComments()
    return true
  }

  const voteComment = async (commentId: number, voteType: 'upvote' | 'downvote') => {
    if (!authStore.isAuthenticated) {
      uiStore.showError('Authentication required', 'Please log in to vote on a comment.')
      return false
    }

    const response = await authStore.fetchWithAuth(`${getBackendUrl()}/api/comments/${commentId}/vote`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ vote_type: voteType }),
    })

    if (!response.ok) {
      uiStore.showError('Failed to vote on comment', `Unable to vote on the comment. Please try again. (Error: ${response.status})`)
      return false
    }

    await fetchComments()
    return true
  }

  return {
    comments,
    loading,
    submitting,
    error,
    fetchComments,
    postComment,
    updateComment,
    deleteComment,
    voteComment,
  }
}
