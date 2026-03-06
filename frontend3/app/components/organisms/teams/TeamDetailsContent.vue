<template>
  <div class="team-details-content">
    <!-- Tabs Navigation -->
    <div v-if="showTabs" class="tabs-navigation mb-6">
      <nav class="flex space-x-1 border-b border-gray-200 dark:border-gray-700">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          type="button"
          class="tab-button px-4 py-2 text-sm font-medium rounded-t-lg transition-colors duration-200"
          :class="{
            'bg-white dark:bg-gray-800 text-primary-600 dark:text-primary-400 border border-gray-200 dark:border-gray-700 border-b-0': localActiveTab === tab.id,
            'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800': localActiveTab !== tab.id
          }"
          @click="onTabChange(tab.id)"
        >
          <div class="flex items-center">
            {{ tab.label }}
            <span
              v-if="tab.badge"
              class="ml-2 px-2 py-0.5 text-xs font-medium rounded-full"
              :class="tab.badgeClass"
            >
              {{ tab.badge }}
            </span>
          </div>
        </button>
      </nav>
    </div>
    
    <!-- Tab Content -->
    <div class="tab-content">
      <!-- Overview Tab -->
      <div v-if="localActiveTab === 'overview'" class="overview-tab">
        <!-- Team Description -->
        <div v-if="team.description" class="team-description-section mb-8">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
            About This Team
          </h3>
          <div class="prose prose-sm dark:prose-invert max-w-none">
            <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line">
              {{ team.description }}
            </p>
          </div>
        </div>
        
        <!-- Team Tags -->
        <div v-if="team.tags && team.tags.length > 0" class="tags-section mb-8">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
            Tags
          </h3>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="tag in team.tags"
              :key="tag"
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200"
            >
              {{ tag }}
            </span>
          </div>
        </div>
        
        <!-- Team Stats -->
        <div v-if="team.stats" class="stats-section mb-8">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
            Team Statistics
          </h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="stat-item text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
                {{ team.stats.memberCount }}
              </div>
              <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
                Members
              </div>
            </div>
            <div class="stat-item text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
                {{ team.stats.projectCount }}
              </div>
              <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
                Projects
              </div>
            </div>
            <div class="stat-item text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
                {{ team.stats.activeProjectCount }}
              </div>
              <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
                Active Projects
              </div>
            </div>
            <div class="stat-item text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
                {{ team.stats.viewCount }}
              </div>
              <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
                Views
              </div>
            </div>
          </div>
        </div>
        
        <!-- Last Activity -->
        <div v-if="team.stats?.lastActivityAt" class="activity-section">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
            Last Activity
          </h3>
          <div class="text-gray-700 dark:text-gray-300">
            {{ formatTimeAgo(team.stats.lastActivityAt) }}
          </div>
        </div>
      </div>
      
      <!-- Members Tab -->
      <div v-if="localActiveTab === 'members'" class="members-tab">
        <div class="members-header flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Team Members
          </h3>
          <div v-if="canManageTeam" class="actions">
            <TeamInviteButton
              :team="team"
              size="sm"
              variant="primary"
              @invite="onInvite"
            />
          </div>
        </div>
        
        <!-- Member List -->
        <div v-if="members && members.length > 0" class="members-list space-y-3">
          <TeamMemberItem
            v-for="member in members"
            :key="member.id"
            :member="member"
            :team="team"
            :canManageTeam="canManageTeam"
            @remove="onRemoveMember"
            @promote="onPromoteMember"
            @demote="onDemoteMember"
          />
        </div>
        <div v-else class="text-center py-8 text-gray-500 dark:text-gray-400">
          <svg class="h-12 w-12 mx-auto text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="mt-2">No members yet</p>
          <p class="text-sm mt-1">Invite members to join your team</p>
        </div>

        <!-- Invited Members Section -->
        <div class="invited-members-section mt-8">
          <h4 class="text-md font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Invited Members
          </h4>
          <div v-if="invitations && invitations.length > 0" class="space-y-3">
            <TeamInvitationItem
              v-for="invitation in invitations"
              :key="invitation.id"
              :invitation="invitation"
              :team="team"
              :current-user-id="team.createdBy"
              :show-actions="canManageTeam"
              @accept="onAcceptInvitation"
              @reject="onRejectInvitation"
              @resend="onResendInvitation"
              @cancel="onCancelInvitation"
            />
          </div>
          <div v-else class="text-center py-6 border border-gray-200 dark:border-gray-700 rounded-lg">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">No pending invitations</p>
          </div>
        </div>
      </div>
      
      <!-- Settings Tab -->
      <div v-if="localActiveTab === 'settings' && canManageTeam" class="settings-tab">
        <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Team Settings
          </h3>
          <p class="text-gray-600 dark:text-gray-400 mb-6">
            Manage your team settings, visibility, and members.
          </p>
          <div class="space-y-4">
            <div class="setting-item">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Team Name
              </label>
              <input
                type="text"
                :value="team.name"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
                disabled
              />
            </div>
            <div class="setting-item">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Team Visibility
              </label>
              <div class="flex items-center space-x-4">
                <span class="text-gray-700 dark:text-gray-300">
                  {{ teamVisibility === 'public' ? 'Public' : 'Private' }}
                </span>
                <TeamVisibilityBadge
                  :visibility="teamVisibility"
                  size="sm"
                  :show-label="true"
                />
              </div>
            </div>
            <div class="setting-item">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Max Members
              </label>
              <div class="text-gray-700 dark:text-gray-300">
                {{ team.maxMembers || 'Unlimited' }}
              </div>
            </div>
            <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
              <button
                type="button"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                @click="onDeleteTeam"
              >
                Delete Team
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-overlay absolute inset-0 bg-white dark:bg-gray-900 bg-opacity-75 dark:bg-opacity-75 flex items-center justify-center rounded-lg">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Team, TeamMember, TeamInvitation } from '~/types/team-types'
import TeamMemberItem from '~/components/molecules/teams/TeamMemberItem.vue'
import TeamInviteButton from '~/components/atoms/teams/TeamInviteButton.vue'
import TeamVisibilityBadge from '~/components/atoms/teams/TeamVisibilityBadge.vue'
import TeamInvitationItem from '~/components/molecules/teams/TeamInvitationItem.vue'

const props = withDefaults(defineProps<{
  team: Team
  loading?: boolean
  showTabs?: boolean
  activeTab?: string
  members?: TeamMember[]
  invitations?: TeamInvitation[]
  canManageTeam?: boolean
}>(), {
  loading: false,
  showTabs: true,
  activeTab: 'overview',
  members: () => [],
  invitations: () => [],
  canManageTeam: false,
})

const emit = defineEmits<{
  'tab-change': [tabId: string]
  invite: [teamId: string]
  'remove-member': [memberId: string]
  'promote-member': [memberId: string]
  'demote-member': [memberId: string]
  'delete-team': [teamId: string]
  'accept-invitation': [invitationId: string]
  'reject-invitation': [invitationId: string]
  'resend-invitation': [invitationId: string]
  'cancel-invitation': [invitationId: string]
}>()

// Local state
const localActiveTab = ref(props.activeTab)

// Computed properties
const teamVisibility = computed(() => props.team.visibility || 'public')

const tabs = computed(() => [
  {
    id: 'overview',
    label: 'Overview',
    badge: null,
    badgeClass: '',
  },
  {
    id: 'members',
    label: 'Members',
    badge: props.members?.length || 0,
    badgeClass: 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200',
  },
  {
    id: 'settings',
    label: 'Settings',
    badge: null,
    badgeClass: '',
  },
])

// Event handlers
const onTabChange = (tabId: string) => {
  localActiveTab.value = tabId
  emit('tab-change', tabId)
}

const onInvite = () => {
  emit('invite', props.team.id)
}

const onRemoveMember = (memberId: string) => {
  emit('remove-member', memberId)
}

const onPromoteMember = (memberId: string) => {
  emit('promote-member', memberId)
}

const onDemoteMember = (memberId: string) => {
  emit('demote-member', memberId)
}

const onDeleteTeam = () => {
  emit('delete-team', props.team.id)
}

// Invitation event handlers
const onAcceptInvitation = (invitationId: string) => {
  emit('accept-invitation', invitationId)
}

const onRejectInvitation = (invitationId: string) => {
  emit('reject-invitation', invitationId)
}

const onResendInvitation = (invitationId: string) => {
  emit('resend-invitation', invitationId)
}

const onCancelInvitation = (invitationId: string) => {
  emit('cancel-invitation', invitationId)
}

// Helper functions
const formatTimeAgo = (timestamp: string | null) => {
  if (!timestamp) return 'Never'
  
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMinutes = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  
  if (diffMinutes < 1) {
    return 'Just now'
  } else if (diffMinutes < 60) {
    return `${diffMinutes}m ago`
  } else if (diffHours < 24) {
    return `${diffHours}h ago`
  } else if (diffDays < 7) {
    return `${diffDays}d ago`
  } else {
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }
}
</script>

<style scoped>
.tab-button {
  transition: all 0.2s ease;
}

.tab-button:hover {
  transform: translateY(-1px);
}

.loading-overlay {
  z-index: 10;
}
</style>