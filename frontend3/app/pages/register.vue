<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <RegisterForm
      :name="username"
      :email="email"
      :password="password"
      :confirm-password="confirmPassword"
      :terms-accepted="acceptTerms"
      :newsletter-opt-in="newsletterOptIn"
      :error="authStore.error || undefined"
      :success="registrationSuccess ? t('auth.register.successMessage') : undefined"
      :loading="authStore.isLoading"
      :disabled="authStore.isLoading"
      :title="t('auth.register.title')"
      :subtitle="t('auth.register.subtitle')"
      :name-label="t('auth.register.username')"
      :name-placeholder="t('auth.register.usernamePlaceholder')"
      :email-label="t('auth.register.email')"
      :email-placeholder="t('auth.register.emailPlaceholder')"
      :password-label="t('auth.register.password')"
      :password-placeholder="t('auth.register.passwordPlaceholder')"
      :password-hint="t('auth.register.passwordRequirements')"
      :confirm-password-label="t('auth.register.confirmPassword')"
      :confirm-password-placeholder="t('auth.register.confirmPasswordPlaceholder')"
      :terms-label="t('auth.register.termsOfService')"
      :terms-text="t('auth.register.acceptTerms')"
      :terms-link="'/terms'"
      :terms-link-text="t('auth.register.termsOfService')"
      :newsletter-label="t('auth.register.newsletter')"
      :newsletter-text="t('auth.register.newsletterText')"
      :footer-text="t('auth.register.alreadyHaveAccount')"
      :footer-link-text="t('auth.register.signIn')"
      :footer-link="'/login'"
      :submit-button-text="t('auth.register.createAccount')"
      :submit-button-loading-text="t('auth.register.creatingAccount')"
      :show-oauth="true"
      :oauth-providers="['github', 'google']"
      :oauth-divider-text="t('auth.register.orWithEmail')"
      @submit="handleRegistration"
      @name-change="username = $event"
      @email-change="email = $event"
      @password-change="password = $event"
      @confirm-password-change="confirmPassword = $event"
      @oauth-click="handleOAuthClick"
    >
      <!-- Custom success message -->
      <template v-if="registrationSuccess" #success>
        <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4 mb-6">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-green-600 dark:text-green-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <div>
              <p class="text-sm font-medium text-green-600 dark:text-green-400">
                {{ t('auth.register.successTitle') }}
              </p>
              <p class="text-sm text-green-600 dark:text-green-400 mt-1">
                {{ t('auth.register.successMessage') }}
              </p>
            </div>
          </div>
        </div>
      </template>
    </RegisterForm>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useI18n } from 'vue-i18n'
import { authMiddleware } from '~/middleware/auth'
import RegisterForm from '~/components/organisms/auth/RegisterForm.vue'

definePageMeta({
  middleware: authMiddleware
})

const { t } = useI18n()
const authStore = useAuthStore()

const email = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const acceptTerms = ref(false)
const newsletterOptIn = ref(false)
const registrationSuccess = ref(false)

// Redirect authenticated users away from register page
onMounted(() => {
  // Initialize auth to ensure we have latest state
  authStore.initializeAuth()
  
  // If user is already authenticated, redirect to home
  if (authStore.isAuthenticated) {
    navigateTo('/')
  }
})

const handleOAuthClick = (provider: 'github' | 'google' | 'custom') => {
  if (provider === 'github') {
    authStore.loginWithGitHub()
  } else if (provider === 'google') {
    authStore.loginWithGoogle()
  }
}

const handleRegistration = async () => {
  // Validate passwords match
  if (password.value !== confirmPassword.value) {
    authStore.error = t('auth.register.passwordsDoNotMatch')
    return
  }

  // Validate password strength (minimum 8 characters)
  if (password.value.length < 8) {
    authStore.error = t('auth.register.passwordTooShort')
    return
  }

  try {
    await authStore.registerWithEmail({
      email: email.value,
      username: username.value,
      password: password.value,
      confirmPassword: confirmPassword.value
    })
    
    // Show success message
    registrationSuccess.value = true
    
    // Clear form
    email.value = ''
    username.value = ''
    password.value = ''
    confirmPassword.value = ''
    acceptTerms.value = false
    newsletterOptIn.value = false
    
  } catch (error) {
    // Error is already handled in the store
    console.error('Registration failed:', error)
  }
}
</script>