import { ref, computed, type Ref } from 'vue'
import { useTeamStore } from '~/stores/team'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n } from '#imports'

export interface TeamMember {
  id: number
  user_id: number
  user?: {
    id: number
    name: string
    username: string
    avatar_url?: string
  }
  role: 'owner' | 'member'
  joined_at: string
}

export interface UseTeamMembersOptions {
  teamId: Ref<number | string>
  autoFetch?: boolean
  labels?: {
    confirmRemoveMember?: string
    confirmMakeOwner?: string
    confirmDemoteOwner?: string
    memberRemovedSuccess?: string
  }
}

export function useTeamMembers(options: UseTeamMembersOptions) {
  const { teamId, autoFetch = true, labels: customLabels } = options
  
  const teamStore = useTeamStore()
  const authStore = useAuthStore()
  const uiStore = useUIStore()
  const { t } = useI18n()

  // Default labels with i18n fallback
  const labels = {
    confirmRemoveMember: customLabels?.confirmRemoveMember || t('teams.confirmRemoveMember'),
    confirmMakeOwner: customLabels?.confirmMakeOwner || t('teams.confirmMakeOwner'),
    confirmDemoteOwner: customLabels?.confirmDemoteOwner || t('teams.confirmDemoteOwner'),
    memberRemovedSuccess: customLabels?.memberRemovedSuccess || t('teams.memberRemovedSuccess'),
  }

  // State
  const members = ref<TeamMember[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const currentUserId = computed(() => authStore.user?.id ? Number(authStore.user.id) : null)
  
  const isTeamOwner = computed(() => {
    if (!currentUserId.value) return false
    const currentUserMember = members.value.find(m => m.user_id === currentUserId.value)
    return currentUserMember?.role === 'owner'
  })

  const isTeamMember = computed(() => {
    if (!currentUserId.value) return false
    return members.value.some(m => m.user_id === currentUserId.value)
  })

  const memberCount = computed(() => members.value.length)
  
  const owners = computed(() => members.value.filter(m => m.role === 'owner'))
  const regularMembers = computed(() => members.value.filter(m => m.role === 'member'))

  // Methods
  async function fetchMembers() {
    if (!teamId.value) {
      error.value = 'Team ID is required'
      return
    }

    loading.value = true
    error.value = null

    try {
      // Use teamStore to fetch members
      await teamStore.fetchTeamMembers(Number(teamId.value))
      
      // Get members from store
      const storeMembers = teamStore.teamMembers.get(Number(teamId.value)) || []
      members.value = storeMembers.map((member: any) => ({
        id: member.id,
        user_id: member.user_id,
        user: member.user,
        role: member.role,
        joined_at: member.joined_at || member.created_at,
      }))
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch team members'
      console.error('Failed to fetch team members:', err)
      members.value = []
    } finally {
      loading.value = false
    }
  }

  async function removeMember(userId: number) {
    if (!isTeamOwner.value) {
      uiStore.showError('Permission denied', 'Only team owners can remove members')
      return false
    }

    const confirmed = confirm(labels.confirmRemoveMember)
    if (!confirmed) return false

    try {
      await teamStore.removeTeamMember(Number(teamId.value), userId)
      uiStore.showSuccess(labels.memberRemovedSuccess)
      
      // Refresh members list
      await fetchMembers()
      return true
    } catch (err) {
      console.error('Failed to remove member:', err)
      uiStore.showError('Failed to remove member', err instanceof Error ? err.message : 'Unknown error')
      return false
    }
  }

  async function makeOwner(userId: number) {
    if (!isTeamOwner.value) {
      uiStore.showError('Permission denied', 'Only team owners can change roles')
      return false
    }

    const confirmed = confirm(labels.confirmMakeOwner)
    if (!confirmed) return false

    try {
      await teamStore.updateTeamMemberRole(Number(teamId.value), userId, 'owner')
      
      // Refresh members list
      await fetchMembers()
      return true
    } catch (err) {
      console.error('Failed to make member owner:', err)
      uiStore.showError('Failed to change role', err instanceof Error ? err.message : 'Unknown error')
      return false
    }
  }

  async function makeMember(userId: number) {
    if (!isTeamOwner.value) {
      uiStore.showError('Permission denied', 'Only team owners can change roles')
      return false
    }

    const confirmed = confirm(labels.confirmDemoteOwner)
    if (!confirmed) return false

    try {
      await teamStore.updateTeamMemberRole(Number(teamId.value), userId, 'member')
      
      // Refresh members list
      await fetchMembers()
      return true
    } catch (err) {
      console.error('Failed to make owner member:', err)
      uiStore.showError('Failed to change role', err instanceof Error ? err.message : 'Unknown error')
      return false
    }
  }

  async function addMember(userId: number, role: 'owner' | 'member' = 'member') {
    if (!isTeamOwner.value) {
      uiStore.showError('Permission denied', 'Only team owners can add members')
      return false
    }

    try {
      await teamStore.addTeamMember(Number(teamId.value), userId, role)
      
      // Refresh members list
      await fetchMembers()
      return true
    } catch (err) {
      console.error('Failed to add member:', err)
      uiStore.showError('Failed to add member', err instanceof Error ? err.message : 'Unknown error')
      return false
    }
  }

  function getMember(userId: number): TeamMember | undefined {
    return members.value.find(m => m.user_id === userId)
  }

  function isUserMember(userId: number): boolean {
    return members.value.some(m => m.user_id === userId)
  }

  function isUserOwner(userId: number): boolean {
    const member = getMember(userId)
    return member?.role === 'owner'
  }

  // Auto-fetch on mount if enabled
  if (autoFetch) {
    fetchMembers()
  }

  return {
    // State
    members,
    loading,
    error,
    
    // Computed
    currentUserId,
    isTeamOwner,
    isTeamMember,
    memberCount,
    owners,
    regularMembers,
    
    // Methods
    fetchMembers,
    removeMember,
    makeOwner,
    makeMember,
    addMember,
    getMember,
    isUserMember,
    isUserOwner,
  }
}

export type UseTeamMembersReturn = ReturnType<typeof useTeamMembers>