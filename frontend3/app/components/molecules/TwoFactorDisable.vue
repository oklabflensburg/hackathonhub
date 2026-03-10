<template>
  <div class="two-factor-disable">
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
        Zwei-Faktor-Authentifizierung deaktivieren
      </h3>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Durch das Deaktivieren der Zwei-Faktor-Authentifizierung wird dein Konto weniger sicher. Du musst dein Passwort bestätigen, um fortzufahren.
      </p>
    </div>

    <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
            Sicherheitswarnung
          </h3>
          <div class="mt-2 text-sm text-red-700 dark:text-red-300">
            <p>
              Durch das Deaktivieren der Zwei-Faktor-Authentifizierung verlierst du einen wichtigen Sicherheitsschutz für dein Konto.
            </p>
          </div>
        </div>
      </div>
    </div>

    <form @submit.prevent="disable2FA" class="space-y-4">
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Passwort bestätigen
        </label>
        <input
          v-model="password"
          type="password"
          id="password"
          required
          class="block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-500 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          placeholder="Gib dein Passwort ein"
        />
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
          Du musst dein Passwort eingeben, um die Änderung zu bestätigen.
        </p>
      </div>

      <div class="flex justify-end space-x-3">
        <button
          type="button"
          @click="$emit('cancel')"
          class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
        >
          Abbrechen
        </button>
        <button
          type="submit"
          :disabled="!password || isLoading"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading" class="mr-2">
            <svg class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </span>
          {{ isLoading ? 'Wird deaktiviert...' : '2FA deaktivieren' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUIStore } from '~/stores/ui'
import { useAuthStore } from '~/stores/auth'

interface Emits {
  (e: 'cancel'): void
  (e: 'complete'): void
}

const emit = defineEmits<Emits>()

const uiStore = useUIStore()
const authStore = useAuthStore()
const password = ref('')
const isLoading = ref(false)

const disable2FA = async () => {
  if (!password.value) {
    uiStore.showError('Fehler', 'Bitte gib dein Passwort ein.')
    return
  }

  isLoading.value = true
  try {
    const response = await authStore.fetchWithAuth('/api/settings/security/2fa/disable', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        password: password.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.message || 'Deaktivierung fehlgeschlagen')
    }

    uiStore.showSuccess('Erfolg', 'Zwei-Faktor-Authentifizierung wurde deaktiviert.')
    emit('complete')
  } catch (error) {
    uiStore.showError('Fehler', error instanceof Error ? error.message : 'Deaktivierung fehlgeschlagen.')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.two-factor-disable {
  @apply max-w-md mx-auto;
}
</style>