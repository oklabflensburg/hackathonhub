a<template>
  <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4 sm:p-5 lg:p-6 mb-6">
    <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">{{ title }}</h3>
    <div class="space-y-4">
      <div class="flex justify-between items-center">
        <span class="text-gray-600 dark:text-gray-400">{{ labels.status }}</span>
        <Badge :variant="statusVariant" class="capitalize">{{ hackathon.status }}</Badge>
      </div>
      <StatItem :label="labels.participants" :value="hackathon.participant_count || 0" />
      <StatItem :label="labels.views" :value="hackathon.view_count || 0" />
      <StatItem :label="labels.projects" :value="hackathon.project_count || 0" />
      <StatItem :label="labels.registrationDeadline" :value="hackathon.registration_deadline" :format="(val) => formatDateTime(String(val))" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { HackathonStatsProps } from '~/types/hackathon-types'
import Badge from '~/components/atoms/Badge.vue'
import StatItem from '~/components/molecules/StatItem.vue'

const props = defineProps<HackathonStatsProps>()

const statusVariant = computed(() => {
  if (props.hackathon.status === 'active') return 'success'
  if (props.hackathon.status === 'upcoming') return 'warning'
  return 'gray'
})
</script>