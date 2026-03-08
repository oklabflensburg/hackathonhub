<template>
  <div class="relative">
    <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <textarea
      :id="id"
      :value="modelValue"
      :placeholder="placeholder"
      :rows="rows"
      :disabled="disabled"
      :readonly="readonly"
      :class="[
        'w-full px-4 py-3 rounded-lg border focus:ring-2 focus:ring-offset-1 transition-colors',
        'bg-white dark:bg-gray-800 text-gray-900 dark:text-white',
        'placeholder-gray-500 dark:placeholder-gray-400',
        error ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-gray-300 dark:border-gray-600 focus:border-primary-500 focus:ring-primary-500/20',
        disabled && 'opacity-50 cursor-not-allowed',
        resize && 'resize' || 'resize-none'
      ]"
      @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
      @blur="$emit('blur')"
      @focus="$emit('focus')"
    />
    
    <div v-if="(typeof error === 'string' && error) || hint" class="mt-1 text-sm">
      <p v-if="typeof error === 'string' && error" class="text-red-600 dark:text-red-400">{{ error }}</p>
      <p v-else-if="hint" class="text-gray-500 dark:text-gray-400">{{ hint }}</p>
    </div>
    
    <div v-if="characterCount" class="mt-1 text-xs text-gray-500 dark:text-gray-400 text-right">
      {{ modelValue?.toString().length || 0 }} / {{ maxLength }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue?: string
  label?: string
  placeholder?: string
  error?: string | boolean
  hint?: string
  id?: string
  rows?: number
  disabled?: boolean
  readonly?: boolean
  required?: boolean
  resize?: boolean
  characterCount?: boolean
  maxLength?: number
}

const props = withDefaults(defineProps<Props>(), {
  rows: 4,
  resize: false,
  characterCount: false,
  maxLength: 500
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  blur: []
  focus: []
}>()

const id = computed(() => props.id || `textarea-${Math.random().toString(36).substr(2, 9)}`)
</script>