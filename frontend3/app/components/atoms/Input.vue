<template>
  <div class="relative">
    <input
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :class="inputClasses"
      @input="onInput"
      @focus="$emit('focus', $event)"
      @blur="$emit('blur', $event)"
      @change="$emit('change', $event)"
    />
    <button
      v-if="clearable && modelValue && !disabled && !readonly"
      type="button"
      class="absolute inset-y-0 right-2 my-auto text-gray-400 hover:text-gray-600"
      @click="clear"
    >
      ✕
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  type?: string
  modelValue?: string | number
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  error?: boolean
  success?: boolean
  clearable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  modelValue: '',
  placeholder: '',
  disabled: false,
  readonly: false,
  error: false,
  success: false,
  clearable: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  focus: [event: FocusEvent]
  blur: [event: FocusEvent]
  input: [event: Event]
  change: [event: Event]
}>()

const inputClasses = computed(() => [
  'w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 transition-colors',
  props.error
    ? 'border-red-500 focus:ring-red-500'
    : props.success
      ? 'border-green-500 focus:ring-green-500'
      : 'border-gray-300 dark:border-gray-600 focus:ring-primary-500',
  props.clearable ? 'pr-9' : '',
])

const onInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
  emit('input', event)
}

const clear = () => emit('update:modelValue', '')
</script>
