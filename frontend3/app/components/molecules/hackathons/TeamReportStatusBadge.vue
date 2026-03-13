<template>
  <span :class="badgeClass" class="inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold uppercase tracking-wide">
    {{ statusLabel }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: string
}>()

const statusLabel = computed(() => props.status.replace('_', ' '))
const badgeClass = computed(() => {
  switch (props.status) {
    case 'resolved':
      return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300'
    case 'reviewed':
      return 'bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-300'
    case 'dismissed':
      return 'bg-slate-200 text-slate-700 dark:bg-slate-600/30 dark:text-slate-200'
    default:
      return 'bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-300'
  }
})
</script>
