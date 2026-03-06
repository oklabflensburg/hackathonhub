<template>
  <div class="flex justify-between items-center">
    <span class="text-gray-600 dark:text-gray-400">{{ label }}</span>
    <span v-if="value !== undefined && value !== null" class="font-bold text-gray-900 dark:text-white">{{ formattedValue }}</span>
    <slot v-else name="value">
      <span class="font-bold text-gray-900 dark:text-white">N/A</span>
    </slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  label: string
  value?: string | number
  format?: (val: string | number) => string
}>()

const formattedValue = computed(() => {
  if (props.value === undefined || props.value === null) return 'N/A'
  if (props.format) return props.format(props.value)
  return String(props.value)
})
</script>