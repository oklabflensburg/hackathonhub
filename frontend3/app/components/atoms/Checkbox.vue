<template>
  <div class="flex items-start">
    <div class="flex items-center h-5">
      <input
        :id="id"
        type="checkbox"
        :checked="modelValue"
        :disabled="disabled"
        :class="[
          'w-4 h-4 rounded border focus:ring-2 focus:ring-offset-1 transition-colors',
          'bg-white dark:bg-gray-800 text-primary-600',
          error ? 'border-red-500 focus:ring-red-500/20' : 'border-gray-300 dark:border-gray-600 focus:ring-primary-500/20',
          disabled && 'opacity-50 cursor-not-allowed'
        ]"
        @change="$emit('update:modelValue', ($event.target as HTMLInputElement).checked)"
        @blur="$emit('blur')"
        @focus="$emit('focus')"
      />
    </div>
    
    <div class="ml-3 text-sm">
      <label :for="id" class="font-medium text-gray-700 dark:text-gray-300 cursor-pointer">
        {{ label }}
        <span v-if="required" class="text-red-500">*</span>
      </label>
      
      <p v-if="description" class="text-gray-500 dark:text-gray-400 mt-1">
        {{ description }}
      </p>
      
      <div v-if="error || hint" class="mt-1">
        <p v-if="error" class="text-red-600 dark:text-red-400">{{ error }}</p>
        <p v-else-if="hint" class="text-gray-500 dark:text-gray-400">{{ hint }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, useId } from 'vue'

interface Props {
  modelValue?: boolean
  label: string
  description?: string
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
  'update:modelValue': [value: boolean]
  blur: []
  focus: []
}>()

const generatedId = useId()
const id = computed(() => props.id || `checkbox-${generatedId}`)
</script>
