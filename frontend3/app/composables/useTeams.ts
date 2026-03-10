import { ref, computed, watch } from 'vue'
import { useFetch, useRuntimeConfig } from '#imports'
import {
  TeamSortOption,
  TeamFilterOption,
  TeamVisibility,
  TeamStatus,
  TeamRole,
  TeamInvitationStatus,
  type Team,
  type TeamMember,
  type TeamInvitation,
  type TeamStats,
  type TeamCreateData,
  type TeamUpdateData,
  type TeamInvitationCreateData,
  type TeamMemberRole
} from '~/types/team-types'

interface UseTeamsOptions {
  hackathonId?: string | null
  userId?: string | null
  initialSort?: TeamSortOption
  initialFilter?: TeamFilterOption
  pageSize?: number
  autoFetch?: boolean
}

export function useTeams(options: UseTeamsOptions = {}) {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiUrl || 'http://localhost:8000'
  
  // Default options
  const {
    hackathonId = null,
    userId = null,
    initialSort = TeamSortOption.CREATED_AT_DESC,
    initialFilter = TeamFilterOption.ALL,
    pageSize = 12,
    autoFetch = true
  } = options
  
  // Reactive state
  const teams = ref<Team[]>([])
  const teamMembers = ref<TeamMember[]>([])
  const teamInvitations = ref<TeamInvitation[]>([])
  const stats = ref<TeamStats | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  // Pagination
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalCount = ref(0)
  const hasNextPage = computed(() => currentPage.value < totalPages.value)
  const hasPreviousPage = computed(() => currentPage.value > 1)
  
  // Filters and sorting
  const sortOption = ref<TeamSortOption>(initialSort)
  const filterOption = ref<TeamFilterOption>(initialFilter)
  const searchQuery = ref('')
  
  // Computed properties
  const filteredTeams = computed(() => {
    let result = [...teams.value]
    
    // Apply search filter
    if (searchQuery.value.trim()) {
      const query = searchQuery.value.toLowerCase().trim()
      result = result.filter(team =>
        team.name.toLowerCase().includes(query) ||
        team.description?.toLowerCase().includes(query) ||
        team.tags?.some(tag => tag.toLowerCase().includes(query))
      )
    }
    
    // Apply filter option
    switch (filterOption.value) {
      case TeamFilterOption.PUBLIC:
        result = result.filter(team => team.visibility === TeamVisibility.PUBLIC)
        break
      case TeamFilterOption.PRIVATE:
        result = result.filter(team => team.visibility === TeamVisibility.PRIVATE)
        break
      case TeamFilterOption.ACTIVE:
        result = result.filter(team => team.status === TeamStatus.ACTIVE)
        break
      case TeamFilterOption.INACTIVE:
        result = result.filter(team => team.status === TeamStatus.INACTIVE)
        break
      case TeamFilterOption.HAS_OPEN_SLOTS:
        result = result.filter(team => {
          const memberCount = team.stats?.memberCount || 0
          const maxMembers = team.maxMembers || Infinity
          return memberCount < maxMembers
        })
        break
      case TeamFilterOption.NEEDS_MEMBERS:
        result = result.filter(team => {
          const memberCount = team.stats?.memberCount || 0
          const maxMembers = team.maxMembers || Infinity
          return memberCount < maxMembers && maxMembers - memberCount >= 3
        })
        break
      // TeamFilterOption.ALL - no additional filtering
    }
    
    // Apply sorting
    result.sort((a, b) => {
      switch (sortOption.value) {
        case TeamSortOption.NAME_ASC:
          return a.name.localeCompare(b.name)
        case TeamSortOption.NAME_DESC:
          return b.name.localeCompare(a.name)
        case TeamSortOption.CREATED_AT_DESC:
          return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
        case TeamSortOption.CREATED_AT_ASC:
          return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
        case TeamSortOption.MEMBER_COUNT_DESC:
          return (b.stats?.memberCount || 0) - (a.stats?.memberCount || 0)
        case TeamSortOption.MEMBER_COUNT_ASC:
          return (a.stats?.memberCount || 0) - (b.stats?.memberCount || 0)
        case TeamSortOption.PROJECT_COUNT_DESC:
          return (b.stats?.projectCount || 0) - (a.stats?.projectCount || 0)
        case TeamSortOption.PROJECT_COUNT_ASC:
          return (a.stats?.projectCount || 0) - (b.stats?.projectCount || 0)
        default:
          return 0
      }
    })
    
    return result
  })
  
  const teamMembersMap = computed(() => {
    const map: Record<string, TeamMember[]> = {}
    teamMembers.value.forEach(member => {
      if (!map[member.teamId]) {
        map[member.teamId] = []
      }
      map[member.teamId]!.push(member)
    })
    return map
  })
  
  const userTeams = computed(() => {
    if (!userId) return []
    return teams.value.filter(team => {
      const teamMember = teamMembers.value.find(m => m.teamId === team.id && m.userId === userId)
      return !!teamMember
    })
  })
  
  const joinedTeams = computed(() => {
    if (!userId) return []
    return teams.value.filter(team => {
      const teamMember = teamMembers.value.find(m => 
        m.teamId === team.id && 
        m.userId === userId && 
        m.role !== TeamRole.PENDING
      )
      return !!teamMember
    })
  })
  
  const pendingInvitations = computed(() => {
    if (!userId) return []
    return teamInvitations.value.filter(invitation =>
      invitation.invitedUserId === userId
    )
  })
  
  // Watch for changes that should trigger refetch
  watch([sortOption, filterOption, searchQuery], () => {
    if (autoFetch) {
      fetchTeams({ page: 1 })
    }
  })
  
  // API methods
  const fetchTeams = async (fetchOptions: { page?: number; force?: boolean } = {}) => {
    const { page = currentPage.value, force = false } = fetchOptions
    
    if (loading.value && !force) return
    
    loading.value = true
    error.value = null
    
    try {
      const queryParams = new URLSearchParams({
        page: page.toString(),
        page_size: pageSize.toString(),
        sort: sortOption.value,
        filter: filterOption.value
      })
      
      if (searchQuery.value.trim()) {
        queryParams.set('search', searchQuery.value.trim())
      }
      
      if (hackathonId) {
        queryParams.set('hackathon_id', hackathonId)
      }
      
      if (userId) {
        queryParams.set('user_id', userId)
      }
      
      const url = `${apiBase}/api/teams?${queryParams}`
      const { data, error: fetchError } = await useFetch(url)
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to fetch teams')
      }
      
      const response = data.value as any
      teams.value = response.items || response.teams || []
      totalCount.value = response.total || response.count || teams.value.length
      totalPages.value = response.pages || Math.ceil(totalCount.value / pageSize)
      currentPage.value = page
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
      console.error('Error fetching teams:', err)
    } finally {
      loading.value = false
    }
  }
  
  const fetchTeam = async (teamId: string): Promise<Team | null> => {
    loading.value = true
    error.value = null
    
    try {
      const url = `${apiBase}/api/teams/${teamId}`
      const { data, error: fetchError } = await useFetch(url)
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to fetch team')
      }
      
      const team = data.value as Team
      
      // Update teams list if team exists
      const index = teams.value.findIndex(t => t.id === teamId)
      if (index !== -1) {
        teams.value[index] = team
      } else {
        teams.value.push(team)
      }
      
      return team
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
      console.error('Error fetching team:', err)
      return null
    } finally {
      loading.value = false
    }
  }
  
  const fetchTeamMembers = async (teamId: string): Promise<TeamMember[]> => {
    try {
      const url = `${apiBase}/api/teams/${teamId}/members`
      const { data, error: fetchError } = await useFetch(url)
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to fetch team members')
      }
      
      const members = (data.value as TeamMember[]).map(member => ({
        ...member,
        teamId
      }))
      
      // Update team members list
      teamMembers.value = [
        ...teamMembers.value.filter(m => m.teamId !== teamId),
        ...members
      ]
      
      return members
    } catch (err) {
      console.error('Error fetching team members:', err)
      return []
    }
  }
  
  const fetchTeamInvitations = async (teamId: string): Promise<TeamInvitation[]> => {
    try {
      const url = `${apiBase}/api/teams/${teamId}/invitations`
      const { data, error: fetchError } = await useFetch(url)
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to fetch team invitations')
      }
      
      const invitations = (data.value as TeamInvitation[]).map(invitation => ({
        ...invitation,
        teamId
      }))
      
      // Update team invitations list
      teamInvitations.value = [
        ...teamInvitations.value.filter(i => i.teamId !== teamId),
        ...invitations
      ]
      
      return invitations
    } catch (err) {
      console.error('Error fetching team invitations:', err)
      return []
    }
  }
  
  const fetchTeamStats = async (): Promise<TeamStats | null> => {
    try {
      const queryParams = new URLSearchParams()
      if (hackathonId) {
        queryParams.set('hackathon_id', hackathonId)
      }
      
      const url = `${apiBase}/api/teams/stats${queryParams.toString() ? `?${queryParams}` : ''}`
      const { data, error: fetchError } = await useFetch(url)
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to fetch team stats')
      }
      
      stats.value = data.value as TeamStats
      return stats.value
    } catch (err) {
      console.error('Error fetching team stats:', err)
      return null
    }
  }
  
  const createTeam = async (data: TeamCreateData): Promise<Team | null> => {
    loading.value = true
    error.value = null
    
    try {
      const url = `${apiBase}/api/teams`
      const { data: response, error: fetchError } = await useFetch(url, {
        method: 'POST',
        body: data
      })
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to create team')
      }
      
      const team = response.value as Team
      teams.value.unshift(team)
      totalCount.value += 1
      
      return team
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
      console.error('Error creating team:', err)
      return null
    } finally {
      loading.value = false
    }
  }
  
  const updateTeam = async (teamId: string, data: TeamUpdateData): Promise<Team | null> => {
    loading.value = true
    error.value = null
    
    try {
      const url = `${apiBase}/api/teams/${teamId}`
      const { data: response, error: fetchError } = await useFetch(url, {
        method: 'PUT',
        body: data
      })
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to update team')
      }
      
      const team = response.value as Team
      
      // Update teams list
      const index = teams.value.findIndex(t => t.id === teamId)
      if (index !== -1) {
        teams.value[index] = team
      }
      
      return team
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
      console.error('Error updating team:', err)
      return null
    } finally {
      loading.value = false
    }
  }
  
  const deleteTeam = async (teamId: string): Promise<boolean> => {
    loading.value = true
    error.value = null
    
    try {
      const url = `${apiBase}/api/teams/${teamId}`
      const { error: fetchError } = await useFetch(url, {
        method: 'DELETE'
      })
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to delete team')
      }
      
      // Remove from teams list
      teams.value = teams.value.filter(t => t.id !== teamId)
      totalCount.value = Math.max(0, totalCount.value - 1)
      
      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
      console.error('Error deleting team:', err)
      return false
    } finally {
      loading.value = false
    }
  }
  
  const joinTeam = async (teamId: string): Promise<boolean> => {
    try {
      const url = `${apiBase}/api/teams/${teamId}/join`
      const { error: fetchError } = await useFetch(url, {
        method: 'POST'
      })
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to join team')
      }
      
      // Refresh team data
      await fetchTeam(teamId)
      
      return true
    } catch (err) {
      console.error('Error joining team:', err)
      return false
    }
  }
  
  const leaveTeam = async (teamId: string): Promise<boolean> => {
    try {
      const url = `${apiBase}/api/teams/${teamId}/leave`
      const { error: fetchError } = await useFetch(url, {
        method: 'POST'
      })
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to leave team')
      }
      
      // Refresh team data
      await fetchTeam(teamId)
      
      return true
    } catch (err) {
      console.error('Error leaving team:', err)
      return false
    }
  }
  
  const cancelJoinRequest = async (teamId: string): Promise<boolean> => {
    try {
      const url = `${apiBase}/api/teams/${teamId}/cancel-join`
      const { error: fetchError } = await useFetch(url, {
        method: 'POST'
      })
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to cancel join request')
      }
      
      // Refresh team data
      await fetchTeam(teamId)
      
      return true
    } catch (err) {
      console.error('Error canceling join request:', err)
      return false
    }
  }
  
  const inviteMember = async (teamId: string, data: TeamInvitationCreateData): Promise<TeamInvitation | null> => {
    try {
      const url = `${apiBase}/api/teams/${teamId}/invitations`
      const { data: response, error: fetchError } = await useFetch(url, {
        method: 'POST',
        body: data
      })
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to invite member')
      }
      
      const invitation = response.value as TeamInvitation
      
      // Update invitations list
      teamInvitations.value.push({
        ...invitation,
        teamId
      })
      
      return invitation
    } catch (err) {
      console.error('Error inviting member:', err)
      return null
    }
  }
  
  const acceptInvitation = async (invitationId: string): Promise<boolean> => {
    try {
      const url = `${apiBase}/api/team-invitations/${invitationId}/accept`
      const { error: fetchError } = await useFetch(url, {
        method: 'POST'
      })
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to accept invitation')
      }
      
      // Update invitation status
      const index = teamInvitations.value.findIndex(i => i.id === invitationId)
      if (index !== -1 && teamInvitations.value[index]) {
        teamInvitations.value[index]!.status = TeamInvitationStatus.ACCEPTED
      }
      
      return true
    } catch (err) {
      console.error('Error accepting invitation:', err)
      return false
    }
  }
  
  const rejectInvitation = async (invitationId: string): Promise<boolean> => {
    try {
      const url = `${apiBase}/api/team-invitations/${invitationId}/reject`
      const { error: fetchError } = await useFetch(url, {
        method: 'POST'
      })
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to reject invitation')
      }
      
      // Update invitation status
      const index = teamInvitations.value.findIndex(i => i.id === invitationId)
      if (index !== -1 && teamInvitations.value[index]) {
        teamInvitations.value[index]!.status = TeamInvitationStatus.REJECTED
      }
      
      return true
    } catch (err) {
      console.error('Error rejecting invitation:', err)
      return false
    }
  }
  
  const cancelInvitation = async (invitationId: string): Promise<boolean> => {
    try {
      const url = `${apiBase}/api/team-invitations/${invitationId}`
      const { error: fetchError } = await useFetch(url, {
        method: 'DELETE'
      })
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to cancel invitation')
      }
      
      // Remove from invitations list
      teamInvitations.value = teamInvitations.value.filter(i => i.id !== invitationId)
      
      return true
    } catch (err) {
      console.error('Error canceling invitation:', err)
      return false
    }
  }
  
  const updateMemberRole = async (teamId: string, memberId: string, role: TeamMemberRole): Promise<boolean> => {
    try {
      const url = `${apiBase}/api/teams/${teamId}/members/${memberId}`
      const { error: fetchError } = await useFetch(url, {
        method: 'PUT',
        body: { role }
      })
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to update member role')
      }
      
      // Update member role in list
      const index = teamMembers.value.findIndex(m => m.id === memberId && m.teamId === teamId)
      if (index !== -1) {
        teamMembers.value[index]!.role = role
      }
      
      return true
    } catch (err) {
      console.error('Error updating member role:', err)
      return false
    }
  }
  
  const removeMember = async (teamId: string, memberId: string): Promise<boolean> => {
    try {
      const url = `${apiBase}/api/teams/${teamId}/members/${memberId}`
      const { error: fetchError } = await useFetch(url, {
        method: 'DELETE'
      })
      
      if (fetchError.value) {
        throw new Error(fetchError.value.message || 'Failed to remove member')
      }
      
      // Remove from members list
      teamMembers.value = teamMembers.value.filter(m => !(m.id === memberId && m.teamId === teamId))
      
      return true
    } catch (err) {
      console.error('Error removing member:', err)
      return false
    }
  }
  
  // Pagination methods
  const goToPage = async (page: number) => {
    if (page < 1 || page > totalPages.value) return
    await fetchTeams({ page })
  }
  
  const goToNextPage = async () => {
    if (hasNextPage.value) {
      await fetchTeams({ page: currentPage.value + 1 })
    }
  }
  
  const goToPreviousPage = async () => {
    if (hasPreviousPage.value) {
      await fetchTeams({ page: currentPage.value - 1 })
    }
  }
  
  // Reset method
  const reset = () => {
    teams.value = []
    teamMembers.value = []
    teamInvitations.value = []
    stats.value = null
    loading.value = false
    error.value = null
    currentPage.value = 1
    totalPages.value = 1
    totalCount.value = 0
    sortOption.value = initialSort
    filterOption.value = initialFilter
    searchQuery.value = ''
  }
  
  // Auto-fetch on initialization if enabled
  if (autoFetch) {
    fetchTeams()
  }
  
  return {
    // State
    teams,
    teamMembers,
    teamInvitations,
    stats,
    loading,
    error,
    
    // Pagination
    currentPage,
    totalPages,
    totalCount,
    hasNextPage,
    hasPreviousPage,
    
    // Filters and sorting
    sortOption,
    filterOption,
    searchQuery,
    
    // Computed
    filteredTeams,
    teamMembersMap,
    userTeams,
    joinedTeams,
    pendingInvitations,
    
    // Methods
    fetchTeams,
    fetchTeam,
    fetchTeamMembers,
    fetchTeamInvitations,
    fetchTeamStats,
    
    createTeam,
    updateTeam,
    deleteTeam,
    
    joinTeam,
    leaveTeam,
    cancelJoinRequest,
    
    inviteMember,
    acceptInvitation,
    rejectInvitation,
    cancelInvitation,
    
    updateMemberRole,
    removeMember,
    
    // Pagination
    goToPage,
    goToNextPage,
    goToPreviousPage,
    
    // Reset
    reset
  }
}