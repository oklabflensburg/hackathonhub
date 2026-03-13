<template>
  <div class="min-h-screen bg-gray-50 py-8 dark:bg-gray-900">
    <div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
      <div v-if="!authStore.isAuthenticated" class="rounded-2xl border border-amber-200 bg-amber-50 p-6 text-sm text-amber-800 dark:border-amber-500/30 dark:bg-amber-500/10 dark:text-amber-200">
        You need to sign in to review team reports.
      </div>

      <div v-else-if="loading" class="py-20 text-center text-gray-500 dark:text-gray-400">Loading team reports...</div>

      <div v-else-if="forbidden" class="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700 dark:border-red-500/30 dark:bg-red-500/10 dark:text-red-200">
        You are not allowed to access team reports for this hackathon.
      </div>

      <div v-else-if="error" class="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700 dark:border-red-500/30 dark:bg-red-500/10 dark:text-red-200">
        {{ error }}
      </div>

      <HackathonTeamReportsPage
        v-else
        :hackathon-id="hackathonId"
        :reports="reports"
        :teams="teams"
        :filters="filters"
        @apply-filters="applyFilters"
        @review="openReview"
      />
    </div>

    <TeamReportReviewModal
      :visible="reviewModalOpen"
      :report="selectedReport"
      :loading="saving"
      @close="closeReview"
      @submit="submitReview"
    />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import { useRoute, navigateTo } from '#imports'
import HackathonTeamReportsPage from '~/components/organisms/hackathons/HackathonTeamReportsPage.vue'
import TeamReportReviewModal from '~/components/organisms/hackathons/TeamReportReviewModal.vue'
import { useHackathonTeamReports, type HackathonTeamReportSummary } from '~/composables/useHackathonTeamReports'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

const route = useRoute()
const authStore = useAuthStore()
const uiStore = useUIStore()
const hackathonId = String(route.params.id)

const { reports, teams, loading, error, forbidden, fetchReports, updateReport } = useHackathonTeamReports()
const filters = reactive<{ status?: string; teamId?: number | null }>({
  status: undefined,
  teamId: null,
})
const reviewModalOpen = ref(false)
const selectedReport = ref<HackathonTeamReportSummary | null>(null)
const saving = ref(false)

watch(() => authStore.isAuthenticated, (isAuthenticated) => {
  if (!isAuthenticated) {
    navigateTo('/login')
  }
}, { immediate: true })

await fetchReports(hackathonId, filters).catch(() => undefined)

function applyFilters(nextFilters: { status?: string; teamId?: number | null }) {
  filters.status = nextFilters.status
  filters.teamId = nextFilters.teamId ?? null
  fetchReports(hackathonId, filters).catch(() => undefined)
}

function openReview(report: HackathonTeamReportSummary) {
  selectedReport.value = report
  reviewModalOpen.value = true
}

function closeReview() {
  reviewModalOpen.value = false
  selectedReport.value = null
}

async function submitReview(payload: { status: string; resolution_note?: string | null }) {
  if (!selectedReport.value) return
  saving.value = true
  try {
    await updateReport(selectedReport.value.id, payload)
    uiStore.showSuccess('Team report updated', 'Moderation')
    closeReview()
  } catch (err: any) {
    uiStore.showError(err?.message || 'Failed to update team report', 'Moderation')
  } finally {
    saving.value = false
  }
}
</script>
