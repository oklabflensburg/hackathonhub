/**
 * Theme Composable für Atomic Design Layout-Komponenten
 * Verwaltet Theme (light/dark/system) mit Persistenz und System-Präferenz-Erkennung
 */

import type { ThemeState } from '~/types/layout-types'

/**
 * Theme Optionen
 */
export type Theme = 'light' | 'dark' | 'system'

/**
 * Theme Composable Rückgabetyp
 */
export interface UseThemeReturn {
  /** Aktueller Theme-Zustand */
  state: Ref<ThemeState>
  /** Aktuelles angewendetes Theme */
  currentTheme: ComputedRef<'light' | 'dark'>
  /** Theme wechseln */
  setTheme: (theme: Theme) => void
  /** Theme toggle (light/dark) */
  toggleTheme: () => void
  /** System-Präferenz verwenden */
  useSystemPreference: () => void
  /** Theme zurücksetzen auf gespeicherten Wert */
  resetTheme: () => void
  /** Theme in localStorage speichern */
  persistTheme: () => void
}

/**
 * Theme Composable
 */
export function useTheme(): UseThemeReturn {
  // Zustand
  const state = ref<ThemeState>({
    current: 'system',
    systemPreference: 'light',
    persisted: false,
  })

  // SSR-safe Prüfung für Browser-APIs
  const isClient = typeof window !== 'undefined'
  const isLocalStorageAvailable = isClient && typeof localStorage !== 'undefined'
  const isMatchMediaAvailable = isClient && typeof window.matchMedia !== 'undefined'

  // Initialisiere Theme
  onMounted(() => {
    initializeTheme()
  })

  // System-Präferenz-Änderungen überwachen
  if (isMatchMediaAvailable) {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    
    const handleSystemPreferenceChange = (e: MediaQueryListEvent) => {
      state.value.systemPreference = e.matches ? 'dark' : 'light'
      
      // Wenn aktuelles Theme 'system' ist, Theme aktualisieren
      if (state.value.current === 'system') {
        applyThemeToDocument(state.value.systemPreference)
      }
    }
    
    // Event Listener hinzufügen
    mediaQuery.addEventListener('change', handleSystemPreferenceChange)
    
    // Cleanup
    onUnmounted(() => {
      mediaQuery.removeEventListener('change', handleSystemPreferenceChange)
    })
  }

  /**
   * Theme initialisieren
   */
  function initializeTheme(): void {
    if (!isClient) return

    // 1. System-Präferenz ermitteln
    if (isMatchMediaAvailable) {
      state.value.systemPreference = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light'
    }

    // 2. Gespeichertes Theme laden
    let savedTheme: Theme | null = null
    if (isLocalStorageAvailable) {
      const saved = localStorage.getItem('theme')
      if (saved === 'light' || saved === 'dark' || saved === 'system') {
        savedTheme = saved
        state.value.persisted = true
      }
    }

    // 3. Theme anwenden (gespeichertes > system)
    const themeToApply = savedTheme || 'system'
    state.value.current = themeToApply
    
    applyTheme(themeToApply, false) // Nicht erneut persistieren
  }

  /**
   * Theme auf Document anwenden
   */
  function applyThemeToDocument(theme: 'light' | 'dark'): void {
    if (!isClient) return

    const root = document.documentElement
    
    // Alte Klassen entfernen
    root.classList.remove('light', 'dark')
    
    // Neue Klasse hinzufügen
    root.classList.add(theme)
    
    // Data-Attribute setzen
    root.setAttribute('data-theme', theme)
    
    // Meta Tag aktualisieren
    updateMetaThemeColor(theme)
  }

  /**
   * Meta Theme Color aktualisieren
   */
  function updateMetaThemeColor(theme: 'light' | 'dark'): void {
    if (!isClient) return

    // Finde oder erstelle meta[name="theme-color"]
    let metaThemeColor = document.querySelector('meta[name="theme-color"]')
    
    if (!metaThemeColor) {
      metaThemeColor = document.createElement('meta')
      metaThemeColor.setAttribute('name', 'theme-color')
      document.head.appendChild(metaThemeColor)
    }
    
    // Setze Farbe basierend auf Theme
    const color = theme === 'dark' ? '#1f2937' : '#ffffff' // gray-800 / white
    metaThemeColor.setAttribute('content', color)
  }

  /**
   * Theme anwenden
   */
  function applyTheme(theme: Theme, persist: boolean = true): void {
    // Bestimme tatsächliches Theme (light/dark)
    const actualTheme = theme === 'system' 
      ? state.value.systemPreference 
      : theme
    
    // Auf Document anwenden
    applyThemeToDocument(actualTheme)
    
    // Zustand aktualisieren
    state.value.current = theme
    
    // Persistieren wenn gewünscht
    if (persist && isLocalStorageAvailable) {
      localStorage.setItem('theme', theme)
      state.value.persisted = true
    }
  }

  /**
   * Theme setzen
   */
  function setTheme(theme: Theme): void {
    applyTheme(theme)
    // Event emit für andere Komponenten
    if (isClient) {
      window.dispatchEvent(new CustomEvent('theme-change', { detail: { theme } }))
    }
  }

  /**
   * Theme toggle (light/dark)
   */
  function toggleTheme(): void {
    const newTheme = state.value.current === 'dark' ? 'light' : 'dark'
    setTheme(newTheme)
  }

  /**
   * System-Präferenz verwenden
   */
  function useSystemPreference(): void {
    setTheme('system')
  }

  /**
   * Theme zurücksetzen
   */
  function resetTheme(): void {
    if (isLocalStorageAvailable) {
      localStorage.removeItem('theme')
    }
    state.value.persisted = false
    setTheme('system')
  }

  /**
   * Theme persistieren
   */
  function persistTheme(): void {
    if (isLocalStorageAvailable) {
      localStorage.setItem('theme', state.value.current)
      state.value.persisted = true
    }
  }

  // Aktuelles angewendetes Theme (berechnet)
  const currentTheme = computed(() => {
    return state.value.current === 'system'
      ? state.value.systemPreference
      : state.value.current
  })

  return {
    state,
    currentTheme,
    setTheme,
    toggleTheme,
    useSystemPreference,
    resetTheme,
    persistTheme,
  }
}

/**
 * Theme Hook für Komponenten
 * Vereinfachte Version von useTheme()
 */
export function useThemeHook() {
  const theme = useTheme()
  
  return {
    theme: theme.currentTheme,
    themeState: theme.state,
    toggleTheme: theme.toggleTheme,
    setTheme: theme.setTheme,
    isDark: computed(() => theme.currentTheme.value === 'dark'),
    isLight: computed(() => theme.currentTheme.value === 'light'),
    isSystem: computed(() => theme.state.value.current === 'system'),
  }
}