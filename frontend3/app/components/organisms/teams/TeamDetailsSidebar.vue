<template>
  <aside class="team-details-sidebar" :class="sidebarClasses">
    <!-- Team Avatar -->
    <div class="team-avatar-section mb-6">
      <div class="relative">
        <div class="avatar-container mx-auto">
          <div
            v-if="team.avatarUrl"
            class="team-avatar w-32 h-32 rounded-full mx-auto bg-gray-200 dark:bg-gray-700 bg-cover bg-center"
            :style="{ backgroundImage: `url('${team.avatarUrl}')` }"
          />
          <div
            v-else
            class="team-avatar-placeholder w-32 h-32 rounded-full mx-auto bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center"
          >
            <span class="text-4xl font-bold text-white">
              {{ team.name.charAt(0).toUpperCase() }}
            </span>
          </div>
          
          <!-- Avatar Upload Button -->
          <button
            v-if="canManageTeam"
            type="button"
            class="avatar-upload-button absolute bottom-0 right-0 bg-white dark:bg-gray-800 rounded-full p-2 border border-gray-300 dark:border-gray-600 shadow-sm hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            @click="onAvatarUpload"
          >
            <svg class="h-5 w-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>
        </div>
        
        <div class="team-name text-center mt-4">
          <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">
            {{ team.name }}
          </h2>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {{ team.slug }}
          </p>
        </div>
      </div>
    </div>
    
    <!-- Team Stats -->
    <div class="team-stats-section mb-6">
      <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">
        Team Statistics
      </h3>
      
      <div class="stats-grid grid grid-cols-2 gap-3">
        <!-- Members Stat -->
        <div class="stat-item bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
          <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
            {{ team.stats?.memberCount || 0 }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Members
          </div>
          <div class="stat-progress mt-2">
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5">
              <div
                class="bg-green-500 h-1.5 rounded-full"
                :style="{ width: `${memberProgress}%` }"
              />
            </div>
            <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
              {{ memberProgress }}% of capacity
            </div>
          </div>
        </div>
        
        <!-- Projects Stat -->
        <div class="stat-item bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
          <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
            {{ team.stats?.projectCount || 0 }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Projects
          </div>
          <div class="stat-trend mt-2">
            <div class="flex items-center text-xs text-gray-600 dark:text-gray-400">
              <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <span>Active projects</span>
            </div>
          </div>
        </div>
        
        <!-- Activity Level -->
        <div class="stat-item bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
          <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
            {{ activityLevel }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Activity Level
          </div>
          <div class="stat-rating mt-2">
            <div class="flex items-center">
              <div class="flex">
                <svg
                  v-for="i in 5"
                  :key="i"
                  class="h-4 w-4"
                  :class="i <= activityStars ? 'text-yellow-400' : 'text-gray-300 dark:text-gray-600'"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.922-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Created Date -->
        <div class="stat-item bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
          <div class="stat-value text-lg font-bold text-gray-900 dark:text-gray-100">
            {{ formatDate(team.createdAt) }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Created
          </div>
          <div class="stat-age mt-2 text-xs text-gray-500 dark:text-gray-400">
            {{ teamAge }} old
          </div>
        </div>
      </div>
    </div>
    
    <!-- Team Info -->
    <div class="team-info-section mb-6">
      <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">
        Team Information
      </h3>
      
      <div class="info-list space-y-3">
        <!-- Visibility -->
        <div class="info-item flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-400">
            Visibility
          </span>
          <TeamVisibilityBadge
            :visibility="teamVisibility"
            size="sm"
            :show-label="true"
          />
        </div>
        
        <!-- Status -->
        <div class="info-item flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-400">
            Status
          </span>
          <TeamBadge
            :status="team.status"
            size="sm"
            :show-label="true"
          />
        </div>
        
        <!-- Max Members -->
        <div class="info-item flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-400">
            Max Members
          </span>
          <span class="text-sm font-medium text-gray-900 dark:text-gray-100">
            {{ team.maxMembers || 'Unlimited' }}
          </span>
        </div>
        
        <!-- Hackathon -->
        <div v-if="team.hackathonId" class="info-item flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-400">
            Hackathon
          </span>
          <a
            :href="`/hackathons/${team.hackathonId}`"
            class="text-sm font-medium text-primary-600 dark:text-primary-400 hover:underline"
          >
            View Hackathon
          </a>
        </div>
        
        <!-- Created By -->
        <div class="info-item flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-400">
            Created By
          </span>
          <span class="text-sm font-medium text-gray-900 dark:text-gray-100">
            {{ createdByName }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- Quick Actions -->
    <div v-if="showActions" class="quick-actions-section">
      <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">
        Quick Actions
      </h3>
      
      <div class="actions-list space-y-2">
        <!-- Join/Leave Button -->
        <TeamJoinButton
          v-if="userId && !isMember"
          :team="team"
          :userId="userId"
          :isMember="isMember"
          :isInvited="isInvited"
          size="md"
          variant="primary"
          full-width
          @join="onJoin"
          @leave="onLeave"
        />
        
        <!-- Invite Members -->
        <TeamInviteButton
          v-if="isMember"
          :team="team"
          size="md"
          variant="secondary"
          full-width
          @invite="onInvite"
        />
        
        <!-- Team Settings -->
        <TeamSettingsButton
          v-if="canManageTeam"
          :team="team"
          size="md"
          variant="outline"
          full-width
          @settings="onSettings"
        />
        
        <!-- View Members -->
        <button
          type="button"
          class="w-full inline-flex items-center justify-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          @click="onViewMembers"
        >
          <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          View All Members
        </button>
        
        <!-- View Projects -->
        <button
          type="button"
          class="w-full inline-flex items-center justify-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          @click="onViewProjects"
        >
          <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          View Projects
        </button>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-overlay absolute inset-0 bg-white dark:bg-gray-900 bg-opacity-75 dark:bg-opacity-75 flex items-center justify-center rounded-lg">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Team } from '~/types/team-types'
import TeamVisibilityBadge from '~/components/atoms/teams/TeamVisibilityBadge.vue'
import TeamBadge from '~/components/atoms/teams/TeamBadge.vue'
import TeamJoinButton from '~/components/atoms/teams/TeamJoinButton.vue'
import TeamInviteButton from '~/components/atoms/teams/TeamInviteButton.vue'
import TeamSettingsButton from '~/components/atoms/teams/TeamSettingsButton.vue'

const props = withDefaults(defineProps<{
  team: Team
  loading?: boolean
  userId?: string | null
  showActions?: boolean
  createdByName?: string
  isMember?: boolean
  isInvited?: boolean
  canManageTeam?: boolean
}>(), {
  loading: false,
  userId: null,
  showActions: true,
  createdByName: 'Unknown',
  isMember: false,
  isInvited: false,
  canManageTeam: false,
})

const emit = defineEmits<{
  join: [teamId: string]
  leave: [teamId: string]
  invite: [teamId: string]
  settings: [teamId: string]
  'avatar-upload': [teamId: string]
  'view-members': [teamId: string]
  'view-projects': [teamId: string]
}>()

// CSS-Klassen
const sidebarClasses = computed(() => ({
  'loading': props.loading,
  'has-actions': props.showActions,
}))

// Berechnete Werte
const teamVisibility = computed(() => props.team.visibility || 'public')

const memberProgress = computed(() => {
  const memberCount = props.team.stats?.memberCount || 0
  const maxMembers = props.team.maxMembers
  if (!maxMembers) return 0
  return Math.min(100, Math.round((memberCount / maxMembers) * 100))
})

const activityStars = computed(() => {
  // Simulierte Aktivitätsbewertung basierend auf Mitgliederanzahl und Projekten
  const memberCount = props.team.stats?.memberCount || 0
  const projectCount = props.team.stats?.projectCount || 0
  const score = memberCount * 2 + projectCount * 3
  return Math.min(5, Math.max(1, Math.round(score / 10)))
})

const activityLevel = computed(() => {
  const stars = activityStars.value
  if (stars >= 4) return 'High'
  if (stars >= 3) return 'Medium'
  return 'Low'
})

const teamAge = computed(() => {
  const created = new Date(props.team.createdAt)
  const now = new Date()
  const diffMs = now.getTime() - created.getTime()
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  
  if (diffDays < 1) {
    return 'Today'
  } else if (diffDays === 1) {
    return '1 day'
  } else if (diffDays < 7) {
    return `${diffDays} days`
  } else if (diffDays < 30) {
    const weeks = Math.floor(diffDays / 7)
    return `${weeks} week${weeks > 1 ? 's' : ''}`
  } else if (diffDays < 365) {
    const months = Math.floor(diffDays / 30)
    return `${months} month${months > 1 ? 's' : ''}`
  } else {
    const years = Math.floor(diffDays / 365)
    return `${years} year${years > 1 ? 's' : ''}`
  }
})

// Event-Handler
const onAvatarUpload = () => {
  emit('avatar-upload', props.team.id)
}

const onJoin = () => {
  emit('join', props.team.id)
}

const onLeave = () => {
  emit('leave', props.team.id)
}

const onInvite = () => {
  console.log('TeamDetailsSidebar: Invite button clicked, teamId:', props.team.id)
  emit('invite', props.team.id)
}

const onSettings = () => {
  emit('settings', props.team.id)
}

const onViewMembers = () => {
  emit('view-members', props.team.id)
}

const onViewProjects = () => {
  emit('view-projects', props.team.id)
}

// Hilfsfunktionen
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}
</script>