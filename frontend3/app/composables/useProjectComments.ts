import { ref, computed } from 'vue'
import type { ProjectComment, User } from '~/types/project-types'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

/**
 * Composable für Projekt-Kommentar-Logik mit echter API-Integration
 * Bietet Funktionen zum Verwalten von Kommentaren für Projekte
 */
export function useProjectComments() {
  // Stores
  const authStore = useAuthStore()
  const uiStore = useUIStore()

  // State
  const comments = ref<ProjectComment[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const postingComment = ref(false)
  const editingCommentId = ref<string | null>(null)
  const replyingToCommentId = ref<string | null>(null)
  
  // Filter State
  const sortBy = ref<'newest' | 'oldest' | 'most_voted'>('newest')
  const showReplies = ref(true)
  const filterByUser = ref<string | null>(null)
  
  // Computed Properties
  const sortedComments = computed(() => {
    const commentsToSort = [...comments.value]
    
    switch (sortBy.value) {
      case 'newest':
        return commentsToSort.sort((a, b) =>
          new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
        )
      
      case 'oldest':
        return commentsToSort.sort((a, b) =>
          new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
        )
      
      case 'most_voted':
        return commentsToSort.sort((a, b) => b.votes - a.votes)
      
      default:
        return commentsToSort
    }
  })
  
  const filteredComments = computed(() => {
    let result = sortedComments.value
    
    // Filter by user
    if (filterByUser.value) {
      result = result.filter(comment => comment.user.id === filterByUser.value)
    }
    
    // Filter replies if showReplies is false
    if (!showReplies.value) {
      result = result.filter(comment => !comment.parentId)
    }
    
    return result
  })
  
  const topLevelComments = computed(() => {
    return filteredComments.value.filter(comment => !comment.parentId)
  })
  
  const commentCount = computed(() => {
    return comments.value.length
  })
  
  const replyCount = computed(() => {
    return comments.value.filter(comment => comment.parentId).length
  })
  
  const totalVotes = computed(() => {
    return comments.value.reduce((sum, comment) => sum + comment.votes, 0)
  })
  
  const isLoading = computed(() => loading.value || postingComment.value)
  
  const hasComments = computed(() => comments.value.length > 0)

  // Helper function to transform API response to ProjectComment type
  const transformApiComment = (apiComment: any): ProjectComment => {
    // Calculate total votes from upvote_count and downvote_count
    const votes = (apiComment.upvote_count || 0) - (apiComment.downvote_count || 0)
    
    // Transform user data
    const user: User = {
      id: apiComment.user_id?.toString() || apiComment.user?.id?.toString() || '',
      username: apiComment.user_name || apiComment.user?.username || 'Unknown',
      avatarUrl: apiComment.user?.avatar_url || undefined,
      email: apiComment.user?.email || undefined,
      role: apiComment.user?.role || undefined,
      bio: apiComment.user?.bio || undefined,
      createdAt: apiComment.user?.created_at || undefined
    }

    // Transform replies recursively
    const replies = apiComment.replies?.map(transformApiComment) || []

    return {
      id: apiComment.id?.toString() || '',
      userId: apiComment.user_id?.toString() || '',
      user,
      content: apiComment.content || '',
      parentId: apiComment.parent_id?.toString() || undefined,
      votes,
      userVote: null, // Will be populated separately if user has voted
      createdAt: apiComment.created_at || new Date().toISOString(),
      updatedAt: apiComment.updated_at || new Date().toISOString(),
      replies
    }
  }

  // Helper function to find a comment by ID (recursive)
  const findCommentById = (commentId: string, commentList: ProjectComment[] = comments.value): ProjectComment | null => {
    for (let i = 0; i < commentList.length; i++) {
      const comment = commentList[i]!
      if (comment.id === commentId) {
        return comment
      }
      
      if (comment.replies && comment.replies.length > 0) {
        const foundInReplies = findCommentById(commentId, comment.replies)
        if (foundInReplies) {
          return foundInReplies
        }
      }
    }
    
    return null
  }

  // Helper function to remove a comment by ID (recursive)
  const removeCommentById = (commentId: string, commentList: ProjectComment[] = comments.value): boolean => {
    for (let i = 0; i < commentList.length; i++) {
      const comment = commentList[i]!
      
      if (comment.id === commentId) {
        commentList.splice(i, 1)
        return true
      }
      
      if (comment.replies && comment.replies.length > 0) {
        if (removeCommentById(commentId, comment.replies)) {
          return true
        }
      }
    }
    
    return false
  }

  // Helper function to build comment tree with depth
  const buildCommentTree = (): Array<ProjectComment & { depth: number }> => {
    const tree: Array<ProjectComment & { depth: number }> = []
    
    const build = (commentList: ProjectComment[], depth: number = 0) => {
      commentList.forEach(comment => {
        tree.push({ ...comment, depth })
        
        if (comment.replies && comment.replies.length > 0) {
          build(comment.replies, depth + 1)
        }
      })
    }
    
    build(topLevelComments.value)
    return tree
  }

  // Methods
  const loadComments = async (projectId: string, options: {
    forceRefresh?: boolean
    includeReplies?: boolean
  } = {}) => {
    if (loading.value && !options.forceRefresh) return
    
    try {
      loading.value = true
      error.value = null
      
      const response = await authStore.fetchWithAuth(`/api/projects/${projectId}/comments`)
      if (!response.ok) {
        throw new Error(`Failed to load comments: ${response.status}`)
      }
      
      const data = await response.json()
      const apiComments = data.comments || []
      
      // Transform API comments to frontend format
      comments.value = apiComments.map(transformApiComment)
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load comments'
      console.error('Error loading comments:', err)
      uiStore.showError('Fehler beim Laden der Kommentare')
    } finally {
      loading.value = false
    }
  }
  
  const postComment = async (
    projectId: string,
    content: string,
    options: {
      parentId?: string
      onSuccess?: (comment: ProjectComment) => void
      onError?: (error: Error) => void
    } = {}
  ) => {
    const { parentId, onSuccess, onError } = options
    
    if (postingComment.value) return
    
    try {
      postingComment.value = true
      error.value = null
      
      const payload: any = { content }
      if (parentId) {
        payload.parent_id = parseInt(parentId, 10)
      }
      
      const response = await authStore.fetchWithAuth(`/api/projects/${projectId}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      
      if (!response.ok) {
        throw new Error(`Failed to post comment: ${response.status}`)
      }
      
      const apiComment = await response.json()
      const newComment = transformApiComment(apiComment)
      
      // Add to comments list
      if (parentId) {
        // Find parent comment and add reply
        const parentComment = findCommentById(parentId)
        if (parentComment) {
          if (!parentComment.replies) {
            parentComment.replies = []
          }
          parentComment.replies.push(newComment)
        }
      } else {
        comments.value.push(newComment)
      }
      
      if (onSuccess) {
        onSuccess(newComment)
      }
      
      // Reset reply state
      if (replyingToCommentId.value === parentId) {
        replyingToCommentId.value = null
      }
      
      uiStore.showSuccess('Kommentar erfolgreich gepostet')
      return newComment
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to post comment'
      error.value = errorMessage
      
      if (onError) {
        onError(err instanceof Error ? err : new Error(errorMessage))
      }
      
      uiStore.showError('Fehler beim Posten des Kommentars')
      throw err
      
    } finally {
      postingComment.value = false
    }
  }
  
  const editComment = async (
    commentId: string,
    content: string,
    options: {
      onSuccess?: (comment: ProjectComment) => void
      onError?: (error: Error) => void
    } = {}
  ) => {
    const { onSuccess, onError } = options
    
    try {
      editingCommentId.value = commentId
      error.value = null
      
      const response = await authStore.fetchWithAuth(`/api/comments/${commentId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content })
      })
      
      if (!response.ok) {
        throw new Error(`Failed to edit comment: ${response.status}`)
      }
      
      const apiComment = await response.json()
      const updatedComment = transformApiComment(apiComment)
      
      // Update local comment
      const comment = findCommentById(commentId)
      if (comment) {
        comment.content = updatedComment.content
        comment.updatedAt = updatedComment.updatedAt
        
        if (onSuccess) {
          onSuccess(comment)
        }
      }
      
      uiStore.showSuccess('Kommentar erfolgreich aktualisiert')
      return comment
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to edit comment'
      error.value = errorMessage
      
      if (onError) {
        onError(err instanceof Error ? err : new Error(errorMessage))
      }
      
      uiStore.showError('Fehler beim Aktualisieren des Kommentars')
      throw err
      
    } finally {
      editingCommentId.value = null
    }
  }
  
  const deleteComment = async (
    commentId: string,
    options: {
      onSuccess?: () => void
      onError?: (error: Error) => void
    } = {}
  ) => {
    const { onSuccess, onError } = options
    
    try {
      const response = await authStore.fetchWithAuth(`/api/comments/${commentId}`, {
        method: 'DELETE'
      })
      
      if (!response.ok) {
        throw new Error(`Failed to delete comment: ${response.status}`)
      }
      
      // Remove from local comments
      removeCommentById(commentId)
      
      if (onSuccess) {
        onSuccess()
      }
      
      uiStore.showSuccess('Kommentar erfolgreich gelöscht')
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete comment'
      error.value = errorMessage
      
      if (onError) {
        onError(err instanceof Error ? err : new Error(errorMessage))
      }
      
      uiStore.showError('Fehler beim Löschen des Kommentars')
      throw err
    }
  }
  
  const voteComment = async (
    commentId: string,
    voteValue: 1 | -1 | null,
    options: {
      optimisticUpdate?: boolean
      onSuccess?: (comment: ProjectComment) => void
      onError?: (error: Error) => void
    } = {}
  ) => {
    const { optimisticUpdate = true, onSuccess, onError } = options
    
    try {
      // Determine vote type for API
      let voteType: string | null = null
      if (voteValue === 1) voteType = 'upvote'
      else if (voteValue === -1) voteType = 'downvote'
      
      // If voteValue is null, we need to remove vote
      // The API handles removal when sending same vote type again
      const comment = findCommentById(commentId)
      if (!comment) throw new Error('Comment not found')
      
      // For null vote, we need to know current vote to send opposite
      if (voteValue === null) {
        // Send current vote type to remove it
        voteType = comment.userVote === 1 ? 'upvote' : 'downvote'
      }
      
      if (!voteType) {
        throw new Error('Invalid vote value')
      }
      
      const response = await authStore.fetchWithAuth(`/api/comments/${commentId}/vote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vote_type: voteType })
      })
      
      if (!response.ok) {
        throw new Error(`Failed to vote on comment: ${response.status}`)
      }
      
      // Update local comment based on response
      const data = await response.json()
      
      // Parse response to determine new vote state
      const message = data.message || ''
      let newVoteValue: 1 | -1 | null = null
      
      if (message.includes('Added upvote')) newVoteValue = 1
      else if (message.includes('Added downvote')) newVoteValue = -1
      else if (message.includes('Removed')) newVoteValue = null
      else if (message.includes('Changed vote to upvote')) newVoteValue = 1
      else if (message.includes('Changed vote to downvote')) newVoteValue = -1
      
      // Update vote count locally
      if (comment) {
        const previousVote = comment.userVote
        
        // Update vote count (simplified - in reality we should get updated counts from API)
        if (previousVote === 1 && newVoteValue !== 1) {
          comment.votes = Math.max(0, comment.votes - 1)
        } else if (previousVote === -1 && newVoteValue !== -1) {
          comment.votes = Math.max(0, comment.votes + 1)
        } else if (previousVote !== 1 && newVoteValue === 1) {
          comment.votes += 1
        } else if (previousVote !== -1 && newVoteValue === -1) {
          comment.votes = Math.max(0, comment.votes - 1)
        }
        
        comment.userVote = newVoteValue
        
        if (onSuccess) {
          onSuccess(comment)
        }
      }
      
      return comment
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to vote on comment'
      
      if (onError) {
        onError(err instanceof Error ? err : new Error(errorMessage))
      }
      
      uiStore.showError('Fehler beim Abstimmen')
      throw err
    }
  }
  
  const setSortBy = (sortOption: 'newest' | 'oldest' | 'most_voted') => {
    sortBy.value = sortOption
  }
  
  const toggleShowReplies = () => {
    showReplies.value = !showReplies.value
  }
  
  const setFilterByUser = (userId: string | null) => {
    filterByUser.value = userId
  }
  
  const startReply = (commentId: string) => {
    replyingToCommentId.value = commentId
  }
  
  const cancelReply = () => {
    replyingToCommentId.value = null
  }
  
  const startEdit = (commentId: string) => {
    editingCommentId.value = commentId
  }
  
  const cancelEdit = () => {
    editingCommentId.value = null
  }
  
  const clearError = () => {
    error.value = null
  }
  
  const clearComments = () => {
    comments.value = []
  }
  
  const getCommentById = (commentId: string): ProjectComment | null => {
    return findCommentById(commentId)
  }
  
  const getReplies = (commentId: string): ProjectComment[] => {
    const comment = findCommentById(commentId)
    return comment?.replies || []
  }
  
  const getCommentThread = (commentId: string): ProjectComment[] => {
    const thread: ProjectComment[] = []
    let currentComment = findCommentById(commentId)
    
    // Go up the parent chain
    while (currentComment) {
      thread.unshift(currentComment)
      
      if (currentComment.parentId) {
        currentComment = findCommentById(currentComment.parentId)
      } else {
        break
      }
    }
    
    return thread
  }
  
  const getCommentStats = () => {
    const stats = {
      totalComments: commentCount.value,
      totalReplies: replyCount.value,
      totalVotes: totalVotes.value,
      averageVotesPerComment: 0,
      mostVotedComment: null as ProjectComment | null,
      mostRepliedComment: null as ProjectComment | null,
      userDistribution: {} as Record<string, number>
    }
    
    if (comments.value.length === 0) {
      return stats
    }
    
    let maxVotes = -1
    let maxReplies = -1
    
    comments.value.forEach(comment => {
      // Track user distribution
      const userId = comment.user.id
      stats.userDistribution[userId] = (stats.userDistribution[userId] || 0) + 1
      
      // Track most voted comment
      if (comment.votes > maxVotes) {
        maxVotes = comment.votes
        stats.mostVotedComment = comment
      }
      
      // Track most replied comment
      const replyCount = comment.replies?.length || 0
      if (replyCount > maxReplies) {
        maxReplies = replyCount
        stats.mostRepliedComment = comment
      }
    })
    
    // Calculate average votes per comment
    stats.averageVotesPerComment = stats.totalComments > 0 
      ? stats.totalVotes / stats.totalComments 
      : 0
    
    return stats
  }

  // Return all public methods and state
  return {
    // State
    comments,
    loading,
    error,
    postingComment,
    editingCommentId,
    replyingToCommentId,
    sortBy,
    showReplies,
    filterByUser,
    
    // Computed Properties
    sortedComments,
    filteredComments,
    topLevelComments,
    commentCount,
    replyCount,
    totalVotes,
    isLoading,
    hasComments,
    
    // Methods
    loadComments,
    postComment,
    editComment,
    deleteComment,
    voteComment,
    setSortBy,
    toggleShowReplies,
    setFilterByUser,
    startReply,
    cancelReply,
    startEdit,
    cancelEdit,
    clearError,
    clearComments,
    getCommentById,
    getReplies,
    getCommentThread,
    getCommentStats,
    buildCommentTree,
    findCommentById,
    removeCommentById
  }
}
