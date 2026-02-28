<template>
  <div>
    <label v-if="label" :for="id" class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-200">
      <slot name="label">{{ label }}</slot>
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <slot />

    <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
    <p v-else-if="help" class="mt-1 text-sm text-gray-500 dark:text-gray-400">
      <slot name="help">{{ help }}</slot>
    </p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  label?: string
  required?: boolean
  error?: string
  help?: string
  id?: string
}

withDefaults(defineProps<Props>(), {
  label: '',
  required: false,
  error: '',
  help: '',
  id: undefined,
})
</script>
