<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <ForgotPasswordForm
      :email="email"
      :error="errorMessage"
      :success="successMessage"
      :loading="isLoading"
      :disabled="isLoading"
      :title="t('auth.forgotPassword.title')"
      :subtitle="t('auth.forgotPassword.subtitle')"
      :email-label="t('auth.forgotPassword.email')"
      :email-placeholder="t('auth.forgotPassword.emailPlaceholder')"
      :email-hint="t('auth.forgotPassword.instructions')"
      :submit-button-text="t('auth.forgotPassword.sendResetLink')"
      :submit-button-loading-text="t('auth.forgotPassword.sending')"
      :footer-text="t('auth.forgotPassword.backToLogin')"
      :footer-link-text="t('auth.forgotPassword.backToLogin')"
      :footer-link="'/login'"
      @submit="handleForgotPassword"
      @email-change="email = $event"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUIStore } from '~/stores/ui'
import { useAuth } from '~/composables/useAuth'
import ForgotPasswordForm from '~/components/organisms/auth/ForgotPasswordForm.vue'

const { t } = useI18n()
const uiStore = useUIStore()
const { forgotPassword, isLoading: authLoading, error: authError, clearError } = useAuth({
  autoRedirect: false
})

const email = ref('')
const successMessage = ref<string | undefined>(undefined)

// Computed Properties
const isLoading = computed(() => authLoading.value)
const errorMessage = computed(() => {
  const err = authError.value
  return err === null ? undefined : err
})

const handleForgotPassword = async () => {
  clearError()
  successMessage.value = undefined
  
  try {
    await forgotPassword({ email: email.value })
    
    // Show success message in the form
    successMessage.value = t('auth.forgotPassword.successMessage')
    
    // Also show notification
    uiStore.showSuccess(
      t('auth.forgotPassword.successMessage'),
      t('auth.forgotPassword.title')
    )
    
    // Clear email field
    email.value = ''
    
  } catch (error: any) {
    console.error('Forgot password error:', error)
    
    // Error message wird bereits vom Composable gesetzt
    // Zusätzliche Notification anzeigen
    uiStore.showError(
      error.message || t('auth.forgotPassword.errorMessage'),
      t('auth.forgotPassword.title')
    )
  }
}
</script>