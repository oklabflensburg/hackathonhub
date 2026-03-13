<template>
  <div class="grid gap-4 rounded-2xl border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-800 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)_auto]">
    <label class="space-y-2 text-sm">
      <span class="font-medium text-gray-700 dark:text-gray-200">Status</span>
      <select v-model="localStatus" class="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm dark:border-gray-600 dark:bg-gray-900 dark:text-white">
        <option value="">All statuses</option>
        <option value="pending">Pending</option>
        <option value="reviewed">Reviewed</option>
        <option value="resolved">Resolved</option>
        <option value="dismissed">Dismissed</option>
      </select>
    </label>

    <label class="space-y-2 text-sm">
      <span class="font-medium text-gray-700 dark:text-gray-200">Team</span>
      <select v-model="localTeamId" class="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm dark:border-gray-600 dark:bg-gray-900 dark:text-white">
        <option value="">All teams</option>
        <option v-for="team in teams" :key="team.id" :value="String(team.id)">{{ team.name }}</option>
      </select>
    </label>

    <div class="flex items-end gap-3">
      <button class="btn btn-primary" @click="applyFilters">Apply</button>
      <button class="btn btn-outline" @click="resetFilters">Reset</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  status?: string
  teamId?: number | null
  teams: Array<{ id: number; name: string }>
}>()

const emit = defineEmits<{
  (e: 'apply', payload: { status?: string; teamId?: number | null }): void
}>()

const localStatus = ref(props.status || '')
const localTeamId = ref(props.teamId ? String(props.teamId) : '')

watch(() => props.status, (value) => {
  localStatus.value = value || ''
})
watch(() => props.teamId, (value) => {
  localTeamId.value = value ? String(value) : ''
})

function applyFilters() {
  emit('apply', {
    status: localStatus.value || undefined,
    teamId: localTeamId.value ? Number(localTeamId.value) : null,
  })
}

function resetFilters() {
  localStatus.value = ''
  localTeamId.value = ''
  applyFilters()
}
</script>
