/**
 * TypeScript-Typen für Atomic Design Projekt-Komponenten
 * Definiert alle Typen für Projekt-bezogene Komponenten
 */

/**
 * Benutzer (vereinfachte Version für Projekt-Komponenten)
 */
export interface User {
  id: string
  username: string
  email?: string
  avatarUrl?: string
  role?: string
  bio?: string
  createdAt?: string
}

/**
 * Projekt-Status Enum
 */
export enum ProjectStatus {
  DRAFT = 'draft',
  ACTIVE = 'active',
  COMPLETED = 'completed',
  ARCHIVED = 'archived',
  UNDER_REVIEW = 'under_review',
}

/**
 * Projekt-Visibility Enum
 */
export enum ProjectVisibility {
  PUBLIC = 'public',
  PRIVATE = 'private',
  TEAM_ONLY = 'team_only',
}

/**
 * Projekt-Technologie/Kategorie
 */
export interface ProjectTechnology {
  id: string
  name: string
  slug: string
  color: string
  icon?: string
}

/**
 * Projekt-Tag
 */
export interface ProjectTag {
  id: string
  name: string
  slug: string
  color: string
  description?: string
}

/**
 * Projekt-Team-Mitglied
 */
export interface ProjectTeamMember {
  user: User
  role: 'owner' | 'member' | 'contributor'
  joinedAt: string
}

/**
 * Projekt-Statistiken
 */
export interface ProjectStats {
  views: number
  votes: number
  comments: number
  shares: number
  bookmarks: number
}

/**
 * Projekt-Vote
 */
export interface ProjectVote {
  id: string
  userId: string
  projectId: string
  value: 1 | -1 // Upvote (1) oder Downvote (-1)
  createdAt: string
}

/**
 * Projekt-Kommentar
 */
export interface ProjectComment {
  id: string
  userId: string
  user: User
  content: string
  parentId?: string // Für Threaded Comments
  votes: number
  userVote?: 1 | -1 | null // Aktueller Benutzer-Vote
  createdAt: string
  updatedAt: string
  replies?: ProjectComment[]
}

/**
 * Projekt-Haupt-Interface
 */
export interface Project {
  id: string
  title: string
  slug: string
  description: string
  shortDescription?: string
  content?: string
  status: ProjectStatus
  visibility: ProjectVisibility
  featuredImage?: string
  galleryImages?: string[]
  
  // Metadaten
  createdAt: string
  updatedAt: string
  publishedAt?: string
  deadline?: string
  
  // Beziehungen
  team: ProjectTeamMember[]
  technologies: ProjectTechnology[]
  tags: ProjectTag[]
  hackathonId?: string
  hackathonName?: string
  
  // Statistiken
  stats: ProjectStats
  
  // User-spezifische Daten
  userVote?: 1 | -1 | null
  isBookmarked?: boolean
  isFollowing?: boolean
  
  // SEO
  metaTitle?: string
  metaDescription?: string
  keywords?: string[]
}

/**
 * Projekt-Filter-Optionen
 */
export interface ProjectFilterOptions {
  // Status-Filter
  status?: ProjectStatus[]
  
  // Technologie/Tag-Filter
  technologies?: string[]
  tags?: string[]
  
  // Hackathon-Filter
  hackathonId?: string
  
  // Team-Filter
  teamSize?: {
    min?: number
    max?: number
  }
  
  // Zeit-Filter
  createdAt?: {
    from?: string
    to?: string
  }
  
  // Such-Filter
  search?: string
  
  // Visibility-Filter
  visibility?: ProjectVisibility[]
  
  // Benutzer-spezifische Filter
  userId?: string // Projekte eines bestimmten Benutzers
  teamMemberId?: string // Projekte, bei denen Benutzer Team-Mitglied ist
  bookmarked?: boolean // Nur bookmarkete Projekte
  voted?: 'upvoted' | 'downvoted' // Nur up/downgevotete Projekte
}

/**
 * Projekt-Sortier-Optionen
 */
export enum ProjectSortOption {
  NEWEST = 'newest',
  OLDEST = 'oldest',
  MOST_VIEWED = 'most_viewed',
  MOST_VOTED = 'most_voted',
  MOST_COMMENTED = 'most_commented',
  TRENDING = 'trending',
  DEADLINE = 'deadline',
  ALPHABETICAL = 'alphabetical',
}

/**
 * Projekt-Sortier-Konfiguration
 */
export interface ProjectSortConfig {
  field: ProjectSortOption
  direction: 'asc' | 'desc'
}

/**
 * Projekt-Listen-Konfiguration
 */
export interface ProjectListConfig {
  page: number
  pageSize: number
  filters: ProjectFilterOptions
  sort: ProjectSortConfig
}

/**
 * Projekt-Listen-Antwort
 */
export interface ProjectListResponse {
  projects: Project[]
  total: number
  page: number
  pageSize: number
  totalPages: number
  hasMore: boolean
}

/**
 * Projekt-Karten-Props
 */
export interface ProjectCardProps {
  project: Project
  variant?: 'default' | 'compact' | 'featured'
  showActions?: boolean
  showStats?: boolean
  showTeam?: boolean
  showTechnologies?: boolean
  clickable?: boolean
  loading?: boolean
}

/**
 * Projekt-Status-Badge-Props
 */
export interface ProjectStatusBadgeProps {
  status: ProjectStatus
  size?: 'sm' | 'md' | 'lg'
  variant?: 'solid' | 'outline' | 'soft'
  showLabel?: boolean
  showIcon?: boolean
}

/**
 * Projekt-Tag-Props
 */
export interface ProjectTagProps {
  tag: ProjectTag
  size?: 'sm' | 'md' | 'lg'
  removable?: boolean
  clickable?: boolean
  onRemove?: (tag: ProjectTag) => void
  onClick?: (tag: ProjectTag) => void
}

/**
 * Projekt-Vote-Button-Props
 */
export interface ProjectVoteButtonProps {
  projectId: string
  hasVoted?: boolean
  voteCount: number
  size?: 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'primary' | 'secondary' | 'success' | 'danger'
  disabled?: boolean
  showCount?: boolean
  onVote?: (projectId: string, voteType: 'up' | 'down') => Promise<void> | void
  onUnvote?: (projectId: string) => Promise<void> | void
}

/**
 * Projekt-Comment-Button-Props
 */
export interface ProjectCommentButtonProps {
  projectId: string
  commentCount: number
  size?: 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'primary' | 'secondary' | 'success' | 'danger'
  disabled?: boolean
  showCount?: boolean
  onClick?: (projectId: string) => void
}

/**
 * Projekt-Share-Button-Props
 */
export interface ProjectShareButtonProps {
  project: Project
  size?: 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'primary' | 'secondary' | 'success' | 'danger'
  platforms?: SharePlatform[]
  disabled?: boolean
}

/**
 * Share-Plattformen
 */
export enum SharePlatform {
  TWITTER = 'twitter',
  FACEBOOK = 'facebook',
  LINKEDIN = 'linkedin',
  REDDIT = 'reddit',
  WHATSAPP = 'whatsapp',
  TELEGRAM = 'telegram',
  EMAIL = 'email',
  COPY_LINK = 'copy_link',
}

/**
 * Projekt-Filter-Item-Props
 */
export interface ProjectFilterItemProps {
  filter: {
    id: string
    label: string
    value: any
    type: 'checkbox' | 'radio' | 'range' | 'search'
    options?: Array<{ label: string; value: any; count?: number }>
  }
  selected: boolean
  count?: number
  disabled?: boolean
  onChange: (filterId: string, value: any, selected: boolean) => void
}

/**
 * Projekt-Sort-Option-Props
 */
export interface ProjectSortOptionProps {
  option: {
    id: ProjectSortOption
    label: string
    direction?: 'asc' | 'desc'
  }
  selected: boolean
  onChange: (optionId: ProjectSortOption, direction?: 'asc' | 'desc') => void
}

/**
 * Projekt-Listen-Props
 */
export interface ProjectListProps {
  projects: Project[]
  loading?: boolean
  emptyMessage?: string
  variant?: 'grid' | 'list'
  columns?: number // Für Grid-Variant
  cardVariant?: 'default' | 'compact' | 'featured'
  pagination?: {
    page: number
    pageSize: number
    total: number
    onPageChange: (page: number) => void
  }
}

/**
 * Projekt-Filter-Props
 */
export interface ProjectFiltersProps {
  filters: ProjectFilterOptions
  availableTechnologies: ProjectTechnology[]
  availableTags: ProjectTag[]
  loading?: boolean
  onChange: (filters: ProjectFilterOptions) => void
  onReset?: () => void
}

/**
 * Projekt-Details-Header-Props
 */
export interface ProjectDetailsHeaderProps {
  project: Project
  loading?: boolean
  showActions?: boolean
  onEdit?: () => void
  onDelete?: () => void
  onShare?: () => void
  onBookmark?: (bookmarked: boolean) => void
}

/**
 * Projekt-Details-Sidebar-Props
 */
export interface ProjectDetailsSidebarProps {
  project: Project
  loading?: boolean
  showStats?: boolean
  showTeam?: boolean
  showRelated?: boolean
  onTeamMemberClick?: (member: ProjectTeamMember) => void
}

/**
 * Projekte-Page-Template-Props
 */
export interface ProjectsPageTemplateProps {
  projects: Project[]
  loading?: boolean
  filters: ProjectFilterOptions
  sort: ProjectSortConfig
  pagination: {
    page: number
    pageSize: number
    total: number
  }
  availableTechnologies: ProjectTechnology[]
  availableTags: ProjectTag[]
  onFiltersChange: (filters: ProjectFilterOptions) => void
  onSortChange: (sort: ProjectSortConfig) => void
  onPageChange: (page: number) => void
}

/**
 * Projekt-Details-Template-Props
 */
export interface ProjectDetailsTemplateProps {
  project: Project
  loading?: boolean
  comments: ProjectComment[]
  relatedProjects: Project[]
  onCommentSubmit: (content: string, parentId?: string) => Promise<void>
  onCommentVote: (commentId: string, vote: 1 | -1 | null) => Promise<void>
  onProjectVote: (vote: 1 | -1 | null) => Promise<void>
  onProjectBookmark: (bookmarked: boolean) => Promise<void>
}

/**
 * Utility-Typen für Projekt-Komponenten
 */

// Projekt-Status-Farb-Mapping
export const PROJECT_STATUS_COLORS: Record<ProjectStatus, string> = {
  [ProjectStatus.DRAFT]: 'gray',
  [ProjectStatus.ACTIVE]: 'green',
  [ProjectStatus.COMPLETED]: 'blue',
  [ProjectStatus.ARCHIVED]: 'orange',
  [ProjectStatus.UNDER_REVIEW]: 'yellow',
}

// Projekt-Status-Labels
export const PROJECT_STATUS_LABELS: Record<ProjectStatus, string> = {
  [ProjectStatus.DRAFT]: 'Entwurf',
  [ProjectStatus.ACTIVE]: 'Aktiv',
  [ProjectStatus.COMPLETED]: 'Abgeschlossen',
  [ProjectStatus.ARCHIVED]: 'Archiviert',
  [ProjectStatus.UNDER_REVIEW]: 'In Prüfung',
}

// Projekt-Status-Icons
export const PROJECT_STATUS_ICONS: Record<ProjectStatus, string> = {
  [ProjectStatus.DRAFT]: 'i-heroicons-document-text',
  [ProjectStatus.ACTIVE]: 'i-heroicons-play',
  [ProjectStatus.COMPLETED]: 'i-heroicons-check-circle',
  [ProjectStatus.ARCHIVED]: 'i-heroicons-archive-box',
  [ProjectStatus.UNDER_REVIEW]: 'i-heroicons-clock',
}

// Projekt-Sort-Option-Labels
export const PROJECT_SORT_LABELS: Record<ProjectSortOption, string> = {
  [ProjectSortOption.NEWEST]: 'Neueste',
  [ProjectSortOption.OLDEST]: 'Älteste',
  [ProjectSortOption.MOST_VIEWED]: 'Meist gesehen',
  [ProjectSortOption.MOST_VOTED]: 'Meist gevotet',
  [ProjectSortOption.MOST_COMMENTED]: 'Meist kommentiert',
  [ProjectSortOption.TRENDING]: 'Trending',
  [ProjectSortOption.DEADLINE]: 'Deadline',
  [ProjectSortOption.ALPHABETICAL]: 'Alphabetisch',
}

/**
 * Hilfsfunktionen für Projekt-Typen
 */

// Prüft ob Projekt sichtbar ist für aktuellen Benutzer
export function isProjectVisible(
  project: Project,
  currentUserId?: string,
  isAuthenticated: boolean = false
): boolean {
  if (project.visibility === ProjectVisibility.PUBLIC) {
    return true
  }
  
  if (project.visibility === ProjectVisibility.PRIVATE && currentUserId) {
    // Prüfe ob Benutzer Team-Mitglied ist
    return project.team.some(member => member.user.id === currentUserId)
  }
  
  if (project.visibility === ProjectVisibility.TEAM_ONLY && isAuthenticated) {
    return true
  }
  
  return false
}

// Formatiert Projekt-Statistiken für Anzeige
export function formatProjectStats(stats: ProjectStats): {
  views: string
  votes: string
  comments: string
  shares: string
  bookmarks: string
} {
  const formatNumber = (num: number): string => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`
    }
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`
    }
    return num.toString()
  }
  
  return {
    views: formatNumber(stats.views),
    votes: formatNumber(stats.votes),
    comments: formatNumber(stats.comments),
    shares: formatNumber(stats.shares),
    bookmarks: formatNumber(stats.bookmarks),
  }
}
