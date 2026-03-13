<template>
  <div v-if="loading" class="container mx-auto px-4 py-8 text-center">
    <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    <p class="mt-4 text-gray-600 dark:text-gray-400">{{ t('teams.loadingTeam') }}</p>
  </div>

  <div v-else-if="error" class="container mx-auto px-4 py-8 text-center">
    <div
      class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400 mb-4">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </div>
    <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">{{ t('teams.errorLoadingTeam') }}</h3>
    <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
    <button @click="loadTeam" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700">
      {{ t('common.tryAgain') }}
    </button>
  </div>

  <div v-else-if="team" class="container mx-auto px-4 py-8">
    <TeamDetailsHeader
      :team="team"
      :is-member="isTeamMember"
      :user-id="currentUserId"
      :user-role="currentUserRole"
      :can-manage-team="isTeamOwner"
      @edit="editTeam"
      @leave="leaveTeam"
      @join="joinTeam"
      @delete="deleteTeam"
      @report="reportTeam"
      @share="shareTeam"
    />

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-8 mt-8">
      <div class="lg:col-span-3">
        <TeamDetailsContent
          :team="team"
          :members="members"
          :invitations="invitations"
          :can-manage-team="isTeamOwner"
          :current-user-id="currentUserId"
          @invite="inviteMember"
          @remove-member="handleRemoveMember"
          @accept-invitation="handleAcceptInvitation"
          @reject-invitation="handleRejectInvitation"
          @resend-invitation="handleResendInvitation"
          @cancel-invitation="handleCancelInvitation"
          @delete-team="deleteTeam"
        />


        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mt-8">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ t('teams.teamProjects') }}</h3>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              {{ projects.length }} {{ t('teams.projects') }}
            </div>
          </div>

          <div v-if="projectsLoading" class="text-center py-8">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            <p class="mt-2 text-gray-600 dark:text-gray-400">{{ t('teams.loadingProjects') }}</p>
          </div>

          <div v-else-if="projects.length === 0" class="text-center py-8">
            <div
              class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 mb-4">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <p class="text-gray-600 dark:text-gray-400">{{ t('teams.noProjectsYet') }}</p>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">
              {{ t('teams.createProjectForTeam') }}
            </p>
            <button
              v-if="isTeamMember && team.hackathonId"
              @click="createProject"
              class="inline-block mt-4 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-md text-sm font-medium"
            >
              {{ t('teams.createProject') }}
            </button>
          </div>

          <div v-else class="space-y-4">
            <div v-for="project in projects" :key="project.id"
              class="p-4 rounded-lg border border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center mb-2">
                    <a
                      :href="`/projects/${project.id}`"
                      class="font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400"
                    >
                      {{ project.title || project.name }}
                    </a>
                    <span v-if="project.hackathon"
                      class="ml-2 px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300 rounded-full">
                      {{ project.hackathon.name }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
                    {{ project.description }}
                  </p>
                  <div class="flex items-center text-sm text-gray-500 dark:text-gray-400">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {{ formatDate(project.created_at) }}
                  </div>
                </div>
                <div class="ml-4">
                  <a
                    :href="`/projects/${project.id}`"
                    class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300"
                  >
                    {{ t('teams.viewProject') }}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="lg:col-span-1">
        <TeamDetailsSidebar
          :team="team"
          :created-by-name="createdByName"
          :user-id="currentUserId"
          :is-member="isTeamMember"
          :can-manage-team="isTeamOwner"
          @settings="editTeam"
          @invite="inviteMember"
          @leave="leaveTeam"
          @join="joinTeam"
        />
      </div>
    </div>

    <div v-if="showLeaveConfirm" class="fixed inset-0 bg-gray-500 dark:bg-gray-900 bg-opacity-75 dark:bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg max-w-md w-full p-6">
        <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4">
          {{ t('teams.confirmLeaveTeamTitle') }}
        </h3>
        <p class="text-gray-700 dark:text-gray-300 mb-6">
          {{ t('teams.confirmLeaveTeam') }}
        </p>
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
            @click="cancelLeave"
          >
            {{ t('common.cancel') }}
          </button>
          <button
            type="button"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            @click="confirmLeave"
          >
            {{ t('teams.leaveTeam') }}
          </button>
        </div>
      </div>
    </div>

    <Modal
      v-model="showReportModal"
      title="Report Team"
      description="Tell us why this team should be reviewed."
      size="md"
      @close="closeReportModal"
    >
      <div class="space-y-4">
        <div>
          <label for="team-report-reason" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Reason
          </label>
          <textarea
            id="team-report-reason"
            v-model="reportReason"
            rows="5"
            class="w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            placeholder="Describe the issue with this team"
          />
        </div>
      </div>

      <template #footer>
        <button
          type="button"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
          @click="closeReportModal"
        >
          {{ t('common.cancel') }}
        </button>
        <button
          type="button"
          class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700"
          @click="submitTeamReport"
        >
          Send Report
        </button>
      </template>
    </Modal>

    <Modal
      v-model="showInviteModal"
      :title="t('teams.inviteMembers')"
      size="lg"
      @close="closeInviteModal"
    >
      <div class="modal-content">
        <TeamInviteSection
          v-if="team && isTeamOwner"
          :team-id="Number(team.id)"
          :current-member-count="members.length"
          :max-members="team.maxMembers || 5"
          :is-team-owner="isTeamOwner"
          :is-team-full="isTeamFull"
          :exclude-user-ids="members.map(member => Number(member.userId))"
          @invite-sent="handleInviteSent"
          @error="handleInviteError"
        />
        <div v-else class="text-center py-8">
          <p class="text-gray-600 dark:text-gray-400">{{ t('teams.onlyOwnerCanInvite') }}</p>
        </div>
      </div>

      <template #footer>
        <button
          type="button"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
          @click="closeInviteModal"
        >
          {{ t('common.close') }}
        </button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from '#app'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '~/stores/auth'
import { useTeamStore } from '~/stores/team'
import { useUIStore } from '~/stores/ui'
import { TeamRole, TeamStatus, TeamVisibility, type Team, type TeamInvitation, type TeamMember } from '~/types/team-types'
import TeamDetailsContent from '~/components/organisms/teams/TeamDetailsContent.vue'
import TeamDetailsHeader from '~/components/organisms/teams/TeamDetailsHeader.vue'
import TeamDetailsSidebar from '~/components/organisms/teams/TeamDetailsSidebar.vue'
import Modal from '~/components/molecules/Modal.vue'
import TeamInviteSection from '~/components/organisms/teams/TeamInviteSection.vue'

const route = useRoute()
const router = useRouter()
const teamStore = useTeamStore()
const authStore = useAuthStore()
const uiStore = useUIStore()
const { t } = useI18n()

const loading = ref(true)
const error = ref<string | null>(null)
const team = ref<Team | null>(null)
const members = ref<TeamMember[]>([])
const invitations = ref<TeamInvitation[]>([])
const projects = ref<any[]>([])
const projectsLoading = ref(false)
const showLeaveConfirm = ref(false)
const showInviteModal = ref(false)
const showReportModal = ref(false)
const reportReason = ref('')
const createdByName = ref('Unknown')

const teamId = computed(() => Number(route.params.id))
const currentUserId = computed(() => authStore.user?.id?.toString() || null)
const currentUserRole = computed(() => members.value.find(member => member.userId === currentUserId.value)?.role || null)
const isTeamMember = computed(() => members.value.some(member => member.userId === currentUserId.value))
const isTeamOwner = computed(() => currentUserRole.value === TeamRole.OWNER)
const isTeamFull = computed(() => {
  if (!team.value?.maxMembers) {
    return false
  }
  return members.value.length >= team.value.maxMembers
})

function mapTeam(rawTeam: any): Team {
  return {
    id: String(rawTeam.id),
    name: rawTeam.name,
    description: rawTeam.description || null,
    slug: rawTeam.slug || rawTeam.name?.toLowerCase().replace(/\s+/g, '-') || '',
    avatarUrl: rawTeam.avatar_url || null,
    bannerUrl: rawTeam.banner_url || null,
    visibility: rawTeam.is_open ? TeamVisibility.PUBLIC : TeamVisibility.PRIVATE,
    status: TeamStatus.ACTIVE,
    maxMembers: rawTeam.max_members ?? null,
    createdAt: rawTeam.created_at,
    updatedAt: rawTeam.updated_at || rawTeam.created_at,
    createdBy: String(rawTeam.created_by),
    hackathonId: rawTeam.hackathon_id ? String(rawTeam.hackathon_id) : null,
    tags: Array.isArray(rawTeam.tags) ? rawTeam.tags : [],
    stats: {
      memberCount: rawTeam.member_count || rawTeam._member_count || 0,
      projectCount: rawTeam.project_count || 0,
      activeProjectCount: rawTeam.active_project_count || 0,
      completedProjectCount: rawTeam.completed_project_count || 0,
      totalVotes: rawTeam.total_votes || 0,
      totalComments: rawTeam.total_comments || 0,
      averageRating: rawTeam.average_rating ?? null,
      lastActivityAt: rawTeam.last_activity_at || rawTeam.updated_at || rawTeam.created_at || null,
      viewCount: rawTeam.view_count || 0,
      engagementScore: rawTeam.engagement_score || 0,
      engagementLevel: rawTeam.engagement_level || 'low',
    },
  }
}

function mapMember(rawMember: any): TeamMember {
  return {
    id: String(rawMember.id),
    userId: String(rawMember.user_id),
    teamId: String(rawMember.team_id),
    role: (rawMember.role || TeamRole.MEMBER) as TeamRole,
    joinedAt: rawMember.joined_at,
    user: rawMember.user
      ? {
          id: String(rawMember.user.id),
          username: rawMember.user.username || '',
          displayName: rawMember.user.display_name || rawMember.user.name || null,
          avatarUrl: rawMember.user.avatar_url || null,
          email: rawMember.user.email || null,
          bio: rawMember.user.bio || null,
          skills: Array.isArray(rawMember.user.skills) ? rawMember.user.skills : [],
        }
      : undefined,
  }
}

function mapInvitation(rawInvitation: any): TeamInvitation {
  return {
    id: String(rawInvitation.id),
    teamId: String(rawInvitation.team_id),
    invitedUserId: rawInvitation.invited_user_id ? String(rawInvitation.invited_user_id) : null,
    invitedEmail: rawInvitation.invited_email || null,
    invitedByUserId: String(rawInvitation.invited_by),
    role: (rawInvitation.role || TeamRole.MEMBER) as TeamRole,
    status: (rawInvitation.status === 'declined' ? 'rejected' : rawInvitation.status) as TeamInvitation['status'],
    message: rawInvitation.message || null,
    expiresAt: rawInvitation.expires_at || rawInvitation.created_at,
    createdAt: rawInvitation.created_at,
    updatedAt: rawInvitation.updated_at || rawInvitation.created_at,
    invitedByUser: rawInvitation.inviter
      ? {
          id: String(rawInvitation.inviter.id),
          username: rawInvitation.inviter.username || '',
          displayName: rawInvitation.inviter.display_name || rawInvitation.inviter.name || null,
          avatarUrl: rawInvitation.inviter.avatar_url || null,
          email: rawInvitation.inviter.email || null,
          bio: rawInvitation.inviter.bio || null,
          skills: Array.isArray(rawInvitation.inviter.skills) ? rawInvitation.inviter.skills : [],
        }
      : undefined,
    invitedUser: rawInvitation.invited_user
      ? {
          id: String(rawInvitation.invited_user.id),
          username: rawInvitation.invited_user.username || '',
          displayName: rawInvitation.invited_user.display_name || rawInvitation.invited_user.name || null,
          avatarUrl: rawInvitation.invited_user.avatar_url || null,
          email: rawInvitation.invited_user.email || null,
          bio: rawInvitation.invited_user.bio || null,
          skills: Array.isArray(rawInvitation.invited_user.skills) ? rawInvitation.invited_user.skills : [],
        }
      : undefined,
  }
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}

async function loadTeam() {
  loading.value = true
  error.value = null

  try {
    const rawTeam = await teamStore.fetchTeam(teamId.value)
    team.value = mapTeam(rawTeam)
    createdByName.value = rawTeam.creator?.name || rawTeam.creator?.username || 'Unknown'
    members.value = (teamStore.teamMembers.get(teamId.value) || []).map(mapMember)
    invitations.value = (await teamStore.fetchTeamInvitations(teamId.value)).map(mapInvitation)
    await loadTeamProjects()
  } catch (err) {
    error.value = err instanceof Error ? err.message : t('teams.failedToLoadTeam')
    console.error('Failed to load team:', err)
  } finally {
    loading.value = false
  }
}

async function loadTeamProjects() {
  if (!teamId.value) {
    return
  }

  projectsLoading.value = true
  try {
    projects.value = await teamStore.fetchTeamProjects(teamId.value)
  } catch (err) {
    console.error('Failed to load team projects:', err)
    projects.value = []
  } finally {
    projectsLoading.value = false
  }
}

async function joinTeam() {
  if (!authStore.user?.id) {
    uiStore.showError(t('teams.loginRequiredToJoin'), t('common.authenticationRequired'))
    router.push('/login')
    return
  }

  if (team.value?.visibility !== TeamVisibility.PUBLIC) {
    uiStore.showInfo(t('teams.teamClosedMessage'), t('teams.closedTeam'))
    return
  }

  try {
    await teamStore.joinTeam(teamId.value)
    uiStore.showSuccess(t('teams.joinedTeamSuccess'))
    await loadTeam()
  } catch (err) {
    console.error('Failed to join team:', err)
  }
}

function leaveTeam() {
  if (!authStore.user?.id) {
    return
  }
  showLeaveConfirm.value = true
}

async function confirmLeave() {
  if (!authStore.user?.id) {
    return
  }

  try {
    await teamStore.leaveTeam(teamId.value)
    uiStore.showSuccess(t('teams.leftTeamSuccess'))
    router.push('/teams')
  } catch (err) {
    console.error('Failed to leave team:', err)
  } finally {
    showLeaveConfirm.value = false
  }
}

function cancelLeave() {
  showLeaveConfirm.value = false
}

async function removeMember(userId: string) {
  if (!isTeamOwner.value) {
    return
  }

  try {
    const confirmed = confirm(t('teams.confirmRemoveMember'))
    if (!confirmed) {
      return
    }

    await teamStore.removeTeamMember(teamId.value, Number(userId))
    uiStore.showSuccess(t('teams.memberRemovedSuccess'))
    await loadTeam()
  } catch (err) {
    console.error('Failed to remove member:', err)
  }
}

function handleRemoveMember(userId: string) {
  return removeMember(userId)
}

function editTeam() {
  router.push(`/teams/${teamId.value}/edit`)
}

function inviteMember() {
  showInviteModal.value = true
}

function closeInviteModal() {
  showInviteModal.value = false
}

function handleInviteSent() {
  uiStore.showSuccess(t('teams.invitationSent'))
  closeInviteModal()
  loadTeam()
}

function handleInviteError(payload: { message: string }) {
  uiStore.showError(payload.message, t('teams.invitationFailed'))
}

async function handleAcceptInvitation(invitationId: string) {
  try {
    await teamStore.acceptInvitation(Number(invitationId))
    uiStore.showSuccess(t('teams.invitationAccepted'))
    await loadTeam()
  } catch (err) {
    console.error('Failed to accept invitation:', err)
    uiStore.showError(t('teams.invitationAcceptFailed'))
  }
}

async function handleRejectInvitation(invitationId: string) {
  try {
    await teamStore.declineInvitation(Number(invitationId))
    uiStore.showSuccess(t('teams.invitationRejected'))
    await loadTeam()
  } catch (err) {
    console.error('Failed to reject invitation:', err)
    uiStore.showError(t('teams.invitationRejectFailed'))
  }
}

function handleResendInvitation() {
  uiStore.showInfo('Resend functionality not yet implemented')
}

async function handleCancelInvitation(invitationId: string) {
  try {
    await teamStore.cancelInvitation(Number(invitationId))
    uiStore.showSuccess(t('teams.invitationCancelled'))
    await loadTeam()
  } catch (err) {
    console.error('Failed to cancel invitation:', err)
    uiStore.showError(t('teams.invitationCancelFailed'))
  }
}

async function deleteTeam() {
  if (!isTeamOwner.value) {
    return
  }

  const confirmed = confirm(t('teams.confirmDeleteTeam') || 'Delete this team?')
  if (!confirmed) {
    return
  }

  try {
    await teamStore.deleteTeam(teamId.value)
    router.push('/teams')
  } catch (err) {
    console.error('Failed to delete team:', err)
  }
}

function createProject() {
  const query = new URLSearchParams()
  query.set('team', String(teamId.value))
  if (team.value?.hackathonId) {
    query.set('hackathon', team.value.hackathonId)
  }
  router.push(`/create/project?${query.toString()}`)
}

function viewProject(projectId: number | string) {
  router.push(`/projects/${projectId}`)
}

async function shareTeam() {
  if (!team.value) {
    return
  }

  const shareUrl = window.location.href
  const shareText = `Check out the team ${team.value.name} on Hackathon Hub.`

  try {
    if (navigator.share) {
      await navigator.share({
        title: team.value.name,
        text: shareText,
        url: shareUrl,
      })
      return
    }

    await navigator.clipboard.writeText(shareUrl)
    uiStore.showSuccess('Team link copied to clipboard')
  } catch (err) {
    console.error('Failed to share team:', err)
    uiStore.showError('Failed to share team link')
  }
}

function reportTeam() {
  reportReason.value = ''
  showReportModal.value = true
}

function closeReportModal() {
  showReportModal.value = false
  reportReason.value = ''
}

async function submitTeamReport() {
  if (!team.value) {
    return
  }

  const trimmedReason = reportReason.value.trim()
  if (!trimmedReason) {
    uiStore.showError('Please provide a reason for the report')
    return
  }

  try {
    await teamStore.reportTeam(teamId.value, trimmedReason)
    uiStore.showSuccess('Team report submitted')
    closeReportModal()
  } catch (err) {
    console.error('Failed to report team:', err)
  }
}

onMounted(() => {
  loadTeam()
})
</script>

<style scoped>
.container {
  max-width: 1280px;
}
</style>
