import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { usePreferencesStore } from './preferences'

export const useThemeStore = defineStore('theme', () => {
  const themeCookie = useCookie<'light' | 'dark' | 'system' | null>('theme')
  const selectedTheme = ref<'light' | 'dark' | 'system'>(themeCookie.value ?? 'system')
  const systemPrefersDark = ref(false)
  const isInitialized = ref(false)

  const resolvedTheme = computed<'light' | 'dark'>(() => {
    if (selectedTheme.value === 'system') {
      return systemPrefersDark.value ? 'dark' : 'light'
    }
    return selectedTheme.value
  })
  const isDark = computed(() => resolvedTheme.value === 'dark')
  const theme = computed(() => selectedTheme.value)

  const syncSystemPreference = () => {
    if (typeof window === 'undefined') return
    systemPrefersDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }

  function toggleTheme() {
    setTheme(isDark.value ? 'light' : 'dark')
  }

  function setTheme(nextTheme: 'light' | 'dark' | 'system') {
    selectedTheme.value = nextTheme
    themeCookie.value = nextTheme
    const preferences = usePreferencesStore()
    preferences.theme.setTheme(nextTheme)
    updateDocumentClass()
  }

  function initializeTheme() {
    if (typeof window === 'undefined') {
      isInitialized.value = true
      return theme.value
    }

    const preferences = usePreferencesStore()
    const savedTheme = preferences.theme.initialize()
    selectedTheme.value = savedTheme
    syncSystemPreference()
    updateDocumentClass()
    isInitialized.value = true
    return savedTheme
  }

  function updateDocumentClass() {
    if (typeof window === 'undefined') return
    document.documentElement.classList.remove('light', 'dark')
    if (resolvedTheme.value === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.add('light')
    }
    document.documentElement.setAttribute('data-theme', resolvedTheme.value)
  }

  return {
    isDark,
    isInitialized,
    theme,
    toggleTheme,
    setTheme,
    initializeTheme
  }
})
