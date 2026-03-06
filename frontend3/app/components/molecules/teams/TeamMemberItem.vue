<template>
  <div class="team-member-item" :class="itemClasses">
    <!-- Member Info -->
    <div class="member-info">
      <TeamMemberAvatar
        :member="member"
        size="md"
        :show-name="true"
        :show-role="true"
      />
      
      <!-- Additional Member Details -->
      <div v-if="!compact" class="member-details">
        <div class="member-name-role">
          <span class="member-name">
            {{ member.user?.displayName || member.user?.username || 'Unknown User' }}
          </span>
          <TeamRoleBadge
            :role="member.role"
            size="sm"
            class="ml-2"
          />
        </div>
        
        <!-- Member Skills -->
        <div v-if="member.user?.skills && member.user.skills.length > 0" class="member-skills">
          <div class="flex flex-wrap gap-1 mt-1">
            <span
              v-for="skill in member.user.skills.slice(0, 3)"
              :key="skill"
              class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
            >
              {{ skill }}
            </span>
            <span
              v-if="member.user.skills.length > 3"
              class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200"
            >
              +{{ member.user.skills.length - 3 }}
            </span>
          </div>
        </div>
        
        <!-- Join Date -->
        <div class="join-date text-xs text-gray-500 dark:text-gray-400">
          Joined {{ formatDate(member.joinedAt) }}
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div v-if="showActions && canManageTeam" class="member-actions">
      <!-- Role Dropdown -->
      <div v-if="member.user?.id !== team.createdBy" class="role-dropdown">
        <select
          :value="member.role"
          :disabled="!canChangeRole"
          class="text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          @change="handleRoleChange($event)"
        >
          <option value="member">Member</option>
          <option value="admin">Admin</option>
          <option v-if="member.role === 'owner'" value="owner" disabled>Owner</option>
        </select>
      </div>
      
      <!-- Remove Button -->
      <button
        v-if="canRemoveMember"
        type="button"
        class="remove-button text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300"
        :disabled="removing"
        @click="handleRemove"
      >
        <span v-if="removing" class="flex items-center">
          <svg class="animate-spin h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          Removing...
        </span>
        <span v-else class="flex items-center">
          <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Remove
        </span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { TeamMemberItemProps } from '~/types/team-types'
import TeamMemberAvatar from '~/components/atoms/teams/TeamMemberAvatar.vue'
import TeamRoleBadge from '~/components/atoms/teams/TeamRoleBadge.vue'

const props = withDefaults(defineProps<TeamMemberItemProps & {
  compact?: boolean
}>(), {
  currentUserId: null,
  showActions: true,
  compact: false,
})

const emit = defineEmits<{
  'role-update': [memberId: string, role: string]
  remove: [memberId: string]
}>()

const removing = ref(false)

// Berechne Berechtigungen
const isCurrentUser = computed(() => props.member.user?.id === props.currentUserId)
const isTeamOwner = computed(() => props.member.user?.id === props.team.createdBy)
const isCurrentUserOwner = computed(() => props.currentUserId === props.team.createdBy)
const isCurrentUserAdmin = computed(() => {
  // Hier müsste die Logik für Admin-Berechtigung implementiert werden
  return false
})

const canManageTeam = computed(() => isCurrentUserOwner.value || isCurrentUserAdmin.value)
const canChangeRole = computed(() => canManageTeam.value && !isTeamOwner.value)
const canRemoveMember = computed(() => {
  if (!canManageTeam.value) return false
  if (isTeamOwner.value) return false // Owner kann nicht entfernt werden
  if (isCurrentUser.value) return false // Kann sich selbst nicht entfernen
  return true
})

// CSS-Klassen
const itemClasses = computed(() => ({
  'compact': props.compact,
  'has-actions': props.showActions && canManageTeam.value,
  'is-current-user': isCurrentUser.value,
  'is-team-owner': isTeamOwner.value,
}))

// Formatierungsfunktionen
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
}

// Event-Handler
const handleRoleChange = (event: Event) => {
  const select = event.target as HTMLSelectElement
  const newRole = select.value
  emit('role-update', props.member.id, newRole)
}

const handleRemove = () => {
  if (confirm(`Are you sure you want to remove ${props.member.user?.displayName || 'this member'} from the team?`)) {
    removing.value = true
    emit('remove', props.member.id)
    // Reset removing state after a delay (should be reset by parent)
    setTimeout(() => {
      removing.value = false
    }, 3000)
  }
}
</script>

<style scoped>
.team-member-item {
  @apply flex items-center justify-between p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200;
}

.member-info {
  @apply flex items-center space-x-4 flex-1;
}

.member-details {
  @apply flex-1 min-w-0;
}

.member-name-role {
  @apply flex items-center mb-1;
}

.member-name {
  @apply text-sm font-medium text-gray-900 dark:text-gray-100 truncate;
}

.member-stats {
  @apply flex items-center text-xs text-gray-600 dark:text-gray-400 mb-1;
}

.stat-item {
  @apply flex items-center;
}

.join-date {
  @apply mt-1;
}

.member-actions {
  @apply flex items-center space-x-3;
}

.role-dropdown select {
  @apply text-sm;
}

.remove-button {
  @apply text-sm font-medium transition-colors duration-200;
}

.remove-button:disabled {
  @apply opacity-50 cursor-not-allowed;
}

/* Compact mode */
.team-member-item.compact {
  @apply p-2;
}

.team-member-item.compact .member-details {
  @apply hidden;
}
</style>