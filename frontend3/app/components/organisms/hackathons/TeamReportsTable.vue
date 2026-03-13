<template>
  <div class="overflow-hidden rounded-2xl border border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
    <div v-if="reports.length === 0" class="px-6 py-12 text-center text-sm text-gray-500 dark:text-gray-400">
      No team reports found for the selected filters.
    </div>

    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-900/40">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Team</th>
            <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Reporter</th>
            <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Reason</th>
            <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Status</th>
            <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Created</th>
            <th class="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wide text-gray-500">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="report in reports" :key="report.id" class="align-top">
            <td class="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white">{{ report.team?.name || `Team #${report.team_id}` }}</td>
            <td class="px-6 py-4 text-sm text-gray-600 dark:text-gray-300">{{ report.reporter?.name || report.reporter?.username || `User #${report.reporter_id}` }}</td>
            <td class="px-6 py-4 text-sm text-gray-600 dark:text-gray-300">
              <p class="max-w-xl whitespace-pre-wrap break-words">{{ report.reason }}</p>
              <p v-if="report.resolution_note" class="mt-2 text-xs text-gray-500 dark:text-gray-400">Resolution: {{ report.resolution_note }}</p>
            </td>
            <td class="px-6 py-4 text-sm"><TeamReportStatusBadge :status="report.status" /></td>
            <td class="px-6 py-4 text-sm text-gray-600 dark:text-gray-300">{{ formatDate(report.created_at) }}</td>
            <td class="px-6 py-4 text-right text-sm">
              <button class="btn btn-outline" @click="$emit('review', report)">Review</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import TeamReportStatusBadge from '~/components/molecules/hackathons/TeamReportStatusBadge.vue'
import type { HackathonTeamReportSummary } from '~/composables/useHackathonTeamReports'

defineProps<{
  reports: HackathonTeamReportSummary[]
}>()

defineEmits<{
  (e: 'review', report: HackathonTeamReportSummary): void
}>()

function formatDate(value: string) {
  return new Date(value).toLocaleString()
}
</script>
