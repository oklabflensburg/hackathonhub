<template>
  <header class="sticky top-0 z-50 bg-white/95 dark:bg-gray-900/95 backdrop-blur-lg border-b border-gray-200/50 dark:border-gray-800/50 shadow-soft">
    <Container class="px-3 sm:px-4 py-3 sm:py-4" :size="'2xl'">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3 sm:space-x-4">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            :aria-label="t('appHeader.toggleSidebar')"
            class="lg:hidden"
            @click="uiStore.toggleSidebar"
          >
            <template #icon-left>
              <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </template>
          </Button>

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
          <Button
            type="button"
            variant="ghost"
            size="sm"
            :title="themeStore.isDark ? t('appHeader.switchToLightMode') : t('appHeader.switchToDarkMode')"
            :aria-label="t('appHeader.toggleTheme')"
            @click="toggleTheme"
          >
            <svg
              v-if="themeStore.isDark"
              class="w-5 h-5 sm:w-6 sm:h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
              />
            </svg>
            <svg
              v-else
              class="w-5 h-5 sm:w-6 sm:h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
          </Button>

          <LanguageSwitcher />

          <div v-if="authStore.isAuthenticated" class="flex items-center gap-2">
            <NotificationBadge />
            <div class="relative" ref="userMenuContainer">
              <UserAvatarButton
                :avatar-url="authStore.user?.avatar_url"
                :username="username"
                :subtitle="t('appHeader.viewProfile')"
                :menu-label="t('appHeader.userMenu')"
                :open="isUserMenuOpen"
                @toggle="isUserMenuOpen = !isUserMenuOpen"
              />

              <div
                v-if="isUserMenuOpen"
                class="absolute right-0 mt-2 w-48 sm:w-56 bg-white dark:bg-gray-800 rounded-xl shadow-elevated border border-gray-200 dark:border-gray-700 py-2 z-50 animate-slide-in glass-effect"
              >
                <div class="px-3 sm:px-4 py-2 sm:py-3 border-b border-gray-100 dark:border-gray-700">
                  <p class="font-medium text-gray-900 dark:text-white text-sm sm:text-base">
                    {{ t('appHeader.userMenu') }}
                  </p>
                  <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">
                    {{ username }}
                  </p>
                </div>

                <NuxtLink
                  to="/profile"
                  class="flex items-center w-full px-3 sm:px-4 py-2 sm:py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm sm:text-base"
                  @click="isUserMenuOpen = false"
                >
                  {{ t('appHeader.myProfile') }}
                </NuxtLink>
                <NuxtLink
                  to="/my-projects"
                  class="flex items-center w-full px-3 sm:px-4 py-2 sm:py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm sm:text-base"
                  @click="isUserMenuOpen = false"
                >
                  {{ t('appHeader.myProjects') }}
                </NuxtLink>
                <NuxtLink
                  to="/my-votes"
                  class="flex items-center w-full px-3 sm:px-4 py-2 sm:py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm sm:text-base"
                  @click="isUserMenuOpen = false"
                >
                  {{ t('appHeader.myVotes') }}
                </NuxtLink>
                <button
                  type="button"
                  class="flex items-center w-full px-3 sm:px-4 py-2 sm:py-3 text-red-600 dark:text-red-400 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm sm:text-base"
                  @click="handleLogout"
                >
                  {{ t('appHeader.logout') }}
                </button>
              </div>
            </div>
          </div>

          <div v-else class="flex items-center gap-1 sm:gap-2">
            <NuxtLink
              to="/login"
              class="inline-flex items-center justify-center font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:opacity-50 disabled:cursor-not-allowed px-2 py-1 text-xs text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 focus:ring-gray-500/20 rounded-lg text-xs sm:text-sm"
            >
              {{ t('appHeader.login') }}
            </NuxtLink>
            <NuxtLink
              to="/register"
              class="inline-flex items-center justify-center font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:opacity-50 disabled:cursor-not-allowed px-2 py-1 text-xs bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500/20 rounded-lg text-xs sm:text-sm"
            >
              {{ t('appHeader.createAccount') }}
            </NuxtLink>
          </div>
        </div>
      </div>
    </Container>
  </header>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from '#imports'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '~/stores/auth'
import { useThemeStore } from '~/stores/theme'
import { useUIStore } from '~/stores/ui'
import HeaderNavLinks from '~/components/molecules/HeaderNavLinks.vue'
import UserAvatarButton from '~/components/molecules/UserAvatarButton.vue'
import LanguageSwitcher from '~/components/LanguageSwitcher.vue'
import Container from '~/components/atoms/Container.vue'
import NotificationBadge from '~/components/atoms/NotificationBadge.vue'
import Button from '~/components/atoms/Button.vue'

const route = useRoute()
const { t } = useI18n()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const uiStore = useUIStore()

const isUserMenuOpen = ref(false)
const username = computed(() => authStore.user?.username || authStore.user?.name || 'User')
const userMenuContainer = ref<HTMLElement | null>(null)

const navLinks = computed(() => {
  const links = [
    { to: '/', label: t('appHeader.dashboard') },
    { to: '/hackathons', label: t('appHeader.hackathons') },
    { to: '/projects', label: t('appHeader.projects') },
  ]

  return links
})

const toggleTheme = () => {
  themeStore.toggleTheme()
}

const handleLogout = async () => {
  await authStore.logout()
  isUserMenuOpen.value = false
}

const closeUserMenu = () => {
  isUserMenuOpen.value = false
}

// Klick-außerhalb-Listener
const handleClickOutside = (event: MouseEvent) => {
  if (userMenuContainer.value && !userMenuContainer.value.contains(event.target as Node)) {
    closeUserMenu()
  }
}

watch(isUserMenuOpen, (newValue) => {
  if (newValue) {
    // Füge Event-Listener hinzu, mit einer kleinen Verzögerung um sofortige Auslösung zu vermeiden
    setTimeout(() => {
      document.addEventListener('click', handleClickOutside)
    }, 0)
  } else {
    document.removeEventListener('click', handleClickOutside)
  }
})

onMounted(() => {
  themeStore.initializeTheme()
})

// Aufräumen beim Unmount
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
