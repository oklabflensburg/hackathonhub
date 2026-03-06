<template>
  <div class="team-card-footer" :class="footerClasses">
    <!-- Mitgliederanzahl -->
    <div v-if="showMemberCount" class="member-count" :class="memberCountClasses">
      <span class="member-icon" aria-hidden="true">
        <svg
          class="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </span>
      <span class="member-value" :class="memberValueClasses">
        {{ team.stats?.memberCount || 0 }}
      </span>
      <span class="member-label sr-only">
        {{ $t('teams.members') }}
      </span>
    </div>

    <!-- Join-Button -->
    <div v-if="showJoinButton && userId" class="join-button-container">
      <TeamJoinButton
        :team="team"
        :userId="userId"
        :isMember="isMember"
        :isInvited="isInvited"
        size="sm"
        variant="secondary"
        @join="handleJoin"
        @leave="handleLeave"
      />
    </div>

    <!-- Aktionen für Team-Mitglieder -->
    <div v-else-if="isMember" class="member-actions">
      <div class="flex items-center gap-2">
        <TeamInviteButton
          :team="team"
          size="sm"
          variant="ghost"
          @invite="handleInvite"
        />
        <TeamSettingsButton
          :team="team"
          size="sm"
          variant="ghost"
          @settings="handleSettings"
        />
      </div>
    </div>

    <!-- Slot für benutzerdefinierte Inhalte -->
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { TeamCardFooterProps } from '~/types/team-types'
import TeamJoinButton from '~/components/atoms/teams/TeamJoinButton.vue'
import TeamInviteButton from '~/components/atoms/teams/TeamInviteButton.vue'
import TeamSettingsButton from '~/components/atoms/teams/TeamSettingsButton.vue'

interface ExtendedTeamCardFooterProps extends TeamCardFooterProps {
  isMember?: boolean
  isInvited?: boolean
}

const props = withDefaults(defineProps<ExtendedTeamCardFooterProps>(), {
  showMemberCount: true,
  showJoinButton: true,
  userId: null,
  isMember: false,
  isInvited: false,
})

const emit = defineEmits<{
  join: [teamId: string]
  leave: [teamId: string]
  invite: [teamId: string]
  settings: [teamId: string]
}>()

// Berechne, ob das Team voll ist
const isTeamFull = computed(() => {
  const memberCount = props.team.stats?.memberCount || 0
  const maxMembers = props.team.maxMembers
  return maxMembers !== null && memberCount >= maxMembers
})

// CSS-Klassen
const footerClasses = computed(() => ({
  'has-member-count': props.showMemberCount,
  'has-join-button': props.showJoinButton && props.userId,
  'is-member': props.isMember,
}))

const memberCountClasses = computed(() => ({
  'text-gray-600 dark:text-gray-400': true,
  'hover:text-gray-900 dark:hover:text-gray-200': true,
}))

const memberValueClasses = computed(() => ({
  'font-medium': true,
  'ml-1': true,
}))

// Event-Handler
const handleJoin = () => {
  emit('join', props.team.id)
}

const handleLeave = () => {
  emit('leave', props.team.id)
}

const handleInvite = () => {
  emit('invite', props.team.id)
}

const handleSettings = () => {
  emit('settings', props.team.id)
}
</script>

<style scoped>
.team-card-footer {
  @apply flex items-center justify-between pt-4 mt-4 border-t border-gray-200 dark:border-gray-700;
}

.member-count {
  @apply flex items-center gap-1 text-sm;
}

.member-icon {
  @apply text-gray-500 dark:text-gray-400;
}

.member-value {
  @apply text-gray-900 dark:text-gray-100;
}

.join-button-container {
  @apply flex-shrink-0;
}

.member-actions {
  @apply flex-shrink-0;
}
</style>