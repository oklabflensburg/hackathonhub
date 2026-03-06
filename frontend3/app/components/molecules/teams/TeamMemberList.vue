<template>
  <div class="team-member-list">
    <!-- Header -->
    <div v-if="!compact" class="mb-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
        {{ $t('teams.members.title') }}
      </h3>
      <p v-if="members.length > 0" class="text-sm text-gray-600 dark:text-gray-400 mt-1">
        {{ $t('teams.members.count', { count: members.length }) }}
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>

    <!-- Empty State -->
    <div v-else-if="members.length === 0" class="text-center py-8">
      <div class="text-gray-400 dark:text-gray-600 mb-3">
        <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <p class="text-gray-600 dark:text-gray-400">
        {{ $t('teams.members.empty') }}
      </p>
    </div>

    <!-- Member List -->
    <div v-else class="space-y-3">
      <!-- Visible Members -->
      <div v-for="member in visibleMembers" :key="member.id" class="flex items-center justify-between p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
        <!-- Member Info -->
        <div class="flex items-center space-x-3">
          <!-- Avatar -->
          <TeamMemberAvatar
            :member="member"
            :size="compact ? 'sm' : 'md'"
            :show-name="!compact"
            :show-role="!compact"
          />

          <!-- Member Details (only in non-compact mode) -->
          <div v-if="!compact" class="flex-1 min-w-0">
            <div class="flex items-center space-x-2">
              <span class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                {{ member.user?.displayName || member.user?.username || 'Unknown User' }}
              </span>
              <span v-if="member.user?.id === team.createdBy" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200">
                {{ $t('teams.roles.owner') }}
              </span>
            </div>
            <p v-if="member.user?.email" class="text-xs text-gray-500 dark:text-gray-400 truncate">
              {{ member.user.email }}
            </p>
          </div>
        </div>

        <!-- Actions -->
        <div v-if="showActions && canManageTeam" class="flex items-center space-x-2">
          <!-- Role Selector (for non-owners) -->
          <select
            v-if="member.user?.id !== team.createdBy && member.user?.id !== currentUserId"
            :value="member.role"
            @change="handleRoleUpdate(member.id, $event)"
            class="text-xs border border-gray-300 dark:border-gray-600 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="admin">{{ $t('teams.roles.admin') }}</option>
            <option value="member">{{ $t('teams.roles.member') }}</option>
          </select>

          <!-- Remove Button (for non-owners and not self) -->
          <button
            v-if="member.user?.id !== team.createdBy && member.user?.id !== currentUserId"
            @click="handleRemove(member.id)"
            class="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 p-1 rounded-full hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors duration-200"
            :title="$t('teams.actions.removeMember')"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>

          <!-- View Profile Button -->
          <button
            @click="handleViewProfile(member.user?.id)"
            class="text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300 p-1 rounded-full hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors duration-200"
            :title="$t('teams.actions.viewProfile')"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </button>
        </div>

        <!-- Role Badge (in compact mode) -->
        <div v-else-if="compact" class="ml-2">
          <span :class="roleBadgeClasses(member.role)" class="text-xs px-2 py-0.5 rounded-full">
            {{ getRoleText(member.role) }}
          </span>
        </div>
      </div>

      <!-- Show More Indicator -->
      <div v-if="hasMoreMembers && !compact" class="text-center pt-2">
        <button
          @click="showAllMembers = true"
          class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium"
        >
          {{ $t('teams.members.showMore', { remaining: remainingMembers }) }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { TeamRole } from '~/types/team-types'
import type { TeamMemberListProps, TeamMemberListEmits } from '~/types/team-types'
import { canUserManageTeam } from '~/types/team-types'

const props = withDefaults(defineProps<TeamMemberListProps>(), {
  showActions: false,
  maxVisible: 5,
  compact: false,
  loading: false,
})

const emit = defineEmits<TeamMemberListEmits>()

const showAllMembers = ref(false)

// Check if current user can manage the team
const canManageTeam = computed(() => {
  return canUserManageTeam(props.currentUserId ?? null, props.team, props.members)
})

// Get visible members based on maxVisible
const visibleMembers = computed(() => {
  if (showAllMembers.value || props.compact) {
    return props.members
  }
  return props.members.slice(0, props.maxVisible)
})

// Check if there are more members to show
const hasMoreMembers = computed(() => {
  return !showAllMembers.value && props.members.length > props.maxVisible
})

// Count of remaining members
const remainingMembers = computed(() => {
  return props.members.length - props.maxVisible
})

// Get role text for display
const getRoleText = (role: TeamRole): string => {
  switch (role) {
    case TeamRole.OWNER:
      return 'Owner'
    case TeamRole.ADMIN:
      return 'Admin'
    case TeamRole.MEMBER:
      return 'Member'
    case TeamRole.PENDING:
      return 'Pending'
    default:
      return 'Unknown'
  }
}

// Role badge classes
const roleBadgeClasses = (role: TeamRole): string => {
  const baseClasses = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium'
  
  switch (role) {
    case TeamRole.OWNER:
      return `${baseClasses} bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200`
    case TeamRole.ADMIN:
      return `${baseClasses} bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200`
    case TeamRole.MEMBER:
      return `${baseClasses} bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200`
    case TeamRole.PENDING:
      return `${baseClasses} bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200`
    default:
      return `${baseClasses} bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200`
  }
}

// Event handlers
const handleRoleUpdate = (memberId: string, event: Event) => {
  const target = event.target as HTMLSelectElement
  const role = target.value as TeamRole
  emit('role-update', memberId, role)
}

const handleRemove = (memberId: string) => {
  if (confirm('Are you sure you want to remove this member?')) {
    emit('remove', memberId)
  }
}

const handleViewProfile = (userId?: string) => {
  if (userId) {
    emit('view-profile', userId)
  }
}
</script>

<style scoped>
.team-member-list {
  @apply w-full;
}

/* Smooth transitions */
.team-member-list > * {
  @apply transition-all duration-200;
}

/* Hover effects for member items */
div[class*="bg-white"]:hover,
div[class*="bg-gray-800"]:hover {
  @apply transform transition-transform duration-200;
}

/* Compact mode adjustments */
.compact-mode .team-member-list {
  @apply space-y-1;
}

/* Loading animation */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>