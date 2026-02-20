<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Team Invitations</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        Manage your pending team invitations
      </p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">Loading invitations...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-12">
      <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400 mb-4">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Error Loading Invitations</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
      <button @click="loadInvitations" class="btn btn-outline">Try Again</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="invitations.length === 0" class="text-center py-12">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 mb-4">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No Pending Invitations</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        You don't have any pending team invitations at the moment.
      </p>
      <router-link to="/teams" class="btn btn-primary">
        Browse Teams
      </router-link>
    </div>

    <!-- Invitations List -->
    <div v-else class="space-y-6">
      <div
        v-for="invitation in invitations"
        :key="invitation.id"
        class="bg-white dark:bg-gray-800 rounded-lg shadow p-6"
      >
        <div class="flex flex-col md:flex-row md:items-start justify-between">
          <!-- Invitation Info -->
          <div class="mb-4 md:mb-0">
            <div class="flex items-center mb-2">
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                {{ invitation.team?.name || 'Unknown Team' }}
              </h3>
              <span
                v-if="invitation.status === 'pending'"
                class="ml-3 px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200 rounded-full"
              >
                Pending
              </span>
              <span
                v-else-if="invitation.status === 'accepted'"
                class="ml-3 px-2 py-1 text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 rounded-full"
              >
                Accepted
              </span>
              <span
                v-else
                class="ml-3 px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300 rounded-full"
              >
                Declined
              </span>
            </div>
            
            <div class="space-y-2">
              <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>Invited {{ formatDate(invitation.created_at) }}</span>
              </div>
              
              <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span>Invited by: {{ invitation.inviter?.username || 'Unknown User' }}</span>
              </div>
              
              <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span>Hackathon: {{ invitation.team?.hackathon?.name || 'Unknown' }}</span>
              </div>
            </div>
            
            <div v-if="invitation.message" class="mt-4 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <p class="text-sm text-gray-600 dark:text-gray-400">
                <span class="font-medium">Message:</span> {{ invitation.message }}
              </p>
            </div>
          </div>
          
          <!-- Actions -->
          <div v-if="invitation.status === 'pending'" class="flex space-x-3">
            <button
              @click="declineInvitation(invitation.id)"
              class="btn btn-outline text-red-600 dark:text-red-400 border-red-300 dark:border-red-700 hover:bg-red-50 dark:hover:bg-red-900/20"
              :disabled="processingInvitation === invitation.id"
            >
              <span v-if="processingInvitation === invitation.id && actionType === 'decline'">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Declining...
              </span>
              <span v-else>Decline</span>
            </button>
            <button
              @click="acceptInvitation(invitation.id)"
              class="btn btn-primary"
              :disabled="processingInvitation === invitation.id"
            >
              <span v-if="processingInvitation === invitation.id && actionType === 'accept'">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Accepting...
              </span>
              <span v-else>Accept Invitation</span>
            </button>
          </div>
          
          <div v-else class="text-sm text-gray-600 dark:text-gray-400">
            <p>
              {{ invitation.status === 'accepted' ? 'You accepted this invitation' : 'You declined this invitation' }}
              {{ formatDate(invitation.updated_at) }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTeamStore } from '~/stores/team'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

const teamStore = useTeamStore()
const authStore = useAuthStore()
const uiStore = useUIStore()

// State
const loading = ref(true)
const error = ref<string | null>(null)
const invitations = ref<any[]>([])
const processingInvitation = ref<number | null>(null)
const actionType = ref<'accept' | 'decline' | null>(null)

// Methods
function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}

async function loadInvitations() {
  loading.value = true
  error.value = null
  
  try {
    invitations.value = await teamStore.fetchMyInvitations()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load invitations'
    console.error('Failed to load invitations:', err)
  } finally {
    loading.value = false
  }
}

async function acceptInvitation(invitationId: number) {
  processingInvitation.value = invitationId
  actionType.value = 'accept'
  
  try {
    await teamStore.acceptInvitation(invitationId)
    uiStore.showSuccess('Invitation accepted! You are now a member of the team.')
    
    // Reload invitations
    await loadInvitations()
  } catch (err) {
    console.error('Failed to accept invitation:', err)
  } finally {
    processingInvitation.value = null
    actionType.value = null
  }
}

async function declineInvitation(invitationId: number) {
  processingInvitation.value = invitationId
  actionType.value = 'decline'
  
  try {
    await teamStore.declineInvitation(invitationId)
    uiStore.showSuccess('Invitation declined')
    
    // Reload invitations
    await loadInvitations()
  } catch (err) {
    console.error('Failed to decline invitation:', err)
  } finally {
    processingInvitation.value = null
    actionType.value = null
  }
}

// Lifecycle
onMounted(() => {
  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    uiStore.showError('You must be logged in to view invitations', 'Authentication Required')
    return
  }
  
  loadInvitations()
})
</script>