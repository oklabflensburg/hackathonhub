import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'

export interface Vote {
  id: number
  user_id: number
  project_id: number
  vote_type: string
  created_at: string
}

export interface ProjectVoteStats {
  project_id: number
  upvotes: number
  downvotes: number
  total_score: number
  user_vote?: string | null
}

export const useVotingStore = defineStore('voting', () => {
  const authStore = useAuthStore()
  const config = useRuntimeConfig()
  const votes = ref<Map<number, Vote>>(new Map()) // project_id -> Vote
  const projectStats = ref<Map<number, ProjectVoteStats>>(new Map())
  const isLoading = ref<Map<number, boolean>>(new Map())
  const error = ref<string | null>(null)

  const userVotes = computed(() => {
    const userVotesMap = new Map<number, string>()
    votes.value.forEach((vote, projectId) => {
      if (vote.user_id === authStore.user?.id) {
        userVotesMap.set(projectId, vote.vote_type)
      }
    })
    return userVotesMap
  })

  async function voteForProject(projectId: number, voteType: 'up' | 'down') {
    if (!authStore.isAuthenticated) {
      throw new Error('You must be logged in to vote')
    }

    isLoading.value.set(projectId, true)
    error.value = null

    try {
      // Use fetchWithAuth for auto-refresh token handling
      const response = await authStore.fetchWithAuth(`/api/projects/${projectId}/vote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ vote_type: voteType })
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || 'Failed to vote')
      }

      const data = await response.json()
      
      // Update local state - create new Map for reactivity
      if (data.vote) {
        const newVotes = new Map(votes.value)
        newVotes.set(projectId, data.vote)
        votes.value = newVotes
      }
      
      // Update project stats - create new Map for reactivity
      if (data.project_stats) {
        const newStats = new Map(projectStats.value)
        newStats.set(projectId, data.project_stats)
        projectStats.value = newStats
      }

      return data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Voting failed'
      throw err
    } finally {
      isLoading.value.set(projectId, false)
    }
  }

  async function removeVote(projectId: number) {
    if (!authStore.isAuthenticated) {
      throw new Error('You must be logged in to remove vote')
    }

    isLoading.value.set(projectId, true)
    error.value = null

    try {
      // Use fetchWithAuth for auto-refresh token handling
      const response = await authStore.fetchWithAuth(`/api/projects/${projectId}/vote`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || 'Failed to remove vote')
      }

      const data = await response.json()
      
      // Remove vote from local state - create new Map for reactivity
      const newVotes = new Map(votes.value)
      newVotes.delete(projectId)
      votes.value = newVotes
      
      // Update project stats - create new Map for reactivity
      if (data.project_stats) {
        const newStats = new Map(projectStats.value)
        newStats.set(projectId, data.project_stats)
        projectStats.value = newStats
      }

      return data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to remove vote'
      throw err
    } finally {
      isLoading.value.set(projectId, false)
    }
  }

  async function getProjectVoteStats(projectId: number) {
    try {
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'
      const response = await fetch(`${backendUrl}/api/projects/${projectId}/vote-stats`)
      
      if (response.ok) {
        const stats = await response.json()
        // Create new Map for reactivity
        const newStats = new Map(projectStats.value)
        newStats.set(projectId, stats)
        projectStats.value = newStats
        return stats
      } else if (response.status === 404) {
        // Project doesn't exist or endpoint not found, return default stats
        const defaultStats = {
          project_id: projectId,
          upvotes: 0,
          downvotes: 0,
          total_score: 0,
          user_vote: null
        }
        const newStats = new Map(projectStats.value)
        newStats.set(projectId, defaultStats)
        projectStats.value = newStats
        return defaultStats
      }
    } catch (err) {
      console.error('Failed to fetch vote stats:', err)
      // Return default stats on any error
      const defaultStats = {
        project_id: projectId,
        upvotes: 0,
        downvotes: 0,
        total_score: 0,
        user_vote: null
      }
      const newStats = new Map(projectStats.value)
      newStats.set(projectId, defaultStats)
      projectStats.value = newStats
      return defaultStats
    }
  }

  async function getUserVotes() {
    if (!authStore.isAuthenticated) return

    try {
      // Use fetchWithAuth for auto-refresh token handling
      const response = await authStore.fetchWithAuth('/api/users/me/votes')

      if (response.ok) {
        const userVotes = await response.json()
        // Update local votes map - create new Map for reactivity
        const newVotes = new Map(votes.value)
        userVotes.forEach((vote: Vote) => {
          newVotes.set(vote.project_id, vote)
        })
        votes.value = newVotes
        return userVotes
      }
    } catch (err) {
      console.error('Failed to fetch user votes:', err)
    }
  }

  function getProjectStats(projectId: number): ProjectVoteStats | undefined {
    return projectStats.value.get(projectId)
  }

  function getUserVoteForProject(projectId: number): string | null {
    const vote = votes.value.get(projectId)
    if (!vote || vote.user_id !== authStore.user?.id) return null
    // Map backend vote_type ('upvote'/'downvote') to frontend ('up'/'down')
    if (vote.vote_type === 'upvote') return 'up'
    if (vote.vote_type === 'downvote') return 'down'
    return vote.vote_type
  }

  function isVotingInProgress(projectId: number): boolean {
    return isLoading.value.get(projectId) || false
  }

  return {
    votes,
    projectStats,
    isLoading,
    error,
    userVotes,
    voteForProject,
    removeVote,
    getProjectVoteStats,
    getUserVotes,
    getProjectStats,
    getUserVoteForProject,
    isVotingInProgress
  }
})