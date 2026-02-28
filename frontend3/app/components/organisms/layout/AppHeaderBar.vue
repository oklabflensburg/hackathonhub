<template>
  <header class="sticky top-0 z-50 bg-white/95 dark:bg-gray-900/95 backdrop-blur-lg border-b border-gray-200/50 dark:border-gray-800/50 shadow-soft">
    <div class="container mx-auto px-3 sm:px-4 py-3 sm:py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3 sm:space-x-4">
          <button
            type="button"
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 lg:hidden transition-colors duration-200"
            :aria-label="t('appHeader.toggleSidebar')"
            @click="uiStore.toggleSidebar"
          >
            <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <NuxtLink to="/" class="flex items-center space-x-2 sm:space-x-3 group">
            <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center shadow-md group-hover:shadow-lg transition-shadow duration-200">
              <span class="text-white font-bold text-lg sm:text-xl">H</span>
            </div>
            <div class="hidden sm:block">
              <h1 class="text-lg sm:text-xl font-bold text-gray-900 dark:text-white">{{ t('app.name') }}</h1>
              <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">{{ t('appHeader.tagline') }}</p>
            </div>
            <div class="sm:hidden">
              <h1 class="text-lg font-bold text-gray-900 dark:text-white">{{ t('appHeader.mobileLogo') }}</h1>
            </div>
          </NuxtLink>
        </div>

        <HeaderNavLinks :links="navLinks" :current-path="route.path" />

        <div class="flex items-center space-x-2 sm:space-x-4">
          <button
            type="button"
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
            :title="themeStore.isDark ? t('appHeader.switchToLightMode') : t('appHeader.switchToDarkMode')"
            :aria-label="t('appHeader.toggleTheme')"
            @click="toggleTheme"
          >
            <span class="text-lg sm:text-xl">{{ themeStore.icon }}</span>
          </button>

          <LanguageSwitcher />

          <div v-if="authStore.isAuthenticated" class="relative">
            <UserAvatarButton
              :avatar-url="authStore.user?.avatar_url"
              :username="username"
              :subtitle="t('appHeader.viewProfile')"
              :menu-label="t('appHeader.userMenu')"
              @toggle="isUserMenuOpen = !isUserMenuOpen"
            />

            <div
              v-if="isUserMenuOpen"
              class="absolute right-0 mt-2 w-56 rounded-lg bg-white dark:bg-gray-800 shadow-lg border border-gray-200 dark:border-gray-700 py-2"
            >
              <NuxtLink to="/profile" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700" @click="isUserMenuOpen = false">
                {{ t('appHeader.myProfile') }}
              </NuxtLink>
              <NuxtLink to="/my-projects" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700" @click="isUserMenuOpen = false">
                {{ t('appHeader.myProjects') }}
              </NuxtLink>
              <NuxtLink to="/my-votes" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700" @click="isUserMenuOpen = false">
                {{ t('appHeader.myVotes') }}
              </NuxtLink>
              <button type="button" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20" @click="handleLogout">
                {{ t('appHeader.logout') }}
              </button>
            </div>
          </div>

          <div v-else class="hidden sm:flex items-center gap-2">
            <NuxtLink to="/login" class="px-3 py-2 rounded-lg text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800">
              {{ t('appHeader.login') }}
            </NuxtLink>
            <NuxtLink to="/register" class="px-3 py-2 rounded-lg text-sm text-white bg-primary-600 hover:bg-primary-700">
              {{ t('appHeader.createAccount') }}
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from '#imports'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '~/stores/auth'
import { useThemeStore } from '~/stores/theme'
import { useUIStore } from '~/stores/ui'
import HeaderNavLinks from '~/components/molecules/HeaderNavLinks.vue'
import UserAvatarButton from '~/components/molecules/UserAvatarButton.vue'
import LanguageSwitcher from '~/components/LanguageSwitcher.vue'

const route = useRoute()
const { t } = useI18n()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const uiStore = useUIStore()

const isUserMenuOpen = ref(false)
const username = computed(() => authStore.user?.username || authStore.user?.name || 'User')

const navLinks = computed(() => {
  const links = [
    { to: '/', label: t('appHeader.dashboard') },
    { to: '/hackathons', label: t('appHeader.hackathons') },
    { to: '/projects', label: t('appHeader.projects') },
  ]

  if (authStore.isAuthenticated) {
    links.push({ to: '/create', label: t('appHeader.create') })
  }

  return links
})

const toggleTheme = () => {
  themeStore.toggleTheme()
  themeStore.initializeTheme()
}

const handleLogout = async () => {
  await authStore.logout()
  isUserMenuOpen.value = false
}
</script>
