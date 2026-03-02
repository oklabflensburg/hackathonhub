<template>
  <div v-if="shouldShow" class="team-invite-section bg-white dark:bg-gray-800 rounded-lg shadow p-6 space-y-6 mb-6">
    <!-- Before form slot -->
    <slot name="before-form"></slot>

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        {{ title }}
      </h3>
      <div v-if="showMemberCount && maxMembers" class="text-sm text-gray-600 dark:text-gray-400">
        {{ memberCountLabel }}
      </div>
    </div>

    <!-- Team full message -->
    <div v-if="isTeamFull" class="mb-6">
      <slot name="team-full-message" :current-member-count="currentMemberCount" :max-members="maxMembers">
        <div class="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.998-.833-2.732 0L4.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            <div>
              <p class="text-sm font-medium text-yellow-800 dark:text-yellow-200">
                {{ teamFullTitle }}
              </p>
              <p class="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                {{ teamFullDescription }}
              </p>
            </div>
          </div>
        </div>
      </slot>
    </div>

    <!-- Invite form (only shown if team is not full) -->
    <div v-else>
      <InviteUserForm
        :team-id="teamId"
        :max-members="maxMembers"
        :current-member-count="currentMemberCount"
        :disabled="disabled"
        :placeholder="placeholder"
        :button-label="buttonLabel"
        :help-text="helpText"
        :show-member-count="false"
        :show-title="false"
        :show-help-text="true"
        :exclude-user-ids="excludeUserIds"
        @invite-sent="handleInviteSent"
        @error="handleError"
        @search="handleSearch"
      />

      <!-- Help text slot (optional - can be overridden by parent) -->
      <slot name="help-text" :current-member-count="currentMemberCount" :max-members="maxMembers">
        <!-- Empty by default - help text is already shown in InviteUserForm -->
      </slot>
    </div>

    <!-- After form slot -->
    <slot name="after-form"></slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import InviteUserForm from '~/components/molecules/InviteUserForm.vue'
import type { TeamInviteSectionProps } from '~/types/team-invitations'

const props = withDefaults(defineProps<TeamInviteSectionProps>(), {
  currentMemberCount: 0,
  maxMembers: 5,
  showHelpText: true,
  showMemberCount: true,
  disabled: false,
  excludeUserIds: () => [],
  labels: () => ({})
})

const emit = defineEmits<{
  'invite-sent': [{ userId: number, username: string }]
  'error': [{ message: string, code?: string }]
  'search': [{ query: string }]
}>()

const { t } = useI18n()

// Computed
const shouldShow = computed(() => {
  return props.isTeamOwner && !props.disabled
})

const isTeamFull = computed(() => {
  return props.isTeamFull || (props.maxMembers && props.currentMemberCount >= props.maxMembers)
})

const title = computed(() => {
  return props.labels?.title || t('teams.inviteMembers') || 'Invite Members'
})

const placeholder = computed(() => {
  return props.labels?.placeholder || t('teams.enterUsername') || 'Enter username'
})

const buttonLabel = computed(() => {
  return props.labels?.button || t('teams.invite') || 'Invite'
})

const helpText = computed(() => {
  return props.labels?.helpText || t('teams.inviteUsernameHelp') || 'Enter a username to invite them to your team'
})

const helpTextInline = computed(() => {
  return props.labels?.helpText || t('teams.inviteUsernameHelp') || 'Enter a username to invite them to your team'
})

const memberCountLabel = computed(() => {
  if (props.labels?.memberCount) {
    return props.labels.memberCount
  }
  return t('teams.memberCount', {
    current: props.currentMemberCount,
    max: props.maxMembers
  }) || `${props.currentMemberCount}/${props.maxMembers} members`
})

const teamFullTitle = computed(() => {
  return props.labels?.teamFull || t('teams.teamFull') || 'Team is full'
})

const teamFullDescription = computed(() => {
  return t('teams.teamFullDescription') || 'You cannot invite more members because the team has reached its maximum capacity.'
})

// Methods
function handleInviteSent(payload: { userId: number, username: string }) {
  emit('invite-sent', payload)
}

function handleError(payload: { message: string, code?: string }) {
  emit('error', payload)
}

function handleSearch(payload: { query: string }) {
  emit('search', payload)
}
</script>

<style scoped>
.team-invite-section {
  transition: all 0.2s ease;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .team-invite-section {
    @apply p-4;
  }
  
  .team-invite-section .flex.items-center.justify-between {
    @apply flex-col items-start gap-2;
  }
}
</style>