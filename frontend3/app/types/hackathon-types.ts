/**
 * Hackathon TypeScript interfaces for atomic design refactoring
 */

export interface Prize {
  name: string
  description: string
  value: string
}

export interface Organizer {
  name: string
  role: string
}

export interface Hackathon {
  id: number
  name: string
  description: string
  start_date: string
  end_date: string
  location: string
  image_url: string
  status: 'upcoming' | 'active' | 'completed'
  is_active: boolean
  participant_count: number
  view_count: number
  project_count: number
  registration_deadline: string
  prizes: Prize[]
  rules: string
  organizers: Organizer[]
  prize_pool: string
  created_at: string
  updated_at: string
}

export interface HackathonFormData {
  name: string
  description: string
  start_date: string
  end_date: string
  location: string
  image_url: string
  prizes: Prize[]
  rules: string
  organizers: Organizer[]
  prize_pool: string
}

export interface HackathonFilters {
  status?: 'all' | 'upcoming' | 'active' | 'completed'
  search?: string
  sortBy?: 'newest' | 'popular' | 'upcoming' | 'active'
}

export interface HackathonListCardProps {
  hackathon: Hackathon
  showStatus?: boolean
  showActions?: boolean
  compact?: boolean
}

export interface HackathonHeroProps {
  hackathon: Hackathon
  formatDateTime: (dateString: string) => string
  virtualLabel: string
}

export interface HackathonDescriptionProps {
  title: string
  description: string
}

export interface PrizeListProps {
  title: string
  prizes: Prize[]
}

export interface RulesSectionProps {
  title: string
  rules: string
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
  }
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
}

export interface ParticipantListProps {
  title: string
  teams: any[]
  loading: boolean
  error: string | null
  requiresAuth: boolean
  onRetry: () => void
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
}