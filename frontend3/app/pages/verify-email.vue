<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Title -->
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          {{ t('auth.verifyEmail.title') }}
        </h1>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          {{ t('auth.verifyEmail.subtitle') }}
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <p class="mt-4 text-gray-600 dark:text-gray-400">
          {{ t('auth.verifyEmail.verifying') }}
        </p>
      </div>

      <!-- Success Message -->
      <div v-else-if="isVerified" class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6">
        <div class="flex items-center">
          <svg class="w-8 h-8 text-green-600 dark:text-green-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <div>
            <p class="text-lg font-medium text-green-600 dark:text-green-400">
              {{ t('auth.verifyEmail.successTitle') }}
            </p>
            <p class="text-sm text-green-600 dark:text-green-400 mt-1">
              {{ t('auth.verifyEmail.successMessage') }}
            </p>
          </div>
        </div>
        <div class="mt-6">
          <NuxtLink
            to="/login"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            {{ t('auth.verifyEmail.goToLogin') }}
          </NuxtLink>
        </div>
      </div>

      <!-- Error Message -->
      <div v-else-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
        <div class="flex items-center">
          <svg class="w-8 h-8 text-red-600 dark:text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <p class="text-lg font-medium text-red-600 dark:text-red-400">
              {{ t('auth.verifyEmail.errorTitle') }}
            </p>
            <p class="text-sm text-red-600 dark:text-red-400 mt-1">
              {{ error }}
            </p>
          </div>
        </div>
        <div class="mt-6 space-y-3">
          <NuxtLink
            to="/login"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            {{ t('auth.verifyEmail.goToLogin') }}
          </NuxtLink>
          <NuxtLink
            to="/register"
            class="w-full flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            {{ t('auth.verifyEmail.registerAgain') }}
          </NuxtLink>
        </div>
      </div>

      <!-- No Token Message -->
      <div v-else class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
        <div class="flex items-center">
          <svg class="w-8 h-8 text-yellow-600 dark:text-yellow-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.998-.833-2.768 0L4.342 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <div>
            <p class="text-lg font-medium text-yellow-600 dark:text-yellow-400">
              {{ t('auth.verifyEmail.noTokenTitle') }}
            </p>
            <p class="text-sm text-yellow-600 dark:text-yellow-400 mt-1">
              {{ t('auth.verifyEmail.noTokenMessage') }}
            </p>
          </div>
        </div>
        <div class="mt-6">
          <NuxtLink
            to="/login"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            {{ t('auth.verifyEmail.goToLogin') }}
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from '#imports'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const isLoading = ref(true)
const isVerified = ref(false)
const error = ref<string | null>(null)

async function verifyEmailToken(token: string) {
  try {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    const response = await fetch(`${backendUrl}/api/auth/verify-email`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Verification failed with status ${response.status}`)
    }

    const data = await response.json()
    console.log('Email verification successful:', data)
    return data
  } catch (err) {
    console.error('Email verification error:', err)
    throw err
  }
}

onMounted(async () => {
  const token = route.query.token as string

  if (!token) {
    isLoading.value = false
    return
  }

  try {
    await verifyEmailToken(token)
    isVerified.value = true
    error.value = null
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unknown error occurred'
    isVerified.value = false
  } finally {
    isLoading.value = false
  }
})
</script>