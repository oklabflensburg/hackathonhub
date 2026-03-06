import { ref, computed, watch } from 'vue'
import type { ProjectComment } from '../types/project-types'

/**
 * Composable für Projekt-Kommentar-Logik
 * Bietet Funktionen zum Verwalten von Kommentaren für Projekte
 */
export function useProjectComments() {
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
  
  // Methods
  const loadComments = async (projectId: string, options: {
    forceRefresh?: boolean
    includeReplies?: boolean
  } = {}) => {
    if (loading.value && !options.forceRefresh) return
    
    try {
      loading.value = true
      error.value = null
      
      // Hier würde normalerweise ein API-Call stehen
      // const response = await api.getProjectComments(projectId, options)
      
      // Simulierte Antwort für Entwicklung
      comments.value = []
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load comments'
      console.error('Error loading comments:', err)
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
      
      // Hier würde normalerweise ein API-Call stehen
      // const response = await api.postComment(projectId, content, parentId)
      
      // Simulierte Antwort für Entwicklung
      const newComment: ProjectComment = {
        id: `comment-${Date.now()}`,
        userId: 'current-user',
        user: {
          id: 'current-user',
          username: 'Current User',
          avatarUrl: undefined
        },
        content,
        parentId: parentId || undefined,
        votes: 0,
        userVote: null,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        replies: []
      }
      
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
      
      return newComment
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to post comment'
      error.value = errorMessage
      
      if (onError) {
        onError(err instanceof Error ? err : new Error(errorMessage))
      }
      
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
      
      // Hier würde normalerweise ein API-Call stehen
      // const response = await api.editComment(commentId, content)
      
      // Update local comment
      const comment = findCommentById(commentId)
      if (comment) {
        comment.content = content
        comment.updatedAt = new Date().toISOString()
        
        if (onSuccess) {
          onSuccess(comment)
        }
      }
      
      return comment
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to edit comment'
      error.value = errorMessage
      
      if (onError) {
        onError(err instanceof Error ? err : new Error(errorMessage))
      }
      
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
      // Hier würde normalerweise ein API-Call stehen
      // await api.deleteComment(commentId)
      
      // Remove from local comments
      removeCommentById(commentId)
      
      if (onSuccess) {
        onSuccess()
      }
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete comment'
      error.value = errorMessage
      
      if (onError) {
        onError(err instanceof Error ? err : new Error(errorMessage))
      }
      
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
      // Hier würde normalerweise ein API-Call stehen
      // const response = await api.voteComment(commentId, voteValue)
      
      // Update local comment
      const comment = findCommentById(commentId)
      if (comment) {
        const previousVote = comment.userVote
        
        // Update vote count
        if (previousVote === 1 && voteValue !== 1) {
          comment.votes = Math.max(0, comment.votes - 1)
        } else if (previousVote === -1 && voteValue !== -1) {
          comment.votes = Math.max(0, comment.votes + 1)
        } else if (previousVote !== 1 && voteValue === 1) {
          comment.votes += 1
        } else if (previousVote !== -1 && voteValue === -1) {
          comment.votes = Math.max(0, comment.votes - 1)
        }
        
        comment.userVote = voteValue
        
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
      
      // Find most voted comment
      if (comment.votes > maxVotes) {
        maxVotes = comment.votes
        stats.mostVotedComment = comment
      }
      
      // Find most replied comment
      const replyCount = comment.replies?.length || 0
      if (replyCount > maxReplies) {
        maxReplies = replyCount
        stats.mostRepliedComment = comment
      }
    })
    
    // Calculate average
    stats.averageVotesPerComment = totalVotes.value / commentCount.value
    
    return stats
  }
  
  const exportComments = (): string => {
    const exportData = {
      comments: comments.value,
      stats: getCommentStats(),
      exportDate: new Date().toISOString(),
      totalCount: commentCount.value
    }
    
    return JSON.stringify(exportData, null, 2)
  }
  
  const importComments = (commentsJson: string): boolean => {
    try {
      const importData = JSON.parse(commentsJson)
      
      if (importData.comments && Array.isArray(importData.comments)) {
        comments.value = importData.comments
        return true
      }
      
      return false
      
    } catch (error) {
      console.error('Failed to import comments:', error)
      return false
    }
  }
  
  const validateComment = (content: string): { valid: boolean; errors: string[] } => {
    const errors: string[] = []
    
    // Content validation
    if (!content.trim()) {
      errors.push('Comment cannot be empty')
    }
    
    if (content.length < 3) {
      errors.push('Comment must be at least 3 characters long')
    }
    
    if (content.length > 5000) {
      errors.push('Comment cannot exceed 5000 characters')
    }
    
    // Spam detection (simplified)
    const spamPatterns = [
      /http[s]?:\/\/[^\s]+/g, // URLs
      /[A-Z]{5,}/g, // Excessive caps
      /!{3,}/g, // Excessive exclamation marks
    ]
    
    spamPatterns.forEach(pattern => {
      if (pattern.test(content)) {
        errors.push('Comment contains suspicious content')
      }
    })
    
    return {
      valid: errors.length === 0,
      errors
    }
  }
  
  // Helper Functions
  const findCommentById = (commentId: string): ProjectComment | null => {
    // Recursive search through comments and replies
    const search = (commentList: ProjectComment[]): ProjectComment | null => {
      for (const comment of commentList) {
        if (comment.id === commentId) {
          return comment
        }
        
        if (comment.replies && comment.replies.length > 0) {
          const found = search(comment.replies)
          if (found) {
            return found
          }
        }
      }
      
      return null
    }
    
    return search(comments.value)
  }
  
  const removeCommentById = (commentId: string): boolean => {
    // Recursive removal
    const remove = (commentList: ProjectComment[]): boolean => {
      for (let i = 0; i < commentList.length; i++) {
        const comment = commentList[i]
        
        if (comment.id === commentId) {
          commentList.splice(i, 1)
          return true
        }
        
        if (comment.replies && comment.replies.length > 0) {
          if (remove(comment.replies)) {
            return true
          }
        }
      }
      
      return false
    }
    
    return remove(comments.value)
  }
  
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
  
  // Watch for changes to update computed properties
  watch(comments, () => {
    // Rebuild comment tree or update stats if needed
  }, { deep: true })
  
  return {
    // State
    comments: filteredComments,
    topLevelComments,
    loading,
    error,
    postingComment,
    editingCommentId,
    replyingToCommentId,
    sortBy,
    showReplies,
    filterByUser,
    
    // Computed
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
    exportComments,
    importComments,
    validateComment,
    findCommentById,
    removeCommentById,
    buildCommentTree,
  }
}

export type UseProjectCommentsReturn = ReturnType<typeof useProjectComments>