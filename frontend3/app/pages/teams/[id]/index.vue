<template>
  <div v-if="loading" class="container mx-auto px-4 py-8 text-center">
    <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    <p class="mt-4 text-gray-600 dark:text-gray-400">{{ t('teams.loadingTeam') }}</p>
  </div>

  <div v-else-if="error" class="container mx-auto px-4 py-8 text-center">
    <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400 mb-4">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </div>
    <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">{{ t('teams.errorLoadingTeam') }}</h3>
    <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
    <button @click="loadTeam" class="btn btn-outline">{{ t('common.tryAgain') }}</button>
  </div>

  <div v-else-if="team" class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-start justify-between mb-8">
      <div>
        <div class="flex items-center mb-2">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ team.name }}</h1>
          <span
            :class="[
              'ml-3 px-2 py-1 text-xs font-medium rounded-full',
              team.is_open
                ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
            ]"
          >
            {{ team.is_open ? t('teams.open') : t('teams.closed') }}
          </span>
        </div>
        <p class="text-gray-600 dark:text-gray-400">
          {{ t('teams.teamFor', { hackathon: '' }) }}
          <NuxtLink 
            v-if="team.hackathon"
            :to="`/hackathons/${team.hackathon.id}`"
            class="text-primary-600 dark:text-primary-400 hover:underline"
          >
            {{ team.hackathon.name }}
          </NuxtLink>
          <span v-else class="text-gray-500 dark:text-gray-400">
            {{ t('common.unknownHackathon') }}
          </span>
        </p>
      </div>
      
      <div class="mt-4 md:mt-0 flex space-x-3">
        <button
          v-if="isTeamOwner"
          @click="editTeam"
          class="btn btn-outline"
        >
          {{ t('teams.editTeam') }}
        </button>
        <button
          v-if="isTeamMember"
          @click="leaveTeam"
          class="btn btn-outline text-red-600 dark:text-red-400 border-red-300 dark:border-red-700 hover:bg-red-50 dark:hover:bg-red-900/20"
        >
          {{ t('teams.leaveTeam') }}
        </button>
        <button
          v-else-if="team.is_open && !isTeamFull"
          @click="joinTeam"
          class="btn btn-primary"
        >
          {{ t('teams.joinTeam') }}
        </button>
      </div>
    </div>

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
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ t('teams.teamMembers') }}</h3>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              {{ members.length }} / {{ team.max_members }} {{ t('teams.members') }}
            </div>
          </div>

          <div v-if="members.length === 0" class="text-center py-8">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 mb-4">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p class="text-gray-600 dark:text-gray-400">{{ t('teams.noMembersYet') }}</p>
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="member in members"
              :key="member.id"
              class="flex items-center justify-between p-4 rounded-lg border border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50"
            >
              <div class="flex items-center">
                 <NuxtLink 
                   v-if="member.user"
                   :to="`/users/${member.user.id}`"
                   class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center mr-4 overflow-hidden hover:opacity-90 transition-opacity"
                 >
                   <img
                     v-if="member.user?.avatar_url"
                     :src="member.user.avatar_url"
                     :alt="member.user?.name || member.user?.username || t('teams.unknownUser')"
                     class="w-full h-full object-cover"
                     @error="handleAvatarError"
                   />
                   <span
                     v-else
                     class="text-sm font-medium text-primary-600 dark:text-primary-400"
                   >
                     {{ (member.user?.name || member.user?.username || t('teams.unknownUserInitial')).charAt(0).toUpperCase() }}
                   </span>
                 </NuxtLink>
                 <div v-else class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center mr-4 overflow-hidden">
                   <span class="text-sm font-medium text-primary-600 dark:text-primary-400">
                     {{ t('teams.unknownUserInitial').charAt(0).toUpperCase() }}
                   </span>
                 </div>
                 <div>
                   <div class="flex items-center">
                     <NuxtLink 
                       v-if="member.user"
                       :to="`/users/${member.user.id}`"
                       class="font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400"
                     >
                       {{ member.user?.name || member.user?.username || t('teams.unknownUser') }}
                     </NuxtLink>
                     <span v-else class="font-medium text-gray-900 dark:text-white">
                       {{ t('teams.unknownUser') }}
                     </span>
                     <span
                       v-if="member.role === 'owner'"
                       class="ml-2 px-2 py-0.5 text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 rounded-full"
                     >
                       {{ t('teams.owner') }}
                     </span>
                   </div>
                   <p class="text-sm text-gray-500 dark:text-gray-400">
                     {{ t('teams.joined') }} {{ formatDate(member.joined_at) }}
                   </p>
                 </div>
              </div>
              
              <div v-if="isTeamOwner && member.user_id !== authStore.user?.id" class="flex items-center space-x-2">
                <button
                  v-if="member.role === 'member'"
                  @click="makeOwner(member.user_id)"
                  class="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
                  :title="t('teams.makeOwner')"
                >
                  {{ t('teams.makeOwner') }}
                </button>
                <button
                  v-else
                  @click="makeMember(member.user_id)"
                  class="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-300"
                  :title="t('teams.makeMember')"
                >
                  {{ t('teams.makeMember') }}
                </button>
                <button
                  @click="removeMember(member.user_id)"
                  class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300"
                  :title="t('teams.confirmRemoveMember')"
                >
                  {{ t('common.remove') }}
                </button>
              </div>
            </div>
          </div>

          <!-- Invite Section (for owners) -->
          <div v-if="isTeamOwner && !isTeamFull" class="mt-8 pt-6 border-t border-gray-100 dark:border-gray-700">
            <h4 class="text-md font-medium text-gray-900 dark:text-white mb-4">{{ t('teams.inviteMembers') }}</h4>
            <div class="flex space-x-3">
              <input
                v-model="inviteUsername"
                type="text"
                :placeholder="t('teams.enterUsername')"
                class="flex-1 input"
                @keyup.enter="sendInvitation"
              />
              <button
                @click="sendInvitation"
                class="btn btn-primary"
                :disabled="!inviteUsername.trim() || inviting"
              >
                <span v-if="inviting">{{ t('teams.inviting') }}</span>
                <span v-else>{{ t('teams.invite') }}</span>
              </button>
            </div>
             <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">
               {{ t('teams.inviteUsernameHelp') }}
             </p>
          </div>
        </div>
      </div>

      <!-- Right Column: Team Stats & Info -->
      <div>
        <!-- Team Stats -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
           <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ t('teams.teamInfo') }}</h3>
          
          <div class="space-y-4">
            <div>
               <p class="text-sm text-gray-500 dark:text-gray-400">{{ t('teams.created') }}</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ formatDate(team.created_at) }}</p>
            </div>
            
            <div>
               <p class="text-sm text-gray-500 dark:text-gray-400">{{ t('teams.hackathon') }}</p>
               <p class="font-medium text-gray-900 dark:text-white">
                 <NuxtLink 
                   v-if="team.hackathon"
                   :to="`/hackathons/${team.hackathon.id}`"
                   class="text-primary-600 dark:text-primary-400 hover:underline"
                 >
                   {{ team.hackathon.name }}
                 </NuxtLink>
                 <span v-else class="text-gray-500 dark:text-gray-400">
                   {{ t('teams.unknown') }}
                 </span>
               </p>
            </div>
            
            <div>
               <p class="text-sm text-gray-500 dark:text-gray-400">{{ t('teams.teamSize') }}</p>
               <p class="font-medium text-gray-900 dark:text-white">{{ members.length }} / {{ team.max_members }} {{ t('teams.members') }}</p>
            </div>
            
            <div>
               <p class="text-sm text-gray-500 dark:text-gray-400">{{ t('teams.status') }}</p>
               <p class="font-medium text-gray-900 dark:text-white">
                 {{ team.is_open ? t('teams.openDescription') : t('teams.closedDescription') }}
               </p>
            </div>
            
             <div v-if="team.creator">
                <p class="text-sm text-gray-500 dark:text-gray-400">{{ t('teams.createdBy') }}</p>
               <div class="flex items-center mt-1">
                 <NuxtLink 
                   :to="`/users/${team.creator.id}`"
                   class="flex items-center hover:opacity-90 transition-opacity"
                 >
                   <div class="w-6 h-6 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center mr-2 overflow-hidden">
                     <img
                       v-if="team.creator.avatar_url"
                       :src="team.creator.avatar_url"
                       :alt="team.creator.username"
                       class="w-full h-full object-cover"
                       @error="handleAvatarError"
                     />
                     <span
                       v-else
                       class="text-xs font-medium text-primary-600 dark:text-primary-400"
                     >
                       {{ team.creator.username.charAt(0).toUpperCase() }}
                     </span>
                   </div>
                   <span class="font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400">{{ team.creator.username }}</span>
                 </NuxtLink>
               </div>
             </div>
          </div>
        </div>

        <!-- Actions (for owners) -->
        <div v-if="isTeamOwner" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
           <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ t('teams.teamManagement') }}</h3>
          
          <div class="space-y-3">
            <button
              @click="editTeam"
              class="w-full btn btn-outline justify-start"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
               {{ t('teams.editTeamDetails') }}
            </button>
            
            <button
              @click="deleteTeam"
              class="w-full btn btn-outline justify-start text-red-600 dark:text-red-400 border-red-300 dark:border-red-700 hover:bg-red-50 dark:hover:bg-red-900/20"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
               {{ t('teams.deleteTeam') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from '#app'
import { useTeamStore } from '~/stores/team'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'

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
const inviteUsername = ref('')
const inviting = ref(false)

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
  } catch (err) {
    error.value = err instanceof Error ? err.message : t('teams.failedToLoadTeam')
    console.error('Failed to load team:', err)
  } finally {
    loading.value = false
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

  try {
    const confirmed = confirm(t('teams.confirmLeaveTeam'))
    if (!confirmed) return

    await teamStore.removeTeamMember(teamId.value, authStore.user.id)
    uiStore.showSuccess(t('teams.leftTeamSuccess'))
    router.push('/teams')
  } catch (err) {
    console.error('Failed to leave team:', err)
  }
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
    uiStore.showSuccess(t('teams.invitationSentTo', { username: inviteUsername.value }))
    inviteUsername.value = ''
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : t('teams.invitationError')
    uiStore.showError(errorMsg, t('teams.invitationError'))
  } finally {
    inviting.value = false
  }
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