<template>
  <div class="relative">
    <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <div class="relative">
      <select
        :id="id"
        :value="modelValue"
        :disabled="disabled"
        :class="[
          'w-full px-4 py-2 rounded-lg border focus:ring-2 focus:ring-offset-1 transition-colors appearance-none',
          'bg-white dark:bg-gray-800 text-gray-900 dark:text-white',
          error ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-gray-300 dark:border-gray-600 focus:border-primary-500 focus:ring-primary-500/20',
          disabled && 'opacity-50 cursor-not-allowed'
        ]"
        @change="onChange($event)"
        @blur="$emit('blur')"
        @focus="$emit('focus')"
      >
        <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
        <option
          v-for="option in options"
          :key="option.value === null ? 'null' : option.value"
          :value="option.value"
          :disabled="option.disabled"
        >
          {{ option.label }}
        </option>
      </select>
      
      <!-- Dropdown arrow -->
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-gray-500 dark:text-gray-400">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </div>
    
    <div v-if="error || hint" class="mt-1 text-sm">
      <p v-if="error" class="text-red-600 dark:text-red-400">{{ error }}</p>
      <p v-else-if="hint" class="text-gray-500 dark:text-gray-400">{{ hint }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Option {
  value: string | number | null
  label: string
  disabled?: boolean
}

interface Props {
  modelValue?: string | number | null
  label?: string
  placeholder?: string
  options: Option[]
  error?: string
  hint?: string
  id?: string
  disabled?: boolean
  required?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  required: false
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number | null]
  blur: []
  focus: []
}>()

function onChange(event: Event) {
  const target = event.target as HTMLSelectElement
  const selectedValue = target.value
  // Find the corresponding option to get the original type
  const option = props.options.find(opt => {
    if (opt.value === null) {
      // For null values, the HTML value will be empty string
      return selectedValue === '' || selectedValue === 'null'
    }
    // Compare string representation
    return String(opt.value) === selectedValue
  })
  // If option found, emit the original value, otherwise emit the string
  const emittedValue = option ? option.value : selectedValue
  emit('update:modelValue', emittedValue)
}

const id = computed(() => props.id || `select-${Math.random().toString(36).substr(2, 9)}`)
</script>