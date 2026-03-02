<template>
  <div v-if="loading" class="container mx-auto px-4 py-8 text-center">
    <LoadingSpinner size="lg" color="primary" />
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
    <button @click="loadTeam" class="btn btn-outline">{{ t('common.tryAgain') }}</button>
  </div>

  <div v-else-if="team" class="container mx-auto px-4 py-8">
    <TeamDetailHeader :team="team" :is-owner="isTeamOwner" :is-member="isTeamMember" :is-full="isTeamFull" @edit="editTeam" @leave="leaveTeam" @join="joinTeam" />

    <!-- Team Info -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left Column: Team Details -->
      <div class="lg:col-span-2">
        <!-- Description -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ t('common.description') }}</h3>
          <p class="text-gray-600 dark:text-gray-400 whitespace-pre-line">
            {{ team.description || t('teams.noDescriptionProvided') }}
          </p>
        </div>

        <!-- Members -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
          <TeamMembers :members="members" :current-user-id="authStore.user?.id ? Number(authStore.user.id) : null"
            :is-team-owner="isTeamOwner" :max-members="team.max_members" :loading="false" :error="null"
            :show-member-badge="false" :format-date="formatDate"
            @make-owner="makeOwner" @make-member="makeMember" @remove-member="removeMember" @retry="loadTeam" />
        </div>

        <!-- Atomic Design Invite Section (for owners) -->
        <TeamInviteSection
          v-if="isTeamOwner"
          :team-id="teamId"
          :is-team-owner="isTeamOwner"
          :is-team-full="isTeamFull"
          :current-member-count="members.length"
          :max-members="team.max_members"
          :disabled="inviting"
          :exclude-user-ids="memberIds"
          @invite-sent="handleAtomicInviteSent"
          @error="handleAtomicInviteError"
          @search="handleAtomicInviteSearch"
        />

        <!-- Atomic Design Team Invitations (visible to team members) -->
        <TeamInvitations
          v-if="isTeamMember"
          :team-id="teamId"
          :is-team-owner="isTeamOwner"
          :auto-load="true"
          :poll-interval="30000"
          @invitation-cancelled="handleInvitationCancelled"
          @error="handleInvitationsError"
        />

        <!-- Team Projects -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mt-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ t('teams.teamProjects') }}</h3>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              {{ projects.length }} {{ t('teams.projects') }}
            </div>
          </div>

          <div v-if="projectsLoading" class="text-center py-8">
            <LoadingSpinner size="md" color="primary" />
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
            <NuxtLink v-if="isTeamMember && team.hackathon"
              :to="`/create?hackathon=${team.hackathon.id}&team=${teamId}`" class="inline-block mt-4 btn btn-primary">
              {{ t('teams.createProject') }}
            </NuxtLink>
          </div>

          <div v-else class="space-y-4">
            <div v-for="project in projects" :key="project.id"
              class="p-4 rounded-lg border border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center mb-2">
                    <NuxtLink :to="`/projects/${project.id}`"
                      class="font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400">
                      {{ project.name }}
                    </NuxtLink>
                    <span v-if="project.hackathon"
                      class="ml-2 px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300 rounded-full">
                      {{ project.hackathon.name }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
                    {{ project.description }}
                  </p>
                  <div class="flex flex-wrap gap-2 mb-3">
                    <span v-for="tech in project.tech_stack?.slice(0, 3)" :key="tech"
                      class="px-2 py-1 text-xs font-medium bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200 rounded-full">
                      {{ tech }}
                    </span>
                    <span v-if="project.tech_stack && project.tech_stack.length > 3"
                      class="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300 rounded-full">
                      +{{ project.tech_stack.length - 3 }}
                    </span>
                  </div>
                  <div class="flex items-center text-sm text-gray-500 dark:text-gray-400">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {{ formatDate(project.created_at) }}
                  </div>
                </div>
                <div class="ml-4">
                  <NuxtLink :to="`/projects/${project.id}`"
                    class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300">
                    {{ t('teams.viewProject') }}
                  </NuxtLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Team Stats & Info -->
      <div class="lg:col-span-1">
        <TeamSidebar :team="team" :members="members" :is-owner="isTeamOwner" @edit="editTeam" @delete="deleteTeam" />
      </div>
    </div>

    <!-- Leave Team Confirmation Dialog -->
    <ConfirmDialog
      v-model="showLeaveConfirm"
      :title="t('teams.confirmLeaveTeamTitle')"
      :description="t('teams.confirmLeaveTeam')"
      :confirm-text="t('teams.leaveTeam')"
      :cancel-text="t('common.cancel')"
      destructive
      @confirm="confirmLeave"
      @cancel="cancelLeave"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from '#app'
import { useTeamStore } from '~/stores/team'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'
import TeamDetailHeader from '~/components/teams/TeamDetailHeader.vue'
import TeamSidebar from '~/components/teams/TeamSidebar.vue'
import TeamMembers from '~/components/organisms/teams/TeamMembers.vue'
import TeamInvitations from '~/components/organisms/teams/TeamInvitations.vue'
import TeamInviteSection from '~/components/organisms/teams/TeamInviteSection.vue'
import LoadingSpinner from '~/components/atoms/LoadingSpinner.vue'
import ConfirmDialog from '~/components/organisms/ConfirmDialog.vue'
import { useTeamMembers } from '~/composables/useTeamMembers'

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
const projects = ref<any[]>([])
const projectsLoading = ref(false)
const invitations = ref<any[]>([])
const invitationsLoading = ref(false)
const inviteUsername = ref('')
const inviting = ref(false)
const userSuggestions = ref<any[]>([])
const searching = ref(false)
const showSuggestions = ref(false)
const showLeaveConfirm = ref(false)
let searchTimeout: NodeJS.Timeout | null = null

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

const pendingInvitations = computed(() => {
  return invitations.value.filter(inv => inv.status === 'pending')
})

const memberIds = computed(() => {
  return members.value.map(member => member.user_id)
})

// Methods
function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}

function handleAvatarError(event: Event) {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  // The parent div will show the fallback initials automatically
  // because we're using v-if/v-else
}

async function loadTeam() {
  loading.value = true
  error.value = null

  try {
    team.value = await teamStore.fetchTeam(teamId.value)
    members.value = teamStore.teamMembers.get(teamId.value) || []

    // Load team projects
    await loadTeamProjects()

    // Load team invitations (only for team members)
    if (isTeamMember.value) {
      await loadTeamInvitations()
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : t('teams.failedToLoadTeam')
    console.error('Failed to load team:', err)
  } finally {
    loading.value = false
  }
}

async function loadTeamInvitations() {
  if (!teamId.value) return

  invitationsLoading.value = true
  try {
    invitations.value = await teamStore.fetchTeamInvitations(teamId.value)
  } catch (err) {
    console.error('Failed to load team invitations:', err)
    invitations.value = []
  } finally {
    invitationsLoading.value = false
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
      await teamStore.addTeamMember(teamId.value, authStore.user.id, 'member')
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
    await teamStore.removeTeamMember(teamId.value, authStore.user.id)
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

async function searchUsers() {
  const query = inviteUsername.value.trim()

  if (!query || query.length < 2) {
    userSuggestions.value = []
    showSuggestions.value = false
    return
  }

  // Clear previous timeout
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }

  // Debounce search to avoid too many API calls
  searchTimeout = setTimeout(async () => {
    searching.value = true
    try {
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'
      const response = await authStore.fetchWithAuth(`/api/users?username=${encodeURIComponent(query)}&limit=8`)

      if (response.ok) {
        const users = await response.json()
        console.log('Search results:', users, 'for query:', query)
        // Filter out users who are already team members
        const memberUserIds = new Set(
          members.value
            .map(m => m.user_id)
            .filter(id => id != null)
            .map(id => Number(id))
        )
        const filteredUsers = users.filter((user: any) => {
          const userId = Number(user.id)
          return !memberUserIds.has(userId)
        })
        console.log('Filtered users:', filteredUsers, 'member IDs:', Array.from(memberUserIds))
        userSuggestions.value = filteredUsers
        showSuggestions.value = true
      } else {
        console.error('Search failed with status:', response.status, response.statusText)
        const errorText = await response.text().catch(() => '')
        console.error('Error response:', errorText)
      }
    } catch (err) {
      console.error('Failed to search users:', err)
      console.error('Error details:', err)
      userSuggestions.value = []
    } finally {
      searching.value = false
    }
  }, 300)
}

function selectUser(user: any) {
  inviteUsername.value = user.username
  userSuggestions.value = []
  showSuggestions.value = false
}

function onInputBlur() {
  // Delay hiding suggestions to allow click on suggestion
  setTimeout(() => {
    showSuggestions.value = false
  }, 200)
}

async function sendInvitation() {
  if (!inviteUsername.value.trim()) return

  inviting.value = true
  try {
    // First, we need to get the user ID from username
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    const response = await authStore.fetchWithAuth(`/api/users?username=${encodeURIComponent(inviteUsername.value)}`)

    if (!response.ok) {
      throw new Error(t('teams.userNotFound'))
    }

    const users = await response.json()
    if (users.length === 0) {
      throw new Error(t('teams.userNotFound'))
    }

    const user = users[0]

    // Send invitation
    await teamStore.inviteToTeam(teamId.value, user.id)
    inviteUsername.value = ''
    userSuggestions.value = []
    showSuggestions.value = false

    // Refresh invitations list
    if (isTeamMember.value) {
      await loadTeamInvitations()
    }
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : t('teams.invitationError')
    uiStore.showError(errorMsg, t('teams.invitationError'))
  } finally {
    inviting.value = false
  }
}

async function cancelInvitation(invitationId: number) {
  if (!isTeamOwner.value) return

  try {
    const confirmed = confirm('Are you sure you want to cancel this invitation?')
    if (!confirmed) return

    await teamStore.cancelInvitation(invitationId)
    uiStore.showSuccess('Invitation cancelled successfully')

    // Refresh invitations list
    await loadTeamInvitations()
  } catch (err) {
    console.error('Failed to cancel invitation:', err)
  }
}

// Atomic Design Event Handlers
function handleAtomicInviteSent(payload: { userId: number, username: string }) {
  console.log('Atomic invite sent:', payload)
  
  // The invitation is already sent by InviteUserForm via useTeamInvitations composable
  // This handler is for additional side effects like analytics or notifications
  
  // Refresh invitations if needed (already done by useTeamInvitations, but we can double-check)
  if (isTeamMember.value) {
    loadTeamInvitations()
  }
}

function handleAtomicInviteError(payload: { message: string, code?: string }) {
  console.error('Atomic invite error:', payload)
  uiStore.showError(payload.message, t('teams.invitationFailed'))
}

function handleAtomicInviteSearch(payload: { query: string }) {
  console.log('Atomic invite search:', payload)
  // Can be used for analytics or additional processing
}

function handleInvitationCancelled(payload: { invitationId: number }) {
  console.log('Invitation cancelled:', payload)
  uiStore.showSuccess(t('teams.invitationCancelledSuccess'))
  // Refresh invitations
  if (isTeamMember.value) {
    loadTeamInvitations()
  }
}

function handleInvitationsError(payload: { message: string, code?: string }) {
  console.error('Invitations error:', payload)
  uiStore.showError(payload.message, t('teams.failedToLoadInvitations'))
}

function editTeam() {
  router.push(`/teams/${teamId.value}/edit`)
}

async function deleteTeam() {
  if (!isTeamOwner.value) return

  try {
    const confirmed = confirm(t('teams.confirmDeleteTeam'))
    if (!confirmed) return

    await teamStore.deleteTeam(teamId.value)
    uiStore.showSuccess(t('teams.teamDeletedSuccess'))
    router.push('/teams')
  } catch (err) {
    console.error('Failed to delete team:', err)
  }
}

// Lifecycle
onMounted(() => {
  loadTeam()
})
</script>

<style scoped>
.team-member-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  font-size: 0.875rem;
}

.team-member-avatar.owner {
  background-color: #dbeafe;
  color: #1d4ed8;
}

.dark .team-member-avatar.owner {
  background-color: #1e3a8a;
  color: #93c5fd;
}
</style>