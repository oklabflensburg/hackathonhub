import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { usePreferencesStore } from './preferences'

export const useThemeStore = defineStore('theme', () => {
  // Initialize with false for SSR, will be updated on client
  const isDark = ref(false)

  const theme = computed(() => isDark.value ? 'dark' : 'light')
  const icon = computed(() => isDark.value ? '🌙' : '☀️')

  function toggleTheme() {
    const preferences = usePreferencesStore()
    const newTheme = isDark.value ? 'light' : 'dark'
    isDark.value = !isDark.value
    preferences.theme.setTheme(newTheme)
  }

  function setTheme(dark: boolean) {
    isDark.value = dark
    const preferences = usePreferencesStore()
    preferences.theme.setTheme(dark ? 'dark' : 'light')
  }

  function initializeTheme() {
    const preferences = usePreferencesStore()
    const savedTheme = preferences.theme.initialize()
    isDark.value = savedTheme === 'dark'
    updateDocumentClass()
  }

  function updateDocumentClass() {
    if (typeof window === 'undefined') return
    if (isDark.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // Initialize theme immediately if we're on client side
  if (typeof window !== 'undefined') {
    initializeTheme()
  }

  return {
    isDark,
    theme,
    icon,
    toggleTheme,
    setTheme,
    initializeTheme
  }
})