<template>
  <div>
    <label
      v-if="label"
      :for="id"
      class="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-1"
    >
      {{ label }}
      <span
        v-if="required"
        class="ml-1 text-xs text-red-500 dark:text-red-400"
        aria-label="Required"
      >
        *
      </span>
    </label>
    <Select
      :id="id"
      :model-value="modelValue"
      :options="options"
      :placeholder="placeholder"
      :disabled="disabled"
      :error="!!error"
      @update:model-value="$emit('update:modelValue', $event)"
    />
    <div v-if="description || error" class="mt-1">
      <p
        v-if="description && !error"
        class="text-sm text-gray-500 dark:text-gray-400"
      >
        {{ description }}
      </p>
      <p
        v-if="error"
        class="text-sm text-red-600 dark:text-red-400"
      >
        {{ error }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import Select from '~/components/atoms/Select.vue'

interface Option {
  value: string | number | null
  label: string
  disabled?: boolean
}

interface Props {
  modelValue: string | number | null
  label?: string
  description?: string
  error?: string
  options: Option[]
  placeholder?: string
  id?: string
  required?: boolean
  disabled?: boolean
}

withDefaults(defineProps<Props>(), {
  label: '',
  description: '',
  error: '',
  placeholder: 'Select an option',
  id: undefined,
  required: false,
  disabled: false
})

defineEmits<{
  'update:modelValue': [value: string | number | null]
}>()
</script>