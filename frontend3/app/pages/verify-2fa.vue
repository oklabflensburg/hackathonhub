<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="flex justify-center">
        <div class="w-16 h-16 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
          <Icon name="shield" class="w-8 h-8 text-primary-600 dark:text-primary-400" />
        </div>
      </div>
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">
        Zwei-Faktor-Authentifizierung
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
        Gib den 6-stelligen Code von deiner Authenticator-App ein
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white dark:bg-gray-800 py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <!-- Error Message -->
        <div v-if="error" class="mb-6">
          <ErrorMessage
            :message="error"
            type="error"
            dismissible
            @dismiss="error = ''"
          />
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="text-center py-8">
          <LoadingSpinner size="lg" color="primary" class="mx-auto mb-4" />
          <p class="text-gray-700 dark:text-gray-300">Verifiziere Code...</p>
        </div>

        <!-- Verification Form -->
        <div v-else>
          <form @submit.prevent="verifyCode" class="space-y-6">
            <!-- Code Input -->
            <div>
              <label for="code" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                6-stelliger Verifizierungscode
              </label>
              <div class="mt-1">
                <input
                  id="code"
                  v-model="code"
                  type="text"
                  inputmode="numeric"
                  pattern="[0-9]*"
                  maxlength="6"
                  autocomplete="one-time-code"
                  required
                  class="appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white sm:text-sm text-center text-2xl tracking-widest"
                  placeholder="123456"
                  :disabled="isLoading"
                  @input="formatCode"
                />
              </div>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                Öffne deine Authenticator-App (Google Authenticator, Authy, etc.) und gib den aktuellen 6-stelligen Code ein.
              </p>
            </div>

            <!-- Remember Device Option -->
            <div class="flex items-center">
              <input
                id="remember-device"
                v-model="rememberDevice"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600 rounded dark:bg-gray-700"
                :disabled="isLoading"
              />
              <label for="remember-device" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                Dieses Gerät für 30 Tage merken
              </label>
            </div>

            <!-- Action Buttons -->
            <div class="flex flex-col sm:flex-row gap-3">
              <Button
                type="submit"
                variant="primary"
                class="flex-1"
                :loading="isLoading"
                :disabled="!isValidCode || isLoading"
              >
                <Icon name="check" class="mr-2" />
                Verifizieren
              </Button>
              <Button
                type="button"
                variant="outline"
                class="flex-1"
                :disabled="isLoading"
                @click="cancelVerification"
              >
                <Icon name="x" class="mr-2" />
                Abbrechen
              </Button>
            </div>
          </form>

          <!-- Help Section -->
          <div class="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
            <div class="space-y-4">
              <div class="flex items-start gap-3">
                <Icon name="help-circle" class="w-5 h-5 text-gray-400 dark:text-gray-500 mt-0.5 flex-shrink-0" />
                <div>
                  <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100">
                    Probleme mit dem Code?
                  </h3>
                  <ul class="mt-2 text-sm text-gray-600 dark:text-gray-400 space-y-1">
                    <li>• Stelle sicher, dass die Uhrzeit auf deinem Gerät korrekt ist</li>
                    <li>• Der Code aktualisiert sich alle 30 Sekunden</li>
                    <li>• Verwende einen Backup-Code, falls verfügbar</li>
                  </ul>
                </div>
              </div>

              <div class="flex items-start gap-3">
                <Icon name="key" class="w-5 h-5 text-gray-400 dark:text-gray-500 mt-0.5 flex-shrink-0" />
                <div>
                  <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100">
                    Backup-Codes verwenden
                  </h3>
                  <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
                    Falls du keinen Zugriff auf deine Authenticator-App hast, kannst du einen deiner Backup-Codes verwenden.
                  </p>
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    class="mt-2"
                    :disabled="isLoading"
                    @click="useBackupCode"
                  >
                    <Icon name="key" class="mr-2" />
                    Mit Backup-Code fortfahren
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Backup Code Modal -->
    <Modal
      v-model="showBackupCodeModal"
      title="Backup-Code verwenden"
      size="md"
    >
      <div class="p-6">
        <div class="mb-6">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
            Gib einen deiner Backup-Codes ein. Jeder Code kann nur einmal verwendet werden.
          </p>
          <div>
            <label for="backup-code" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Backup-Code
            </label>
            <input
              id="backup-code"
              v-model="backupCode"
              type="text"
              class="appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white sm:text-sm"
              placeholder="xxxx-xxxx-xxxx"
              :disabled="isLoading"
            />
          </div>
        </div>
        <div class="flex justify-end gap-3">
          <Button
            @click="showBackupCodeModal = false"
            variant="outline"
            :disabled="isLoading"
          >
            Abbrechen
          </Button>
          <Button
            @click="verifyBackupCode"
            variant="primary"
            :loading="isLoading"
            :disabled="!backupCode || isLoading"
          >
            Verifizieren
          </Button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from '#imports'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import Icon from '~/components/atoms/Icon.vue'
import Button from '~/components/atoms/Button.vue'
import ErrorMessage from '~/components/atoms/ErrorMessage.vue'
import LoadingSpinner from '~/components/atoms/LoadingSpinner.vue'
import Modal from '~/components/molecules/Modal.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const uiStore = useUIStore()

// State
const code = ref('')
const backupCode = ref('')
const rememberDevice = ref(false)
const isLoading = ref(false)
const error = ref('')
const showBackupCodeModal = ref(false)

// Computed
const isValidCode = computed(() => {
  return /^\d{6}$/.test(code.value)
})

// Format code input (only numbers, max 6 digits)
const formatCode = (event: Event) => {
  const input = event.target as HTMLInputElement
  let value = input.value.replace(/\D/g, '')
  value = value.slice(0, 6)
  code.value = value
  input.value = value
}

// Verify TOTP code
const verifyCode = async () => {
  if (!isValidCode.value) {
    error.value = 'Bitte gib einen gültigen 6-stelligen Code ein.'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    // Get temp token from route query, sessionStorage, or localStorage
    const tempToken = route.query.temp_token as string || 
                     sessionStorage.getItem('2fa_temp_token') || 
                     localStorage.getItem('2fa_temp_token') || ''
    
    if (!tempToken) {
      throw new Error('Sitzung abgelaufen. Bitte melde dich erneut an.')
    }

    // Call auth store to verify 2FA
    const success = await authStore.verifyTwoFactor({
      code: code.value,
      temp_token: tempToken,
      remember_device: rememberDevice.value
    })

    if (success) {
      uiStore.showSuccess('Erfolgreich verifiziert!', 'Du wirst weitergeleitet...')
      
      // Clear temp token from all storage locations
      localStorage.removeItem('2fa_temp_token')
      sessionStorage.removeItem('2fa_temp_token')
      sessionStorage.removeItem('2fa_user_id')
      
      // Redirect to intended destination or home
      const redirectTo = route.query.redirect as string || '/'
      setTimeout(() => {
        router.push(redirectTo)
      }, 1500)
    } else {
      error.value = 'Ungültiger Code. Bitte versuche es erneut.'
    }
  } catch (err: any) {
    error.value = err.message || 'Verifizierung fehlgeschlagen. Bitte versuche es erneut.'
    console.error('2FA verification error:', err)
  } finally {
    isLoading.value = false
  }
}

// Verify backup code
const verifyBackupCode = async () => {
  if (!backupCode.value.trim()) {
    error.value = 'Bitte gib einen Backup-Code ein.'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    const tempToken = route.query.temp_token as string || 
                     sessionStorage.getItem('2fa_temp_token') || 
                     localStorage.getItem('2fa_temp_token') || ''
    
    if (!tempToken) {
      throw new Error('Sitzung abgelaufen. Bitte melde dich erneut an.')
    }

    // Call auth store to verify backup code
    const success = await authStore.verifyTwoFactorBackup({
      backup_code: backupCode.value.trim(),
      temp_token: tempToken
    })

    if (success) {
      uiStore.showSuccess('Backup-Code akzeptiert!', 'Du wirst weitergeleitet...')
      
      // Clear temp token from all storage locations
      localStorage.removeItem('2fa_temp_token')
      sessionStorage.removeItem('2fa_temp_token')
      sessionStorage.removeItem('2fa_user_id')
      
      // Redirect to intended destination or home
      const redirectTo = route.query.redirect as string || '/'
      setTimeout(() => {
        router.push(redirectTo)
      }, 1500)
    } else {
      error.value = 'Ungültiger Backup-Code. Bitte versuche es erneut.'
    }
  } catch (err: any) {
    error.value = err.message || 'Verifizierung fehlgeschlagen. Bitte versuche es erneut.'
    console.error('Backup code verification error:', err)
  } finally {
    isLoading.value = false
    showBackupCodeModal.value = false
  }
}

// Use backup code
const useBackupCode = () => {
  showBackupCodeModal.value = true
  backupCode.value = ''
}

// Cancel verification
const cancelVerification = () => {
  // Clear temp token from all storage locations
  localStorage.removeItem('2fa_temp_token')
  sessionStorage.removeItem('2fa_temp_token')
  sessionStorage.removeItem('2fa_user_id')
  
  // Redirect to login
  router.push('/login')
}

// Check if user should be on this page
onMounted(() => {
  // Check if user is already authenticated (shouldn't be here)
  if (authStore.isAuthenticated) {
    router.push('/')
    return
  }

  // Check if we have a temp token
  const tempToken = route.query.temp_token as string || 
                   sessionStorage.getItem('2fa_temp_token') || 
                   localStorage.getItem('2fa_temp_token')
  if (!tempToken) {
    error.value = 'Keine gültige Sitzung gefunden. Bitte melde dich erneut an.'
    
    // Redirect to login after a delay
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } else {
    // Store temp token in localStorage for persistence (if it came from sessionStorage)
    if (sessionStorage.getItem('2fa_temp_token')) {
      localStorage.setItem('2fa_temp_token', tempToken)
    }
  }
})
</script>

<style scoped>
/* Custom styles for 2FA page */
input[type="text"] {
  letter-spacing: 0.5em;
}

input::placeholder {
  letter-spacing: normal;
  opacity: 0.5;
}
</style>