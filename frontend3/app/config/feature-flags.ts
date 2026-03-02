/**
 * Feature Flags für die schrittweise Migration von Features
 * Diese Flags ermöglichen es, neue Features schrittweise zu aktivieren
 * und bei Bedarf schnell zu deaktivieren.
 */

export interface FeatureFlags {
  /**
   * Atomic Design Team Invitations
   * Aktiviert die neuen Atomic Design Komponenten für Team-Einladungen
   * Standard: false (alte Implementierung)
   */
  atomicTeamInvitations: boolean
  
  /**
   * Neue User Search mit Debouncing
   * Aktiviert die verbesserte Benutzersuche mit Debouncing
   * Standard: false (alte Implementierung)
   */
  improvedUserSearch: boolean
  
  /**
   * Real-time Invitation Updates
   * Aktiviert Polling für Echtzeit-Updates von Einladungen
   * Standard: false (kein Polling)
   */
  realTimeInvitations: boolean
  
  /**
   * Neue Team Management UI
   * Aktiviert die überarbeitete Team-Management-Oberfläche
   * Standard: false (alte UI)
   */
  newTeamManagementUI: boolean
}

/**
 * Feature Flag Konfiguration
 * Kann über Umgebungsvariablen oder Runtime-Konfiguration gesteuert werden
 */
const featureFlags: FeatureFlags = {
  atomicTeamInvitations: process.env.NUXT_PUBLIC_FEATURE_ATOMIC_TEAM_INVITATIONS === 'true' || false,
  improvedUserSearch: process.env.NUXT_PUBLIC_FEATURE_IMPROVED_USER_SEARCH === 'true' || false,
  realTimeInvitations: process.env.NUXT_PUBLIC_FEATURE_REAL_TIME_INVITATIONS === 'true' || false,
  newTeamManagementUI: process.env.NUXT_PUBLIC_FEATURE_NEW_TEAM_MANAGEMENT_UI === 'true' || false,
}

/**
 * Feature Flag Hook für Vue Komponenten
 */
export function useFeatureFlags() {
  // Für jetzt verwenden wir statische Flags
  // In einer echten Implementierung würden wir RuntimeConfig oder einen Store verwenden
  const flags: FeatureFlags = {
    atomicTeamInvitations: true, // Standardmäßig aktiviert für Testing
    improvedUserSearch: true,
    realTimeInvitations: false,
    newTeamManagementUI: false,
  }
  
  return {
    flags,
    isEnabled: (flag: keyof FeatureFlags) => flags[flag],
    enable: (flag: keyof FeatureFlags) => {
      flags[flag] = true
      // In einer echten Implementierung würde dies in einen Store oder Backend gespeichert
      console.log(`Feature flag "${flag}" enabled`)
    },
    disable: (flag: keyof FeatureFlags) => {
      flags[flag] = false
      console.log(`Feature flag "${flag}" disabled`)
    },
  }
}

/**
 * Feature Flag Guard für Komponenten
 * Verwendet Conditional Rendering basierend auf Feature Flags
 */
export function withFeatureFlag<T extends object>(
  flag: keyof FeatureFlags,
  Component: T,
  FallbackComponent?: T
) {
  return defineComponent({
    setup(props, { slots }) {
      const { isEnabled } = useFeatureFlags()
      const enabled = isEnabled(flag)
      
      return () => {
        if (enabled) {
          return h(Component, props, slots)
        } else if (FallbackComponent) {
          return h(FallbackComponent, props, slots)
        }
        return null
      }
    },
  })
}

export default featureFlags