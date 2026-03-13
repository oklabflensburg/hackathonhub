/**
 * Benutzer-bezogene TypeScript Interfaces und Typen
 */

import type { Project } from './project-types'
import type { Team } from './team-types'
import type { Hackathon } from './hackathon-types'

export interface User {
  id: number
  github_id?: string
  google_id?: string
  username: string
  avatar_url: string
  email?: string
  email_verified?: boolean
  auth_method?: 'github' | 'google' | 'email'
  created_at: string
  last_login?: string
  name?: string
  bio?: string
  location?: string
  company?: string
  updated_at?: string
  is_admin?: boolean
  role?: string
  roles?: string[]
  permissions?: string[]
  // Extended fields from /api/me (UserWithDetails)
  teams?: Array<{
    id: number
    team_id: number
    user_id: number
    role: 'owner' | 'member'
    joined_at: string
    team?: {
      id: number
      name: string
      description: string
      hackathon_id: number
      max_members: number
      is_open: boolean
      created_by: number
      created_at: string
      member_count?: number
    }
  }>
  projects?: any[]
  votes?: any[]
  comments?: any[]
  hackathon_registrations?: any[]
}

export interface UserProfile extends User {
  stats?: UserStats
  // Note: teams, projects, hackathons are already defined in User interface
  // These are kept for backward compatibility
}

export interface UserStats {
  hackathonsCreated: number
  projectsSubmitted: number
  totalVotes: number
  // Optionale Felder für zukünftige Erweiterungen
  teamCount?: number
  commentCount?: number
  followerCount?: number
  followingCount?: number
  averageRating?: number
  totalPoints?: number
}

export interface UserPreferences {
  emailNotifications: boolean
  pushNotifications: boolean
  language: string
  timezone: string
  theme: 'light' | 'dark' | 'system'
  notifications: {
    projectUpdates: boolean
    teamInvitations: boolean
    hackathonReminders: boolean
    newsletter: boolean
  }
}

export interface UserActivity {
  id: string
  userId: string
  type: UserActivityType
  entityType: 'project' | 'team' | 'hackathon' | 'comment' | 'vote'
  entityId: string
  entityName: string
  createdAt: string
  metadata?: Record<string, any>
}

export interface UserSession {
  id: string
  userId: string
  token: string
  userAgent?: string
  ipAddress?: string
  createdAt: string
  lastActiveAt: string
  expiresAt: string
}

export interface UserNotificationPreference {
  id: string
  userId: string
  type: NotificationType
  email: boolean
  push: boolean
  inApp: boolean
  createdAt: string
  updatedAt: string
}

export type UserRole = string // Backend hat keine festen Rollen, aber möglicherweise in Teams

export type UserActivityType = 
  | 'project_created'
  | 'project_updated'
  | 'team_joined'
  | 'team_created'
  | 'hackathon_registered'
  | 'comment_created'
  | 'vote_cast'
  | 'profile_updated'
  | 'achievement_unlocked'

export interface UserSearchResult {
  id: number
  username: string
  email: string
  name?: string
  avatarUrl?: string
  bio?: string
  location?: string
  emailVerified: boolean
  matchScore: number
}

export interface UserInvitation {
  id: string
  email: string
  invitedByUserId: number
  teamId?: string
  projectId?: string
  hackathonId?: string
  role: string
  status: 'pending' | 'accepted' | 'rejected' | 'expired'
  expiresAt: string
  createdAt: string
  updatedAt: string
}

export interface UserFollow {
  id: string
  followerId: string
  followingId: string
  createdAt: string
}

export interface UserAchievement {
  id: string
  userId: string
  achievementId: string
  name: string
  description: string
  icon: string
  unlockedAt: string
  progress?: number
  totalRequired?: number
}

// Request/Response Types
export interface CreateUserRequest {
  firstName: string
  lastName: string
  email: string
  password: string
  avatarUrl?: string
  bio?: string
  location?: string
  website?: string
}

export interface UpdateUserRequest {
  firstName?: string
  lastName?: string
  email?: string
  avatarUrl?: string
  bio?: string
  location?: string
  website?: string
  language?: string
  timezone?: string
}

export interface UpdateUserPreferencesRequest {
  emailNotifications?: boolean
  pushNotifications?: boolean
  language?: string
  timezone?: string
  theme?: 'light' | 'dark' | 'system'
  notifications?: {
    projectUpdates?: boolean
    teamInvitations?: boolean
    hackathonReminders?: boolean
    newsletter?: boolean
  }
}

export interface ChangePasswordRequest {
  currentPassword: string
  newPassword: string
}

export interface ResetPasswordRequest {
  email: string
  token: string
  newPassword: string
}

export interface UserResponse {
  user: User
  stats?: UserStats
  preferences?: UserPreferences
}

export interface UsersResponse {
  users: User[]
  total: number
  page: number
  pageSize: number
}

export interface UserActivitiesResponse {
  activities: UserActivity[]
  total: number
  page: number
  pageSize: number
}

// Utility Types
export type UserSortField = 
  | 'firstName'
  | 'lastName'
  | 'email'
  | 'createdAt'
  | 'projectCount'
  | 'teamCount'
  | 'hackathonCount'

export interface UserFilter {
  search?: string
  role?: UserRole
  isVerified?: boolean
  isActive?: boolean
  hasTeam?: boolean
  hasProject?: boolean
  location?: string
  createdAtFrom?: string
  createdAtTo?: string
}

// Mock-Daten wurden entfernt, da jetzt echte API-Aufrufe verwendet werden