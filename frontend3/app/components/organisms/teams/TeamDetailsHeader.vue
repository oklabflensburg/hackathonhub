<template>
  <header class="team-details-header" :class="headerClasses">
    <!-- Breadcrumb Navigation -->
    <nav
      v-if="showBreadcrumb"
      class="breadcrumb mb-4"
      aria-label="Breadcrumb"
    >
      <ol class="flex items-center space-x-2 text-sm">
        <li>
          <a
            href="/teams"
            class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
          >
            {{ $t('teams.title') }}
          </a>
        </li>
        <li>
          <svg
            class="h-4 w-4 text-gray-400 dark:text-gray-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </li>
        <li class="text-gray-700 dark:text-gray-300 font-medium truncate">
          {{ team.name }}
        </li>
      </ol>
    </nav>
    
    <!-- Main Header Content -->
    <div class="header-content">
      <!-- Title and Status Row -->
      <div class="title-row flex items-start justify-between mb-4">
        <div class="title-section flex-1">
          <div class="flex items-center gap-3 mb-2">
            <h1 class="team-title text-3xl font-bold text-gray-900 dark:text-gray-100">
              {{ team.name }}
            </h1>
            <TeamVisibilityBadge
              :visibility="teamVisibility"
              size="lg"
            />
            <TeamRoleBadge
              v-if="userRole"
              :role="userRole"
              size="lg"
            />
          </div>
          
          <div class="title-meta flex flex-wrap items-center gap-3">
            <!-- Team Status -->
            <TeamBadge
              :status="team.status"
              size="md"
              :show-label="true"
            />
            
            <!-- Member Count -->
            <div class="member-count flex items-center text-sm text-gray-600 dark:text-gray-400">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{{ team.stats?.memberCount || 0 }} / {{ team.maxMembers || '∞' }} members</span>
            </div>
            
            <!-- Created Date -->
            <div class="created-date flex items-center text-sm text-gray-600 dark:text-gray-400">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>Created {{ formatDate(team.createdAt) }}</span>
            </div>
            
            <!-- Hackathon Badge -->
            <div v-if="team.hackathonId" class="hackathon-badge">
              <a
                :href="`/hackathons/${team.hackathonId}`"
                class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200 hover:bg-purple-200 dark:hover:bg-purple-800"
              >
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Hackathon Team
              </a>
            </div>
          </div>
        </div>
        
        <!-- Action Buttons -->
        <div v-if="showActions" class="action-buttons flex items-center gap-2">
          <!-- Join/Leave Button -->
          <TeamJoinButton
            v-if="userId && !isMember"
            :team="team"
            :userId="userId"
            :isMember="isMember"
            :isInvited="isInvited"
            size="lg"
            variant="primary"
            @join="handleJoin"
            @leave="handleLeave"
          />
          
          <!-- Invite Button -->
          <TeamInviteButton
            v-if="isMember"
            :team="team"
            size="lg"
            variant="secondary"
            @invite="handleInvite"
          />
          
          <!-- Settings Button -->
          <TeamSettingsButton
            v-if="canManageTeam"
            :team="team"
            size="lg"
            variant="outline"
            @settings="handleSettings"
          />
          
          <!-- More Actions Dropdown -->
          <div v-if="showMoreActions" class="more-actions-dropdown relative">
            <button
              type="button"
              class="inline-flex items-center p-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              @click="toggleMoreActions"
            >
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
              </svg>
            </button>
            
            <!-- Dropdown Menu -->
            <div
              v-if="showMoreActionsMenu"
              class="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 focus:outline-none z-10"
            >
              <div class="py-1">
                <a
                  v-if="canManageTeam"
                  href="#"
                  class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                  @click.prevent="handleEdit"
                >
                  Edit Team
                </a>
                <a
                  v-if="canManageTeam"
                  href="#"
                  class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                  @click.prevent="handleDelete"
                >
                  Delete Team
                </a>
                <a
                  href="#"
                  class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                  @click.prevent="handleReport"
                >
                  Report Team
                </a>
                <a
                  href="#"
                  class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                  @click.prevent="handleShare"
                >
                  Share Team
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Team Description -->
      <div v-if="team.description" class="team-description mb-6">
        <p class="text-gray-700 dark:text-gray-300">
          {{ team.description }}
        </p>
      </div>
      
      <!-- Team Tags -->
      <div v-if="team.tags && team.tags.length > 0" class="team-tags mb-6">
        <div class="flex flex-wrap gap-2">
          <span
            v-for="tag in team.tags"
            :key="tag"
            class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
          >
            {{ tag }}
          </span>
        </div>
      </div>
      
      <!-- Loading State -->
      <div v-if="loading" class="loading-overlay absolute inset-0 bg-white dark:bg-gray-900 bg-opacity-75 dark:bg-opacity-75 flex items-center justify-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { TeamVisibility, type Team, type TeamRole } from '~/types/team-types'
import TeamVisibilityBadge from '~/components/atoms/teams/TeamVisibilityBadge.vue'
import TeamRoleBadge from '~/components/atoms/teams/TeamRoleBadge.vue'
import TeamBadge from '~/components/atoms/teams/TeamBadge.vue'
import TeamJoinButton from '~/components/atoms/teams/TeamJoinButton.vue'
import TeamInviteButton from '~/components/atoms/teams/TeamInviteButton.vue'
import TeamSettingsButton from '~/components/atoms/teams/TeamSettingsButton.vue'

const props = withDefaults(defineProps<{
  team: Team
  loading?: boolean
  userId?: string | null
  showActions?: boolean
  showBreadcrumb?: boolean
  showMoreActions?: boolean
  userRole?: TeamRole | null
  isMember?: boolean
  isInvited?: boolean
  canManageTeam?: boolean
}>(), {
  showBreadcrumb: true,
  showActions: true,
  showMoreActions: true,
  loading: false,
  userId: null,
  userRole: null,
  isMember: false,
  isInvited: false,
  canManageTeam: false,
})

const emit = defineEmits<{
  join: [teamId: string]
  leave: [teamId: string]
  invite: [teamId: string]
  settings: [teamId: string]
  edit: [teamId: string]
  delete: [teamId: string]
  report: [teamId: string]
  share: [teamId: string]
}>()

const showMoreActionsMenu = ref(false)

// Computed properties
const teamVisibility = computed(() => {
  if (props.team.visibility) {
    return props.team.visibility
  }
  // Fallback: use is_open if available (for API compatibility)
  const teamAny = props.team as any
  if (teamAny.is_open !== undefined) {
    return teamAny.is_open ? TeamVisibility.PUBLIC : TeamVisibility.PRIVATE
  }
  return TeamVisibility.PUBLIC
})

// CSS-Klassen
const headerClasses = computed(() => ({
  'loading': props.loading,
  'has-breadcrumb': props.showBreadcrumb,
  'has-actions': props.showActions,
}))

// Formatierungsfunktionen
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
}

// Event-Handler
const handleJoin = () => {
  emit('join', props.team.id)
}

const handleLeave = () => {
  emit('leave', props.team.id)
}

const handleInvite = () => {
  emit('invite', props.team.id)
}

const handleSettings = () => {
  emit('settings', props.team.id)
}

const handleEdit = () => {
  emit('edit', props.team.id)
}

const handleDelete = () => {
  emit('delete', props.team.id)
}

const handleReport = () => {
  emit('report', props.team.id)
}

const handleShare = () => {
  emit('share', props.team.id)
}

const toggleMoreActions = () => {
  showMoreActionsMenu.value = !showMoreActionsMenu.value
}

// Close dropdown when clicking outside
const closeDropdown = () => {
  showMoreActionsMenu.value = false
}
</script>

<style scoped>
.team-details-header {
  @apply relative mb-8 pb-6 border-b border-gray-200 dark:border-gray-700;
}

.breadcrumb {
  @apply text-sm;
}

.header-content {
  @apply relative;
}

.title-row {
  @apply flex items-start justify-between;
}

.title-section {
  @apply flex-1;
}

.team-title {
  @apply text-3xl font-bold text-gray-900 dark:text-gray-100;
}

.title-meta {
  @apply flex flex-wrap items-center gap-3 mt-2;
}

.member-count,
.created-date {
  @apply flex items-center text-sm text-gray-600 dark:text-gray-400;
}

.action-buttons {
  @apply flex items-center gap-2;
}

.more-actions-dropdown {
  @apply relative;
}

.team-description {
  @apply text-gray-700 dark:text-gray-300;
}

.team-tags {
  @apply flex flex-wrap gap-2;
}

.loading-overlay {
  @apply absolute inset-0 bg-white dark:bg-gray-900 bg-opacity-75 dark:bg-opacity-75 flex items-center justify-center;
}
</style>