<template>
  <AuthCard
    :title="title"
    :subtitle="subtitle"
    :error="error"
    :success="success"
    :loading="loading"
    :disabled="disabled"
    :footer-text="footerText"
    :footer-link-text="footerLinkText"
    :footer-link="footerLink"
  >
    <template #default>
      <AuthForm
        :loading="loading"
        :disabled="disabled"
        :submit-button-text="submitButtonText"
        :submit-button-loading-text="submitButtonLoadingText"
        @submit="$emit('submit')"
      >
        <template #fields>
          <!-- Email field -->
          <div class="space-y-2">
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ emailLabel }}
            </label>
            <input
              id="email"
              :value="email"
              type="email"
              required
              :disabled="disabled"
              :placeholder="emailPlaceholder"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
              @input="$emit('email-change', ($event.target as HTMLInputElement).value)"
            />
            <p v-if="emailHint" class="mt-2 text-sm text-gray-500 dark:text-gray-400">
              {{ emailHint }}
            </p>
          </div>
        </template>
      </AuthForm>
    </template>
  </AuthCard>
</template>

<script setup lang="ts">
import AuthCard from '~/components/atoms/AuthCard.vue'
import AuthForm from '~/components/molecules/AuthForm.vue'

interface Props {
  // Form data
  email?: string
  
  // UI state
  error?: string
  success?: string
  loading?: boolean
  disabled?: boolean
  
  // Content
  title?: string
  subtitle?: string
  emailLabel?: string
  emailPlaceholder?: string
  emailHint?: string
  submitButtonText?: string
  submitButtonLoadingText?: string
  footerText?: string
  footerLinkText?: string
  footerLink?: string
}

const props = withDefaults(defineProps<Props>(), {
  email: '',
  error: undefined,
  success: undefined,
  loading: false,
  disabled: false,
  title: 'Forgot Password',
  subtitle: 'Enter your email address and we will send you a link to reset your password.',
  emailLabel: 'Email Address',
  emailPlaceholder: 'you@example.com',
  emailHint: 'We will send you a password reset link to this email address.',
  submitButtonText: 'Send Reset Link',
  submitButtonLoadingText: 'Sending...',
  footerText: 'Remember your password?',
  footerLinkText: 'Sign in',
  footerLink: '/login'
})

const emit = defineEmits<{
  'submit': []
  'email-change': [value: string]
}>()
</script>