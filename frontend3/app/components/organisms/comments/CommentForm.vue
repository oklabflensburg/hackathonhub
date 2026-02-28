<template>
  <div>
    <textarea
      :value="modelValue"
      :placeholder="placeholder"
      rows="3"
      class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
      :disabled="loading"
      @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
    />
    <div class="flex justify-end space-x-2 mt-3">
      <Button v-if="showCancel" variant="ghost" :disabled="loading" @click="$emit('cancel')">Cancel</Button>
      <Button variant="primary" :loading="loading" :disabled="!modelValue.trim()" @click="$emit('submit')">
        {{ submitLabel }}
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from '~/components/atoms/Button.vue'

interface Props {
  modelValue: string
  loading?: boolean
  placeholder?: string
  showCancel?: boolean
  submitLabel?: string
}

withDefaults(defineProps<Props>(), {
  loading: false,
  placeholder: 'Write a comment…',
  showCancel: false,
  submitLabel: 'Post',
})

defineEmits<{
  'update:modelValue': [value: string]
  submit: []
  cancel: []
}>()
</script>
