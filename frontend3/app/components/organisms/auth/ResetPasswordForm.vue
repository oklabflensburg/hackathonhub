<template>
  <AuthCard
    :title="props.title"
    :subtitle="props.subtitle"
    :error="props.error"
    :success="props.success"
    :loading="props.loading"
    :disabled="props.disabled"
    :footer-text="props.footerText"
    :footer-link-text="props.footerLinkText"
    :footer-link="props.footerLink"
  >
    <template #default>
      <!-- Invalid Token Message -->
      <div v-if="props.invalidToken" class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 mb-6">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <span class="text-sm text-yellow-600 dark:text-yellow-400">{{ props.invalidTokenMessage }}</span>
        </div>
        <div class="mt-4 text-center">
          <NuxtLink :to="props.requestNewLink" class="text-sm font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400">
            {{ props.requestNewLinkText }}
          </NuxtLink>
        </div>
      </div>

      <!-- Form (only show if token is valid) -->
      <AuthForm
        v-if="!props.invalidToken"
        :loading="props.loading"
        :disabled="props.disabled"
        :submit-button-text="props.submitButtonText"
        :submit-button-loading-text="props.submitButtonLoadingText"
        @submit="$emit('submit')"
      >
        <template #fields>
          <!-- Password field -->
          <div class="space-y-2">
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ props.passwordLabel }}
            </label>
            <input
              id="password"
              :value="props.password"
              type="password"
              required
              minlength="8"
              :disabled="props.disabled"
              :placeholder="props.passwordPlaceholder"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
              @input="$emit('password-change', ($event.target as HTMLInputElement).value)"
            />
            <p v-if="props.passwordHint" class="mt-2 text-sm text-gray-500 dark:text-gray-400">
              {{ props.passwordHint }}
            </p>
          </div>

          <!-- Confirm Password field -->
          <div class="space-y-2">
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ props.confirmPasswordLabel }}
            </label>
            <input
              id="confirmPassword"
              :value="props.confirmPassword"
              type="password"
              required
              minlength="8"
              :disabled="props.disabled"
              :placeholder="props.confirmPasswordPlaceholder"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
              @input="$emit('confirm-password-change', ($event.target as HTMLInputElement).value)"
            />
            <p v-if="props.passwordMismatch" class="mt-2 text-sm text-red-600 dark:text-red-400">
              {{ props.passwordMismatchMessage }}
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
  password?: string
  confirmPassword?: string
  
  // UI state
  error?: string
  success?: string
  loading?: boolean
  disabled?: boolean
  invalidToken?: boolean
  passwordMismatch?: boolean
  
  // Content
  title?: string
  subtitle?: string
  passwordLabel?: string
  passwordPlaceholder?: string
  passwordHint?: string
  confirmPasswordLabel?: string
  confirmPasswordPlaceholder?: string
  passwordMismatchMessage?: string
  invalidTokenMessage?: string
  requestNewLink?: string
  requestNewLinkText?: string
  submitButtonText?: string
  submitButtonLoadingText?: string
  footerText?: string
  footerLinkText?: string
  footerLink?: string
}

const props = withDefaults(defineProps<Props>(), {
  password: '',
  confirmPassword: '',
  error: undefined,
  success: undefined,
  loading: false,
  disabled: false,
  invalidToken: false,
  passwordMismatch: false,
  title: 'Reset Password',
  subtitle: 'Enter your new password below.',
  passwordLabel: 'New Password',
  passwordPlaceholder: 'Enter your new password',
  passwordHint: 'Password must be at least 8 characters long.',
  confirmPasswordLabel: 'Confirm Password',
  confirmPasswordPlaceholder: 'Confirm your new password',
  passwordMismatchMessage: 'Passwords do not match.',
  invalidTokenMessage: 'This password reset link is invalid or has expired.',
  requestNewLink: '/forgot-password',
  requestNewLinkText: 'Request a new password reset link',
  submitButtonText: 'Reset Password',
  submitButtonLoadingText: 'Resetting...',
  footerText: 'Remember your password?',
  footerLinkText: 'Sign in',
  footerLink: '/login'
})

const emit = defineEmits<{
  'submit': []
  'password-change': [value: string]
  'confirm-password-change': [value: string]
}>()
</script>