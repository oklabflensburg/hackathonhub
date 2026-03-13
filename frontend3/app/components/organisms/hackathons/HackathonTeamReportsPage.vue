<template>
  <section class="space-y-6">
    <header class="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
      <div>
        <p class="text-sm font-medium uppercase tracking-[0.2em] text-gray-500 dark:text-gray-400">Moderation</p>
        <h1 class="text-3xl font-semibold text-gray-900 dark:text-white">Team Reports</h1>
        <p class="text-sm text-gray-600 dark:text-gray-300">Review reports submitted against teams in this hackathon.</p>
      </div>
      <NuxtLink :to="`/hackathons/${hackathonId}`" class="btn btn-outline">Back to Hackathon</NuxtLink>
    </header>

    <TeamReportFilters :status="filters.status" :team-id="filters.teamId" :teams="teams" @apply="$emit('apply-filters', $event)" />
    <TeamReportsTable :reports="reports" @review="$emit('review', $event)" />
  </section>
</template>

<script setup lang="ts">
import TeamReportFilters from '~/components/molecules/hackathons/TeamReportFilters.vue'
import TeamReportsTable from '~/components/organisms/hackathons/TeamReportsTable.vue'
import type { HackathonTeamReportSummary } from '~/composables/useHackathonTeamReports'

defineProps<{
  hackathonId: string
  reports: HackathonTeamReportSummary[]
  teams: Array<{ id: number; name: string }>
  filters: { status?: string; teamId?: number | null }
}>()

defineEmits<{
  (e: 'apply-filters', payload: { status?: string; teamId?: number | null }): void
  (e: 'review', report: HackathonTeamReportSummary): void
}>()
</script>
