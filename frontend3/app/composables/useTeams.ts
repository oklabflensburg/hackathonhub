/**
 * Teams Composable
 * Bietet eine konsistente Schnittstelle für alle Team-Operationen
 * Kapselt API-Aufrufe und bietet reaktiven State, Loading-States und Error-Handling
 * 
 * Migriert zur Verwendung zentraler Typ-Definitionen aus team-types.ts
 */

import { ref, computed, type Ref } from 'vue'
import { useApiClient } from '~/utils/api-client'
import { useUIStore } from '~/stores/ui'
import type {
  Team,
  TeamMember,
  TeamInvitation,
  TeamCreateUpdatePayload,
  TeamInvitationCreateData,
  TeamMemberUpdatePayload,
  TeamSearchFilterOptions,
  TeamPaginationResponse,
  TeamFilterState,
  UseTeamsReturn
} from '~/types/team-types'
import {
  TeamRole,
  TeamStatus,
  TeamVisibility,
  TeamInvitationStatus,
  TeamSortOption
} from '~/types/team-types'

// API Response Interfaces (snake_case from backend)
interface ApiTeam {
  id: number
  name: string
  description?: string
  hackathon_id: number
  max_members: number
  is_open: boolean
  created_by: number
  created_at: string
  creator?: any
  hackathon?: any
  member_count?: number
  _member_count?: number
}

interface ApiTeamMember {
  id: number
  team_id: number
  user_id: number
  role: string
  joined_at: string
  user?: any
  team?: any
}

interface ApiTeamInvitation {
  id: number
  team_id: number
  invited_user_id: number
  invited_by: number
  status: string
  created_at: string
  expires_at?: string
  invited_user?: any
  inviter?: any
  team?: any
}

export interface UseTeamsOptions {
  /** Automatisches Error-Handling (Notifications) */
  autoErrorHandling?: boolean
  /** Automatisches Success-Handling (Notifications) */
  autoSuccessHandling?: boolean
  /** Initiale Team-ID für Single-Team-Operationen */
  initialTeamId?: string
  /** Hackathon-ID für Filterung */
  hackathonId?: string
  /** Initiale Filter */
  initialFilters?: Partial<TeamFilterState>
  /** Initiale Sortierung */
  initialSort?: TeamSortOption
  /** Initiale Suchanfrage */
  initialSearch?: string
  /** Seitengröße für Pagination */
  pageSize?: number
}

/**
 * Teams Composable
 */
export function useTeams(options: UseTeamsOptions = {}): UseTeamsReturn {
  const {
    autoErrorHandling = true,
    autoSuccessHandling = true,
    initialTeamId,
    hackathonId,
    initialFilters = {},
    initialSort = TeamSortOption.CREATED_AT_DESC,
    initialSearch = '',
    pageSize = 20
  } = options

  // Stores und Services
  const uiStore = useUIStore()
  const apiClient = useApiClient()

  // State
  const teams: Ref<Team[]> = ref([])
  const loading = ref(false)
  const error: Ref<string | null> = ref(null)
  const totalCount = ref(0)
  const page = ref(1)
  const pageSizeRef = ref(pageSize)
  const searchQuery = ref(initialSearch)
  const selectedFilters: Ref<Partial<TeamFilterState>> = ref(initialFilters)
  const sortOption: Ref<TeamSortOption> = ref(initialSort)

  // Current team state
  const currentTeam = ref<Team | null>(null)
  const teamMembers = ref<TeamMember[]>([])
  const teamInvitations = ref<TeamInvitation[]>([])
  const teamProjects = ref<any[]>([])

  // Computed Properties
  const hasTeams = computed(() => teams.value.length > 0)
  const teamCount = computed(() => teams.value.length)
  const currentTeamMembers = computed(() => teamMembers.value)
  const currentTeamInvitations = computed(() => teamInvitations.value)

  /**
   * API Response zu Frontend-Typ mappen
   */
  function mapApiTeamToTeam(apiTeam: ApiTeam): Team {
    return {
      id: apiTeam.id.toString(),
      name: apiTeam.name,
      description: apiTeam.description || null,
      slug: apiTeam.name.toLowerCase().replace(/\s+/g, '-'),
      avatarUrl: null,
      bannerUrl: null,
      visibility: apiTeam.is_open ? TeamVisibility.PUBLIC : TeamVisibility.PRIVATE,
      status: TeamStatus.ACTIVE,
      maxMembers: apiTeam.max_members || null,
      createdAt: apiTeam.created_at,
      updatedAt: apiTeam.created_at,
      createdBy: apiTeam.created_by.toString(),
      hackathonId: apiTeam.hackathon_id ? apiTeam.hackathon_id.toString() : null,
      tags: [],
      stats: {
        memberCount: apiTeam.member_count || apiTeam._member_count || 0,
        projectCount: 0,
        activeProjectCount: 0,
        completedProjectCount: 0,
        totalVotes: 0,
        totalComments: 0,
        averageRating: null,
        lastActivityAt: null,
        viewCount: 0
      }
    }
  }

  /**
   * API Team Member zu Frontend-Typ mappen
   */
  function mapApiTeamMemberToTeamMember(apiMember: ApiTeamMember): TeamMember {
    return {
      id: apiMember.id.toString(),
      userId: apiMember.user_id.toString(),
      teamId: apiMember.team_id.toString(),
      role: apiMember.role as TeamRole,
      joinedAt: apiMember.joined_at,
      user: apiMember.user ? {
        id: apiMember.user.id?.toString() || '',
        username: apiMember.user.username || '',
        displayName: apiMember.user.display_name || null,
        avatarUrl: apiMember.user.avatar_url || null,
        email: apiMember.user.email || null,
        bio: apiMember.user.bio || null,
        skills: apiMember.user.skills || []
      } : undefined
    }
  }

  /**
   * API Team Invitation zu Frontend-Typ mappen
   */
  function mapApiTeamInvitationToTeamInvitation(apiInvitation: ApiTeamInvitation): TeamInvitation {
    return {
      id: apiInvitation.id.toString(),
      teamId: apiInvitation.team_id.toString(),
      invitedUserId: apiInvitation.invited_user_id ? apiInvitation.invited_user_id.toString() : null,
      invitedEmail: null,
      invitedByUserId: apiInvitation.invited_by.toString(),
      role: (apiInvitation as any).role as TeamRole || TeamRole.MEMBER,
      status: apiInvitation.status as TeamInvitationStatus,
      message: null,
      expiresAt: apiInvitation.expires_at || '',
      createdAt: apiInvitation.created_at,
      updatedAt: apiInvitation.created_at,
      team: apiInvitation.team ? mapApiTeamToTeam(apiInvitation.team) : undefined,
      invitedByUser: apiInvitation.inviter ? {
        id: apiInvitation.inviter.id?.toString() || '',
        username: apiInvitation.inviter.username || '',
        displayName: apiInvitation.inviter.display_name || null,
        avatarUrl: apiInvitation.inviter.avatar_url || null,
        email: apiInvitation.inviter.email || null,
        bio: apiInvitation.inviter.bio || null,
        skills: apiInvitation.inviter.skills || []
      } : undefined,
      invitedUser: apiInvitation.invited_user ? {
        id: apiInvitation.invited_user.id?.toString() || '',
        username: apiInvitation.invited_user.username || '',
        displayName: apiInvitation.invited_user.display_name || null,
        avatarUrl: apiInvitation.invited_user.avatar_url || null,
        email: apiInvitation.invited_user.email || null,
        bio: apiInvitation.invited_user.bio || null,
        skills: apiInvitation.invited_user.skills || []
      } : undefined
    }
  }

  /**
   * Frontend-Typ zu API Payload mappen
   */
  function mapTeamCreateUpdatePayloadToApi(payload: TeamCreateUpdatePayload): any {
    return {
      name: payload.name,
      description: payload.description,
      visibility: payload.visibility,
      max_members: payload.maxMembers,
      hackathon_id: payload.hackathonId ? parseInt(payload.hackathonId) : null,
      tags: payload.tags,
      is_open: payload.visibility === TeamVisibility.PUBLIC
    }
  }

  /**
   * Alle Teams abrufen
   */
  async function fetchTeams(fetchOptions?: TeamSearchFilterOptions): Promise<void> {
    try {
      loading.value = true
      error.value = null

      const options = fetchOptions || {
        query: searchQuery.value,
        page: page.value,
        pageSize: pageSizeRef.value,
        sortBy: sortOption.value,
        filters: selectedFilters.value,
        hackathonId: hackathonId
      }

      const queryParams = new URLSearchParams()
      if (options.query) queryParams.append('search', options.query)
      if (options.page) queryParams.append('page', options.page.toString())
      if (options.pageSize) queryParams.append('limit', options.pageSize.toString())
      if (options.hackathonId) queryParams.append('hackathon_id', options.hackathonId)
      
      // Filter hinzufügen
      if (options.filters?.visibility && options.filters.visibility !== 'all') {
        queryParams.append('is_open', options.filters.visibility === TeamVisibility.PUBLIC ? 'true' : 'false')
      }

      const url = `/api/teams${queryParams.toString() ? `?${queryParams.toString()}` : ''}`
      const response = await apiClient.get<ApiTeam[]>(url)

      // Mappen und speichern
      teams.value = response.map(mapApiTeamToTeam)
      totalCount.value = response.length
      
      // Update state
      if (options.page) page.value = options.page
      if (options.pageSize) pageSizeRef.value = options.pageSize
      if (options.query !== undefined) searchQuery.value = options.query || ''
      if (options.sortBy) sortOption.value = options.sortBy
      if (options.filters) selectedFilters.value = options.filters

    } catch (err: any) {
      error.value = err.message || 'Fehler beim Abrufen der Teams'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Teams Fehler')
      }
      
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Einzelnes Team abrufen
   */
  async function fetchTeam(teamId: string): Promise<Team | null> {
    try {
      loading.value = true
      error.value = null

      const response = await apiClient.get<ApiTeam>(`/api/teams/${teamId}`)
      const team = mapApiTeamToTeam(response)
      currentTeam.value = team

      // Team-Mitglieder und Einladungen abrufen
      await fetchTeamMembers(teamId)
      await fetchTeamInvitations(teamId)
      // await fetchTeamProjects(teamId) // TODO: Implement wenn Projekte-API verfügbar

      return team
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Abrufen des Teams'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Team Fehler')
      }
      
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * Team erstellen
   */
  async function createTeam(data: TeamCreateUpdatePayload): Promise<Team | null> {
    try {
      loading.value = true
      error.value = null

      const apiPayload = mapTeamCreateUpdatePayloadToApi(data)
      const response = await apiClient.post<ApiTeam>('/api/teams', apiPayload, {
        skipErrorNotification: true
      })

      const team = mapApiTeamToTeam(response)
      
      // Zum lokalen State hinzufügen
      teams.value = [team, ...teams.value]
      currentTeam.value = team

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Team erfolgreich erstellt', 'Team')
      }

      return team
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Erstellen des Teams'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Team Erstellung Fehler')
      }
      
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * Team aktualisieren
   */
  async function updateTeam(teamId: string, data: TeamCreateUpdatePayload): Promise<Team | null> {
    try {
      loading.value = true
      error.value = null

      const apiPayload = mapTeamCreateUpdatePayloadToApi(data)
      const response = await apiClient.put<ApiTeam>(`/api/teams/${teamId}`, apiPayload, {
        skipErrorNotification: true
      })

      const team = mapApiTeamToTeam(response)
      
      // Lokalen State aktualisieren
      if (currentTeam.value?.id === teamId) {
        currentTeam.value = team
      }

      // In der Teams-Liste aktualisieren
      const index = teams.value.findIndex(t => t.id === teamId)
      if (index !== -1) {
        teams.value[index] = team
      }

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Team erfolgreich aktualisiert', 'Team')
      }

      return team
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Aktualisieren des Teams'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Team Update Fehler')
      }
      
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * Team löschen
   */
  async function deleteTeam(teamId: string): Promise<boolean> {
    try {
      loading.value = true
      error.value = null

      await apiClient.delete(`/api/teams/${teamId}`, {
        skipErrorNotification: true
      })

      // Aus lokalem State entfernen
      teams.value = teams.value.filter(t => t.id !== teamId)
      if (currentTeam.value?.id === teamId) {
        currentTeam.value = null
        teamMembers.value = []
        teamInvitations.value = []
        teamProjects.value = []
      }

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Team erfolgreich gelöscht', 'Team')
      }

      return true
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Löschen des Teams'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Team Löschung Fehler')
      }
      
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Team-Mitglieder abrufen
   */
  async function fetchTeamMembers(teamId: string): Promise<void> {
    try {
      const response = await apiClient.get<ApiTeamMember[]>(`/api/teams/${teamId}/members`)
      teamMembers.value = response.map(mapApiTeamMemberToTeamMember)
    } catch (err: any) {
      console.error('Fehler beim Abrufen der Team-Mitglieder:', err)
      throw err
    }
  }

  /**
   * Team-Einladungen abrufen
   */
  async function fetchTeamInvitations(teamId: string): Promise<void> {
    try {
      const response = await apiClient.get<ApiTeamInvitation[]>(`/api/teams/${teamId}/invitations`)
      teamInvitations.value = response.map(mapApiTeamInvitationToTeamInvitation)
    } catch (err: any) {
      console.error('Fehler beim Abrufen der Team-Einladungen:', err)
      throw err
    }
  }

  /**
   * Team-Mitglied hinzufügen
   */
  async function addMember(teamId: string, userId: string, role: TeamRole = TeamRole.MEMBER): Promise<boolean> {
    try {
      loading.value = true
      error.value = null

      const apiPayload = {
        user_id: parseInt(userId),
        role: role
      }

      const response = await apiClient.post<ApiTeamMember>(`/api/teams/${teamId}/members`, apiPayload, {
        skipErrorNotification: true
      })

      // Zum lokalen State hinzufügen
      const member = mapApiTeamMemberToTeamMember(response)
      teamMembers.value = [...teamMembers.value, member]

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Mitglied erfolgreich hinzugefügt', 'Team')
      }

      return true
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Hinzufügen des Mitglieds'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Mitglied Hinzufügung Fehler')
      }
      
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Team-Mitglied entfernen
   */
  async function removeMember(teamId: string, memberId: string): Promise<boolean> {
    try {
      loading.value = true
      error.value = null

      await apiClient.delete(`/api/teams/${teamId}/members/${memberId}`, {
        skipErrorNotification: true
      })

      // Aus lokalem State entfernen
      teamMembers.value = teamMembers.value.filter(m => m.id !== memberId)

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Mitglied erfolgreich entfernt', 'Team')
      }

      return true
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Entfernen des Mitglieds'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Mitglied Entfernung Fehler')
      }
      
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Team-Mitglied Rolle aktualisieren
   */
  async function updateMemberRole(teamId: string, memberId: string, role: TeamRole): Promise<boolean> {
    try {
      loading.value = true
      error.value = null

      const apiPayload = { role }
      const response = await apiClient.put<ApiTeamMember>(`/api/teams/${teamId}/members/${memberId}`, apiPayload, {
        skipErrorNotification: true
      })

      // Lokalen State aktualisieren
      const member = mapApiTeamMemberToTeamMember(response)
      const index = teamMembers.value.findIndex(m => m.id === memberId)
      if (index !== -1) {
        teamMembers.value[index] = member
      }

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Mitglied erfolgreich aktualisiert', 'Team')
      }

      return true
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Aktualisieren des Mitglieds'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Mitglied Update Fehler')
      }
      
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Team beitreten
   */
  async function joinTeam(teamId: string): Promise<boolean> {
    try {
      loading.value = true
      error.value = null

      await apiClient.post(`/api/teams/${teamId}/join`, {}, {
        skipErrorNotification: true
      })

      // Team in der Liste aktualisieren
      const index = teams.value.findIndex(t => t.id === teamId)
      if (index !== -1) {
        const team = teams.value[index]
        teams.value[index] = {
          ...team,
          stats: {
            ...team.stats!,
            memberCount: (team.stats?.memberCount || 0) + 1
          }
        }
      }

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Team erfolgreich beigetreten', 'Team')
      }

      return true
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Beitreten zum Team'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Team Beitritt Fehler')
      }
      
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Team verlassen
   */
  async function leaveTeam(teamId: string): Promise<boolean> {
    try {
      loading.value = true
      error.value = null

      await apiClient.post(`/api/teams/${teamId}/leave`, {}, {
        skipErrorNotification: true
      })

      // Team in der Liste aktualisieren
      const index = teams.value.findIndex(t => t.id === teamId)
      if (index !== -1) {
        const team = teams.value[index]
        teams.value[index] = {
          ...team,
          stats: {
            ...team.stats!,
            memberCount: Math.max(0, (team.stats?.memberCount || 1) - 1)
          }
        }
      }

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Team erfolgreich verlassen', 'Team')
      }

      return true
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Verlassen des Teams'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Team Verlassen Fehler')
      }
      
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Prüfen ob Benutzer Team-Mitglied ist
   */
  function isUserMember(teamId: string, userId: string): boolean {
    return teamMembers.value.some(member => 
      member.teamId === teamId && member.userId === userId
    )
  }

  /**
   * Benutzer-Rolle im Team abrufen
   */
  function getUserRole(teamId: string, userId: string): TeamRole | null {
    const member = teamMembers.value.find(m => 
      m.teamId === teamId && m.userId === userId
    )
    return member?.role || null
  }

  /**
   * Filter zurücksetzen
   */
  function resetFilters(): void {
    selectedFilters.value = {}
    page.value = 1
  }

  /**
   * Suche zurücksetzen
   */
  function resetSearch(): void {
    searchQuery.value = ''
    page.value = 1
  }

  // Return das UseTeamsReturn Interface
  return {
    teams,
    loading,
    error,
    totalCount,
    page,
    pageSize: pageSizeRef,
    searchQuery,
    selectedFilters,
    sortOption,
    
    fetchTeams,
    fetchTeam,
    createTeam,
    updateTeam,
    deleteTeam,
    joinTeam,
    leaveTeam,
    resetFilters,
    resetSearch,
    
    // Zusätzliche Methoden für Team-Mitglieder (nicht im Interface, aber nützlich)
    fetchTeamMembers,
    fetchTeamInvitations,
    addMember,
    removeMember,
    updateMemberRole,
    isUserMember,
    getUserRole
  }
}
