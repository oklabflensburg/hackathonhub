<template>
  <form
    :class="[
      'space-y-6',
      className
    ]"
    @submit.prevent="$emit('submit', $event)"
  >
    <!-- Form Header -->
    <div v-if="title || subtitle" class="text-center">
      <h2 v-if="title" class="text-2xl font-bold text-gray-900 dark:text-white">
        {{ title }}
      </h2>
      <p v-if="subtitle" class="mt-2 text-sm text-gray-600 dark:text-gray-400">
        {{ subtitle }}
      </p>
    </div>

    <!-- Error Message -->
    <div
      v-if="error"
      class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4"
    >
      <div class="flex items-center">
        <svg class="w-5 h-5 text-red-600 dark:text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="text-sm text-red-600 dark:text-red-400">{{ error }}</span>
      </div>
    </div>

    <!-- Success Message -->
    <div
      v-if="success"
      class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4"
    >
      <div class="flex items-center">
        <svg class="w-5 h-5 text-green-600 dark:text-green-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="text-sm text-green-600 dark:text-green-400">{{ success }}</span>
      </div>
    </div>

    <!-- Form Fields Slot -->
    <div class="space-y-4">
      <slot />
    </div>

    <!-- Submit Button -->
    <div>
      <Button
        :type="submitButtonType"
        :variant="submitButtonVariant"
        :size="submitButtonSize"
        :disabled="loading || disabled"
        :full-width="true"
        :class="submitButtonClass"
      >
        <template v-if="loading" #icon-left>
          <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </template>
        {{ loading ? submitButtonLoadingText : submitButtonText }}
      </Button>
    </div>

    <!-- Form Footer Slot -->
    <div v-if="$slots.footer" class="pt-4 border-t border-gray-200 dark:border-gray-700">
      <slot name="footer" />
    </div>
  </form>
</template>

<script setup lang="ts">
import Button from '~/components/atoms/Button.vue'

interface Props {
  title?: string
  subtitle?: string
  error?: string
  success?: string
  loading?: boolean
  disabled?: boolean
  className?: string
  submitButtonText?: string
  submitButtonLoadingText?: string
  submitButtonType?: 'button' | 'submit' | 'reset'
  submitButtonVariant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  submitButtonSize?: 'xs' | 'sm' | 'md' | 'lg'
  submitButtonClass?: string
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  disabled: false,
  className: '',
  submitButtonText: 'Submit',
  submitButtonLoadingText: 'Submitting...',
  submitButtonType: 'submit',
  submitButtonVariant: 'primary',
  submitButtonSize: 'md',
  submitButtonClass: ''
})

const emit = defineEmits<{
  submit: [event: Event]
}>()
</script>