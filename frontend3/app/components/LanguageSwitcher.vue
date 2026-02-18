<template>
  <div class="relative">
    <button
      @click="toggleLanguageMenu"
      class="flex items-center space-x-1 sm:space-x-2 p-1.5 sm:p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
      :aria-label="t('languageSwitcher.ariaLabel')"
    >
      <span class="text-lg sm:text-xl">🌐</span>
      <span class="hidden sm:inline text-sm sm:text-base font-medium text-gray-700 dark:text-gray-300">
        {{ currentLanguageName }}
      </span>
      <svg
        class="w-4 h-4 sm:w-5 sm:h-5 text-gray-500 dark:text-gray-400 transition-transform"
        :class="{ 'rotate-180': languageMenuOpen }"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Language Dropdown Menu -->
    <div
      v-if="languageMenuOpen"
      class="absolute right-0 mt-2 w-48 sm:w-56 bg-white dark:bg-gray-800 rounded-xl shadow-elevated border border-gray-200 dark:border-gray-700 py-2 z-50 animate-slide-in glass-effect"
    >
      <div class="px-3 sm:px-4 py-2 sm:py-3 border-b border-gray-100 dark:border-gray-700">
        <p class="font-medium text-gray-900 dark:text-white text-sm sm:text-base">
          {{ t('languageSwitcher.selectLanguage') }}
        </p>
      </div>
      
      <button
        @click="switchLanguage('en')"
        class="flex items-center w-full px-3 sm:px-4 py-2 sm:py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm sm:text-base"
        :class="{ 'bg-gray-50 dark:bg-gray-700': locale === 'en' }"
      >
        <span class="flex-1 text-left">{{ t('languageSwitcher.english') }}</span>
        <svg v-if="locale === 'en'" class="w-4 h-4 sm:w-5 sm:h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
      </button>
      
      <button
        @click="switchLanguage('de')"
        class="flex items-center w-full px-3 sm:px-4 py-2 sm:py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm sm:text-base"
        :class="{ 'bg-gray-50 dark:bg-gray-700': locale === 'de' }"
      >
        <span class="flex-1 text-left">{{ t('languageSwitcher.german') }}</span>
        <svg v-if="locale === 'de'" class="w-4 h-4 sm:w-5 sm:h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// useI18n is auto-imported by @nuxtjs/i18n
const { locale, t } = useI18n()
const switchLocalePath = useSwitchLocalePath()

const languageMenuOpen = ref(false)

const currentLanguageName = computed(() => {
  return locale.value === 'en' ? t('languageSwitcher.english') : t('languageSwitcher.german')
})

const toggleLanguageMenu = () => {
  languageMenuOpen.value = !languageMenuOpen.value
}

const switchLanguage = async (lang: 'de' | 'en') => {
  if (lang === locale.value) {
    languageMenuOpen.value = false
    return
  }

  const targetPath = switchLocalePath(lang)

  languageMenuOpen.value = false

  if (targetPath) {
    await navigateTo(targetPath)
  } else {
    locale.value = lang
  }

  // Save preference to localStorage
  if (process.client) {
    localStorage.setItem('preferred-language', lang)
  }
}

// Close menu when clicking outside
if (process.client) {
  document.addEventListener('click', (event) => {
    const target = event.target as HTMLElement
    if (!target.closest('.relative')) {
      languageMenuOpen.value = false
    }
  })
}
</script>