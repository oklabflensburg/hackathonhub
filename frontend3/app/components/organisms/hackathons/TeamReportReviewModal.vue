<template>
  <Modal :model-value="visible" @update:model-value="value => { if (!value) $emit('close') }" @close="$emit('close')">
    <div class="space-y-5">
      <div>
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Review Team Report</h3>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">{{ report?.team?.name || `Team #${report?.team_id}` }}</p>
      </div>

      <div class="rounded-xl border border-gray-200 bg-gray-50 p-4 text-sm text-gray-700 dark:border-gray-700 dark:bg-gray-900/50 dark:text-gray-200">
        {{ report?.reason }}
      </div>

      <label class="block space-y-2 text-sm">
        <span class="font-medium text-gray-700 dark:text-gray-200">Status</span>
        <select v-model="localStatus" class="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 dark:border-gray-600 dark:bg-gray-900 dark:text-white">
          <option value="pending">Pending</option>
          <option value="reviewed">Reviewed</option>
          <option value="resolved">Resolved</option>
          <option value="dismissed">Dismissed</option>
        </select>
      </label>

      <label class="block space-y-2 text-sm">
        <span class="font-medium text-gray-700 dark:text-gray-200">Resolution note</span>
        <textarea v-model="localNote" rows="4" class="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 dark:border-gray-600 dark:bg-gray-900 dark:text-white" placeholder="Add a moderation note"></textarea>
      </label>

      <div class="flex justify-end gap-3">
        <button class="btn btn-outline" @click="$emit('close')">Cancel</button>
        <button class="btn btn-primary" :disabled="loading" @click="submit">{{ loading ? 'Saving...' : 'Save review' }}</button>
      </div>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Modal from '~/components/molecules/Modal.vue'
import type { HackathonTeamReportSummary } from '~/composables/useHackathonTeamReports'

const props = defineProps<{
  visible: boolean
  report: HackathonTeamReportSummary | null
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'submit', payload: { status: string; resolution_note?: string | null }): void
}>()

const localStatus = ref('pending')
const localNote = ref('')

watch(() => props.report, (report) => {
  localStatus.value = report?.status || 'pending'
  localNote.value = report?.resolution_note || ''
}, { immediate: true })

function submit() {
  emit('submit', {
    status: localStatus.value,
    resolution_note: localNote.value.trim() || null,
  })
}
</script>
