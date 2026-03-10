<template>
  <div class="two-factor-setup">
    <!-- Step 1: Enable 2FA -->
    <div v-if="step === 1" class="step-1">
      <div class="mb-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
          Zwei-Faktor-Authentifizierung aktivieren
        </h3>
        <p class="text-sm text-gray-600 dark:text-gray-400">
          Die Zwei-Faktor-Authentifizierung erhöht die Sicherheit deines Kontos, indem sie neben deinem Passwort einen zusätzlichen Verifizierungscode erfordert.
        </p>
      </div>

      <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-yellow-800 dark:text-yellow-200">
              Wichtige Informationen
            </h3>
            <div class="mt-2 text-sm text-yellow-700 dark:text-yellow-300">
              <ul class="list-disc pl-5 space-y-1">
                <li>Speichere die Backup-Codes an einem sicheren Ort</li>
                <li>Du benötigst eine Authenticator-App (Google Authenticator, Authy, etc.)</li>
                <li>Ohne Backup-Codes oder Authenticator-App verlierst du den Zugang zu deinem Konto</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div class="flex justify-end">
        <button
          @click="enable2FA"
          :disabled="isLoading"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading" class="mr-2">
            <svg class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </span>
          {{ isLoading ? 'Wird vorbereitet...' : '2FA aktivieren' }}
        </button>
      </div>
    </div>

    <!-- Step 2: Show QR Code and Secret -->
    <div v-if="step === 2" class="step-2">
      <div class="mb-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
          Scanne den QR-Code
        </h3>
        <p class="text-sm text-gray-600 dark:text-gray-400">
          Scanne diesen QR-Code mit deiner Authenticator-App oder gib den Secret manuell ein.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <!-- QR Code -->
        <div class="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">QR-Code</h4>
          <div class="flex justify-center">
            <img :src="setupData.qr_code" alt="QR Code" class="w-48 h-48 border border-gray-300 dark:border-gray-600 rounded" />
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 text-center mt-3">
            Scanne mit Google Authenticator, Authy oder einer ähnlichen App
          </p>
        </div>

        <!-- Manual Setup -->
        <div class="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">Manuelle Einrichtung</h4>
          <div class="space-y-3">
            <div>
              <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                Secret
              </label>
              <div class="flex">
                <input
                  type="text"
                  :value="setupData.secret"
                  readonly
                  class="flex-1 block w-full rounded-l-md border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 px-3 py-2 text-sm text-gray-900 dark:text-gray-100"
                />
                <button
                  @click="copySecret"
                  class="inline-flex items-center px-3 py-2 border border-l-0 border-gray-300 dark:border-gray-600 rounded-r-md bg-gray-50 dark:bg-gray-700 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600"
                >
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </button>
              </div>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Gib diesen Code manuell in deiner Authenticator-App ein
              </p>
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                Verifizierungscode
              </label>
              <input
                v-model="verificationCode"
                type="text"
                placeholder="6-stelliger Code"
                maxlength="6"
                class="block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-500 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                @input="onCodeInput"
              />
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Gib den 6-stelligen Code aus deiner Authenticator-App ein
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Backup Codes -->
      <div class="mb-6">
        <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">Backup-Codes</h4>
        <div class="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
            Speichere diese Codes an einem sicheren Ort. Du kannst sie verwenden, wenn du keinen Zugang zu deiner Authenticator-App hast.
          </p>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-2 mb-4">
            <div
              v-for="(code, index) in setupData.backup_codes"
              :key="index"
              class="bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-center font-mono text-sm"
            >
              {{ code }}
            </div>
          </div>
          <div class="flex space-x-3">
            <button
              @click="downloadBackupCodes"
              class="inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download
            </button>
            <button
              @click="copyBackupCodes"
              class="inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Kopieren
            </button>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex justify-between">
        <button
          @click="step = 1"
          class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
        >
          Zurück
        </button>
        <button
          @click="verify2FA"
          :disabled="!verificationCode || verificationCode.length !== 6 || isLoading"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading" class="mr-2">
            <svg class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </span>
          {{ isLoading ? 'Wird verifiziert...' : 'Verifizieren und aktivieren' }}
        </button>
      </div>
    </div>

    <!-- Step 3: Success -->
    <div v-if="step === 3" class="step-3">
      <div class="text-center">
        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 dark:bg-green-900/30 mb-4">
          <svg class="h-6 w-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
          Zwei-Faktor-Authentifizierung aktiviert!
        </h3>
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
          Dein Konto ist jetzt durch Zwei-Faktor-Authentifizierung geschützt. Vergiss nicht, deine Backup-Codes sicher aufzubewahren.
        </p>
        <button
          @click="$emit('completed')"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          Fertig
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUIStore } from '~/stores/ui'
import { useAuthStore } from '~/stores/auth'

interface TwoFactorSetupData {
  qr_code: string
  secret: string
  backup_codes: string[]
}

interface Props {
  onCompleted?: () => void
}

const props = defineProps<Props>()
const emit = defineEmits<{
  completed: []
}>()

const uiStore = useUIStore()
const authStore = useAuthStore()
const step = ref(1)
const isLoading = ref(false)
const verificationCode = ref('')
const setupData = ref<TwoFactorSetupData>({
  qr_code: '',
  secret: '',
  backup_codes: []
})

const enable2FA = async () => {
  isLoading.value = true
  try {
    const response = await authStore.fetchWithAuth('/api/settings/security/2fa/enable', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: 'Failed to enable 2FA' }))
      throw new Error(errorData.message || '2FA konnte nicht aktiviert werden')
    }

    const data = await response.json()
    setupData.value = data
    step.value = 2
    uiStore.showSuccess('Erfolg', '2FA wurde vorbereitet. Scanne jetzt den QR-Code mit deiner Authenticator-App.')
  } catch (error) {
    uiStore.showError('Fehler', error instanceof Error ? error.message : '2FA konnte nicht aktiviert werden. Bitte versuche es erneut.')
    console.error('Error enabling 2FA:', error)
  } finally {
    isLoading.value = false
  }
}

const verify2FA = async () => {
  if (verificationCode.value.length !== 6) {
    uiStore.showError('Fehler', 'Bitte gib einen 6-stelligen Verifizierungscode ein.')
    return
  }

  // Ensure 2FA setup was completed first
  if (!setupData.value.secret) {
    uiStore.showError('Fehler', 'Bitte aktiviere zuerst 2FA, bevor du den Code verifizierst.')
    return
  }

  isLoading.value = true
  try {
    const response = await authStore.fetchWithAuth('/api/settings/security/2fa/verify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        code: verificationCode.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: 'Verifizierung fehlgeschlagen' }))
      throw new Error(errorData.message || 'Verifizierung fehlgeschlagen')
    }

    const result = await response.json()
    step.value = 3
    uiStore.showSuccess('Erfolg', result.message || 'Zwei-Faktor-Authentifizierung wurde erfolgreich aktiviert.')
    
    // Refresh token to ensure valid session after 2FA activation
    try {
      await authStore.refreshToken()
    } catch (refreshError) {
      console.warn('Token refresh after 2FA activation failed:', refreshError)
      // Non-critical error, user can still continue
    }
    
    // Emit completed event to parent
    emit('completed')
  } catch (error) {
    uiStore.showError('Fehler', error instanceof Error ? error.message : 'Verifizierung fehlgeschlagen.')
  } finally {
    isLoading.value = false
  }
}

const onCodeInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  // Only allow numbers
  verificationCode.value = input.value.replace(/\D/g, '').slice(0, 6)
}

const copySecret = () => {
  navigator.clipboard.writeText(setupData.value.secret)
    .then(() => {
      uiStore.showSuccess('Erfolg', 'Secret wurde in die Zwischenablage kopiert.')
    })
    .catch(() => {
      uiStore.showError('Fehler', 'Secret konnte nicht kopiert werden.')
    })
}

const copyBackupCodes = () => {
  const codes = setupData.value.backup_codes.join('\n')
  navigator.clipboard.writeText(codes)
    .then(() => {
      uiStore.showSuccess('Erfolg', 'Backup-Codes wurden in die Zwischenablage kopiert.')
    })
    .catch(() => {
      uiStore.showError('Fehler', 'Backup-Codes konnten nicht kopiert werden.')
    })
}

const downloadBackupCodes = () => {
  const codes = setupData.value.backup_codes.join('\n')
  const blob = new Blob([`Backup-Codes für Hackathon Hub\n\n${codes}\n\nSpeichere diese Codes an einem sicheren Ort!`], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'hackathon-hub-backup-codes.txt'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  uiStore.showSuccess('Erfolg', 'Backup-Codes wurden heruntergeladen.')
}
</script>

<style scoped>
.two-factor-setup {
  @apply max-w-4xl mx-auto;
}
</style>