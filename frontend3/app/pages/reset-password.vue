<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Title -->
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          {{ t('auth.resetPassword.title') }}
        </h1>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          {{ t('auth.resetPassword.subtitle') }}
        </p>
      </div>

      <!-- Success Message -->
      <div v-if="successMessage" class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-green-600 dark:text-green-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span class="text-sm text-green-600 dark:text-green-400">{{ successMessage }}</span>
        </div>
        <div class="mt-4 text-center">
          <NuxtLink to="/login" class="text-sm font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400">
            {{ t('auth.resetPassword.backToLogin') }}
          </NuxtLink>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-red-600 dark:text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-sm text-red-600 dark:text-red-400">{{ errorMessage }}</span>
        </div>
      </div>

      <!-- Invalid Token Message -->
      <div v-if="invalidToken" class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <span class="text-sm text-yellow-600 dark:text-yellow-400">{{ t('auth.resetPassword.invalidToken') }}</span>
        </div>
        <div class="mt-4 text-center">
          <NuxtLink to="/forgot-password" class="text-sm font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400">
            {{ t('auth.resetPassword.requestNewLink') }}
          </NuxtLink>
        </div>
      </div>

      <!-- Form (only show if token is valid and not successful) -->
      <form v-if="token && !successMessage && !invalidToken" @submit.prevent="handleResetPassword" class="space-y-6">
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ t('auth.resetPassword.newPassword') }}
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            minlength="8"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white"
            :placeholder="t('auth.resetPassword.passwordPlaceholder')"
            :disabled="isLoading"
          />
        </div>

        <div>
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ t('auth.resetPassword.confirmPassword') }}
          </label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            required
            minlength="8"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white"
            :placeholder="t('auth.resetPassword.confirmPasswordPlaceholder')"
            :disabled="isLoading"
          />
          <p v-if="passwordMismatch" class="mt-2 text-sm text-red-600 dark:text-red-400">
            {{ t('auth.resetPassword.passwordMismatch') }}
          </p>
        </div>

        <div class="flex items-center justify-between">
          <NuxtLink to="/login" class="text-sm font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400">
            {{ t('auth.resetPassword.backToLogin') }}
          </NuxtLink>
          
          <button
            type="submit"
            :disabled="isButtonDisabled"
            class="inline-flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ t('auth.resetPassword.resetting') }}
            </span>
            <span v-else>
              {{ t('auth.resetPassword.resetPassword') }}
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from '#imports'

const { t } = useI18n()
const route = useRoute()

const token = ref('')
const password = ref('')
const confirmPassword = ref('')
const isLoading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const invalidToken = ref(false)

const passwordMismatch = computed(() => {
  return password.value && confirmPassword.value && password.value !== confirmPassword.value
})

const isButtonDisabled = computed(() => {
  return Boolean(isLoading.value || passwordMismatch.value)
})

onMounted(() => {
  // Get token from URL query parameter
  const tokenParam = route.query.token as string
  if (!tokenParam) {
    invalidToken.value = true
    errorMessage.value = t('auth.resetPassword.missingToken')
  } else {
    token.value = tokenParam
  }
})

const handleResetPassword = async () => {
  if (passwordMismatch.value) {
    return
  }
  
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    const response = await $fetch<{ message: string }>('/api/auth/reset-password', {
      method: 'POST',
      body: JSON.stringify({ 
        token: token.value,
        new_password: password.value 
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    successMessage.value = response.message || t('auth.resetPassword.successMessage')
  } catch (error: any) {
    console.error('Reset password error:', error)
    
    if (error.data?.detail) {
      errorMessage.value = error.data.detail
      // Check if token is invalid
      if (error.data.detail.includes('Invalid') || error.data.detail.includes('expired')) {
        invalidToken.value = true
      }
    } else {
      errorMessage.value = t('auth.resetPassword.errorMessage')
    }
  } finally {
    isLoading.value = false
  }
}
</script>