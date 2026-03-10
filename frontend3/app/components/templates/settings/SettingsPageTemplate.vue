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
    <div class="flex flex-col lg:flex-row gap-8">
      <!-- Left Sidebar: Navigation -->
      <div class="lg:w-64 flex-shrink-0">
        <SettingsNavigation
          :active-tab="activeTab"
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
import SettingsNavigation from '~/components/organisms/settings/SettingsNavigation.vue'
import SettingsContent from '~/components/organisms/settings/SettingsContent.vue'
import SettingsActions from '~/components/organisms/settings/SettingsActions.vue'
import LoadingSpinner from '~/components/atoms/LoadingSpinner.vue'
import type {
  ProfileSettings,
  SecuritySettings,
  NotificationSettings,
  PrivacySettings,
  PlatformPreferences,
  UserSettings,
  SettingsResponse
} from '~/types/settings-types'

// Auth store
const authStore = useAuthStore()

// Reactive state
const activeTab = ref('profile')
const isLoading = ref(false)
const isSaving = ref(false)
const autoSaveEnabled = ref(true)
const hasUnsavedChanges = ref(false)
const lastSavedAt = ref<string>()
const error = ref<string>()
const successMessage = ref<string>()

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
  active_sessions: []
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
      security.value = data.settings.security
      notifications.value = data.settings.notifications
      privacy.value = data.settings.privacy
      platform.value = data.settings.platform
      
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

const handlePlatformUpdate = (updatedPlatform: PlatformPreferences) => {
  platform.value = updatedPlatform
  hasUnsavedChanges.value = true
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
  security.value.active_sessions = security.value.active_sessions.filter(
    session => session.id !== sessionId
  )
  hasUnsavedChanges.value = true
  successMessage.value = 'Sitzung beendet'
  
  setTimeout(() => {
    successMessage.value = undefined
  }, 3000)
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
      security.value = data.settings.security
      notifications.value = data.settings.notifications
      privacy.value = data.settings.privacy
      platform.value = data.settings.platform
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