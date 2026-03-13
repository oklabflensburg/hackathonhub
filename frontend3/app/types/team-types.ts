/**
 * Team TypeScript Types for Atomic Design Components
 * 
 * This file defines all TypeScript interfaces and enums for team components
 * Used across atoms, molecules, organisms, templates, and composables
 */

// ==================== ENUMS ====================

/**
 * Team roles within a team
 */
export enum TeamRole {
  OWNER = 'owner',
  ADMIN = 'admin',
  MEMBER = 'member',
  PENDING = 'pending'
}

/**
 * Team status
 */
export enum TeamStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  ARCHIVED = 'archived',
  DELETED = 'deleted'
}

/**
 * Team visibility
 */
export enum TeamVisibility {
  PUBLIC = 'public',
  PRIVATE = 'private'
}

/**
 * Team invitation status
 */
export enum TeamInvitationStatus {
  PENDING = 'pending',
  ACCEPTED = 'accepted',
  REJECTED = 'rejected',
  EXPIRED = 'expired'
}

/**
 * Team sort options
 */
export enum TeamSortOption {
  NAME_ASC = 'name_asc',
  NAME_DESC = 'name_desc',
  CREATED_AT_ASC = 'created_at_asc',
  CREATED_AT_DESC = 'created_at_desc',
  MEMBER_COUNT_ASC = 'member_count_asc',
  MEMBER_COUNT_DESC = 'member_count_desc',
  PROJECT_COUNT_ASC = 'project_count_asc',
  PROJECT_COUNT_DESC = 'project_count_desc'
}

/**
 * Team filter options
 */
export enum TeamFilterOption {
  ALL = 'all',
  PUBLIC = 'public',
  PRIVATE = 'private',
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  HAS_OPEN_SLOTS = 'has_open_slots',
  NEEDS_MEMBERS = 'needs_members'
}

// ==================== INTERFACES ====================

/**
 * Base team interface
 */
export interface Team {
  id: string
  name: string
  description: string | null
  slug: string
  avatarUrl: string | null
  bannerUrl: string | null
  visibility: TeamVisibility
  status: TeamStatus
  maxMembers: number | null
  createdAt: string
  updatedAt: string
  createdBy: string
  hackathonId: string | null
  tags: string[]
  stats?: TeamStats
}

/**
 * Team statistics
 */
export interface TeamStats {
  memberCount: number
  projectCount: number
  activeProjectCount: number
  completedProjectCount: number
  totalVotes: number
  totalComments: number
  averageRating: number | null
  lastActivityAt: string | null
  viewCount: number
  engagementScore: number
  engagementLevel: 'low' | 'medium' | 'high'
}

/**
 * Team member interface
 */
export interface TeamMember {
  id: string
  userId: string
  teamId: string
  role: TeamRole
  joinedAt: string
  user?: TeamMemberUser
}

/**
 * User information for team members
 */
export interface TeamMemberUser {
  id: string
  username: string
  displayName: string | null
  display_name?: string | null
  avatarUrl: string | null
  avatar_url?: string | null
  email: string | null
  bio: string | null
  skills: string[]
}

/**
 * Team invitation interface
 */
export interface TeamInvitation {
  id: string
  teamId: string
  invitedUserId: string | null
  invitedEmail: string | null
  invitedByUserId: string
  role: TeamRole
  status: TeamInvitationStatus
  message: string | null
  expiresAt: string
  createdAt: string
  updatedAt: string
  team?: Team
  invitedByUser?: TeamMemberUser
  invitedUser?: TeamMemberUser
}

/**
 * Team creation/update payload
 */
export interface TeamCreateUpdatePayload {
  name: string
  description?: string | null
  visibility: TeamVisibility
  maxMembers?: number | null
  hackathonId?: string | null
  tags?: string[]
}

/**
 * Team creation data (alias for TeamCreateUpdatePayload)
 */
export type TeamCreateData = TeamCreateUpdatePayload

/**
 * Team update data (alias for TeamCreateUpdatePayload)
 */
export type TeamUpdateData = Partial<TeamCreateUpdatePayload>

/**
 * Team invitation creation data
 */
export interface TeamInvitationCreateData {
  email?: string
  userId?: string
  role: TeamRole
  message?: string | null
}

/**
 * Team member role type (alias for TeamRole)
 */
export type TeamMemberRole = TeamRole

/**
 * Team invitation payload
 */
export interface TeamInvitationPayload {
  email?: string
  userId?: string
  role: TeamRole
  message?: string | null
}

/**
 * Team member update payload
 */
export interface TeamMemberUpdatePayload {
  role: TeamRole
}

/**
 * Team filter state
 */
export interface TeamFilterState {
  visibility: TeamVisibility | 'all'
  status: TeamStatus | 'all'
  hasOpenSlots: boolean | null
  needsMembers: boolean | null
  tags: string[]
  hackathonId: string | null
}

/**
 * Team search and filter options
 */
export interface TeamSearchFilterOptions {
  query?: string
  page?: number
  pageSize?: number
  sortBy?: TeamSortOption
  filters?: Partial<TeamFilterState>
  hackathonId?: string | null
  userId?: string | null
}

/**
 * Team pagination response
 */
export interface TeamPaginationResponse {
  teams: Team[]
  totalCount: number
  page: number
  pageSize: number
  totalPages: number
}

/**
 * Team list props for components
 */
export interface TeamListProps {
  teams: Team[]
  loading?: boolean
  error?: string | null
  emptyMessage?: string
  userId?: string | null
  compact?: boolean
  showActions?: boolean
}

/**
 * Team card props for components
 */
export interface TeamCardProps {
  team: Team
  userId?: string | null
  compact?: boolean
  showActions?: boolean
  showDescription?: boolean
  showStats?: boolean
  maxDescriptionLength?: number
}

/**
 * Team details props for components
 */
export interface TeamDetailsProps {
  team: Team
  members: TeamMember[]
  invitations: TeamInvitation[]
  loading?: boolean
  error?: string | null
  userId?: string | null
  showActions?: boolean
}

/**
 * Team member item props
 */
export interface TeamMemberItemProps {
  member: TeamMember
  team: Team
  currentUserId?: string | null
  showActions?: boolean
  onRoleUpdate?: (memberId: string, role: TeamRole) => void
  onRemove?: (memberId: string) => void
}

/**
 * Team invitation item props
 */
export interface TeamInvitationItemProps {
  invitation: TeamInvitation
  team: Team
  currentUserId?: string | null
  showActions?: boolean
  onAccept?: (invitationId: string) => void
  onReject?: (invitationId: string) => void
  onResend?: (invitationId: string) => void
  onCancel?: (invitationId: string) => void
}

/**
 * Team badge props
 */
export interface TeamBadgeProps {
  status?: TeamStatus
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
}

/**
 * Team visibility badge props
 */
export interface TeamVisibilityBadgeProps {
  visibility: TeamVisibility
  size?: 'sm' | 'md' | 'lg'
}

/**
 * Team role badge props
 */
export interface TeamRoleBadgeProps {
  role: TeamRole
  size?: 'sm' | 'md' | 'lg'
}

/**
 * Team member avatar props
 */
export interface TeamMemberAvatarProps {
  member: TeamMember | TeamMemberUser
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  showName?: boolean
  showRole?: boolean
}

/**
 * Team join button props
 */
export interface TeamJoinButtonProps {
  team: Team
  userId?: string | null
  isMember?: boolean
  loading?: boolean
  onJoin?: (teamId: string) => void
  onLeave?: (teamId: string) => void
}

/**
 * Team invite button props
 */
export interface TeamInviteButtonProps {
  team: Team
  disabled?: boolean
  loading?: boolean
  onInvite?: (teamId: string) => void
}

/**
 * Team settings button props
 */
export interface TeamSettingsButtonProps {
  team: Team
  disabled?: boolean
  loading?: boolean
  onSettings?: (teamId: string) => void
}

// ==================== UTILITY TYPES ====================

/**
 * Team card header props
 */
export interface TeamCardHeaderProps {
  team: Team
  showActions?: boolean
  compact?: boolean
}

/**
 * Team card content props
 */
export interface TeamCardContentProps {
  team: Team
  showDescription?: boolean
  showStats?: boolean
  maxDescriptionLength?: number
}

/**
 * Team card footer props
 */
export interface TeamCardFooterProps {
  team: Team
  userId?: string | null
  showMemberCount?: boolean
  showJoinButton?: boolean
  showViewCount?: boolean
  showEngagementLevel?: boolean
}

/**
 * Teams page template props
 */
export interface TeamsPageTemplateProps {
  teams: Team[]
  userId?: string | null
  loading?: boolean
  error?: string | null
  totalCount?: number
  page?: number
  pageSize?: number
  searchQuery?: string
  selectedFilters?: Partial<TeamFilterState>
  onSearch?: (query: string) => void
  onFilterChange?: (filters: Partial<TeamFilterState>) => void
  onSortChange?: (sortOption: TeamSortOption) => void
  onPageChange?: (page: number) => void
  onCreateTeam?: () => void
}

/**
 * Team details template props
 */
export interface TeamDetailsTemplateProps {
  team: Team
  members: TeamMember[]
  invitations: TeamInvitation[]
  userId?: string | null
  loading?: boolean
  error?: string | null
  onUpdateTeam?: (teamId: string, data: TeamCreateUpdatePayload) => void
  onDeleteTeam?: (teamId: string) => void
  onInviteMember?: (teamId: string, data: TeamInvitationPayload) => void
  onRemoveMember?: (teamId: string, memberId: string) => void
  onUpdateMemberRole?: (teamId: string, memberId: string, role: TeamRole) => void
  onAcceptInvitation?: (invitationId: string) => void
  onRejectInvitation?: (invitationId: string) => void
  onCancelInvitation?: (invitationId: string) => void
}

// ==================== COMPOSABLE RETURN TYPES ====================

/**
 * UseTeams composable return type
 */
export interface UseTeamsReturn {
  teams: Ref<Team[]>
  loading: Ref<boolean>
  error: Ref<string | null>
  totalCount: Ref<number>
  page: Ref<number>
  pageSize: Ref<number>
  searchQuery: Ref<string>
  selectedFilters: Ref<Partial<TeamFilterState>>
  sortOption: Ref<TeamSortOption>
  
  fetchTeams: (options?: TeamSearchFilterOptions) => Promise<void>
  fetchTeam: (teamId: string) => Promise<Team | null>
  createTeam: (data: TeamCreateUpdatePayload) => Promise<Team | null>
  updateTeam: (teamId: string, data: TeamCreateUpdatePayload) => Promise<Team | null>
  deleteTeam: (teamId: string) => Promise<boolean>
  joinTeam: (teamId: string) => Promise<boolean>
  leaveTeam: (teamId: string) => Promise<boolean>
  resetFilters: () => void
  resetSearch: () => void
  fetchTeamMembers: (teamId: string) => Promise<void>
  fetchTeamInvitations: (teamId: string) => Promise<void>
  addMember: (teamId: string, userId: string, role?: TeamRole) => Promise<boolean>
  removeMember: (teamId: string, memberId: string) => Promise<boolean>
  updateMemberRole: (teamId: string, memberId: string, role: TeamRole) => Promise<boolean>
  isUserMember: (teamId: string, userId: string) => boolean
  getUserRole: (teamId: string, userId: string) => TeamRole | null
}

/**
 * UseTeamMembers composable return type
 */
export interface UseTeamMembersReturn {
  members: Ref<TeamMember[]>
  loading: Ref<boolean>
  error: Ref<string | null>
  
  fetchMembers: (teamId: string) => Promise<void>
  addMember: (teamId: string, userId: string, role?: TeamRole) => Promise<boolean>
  removeMember: (teamId: string, memberId: string) => Promise<boolean>
  updateMemberRole: (teamId: string, memberId: string, role: TeamRole) => Promise<boolean>
  isUserMember: (teamId: string, userId: string) => boolean
  getUserRole: (teamId: string, userId: string) => TeamRole | null
}

/**
 * UseTeamInvitations composable return type
 */
export interface UseTeamInvitationsReturn {
  invitations: Ref<TeamInvitation[]>
  loading: Ref<boolean>
  error: Ref<string | null>
  
  fetchInvitations: (teamId: string) => Promise<void>
  sendInvitation: (teamId: string, data: TeamInvitationPayload) => Promise<boolean>
  acceptInvitation: (invitationId: string) => Promise<boolean>
  rejectInvitation: (invitationId: string) => Promise<boolean>
  cancelInvitation: (invitationId: string) => Promise<boolean>
  resendInvitation: (invitationId: string) => Promise<boolean>
}

// ==================== HELPER FUNCTIONS ====================

/**
 * Check if a team has open slots for new members
 */
export function teamHasOpenSlots(team: Team): boolean {
  if (!team.maxMembers || !team.stats?.memberCount) return true
  return team.stats.memberCount < team.maxMembers
}

/**
 * Check if a team needs more members
 */
export function teamNeedsMembers(team: Team): boolean {
  if (!team.maxMembers || !team.stats?.memberCount) return false
  const ratio = team.stats.memberCount / team.maxMembers
  return ratio < 0.5 // Less than 50% filled
}

/**
 * Get team status color
 */
export function getTeamStatusColor(status?: TeamStatus): 'green' | 'gray' | 'orange' | 'red' {
  const colors: Record<TeamStatus, 'green' | 'gray' | 'orange' | 'red'> = {
    [TeamStatus.ACTIVE]: 'green',
    [TeamStatus.INACTIVE]: 'gray',
    [TeamStatus.ARCHIVED]: 'orange',
    [TeamStatus.DELETED]: 'red'
  }
  return status ? colors[status] || 'gray' : 'gray'
}

/**
 * Get team visibility color
 */
export function getTeamVisibilityColor(visibility: TeamVisibility): string {
  const colors: Record<TeamVisibility, string> = {
    [TeamVisibility.PUBLIC]: 'blue',
    [TeamVisibility.PRIVATE]: 'purple'
  }
  return colors[visibility] || 'gray'
}

/**
 * Get team role color
 */
export function getTeamRoleColor(role: TeamRole): 'red' | 'orange' | 'green' | 'gray' {
  const colors: Record<TeamRole, 'red' | 'orange' | 'green' | 'gray'> = {
    [TeamRole.OWNER]: 'red',
    [TeamRole.ADMIN]: 'orange',
    [TeamRole.MEMBER]: 'green',
    [TeamRole.PENDING]: 'gray'
  }
  return colors[role] || 'gray'
}

/**
 * Format team member count
 */
export function formatTeamMemberCount(team: Team): string {
  if (!team.stats?.memberCount) return '0 members'
  const max = team.maxMembers
  return max ? `${team.stats.memberCount}/${max} members` : `${team.stats.memberCount} members`
}

/**
 * Check if user can manage team
 */
export function canUserManageTeam(userId: string | null, team: Team, members: TeamMember[]): boolean {
  if (!userId) return false
  const member = members.find(m => m.userId === userId)
  return member?.role === TeamRole.OWNER || member?.role === TeamRole.ADMIN
}

/**
 * Check if user can edit team
 */
export function canUserEditTeam(userId: string | null, team: Team, members: TeamMember[]): boolean {
  if (!userId) return false
  const member = members.find(m => m.userId === userId)
  return member?.role === TeamRole.OWNER
}

// ==================== ATOM COMPONENT TYPES ====================

/**
 * Team join button props for atom component
 */
export interface TeamJoinButtonAtomProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'success'
  size?: 'sm' | 'md' | 'lg' | 'xl'
  disabled?: boolean
  loading?: boolean
  fullWidth?: boolean
  icon?: boolean
  label?: string
  loadingText?: string
  ariaLabel?: string
}

/**
 * Team join button emits for atom component
 */
export interface TeamJoinButtonAtomEmits {
  (e: 'click', event: MouseEvent): void
  (e: 'join'): void
}

/**
 * Team invitation status props for atom component
 */
export interface TeamInvitationStatusAtomProps {
  status: TeamInvitationStatus
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
  showIcon?: boolean
}

/**
 * Team invitation status emits for atom component
 */
export interface TeamInvitationStatusAtomEmits {
  (e: 'click', event: MouseEvent): void
}

/**
 * Team member list props for molecule component
 */
export interface TeamMemberListProps {
  members: TeamMember[]
  team: Team
  currentUserId?: string | null
  showActions?: boolean
  maxVisible?: number
  compact?: boolean
  loading?: boolean
}

/**
 * Team member list emits for molecule component
 */
export interface TeamMemberListEmits {
  (e: 'role-update', memberId: string, role: TeamRole): void
  (e: 'remove', memberId: string): void
  (e: 'view-profile', memberId: string): void
}

/**
 * Team invitation card props for molecule component
 */
export interface TeamInvitationCardProps {
  invitation: TeamInvitation
  team: Team
  currentUserId?: string | null
  showActions?: boolean
  compact?: boolean
}

/**
 * Team invitation card emits for molecule component
 */
export interface TeamInvitationCardEmits {
  (e: 'accept', invitationId: string): void
  (e: 'reject', invitationId: string): void
  (e: 'resend', invitationId: string): void
  (e: 'cancel', invitationId: string): void
  (e: 'view-profile', userId: string): void
}
