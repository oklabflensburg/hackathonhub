<template>
  <div class="team-management">
    <!-- Loading State -->
    <div v-if="loading" class="space-y-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 animate-pulse">
        <div class="h-6 bg-gray-300 dark:bg-gray-700 rounded w-1/4 mb-4"></div>
        <div class="space-y-3">
          <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-full"></div>
          <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-2/3"></div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6"
    >
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <svg
            class="h-5 w-5 text-red-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800 dark:text-red-300">
            {{ errorTitle || $t('teams.management.errorTitle') }}
          </h3>
          <div class="mt-2 text-sm text-red-700 dark:text-red-400">
            <p>{{ error }}</p>
          </div>
          <div class="mt-4">
            <button
              type="button"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 dark:text-red-300 dark:bg-red-900/30 dark:hover:bg-red-900/50"
              @click="handleRetry"
            >
              {{ $t('common.retry') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else class="space-y-6">
      <!-- Team Header -->
      <TeamDetailsHeader
        :team="team"
        :can-edit-team="canEditTeam"
        :can-delete-team="canDeleteTeam"
        @edit-team="handleEditTeam"
        @delete-team="handleDeleteTeam"
      />

      <!-- Management Tabs -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md">
        <!-- Tab Navigation -->
        <div class="border-b border-gray-200 dark:border-gray-700">
          <nav class="flex -mb-px">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              :class="[
                'px-6 py-4 text-sm font-medium border-b-2 transition-colors',
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
              ]"
              @click="activeTab = tab.id"
            >
              {{ tab.label }}
              <span
                v-if="tab.badge"
                :class="[
                  'ml-2 px-2 py-0.5 text-xs rounded-full',
                  activeTab === tab.id
                    ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
                    : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                ]"
              >
                {{ tab.badge }}
              </span>
            </button>
          </nav>
        </div>

        <!-- Tab Content -->
        <div class="p-6">
          <!-- Members Tab -->
          <div v-if="activeTab === 'members'">
            <TeamMembersPanel
              :team="team"
              :members="teamMembers"
              :invitations="invitations"
              :current-user-id="currentUserId"
              :can-invite-members="canInviteMembers"
              :can-manage-members="canManageMembers"
              :can-manage-invitations="canManageInvitations"
              @invite-member="handleInviteMember"
              @remove-member="handleRemoveMember"
              @promote-member="handlePromoteMember"
              @demote-member="handleDemoteMember"
              @accept-invitation="handleAcceptInvitation"
              @reject-invitation="handleRejectInvitation"
              @cancel-invitation="handleCancelInvitation"
              @resend-invitation="handleResendInvitation"
              @view-profile="handleViewProfile"
            />
          </div>

          <!-- Settings Tab -->
          <div v-else-if="activeTab === 'settings'">
            <TeamManagementPanel
              :team="team"
              :can-delete-team="canDeleteTeam"
              @delete-team="handleDeleteTeam"
            />
          </div>

          <!-- Projects Tab -->
          <div v-else-if="activeTab === 'projects'">
            <TeamProjectsPanel
              :team="team"
              :projects="projects"
              :can-create-projects="canCreateProjects"
              :can-edit-projects="canEditProjects"
              @create-project="handleCreateProject"
              @view-project="handleViewProject"
              @edit-project="handleEditProject"
            />
          </div>

          <!-- Invitations Tab -->
          <div v-else-if="activeTab === 'invitations'">
            <TeamInvitationsPanel
              :team="team"
              :invitations="invitations"
              :current-user-id="currentUserId"
              :can-manage-invitations="canManageInvitations"
              @accept-invitation="handleAcceptInvitation"
              @reject-invitation="handleRejectInvitation"
              @cancel-invitation="handleCancelInvitation"
              @resend-invitation="handleResendInvitation"
              @view-profile="handleViewProfile"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { Team, TeamMember, TeamInvitation } from '~/types/team-types'
import TeamDetailsHeader from './TeamDetailsHeader.vue'
import TeamManagementPanel from './TeamManagementPanel.vue'
import TeamInvitationsPanel from './TeamInvitationsPanel.vue'
import TeamMembersPanel from './TeamMembersPanel.vue'
import TeamProjectsPanel from './TeamProjectsPanel.vue'

const { t } = useI18n()

// Team Project type (compatible with TeamProjectsPanel)
interface TeamProject {
  id: string
  name: string
  description?: string
  status: string
  voteCount?: number
  commentCount?: number
  memberCount?: number
  createdAt: string
  tags?: string[]
}

// Props
interface Props {
  team: Team
  teamMembers: TeamMember[]
  invitations: TeamInvitation[]
  projects: TeamProject[]
  loading?: boolean
  error?: string
  errorTitle?: string
  currentUserId?: string
  canEditTeam?: boolean
  canDeleteTeam?: boolean
  canInviteMembers?: boolean
  canManageMembers?: boolean
  canManageInvitations?: boolean
  canCreateProjects?: boolean
  canEditProjects?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  error: undefined,
  errorTitle: undefined,
  currentUserId: undefined,
  canEditTeam: false,
  canDeleteTeam: false,
  canInviteMembers: false,
  canManageMembers: false,
  canManageInvitations: false,
  canCreateProjects: false,
  canEditProjects: false
})

// Emits
const emit = defineEmits<{
  'edit-team': [team: Team]
  'delete-team': [team: Team]
  'invite-member': [team: Team]
  'remove-member': [memberId: string]
  'promote-member': [memberId: string]
  'demote-member': [memberId: string]
  'update-role': [memberId: string, role: string]
  'accept-invitation': [invitationId: string]
  'reject-invitation': [invitationId: string]
  'cancel-invitation': [invitationId: string]
  'resend-invitation': [invitationId: string]
  'create-project': [team: Team]
  'view-project': [project: TeamProject]
  'edit-project': [project: TeamProject]
  'view-profile': [userId: string]
  'retry': []
}>()

// Reactive state
const activeTab = ref('members')

// Computed
const tabs = computed(() => [
  {
    id: 'members',
    label: t('teams.management.members'),
    badge: props.teamMembers.length > 0 ? props.teamMembers.length.toString() : undefined
  },
  {
    id: 'projects',
    label: t('teams.management.projects'),
    badge: props.team.stats?.projectCount ? props.team.stats.projectCount.toString() : undefined
  },
  {
    id: 'invitations',
    label: t('teams.management.invitations'),
    badge: props.invitations.length > 0 ? props.invitations.length.toString() : undefined
  },
  {
    id: 'settings',
    label: t('teams.management.settings')
  }
])

// Methods
const handleEditTeam = () => {
  emit('edit-team', props.team)
}

const handleDeleteTeam = () => {
  emit('delete-team', props.team)
}

const handleInviteMember = () => {
  emit('invite-member', props.team)
}

const handleRemoveMember = (memberId: string) => {
  emit('remove-member', memberId)
}

const handlePromoteMember = (memberId: string) => {
  emit('promote-member', memberId)
}

const handleDemoteMember = (memberId: string) => {
  emit('demote-member', memberId)
}

const handleUpdateMemberRole = (memberId: string, role: string) => {
  emit('update-role', memberId, role)
}

const handleAcceptInvitation = (invitationId: string) => {
  emit('accept-invitation', invitationId)
}

const handleRejectInvitation = (invitationId: string) => {
  emit('reject-invitation', invitationId)
}

const handleCancelInvitation = (invitationId: string) => {
  emit('cancel-invitation', invitationId)
}

const handleResendInvitation = (invitationId: string) => {
  emit('resend-invitation', invitationId)
}

const handleCreateProject = () => {
  emit('create-project', props.team)
}

const handleViewProject = (project: TeamProject) => {
  emit('view-project', project)
}

const handleEditProject = (project: TeamProject) => {
  emit('edit-project', project)
}

const handleViewProfile = (userId: string) => {
  emit('view-profile', userId)
}

const handleRetry = () => {
  emit('retry')
}

const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}
</script>

<style scoped>
.team-management {
  @apply max-w-7xl mx-auto;
}
</style>