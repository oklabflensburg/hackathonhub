<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <EmailVerificationStatus
      :loading="isLoading"
      :verified="isVerified"
      :error="error"
      :title="t('auth.verifyEmail.title')"
      :subtitle="t('auth.verifyEmail.subtitle')"
      :loading-message="t('auth.verifyEmail.verifying')"
      :success-title="t('auth.verifyEmail.successTitle')"
      :success-message="t('auth.verifyEmail.successMessage')"
      :error-title="t('auth.verifyEmail.errorTitle')"
      :no-token-title="t('auth.verifyEmail.noTokenTitle')"
      :no-token-message="t('auth.verifyEmail.noTokenMessage')"
      :login-button-text="t('auth.verifyEmail.goToLogin')"
      :register-button-text="t('auth.verifyEmail.registerAgain')"
      :login-link="'/login'"
      :register-link="'/register'"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from '#imports'
import { useI18n } from 'vue-i18n'
import { useAuth } from '~/composables/useAuth'
import EmailVerificationStatus from '~/components/organisms/auth/EmailVerificationStatus.vue'

const { t } = useI18n()
const route = useRoute()
const { verifyEmail, isLoading: authLoading, error: authError, clearError } = useAuth({
  autoRedirect: false
})

const isVerified = ref(false)
const error = ref<string | undefined>(undefined)

// Computed Properties
const isLoading = ref(true)

onMounted(async () => {
  const token = route.query.token as string

  if (!token) {
    isLoading.value = false
    return
  }

  try {
    clearError()
    await verifyEmail({ token })
    isVerified.value = true
    error.value = undefined
  } catch (err: any) {
    error.value = err.message || 'Unknown error occurred'
    isVerified.value = false
  } finally {
    isLoading.value = false
  }
})
</script>