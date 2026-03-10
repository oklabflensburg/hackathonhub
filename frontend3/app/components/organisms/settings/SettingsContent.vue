<template>
  <div class="settings-content">
    <!-- Tab Content Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
        {{ activeTabTitle }}
      </h1>
      <p class="text-gray-600 dark:text-gray-400">
        {{ activeTabDescription }}
      </p>
    </div>

    <!-- General Error Display -->
    <ErrorMessage
      v-if="generalError"
      :message="generalError"
      type="error"
      dismissible
      @dismiss="generalError = ''"
      class="mb-6"
    />

    <!-- Centralized Loading State -->
    <div v-if="isLoading" class="mb-6">
      <div class="flex flex-col items-center justify-center p-8 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
        <LoadingSpinner size="lg" color="primary" class="mb-4" />
        <p class="text-gray-700 dark:text-gray-300 font-medium">{{ loadingMessage }}</p>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">
          Bitte warte einen Moment, während deine Änderungen verarbeitet werden.
        </p>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="space-y-8" :class="{ 'opacity-50 pointer-events-none': isLoading }">
      <!-- Profile Tab -->
      <div v-if="activeTab === 'profile'" class="space-y-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Persönliche Informationen
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <SettingsInput
              label="Benutzername"
              v-model="profileUsername"
              placeholder="maxmustermann"
              :error="errors?.profile?.username"
            />
            <SettingsInput
              label="Name"
              v-model="profileName"
              placeholder="Max Mustermann"
              :error="errors?.profile?.name"
            />
            <SettingsInput
              label="E-Mail"
              v-model="profileEmail"
              type="email"
              placeholder="max@example.com"
              :error="errors?.profile?.email"
            />
            <SettingsInput
              label="Standort"
              v-model="profileLocation"
              placeholder="Berlin, Deutschland"
              :error="errors?.profile?.location"
            />
          </div>
        </div>
      </div>

       <!-- Security Tab -->
       <div v-else-if="activeTab === 'security'" class="space-y-6">
         <!-- Two-Factor Authentication Section -->
         <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
           <TwoFactorStatus
             :enabled="security.two_factor_enabled"
             :last-enabled="security.two_factor_last_enabled"
             :last-used="security.two_factor_last_used"
             :trusted-devices-count="security.trusted_devices_count"
             :remaining-backup-codes="security.remaining_backup_codes"
           />
           
           <!-- Action Buttons -->
           <div class="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
             <div v-if="!security.two_factor_enabled" class="flex flex-col sm:flex-row gap-3">
               <Button
                 @click="showTwoFactorSetup = true"
                 variant="primary"
                 class="flex-1"
               >
                 <Icon name="shield-plus" class="mr-2" />
                 2FA aktivieren
               </Button>
               <Button
                 @click="showTwoFactorInfo = true"
                 variant="outline"
                 class="flex-1"
               >
                 <Icon name="info" class="mr-2" />
                 Mehr erfahren
               </Button>
             </div>
             
             <div v-else class="flex flex-col sm:flex-row gap-3">
               <Button
                 @click="showBackupCodesModal = true"
                 variant="outline"
                 class="flex-1"
               >
                 <Icon name="key" class="mr-2" />
                 Backup-Codes anzeigen
               </Button>
               <Button
                 @click="showTwoFactorDisable = true"
                 variant="danger"
                 class="flex-1"
               >
                 <Icon name="shield-off" class="mr-2" />
                 2FA deaktivieren
               </Button>
               <Button
                 @click="showTwoFactorSetup = true"
                 variant="outline"
                 class="flex-1"
               >
                 <Icon name="refresh-cw" class="mr-2" />
                 Neu einrichten
               </Button>
             </div>
           </div>
         </div>

         <!-- Active Sessions Section -->
         <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
           <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
             Aktive Sitzungen
           </h3>
           <div v-if="security.active_sessions && security.active_sessions.length > 0" class="space-y-4">
             <div
               v-for="session in security.active_sessions"
               :key="session.id"
               class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
             >
               <div class="flex items-center gap-3">
                 <div class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
                   <Icon
                     :name="session.device_type === 'mobile' ? 'smartphone' : 'monitor'"
                     class="text-primary-600 dark:text-primary-400"
                   />
                 </div>
                 <div>
                   <p class="font-medium text-gray-900 dark:text-gray-100">
                     {{ session.device_name || 'Unbekanntes Gerät' }}
                   </p>
                   <p class="text-sm text-gray-600 dark:text-gray-400">
                     {{ session.location || 'Unbekannter Standort' }} • {{ formatDate(session.last_activity) }}
                   </p>
                 </div>
               </div>
               <div class="flex items-center gap-2">
                 <Badge
                   v-if="session.is_current"
                   variant="success"
                   size="sm"
                 >
                   Aktuell
                 </Badge>
                 <Button
                   v-if="!session.is_current"
                   @click="terminateSession(session.id)"
                   variant="ghost"
                   size="sm"
                   class="text-red-600 hover:text-red-700 hover:bg-red-50 dark:text-red-400 dark:hover:text-red-300 dark:hover:bg-red-900/20"
                 >
                   Beenden
                 </Button>
               </div>
             </div>
           </div>
           <div v-else class="text-center py-8">
             <Icon name="shield" class="w-12 h-12 text-gray-400 dark:text-gray-600 mx-auto mb-3" />
             <p class="text-gray-600 dark:text-gray-400">
               Keine aktiven Sitzungen gefunden
             </p>
           </div>
         </div>
       </div>

      <!-- Notifications Tab -->
      <div v-else-if="activeTab === 'notifications'" class="space-y-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Benachrichtigungsarten
          </h3>
          <div class="space-y-4">
            <SettingsToggle
              label="E-Mail-Benachrichtigungen"
               description="Erhalte wichtige Updates per E-Mail."
              v-model="notificationsEmail"
            />
            <SettingsToggle
              label="Push-Benachrichtigungen"
               description="Erhalte Push-Benachrichtigungen in deinem Browser."
              v-model="notificationsPush"
            />
          </div>
        </div>
      </div>

      <!-- Privacy Tab -->
      <div v-else-if="activeTab === 'privacy'" class="space-y-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Profil-Sichtbarkeit
          </h3>
          <div class="space-y-4">
             <SettingsRadioGroup
              label="Wer kann dein Profil sehen?"
              :options="[
                { value: 'public', label: 'Öffentlich', description: 'Jeder kann dein Profil sehen' },
                { value: 'friends_only', label: 'Nur Freunde', description: 'Nur deine Freunde und Teams' },
                { value: 'private', label: 'Privat', description: 'Nur du selbst' }
              ]"
              v-model="privacyProfileVisibility"
            />
          </div>
        </div>
      </div>

      <!-- Platform Tab -->
      <div v-else-if="activeTab === 'platform'" class="space-y-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Erscheinungsbild
          </h3>
          <div class="space-y-4">
            <SettingsSelect
              label="Theme"
              :options="[
                { value: 'system', label: 'System' },
                { value: 'light', label: 'Hell' },
                { value: 'dark', label: 'Dunkel' }
              ]"
              v-model="platformTheme"
            />
          </div>
        </div>
       </div>
     </div>

      <!-- 2FA Setup Modal -->
      <Modal
        v-model="showTwoFactorSetup"
        title="Zwei-Faktor-Authentifizierung einrichten"
        size="lg"
      >
        <TwoFactorSetup @complete="handle2FASetupComplete" />
      </Modal>

      <!-- 2FA Disable Modal -->
      <Modal
        v-model="showTwoFactorDisable"
        title="Zwei-Faktor-Authentifizierung deaktivieren"
        size="md"
      >
        <TwoFactorDisable @complete="handle2FADisableComplete" />
      </Modal>

      <!-- Backup Codes Modal -->
      <Modal
        v-model="showBackupCodesModal"
        title="Backup-Codes"
        size="md"
      >
       <div class="p-6">
         <div class="mb-6">
           <Icon name="key" class="w-12 h-12 text-primary-600 dark:text-primary-400 mx-auto mb-4" />
           <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 text-center mb-2">
             Deine Backup-Codes
           </h3>
           <p class="text-sm text-gray-600 dark:text-gray-400 text-center mb-4">
             Speichere diese Codes an einem sicheren Ort. Du kannst sie verwenden, falls du keinen Zugriff auf deine Authenticator-App hast.
           </p>
         </div>
         <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 mb-6">
           <p class="text-sm text-gray-700 dark:text-gray-300 mb-2">
             <Icon name="alert-triangle" class="inline-block mr-2 text-amber-600 dark:text-amber-400" />
             Jeder Code kann nur einmal verwendet werden.
           </p>
           <p class="text-sm text-gray-700 dark:text-gray-300">
             <Icon name="download" class="inline-block mr-2 text-primary-600 dark:text-primary-400" />
             Lade die Codes herunter oder kopiere sie in einen Passwort-Manager.
           </p>
         </div>
         <div class="flex justify-center gap-3">
           <Button @click="emit('show-backup-codes')" variant="primary">
             Backup-Codes anzeigen
           </Button>
           <Button @click="showBackupCodesModal = false" variant="outline">
             Schließen
           </Button>
         </div>
       </div>
     </Modal>

      <!-- 2FA Info Modal -->
      <Modal
        v-model="showTwoFactorInfo"
        title="Was ist Zwei-Faktor-Authentifizierung?"
        size="lg"
      >
       <div class="p-6">
         <div class="space-y-4">
           <div class="flex items-start gap-3">
             <div class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
               <Icon name="shield" class="text-primary-600 dark:text-primary-400" />
             </div>
             <div>
               <h4 class="font-medium text-gray-900 dark:text-gray-100 mb-1">
                 Erhöhte Sicherheit
               </h4>
               <p class="text-sm text-gray-600 dark:text-gray-400">
                 2FA fügt eine zusätzliche Sicherheitsebene zu deinem Konto hinzu. Selbst wenn jemand dein Passwort kennt, kann er sich nicht ohne den zweiten Faktor anmelden.
               </p>
             </div>
           </div>
           
           <div class="flex items-start gap-3">
             <div class="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0">
               <Icon name="smartphone" class="text-blue-600 dark:text-blue-400" />
             </div>
             <div>
               <h4 class="font-medium text-gray-900 dark:text-gray-100 mb-1">
                 So funktioniert es
               </h4>
               <p class="text-sm text-gray-600 dark:text-gray-400">
                 1. Scanne den QR-Code mit einer Authenticator-App (Google Authenticator, Authy, Microsoft Authenticator)<br>
                 2. Gib den 6-stelligen Code bei der Anmeldung ein<br>
                 3. Dein Konto ist jetzt geschützt
               </p>
             </div>
           </div>
           
           <div class="flex items-start gap-3">
             <div class="w-10 h-10 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center flex-shrink-0">
               <Icon name="key" class="text-green-600 dark:text-green-400" />
             </div>
             <div>
               <h4 class="font-medium text-gray-900 dark:text-gray-100 mb-1">
                 Backup-Codes
               </h4>
               <p class="text-sm text-gray-600 dark:text-gray-400">
                 Du erhältst 10 Backup-Codes, die du an einem sicheren Ort aufbewahren solltest. Verwende sie, falls du dein Gerät verlierst oder keinen Zugriff auf deine Authenticator-App hast.
               </p>
             </div>
           </div>
         </div>
         
         <div class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
           <div class="flex justify-end gap-3">
             <Button @click="showTwoFactorInfo = false" variant="outline">
               Schließen
             </Button>
             <Button @click="showTwoFactorSetup = true; showTwoFactorInfo = false" variant="primary">
               Jetzt einrichten
             </Button>
           </div>
         </div>
       </div>
     </Modal>
   </div>
 </template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type {
  ProfileSettings,
  SecuritySettings,
  NotificationSettings,
  PrivacySettings,
  PlatformPreferences
} from '~/types/settings-types'
import SettingsInput from '~/components/molecules/SettingsInput.vue'
import SettingsToggle from '~/components/molecules/SettingsToggle.vue'
import SettingsSelect from '~/components/molecules/SettingsSelect.vue'
import SettingsRadioGroup from '~/components/molecules/SettingsRadioGroup.vue'
import ErrorMessage from '~/components/atoms/ErrorMessage.vue'
import LoadingSpinner from '~/components/atoms/LoadingSpinner.vue'
import TwoFactorStatus from '~/components/molecules/TwoFactorStatus.vue'
import TwoFactorSetup from '~/components/molecules/TwoFactorSetup.vue'
import TwoFactorDisable from '~/components/molecules/TwoFactorDisable.vue'
import Button from '~/components/atoms/Button.vue'
import Badge from '~/components/atoms/Badge.vue'
import Icon from '~/components/atoms/Icon.vue'
import Modal from '~/components/molecules/Modal.vue'

interface Props {
  activeTab: string
  profile: ProfileSettings
  security: SecuritySettings
  notifications: NotificationSettings
  privacy: PrivacySettings
  platform: PlatformPreferences
  isLoading?: boolean
  loadingOperations?: {
    profile?: boolean
    security?: boolean
    notifications?: boolean
    privacy?: boolean
    platform?: boolean
  }
  errors?: {
    profile?: Partial<Record<keyof ProfileSettings, string>>
    security?: Partial<Record<keyof SecuritySettings, string>>
    notifications?: Partial<Record<keyof NotificationSettings, string>>
    privacy?: Partial<Record<keyof PrivacySettings, string>>
    platform?: Partial<Record<keyof PlatformPreferences, string>>
  }
}

const props = defineProps<Props>()
const generalError = ref<string>('')

// 2FA Modal States
const showTwoFactorSetup = ref(false)
const showTwoFactorDisable = ref(false)
const showBackupCodesModal = ref(false)
const showTwoFactorInfo = ref(false)

// Create computed properties with getter/setter for each profile field
const profileUsername = computed({
  get: () => props.profile.username || '',
  set: (value) => {
    emit('update:profile', { ...props.profile, username: value })
  }
})

const profileName = computed({
  get: () => props.profile.name || '',
  set: (value) => {
    emit('update:profile', { ...props.profile, name: value })
  }
})

const profileEmail = computed({
  get: () => props.profile.email || '',
  set: (value) => {
    emit('update:profile', { ...props.profile, email: value })
  }
})

const profileLocation = computed({
  get: () => props.profile.location || '',
  set: (value) => {
    emit('update:profile', { ...props.profile, location: value })
  }
})

const profileBio = computed({
  get: () => props.profile.bio || '',
  set: (value) => {
    emit('update:profile', { ...props.profile, bio: value })
  }
})

const profileCompany = computed({
  get: () => props.profile.company || '',
  set: (value) => {
    emit('update:profile', { ...props.profile, company: value })
  }
})

const profileAvatarUrl = computed({
  get: () => props.profile.avatar_url || '',
  set: (value) => {
    emit('update:profile', { ...props.profile, avatar_url: value })
  }
})

// Create computed properties for other sections
const securityTwoFactor = computed({
  get: () => props.security.two_factor_enabled,
  set: (value) => {
    emit('update:security', { ...props.security, two_factor_enabled: value })
  }
})

const notificationsEmail = computed({
  get: () => props.notifications.email_enabled,
  set: (value) => {
    emit('update:notifications', { ...props.notifications, email_enabled: value })
  }
})

const notificationsPush = computed({
  get: () => props.notifications.push_enabled,
  set: (value) => {
    emit('update:notifications', { ...props.notifications, push_enabled: value })
  }
})

const privacyProfileVisibility = computed({
  get: () => props.privacy.profile_visibility,
  set: (value) => {
    emit('update:privacy', { ...props.privacy, profile_visibility: value })
  }
})

const platformTheme = computed({
  get: () => props.platform.theme,
  set: (value) => {
    emit('update:platform', { ...props.platform, theme: value })
  }
})

const emit = defineEmits<{
  'update:profile': [value: ProfileSettings]
  'update:security': [value: SecuritySettings]
  'update:notifications': [value: NotificationSettings]
  'update:privacy': [value: PrivacySettings]
  'update:platform': [value: PlatformPreferences]
  'toggle-two-factor': [enabled: boolean]
  'upload-avatar': []
  'remove-avatar': []
  'show-backup-codes': []
  'terminate-session': [sessionId: string]
}>()

const tabTitles: Record<string, string> = {
  profile: 'Profil',
  security: 'Sicherheit',
  notifications: 'Benachrichtigungen',
  privacy: 'Datenschutz',
  platform: 'Plattform'
}

const tabDescriptions: Record<string, string> = {
  profile: 'Verwalte deine persönlichen Informationen und Kontaktdaten',
  security: 'Passwort, Zwei-Faktor-Authentifizierung und Kontosicherheit',
  notifications: 'Einstellungen für E-Mail, Push und In-App-Benachrichtigungen',
  privacy: 'Privatsphäre-Einstellungen und Datenfreigabe',
  platform: 'Theme, Sprache und erweiterte Plattform-Einstellungen'
}

const activeTabTitle = computed(() => tabTitles[props.activeTab] || 'Einstellungen')
const activeTabDescription = computed(() => tabDescriptions[props.activeTab] || 'Verwalte deine Kontoeinstellungen')

// Centralized loading state management
const isLoading = computed(() => {
  // Use global isLoading prop if provided
  if (props.isLoading !== undefined) {
    return props.isLoading
  }
  
  // Otherwise check if any specific operation is loading
  if (props.loadingOperations) {
    return Object.values(props.loadingOperations).some(Boolean)
  }
  
  return false
})

// Loading message based on active tab
const loadingMessage = computed(() => {
  if (!isLoading.value) return ''
  
  const messages: Record<string, string> = {
    profile: 'Profilinformationen werden gespeichert...',
    security: 'Sicherheitseinstellungen werden aktualisiert...',
    notifications: 'Benachrichtigungseinstellungen werden gespeichert...',
    privacy: 'Datenschutzeinstellungen werden aktualisiert...',
    platform: 'Plattformeinstellungen werden gespeichert...'
  }
  
  return messages[props.activeTab] || 'Einstellungen werden gespeichert...'
})

const toggleTwoFactor = (enabled: boolean) => {
  emit('toggle-two-factor', enabled)
}

// 2FA Operation Handlers
const handle2FASetupComplete = () => {
  showTwoFactorSetup.value = false
  // Emit event to parent to refresh security settings
  emit('toggle-two-factor', true)
}

const handle2FADisableComplete = () => {
  showTwoFactorDisable.value = false
  // Emit event to parent to refresh security settings
  emit('toggle-two-factor', false)
}

const uploadAvatar = () => {
  emit('upload-avatar')
}

const removeAvatar = () => {
  emit('remove-avatar')
}

const showBackupCodes = () => {
  emit('show-backup-codes')
}

const terminateSession = (sessionId: string) => {
  emit('terminate-session', sessionId)
}

const formatDate = (dateString: string) => {
  try {
    return new Date(dateString).toLocaleDateString('de-DE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateString
  }
}
</script>

<style scoped>
.settings-content {
  @apply flex-1;
}
</style>