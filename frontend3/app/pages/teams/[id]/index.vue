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
    <!-- Team Details Header -->
    <TeamDetailsHeader
      :team="team"
      :is-owner="isTeamOwner"
      :is-member="isTeamMember"
      :is-full="isTeamFull"
      @edit="editTeam"
      @leave="leaveTeam"
      @join="joinTeam"
    />

    <!-- Team Info -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-8 mt-8">
      <!-- Left Column: Team Details Content -->
      <div class="lg:col-span-3">
        <!-- Team Details Content -->
        <TeamDetailsContent
          :team="team"
          :members="members"
          :invitations="invitations"
          :projects="projects"
          :is-owner="isTeamOwner"
          :is-member="isTeamMember"
          :can-manage-team="isTeamOwner"
          :projects-loading="projectsLoading"
          @create-project="createProject"
          @view-project="viewProject"
          @invite="inviteMember"
          @accept-invitation="handleAcceptInvitation"
          @reject-invitation="handleRejectInvitation"
          @resend-invitation="handleResendInvitation"
          @cancel-invitation="handleCancelInvitation"
        />

        <!-- Team Members Section -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mt-8">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ t('teams.teamMembers') }}</h3>
          <div v-if="members.length === 0" class="text-center py-8">
            <p class="text-gray-600 dark:text-gray-400">{{ t('teams.noMembersYet') }}</p>
          </div>
          <div v-else class="space-y-4">
            <div v-for="member in members" :key="member.id" class="flex items-center justify-between p-3 border border-gray-100 dark:border-gray-700 rounded-lg">
              <div class="flex items-center">
                <div class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-700 dark:text-gray-300 font-medium">
                  {{ member.user?.username?.charAt(0).toUpperCase() || 'U' }}
                </div>
                <div class="ml-3">
                  <p class="font-medium text-gray-900 dark:text-white">{{ member.user?.username || 'Unknown User' }}</p>
                  <p class="text-sm text-gray-500 dark:text-gray-400">{{ member.role === 'owner' ? t('teams.owner') : t('teams.member') }}</p>
                </div>
              </div>
              <div v-if="isTeamOwner && member.user_id !== authStore.user?.id" class="flex space-x-2">
                <button
                  v-if="member.role === 'member'"
                  @click="makeOwner(member.user_id)"
                  class="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                >
                  {{ t('teams.makeOwner') }}
                </button>
                <button
                  v-if="member.role === 'owner'"
                  @click="makeMember(member.user_id)"
                  class="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                >
                  {{ t('teams.makeMember') }}
                </button>
                <button
                  @click="removeMember(member.user_id)"
                  class="px-3 py-1 text-sm border border-red-300 dark:border-red-700 rounded text-red-700 dark:text-red-300 hover:bg-red-50 dark:hover:bg-red-900/30"
                >
                  {{ t('teams.remove') }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Team Projects Section -->
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
              v-if="isTeamMember && team.hackathon"
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
                      {{ project.name }}
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

      <!-- Right Column: Team Sidebar -->
      <div class="lg:col-span-1">
        <TeamDetailsSidebar
          :team="team"
          :members="members"
          :is-owner="isTeamOwner"
          @edit="editTeam"
          @delete="deleteTeam"
          @invite="inviteMember"
        />
      </div>
    </div>

    <!-- Leave Team Confirmation Dialog -->
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

    <!-- Invite Member Modal -->
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
          :max-members="team.max_members || 5"
          :is-team-owner="isTeamOwner"
          :is-team-full="isTeamFull"
          :exclude-user-ids="members.map(m => m.user_id)"
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from '#app'
import { useTeamStore } from '~/stores/team'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'
import TeamDetailsHeader from '~/components/organisms/teams/TeamDetailsHeader.vue'
import TeamDetailsSidebar from '~/components/organisms/teams/TeamDetailsSidebar.vue'
import TeamDetailsContent from '~/components/organisms/teams/TeamDetailsContent.vue'
import Modal from '~/components/molecules/Modal.vue'
import TeamInviteSection from '~/components/organisms/teams/TeamInviteSection.vue'

const route = useRoute()
const router = useRouter()
const teamStore = useTeamStore()
const authStore = useAuthStore()
const uiStore = useUIStore()
const { t } = useI18n()

// State
const loading = ref(true)
const error = ref<string | null>(null)
const team = ref<any>(null)
const members = ref<any[]>([])
const invitations = ref<any[]>([])
const projects = ref<any[]>([])
const projectsLoading = ref(false)
const showLeaveConfirm = ref(false)
const showInviteModal = ref(false)

// Computed
const teamId = computed(() => Number(route.params.id))
const isTeamMember = computed(() => {
  return members.value.some(member => member.user_id === authStore.user?.id)
})
const isTeamOwner = computed(() => {
  return members.value.some(member =>
    member.user_id === authStore.user?.id && member.role === 'owner'
  )
})
const isTeamFull = computed(() => {
  return members.value.length >= (team.value?.max_members || 5)
})

// Methods
function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}

async function loadTeam() {
  loading.value = true
  error.value = null

  try {
    team.value = await teamStore.fetchTeam(teamId.value)
    members.value = teamStore.teamMembers.get(teamId.value) || []

    // Load team invitations
    invitations.value = await teamStore.fetchTeamInvitations(teamId.value)

    // Load team projects
    await loadTeamProjects()
  } catch (err) {
    error.value = err instanceof Error ? err.message : t('teams.failedToLoadTeam')
    console.error('Failed to load team:', err)
  } finally {
    loading.value = false
  }
}

async function loadTeamProjects() {
  if (!teamId.value) return

  projectsLoading.value = true
  try {
    projects.value = await teamStore.fetchTeamProjects(teamId.value, 0, 10)
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

  try {
    // For open teams, users can join directly
    if (team.value.is_open) {
      await teamStore.joinTeam(teamId.value)
      uiStore.showSuccess(t('teams.joinedTeamSuccess'))
      await loadTeam()
    } else {
      uiStore.showInfo(t('teams.teamClosedMessage'), t('teams.closedTeam'))
    }
  } catch (err) {
    console.error('Failed to join team:', err)
  }
}

async function leaveTeam() {
  if (!authStore.user?.id) return
  showLeaveConfirm.value = true
}

async function confirmLeave() {
  if (!authStore.user?.id) return
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

async function removeMember(userId: number) {
  if (!isTeamOwner.value) return

  try {
    const confirmed = confirm(t('teams.confirmRemoveMember'))
    if (!confirmed) return

    await teamStore.removeTeamMember(teamId.value, userId)
    uiStore.showSuccess(t('teams.memberRemovedSuccess'))
    await loadTeam()
  } catch (err) {
    console.error('Failed to remove member:', err)
  }
}

async function makeOwner(userId: number) {
  if (!isTeamOwner.value) return

  try {
    const confirmed = confirm(t('teams.confirmMakeOwner'))
    if (!confirmed) return

    await teamStore.updateTeamMemberRole(teamId.value, userId, 'owner')
    await loadTeam()
  } catch (err) {
    console.error('Failed to make member owner:', err)
  }
}

async function makeMember(userId: number) {
  if (!isTeamOwner.value) return

  try {
    const confirmed = confirm(t('teams.confirmDemoteOwner'))
    if (!confirmed) return

    await teamStore.updateTeamMemberRole(teamId.value, userId, 'member')
    await loadTeam()
  } catch (err) {
    console.error('Failed to make owner member:', err)
  }
}

function editTeam() {
  router.push(`/teams/${teamId.value}/edit`)
}

function inviteMember(teamId: string) {
  showInviteModal.value = true
}

function closeInviteModal() {
  showInviteModal.value = false
}

function handleInviteSent(payload: { userId: number, username: string }) {
  uiStore.showSuccess(t('teams.invitationSent'))
  closeInviteModal()
  // Reload team to update member list
  loadTeam()
}

function handleInviteError(payload: { message: string, code?: string }) {
  uiStore.showError(payload.message, t('teams.invitationFailed'))
}

// Invitation action handlers
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

async function handleResendInvitation(invitationId: string) {
  // Not implemented yet - would need a resend endpoint
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

function deleteTeam() {
  // Implement delete team logic
  console.log('Delete team:', teamId.value)
}

function createProject() {
  if (team.value?.hackathon) {
    router.push(`/create/hackathon?hackathon=${team.value.hackathon.id}&team=${teamId.value}`)
  } else {
    router.push('/create/hackathon')
  }
}

function viewProject(projectId: number) {
  router.push(`/projects/${projectId}`)
}

// Lifecycle
onMounted(() => {
  loadTeam()
})
</script>

<style scoped>
.container {
  max-width: 1280px;
}
</style>
