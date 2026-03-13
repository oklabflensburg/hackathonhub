/**
 * Comments Composable
 * Bietet eine konsistente Schnittstelle für alle Kommentar-Operationen
 * Kapselt API-Aufrufe und bietet reaktiven State, Loading-States und Error-Handling
 */

import { ref, computed } from 'vue'
import { useApiClient } from '~/utils/api-client'
import { useUIStore } from '~/stores/ui'

export interface Comment {
  id: number
  content: string
  user_id: number
  project_id: number
  parent_id?: number
  upvote_count: number
  downvote_count: number
  vote_score: number
  created_at: string
  updated_at?: string
  user?: any
  project?: any
  replies?: Comment[]
}

export type ProjectComment = Comment

export interface CommentCreateData {
  content: string
  parent_id?: number
}

export interface CommentUpdateData {
  content: string
}

export interface CommentVoteData {
  vote_type: 'upvote' | 'downvote'
}

export interface CommentVoteStats {
  upvotes: number
  downvotes: number
  total_score: number
  user_vote?: 'upvote' | 'downvote'
}

export interface UseCommentsOptions {
  /** Automatisches Error-Handling (Notifications) */
  autoErrorHandling?: boolean
  /** Automatisches Success-Handling (Notifications) */
  autoSuccessHandling?: boolean
  /** Projekt-ID für Projekt-Kommentare */
  projectId?: number
  /** Kommentar-ID für Single-Comment-Operationen */
  commentId?: number
}

/**
 * Comments Composable
 */
export function useComments(options: UseCommentsOptions = {}) {
  const {
    autoErrorHandling = true,
    autoSuccessHandling = true,
    projectId,
    commentId
  } = options

  // Stores und Services
  const uiStore = useUIStore()
  const apiClient = useApiClient()

  // State
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const comments = ref<Comment[]>([])
  const currentComment = ref<Comment | null>(null)
  const commentVoteStats = ref<Record<number, CommentVoteStats>>({})

  // Computed Properties
  const hasComments = computed(() => comments.value.length > 0)
  const countComments = (items: Comment[]): number => items.reduce(
    (total, item) => total + 1 + countComments(item.replies || []),
    0
  )
  const commentCount = computed(() => countComments(comments.value))
  const topLevelComments = computed(() => comments.value.filter(c => !c.parent_id))
  const nestedComments = computed(() => {
    const nested: Record<number, Comment[]> = {}
    comments.value.forEach(comment => {
      if (comment.parent_id) {
        const parentId = comment.parent_id
        if (!nested[parentId]) {
          nested[parentId] = []
        }
        nested[parentId].push(comment)
      }
    })
    return nested
  })

  /**
   * Kommentare für ein Projekt abrufen
   */
  async function fetchProjectComments(projectId: number): Promise<Comment[]> {
    try {
      isLoading.value = true
      error.value = null

      const response = await apiClient.get<any>(`/api/projects/${projectId}/comments`)
      const normalized = Array.isArray(response) ? response : (response?.comments || [])
      comments.value = normalized
      return normalized
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Abrufen der Kommentare'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Kommentare Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Einzelnen Kommentar abrufen
   */
  async function fetchComment(commentId: number): Promise<Comment> {
    try {
      isLoading.value = true
      error.value = null

      // Da es keinen direkten GET-Endpunkt für einzelne Kommentare gibt,
      // müssen wir die Kommentare des Projekts laden und filtern
      // Oder wir verwenden einen anderen Ansatz
      // Für jetzt geben wir einen Fehler zurück
      throw new Error('GET-Endpunkt für einzelne Kommentare nicht verfügbar')
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Abrufen des Kommentars'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Kommentar Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Kommentar für ein Projekt erstellen
   */
  async function createProjectComment(projectId: number, commentData: CommentCreateData): Promise<Comment> {
    try {
      isLoading.value = true
      error.value = null

      const response = await apiClient.post<Comment>(`/api/projects/${projectId}/comments`, commentData, {
        skipErrorNotification: true
      })

      if (response.parent_id) {
        comments.value = insertReplyIntoTree(comments.value, response.parent_id, response)
      } else {
        comments.value = [response, ...comments.value]
      }

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Kommentar erfolgreich erstellt', 'Kommentar')
      }

      return response
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Erstellen des Kommentars'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Kommentar Erstellung Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Kommentar aktualisieren
   */
  async function updateComment(commentId: number, commentData: CommentUpdateData): Promise<Comment> {
    try {
      isLoading.value = true
      error.value = null

      const response = await apiClient.put<Comment>(`/api/comments/${commentId}`, commentData, {
        skipErrorNotification: true
      })

      // Lokalen State aktualisieren
      comments.value = updateCommentInTree(comments.value, commentId, response)

      if (currentComment.value?.id === commentId) {
        currentComment.value = response
      }

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Kommentar erfolgreich aktualisiert', 'Kommentar')
      }

      return response
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Aktualisieren des Kommentars'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Kommentar Update Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Kommentar löschen
   */
  async function deleteComment(commentId: number): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      await apiClient.delete(`/api/comments/${commentId}`, {
        skipErrorNotification: true
      })

      // Aus lokalem State entfernen
      comments.value = removeCommentFromTree(comments.value, commentId)

      if (currentComment.value?.id === commentId) {
        currentComment.value = null
      }

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Kommentar erfolgreich gelöscht', 'Kommentar')
      }
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Löschen des Kommentars'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Kommentar Löschung Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Für Kommentar voten
   */
  async function voteForComment(commentId: number, voteType: 'upvote' | 'downvote'): Promise<void> {
    try {
      error.value = null

      await apiClient.post(`/api/comments/${commentId}/vote`, {
        vote_type: voteType
      }, {
        skipErrorNotification: true
      })

      // Vote-Stats aktualisieren
      await fetchCommentVoteStats(commentId)

      // Success Notification
      if (autoSuccessHandling) {
        const message = voteType === 'upvote' ? 'Upvote erfolgreich' : 'Downvote erfolgreich'
        uiStore.showSuccess(message, 'Kommentar Vote')
      }
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Voten für Kommentar'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Kommentar Vote Fehler')
      }
      
      throw err
    }
  }

  /**
   * Vote für Kommentar entfernen
   */
  async function removeCommentVote(commentId: number): Promise<void> {
    try {
      error.value = null

      await apiClient.delete(`/api/comments/${commentId}/vote`, {
        skipErrorNotification: true
      })

      // Vote-Stats aktualisieren
      await fetchCommentVoteStats(commentId)

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Vote erfolgreich entfernt', 'Kommentar Vote')
      }
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Entfernen des Votes'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Kommentar Vote Entfernung Fehler')
      }
      
      throw err
    }
  }

  /**
   * Kommentar-Vote-Statistiken abrufen
   */
  async function fetchCommentVoteStats(commentId: number): Promise<CommentVoteStats> {
    try {
      // Da es keinen direkten Endpunkt für Kommentar-Vote-Statistiken gibt,
      // müssen wir den Kommentar abrufen und die Statistiken extrahieren
      // Für jetzt geben wir leere Statistiken zurück
      const stats: CommentVoteStats = {
        upvotes: 0,
        downvotes: 0,
        total_score: 0
      }
      
      commentVoteStats.value[commentId] = stats
      return stats
    } catch (err: any) {
      console.error('Fehler beim Abrufen der Kommentar-Vote-Statistiken:', err)
      throw err
    }
  }

  /**
   * Antwort auf Kommentar erstellen
   */
  async function createReply(parentCommentId: number, content: string): Promise<Comment> {
    try {
      isLoading.value = true
      error.value = null

      // Zuerst müssen wir die Projekt-ID des Eltern-Kommentars finden
      const parentComment = findCommentById(comments.value, parentCommentId)
      if (!parentComment) {
        throw new Error('Eltern-Kommentar nicht gefunden')
      }

      const commentData: CommentCreateData = {
        content,
        parent_id: parentCommentId
      }

      const response = await apiClient.post<Comment>(`/api/projects/${parentComment.project_id}/comments`, commentData, {
        skipErrorNotification: true
      })

      comments.value = insertReplyIntoTree(comments.value, parentCommentId, response)

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Antwort erfolgreich erstellt', 'Kommentar')
      }

      return response
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Erstellen der Antwort'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Antwort Erstellung Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Kommentare nach Vote-Score sortieren
   */
  function sortCommentsByScore(commentsList: Comment[]): Comment[] {
    return [...commentsList].sort((a, b) => b.vote_score - a.vote_score)
  }

  /**
   * Kommentare nach Datum sortieren (neueste zuerst)
   */
  function sortCommentsByDate(commentsList: Comment[]): Comment[] {
    return [...commentsList].sort((a, b) => {
      const dateA = new Date(a.created_at).getTime()
      const dateB = new Date(b.created_at).getTime()
      return dateB - dateA
    })
  }

  /**
   * Kommentare nach Projekt filtern
   */
  function filterCommentsByProject(projectId: number): Comment[] {
    return comments.value.filter(c => c.project_id === projectId)
  }

  /**
   * Kommentare nach Benutzer filtern
   */
  function filterCommentsByUser(userId: number): Comment[] {
    return comments.value.filter(c => c.user_id === userId)
  }

  /**
   * Antworten auf einen Kommentar abrufen
   */
  function getReplies(commentId: number): Comment[] {
    return findCommentById(comments.value, commentId)?.replies || []
  }

  /**
   * Kommentar-Baum erstellen (für verschachtelte Darstellung)
   */
  function buildCommentTree(): Comment[] {
    return comments.value
  }

  function findCommentById(items: Comment[], commentId: number): Comment | null {
    for (const item of items) {
      if (item.id === commentId) return item
      const nested = findCommentById(item.replies || [], commentId)
      if (nested) return nested
    }
    return null
  }

  function insertReplyIntoTree(items: Comment[], parentId: number, reply: Comment): Comment[] {
    return items.map(item => {
      if (item.id === parentId) {
        return {
          ...item,
          replies: [...(item.replies || []), reply]
        }
      }

      if (item.replies?.length) {
        return {
          ...item,
          replies: insertReplyIntoTree(item.replies, parentId, reply)
        }
      }

      return item
    })
  }

  function updateCommentInTree(items: Comment[], commentId: number, updated: Comment): Comment[] {
    return items.map(item => {
      if (item.id === commentId) {
        return {
          ...item,
          ...updated,
          replies: updated.replies || item.replies || []
        }
      }

      if (item.replies?.length) {
        return {
          ...item,
          replies: updateCommentInTree(item.replies, commentId, updated)
        }
      }

      return item
    })
  }

  function removeCommentFromTree(items: Comment[], commentId: number): Comment[] {
    return items
      .filter(item => item.id !== commentId)
      .map(item => ({
        ...item,
        replies: removeCommentFromTree(item.replies || [], commentId)
      }))
  }

  /**
   * Error zurücksetzen
   */
  function clearError(): void {
    error.value = null
  }

  /**
   * Loading-State zurücksetzen
   */
  function clearLoading(): void {
    isLoading.value = false
  }

  /**
   * Composable zurücksetzen
   */
  function reset(): void {
    isLoading.value = false
    error.value = null
    comments.value = []
    currentComment.value = null
    commentVoteStats.value = {}
  }

  // Alias for fetchProjectComments for backward compatibility
  const fetchComments = (id?: number) => {
    const targetId = id ?? options.projectId
    if (!targetId) {
      throw new Error('Project ID is required to fetch comments')
    }
    return fetchProjectComments(targetId)
  }
  // Aliases for component compatibility
  const loading = computed(() => isLoading.value)
  const submitting = computed(() => isLoading.value)
  const postComment = (content: string, parentId?: number) => {
    if (!options.projectId) {
      throw new Error('Project ID is required to post a comment')
    }
    return createProjectComment(options.projectId, { content, parent_id: parentId })
  }
  const voteComment = voteForComment
  // Alias for updateComment with string parameter
  const updateCommentWithString = (commentId: number, content: string) => {
    return updateComment(commentId, { content })
  }
  
  return {
    // State
    isLoading: computed(() => isLoading.value),
    loading,
    submitting,
    error: computed(() => error.value),
    comments: computed(() => comments.value),
    currentComment: computed(() => currentComment.value),
    commentVoteStats: computed(() => commentVoteStats.value),
    
    // Computed
    hasComments,
    commentCount,
    topLevelComments,
    nestedComments,
    
    // Methods
    fetchProjectComments,
    fetchComments,
    fetchComment,
    createProjectComment,
    postComment,
    updateComment: updateCommentWithString,
    deleteComment,
    voteForComment,
    voteComment,
    removeCommentVote,
    fetchCommentVoteStats,
    createReply,
    sortCommentsByScore,
    sortCommentsByDate,
    filterCommentsByProject,
    filterCommentsByUser,
    getReplies,
    buildCommentTree,
    
    // Utilities
    clearError,
    clearLoading,
    reset
  }
}
