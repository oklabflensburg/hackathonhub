<template>
  <div>
    <label
      v-if="label"
      class="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-2"
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
    <div class="space-y-2">
      <div
        v-for="option in options"
        :key="option.value"
        class="flex items-center"
      >
        <Radio
          :id="`${id}-${option.value}`"
          :model-value="modelValue"
          :value="option.value"
          :label="option.label"
          :name="name"
          :disabled="disabled || option.disabled"
          @update:model-value="$emit('update:modelValue', $event)"
        />
        <label
          :for="`${id}-${option.value}`"
          class="ml-2 text-sm text-gray-700 dark:text-gray-300 cursor-pointer"
          :class="{ 'opacity-50': disabled || option.disabled }"
        >
          {{ option.label }}
          <span
            v-if="option.description"
            class="block text-xs text-gray-500 dark:text-gray-400 mt-0.5"
          >
            {{ option.description }}
          </span>
        </label>
      </div>
    </div>
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
import Radio from '~/components/atoms/Radio.vue'

interface Option {
  value: string | number
  label: string
  description?: string
  disabled?: boolean
}

interface Props {
  modelValue: string | number
  label?: string
  description?: string
  error?: string
  options: Option[]
  name?: string
  id?: string
  required?: boolean
  disabled?: boolean
}

withDefaults(defineProps<Props>(), {
  label: '',
  description: '',
  error: '',
  name: undefined,
  id: undefined,
  required: false,
  disabled: false
})

defineEmits<{
  'update:modelValue': [value: string | number]
}>()
</script>