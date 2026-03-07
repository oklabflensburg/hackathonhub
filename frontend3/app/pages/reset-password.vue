<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <ResetPasswordForm
      :password="password"
      :confirm-password="confirmPassword"
      :error="errorMessage"
      :success="successMessage"
      :loading="isLoading"
      :disabled="isLoading"
      :invalid-token="invalidToken"
      :password-mismatch="passwordMismatch"
      :title="t('auth.resetPassword.title')"
      :subtitle="t('auth.resetPassword.subtitle')"
      :password-label="t('auth.resetPassword.newPassword')"
      :password-placeholder="t('auth.resetPassword.passwordPlaceholder')"
      :password-hint="t('auth.resetPassword.passwordRequirements')"
      :confirm-password-label="t('auth.resetPassword.confirmPassword')"
      :confirm-password-placeholder="t('auth.resetPassword.confirmPasswordPlaceholder')"
      :password-mismatch-message="t('auth.resetPassword.passwordMismatch')"
      :invalid-token-message="t('auth.resetPassword.invalidToken')"
      :request-new-link="'/forgot-password'"
      :request-new-link-text="t('auth.resetPassword.requestNewLink')"
      :submit-button-text="t('auth.resetPassword.resetPassword')"
      :submit-button-loading-text="t('auth.resetPassword.resetting')"
      :footer-text="t('auth.resetPassword.backToLogin')"
      :footer-link-text="t('auth.resetPassword.backToLogin')"
      :footer-link="'/login'"
      @submit="handleResetPassword"
      @password-change="password = $event"
      @confirm-password-change="confirmPassword = $event"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from '#imports'
import { useUIStore } from '~/stores/ui'
import { useAuthStore } from '~/stores/auth'
import ResetPasswordForm from '~/components/organisms/auth/ResetPasswordForm.vue'

const { t } = useI18n()
const route = useRoute()
const config = useRuntimeConfig()
const uiStore = useUIStore()
const authStore = useAuthStore()

const token = ref('')
const password = ref('')
const confirmPassword = ref('')
const isLoading = ref(false)
const invalidToken = ref(false)
const errorMessage = ref<string | undefined>(undefined)
const successMessage = ref<string | undefined>(undefined)

const passwordMismatch = computed(() => {
  return Boolean(password.value && confirmPassword.value && password.value !== confirmPassword.value)
})

onMounted(() => {
  // Get token from URL query parameter
  const tokenParam = route.query.token as string
  if (!tokenParam) {
    invalidToken.value = true
    errorMessage.value = t('auth.resetPassword.missingToken')
    uiStore.showError(
      t('auth.resetPassword.missingToken'),
      t('auth.resetPassword.title')
    )
  } else {
    token.value = tokenParam
  }
})

const handleResetPassword = async () => {
  if (passwordMismatch.value) {
    errorMessage.value = t('auth.resetPassword.passwordMismatch')
    uiStore.showError(
      t('auth.resetPassword.passwordMismatch'),
      t('auth.resetPassword.title')
    )
    return
  }
  
  isLoading.value = true
  errorMessage.value = undefined
  successMessage.value = undefined
  
  try {
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    const response = await fetch(`${backendUrl}/api/auth/reset-password`, {
      method: 'POST',
      body: JSON.stringify({ 
        token: token.value,
        new_password: password.value 
      }),
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
    successMessage.value = data.message || t('auth.resetPassword.successMessage')
    
    // Also show notification
    uiStore.showSuccess(
      data.message || t('auth.resetPassword.successMessage'),
      t('auth.resetPassword.title')
    )
    
    // Clear form
    password.value = ''
    confirmPassword.value = ''
    
    // Redirect to login after a short delay
    setTimeout(() => {
      navigateTo('/login')
    }, 2000)
    
  } catch (error: any) {
    console.error('Reset password error:', error)
    
    // Show error message in the form
    errorMessage.value = error.message || t('auth.resetPassword.errorMessage')
    
    // Also show notification
    uiStore.showError(
      error.message || t('auth.resetPassword.errorMessage'),
      t('auth.resetPassword.title')
    )
    
    // Check if token is invalid
    if (error.message.includes('Invalid') || error.message.includes('expired')) {
      invalidToken.value = true
    }
  } finally {
    isLoading.value = false
  }
}
</script>