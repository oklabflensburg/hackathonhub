/**
 * TypeScript Typen für Team-Einladungen
 * Diese Typen werden von den Composables und Komponenten verwendet.
 */

export type InvitationStatus = 'pending' | 'accepted' | 'declined' | 'cancelled'

export interface TeamInvitation {
  id: number
  team_id: number
  invited_user_id: number
  inviter_id: number
  status: InvitationStatus
  created_at: string
  updated_at: string
  invited_user?: {
    id: number
    username: string
    name?: string
    avatar_url?: string
  }
  inviter?: {
    id: number
    username: string
    avatar_url?: string
  }
  team?: {
    id: number
    name: string
    hackathon?: {
      id: number
      name: string
    }
  }
}

export interface UserSearchResult {
  id: number
  username: string
  name?: string
  avatar_url?: string
  email?: string
  is_member?: boolean
}

export interface UseTeamInvitationsOptions {
  teamId: number | Ref<number>
  autoFetch?: boolean
  pollInterval?: number // für real-time updates in Millisekunden
}

export interface UseUserSearchOptions {
  debounceMs?: number
  minQueryLength?: number
  excludeUserIds?: number[]
}

export interface InvitationItemProps {
  invitation: TeamInvitation
  showCancelButton?: boolean
  showInviter?: boolean
  showTeamInfo?: boolean
  showStatus?: boolean
  formatDate?: (dateString: string) => string
  labels?: {
    pending?: string
    invited?: string
    by?: string
    cancel?: string
    cancelling?: string
    unknownUser?: string
    unknownUserInitial?: string
    teamLabel?: string
  }
}

export interface InviteUserFormProps {
  teamId: number
  maxMembers?: number
  currentMemberCount?: number
  disabled?: boolean
  placeholder?: string
  buttonLabel?: string
  helpText?: string
  showMemberCount?: boolean
  showTitle?: boolean
  showHelpText?: boolean
  excludeUserIds?: number[]
}

export interface UserSearchInputProps {
  modelValue: string
  suggestions: UserSearchResult[]
  loading?: boolean
  placeholder?: string
  minChars?: number
  maxSuggestions?: number
  disabled?: boolean
  excludeUserIds?: number[]
}

export interface TeamInvitationsProps {
  teamId: number
  isTeamOwner: boolean
  showHeader?: boolean
  showEmptyState?: boolean
  showLoadingState?: boolean
  showErrorState?: boolean
  autoLoad?: boolean
  pollInterval?: number
  maxVisible?: number
  labels?: {
    title?: string
    pending?: string
    emptyTitle?: string
    emptyDescription?: string
    loading?: string
    error?: string
    retry?: string
  }
}

export interface TeamInviteSectionProps {
  teamId: number
  isTeamOwner: boolean
  isTeamFull: boolean
  currentMemberCount?: number
  maxMembers?: number
  showHelpText?: boolean
  showMemberCount?: boolean
  disabled?: boolean
  excludeUserIds?: number[]
  labels?: {
    title?: string
    placeholder?: string
    button?: string
    helpText?: string
    memberCount?: string
    teamFull?: string
    teamFullDescription?: string
  }
}

// Hilfsfunktionen
export function formatInvitationDate(dateString: string): string {
  try {
    return new Date(dateString).toLocaleDateString()
  } catch {
    return dateString
  }
}

export function getInvitationStatusColor(status: InvitationStatus): string {
  switch (status) {
    case 'pending': return 'warning'
    case 'accepted': return 'success'
    case 'declined': return 'error'
    case 'cancelled': return 'neutral'
    default: return 'neutral'
  }
}

export function getInvitationStatusLabel(status: InvitationStatus, t?: (key: string) => string): string {
  const defaultLabels = {
    pending: 'Pending',
    accepted: 'Accepted',
    declined: 'Declined',
    cancelled: 'Cancelled'
  }
  
  if (t) {
    return t(`teams.invitationStatus.${status}`) || defaultLabels[status]
  }
  
  return defaultLabels[status]
}