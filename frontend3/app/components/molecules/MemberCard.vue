<template>
  <div class="member-card" :class="{ 'cursor-pointer': clickable }" @click="handleClick">
    <!-- Avatar -->
    <div class="member-avatar">
      <NuxtLink 
        v-if="member.user && !disableLink"
        :to="`/users/${member.user.id}`"
        class="avatar-link"
        @click.stop
      >
        <Avatar
          :src="member.user?.avatar_url"
          :alt="member.user?.name || member.user?.username || t('teams.unknownUser')"
          :size="avatarSize"
          :fallback-text="avatarFallbackText"
        />
      </NuxtLink>
      <Avatar
        v-else
        :src="member.user?.avatar_url"
          :alt="member.user?.name || member.user?.username || t('teams.unknownUser')"
        :size="avatarSize"
        :fallback-text="avatarFallbackText"
      />
    </div>

    <!-- Member Info -->
    <div class="member-info">
      <!-- Name and Role -->
      <div class="member-header">
        <div class="member-name">
          <NuxtLink 
            v-if="member.user && !disableLink"
            :to="`/users/${member.user.id}`"
            class="name-link"
            @click.stop
          >
            {{ member.user?.name || member.user?.username || t('teams.unknownUser') }}
          </NuxtLink>
          <span v-else class="name-text">
            {{ member.user?.name || member.user?.username || t('teams.unknownUser') }}
          </span>
          
          <!-- Role Badge -->
          <span
            v-if="showRole && member.role === 'owner'"
            class="role-badge owner"
          >
            {{ t('teams.owner') }}
          </span>
          <span
            v-else-if="showRole && member.role === 'member'"
            class="role-badge member"
          >
            {{ t('teams.member') }}
          </span>
        </div>
        
        <!-- Joined Date -->
        <div v-if="showJoinedDate" class="joined-date">
          {{ t('teams.joined') }} {{ formatDate(member.joined_at) }}
        </div>
      </div>

      <!-- Additional Info Slot -->
      <slot name="info"></slot>

      <!-- Actions Slot -->
      <div v-if="showActions" class="member-actions">
        <slot name="actions">
          <!-- Default actions if no slot provided -->
          <div v-if="isCurrentUser" class="current-user-indicator">
            {{ t('common.you') }}
          </div>
          <div v-else-if="showDefaultActions" class="default-actions">
            <Button
              v-if="canMakeOwner && member.role === 'member'"
              @click.stop="$emit('make-owner')"
              variant="ghost"
              size="sm"
              class="action-btn make-owner"
              :title="t('teams.makeOwner')"
            >
              {{ t('teams.makeOwner') }}
            </Button>
            <Button
              v-else-if="canMakeMember && member.role === 'owner'"
              @click.stop="$emit('make-member')"
              variant="ghost"
              size="sm"
              class="action-btn make-member"
              :title="t('teams.makeMember')"
            >
              {{ t('teams.makeMember') }}
            </Button>
            <Button
              v-if="canRemove"
              @click.stop="$emit('remove')"
              variant="ghost"
              size="sm"
              class="action-btn remove"
              :title="t('common.remove')"
            >
              {{ t('common.remove') }}
            </Button>
          </div>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { TeamMember } from '~/composables/useTeamMembers'
import Avatar from '~/components/atoms/Avatar.vue'
import Button from '~/components/atoms/Button.vue'

interface Props {
  member: TeamMember
  showRole?: boolean
  showActions?: boolean
  showJoinedDate?: boolean
  showDefaultActions?: boolean
  isCurrentUser?: boolean
  isTeamOwner?: boolean
  canMakeOwner?: boolean
  canMakeMember?: boolean
  canRemove?: boolean
  disableLink?: boolean
  clickable?: boolean
  avatarSize?: 'sm' | 'md' | 'lg'
  bioMaxLength?: number
  
  // Functions
  formatDate?: (dateString: string) => string
  truncateText?: (text: string, maxLength: number) => string
}

const { t } = useI18n()

const props = withDefaults(defineProps<Props>(), {
  showRole: true,
  showActions: true,
  showJoinedDate: true,
  showDefaultActions: true,
  isCurrentUser: false,
  isTeamOwner: false,
  canMakeOwner: false,
  canMakeMember: false,
  canRemove: false,
  disableLink: false,
  clickable: false,
  avatarSize: 'md',
  bioMaxLength: 100,
  formatDate: (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString()
    } catch {
      return dateString
    }
  },
  truncateText: (text: string, maxLength: number) => {
    if (text.length <= maxLength) return text
    return text.substring(0, maxLength) + '...'
  }
})

const emit = defineEmits<{
  'make-owner': []
  'make-member': []
  'remove': []
  'click': [member: TeamMember]
}>()

// Computed
const avatarFallbackText = computed(() => {
  const name = props.member.user?.name || props.member.user?.username || t('teams.unknownUser')
  return name.charAt(0).toUpperCase()
})

const canShowDefaultActions = computed(() => {
  return props.showDefaultActions && props.showActions && !props.isCurrentUser
})

// Methods
function handleClick() {
  if (props.clickable) {
    emit('click', props.member)
  }
}
</script>

<style scoped>
.member-card {
  @apply flex items-start p-4 rounded-lg border border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors;
}

.member-card.cursor-pointer {
  cursor: pointer;
}

.member-avatar {
  @apply flex-shrink-0 mr-4;
}

.avatar-link {
  @apply block hover:opacity-90 transition-opacity;
}

.member-info {
  @apply flex-1 min-w-0;
}

.member-header {
  @apply mb-2;
}

.member-name {
  @apply flex items-center flex-wrap gap-2;
}

.name-link {
  @apply font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400 truncate;
}

.name-text {
  @apply font-medium text-gray-900 dark:text-white truncate;
}

.role-badge {
  @apply px-2 py-0.5 text-xs font-medium rounded-full;
}

.role-badge.owner {
  @apply bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200;
}

.role-badge.member {
  @apply bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200;
}

.joined-date {
  @apply text-sm text-gray-500 dark:text-gray-400 mt-1;
}

.member-bio {
  @apply text-sm text-gray-600 dark:text-gray-400 mt-2 line-clamp-2;
}

.member-actions {
  @apply mt-3 flex items-center gap-2;
}

.current-user-indicator {
  @apply text-sm text-gray-500 dark:text-gray-400 italic;
}

.default-actions {
  @apply flex items-center gap-2;
}

.action-btn {
  @apply text-xs;
}

.action-btn.make-owner {
  @apply text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300;
}

.action-btn.make-member {
  @apply text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-300;
}

.action-btn.remove {
  @apply text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300;
}

/* Responsive */
@media (max-width: 640px) {
  .member-card {
    @apply p-3;
  }
  
  .member-name {
    @apply flex-col items-start gap-1;
  }
  
  .default-actions {
    @apply flex-col items-start gap-1;
  }
}
</style>