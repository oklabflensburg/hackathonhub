/**
 * Hackathon TypeScript interfaces for atomic design refactoring
 * Updated to use consistent camelCase and string IDs
 */

import type { Ref } from 'vue'

// ==================== ENUMS ====================

/**
 * Hackathon status enum
 */
export enum HackathonStatus {
  UPCOMING = 'upcoming',
  ACTIVE = 'active',
  COMPLETED = 'completed',
  DRAFT = 'draft',
  CANCELLED = 'cancelled'
}

/**
 * Hackathon sort options
 */
export enum HackathonSortOption {
  NEWEST = 'newest',
  OLDEST = 'oldest',
  UPCOMING = 'upcoming',
  ACTIVE = 'active',
  POPULAR = 'popular',
  NAME_ASC = 'name_asc',
  NAME_DESC = 'name_desc',
  START_DATE_ASC = 'start_date_asc',
  START_DATE_DESC = 'start_date_desc'
}

/**
 * Hackathon filter options
 */
export enum HackathonFilterOption {
  ALL = 'all',
  UPCOMING = 'upcoming',
  ACTIVE = 'active',
  COMPLETED = 'completed',
  DRAFT = 'draft',
  CANCELLED = 'cancelled',
  HAS_OPEN_REGISTRATION = 'has_open_registration',
  HAS_PRIZES = 'has_prizes',
  VIRTUAL = 'virtual',
  IN_PERSON = 'in_person'
}

// ==================== INTERFACES ====================

export interface Prize {
  name: string
  description: string
  value: string
}

export interface Organizer {
  name: string
  role: string
  avatarUrl?: string | null
  email?: string | null
}

export interface Hackathon {
  id: string
  name: string
  description: string
  shortDescription?: string | null
  startDate: string
  endDate: string
  location: string
  imageUrl: string | null
  bannerUrl?: string | null
  status: HackathonStatus
  isActive: boolean
  participantCount: number
  viewCount: number
  projectCount: number
  registrationDeadline: string | null
  prizes: Prize[]
  rules: string
  organizers: Organizer[]
  prizePool: string | null
  createdAt: string
  updatedAt: string
  tags: string[]
  websiteUrl?: string | null
  contactEmail?: string | null
  maxParticipants?: number | null
  isVirtual: boolean
  timezone?: string | null
  slug?: string
  stats?: HackathonStats
  // Geo coordinates (optional)
  latitude?: number | null
  longitude?: number | null
  // Owner reference (optional)
  ownerId?: number | null
}

export interface HackathonStats {
  teamCount: number
  projectCount: number
  participantCount: number
  averageTeamSize: number
  prizeCount: number
  submissionCount: number
  lastActivityAt: string | null
}

export interface HackathonFormData {
  name: string
  description: string
  shortDescription?: string | null
  startDate: string
  endDate: string
  location: string
  imageUrl?: string | null
  bannerUrl?: string | null
  prizes: Prize[]
  rules: string
  organizers: Organizer[]
  prizePool?: string | null
  tags?: string[]
  websiteUrl?: string | null
  contactEmail?: string | null
  maxParticipants?: number | null
  isVirtual: boolean
  timezone?: string | null
  registrationDeadline?: string | null
}

export interface HackathonFilters {
  status?: HackathonStatus | 'all'
  search?: string
  sortBy?: HackathonSortOption
  tags?: string[]
  location?: string
  isVirtual?: boolean | null
  hasPrizes?: boolean | null
  hasOpenRegistration?: boolean | null
  dateRange?: {
    start?: string
    end?: string
  }
}

export interface HackathonListCardProps {
  hackathon: Hackathon
  showStatus?: boolean
  showActions?: boolean
  compact?: boolean
  showStats?: boolean
  showDescription?: boolean
  maxDescriptionLength?: number
}

export interface HackathonHeroProps {
  hackathon: Hackathon
  formatDateTime: (dateString: string) => string
  virtualLabel: string
  showActions?: boolean
  isRegistered?: boolean
  registrationLoading?: boolean
  onRegister?: () => void
  onUnregister?: () => void
}

export interface HackathonDescriptionProps {
  title: string
  description: string
  maxLength?: number
  expandable?: boolean
}

export interface PrizeListProps {
  title: string
  prizes: Prize[]
  showValue?: boolean
  compact?: boolean
}

export interface RulesSectionProps {
  title: string
  rules: string
  expandable?: boolean
  maxHeight?: string
}

export interface HackathonStatsProps {
  hackathon: Hackathon
  title: string
  formatDateTime: (dateString: string) => string
  labels: {
    status: string
    participants: string
    views: string
    projects: string
    registrationDeadline: string
    teams: string
    prizes: string
  }
  showDetailedStats?: boolean
}

export interface HackathonActionsProps {
  hackathon: Hackathon
  isRegistered: boolean
  isHackathonOwner: boolean
  registrationLoading: boolean
  onRegister: () => void
  onUnregister: () => void
  onEdit: () => void
  onDelete: () => void
  onShare?: () => void
  disabled?: boolean
}

export interface ParticipantListProps {
  title: string
  teams: any[]
  loading: boolean
  error: string | null
  requiresAuth: boolean
  onRetry: () => void
  emptyMessage?: string
  showSearch?: boolean
}

export interface HackathonProjectCardProps {
  project: any
  canEdit: boolean
  labels: {
    votes: string
    comments: string
    views: string
    edit: string
    view: string
  }
  onEdit: () => void
  onView: () => void
  variant?: 'default' | 'compact' | 'featured'
}

// ==================== COMPOSABLE RETURN TYPES ====================

/**
 * UseHackathons composable return type
 */
export interface UseHackathonsReturn {
  hackathons: Ref<Hackathon[]>
  loading: Ref<boolean>
  error: Ref<string | null>
  totalCount: Ref<number>
  page: Ref<number>
  pageSize: Ref<number>
  searchQuery: Ref<string>
  selectedFilters: Ref<Partial<HackathonFilters>>
  sortOption: Ref<HackathonSortOption>
  
  fetchHackathons: (options?: HackathonSearchOptions) => Promise<void>
  fetchHackathon: (hackathonId: string) => Promise<Hackathon | null>
  createHackathon: (data: HackathonFormData) => Promise<Hackathon | null>
  updateHackathon: (hackathonId: string, data: Partial<HackathonFormData>) => Promise<Hackathon | null>
  deleteHackathon: (hackathonId: string) => Promise<boolean>
  registerForHackathon: (hackathonId: string) => Promise<boolean>
  unregisterFromHackathon: (hackathonId: string) => Promise<boolean>
  resetFilters: () => void
  resetSearch: () => void
}

/**
 * Hackathon search and filter options
 */
export interface HackathonSearchOptions {
  query?: string
  page?: number
  pageSize?: number
  sortBy?: HackathonSortOption
  filters?: Partial<HackathonFilters>
  userId?: string | null
}

/**
 * Hackathon pagination response
 */
export interface HackathonPaginationResponse {
  hackathons: Hackathon[]
  totalCount: number
  page: number
  pageSize: number
  totalPages: number
}

// ==================== API-SPECIFIC TYPES ====================

/**
 * API-specific types for useHackathons composable
 */

export interface ApiHackathon {
  id: number
  name: string
  description: string
  start_date: string
  end_date: string
  location: string
  latitude?: number
  longitude?: number
  website?: string
  image_url?: string
  banner_path?: string
  participant_count: number
  view_count: number
  project_count: number
  is_active: boolean
  max_participants?: number
  registration_open: boolean
  prizes?: string
  rules?: string
  organizers?: string
  prize_pool?: string
  owner_id?: number
  created_at: string
  owner?: any
}

export interface ApiHackathonCreateData {
  name: string
  description: string
  start_date: string
  end_date: string
  location: string
  latitude?: number
  longitude?: number
  website?: string
  image_url?: string
  banner_path?: string
  participant_count?: number
  view_count?: number
  project_count?: number
  is_active?: boolean
  max_participants?: number
  registration_open?: boolean
  prizes?: string
  rules?: string
  organizers?: string
  prize_pool?: string
}

export interface ApiHackathonUpdateData {
  name?: string
  description?: string
  start_date?: string
  end_date?: string
  location?: string
  latitude?: number
  longitude?: number
  website?: string
  image_url?: string
  banner_path?: string
  participant_count?: number
  view_count?: number
  project_count?: number
  is_active?: boolean
  max_participants?: number
  registration_open?: boolean
  prizes?: string
  rules?: string
  organizers?: string
  prize_pool?: string
}

export interface ApiHackathonRegistration {
  id: number
  user_id: number
  hackathon_id: number
  status: string
  registered_at: string
  user?: any
  hackathon?: any
}

export interface ApiHackathonRegistrationStatus {
  is_registered: boolean
  hackathon_id: number
  user_id?: number
  registration_id?: number
  status?: string
  registered_at?: string
}

/**
 * Frontend-specific types (camelCase, string IDs)
 */
export interface HackathonCreateData {
  name: string
  description: string
  startDate: string
  endDate: string
  location: string
  latitude?: number
  longitude?: number
  website?: string
  imageUrl?: string
  bannerPath?: string
  participantCount?: number
  viewCount?: number
  projectCount?: number
  isActive?: boolean
  maxParticipants?: number
  registrationOpen?: boolean
  prizes?: string
  rules?: string
  organizers?: string
  prizePool?: string
}

export interface HackathonUpdateData {
  name?: string
  description?: string
  startDate?: string
  endDate?: string
  location?: string
  latitude?: number
  longitude?: number
  website?: string
  imageUrl?: string
  bannerPath?: string
  participantCount?: number
  viewCount?: number
  projectCount?: number
  isActive?: boolean
  maxParticipants?: number
  registrationOpen?: boolean
  prizes?: string
  rules?: string
  organizers?: string
  prizePool?: string
}

export interface HackathonRegistration {
  id: string
  userId: string
  hackathonId: string
  status: string
  registeredAt: string
  user?: any
  hackathon?: any
}

export interface HackathonRegistrationStatus {
  isRegistered: boolean
  hackathonId: string
  userId?: string
  registrationId?: string
  status?: string
  registeredAt?: string
}

// ==================== UTILITY TYPES ====================

/**
 * Hackathon card header props
 */
export interface HackathonCardHeaderProps {
  hackathon: Hackathon
  showActions?: boolean
  compact?: boolean
}

/**
 * Hackathon card content props
 */
export interface HackathonCardContentProps {
  hackathon: Hackathon
  showDescription?: boolean
  showStats?: boolean
  maxDescriptionLength?: number
}

/**
 * Hackathon card footer props
 */
export interface HackathonCardFooterProps {
  hackathon: Hackathon
  userId?: string | null
  showParticipantCount?: boolean
  showRegistrationButton?: boolean
  showStatusBadge?: boolean
}

/**
 * Hackathon status badge props
 */
export interface HackathonStatusBadgeProps {
  status: HackathonStatus
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
  showIcon?: boolean
}

/**
 * Hackathon registration button props
 */
export interface HackathonRegistrationButtonProps {
  hackathon: Hackathon
  isRegistered?: boolean
  loading?: boolean
  disabled?: boolean
  onRegister?: () => void
  onUnregister?: () => void
}

// ==================== UTILITY CONSTANTS ====================

/**
 * Hackathon status colors mapping
 */
export const HACKATHON_STATUS_COLORS: Record<HackathonStatus, string> = {
  [HackathonStatus.UPCOMING]: 'blue',
  [HackathonStatus.ACTIVE]: 'green',
  [HackathonStatus.COMPLETED]: 'gray',
  [HackathonStatus.DRAFT]: 'yellow',
  [HackathonStatus.CANCELLED]: 'red'
}

/**
 * Hackathon status labels
 */
export const HACKATHON_STATUS_LABELS: Record<HackathonStatus, string> = {
  [HackathonStatus.UPCOMING]: 'Bevorstehend',
  [HackathonStatus.ACTIVE]: 'Aktiv',
  [HackathonStatus.COMPLETED]: 'Abgeschlossen',
  [HackathonStatus.DRAFT]: 'Entwurf',
  [HackathonStatus.CANCELLED]: 'Abgesagt'
}

/**
 * Hackathon status icons
 */
export const HACKATHON_STATUS_ICONS: Record<HackathonStatus, string> = {
  [HackathonStatus.UPCOMING]: 'i-heroicons-calendar',
  [HackathonStatus.ACTIVE]: 'i-heroicons-play',
  [HackathonStatus.COMPLETED]: 'i-heroicons-check-circle',
  [HackathonStatus.DRAFT]: 'i-heroicons-document-text',
  [HackathonStatus.CANCELLED]: 'i-heroicons-x-circle'
}