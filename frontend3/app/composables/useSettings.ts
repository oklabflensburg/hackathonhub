import { ref, computed, watch } from 'vue'
import type { Ref } from 'vue'
import type {
  UserSettings,
  ProfileSettings,
  NotificationSettings,
  PrivacySettings,
  PlatformPreferences,
  SecuritySettings,
  OAuthConnections,
  DataManagement,
  SettingsUpdate,
  SettingsValidationResult,
  ValidationError,
  DEFAULT_PROFILE_SETTINGS,
  DEFAULT_SECURITY_SETTINGS,
  DEFAULT_PRIVACY_SETTINGS,
  DEFAULT_PLATFORM_PREFERENCES,
  DEFAULT_NOTIFICATION_SETTINGS,
  DEFAULT_OAUTH_CONNECTIONS
} from '~/types/settings-types'

interface UseSettingsOptions {
  autoSave?: boolean
  saveDelay?: number
  onSave?: (settings: UserSettings) => Promise<void> | void
  onError?: (error: SettingsValidationResult) => void
}

/**
 * Haupt-Composable für die Verwaltung von Benutzereinstellungen
 * Bietet reaktive State-Verwaltung, Validierung und Auto-Save-Funktionalität
 */
export function useSettings(options: UseSettingsOptions = {}) {
  const {
    autoSave = false,
    saveDelay = 1000,
    onSave,
    onError
  } = options

  // Reaktive State-Variablen
  const settings = ref<UserSettings | null>(null)
  const isLoading = ref(false)
  const isSaving = ref(false)
  const validationResult = ref<SettingsValidationResult | null>(null)
  const lastSaved = ref<Date | null>(null)
  const hasUnsavedChanges = ref(false)

  // Computed Properties für einfachen Zugriff auf Settings-Sections
  const profile = computed<ProfileSettings | null>(() => settings.value?.profile ?? null)
  const security = computed<SecuritySettings | null>(() => settings.value?.security ?? null)
  const privacy = computed<PrivacySettings | null>(() => settings.value?.privacy ?? null)
  const platform = computed<PlatformPreferences | null>(() => settings.value?.platform ?? null)
  const notifications = computed<NotificationSettings | null>(() => settings.value?.notifications ?? null)
  const connections = computed<OAuthConnections | null>(() => settings.value?.connections ?? null)
  const data = computed<DataManagement | null>(() => settings.value?.data ?? null)

  // Auto-Save Timer
  let saveTimer: NodeJS.Timeout | null = null

  /**
   * Einstellungen vom Server laden
   */
  async function loadSettings(): Promise<void> {
    try {
      isLoading.value = true
      // TODO: API-Aufruf implementieren
      // const response = await $fetch<UserSettings>('/api/v1/settings')
      // settings.value = response
      
      // Mock-Daten für Entwicklung
      settings.value = getMockSettings()
      validationResult.value = null
    } catch (error) {
      console.error('Failed to load settings:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Einzelne Einstellung aktualisieren
   */
  function updateSetting<T extends keyof UserSettings>(
    section: T,
    key: keyof UserSettings[T],
    value: UserSettings[T][keyof UserSettings[T]]
  ): void {
    if (!settings.value) {
      console.warn('Cannot update setting: settings not loaded')
      return
    }

    // Deep clone für immutable updates
    const newSettings = { ...settings.value }
    
    // Type-safe update
    if (newSettings[section]) {
      // @ts-ignore - TypeScript kann den dynamischen Zugriff nicht sicher inferieren
      newSettings[section][key] = value
    }

    settings.value = newSettings
    hasUnsavedChanges.value = true

    if (autoSave) {
      scheduleAutoSave()
    }
  }

  /**
   * Mehrere Einstellungen auf einmal aktualisieren
   */
  function updateSettings(payload: Partial<UserSettings>): void {
    if (!settings.value) {
      console.warn('Cannot update settings: settings not loaded')
      return
    }

    settings.value = {
      ...settings.value,
      ...payload
    }
    hasUnsavedChanges.value = true

    if (autoSave) {
      scheduleAutoSave()
    }
  }

  /**
   * Einstellungen speichern
   */
  async function saveSettings(): Promise<boolean> {
    if (!settings.value) {
      console.warn('Cannot save: no settings to save')
      return false
    }

    try {
      isSaving.value = true
      
      // Validierung
      const validation = validateSettings(settings.value)
      if (!validation.valid) {
        validationResult.value = validation
        if (onError) {
          onError(validation)
        }
        return false
      }

      // TODO: API-Aufruf implementieren
      // await $fetch('/api/v1/settings', {
      //   method: 'PUT',
      //   body: settings.value
      // })

      // Mock-Speicherung
      await new Promise(resolve => setTimeout(resolve, 300))

      if (onSave) {
        await onSave(settings.value)
      }

      lastSaved.value = new Date()
      hasUnsavedChanges.value = false
      validationResult.value = null
      return true
    } catch (error) {
      console.error('Failed to save settings:', error)
      validationResult.value = {
        valid: false,
        errors: [{
          field: 'general',
          message: 'Failed to save settings. Please try again.',
          code: 'SAVE_FAILED'
        }]
      }
      return false
    } finally {
      isSaving.value = false
    }
  }

  /**
   * Einstellungen zurücksetzen (auf zuletzt gespeicherten Zustand)
   */
  function resetSettings(): void {
    if (!settings.value) return
    
    // TODO: Zuletzt gespeicherten Zustand vom Server laden
    // Für jetzt: Mock-Daten neu laden
    settings.value = getMockSettings()
    hasUnsavedChanges.value = false
    validationResult.value = null
  }

  /**
   * Auto-Save planen
   */
  function scheduleAutoSave(): void {
    if (saveTimer) {
      clearTimeout(saveTimer)
    }

    saveTimer = setTimeout(async () => {
      await saveSettings()
      saveTimer = null
    }, saveDelay)
  }

  /**
   * Einstellungen validieren
   */
  function validateSettings(settingsToValidate: UserSettings): SettingsValidationResult {
    const errors: ValidationError[] = []

    // Profile validieren
    if (settingsToValidate.profile) {
      if (!settingsToValidate.profile.username?.trim()) {
        errors.push({
          field: 'profile.username',
          message: 'Username is required',
          code: 'REQUIRED'
        })
      }
      if (!settingsToValidate.profile.email?.trim()) {
        errors.push({
          field: 'profile.email',
          message: 'Email is required',
          code: 'REQUIRED'
        })
      } else if (!isValidEmail(settingsToValidate.profile.email)) {
        errors.push({
          field: 'profile.email',
          message: 'Invalid email format',
          code: 'INVALID_EMAIL'
        })
      }
    }

    // Security validieren
    if (settingsToValidate.security) {
      // Zusätzliche Validierung für 2FA-Einrichtung könnte hier hinzugefügt werden
    }

    return {
      valid: errors.length === 0,
      errors
    }
  }

  /**
   * Email-Validierung
   */
  function isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  /**
   * Fehler für ein bestimmtes Feld abrufen
   */
  function getFieldErrors(fieldPath: string): ValidationError[] {
    if (!validationResult.value || validationResult.value.valid) {
      return []
    }
    return validationResult.value.errors.filter(error => error.field === fieldPath)
  }

  /**
   * Cleanup bei Komponenten-Zerstörung
   */
  function cleanup(): void {
    if (saveTimer) {
      clearTimeout(saveTimer)
      saveTimer = null
    }
  }

  // Watch für unsaved changes
  watch(hasUnsavedChanges, (newValue) => {
    if (newValue && autoSave) {
      scheduleAutoSave()
    }
  })

  return {
    // State
    settings: settings as Ref<UserSettings | null>,
    isLoading,
    isSaving,
    validationResult,
    lastSaved,
    hasUnsavedChanges,

    // Computed
    profile,
    security,
    privacy,
    platform,
    notifications,
    connections,
    data,

    // Methods
    loadSettings,
    updateSetting,
    updateSettings,
    saveSettings,
    resetSettings,
    validateSettings,
    getFieldErrors,
    cleanup
  }
}

/**
 * Mock-Daten für Entwicklung
 */
function getMockSettings(): UserSettings {
  return {
    profile: {
      username: 'johndoe',
      email: 'john.doe@example.com',
      name: 'John Doe',
      avatar_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=John',
      bio: 'Full-stack developer passionate about hackathons',
      location: 'Berlin, Germany',
      company: 'Tech Corp'
    },
    security: {
      two_factor_enabled: false,
      active_sessions: [
        {
          id: 'session-1',
          device: 'Chrome on Windows',
          location: 'Berlin, Germany',
          ip_address: '192.168.1.1',
          last_active: new Date().toISOString(),
          created_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
          current: true
        }
      ],
      trusted_devices: []
    },
    privacy: {
      profile_visibility: 'public',
      email_visibility: 'private',
      show_online_status: true,
      allow_messages_from: 'all_users',
      show_activity: true,
      allow_tagging: true,
      data_sharing: {
        analytics: true,
        marketing: false,
        third_parties: false
      }
    },
    platform: {
      theme: 'system',
      language: 'en',
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
    },
    notifications: {
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
        system_announcements: true,
        newsletter: false
      }
    },
    connections: {
      github: {
        connected: true,
        username: 'johndoe',
        avatar_url: 'https://github.com/johndoe.png',
        email: 'john.doe@example.com',
        connected_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
        scopes: ['user:email', 'repo']
      },
      google: {
        connected: false
      }
    },
    data: {
      export_status: undefined,
      deletion_status: undefined
    }
  }
}
