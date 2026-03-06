<template>
  <div class="team-invitations-panel">
    <div class="panel-header mb-6">
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">
            Team Invitations
          </h2>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Manage pending invitations and invite new members
          </p>
        </div>
        <button
          type="button"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          @click="showInviteForm = true"
        >
          <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Invite Member
        </button>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-state text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">Loading invitations...</p>
    </div>
    
    <!-- Content -->
    <div v-else class="panel-content">
      <!-- Stats -->
      <div class="stats-grid grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="stat-item bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
          <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
            {{ stats.total }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Total Invitations
          </div>
        </div>
        <div class="stat-item bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
          <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
            {{ stats.pending }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Pending
          </div>
        </div>
        <div class="stat-item bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
          <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
            {{ stats.accepted }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Accepted
          </div>
        </div>
      </div>
      
      <!-- Invitations List -->
      <div class="invitations-list">
        <div v-if="invitations.length > 0" class="space-y-4">
          <TeamInvitationItem
            v-for="invitation in invitations"
            :key="invitation.id"
            :invitation="invitation"
            :team="team"
            @accept="onAcceptInvitation"
            @reject="onRejectInvitation"
            @resend="onResendInvitation"
            @cancel="onCancelInvitation"
          />
        </div>
        <div v-else class="empty-state text-center py-12">
          <svg class="h-16 w-16 mx-auto text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          <h3 class="mt-4 text-lg font-medium text-gray-900 dark:text-gray-100">
            No invitations yet
          </h3>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Invite members to join your team by clicking the "Invite Member" button.
          </p>
        </div>
      </div>
    </div>
    
    <!-- Invite Form Modal -->
    <div v-if="showInviteForm" class="fixed inset-0 bg-gray-500 dark:bg-gray-900 bg-opacity-75 dark:bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg max-w-md w-full p-6">
        <div class="modal-header mb-4">
          <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100">
            Invite Member
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Invite someone to join your team
          </p>
        </div>
        
        <div class="modal-body">
          <div class="space-y-4">
            <!-- Invite Type -->
            <div class="form-group">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Invite Type
              </label>
              <div class="space-y-2">
                <div class="flex items-center">
                  <input
                    id="invite-email"
                    v-model="inviteType"
                    type="radio"
                    value="email"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600"
                  />
                  <label for="invite-email" class="ml-3 block text-sm font-medium text-gray-700 dark:text-gray-300">
                    <span class="font-semibold">Email Address</span>
                    <span class="text-gray-500 dark:text-gray-400 block text-xs mt-1">
                      Invite by email address
                    </span>
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    id="invite-user"
                    v-model="inviteType"
                    type="radio"
                    value="user"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600"
                  />
                  <label for="invite-user" class="ml-3 block text-sm font-medium text-gray-700 dark:text-gray-300">
                    <span class="font-semibold">Existing User</span>
                    <span class="text-gray-500 dark:text-gray-400 block text-xs mt-1">
                      Invite an existing platform user
                    </span>
                  </label>
                </div>
              </div>
            </div>
            
            <!-- Email Input -->
            <div v-if="inviteType === 'email'" class="form-group">
              <label for="invite-email-input" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Email Address *
              </label>
              <input
                id="invite-email-input"
                v-model="inviteData.email"
                type="email"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
                :class="{ 'border-red-300 dark:border-red-600': errors.email }"
                placeholder="user@example.com"
              />
              <p v-if="errors.email" class="mt-1 text-sm text-red-600 dark:text-red-400">
                {{ errors.email }}
              </p>
            </div>
            
            <!-- User Search -->
            <div v-if="inviteType === 'user'" class="form-group">
              <label for="invite-user-search" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Search Users *
              </label>
              <input
                id="invite-user-search"
                v-model="userSearch"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
                placeholder="Search by username or email"
                @input="searchUsers"
              />
              <div v-if="searchResults.length > 0" class="mt-2 border border-gray-200 dark:border-gray-700 rounded-md max-h-48 overflow-y-auto">
                <div
                  v-for="user in searchResults"
                  :key="user.id"
                  class="p-3 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer border-b border-gray-100 dark:border-gray-700 last:border-b-0"
                  @click="selectUser(user)"
                >
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-8 w-8 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center">
                      <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
                        {{ user.displayName?.charAt(0) || user.username?.charAt(0) || 'U' }}
                      </span>
                    </div>
                    <div class="ml-3">
                      <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
                        {{ user.displayName || user.username }}
                      </p>
                      <p class="text-xs text-gray-500 dark:text-gray-400">
                        {{ user.email || 'No email' }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <p v-if="errors.userId" class="mt-1 text-sm text-red-600 dark:text-red-400">
                {{ errors.userId }}
              </p>
            </div>
            
            <!-- Role Selection -->
            <div class="form-group">
              <label for="invite-role" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Role *
              </label>
              <select
                id="invite-role"
                v-model="inviteData.role"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
                :class="{ 'border-red-300 dark:border-red-600': errors.role }"
              >
                <option value="member">Member</option>
                <option value="admin">Admin</option>
              </select>
              <p v-if="errors.role" class="mt-1 text-sm text-red-600 dark:text-red-400">
                {{ errors.role }}
              </p>
            </div>
            
            <!-- Message -->
            <div class="form-group">
              <label for="invite-message" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Message (Optional)
              </label>
              <textarea
                id="invite-message"
                v-model="inviteData.message"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
                placeholder="Add a personal message to your invitation"
              />
              <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                Optional. This message will be included in the invitation.
              </p>
            </div>
          </div>
        </div>
        
        <div class="modal-footer flex justify-end space-x-4 mt-6">
          <button
            type="button"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
            @click="closeInviteForm"
          >
            Cancel
          </button>
          <button
            type="button"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            :disabled="sending"
            @click="sendInvitation"
          >
            <span v-if="sending" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Sending...
            </span>
            <span v-else>
              Send Invitation
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import type { Team, TeamInvitation, TeamMemberUser } from '~/types/team-types'
import TeamInvitationItem from '~/components/molecules/teams/TeamInvitationItem.vue'

const props = withDefaults(defineProps<{
  team: Team
  invitations: TeamInvitation[]
  loading?: boolean
}>(), {
  invitations: () => [],
  loading: false,
})

const emit = defineEmits<{
  invite: [data: { email?: string; userId?: string; role: string; message?: string }]
  'accept-invitation': [invitationId: string]
  'reject-invitation': [invitationId: string]
  'resend-invitation': [invitationId: string]
  'cancel-invitation': [invitationId: string]
}>()

// UI state
const showInviteForm = ref(false)
const inviteType = ref<'email' | 'user'>('email')
const userSearch = ref('')
const searchResults = ref<TeamMemberUser[]>([])
const sending = ref(false)
const errors = reactive<Record<string, string>>({})

// Form data
const inviteData = reactive({
  email: '',
  userId: '',
  role: 'member',
  message: '',
})

// Computed properties
const stats = computed(() => {
  const total = props.invitations.length
  const pending = props.invitations.filter(i => i.status === 'pending').length
  const accepted = props.invitations.filter(i => i.status === 'accepted').length
  const rejected = props.invitations.filter(i => i.status === 'rejected').length
  const expired = props.invitations.filter(i => i.status === 'expired').length
  
  return { total, pending, accepted, rejected, expired }
})

// Methods
const searchUsers = () => {
  // In a real app, this would call an API
  // For now, we'll simulate search results
  if (userSearch.value.trim().length < 2) {
    searchResults.value = []
    return
  }
  
  // Mock search results
  searchResults.value = [
    {
      id: 'user1',
      username: 'johndoe',
      displayName: 'John Doe',
      email: 'john@example.com',
      avatarUrl: null,
      bio: null,
      skills: [],
    },
    {
      id: 'user2',
      username: 'janedoe',
      displayName: 'Jane Doe',
      email: 'jane@example.com',
      avatarUrl: null,
      bio: null,
      skills: [],
    },
  ]
}

const selectUser = (user: TeamMemberUser) => {
  inviteData.userId = user.id
  userSearch.value = user.displayName || user.username || user.email || ''
  searchResults.value = []
}

const validateInviteForm = (): boolean => {
  // Clear previous errors
  Object.keys(errors).forEach(key => delete errors[key])
  
  let isValid = true
  
  if (inviteType.value === 'email') {
    if (!inviteData.email.trim()) {
      errors.email = 'Email address is required'
      isValid = false
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(inviteData.email)) {
      errors.email = 'Please enter a valid email address'
      isValid = false
    }
  } else {
    if (!inviteData.userId.trim()) {
      errors.userId = 'Please select a user'
      isValid = false
    }
  }
  
  if (!inviteData.role) {
    errors.role = 'Role is required'
    isValid = false
  }
  
  return isValid
}

const sendInvitation = async () => {
  if (!validateInviteForm()) {
    return
  }
  
  sending.value = true
  
  try {
    // Prepare invitation data
    const invitationData: { email?: string; userId?: string; role: string; message?: string } = {
      role: inviteData.role,
    }
    
    if (inviteType.value === 'email') {
      invitationData.email = inviteData.email
    } else {
      invitationData.userId = inviteData.userId
    }
    
    if (inviteData.message.trim()) {
      invitationData.message = inviteData.message.trim()
    }
    
    // Emit invite event
    emit('invite', invitationData)
    
    // Reset form
    closeInviteForm()
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
  } catch (error) {
    console.error('Failed to send invitation:', error)
    errors.general = 'Failed to send invitation. Please try again.'
  } finally {
    sending.value = false
  }
}

const closeInviteForm = () => {
  showInviteForm.value = false
  resetInviteForm()
}

const resetInviteForm = () => {
  inviteData.email = ''
  inviteData.userId = ''
  inviteData.role = 'member'
  inviteData.message = ''
  userSearch.value = ''
  searchResults.value = []
  Object.keys(errors).forEach(key => delete errors[key])
}

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
</script>

<style scoped>
.stats-grid {
  display: grid;
}

.invitations-list {
  min-height: 200px;
}

.empty-state {
  border: 2px dashed #e5e7eb;
  border-radius: 0.5rem;
}

.dark .empty-state {
  border-color: #4b5563;
}

.modal-footer button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
