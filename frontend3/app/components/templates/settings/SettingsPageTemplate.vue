<template>
  <div class="settings-page-template">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
        Einstellungen
      </h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        Verwalte deine Kontoeinstellungen, Benachrichtigungen, Datenschutz und Plattformpräferenzen.
      </p>
    </div>

    <!-- Main Content Area -->
    <div class="flex flex-col xl:flex-row gap-6 xl:gap-8">
      <!-- Left Sidebar: Navigation -->
      <div class="xl:w-72 flex-shrink-0">
        <SettingsNavigation
          :active-tab="activeTab"
          :has-unsaved-changes="hasUnsavedChanges"
          :last-updated="lastSavedAt"
          @tab-change="handleTabChange"
        />
      </div>

      <!-- Right Content Area -->
      <div class="flex-1">
        <!-- Settings Content -->
        <SettingsContent
          :active-tab="activeTab"
          :profile="profile"
          :security="security"
          :notifications="notifications"
          :privacy="privacy"
          :platform="platform"
          :is-loading="isSaving"
          :errors="errors"
          @update:profile="handleProfileUpdate"
          @update:security="handleSecurityUpdate"
          @update:notifications="handleNotificationsUpdate"
          @update:privacy="handlePrivacyUpdate"
          @update:platform="handlePlatformUpdate"
          @toggle-two-factor="handleToggleTwoFactor"
          @upload-avatar="handleUploadAvatar"
          @remove-avatar="handleRemoveAvatar"
          @show-backup-codes="handleShowBackupCodes"
          @terminate-session="handleTerminateSession"
          @revoke-trusted-device="handleRevokeTrustedDevice"
          @open-deactivate-account="openAccountModal('deactivate')"
          @open-delete-account="openAccountModal('delete')"
        />

        <!-- Actions Bar -->
        <SettingsActions
          :has-unsaved-changes="hasUnsavedChanges"
          :is-saving="isSaving"
          :auto-save-enabled="autoSaveEnabled"
          :last-saved-at="lastSavedAt"
          :error="error"
          :success-message="successMessage"
          @save="handleSave"
          @reset="handleReset"
          @toggle-auto-save="handleToggleAutoSave"
          @export="handleExport"
        />
      </div>
    </div>

    <AccountClosureModal
      v-model="accountModalOpen"
      :mode="accountModalMode"
      :auth-method="authStore.user?.auth_method"
      :impact="accountImpact"
      :loading="accountActionLoading"
      :error="accountActionError"
      @close="closeAccountModal"
      @submit="submitAccountClosure"
    />

    <!-- Loading Overlay -->
    <div
      v-if="isLoading"
      class="fixed inset-0 bg-black/50 dark:bg-black/70 flex items-center justify-center z-50"
    >
      <div class="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-2xl">
        <div class="flex flex-col items-center gap-4">
          <LoadingSpinner size="xl" color="primary" />
          <p class="text-gray-700 dark:text-gray-300 font-medium">
            Lade Einstellungen...
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useThemeStore } from '~/stores/theme'
import SettingsNavigation from '~/components/organisms/settings/SettingsNavigation.vue'
import SettingsContent from '~/components/organisms/settings/SettingsContent.vue'
import SettingsActions from '~/components/organisms/settings/SettingsActions.vue'
import AccountClosureModal from '~/components/organisms/settings/AccountClosureModal.vue'
import LoadingSpinner from '~/components/atoms/LoadingSpinner.vue'
import type {
  ProfileSettings,
  SecuritySettings,
  NotificationSettings,
  PrivacySettings,
  PlatformPreferences,
  UserSettings,
  SettingsResponse,
  AccountImpactResponse
} from '~/types/settings-types'

// Auth store
const authStore = useAuthStore()
const themeStore = useThemeStore()

// Reactive state
const activeTab = ref('profile')
const isLoading = ref(false)
const isSaving = ref(false)
const autoSaveEnabled = ref(true)
const hasUnsavedChanges = ref(false)
const lastSavedAt = ref<string>()
const error = ref<string>()
const successMessage = ref<string>()
const accountModalOpen = ref(false)
const accountModalMode = ref<'delete' | 'deactivate'>('deactivate')
const accountImpact = ref<AccountImpactResponse | null>(null)
const accountActionLoading = ref(false)
const accountActionError = ref<string>()

// Original settings for reset functionality
const originalSettings = ref<UserSettings | null>(null)

// Settings data
const profile = ref<ProfileSettings>({
  username: '',
  email: '',
  name: '',
  avatar_url: '',
  bio: '',
  location: '',
  company: ''
})

const security = ref<SecuritySettings>({
  two_factor_enabled: false,
  active_sessions: [],
  trusted_devices: []
})

const notifications = ref<NotificationSettings>({
  email_enabled: true,
  push_enabled: true,
  in_app_enabled: true,
  categories: {
    project_updates: true,
    team_invitations: true,
    hackathon_announcements: true,
    comment_replies: true,
    vote_notifications: true,
    mention_notifications: true,
    system_announcements: false,
    newsletter: false
  },
  quiet_hours: {
    enabled: false,
    start: '22:00',
    end: '08:00'
  }
})

const privacy = ref<PrivacySettings>({
  profile_visibility: 'public',
  email_visibility: 'friends_only',
  show_online_status: true,
  allow_messages_from: 'friends_only',
  show_activity: true,
  allow_tagging: true,
  data_sharing: {
    analytics: true,
    marketing: false,
    third_parties: false
  }
})

const platform = ref<PlatformPreferences>({
  theme: 'system',
  language: 'de',
  timezone: 'Europe/Berlin',
  date_format: 'DD/MM/YYYY',
  time_format: '24h',
  notifications_sound: true,
  reduce_animations: false,
  compact_mode: false,
  default_view: {
    hackathons: 'grid',
    projects: 'grid',
    notifications: 'grouped'
  }
})

const errors = ref<Record<string, any>>({})

const syncPlatformTheme = (theme: PlatformPreferences['theme']) => {
  themeStore.setTheme(theme)
  if (authStore.user) {
    authStore.user.theme = theme
  }
}

const normalizeSecuritySettings = (value: Partial<SecuritySettings> | undefined): SecuritySettings => ({
  two_factor_enabled: Boolean(value?.two_factor_enabled),
  two_factor_last_enabled: value?.two_factor_last_enabled,
  two_factor_last_used: value?.two_factor_last_used,
  trusted_devices_count: value?.trusted_devices_count ?? value?.trusted_devices?.length ?? 0,
  remaining_backup_codes: value?.remaining_backup_codes ?? 0,
  active_sessions: (value?.active_sessions ?? []).map(session => ({
    ...session,
    device_name: session.device_name ?? session.device ?? 'Unbekanntes Gerät',
    last_activity: session.last_activity ?? session.last_active,
    is_current: session.is_current ?? session.current
  })),
  trusted_devices: (value?.trusted_devices ?? []).map(device => ({
    ...device,
    device_name: device.device_name ?? device.device ?? 'Unbekanntes Gerät',
    last_activity: device.last_activity ?? device.last_active,
    is_current: device.is_current ?? device.current
  }))
})

// Helper function to load settings from API
const fetchSettings = async () => {
  isLoading.value = true
  error.value = undefined
  
  try {
    const response = await authStore.fetchWithAuth('/api/settings/')
    
    if (!response.ok) {
      throw new Error(`Failed to load settings: ${response.status} ${response.statusText}`)
    }
    
    const data: SettingsResponse = await response.json()
    
    // Update all settings from API response
    if (data.settings) {
      profile.value = data.settings.profile
      security.value = normalizeSecuritySettings(data.settings.security)
      notifications.value = data.settings.notifications
      privacy.value = data.settings.privacy
      platform.value = data.settings.platform
      syncPlatformTheme(data.settings.platform.theme)
      
      // Store original settings for reset functionality
      originalSettings.value = data.settings
    }
    
    lastSavedAt.value = data.last_updated
    hasUnsavedChanges.value = false
    successMessage.value = 'Einstellungen erfolgreich geladen'
    
    setTimeout(() => {
      successMessage.value = undefined
    }, 3000)
    
  } catch (err) {
    console.error('Error loading settings:', err)
    error.value = 'Fehler beim Laden der Einstellungen. Bitte versuche es später erneut.'
    
    // Fallback to mock data for development
    if (process.env.NODE_ENV === 'development') {
      console.warn('Using mock data as fallback')
      profile.value = {
        username: 'maxmustermann',
        email: 'max@example.com',
        name: 'Max Mustermann',
        avatar_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Max',
        bio: 'Full-Stack Entwickler mit Fokus auf Vue.js und Python',
        location: 'Berlin, Deutschland',
        company: 'Tech Innovations GmbH'
      }
      security.value.two_factor_enabled = false
    }
  } finally {
    isLoading.value = false
  }
}

// Computed properties
const activeTabTitle = computed(() => {
  const titles: Record<string, string> = {
    profile: 'Profil',
    security: 'Sicherheit',
    notifications: 'Benachrichtigungen',
    privacy: 'Datenschutz',
    platform: 'Plattform'
  }
  return titles[activeTab.value] || 'Einstellungen'
})

// Event handlers
const handleTabChange = (tab: string) => {
  activeTab.value = tab
}

const handleProfileUpdate = (updatedProfile: ProfileSettings) => {
  profile.value = updatedProfile
  hasUnsavedChanges.value = true
}

const handleSecurityUpdate = (updatedSecurity: SecuritySettings) => {
  security.value = updatedSecurity
  hasUnsavedChanges.value = true
}

const handleNotificationsUpdate = (updatedNotifications: NotificationSettings) => {
  notifications.value = updatedNotifications
  hasUnsavedChanges.value = true
}

const handlePrivacyUpdate = (updatedPrivacy: PrivacySettings) => {
  privacy.value = updatedPrivacy
  hasUnsavedChanges.value = true
}

const savePlatformSettings = async (nextPlatform: PlatformPreferences) => {
  isSaving.value = true
  error.value = undefined

  try {
    const response = await authStore.fetchWithAuth('/api/settings/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        platform: nextPlatform
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`Failed to save platform settings: ${response.status} ${response.statusText} - ${JSON.stringify(errorData)}`)
    }

    const data: SettingsResponse = await response.json()
    if (data.settings) {
      platform.value = data.settings.platform
      syncPlatformTheme(data.settings.platform.theme)
      originalSettings.value = originalSettings.value
        ? { ...originalSettings.value, platform: data.settings.platform }
        : data.settings
    }

    lastSavedAt.value = data.last_updated
    hasUnsavedChanges.value = false
  } catch (err) {
    console.error('Error saving platform settings:', err)
    error.value = 'Fehler beim Speichern der Plattformeinstellungen.'
    if (originalSettings.value) {
      platform.value = originalSettings.value.platform
      syncPlatformTheme(originalSettings.value.platform.theme)
    }
  } finally {
    isSaving.value = false
  }
}

const handlePlatformUpdate = (updatedPlatform: PlatformPreferences) => {
  platform.value = updatedPlatform
  syncPlatformTheme(updatedPlatform.theme)
  hasUnsavedChanges.value = true

  // Platform changes should persist immediately so the theme survives reloads.
  if (autoSaveEnabled.value && !isSaving.value) {
    void savePlatformSettings(updatedPlatform)
  }
}

const handleToggleTwoFactor = (enabled: boolean) => {
  security.value.two_factor_enabled = enabled
  hasUnsavedChanges.value = true
  
  if (enabled) {
    successMessage.value = 'Zwei-Faktor-Authentifizierung aktiviert'
  } else {
    successMessage.value = 'Zwei-Faktor-Authentifizierung deaktiviert'
  }
  
  setTimeout(() => {
    successMessage.value = undefined
  }, 3000)
}

const handleUploadAvatar = () => {
  // Implement avatar upload logic
  console.log('Upload avatar')
}

const handleRemoveAvatar = () => {
  profile.value.avatar_url = ''
  hasUnsavedChanges.value = true
  successMessage.value = 'Profilbild entfernt'
  
  setTimeout(() => {
    successMessage.value = undefined
  }, 3000)
}

const handleShowBackupCodes = () => {
  // Show backup codes modal
  console.log('Show backup codes')
}

const handleTerminateSession = (sessionId: string) => {
  revokeSecurityItem(`/api/settings/security/sessions/${sessionId}`, 'Sitzung beendet')
}

const handleRevokeTrustedDevice = (deviceId: string) => {
  revokeSecurityItem(`/api/settings/security/trusted-devices/${deviceId}`, 'Vertrauenswürdiges Gerät entfernt')
}

const openAccountModal = async (mode: 'delete' | 'deactivate') => {
  accountModalMode.value = mode
  accountActionError.value = undefined
  accountModalOpen.value = true

  try {
    const response = await authStore.fetchWithAuth('/api/settings/account/impact')
    if (!response.ok) {
      throw new Error(`Failed to load account impact: ${response.status}`)
    }
    accountImpact.value = await response.json()
  } catch (err) {
    console.error('Error loading account impact:', err)
    accountImpact.value = null
    accountActionError.value = 'Auswirkungen auf das Konto konnten nicht geladen werden.'
  }
}

const closeAccountModal = () => {
  accountModalOpen.value = false
  accountActionError.value = undefined
}

const submitAccountClosure = async (payload: { password?: string; confirmation: string }) => {
  accountActionLoading.value = true
  accountActionError.value = undefined

  const endpoint = accountModalMode.value === 'delete'
    ? '/api/settings/account/delete'
    : '/api/settings/account/deactivate'

  try {
    const response = await authStore.fetchWithAuth(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    const responseData = await response.json().catch(() => ({}))
    if (!response.ok) {
      throw new Error(responseData?.detail || responseData?.message || `Request failed with status ${response.status}`)
    }

    await authStore.logout()
    await navigateTo('/login')
  } catch (err) {
    console.error('Error closing account:', err)
    accountActionError.value = err instanceof Error ? err.message : 'Kontoaktion fehlgeschlagen.'
  } finally {
    accountActionLoading.value = false
  }
}

const revokeSecurityItem = async (path: string, message: string) => {
  isSaving.value = true
  error.value = undefined

  try {
    const response = await authStore.fetchWithAuth(path, {
      method: 'DELETE'
    })

    if (!response.ok) {
      throw new Error(`Failed to revoke security item: ${response.status} ${response.statusText}`)
    }

    await fetchSettings()
    successMessage.value = message
    setTimeout(() => {
      successMessage.value = undefined
    }, 3000)
  } catch (err) {
    console.error('Error revoking security item:', err)
    error.value = 'Fehler beim Aktualisieren der Sicherheitseinstellungen.'
  } finally {
    isSaving.value = false
  }
}

const handleSave = async () => {
  isSaving.value = true
  error.value = undefined
  successMessage.value = undefined

  try {
    // Prepare settings update request
    const settingsUpdate = {
      profile: profile.value,
      security: security.value,
      notifications: notifications.value,
      privacy: privacy.value,
      platform: platform.value
    }
    
    const response = await authStore.fetchWithAuth('/api/settings/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(settingsUpdate)
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`Failed to save settings: ${response.status} ${response.statusText} - ${JSON.stringify(errorData)}`)
    }
    
    const data: SettingsResponse = await response.json()
    
    // Update with response data
    if (data.settings) {
      profile.value = data.settings.profile
      security.value = normalizeSecuritySettings(data.settings.security)
      notifications.value = data.settings.notifications
      privacy.value = data.settings.privacy
      platform.value = data.settings.platform
      syncPlatformTheme(data.settings.platform.theme)
      originalSettings.value = data.settings
    }
    
    lastSavedAt.value = data.last_updated
    hasUnsavedChanges.value = false
    successMessage.value = 'Einstellungen erfolgreich gespeichert'
    
    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = undefined
    }, 3000)
  } catch (err) {
    console.error('Error saving settings:', err)
    error.value = 'Fehler beim Speichern der Einstellungen. Bitte versuche es später erneut.'
  } finally {
    isSaving.value = false
  }
}

const handleReset = () => {
  // Reset to original values from API
  if (originalSettings.value) {
    profile.value = originalSettings.value.profile
    security.value = originalSettings.value.security
    notifications.value = originalSettings.value.notifications
    privacy.value = originalSettings.value.privacy
    platform.value = originalSettings.value.platform
    syncPlatformTheme(originalSettings.value.platform.theme)
  } else {
    // If no original settings, reload from API
    fetchSettings()
  }
  
  hasUnsavedChanges.value = false
  successMessage.value = 'Änderungen zurückgesetzt'
  
  setTimeout(() => {
    successMessage.value = undefined
  }, 3000)
}

const handleToggleAutoSave = (enabled: boolean) => {
  autoSaveEnabled.value = enabled
}

const handleExport = () => {
  const settingsData = {
    profile: profile.value,
    security: security.value,
    notifications: notifications.value,
    privacy: privacy.value,
    platform: platform.value,
    exported_at: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(settingsData, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `hackathon-hub-settings-${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

// Lifecycle
onMounted(async () => {
  await fetchSettings()
})
</script>

<style scoped>
.settings-page-template {
  @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8;
}
</style>
