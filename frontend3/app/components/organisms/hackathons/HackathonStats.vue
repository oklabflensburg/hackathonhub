<template>
  <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4 sm:p-5 lg:p-6 mb-6">
    <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">{{ title }}</h3>
    <div class="space-y-4">
      <div class="flex justify-between items-center">
        <span class="text-gray-600 dark:text-gray-400">{{ labels.status }}</span>
        <HackathonStatusBadge :status="hackathon.status" :tooltip="getStatusTooltip(hackathon.status)" />
      </div>
      <StatItem :label="labels.participants" :value="hackathon.participantCount || hackathon.participant_count || 0" />
      <StatItem :label="labels.views" :value="hackathon.viewCount || hackathon.view_count || 0" />
      <StatItem :label="labels.projects" :value="hackathon.projectCount || hackathon.project_count || 0" />
      <StatItem :label="labels.registrationDeadline" :value="hackathon.registrationDeadline || hackathon.registration_deadline || ''" :format="(val) => formatDateTime(String(val))" />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { HackathonStatsProps } from '~/types/hackathon-types'
import HackathonStatusBadge from '~/components/atoms/HackathonStatusBadge.vue'
import StatItem from '~/components/molecules/StatItem.vue'

const props = defineProps<HackathonStatsProps>()

const getStatusTooltip = (status: string) => {
  switch (status) {
    case 'active': return 'This hackathon is currently running'
    case 'upcoming': return 'This hackathon will start soon'
    case 'completed': return 'This hackathon has ended'
    default: return `Status: ${status}`
  }
}
</script>
