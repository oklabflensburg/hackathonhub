<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <LoginForm
      :email="email"
      :password="password"
      :remember-me="rememberMe"
      :error="authStore.error || undefined"
      :loading="authStore.isLoading"
      :disabled="authStore.isLoading"
      :title="t('auth.login.title')"
      :subtitle="t('auth.login.subtitle')"
      :email-label="t('auth.login.email')"
      :email-placeholder="t('auth.login.emailPlaceholder')"
      :password-label="t('auth.login.password')"
      :password-placeholder="t('auth.login.passwordPlaceholder')"
      :remember-me-label="t('auth.login.rememberMe')"
      :forgot-password-text="t('auth.login.forgotPassword')"
      :forgot-password-link="'/forgot-password'"
      :submit-button-text="t('auth.login.signIn')"
      :submit-button-loading-text="t('auth.login.signingIn')"
      :footer-text="t('auth.login.noAccount')"
      :footer-link-text="t('auth.login.createAccount')"
      :footer-link="'/register'"
      :show-oauth="true"
      :oauth-providers="['github', 'google']"
      :oauth-divider-text="t('auth.login.orWithEmail')"
      @submit="handleEmailLogin"
      @email-change="email = $event"
      @password-change="password = $event"
      @oauth-click="handleOAuthClick"
    >
      <!-- Custom error handling for email verification -->
      <template v-if="authStore.error" #error>
        <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-red-600 dark:text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="text-sm text-red-600 dark:text-red-400">{{ authStore.error }}</span>
          </div>
          <div v-if="isEmailVerificationError" class="mt-3">
            <button
              @click="resendVerificationEmail"
              :disabled="resendLoading"
              class="text-sm font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="resendLoading" class="flex items-center">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-primary-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ t('auth.verifyEmail.sending') }}
              </span>
              <span v-else>
                {{ t('auth.verifyEmail.resendVerification') }}
              </span>
            </button>
            <div v-if="resendSuccess" class="mt-2 text-sm text-green-600 dark:text-green-400">
              {{ t('auth.verifyEmail.verificationEmailSent') }}
            </div>
          </div>
        </div>
      </template>
    </LoginForm>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useI18n } from 'vue-i18n'
import { authMiddleware } from '~/middleware/auth'
import LoginForm from '~/components/organisms/auth/LoginForm.vue'

definePageMeta({
  middleware: authMiddleware
})

const { t } = useI18n()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const resendLoading = ref(false)
const resendSuccess = ref(false)

// Computed property to check if error is email verification error
const isEmailVerificationError = computed(() => {
  const error = authStore.error
  if (!error) return false
  // Check for English "Email not verified" or German "E-Mail nicht verifiziert"
  return error.includes('Email not verified') || error.includes('E-Mail nicht verifiziert')
})

// Redirect authenticated users away from login page
onMounted(() => {
  // Initialize auth to ensure we have latest state
  authStore.initializeAuth()
  
  // If user is already authenticated, redirect to home
  if (authStore.isAuthenticated) {
    navigateTo('/')
  }
})

const resendVerificationEmail = async () => {
  if (!email.value) return
  resendLoading.value = true
  resendSuccess.value = false
  try {
    await authStore.resendVerificationEmail(email.value)
    resendSuccess.value = true
  } catch (error) {
    console.error('Failed to resend verification email:', error)
  } finally {
    resendLoading.value = false
  }
}

const handleOAuthClick = (provider: 'github' | 'google' | 'custom') => {
  if (provider === 'github') {
    authStore.loginWithGitHub()
  } else if (provider === 'google') {
    authStore.loginWithGoogle()
  }
}

const handleEmailLogin = async () => {
  try {
    const loginSuccessful = await authStore.loginWithEmail({
      email: email.value,
      password: password.value
    })
    
    // Only redirect to home if login was successful and 2FA was not required
    if (loginSuccessful) {
      navigateTo('/')
    }
    // If 2FA is required, the auth store already navigated to /verify-2fa
  } catch (error) {
    // Error is already handled in the store
    console.error('Login failed:', error)
  }
}
</script>