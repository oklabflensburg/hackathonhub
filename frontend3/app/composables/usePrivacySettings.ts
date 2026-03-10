import { computed } from 'vue'
import type { PrivacySettings, VisibilityLevel, MessagePermission } from '~/types/settings-types'
import { useSettings } from './useSettings'

/**
 * Spezialisiertes Composable für Datenschutzeinstellungen
 * Bietet zusätzliche Hilfsfunktionen und Validierung für Privacy-spezifische Operationen
 */
export function usePrivacySettings() {
  const settings = useSettings()
  
  // Reaktive Privacy-Einstellungen
  const privacySettings = computed<PrivacySettings | null>(() => settings.privacy.value)
  
  // Computed Properties für häufig verwendete Werte
  const profileVisibility = computed<VisibilityLevel | null>(() => privacySettings.value?.profile_visibility ?? null)
  const emailVisibility = computed<VisibilityLevel | null>(() => privacySettings.value?.email_visibility ?? null)
  const messagePermission = computed<MessagePermission | null>(() => privacySettings.value?.allow_messages_from ?? null)
  const showOnlineStatus = computed<boolean | null>(() => privacySettings.value?.show_online_status ?? null)
  const allowTagging = computed<boolean | null>(() => privacySettings.value?.allow_tagging ?? null)
  const showActivity = computed<boolean | null>(() => privacySettings.value?.show_activity ?? null)
  
  // Data Sharing Einstellungen
  const dataSharing = computed(() => privacySettings.value?.data_sharing ?? null)
  const allowAnalytics = computed<boolean | null>(() => dataSharing.value?.analytics ?? null)
  const allowMarketing = computed<boolean | null>(() => dataSharing.value?.marketing ?? null)
  const allowThirdParties = computed<boolean | null>(() => dataSharing.value?.third_parties ?? null)
  
  /**
   * Privacy-Einstellung aktualisieren
   */
  function updatePrivacySetting<K extends keyof PrivacySettings>(
    key: K,
    value: PrivacySettings[K]
  ): void {
    if (!privacySettings.value) return
    
    settings.updateSetting('privacy', key, value)
  }
  
  /**
   * Data Sharing Einstellung aktualisieren
   */
  function updateDataSharing<K extends keyof PrivacySettings['data_sharing']>(
    key: K,
    value: PrivacySettings['data_sharing'][K]
  ): void {
    if (!privacySettings.value) return
    
    const updatedDataSharing = {
      ...privacySettings.value.data_sharing,
      [key]: value
    }
    
    updatePrivacySetting('data_sharing', updatedDataSharing)
  }
  
  /**
   * Privacy Level berechnen (basierend auf den Einstellungen)
   * Gibt einen Wert zwischen 0 (sehr privat) und 100 (sehr öffentlich) zurück
   */
  const privacyScore = computed<number>(() => {
    if (!privacySettings.value) return 50
    
    let score = 50 // Neutraler Startwert
    
    // Profile Visibility
    switch (privacySettings.value.profile_visibility) {
      case 'public':
        score += 25
        break
      case 'friends_only':
        score += 10
        break
      case 'private':
        score -= 15
        break
    }
    
    // Email Visibility
    switch (privacySettings.value.email_visibility) {
      case 'public':
        score += 20
        break
      case 'friends_only':
        score += 5
        break
      case 'private':
        score -= 10
        break
    }
    
    // Boolean Einstellungen
    if (privacySettings.value.show_online_status) score += 10
    if (privacySettings.value.show_activity) score += 10
    if (privacySettings.value.allow_tagging) score += 5
    
    // Message Permissions
    switch (privacySettings.value.allow_messages_from) {
      case 'all_users':
        score += 15
        break
      case 'friends_only':
        score += 5
        break
      case 'none':
        score -= 10
        break
    }
    
    // Data Sharing
    if (privacySettings.value.data_sharing.analytics) score += 5
    if (privacySettings.value.data_sharing.marketing) score += 10
    if (privacySettings.value.data_sharing.third_parties) score += 15
    
    // Auf Bereich 0-100 begrenzen
    return Math.max(0, Math.min(100, score))
  })
  
  /**
   * Privacy Level als Text beschreiben
   */
  const privacyLevel = computed<string>(() => {
    const score = privacyScore.value
    
    if (score >= 80) return 'Very Public'
    if (score >= 60) return 'Public'
    if (score >= 40) return 'Balanced'
    if (score >= 20) return 'Private'
    return 'Very Private'
  })
  
  /**
   * Privacy Level als Farbe für UI-Elemente
   */
  const privacyLevelColor = computed<string>(() => {
    const score = privacyScore.value
    
    if (score >= 80) return 'green'
    if (score >= 60) return 'blue'
    if (score >= 40) return 'yellow'
    if (score >= 20) return 'orange'
    return 'red'
  })
  
  /**
   * Alle Privacy-Einstellungen auf Standardwerte zurücksetzen
   */
  function resetToDefaults(): void {
    if (!privacySettings.value) return
    
    const defaultPrivacySettings: PrivacySettings = {
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
    }
    
    settings.updateSetting('privacy', 'profile_visibility', defaultPrivacySettings.profile_visibility)
    settings.updateSetting('privacy', 'email_visibility', defaultPrivacySettings.email_visibility)
    settings.updateSetting('privacy', 'show_online_status', defaultPrivacySettings.show_online_status)
    settings.updateSetting('privacy', 'allow_messages_from', defaultPrivacySettings.allow_messages_from)
    settings.updateSetting('privacy', 'show_activity', defaultPrivacySettings.show_activity)
    settings.updateSetting('privacy', 'allow_tagging', defaultPrivacySettings.allow_tagging)
    settings.updateSetting('privacy', 'data_sharing', defaultPrivacySettings.data_sharing)
  }
  
  /**
   * Privacy-Einstellungen exportieren (für Download)
   */
  function exportPrivacySettings(): string {
    if (!privacySettings.value) return ''
    
    return JSON.stringify({
      privacy_settings: privacySettings.value,
      exported_at: new Date().toISOString(),
      privacy_score: privacyScore.value,
      privacy_level: privacyLevel.value
    }, null, 2)
  }
  
  /**
   * Überprüfen, ob bestimmte Daten mit anderen geteilt werden dürfen
   */
  function canShareData(dataType: 'profile' | 'email' | 'activity' | 'presence', withWhom: 'public' | 'friends' | 'team'): boolean {
    if (!privacySettings.value) return false
    
    switch (dataType) {
      case 'profile':
        return canShareProfile(withWhom)
      case 'email':
        return canShareEmail(withWhom)
      case 'activity':
        return canShareActivity(withWhom)
      case 'presence':
        return canSharePresence(withWhom)
      default:
        return false
    }
  }
  
  /**
   * Hilfsfunktionen für spezifische Datentypen
   */
  function canShareProfile(withWhom: 'public' | 'friends' | 'team'): boolean {
    if (!privacySettings.value) return false
    
    switch (privacySettings.value.profile_visibility) {
      case 'public':
        return true
      case 'friends_only':
        return withWhom === 'friends' || withWhom === 'team'
      case 'private':
        return false
    }
  }
  
  function canShareEmail(withWhom: 'public' | 'friends' | 'team'): boolean {
    if (!privacySettings.value) return false
    
    switch (privacySettings.value.email_visibility) {
      case 'public':
        return true
      case 'friends_only':
        return withWhom === 'friends' || withWhom === 'team'
      case 'private':
        return false
    }
  }
  
  function canShareActivity(withWhom: 'public' | 'friends' | 'team'): boolean {
    if (!privacySettings.value) return false
    
    if (!privacySettings.value.show_activity) return false
    
    // Aktivität folgt der Profile Visibility
    return canShareProfile(withWhom)
  }
  
  function canSharePresence(withWhom: 'public' | 'friends' | 'team'): boolean {
    if (!privacySettings.value) return false
    
    if (!privacySettings.value.show_online_status) return false
    
    // Online-Status folgt der Profile Visibility
    return canShareProfile(withWhom)
  }
  
  return {
    // State
    privacySettings,
    
    // Computed Properties
    profileVisibility,
    emailVisibility,
    messagePermission,
    showOnlineStatus,
    allowTagging,
    showActivity,
    dataSharing,
    allowAnalytics,
    allowMarketing,
    allowThirdParties,
    privacyScore,
    privacyLevel,
    privacyLevelColor,
    
    // Methods
    updatePrivacySetting,
    updateDataSharing,
    resetToDefaults,
    exportPrivacySettings,
    canShareData,
    canShareProfile,
    canShareEmail,
    canShareActivity,
    canSharePresence
  }
}