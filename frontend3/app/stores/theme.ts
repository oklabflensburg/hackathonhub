import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // Initialize with false for SSR, will be updated on client
  const isDark = ref(false)

  const theme = computed(() => isDark.value ? 'dark' : 'light')
  const icon = computed(() => isDark.value ? '🌙' : '☀️')

  function toggleTheme() {
    isDark.value = !isDark.value
    if (typeof window !== 'undefined') {
      localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
      updateDocumentClass()
    }
  }

  function setTheme(dark: boolean) {
    isDark.value = dark
    if (typeof window !== 'undefined') {
      localStorage.setItem('theme', dark ? 'dark' : 'light')
      updateDocumentClass()
    }
  }

  function initializeTheme() {
    if (typeof window === 'undefined') return
    
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      isDark.value = savedTheme === 'dark'
    } else {
      // Check system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      isDark.value = prefersDark
    }
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