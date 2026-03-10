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
    <div class="relative">
      <slot name="prefix" />
      <Input
        :id="id"
        :model-value="modelValue"
        :type="type"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :error="!!error"
        :class="[
          prefixIcon ? 'pl-10' : '',
          suffixIcon ? 'pr-10' : ''
        ]"
        @update:model-value="$emit('update:modelValue', $event)"
        @blur="$emit('blur')"
        @focus="$emit('focus')"
      />
      <slot name="suffix" />
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
import Input from '~/components/atoms/Input.vue'

interface Props {
  modelValue: string
  label?: string
  description?: string
  error?: string
  type?: string
  placeholder?: string
  id?: string
  required?: boolean
  disabled?: boolean
  readonly?: boolean
  prefixIcon?: boolean
  suffixIcon?: boolean
}

withDefaults(defineProps<Props>(), {
  label: '',
  description: '',
  error: '',
  type: 'text',
  placeholder: '',
  id: undefined,
  required: false,
  disabled: false,
  readonly: false,
  prefixIcon: false,
  suffixIcon: false
})

defineEmits<{
  'update:modelValue': [value: string]
  blur: []
  focus: []
}>()
</script>