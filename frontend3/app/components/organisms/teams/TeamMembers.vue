<template>
  <div class="team-members">
    <!-- Header with count -->
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        {{ title || t('teams.teamMembers') }}
      </h3>
      <div class="text-sm text-gray-600 dark:text-gray-400">
        {{ members.length }} / {{ maxMembers }} {{ t('teams.members') }}
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <LoadingSpinner size="md" />
      <p class="mt-2 text-gray-600 dark:text-gray-400">{{ t('teams.loadingMembers') }}</p>
    </div>

    <!-- Error State -->
    <ErrorState v-else-if="error" :title="t('common.error')" :message="error" :retry-label="t('common.retry')" @retry="$emit('retry')" />

    <!-- Empty State -->
    <EmptyState v-else-if="members.length === 0" :title="''" :description="t('teams.noMembersYet')">
      <template #action>
        <slot name="empty-state"></slot>
      </template>
    </EmptyState>

    <!-- Members List -->
    <div v-else class="space-y-4">
      <MemberCard
        v-for="member in members"
        :key="member.id"
        :member="member"
        :show-role="true"
        :show-joined-date="true"
        :show-actions="true"
        :show-default-actions="isTeamOwner"
        :is-current-user="member.user_id === currentUserId"
        :is-team-owner="isTeamOwner"
        :can-make-owner="isTeamOwner && member.user_id !== currentUserId && member.role === 'member'"
        :can-make-member="isTeamOwner && member.user_id !== currentUserId && member.role === 'owner'"
        :can-remove="isTeamOwner && member.user_id !== currentUserId"
        :disable-link="false"
        :clickable="false"
        :avatar-size="'md'"
        :format-date="formatDate"
        @make-owner="$emit('make-owner', member.user_id)"
        @make-member="$emit('make-member', member.user_id)"
        @remove="$emit('remove-member', member.user_id)"
      />
    </div>

    <!-- Slot for additional content -->
    <slot name="footer"></slot>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import type { TeamMember } from '~/stores/team'
import LoadingSpinner from '~/components/atoms/LoadingSpinner.vue'
import ErrorState from '~/components/molecules/ErrorState.vue'
import EmptyState from '~/components/molecules/EmptyState.vue'
import MemberCard from '~/components/molecules/MemberCard.vue'

const { t } = useI18n()

interface Props {
  members: TeamMember[]
  currentUserId?: number | null
  isTeamOwner: boolean
  maxMembers: number
  loading?: boolean
  error?: string | null
  
  // Optional title (falls back to i18n)
  title?: string
  
  // Options
  showMemberBadge?: boolean
  formatDate: (dateString: string) => string
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  showMemberBadge: false,
  loading: false,
  error: null,
  currentUserId: null,
  formatDate: (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString()
    } catch {
      return dateString
    }
  }
})

const emit = defineEmits<{
  'make-owner': [userId: number]
  'make-member': [userId: number]
  'remove-member': [userId: number]
  'retry': []
}>()


</script>

<style scoped>
/* Responsive adjustments */
@media (max-width: 640px) {
  .team-members .flex.items-center.justify-between {
    @apply flex-col items-start gap-2;
  }
}
</style>
