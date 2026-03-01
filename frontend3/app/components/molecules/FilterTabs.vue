<template>
  <div class="flex flex-wrap gap-2 border-b border-gray-200 dark:border-gray-700 pb-4">
    <button
      v-for="filter in filters"
      :key="filter.value"
      @click="$emit('update:modelValue', filter.value)"
      :class="[
        'px-4 py-2 rounded-lg font-medium transition-colors',
        modelValue === filter.value
          ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400'
          : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
      ]"
    >
      {{ filter.label }}
    </button>
  </div>
</template>

<script setup lang="ts">
interface Filter {
  label: string
  value: string
}

interface Props {
  filters: Filter[]
  modelValue: string
}

defineProps<Props>()

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>