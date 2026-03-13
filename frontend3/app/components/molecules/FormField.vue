<template>
  <div class="space-y-2">
    <div class="flex items-center justify-between">
      <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
        {{ label }}
        <span v-if="required" class="text-red-500">*</span>
      </label>
      
      <div v-if="optional" class="text-xs text-gray-500 dark:text-gray-400">
        Optional
      </div>
    </div>
    
    <div class="relative">
      <slot />
      
      <div v-if="icon" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <component :is="icon" class="h-5 w-5 text-gray-400" />
      </div>
    </div>
    
    <div v-if="error || hint" class="text-sm">
      <p v-if="error" class="text-red-600 dark:text-red-400">{{ error }}</p>
      <p v-else-if="hint" class="text-gray-500 dark:text-gray-400">{{ hint }}</p>
    </div>
    
    <div v-if="characterCount && maxLength" class="text-xs text-gray-500 dark:text-gray-400 text-right">
      {{ currentCount }} / {{ maxLength }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, useId } from 'vue'

interface Props {
  label?: string
  error?: string
  hint?: string
  id?: string
  required?: boolean
  optional?: boolean
  icon?: any
  characterCount?: boolean
  maxLength?: number
  currentCount?: number
}

const props = withDefaults(defineProps<Props>(), {
  required: false,
  optional: false,
  characterCount: false,
  currentCount: 0
})

const generatedId = useId()
const id = computed(() => props.id || `form-field-${generatedId}`)
</script>
