<template>
  <div class="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8 space-y-6">
    <div v-if="!authStore.isAuthenticated" class="rounded-2xl border border-yellow-200 bg-yellow-50 p-6 text-yellow-900 dark:border-yellow-800 dark:bg-yellow-950/30 dark:text-yellow-100">
      You need to sign in to review hackathon reports.
    </div>
    <div v-else-if="loading" class="py-20 text-center text-gray-500 dark:text-gray-400">Loading hackathon reports...</div>
    <div v-else-if="forbidden" class="rounded-2xl border border-red-200 bg-red-50 p-6 text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-200">
      You are not allowed to access reports for this hackathon.
    </div>
    <section v-else class="space-y-6">
      <header class="flex items-center justify-between gap-4">
        <div>
          <p class="text-sm font-medium uppercase tracking-[0.2em] text-gray-500 dark:text-gray-400">Moderation</p>
          <h1 class="text-3xl font-semibold text-gray-900 dark:text-white">Hackathon Reports</h1>
        </div>
        <NuxtLink :to="`/hackathons/${hackathonId}`" class="btn btn-outline">Back to Hackathon</NuxtLink>
      </header>
      <div class="rounded-2xl border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800 overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-900/50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Reporter</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Reason</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Status</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Created</th>
              <th class="px-6 py-3"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="report in reports" :key="report.id">
              <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-200">{{ report.reporter?.name || report.reporter?.username || `User #${report.reporter_id}` }}</td>
              <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-200">{{ report.reason }}</td>
              <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-200">{{ report.status }}</td>
              <td class="px-6 py-4 text-sm text-gray-600 dark:text-gray-300">{{ formatDate(report.created_at) }}</td>
              <td class="px-6 py-4 text-right"><button class="btn btn-outline" @click="openReview(report)">Review</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <ReportReviewModal :visible="reviewOpen" :report="selectedReport" :loading="saving" @close="closeReview" @submit="submitReview" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { format } from 'date-fns'
import { useRoute } from '#imports'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useReports, type ResourceReportSummary } from '~/composables/useReports'
import ReportReviewModal from '~/components/organisms/reports/ReportReviewModal.vue'

const route = useRoute()
const hackathonId = computed(() => String(route.params.id))
const authStore = useAuthStore()
const uiStore = useUIStore()
const { reports, loading, forbidden, fetchReports, updateReport } = useReports()
const reviewOpen = ref(false)
const saving = ref(false)
const selectedReport = ref<ResourceReportSummary | null>(null)

function formatDate(value: string) {
  try { return format(new Date(value), 'MMM d, yyyy HH:mm') } catch { return value }
}
function openReview(report: ResourceReportSummary) { selectedReport.value = report; reviewOpen.value = true }
function closeReview() { reviewOpen.value = false; selectedReport.value = null }
async function submitReview(payload: { status: 'pending' | 'reviewed' | 'resolved' | 'dismissed'; resolution_note?: string | null }) {
  if (!selectedReport.value) return
  try {
    saving.value = true
    await updateReport(selectedReport.value.id, payload)
    uiStore.showSuccess('Hackathon report updated', 'Moderation')
    closeReview()
  } catch (err: any) {
    uiStore.showError(err?.message || 'Failed to update report', 'Moderation')
  } finally {
    saving.value = false
  }
}

onMounted(() => { fetchReports('hackathon', hackathonId.value).catch(() => undefined) })
</script>
