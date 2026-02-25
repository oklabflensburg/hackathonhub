<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Title -->
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          {{ t('auth.forgotPassword.title') }}
        </h1>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          {{ t('auth.forgotPassword.subtitle') }}
        </p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleForgotPassword" class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ t('auth.forgotPassword.email') }}
          </label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white"
            :placeholder="t('auth.forgotPassword.emailPlaceholder')"
            :disabled="isLoading"
          />
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            {{ t('auth.forgotPassword.instructions') }}
          </p>
        </div>

        <div class="flex items-center justify-between">
          <NuxtLink to="/login" class="text-sm font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400">
            {{ t('auth.forgotPassword.backToLogin') }}
          </NuxtLink>
          
          <button
            type="submit"
            :disabled="isLoading"
            class="inline-flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ t('auth.forgotPassword.sending') }}
            </span>
            <span v-else>
              {{ t('auth.forgotPassword.sendResetLink') }}
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUIStore } from '~/stores/ui'

const { t } = useI18n()
const config = useRuntimeConfig()
const uiStore = useUIStore()
const authStore = useAuthStore()

const email = ref('')
const isLoading = ref(false)

const handleForgotPassword = async () => {
  isLoading.value = true
  
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
    
    // Show success notification
    uiStore.showSuccess(
      data.message || t('auth.forgotPassword.successMessage'),
      t('auth.forgotPassword.title')
    )
    
    // Clear email field
    email.value = ''
    
  } catch (error: any) {
    console.error('Forgot password error:', error)
    
    // Show error notification
    uiStore.showError(
      error.message || t('auth.forgotPassword.errorMessage'),
      t('auth.forgotPassword.title')
    )
  } finally {
    isLoading.value = false
  }
}
</script>