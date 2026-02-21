import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'
import { useUIStore } from './ui'

export interface Team {
  id: number
  name: string
  description: string
  hackathon_id: number
  max_members: number
  is_open: boolean
  created_by: number
  created_at: string
  updated_at?: string
  member_count?: number
  members?: TeamMember[]
  creator?: {
    id: number
    username: string
    avatar_url?: string
    name?: string
  }
  hackathon?: {
    id: number
    name: string
  }
}

export interface TeamMember {
  id: number
  team_id: number
  user_id: number
  role: 'owner' | 'member'
  joined_at: string
  user?: {
    id: number
    username: string
    avatar_url?: string
    name?: string
  }
  team?: Team
}

export interface TeamInvitation {
  id: number
  team_id: number
  invited_user_id: number
  invited_by: number
  status: 'pending' | 'accepted' | 'declined'
  created_at: string
  expires_at: string | null
  invited_user?: {
    id: number
    username: string
    avatar_url?: string
    name?: string
  }
  inviter?: {
    id: number
    username: string
    avatar_url?: string
    name?: string
  }
  team?: Team
}

export interface CreateTeamData {
  name: string
  description: string
  hackathon_id: number
  max_members?: number
  is_open?: boolean
}

export interface UpdateTeamData {
  name?: string
  description?: string
  hackathon_id?: number
  max_members?: number
  is_open?: boolean
}

export interface InviteToTeamData {
  invited_user_id: number
}

export const useTeamStore = defineStore('team', () => {
  const authStore = useAuthStore()
  const uiStore = useUIStore()
  
  // State
  const teams = ref<Team[]>([])
  const currentTeam = ref<Team | null>(null)
  const teamMembers = ref<Map<number, TeamMember[]>>(new Map()) // team_id -> TeamMember[]
  const invitations = ref<TeamInvitation[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const myTeams = computed(() => {
    if (!authStore.user?.id) return []
    return teams.value.filter(team => 
      teamMembers.value.get(team.id)?.some(member => member.user_id === authStore.user!.id)
    )
  })

  const ownedTeams = computed(() => {
    if (!authStore.user?.id) return []
    return teams.value.filter(team => 
      teamMembers.value.get(team.id)?.some(member => 
        member.user_id === authStore.user!.id && member.role === 'owner'
      )
    )
  })

  const pendingInvitations = computed(() => {
    return invitations.value.filter(inv => inv.status === 'pending')
  })

  // Helper function for API calls
  async function fetchWithAuth(url: string, options: RequestInit = {}) {
    return authStore.fetchWithAuth(url, options)
  }

  // Actions
  async function fetchTeams(params?: {
    hackathon_id?: number
    skip?: number
    limit?: number
    is_open?: boolean
  }) {
    isLoading.value = true
    error.value = null

    try {
      const queryParams = new URLSearchParams()
      if (params?.hackathon_id) queryParams.append('hackathon_id', params.hackathon_id.toString())
      if (params?.skip) queryParams.append('skip', params.skip.toString())
      if (params?.limit) queryParams.append('limit', params.limit.toString())
      if (params?.is_open !== undefined) queryParams.append('is_open', params.is_open.toString())

      const url = `/api/teams${queryParams.toString() ? `?${queryParams.toString()}` : ''}`
      const response = await fetchWithAuth(url)
      
      if (!response.ok) {
        throw new Error(`Failed to fetch teams: ${response.status}`)
      }

      const data = await response.json()
      teams.value = data
      
      // Fetch members for each team
      for (const team of data) {
        await fetchTeamMembers(team.id)
      }
      
      return data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch teams'
      uiStore.showError(error.value, 'Team Error')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchTeam(teamId: number) {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetchWithAuth(`/api/teams/${teamId}`)
      
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Team not found')
        }
        throw new Error(`Failed to fetch team: ${response.status}`)
      }

      const data = await response.json()
      currentTeam.value = data
      
      // Update teams list
      const index = teams.value.findIndex(t => t.id === teamId)
      if (index !== -1) {
        teams.value[index] = data
      } else {
        teams.value.push(data)
      }
      
      // Fetch members
      await fetchTeamMembers(teamId)
      
      return data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch team'
      uiStore.showError(error.value, 'Team Error')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function createTeam(teamData: CreateTeamData) {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetchWithAuth('/api/teams', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(teamData)
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Failed to create team: ${response.status}`)
      }

      const data = await response.json()
      teams.value.push(data)
      currentTeam.value = data
      
      // Fetch members for the new team
      await fetchTeamMembers(data.id)
      
      uiStore.showSuccess('Team created successfully')
      return data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create team'
      uiStore.showError(error.value, 'Team Creation Error')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function updateTeam(teamId: number, teamData: UpdateTeamData) {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetchWithAuth(`/api/teams/${teamId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(teamData)
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Failed to update team: ${response.status}`)
      }

      const data = await response.json()
      
      // Update in teams list
      const index = teams.value.findIndex(t => t.id === teamId)
      if (index !== -1) {
        teams.value[index] = data
      }
      
      // Update current team if it's the one being updated
      if (currentTeam.value?.id === teamId) {
        currentTeam.value = data
      }
      
      uiStore.showSuccess('Team updated successfully')
      return data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update team'
      uiStore.showError(error.value, 'Team Update Error')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function deleteTeam(teamId: number) {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetchWithAuth(`/api/teams/${teamId}`, {
        method: 'DELETE'
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Failed to delete team: ${response.status}`)
      }

      // Remove from teams list
      teams.value = teams.value.filter(t => t.id !== teamId)
      
      // Clear current team if it's the one being deleted
      if (currentTeam.value?.id === teamId) {
        currentTeam.value = null
      }
      
      // Remove members cache
      teamMembers.value.delete(teamId)
      
      uiStore.showSuccess('Team deleted successfully')
      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete team'
      uiStore.showError(error.value, 'Team Deletion Error')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchTeamMembers(teamId: number) {
    try {
      const response = await fetchWithAuth(`/api/teams/${teamId}/members`)
      
      if (!response.ok) {
        // If 403, user might not be a team member - skip caching members
        if (response.status === 403) {
          teamMembers.value.set(teamId, [])
          return []
        }
        throw new Error(`Failed to fetch team members: ${response.status}`)
      }

      const data = await response.json()
      teamMembers.value.set(teamId, data)
      return data
    } catch (err) {
      console.error('Failed to fetch team members:', err)
      // Don't show error to user for member fetching failures
      return []
    }
  }

  async function addTeamMember(teamId: number, userId: number, role: 'owner' | 'member' = 'member') {
    try {
      const response = await fetchWithAuth(`/api/teams/${teamId}/members`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId, role })
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Failed to add team member: ${response.status}`)
      }

      const data = await response.json()
      
      // Update members cache
      const currentMembers = teamMembers.value.get(teamId) || []
      teamMembers.value.set(teamId, [...currentMembers, data])
      
      uiStore.showSuccess('Team member added successfully')
      return data
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to add team member'
      uiStore.showError(errorMsg, 'Team Member Error')
      throw err
    }
  }

  async function removeTeamMember(teamId: number, userId: number) {
    try {
      const response = await fetchWithAuth(`/api/teams/${teamId}/members/${userId}`, {
        method: 'DELETE'
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Failed to remove team member: ${response.status}`)
      }

      // Update members cache
      const currentMembers = teamMembers.value.get(teamId) || []
      teamMembers.value.set(teamId, currentMembers.filter(member => member.user_id !== userId))
      
      // If user removed themselves, update teams list
      if (userId === authStore.user?.id) {
        teams.value = teams.value.filter(t => t.id !== teamId)
        if (currentTeam.value?.id === teamId) {
          currentTeam.value = null
        }
      }
      
      uiStore.showSuccess('Team member removed successfully')
      return true
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to remove team member'
      uiStore.showError(errorMsg, 'Team Member Error')
       throw err
     }
   }

   async function updateTeamMemberRole(teamId: number, userId: number, role: 'owner' | 'member') {
     try {
       const response = await fetchWithAuth(`/api/teams/${teamId}/members/${userId}`, {
         method: 'PATCH',
         headers: {
           'Content-Type': 'application/json'
         },
         body: JSON.stringify({ role })
       })
       
       if (!response.ok) {
         const errorData = await response.json().catch(() => ({}))
         throw new Error(errorData.detail || `Failed to update team member role: ${response.status}`)
       }

       const data = await response.json()
       
       // Update members cache
       const currentMembers = teamMembers.value.get(teamId) || []
       teamMembers.value.set(teamId, currentMembers.map(member => 
         member.user_id === userId ? { ...member, role: data.role } : member
       ))
       
       uiStore.showSuccess(`Team member role updated to ${role}`)
       return data
     } catch (err) {
       const errorMsg = err instanceof Error ? err.message : 'Failed to update team member role'
       uiStore.showError(errorMsg, 'Team Member Error')
       throw err
     }
   }

   async function fetchMyInvitations() {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetchWithAuth('/api/me/invitations')
      
      if (!response.ok) {
        throw new Error(`Failed to fetch invitations: ${response.status}`)
      }

      const data = await response.json()
      invitations.value = data
      return data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch invitations'
      uiStore.showError(error.value, 'Invitations Error')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function acceptInvitation(invitationId: number) {
    try {
      const response = await fetchWithAuth(`/api/invitations/${invitationId}/accept`, {
        method: 'POST'
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Failed to accept invitation: ${response.status}`)
      }

      const data = await response.json()
      
      // Update invitations list
      invitations.value = invitations.value.map(inv => 
        inv.id === invitationId ? { ...inv, status: 'accepted' } : inv
      )
      
      // Add team to teams list
      const teamId = data.team_id
      await fetchTeam(teamId)
      
      uiStore.showSuccess('Invitation accepted successfully')
      return data
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to accept invitation'
      uiStore.showError(errorMsg, 'Invitation Error')
      throw err
    }
  }

  async function declineInvitation(invitationId: number) {
    try {
      const response = await fetchWithAuth(`/api/invitations/${invitationId}/decline`, {
        method: 'POST'
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Failed to decline invitation: ${response.status}`)
      }

      // Update invitations list
      invitations.value = invitations.value.map(inv => 
        inv.id === invitationId ? { ...inv, status: 'declined' } : inv
      )
      
      uiStore.showSuccess('Invitation declined')
      return true
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to decline invitation'
      uiStore.showError(errorMsg, 'Invitation Error')
      throw err
    }
  }

  async function inviteToTeam(teamId: number, userId: number) {
    try {
      const response = await fetchWithAuth(`/api/teams/${teamId}/invitations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ team_id: teamId, invited_user_id: userId })
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Failed to send invitation: ${response.status}`)
      }

      const data = await response.json()
      uiStore.showSuccess('Invitation sent successfully')
      return data
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to send invitation'
      uiStore.showError(errorMsg, 'Invitation Error')
      throw err
    }
  }

  async function fetchHackathonTeams(hackathonId: number) {
    try {
      const response = await fetchWithAuth(`/api/hackathons/${hackathonId}/teams`)
      
      if (!response.ok) {
        throw new Error(`Failed to fetch hackathon teams: ${response.status}`)
      }

      const data = await response.json()
      
      // Update teams list
      data.forEach((team: Team) => {
        const index = teams.value.findIndex(t => t.id === team.id)
        if (index !== -1) {
          teams.value[index] = team
        } else {
          teams.value.push(team)
        }
      })
      
      return data
    } catch (err) {
      console.error('Failed to fetch hackathon teams:', err)
      return []
    }
  }

  // Initialize store with user's teams from auth store
  function initializeFromUser(user: any) {
    if (user?.teams) {
      // Note: The /api/me endpoint now returns teams in the UserWithDetails schema
      // We need to extract and store them
      teams.value = user.teams.map((teamMember: any) => teamMember.team).filter(Boolean)
      
      // Store team members
      user.teams.forEach((teamMember: any) => {
        if (teamMember.team_id) {
          const currentMembers = teamMembers.value.get(teamMember.team_id) || []
          teamMembers.value.set(teamMember.team_id, [...currentMembers, teamMember])
        }
      })
    }
  }

  // Clear store
  function clear() {
    teams.value = []
    currentTeam.value = null
    teamMembers.value.clear()
    invitations.value = []
    error.value = null
  }

  return {
    // State
    teams,
    currentTeam,
    teamMembers,
    invitations,
    isLoading,
    error,
    
    // Computed
    myTeams,
    ownedTeams,
    pendingInvitations,
    
    // Actions
    fetchTeams,
    fetchTeam,
    createTeam,
    updateTeam,
    deleteTeam,
    fetchTeamMembers,
    addTeamMember,
    removeTeamMember,
    updateTeamMemberRole,
    fetchMyInvitations,
    acceptInvitation,
    declineInvitation,
    inviteToTeam,
    fetchHackathonTeams,
    initializeFromUser,
    clear
  }
})