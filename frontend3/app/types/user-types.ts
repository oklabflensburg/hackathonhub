/**
 * Benutzer-bezogene TypeScript Interfaces und Typen
 */

import type { Project } from './project-types'
import type { Team } from './team-types'
import type { Hackathon } from './hackathon-types'

export interface User {
  id: number
  username: string
  email: string
  name?: string
  avatarUrl?: string
  bio?: string
  location?: string
  company?: string
  githubId?: number
  googleId?: string
  emailVerified: boolean
  authMethod?: string
  lastLogin?: string
  createdAt: string
  updatedAt?: string
  // Optional social media usernames (not provided by backend but used by frontend components)
  githubUsername?: string
  twitterUsername?: string
  website?: string
}

export interface UserProfile extends User {
  stats?: UserStats
  teams?: Team[]
  projects?: Project[]
  hackathons?: Hackathon[]
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