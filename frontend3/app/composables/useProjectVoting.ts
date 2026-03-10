import { ref, computed } from 'vue'
import type { Project } from '../types/project-types'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

/**
 * Composable für Projekt-Voting-Logik
 * Bietet Funktionen zum Verwalten von Upvotes/Downvotes für Projekte
 * Verwendet echte API-Aufrufe statt Mock-Daten
 */
export function useProjectVoting() {
  // Stores
  const authStore = useAuthStore()
  const uiStore = useUIStore()

  // State
  const votingInProgress = ref<Set<string>>(new Set())
  const voteErrors = ref<Record<string, string>>({})
  
  // Computed Properties
  const isLoading = computed(() => votingInProgress.value.size > 0)
  
  const hasError = computed(() => Object.keys(voteErrors.value).length > 0)
  
  // Methods
  const voteProject = async (
    projectId: string,
    voteValue: 1 | -1 | null,
    options: {
      optimisticUpdate?: boolean
      onSuccess?: (project: Project) => void
      onError?: (error: Error) => void
    } = {}
  ) => {
    const {
      optimisticUpdate = true,
      onSuccess,
      onError
    } = options
    
    // Prevent duplicate voting
    if (votingInProgress.value.has(projectId)) {
      return
    }
    
    try {
      votingInProgress.value.add(projectId)
      delete voteErrors.value[projectId]
      
      const voteType = voteValue === 1 ? 'upvote' : voteValue === -1 ? 'downvote' : 'remove'
      
      const response = await authStore.fetchWithAuth(`/api/v1/projects/${projectId}/vote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ vote_type: voteType })
      })
      
      if (!response.ok) {
        throw new Error(`Failed to vote on project: ${response.statusText}`)
      }
      
      const result = await response.json()
      
      if (onSuccess) {
        // onSuccess(result)
      }
      
      uiStore.showNotification({
        title: 'Erfolg',
        type: 'success',
        message: voteValue === 1 ? 'Projekt positiv bewertet' : 
                voteValue === -1 ? 'Projekt negativ bewertet' : 
                'Bewertung entfernt'
      })
      
      return result
      
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error'
      voteErrors.value[projectId] = errorMessage
      
      if (onError) {
        onError(error instanceof Error ? error : new Error(errorMessage))
      }
      
      uiStore.showNotification({
        title: 'Fehler',
        type: 'error',
        message: 'Bewertung konnte nicht gespeichert werden'
      })
      
      // Revert optimistic update if it was applied
      if (optimisticUpdate) {
        // Revert logic would go here
      }
      
      throw error
      
    } finally {
      votingInProgress.value.delete(projectId)
    }
  }
  
  const upvoteProject = async (
    projectId: string,
    options?: {
      optimisticUpdate?: boolean
      onSuccess?: (project: Project) => void
      onError?: (error: Error) => void
    }
  ) => {
    return voteProject(projectId, 1, options)
  }
  
  const downvoteProject = async (
    projectId: string,
    options?: {
      optimisticUpdate?: boolean
      onSuccess?: (project: Project) => void
      onError?: (error: Error) => void
    }
  ) => {
    return voteProject(projectId, -1, options)
  }
  
  const removeVote = async (
    projectId: string,
    options?: {
      optimisticUpdate?: boolean
      onSuccess?: (project: Project) => void
      onError?: (error: Error) => void
    }
  ) => {
    return voteProject(projectId, null, options)
  }
  
  const toggleVote = async (
    projectId: string,
    currentVote: 1 | -1 | null,
    options?: {
      optimisticUpdate?: boolean
      onSuccess?: (project: Project) => void
      onError?: (error: Error) => void
    }
  ) => {
    if (currentVote === 1) {
      // Wenn bereits upgevotet, entferne Vote
      return removeVote(projectId, options)
    } else if (currentVote === -1) {
      // Wenn bereits downgevotet, wechsle zu upvote
      return upvoteProject(projectId, options)
    } else {
      // Wenn kein Vote, upvote
      return upvoteProject(projectId, options)
    }
  }
  
  const getVoteStatus = (projectId: string): {
    isVoting: boolean
    error?: string
  } => {
    return {
      isVoting: votingInProgress.value.has(projectId),
      error: voteErrors.value[projectId]
    }
  }
  
  const clearVoteError = (projectId: string) => {
    delete voteErrors.value[projectId]
  }
  
  const clearAllErrors = () => {
    voteErrors.value = {}
  }
  
  const calculateVoteImpact = (
    currentVotes: number,
    newVote: 1 | -1 | null,
    previousVote: 1 | -1 | null
  ): number => {
    // Berechnet die Änderung der Vote-Anzahl basierend auf vorherigem und neuem Vote
    
    if (previousVote === newVote) {
      return 0 // Keine Änderung
    }
    
    if (previousVote === 1 && newVote === null) {
      return -1 // Upvote entfernt
    }
    
    if (previousVote === -1 && newVote === null) {
      return 1 // Downvote entfernt (erhöht Vote-Zahl)
    }
    
    if (previousVote === null && newVote === 1) {
      return 1 // Neuer Upvote
    }
    
    if (previousVote === null && newVote === -1) {
      return -1 // Neuer Downvote
    }
    
    if (previousVote === 1 && newVote === -1) {
      return -2 // Upvote zu Downvote (Netto -2)
    }
    
    if (previousVote === -1 && newVote === 1) {
      return 2 // Downvote zu Upvote (Netto +2)
    }
    
    return 0
  }
  
  const getVoteAnalytics = (projects: Project[]) => {
    const analytics = {
      totalUpvotes: 0,
      totalDownvotes: 0,
      totalVotes: 0,
      upvoteRatio: 0,
      mostUpvoted: null as Project | null,
      mostControversial: null as Project | null,
      userVotes: {
        upvoted: 0,
        downvoted: 0,
        neutral: 0
      }
    }
    
    if (projects.length === 0) {
      return analytics
    }
    
    let maxUpvotes = -1
    let maxControversy = -1
    
    projects.forEach(project => {
      // Zähle Votes basierend auf Vote-Zahl (vereinfacht)
      // In einer echten Implementierung würden wir separate Upvote/Downvote-Zahlen haben
      const upvotes = Math.max(0, project.stats.votes)
      const downvotes = Math.max(0, -project.stats.votes)
      
      analytics.totalUpvotes += upvotes
      analytics.totalDownvotes += downvotes
      analytics.totalVotes += Math.abs(project.stats.votes)
      
      // Benutzer-Votes
      if (project.userVote === 1) {
        analytics.userVotes.upvoted++
      } else if (project.userVote === -1) {
        analytics.userVotes.downvoted++
      } else {
        analytics.userVotes.neutral++
      }
      
      // Finde das meist upgevotete Projekt
      if (upvotes > maxUpvotes) {
        maxUpvotes = upvotes
        analytics.mostUpvoted = project
      }
      
      // Finde das kontroverseste Projekt (ähnlich viele Up- und Downvotes)
      const controversyScore = Math.min(upvotes, downvotes)
      if (controversyScore > maxControversy) {
        maxControversy = controversyScore
        analytics.mostControversial = project
      }
    })
    
    // Berechne Upvote-Ratio
    if (analytics.totalVotes > 0) {
      analytics.upvoteRatio = analytics.totalUpvotes / analytics.totalVotes
    }
    
    return analytics
  }
  
  const validateVote = (
    project: Project,
    userId?: string
  ): { valid: boolean; reason?: string } => {
    // Validierungslogik für Votes
    
    // Prüfe ob Benutzer eingeloggt ist
    if (!userId) {
      return {
        valid: false,
        reason: 'You must be logged in to vote'
      }
    }
    
    // Prüfe ob Projekt votbar ist
    if (project.status === 'archived' || project.status === 'draft') {
      return {
        valid: false,
        reason: 'This project is not currently accepting votes'
      }
    }
    
    // Prüfe ob Benutzer bereits gevotet hat (wenn wir das wissen)
    if (project.userVote !== undefined && project.userVote !== null) {
      // Benutzer hat bereits gevotet, aber das ist okay (kann Vote ändern)
    }
    
    return { valid: true }
  }
  
  const getVoteHistory = async (
    userId: string,
    options: {
      limit?: number
      offset?: number
      projectId?: string
      voteType?: 'upvote' | 'downvote'
    } = {}
  ) => {
    try {
      // Build query parameters
      const queryParams = new URLSearchParams()
      if (options.limit) queryParams.append('limit', options.limit.toString())
      if (options.offset) queryParams.append('offset', options.offset.toString())
      if (options.projectId) queryParams.append('project_id', options.projectId)
      if (options.voteType) queryParams.append('vote_type', options.voteType)
      
      const queryString = queryParams.toString()
      const url = `/api/v1/users/${userId}/votes${queryString ? `?${queryString}` : ''}`
      
      const response = await authStore.fetchWithAuth(url)
      
      if (!response.ok) {
        throw new Error(`Failed to fetch vote history: ${response.statusText}`)
      }
      
      const data = await response.json()
      return {
        votes: data.votes || [],
        total: data.total || 0,
        hasMore: data.hasMore || false
      }
      
    } catch (error) {
      console.error('Error fetching vote history:', error)
      throw error
    }
  }
  
  const exportVotes = (projects: Project[]): string => {
    const voteData = projects.map(project => ({
      projectId: project.id,
      projectTitle: project.title,
      userVote: project.userVote,
      voteCount: project.stats.votes,
      votedAt: new Date().toISOString()
    }))
    
    return JSON.stringify(voteData, null, 2)
  }
  
  const batchVote = async (
    votes: Array<{
      projectId: string
      voteValue: 1 | -1 | null
    }>,
    options?: {
      onProgress?: (completed: number, total: number) => void
      onComplete?: (results: Array<{ success: boolean; projectId: string; error?: string }>) => void
    }
  ) => {
    const results: Array<{ success: boolean; projectId: string; error?: string }> = []
    const total = votes.length
    
    for (let i = 0; i < votes.length; i++) {
      const vote = votes[i]
      if (!vote) continue
      
      const { projectId, voteValue } = vote
      
      try {
        await voteProject(projectId, voteValue, { optimisticUpdate: false })
        results.push({ success: true, projectId })
      } catch (error) {
        results.push({
          success: false,
          projectId,
          error: error instanceof Error ? error.message : 'Unknown error'
        })
      }
      
      if (options?.onProgress) {
        options.onProgress(i + 1, total)
      }
    }
    
    if (options?.onComplete) {
      options.onComplete(results)
    }
    
    return results
  }
  
  return {
    // State
    votingInProgress,
    voteErrors,
    
    // Computed
    isLoading,
    hasError,
    
    // Methods
    voteProject,
    upvoteProject,
    downvoteProject,
    removeVote,
    toggleVote,
    getVoteStatus,
    clearVoteError,
    clearAllErrors,
    calculateVoteImpact,
    getVoteAnalytics,
    validateVote,
    getVoteHistory,
    exportVotes,
    batchVote,
  }
}

export type UseProjectVotingReturn = ReturnType<typeof useProjectVoting>