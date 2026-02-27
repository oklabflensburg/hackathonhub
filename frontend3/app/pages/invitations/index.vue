<template>
  <div class="container mx-auto px-4 py-8">
    <InvitationsPageHeader :title="$t('teams.teamInvitationsTitle')" :description="$t('teams.manageInvitations')" />

    <InvitationsLoadingState v-if="loading" :text="$t('teams.loadingInvitations')" />

    <InvitationsErrorState
      v-else-if="error"
      :title="$t('teams.errorLoadingInvitations')"
      :message="error"
      :retry-label="$t('common.tryAgain')"
      @retry="loadInvitations"
    />

    <InvitationsEmptyState
      v-else-if="invitations.length === 0"
      :title="$t('teams.noPendingInvitationsTitle')"
      :description="$t('teams.noInvitationsDescription')"
      :button-label="$t('teams.browseTeams')"
      to="/teams"
    />

    <div v-else class="space-y-6">
      <InvitationListCard
        v-for="invitation in invitations"
        :key="invitation.id"
        :invitation="invitation"
        :processing-invitation="processingInvitation"
        :action-type="actionType"
        :labels="labels"
        :format-date="formatDate"
        @accept="acceptInvitation"
        @decline="declineInvitation"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '~/stores/auth'
import { useTeamStore } from '~/stores/team'
import { useUIStore } from '~/stores/ui'

const { t } = useI18n()
const teamStore = useTeamStore()
const authStore = useAuthStore()
const uiStore = useUIStore()

const loading = ref(true)
const error = ref<string | null>(null)
const invitations = ref<any[]>([])
const processingInvitation = ref<number | null>(null)
const actionType = ref<'accept' | 'decline' | null>(null)

const labels = computed(() => ({
  unknownTeam: t('teams.unknownTeam'),
  pending: t('teams.pending'),
  accepted: t('teams.accepted'),
  declined: t('teams.declined'),
  invited: t('teams.invited'),
  invitedBy: t('teams.invitedBy'),
  unknownUser: t('teams.unknownUser'),
  hackathonLabel: t('teams.hackathonLabel'),
  unknown: t('common.unknown'),
  messageLabel: t('teams.messageLabel'),
  declining: t('teams.declining'),
  decline: t('teams.decline'),
  accepting: t('teams.accepting'),
  acceptInvitationButton: t('teams.acceptInvitationButton'),
  youAcceptedThisInvitation: t('teams.youAcceptedThisInvitation'),
  youDeclinedThisInvitation: t('teams.youDeclinedThisInvitation'),
}))

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}

async function loadInvitations() {
  loading.value = true
  error.value = null

  try {
    invitations.value = await teamStore.fetchMyInvitations()
  } catch (err) {
    error.value = err instanceof Error ? err.message : t('teams.failedToLoadInvitations')
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
    uiStore.showSuccess(t('teams.invitationAcceptedSuccess'))
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
    uiStore.showSuccess(t('teams.invitationDeclinedSuccess'))
    await loadInvitations()
  } catch (err) {
    console.error('Failed to decline invitation:', err)
  } finally {
    processingInvitation.value = null
    actionType.value = null
  }
}

onMounted(() => {
  if (!authStore.isAuthenticated) {
    uiStore.showError(t('teams.mustBeLoggedInToViewInvitations'), t('common.authenticationRequired'))
    return
  }

  loadInvitations()
})
</script>
