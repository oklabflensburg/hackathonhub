<template>
  <div class="two-factor-status">
    <!-- Status Header -->
    <div class="status-header flex items-center justify-between mb-4">
      <div class="flex items-center gap-3">
        <div class="status-icon">
          <div
            class="w-10 h-10 rounded-full flex items-center justify-center"
            :class="statusIconClasses"
          >
            <Icon
              :name="enabled ? 'shield-check' : 'shield'"
              size="20"
              :class="statusIconColor"
            />
          </div>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            Zwei-Faktor-Authentifizierung
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            {{ statusDescription }}
          </p>
        </div>
      </div>
      <div>
        <span
          class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
          :class="statusBadgeClasses"
        >
          {{ statusText }}
        </span>
      </div>
    </div>

    <!-- Status Details -->
    <div v-if="enabled" class="status-details space-y-3">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Last Enabled -->
        <div class="detail-item">
          <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">
            Aktiviert am
          </p>
          <p class="font-medium text-gray-900 dark:text-white">
            {{ formatDate(lastEnabled) }}
          </p>
        </div>

        <!-- Trusted Devices -->
        <div class="detail-item">
          <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">
            Vertrauenswürdige Geräte
          </p>
          <p class="font-medium text-gray-900 dark:text-white">
            {{ trustedDevicesCount || 'Keine' }}
          </p>
        </div>

        <!-- Last Used -->
        <div v-if="lastUsed" class="detail-item">
          <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">
            Zuletzt verwendet
          </p>
          <p class="font-medium text-gray-900 dark:text-white">
            {{ formatDate(lastUsed) }}
          </p>
        </div>

        <!-- Backup Codes -->
        <div class="detail-item">
          <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">
            Verbleibende Backup-Codes
          </p>
          <p class="font-medium text-gray-900 dark:text-white">
            {{ remainingBackupCodes || 'Unbekannt' }}
          </p>
        </div>
      </div>

      <!-- Security Tips -->
      <div class="security-tips mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
        <div class="flex items-start gap-3">
          <Icon name="info" size="18" class="text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
          <div>
            <p class="text-sm font-medium text-blue-800 dark:text-blue-300 mb-1">
              Sicherheitstipps für 2FA
            </p>
            <ul class="text-sm text-blue-700 dark:text-blue-400 space-y-1">
              <li class="flex items-start gap-2">
                <Icon name="check" size="14" class="mt-0.5 flex-shrink-0" />
                <span>Speichere deine Backup-Codes an einem sicheren Ort</span>
              </li>
              <li class="flex items-start gap-2">
                <Icon name="check" size="14" class="mt-0.5 flex-shrink-0" />
                <span>Verwende eine vertrauenswürdige Authenticator-App</span>
              </li>
              <li class="flex items-start gap-2">
                <Icon name="check" size="14" class="mt-0.5 flex-shrink-0" />
                <span>Melde verdächtige Aktivitäten sofort</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Setup Instructions (when disabled) -->
    <div v-else class="setup-instructions mt-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
      <div class="flex items-start gap-3">
        <Icon name="lock" size="18" class="text-gray-600 dark:text-gray-400 mt-0.5 flex-shrink-0" />
        <div>
          <p class="text-sm font-medium text-gray-800 dark:text-gray-300 mb-1">
            Erhöhe deine Kontosicherheit
          </p>
          <p class="text-sm text-gray-700 dark:text-gray-400">
            Aktiviere die Zwei-Faktor-Authentifizierung, um dein Konto vor unbefugtem Zugriff zu schützen. 
            Du benötigst eine Authenticator-App wie Google Authenticator oder Authy.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { format } from 'date-fns'
import { de } from 'date-fns/locale'
import { Icon } from '~/components/atoms'

interface Props {
  enabled: boolean
  lastEnabled?: string
  lastUsed?: string
  trustedDevicesCount?: number
  remainingBackupCodes?: number
}

const props = withDefaults(defineProps<Props>(), {
  enabled: false,
  lastEnabled: undefined,
  lastUsed: undefined,
  trustedDevicesCount: undefined,
  remainingBackupCodes: undefined
})

// Computed properties
const statusText = computed(() => {
  return props.enabled ? 'Aktiviert' : 'Deaktiviert'
})

const statusDescription = computed(() => {
  return props.enabled
    ? 'Dein Konto ist durch Zwei-Faktor-Authentifizierung geschützt.'
    : 'Dein Konto ist nicht durch Zwei-Faktor-Authentifizierung geschützt.'
})

const statusBadgeClasses = computed(() => {
  return props.enabled
    ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
    : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
})

const statusIconClasses = computed(() => {
  return props.enabled
    ? 'bg-green-100 dark:bg-green-900/30'
    : 'bg-gray-100 dark:bg-gray-800'
})

const statusIconColor = computed(() => {
  return props.enabled
    ? 'text-green-600 dark:text-green-400'
    : 'text-gray-600 dark:text-gray-400'
})

// Format date helper
const formatDate = (dateString?: string) => {
  if (!dateString) return 'Nicht verfügbar'
  
  try {
    const date = new Date(dateString)
    return format(date, 'dd.MM.yyyy HH:mm', { locale: de })
  } catch {
    return 'Ungültiges Datum'
  }
}
</script>

<style scoped>
.two-factor-status {
  @apply bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-6;
}

.status-header {
  @apply pb-4 border-b border-gray-200 dark:border-gray-700;
}

.detail-item {
  @apply p-3 bg-gray-50 dark:bg-gray-800 rounded-lg;
}

.security-tips {
  @apply border border-blue-200 dark:border-blue-800;
}

.setup-instructions {
  @apply border border-gray-200 dark:border-gray-700;
}
</style>