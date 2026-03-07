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
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUIStore } from '~/stores/ui'
import { useAuthStore } from '~/stores/auth'
import ForgotPasswordForm from '~/components/organisms/auth/ForgotPasswordForm.vue'

const { t } = useI18n()
const config = useRuntimeConfig()
const uiStore = useUIStore()
const authStore = useAuthStore()

const email = ref('')
const isLoading = ref(false)
const errorMessage = ref<string | undefined>(undefined)
const successMessage = ref<string | undefined>(undefined)

const handleForgotPassword = async () => {
  isLoading.value = true
  errorMessage.value = undefined
  successMessage.value = undefined
  
  try {
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    const response = await fetch(`${backendUrl}/api/auth/forgot-password`, {
      method: 'POST',
      body: JSON.stringify({ email: email.value }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP error ${response.status}`)
    }
    
    const data = await response.json()
    
    // Show success message in the form
    successMessage.value = data.message || t('auth.forgotPassword.successMessage')
    
    // Also show notification
    uiStore.showSuccess(
      data.message || t('auth.forgotPassword.successMessage'),
      t('auth.forgotPassword.title')
    )
    
    // Clear email field
    email.value = ''
    
  } catch (error: any) {
    console.error('Forgot password error:', error)
    
    // Show error message in the form
    errorMessage.value = error.message || t('auth.forgotPassword.errorMessage')
    
    // Also show notification
    uiStore.showError(
      error.message || t('auth.forgotPassword.errorMessage'),
      t('auth.forgotPassword.title')
    )
  } finally {
    isLoading.value = false
  }
}
</script>