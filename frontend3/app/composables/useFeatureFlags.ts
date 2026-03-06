/**
 * Feature Flags Composable für Atomic Design Refactoring
 * Wrapper um die bestehende Feature-Flags-Implementierung
 */

import { useFeatureFlags as useExistingFeatureFlags } from '~/config/feature-flags'

/**
 * Feature Flags Composable Rückgabetyp
 */
export interface UseFeatureFlagsReturn {
  /** Ist Flag aktiviert */
  isEnabled: (flagName: string) => boolean
  /** Flag aktivieren */
  enableFlag: (flagName: string) => void
  /** Flag deaktivieren */
  disableFlag: (flagName: string) => void
  /** Flag umschalten */
  toggleFlag: (flagName: string) => void
}

/**
 * Feature Flags Composable
 */
export function useFeatureFlags(): UseFeatureFlagsReturn {
  const existingFlags = useExistingFeatureFlags()
  
  /**
   * Ist Flag aktiviert
   */
  function isEnabled(flagName: string): boolean {
    return existingFlags.isEnabled(flagName as any)
  }
  
  /**
   * Flag aktivieren
   */
  function enableFlag(flagName: string): void {
    existingFlags.enable(flagName as any)
  }
  
  /**
   * Flag deaktivieren
   */
  function disableFlag(flagName: string): void {
    existingFlags.disable(flagName as any)
  }
  
  /**
   * Flag umschalten
   */
  function toggleFlag(flagName: string): void {
    if (isEnabled(flagName)) {
      disableFlag(flagName)
    } else {
      enableFlag(flagName)
    }
  }
  
  return {
    isEnabled,
    enableFlag,
    disableFlag,
    toggleFlag,
  }
}

/**
 * Vereinfachter Hook für Feature Flags
 */
export function useFeatureFlag(flagName: string) {
  const featureFlags = useFeatureFlags()
  
  const isEnabled = computed(() => featureFlags.isEnabled(flagName))
  const toggle = () => featureFlags.toggleFlag(flagName)
  const enable = () => featureFlags.enableFlag(flagName)
  const disable = () => featureFlags.disableFlag(flagName)
  
  return {
    isEnabled,
    toggle,
    enable,
    disable,
  }
}