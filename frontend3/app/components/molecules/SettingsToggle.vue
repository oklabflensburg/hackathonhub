<template>
  <div class="flex items-center justify-between">
    <div class="flex-1">
      <div class="flex items-center">
        <label
          :for="id"
          class="text-sm font-medium text-gray-900 dark:text-gray-100"
        >
          {{ label }}
        </label>
        <span
          v-if="required"
          class="ml-1 text-xs text-red-500 dark:text-red-400"
          aria-label="Required"
        >
          *
        </span>
      </div>
      <p
        v-if="description"
        class="mt-1 text-sm text-gray-500 dark:text-gray-400"
      >
        {{ description }}
      </p>
    </div>
    <div class="ml-4">
      <ToggleSwitch
        :id="id"
        :model-value="modelValue"
        :disabled="disabled"
        @update:model-value="$emit('update:modelValue', $event)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import ToggleSwitch from '~/components/atoms/ToggleSwitch.vue'

interface Props {
  modelValue: boolean
  label: string
  description?: string
  id?: string
  required?: boolean
  disabled?: boolean
}

withDefaults(defineProps<Props>(), {
  description: '',
  id: undefined,
  required: false,
  disabled: false
})

defineEmits<{
  'update:modelValue': [value: boolean]
}>()
</script>