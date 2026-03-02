<template>
  <div class="team-invitations bg-white dark:bg-gray-800 rounded-lg shadow p-6">
    <!-- Header -->
    <slot name="header" :count="pendingInvitations.length" :is-team-owner="isTeamOwner">
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          {{ title }}
        </h3>
        <div v-if="showCount" class="text-sm text-gray-600 dark:text-gray-400">
          {{ pendingInvitations.length }} {{ pendingLabel }}
        </div>
      </div>
    </slot>

    <!-- Loading State -->
    <div v-if="loading && showLoadingState">
      <slot name="loading-state">
        <div class="text-center py-8">
          <svg class="animate-spin h-8 w-8 text-primary-600 dark:text-primary-400 mx-auto" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          <p class="mt-2 text-gray-600 dark:text-gray-400">{{ loadingLabel }}</p>
        </div>
      </slot>
    </div>

    <!-- Error State -->
    <div v-else-if="error && showErrorState">
      <slot name="error-state" :error="error" :retry="fetchInvitations">
        <div class="text-center py-8">
          <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400 mb-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">{{ errorTitle }}</h3>
          <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
          <button @click="fetchInvitations" class="btn btn-outline">
            {{ retryLabel }}
          </button>
        </div>
      </slot>
    </div>

    <!-- Empty State -->
    <div v-else-if="pendingInvitations.length === 0 && showEmptyState">
      <slot name="empty-state" :is-team-owner="isTeamOwner">
        <div class="text-center py-8">
          <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 mb-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">{{ emptyTitle }}</h3>
          <p class="text-gray-600 dark:text-gray-400">{{ emptyDescription }}</p>
        </div>
      </slot>
    </div>

    <!-- Invitations List -->
    <div v-else class="space-y-4">
      <div
        v-for="invitation in visibleInvitations"
        :key="invitation.id"
        class="invitation-item"
      >
        <slot
          name="invitation-item"
          :invitation="invitation"
          :cancel="() => handleCancelInvitation(invitation.id)"
        >
          <InvitationItem
            :invitation="invitation"
            :show-cancel-button="isTeamOwner"
            :show-inviter="true"
            :show-team-info="false"
            :show-status="true"
            :format-date="formatDate"
            :labels="invitationItemLabels"
            @cancel="handleCancelInvitation"
            @click="handleInvitationClick"
          />
        </slot>
      </div>

      <!-- Show more button -->
      <div v-if="hasMoreInvitations" class="text-center pt-4">
        <button
          @click="showAllInvitations = true"
          class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300"
        >
          {{ showMoreLabel }}
        </button>
      </div>
    </div>

    <!-- Footer slot -->
    <slot name="footer"></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import InvitationItem from '~/components/molecules/InvitationItem.vue'
import { useTeamInvitations } from '~/composables/useTeamInvitations'
import type { TeamInvitationsProps } from '~/types/team-invitations'

const props = withDefaults(defineProps<TeamInvitationsProps>(), {
  showHeader: true,
  showEmptyState: true,
  showLoadingState: true,
  showErrorState: true,
  autoLoad: true,
  pollInterval: 0,
  maxVisible: 10,
  labels: () => ({})
})

const emit = defineEmits<{
  'invitation-cancelled': [{ invitationId: number, invitation: any }]
  'loaded': [{ invitations: any[], count: number }]
  'error': [{ message: string, code?: string }]
  'retry': []
}>()

const { t } = useI18n()

// Local state
const showAllInvitations = ref(false)

// Use composable
const {
  invitations,
  loading,
  error,
  pendingInvitations,
  fetchInvitations,
  cancelInvitation,
  isTeamOwner: computedIsTeamOwner,
  startPolling,
  stopPolling,
  cleanup
} = useTeamInvitations({
  teamId: props.teamId,
  autoFetch: props.autoLoad,
  pollInterval: props.pollInterval
})

// Use prop if provided, otherwise use computed value
const isTeamOwner = props.isTeamOwner ?? computedIsTeamOwner

// Computed
const visibleInvitations = computed(() => {
  if (showAllInvitations.value || props.maxVisible === 0) {
    return pendingInvitations.value
  }
  return pendingInvitations.value.slice(0, props.maxVisible)
})

const hasMoreInvitations = computed(() => {
  return props.maxVisible > 0 && pendingInvitations.value.length > props.maxVisible && !showAllInvitations.value
})

// Labels
const title = computed(() => {
  return props.labels?.title || t('teams.teamInvitations') || 'Team Invitations'
})

const pendingLabel = computed(() => {
  return props.labels?.pending || t('teams.pending') || 'pending'
})

const loadingLabel = computed(() => {
  return props.labels?.loading || t('teams.loadingInvitations') || 'Loading invitations...'
})

const errorTitle = computed(() => {
  return t('common.error') || 'Error'
})

const retryLabel = computed(() => {
  return props.labels?.retry || t('common.retry') || 'Try again'
})

const emptyTitle = computed(() => {
  return props.labels?.emptyTitle || t('teams.noPendingInvitations') || 'No pending invitations'
})

const emptyDescription = computed(() => {
  return props.labels?.emptyDescription || t('teams.noPendingInvitationsDescription') || 'There are no pending invitations for this team.'
})

const showMoreLabel = computed(() => {
  const remaining = pendingInvitations.value.length - props.maxVisible
  return t('teams.showMoreInvitations', { count: remaining }) || `Show ${remaining} more`
})

const showCount = computed(() => {
  return props.showHeader && pendingInvitations.value.length > 0
})

const invitationItemLabels = computed(() => ({
  pending: t('teams.pending') || 'Pending',
  invited: t('teams.invited') || 'Invited',
  by: t('common.by') || 'by',
  cancel: t('common.cancel') || 'Cancel',
  cancelling: t('teams.cancelling') || 'Cancelling...',
  unknownUser: t('teams.unknownUser') || 'Unknown User',
  unknownUserInitial: t('teams.unknownUserInitial') || '?',
  teamLabel: t('teams.team') || 'Team'
}))

// Methods
function formatDate(dateString: string): string {
  try {
    return new Date(dateString).toLocaleDateString()
  } catch {
    return dateString
  }
}

async function handleCancelInvitation(invitationId: number) {
  const success = await cancelInvitation(invitationId)
  if (success) {
    const invitation = pendingInvitations.value.find(inv => inv.id === invitationId)
    emit('invitation-cancelled', { invitationId, invitation })
  }
}

function handleInvitationClick(invitation: any) {
  // Emit click event if needed
  // emit('invitation-click', invitation)
}

function handleRetry() {
  emit('retry')
  fetchInvitations()
}

// Lifecycle
onMounted(() => {
  if (props.pollInterval && props.pollInterval > 0) {
    startPolling()
  }
  
  // Emit loaded event when invitations are loaded
  if (invitations.value.length > 0 && !loading.value) {
    emit('loaded', { invitations: invitations.value, count: invitations.value.length })
  }
})

onUnmounted(() => {
  cleanup()
})

// Watch for invitations changes
watch(invitations, (newInvitations) => {
  if (newInvitations.length > 0 && !loading.value) {
    emit('loaded', { invitations: newInvitations, count: newInvitations.length })
  }
})

watch(error, (newError) => {
  if (newError) {
    emit('error', { message: newError })
  }
})
</script>

<style scoped>
.team-invitations {
  transition: all 0.2s ease;
}

.invitation-item {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.invitation-item:hover {
  transform: translateY(-1px);
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .team-invitations {
    @apply p-4;
  }
  
  .team-invitations .flex.items-center.justify-between {
    @apply flex-col items-start gap-2;
  }
}
</style>