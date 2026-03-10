<template>
  <button
    type="button"
    role="tab"
    :aria-selected="active"
    :aria-controls="panelId"
    :id="tabId"
    :disabled="disabled"
    :class="[
      'inline-flex items-center justify-center whitespace-nowrap px-4 py-2 text-sm font-medium rounded-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
      active
        ? 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300'
        : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800',
      disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'
    ]"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
interface Props {
  active?: boolean
  disabled?: boolean
  tabId?: string
  panelId?: string
}

withDefaults(defineProps<Props>(), {
  active: false,
  disabled: false,
  tabId: undefined,
  panelId: undefined
})

defineEmits<{
  click: []
}>()
</script>