<template>
  <ClientOnly>
    <header
      :key="`header-${isAuthenticated ? 'auth' : 'unauth'}`"
      class="sticky top-0 z-50 bg-white/95 dark:bg-gray-900/95 backdrop-blur-lg border-b border-gray-200/50 dark:border-gray-800/50 shadow-soft">
      <div class="container mx-auto px-3 sm:px-4 py-3 sm:py-4">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <div class="flex items-center space-x-3 sm:space-x-4">
            <button @click="toggleSidebar"
              class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 lg:hidden transition-colors duration-200"
              :aria-label="t('appHeader.toggleSidebar')">
              <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>

            <NuxtLink to="/" class="flex items-center space-x-2 sm:space-x-3 group">
              <div
                class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center shadow-md group-hover:shadow-lg transition-shadow duration-200">
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

          <!-- Desktop Navigation -->
          <nav class="hidden lg:flex items-center space-x-8">
            <NuxtLink to="/"
              class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors"
              :class="{ 'text-primary-600 dark:text-primary-400': route.path === '/' }">
              {{ t('appHeader.dashboard') }}
            </NuxtLink>
            <NuxtLink to="/hackathons"
              class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors"
              :class="{ 'text-primary-600 dark:text-primary-400': route.path === '/hackathons' }">
              {{ $t('appHeader.hackathons') }}
            </NuxtLink>
            <NuxtLink to="/projects"
              class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors"
              :class="{ 'text-primary-600 dark:text-primary-400': route.path === '/projects' }">
              {{ $t('appHeader.projects') }}
            </NuxtLink>
            <NuxtLink to="/create"
              class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors"
              :class="{ 'text-primary-600 dark:text-primary-400': route.path === '/create' }">
              {{ $t('appHeader.create') }}
            </NuxtLink>

            <!-- User-specific navigation (only shown when authenticated) -->

          </nav>

          <!-- Right Side Actions -->
          <div class="flex items-center space-x-2 sm:space-x-4">
            <!-- Theme Toggle -->
            <button @click="toggleTheme"
              class="p-1.5 sm:p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
              :title="isDark ? $t('appHeader.switchToLightMode') : $t('appHeader.switchToDarkMode')"
              :aria-label="$t('appHeader.toggleTheme')">
              <span class="text-lg sm:text-xl">{{ themeIcon }}</span>
            </button>

            <!-- Language Switcher -->
            <LanguageSwitcher />

            <!-- User Menu -->
            <div v-if="isAuthenticated" class="relative">
              <!-- Debug info -->
              <div class="hidden">
                isAuthenticated: {{ isAuthenticated }}, user: {{ authStore.user?.username }}, token: {{ authStore.token ? 'present' : 'null' }}
              </div>
              <button @click="toggleUserMenu"
                class="flex items-center space-x-1 sm:space-x-3 p-1.5 sm:p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
                :aria-label="$t('appHeader.userMenu')">
                <div class="relative">
                  <div v-if="authStore.user?.avatar_url"
                    class="w-8 h-8 sm:w-10 sm:h-10 rounded-full overflow-hidden border-2 border-white dark:border-gray-800 shadow-sm">
                    <img :src="authStore.user.avatar_url" :alt="username" class="w-full h-full object-cover"
                      @error="handleAvatarError" />
                  </div>
                  <div v-else
                    class="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center border-2 border-white dark:border-gray-800 shadow-sm">
                    <span class="text-primary-600 dark:text-primary-300 font-bold text-sm sm:text-base">
                      {{ userInitials }}
                    </span>
                  </div>
                </div>
                <div class="hidden md:block text-left">
                  <p class="font-medium text-gray-900 dark:text-white text-sm sm:text-base">{{ username }}</p>
                  <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">{{ $t('appHeader.viewProfile') }}</p>
                </div>
                <svg class="w-4 h-4 sm:w-5 sm:h-5 text-gray-500 dark:text-gray-400 transition-transform"
                  :class="{ 'rotate-180': userMenuOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- Dropdown Menu -->
              <div v-if="userMenuOpen"
                class="absolute right-0 mt-2 w-48 sm:w-56 md:w-64 bg-white dark:bg-gray-800 rounded-xl shadow-elevated border border-gray-200 dark:border-gray-700 py-2 z-50 animate-slide-in glass-effect">
                <div class="px-3 sm:px-4 py-2 sm:py-3 border-b border-gray-100 dark:border-gray-700">
                  <p class="font-medium text-gray-900 dark:text-white text-sm sm:text-base">{{ username }}</p>
                  <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 truncate">{{ userEmail }}</p>
                </div>

                <div @click="userMenuOpen = false">
                  <NuxtLink to="/profile"
                    class="flex items-center px-3 sm:px-4 py-2 sm:py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm sm:text-base">
                    <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2 sm:mr-3" fill="none" stroke="currentColor"
                      viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    {{ $t('appHeader.myProfile') }}
                  </NuxtLink>
                </div>

                <div @click="userMenuOpen = false">
                  <NuxtLink to="/my-projects"
                    class="flex items-center px-3 sm:px-4 py-2 sm:py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm sm:text-base">
                    <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2 sm:mr-3" fill="none" stroke="currentColor"
                      viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    {{ $t('appHeader.myProjects') }}
                  </NuxtLink>
                </div>

                <div @click="userMenuOpen = false">
                  <NuxtLink to="/my-votes"
                    class="flex items-center px-3 sm:px-4 py-2 sm:py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm sm:text-base">
                    <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2 sm:mr-3" fill="none" stroke="currentColor"
                      viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                    </svg>
                    {{ $t('appHeader.myVotes') }}
                  </NuxtLink>
                </div>

                <div class="border-t border-gray-100 dark:border-gray-700 mt-2 pt-2">
                  <button @click="handleLogout"
                    class="flex items-center w-full px-3 sm:px-4 py-2 sm:py-3 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors text-sm sm:text-base">
                    <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2 sm:mr-3" fill="none" stroke="currentColor"
                      viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    {{ $t('appHeader.logout') }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Login Dropdown -->
            <div v-else class="relative">
              <button @click="toggleLoginDropdown" :disabled="isLoading"
                class="btn btn-primary flex items-center space-x-1 sm:space-x-2 px-3 py-1.5 sm:px-4 sm:py-2 text-sm sm:text-base">
                <svg v-if="isLoading" class="w-4 h-4 sm:w-5 sm:h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                <svg v-else class="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path
                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                </svg>
                <span class="hidden sm:inline">{{ $t('appHeader.login') }}</span>
                <span class="sm:hidden">{{ $t('appHeader.login') }}</span>
                <svg class="w-4 h-4 ml-1 transition-transform" :class="{ 'rotate-180': loginDropdownOpen }" fill="none"
                  stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- Login Dropdown Menu -->
              <div v-if="loginDropdownOpen"
                class="absolute right-0 mt-2 w-48 sm:w-56 bg-white dark:bg-gray-800 rounded-xl shadow-elevated border border-gray-200 dark:border-gray-700 py-2 z-50 animate-slide-in glass-effect">
                <div class="px-4 py-2 border-b border-gray-100 dark:border-gray-700">
                  <p class="font-medium text-gray-900 dark:text-white text-sm">{{ $t('appHeader.loginOptions') }}</p>
                </div>

                <button @click="loginWithGitHub"
                  class="flex items-center w-full px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm">
                  <svg class="w-5 h-5 mr-3" viewBox="0 0 24 24" fill="currentColor">
                    <path
                      d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                  </svg>
                  {{ $t('appHeader.loginWithGitHub') }}
                </button>

                <button @click="loginWithGoogle"
                  class="flex items-center w-full px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm">
                  <svg class="w-5 h-5 mr-3" viewBox="0 0 24 24">
                    <path fill="#4285F4"
                      d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                    <path fill="#34A853"
                      d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                    <path fill="#FBBC05"
                      d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                    <path fill="#EA4335"
                      d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                  </svg>
                  {{ $t('appHeader.loginWithGoogle') }}
                </button>

                <div class="border-t border-gray-100 dark:border-gray-700 mt-2 pt-2">
                  <NuxtLink to="/login" @click="loginDropdownOpen = false"
                    class="flex items-center w-full px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    {{ $t('appHeader.loginWithEmail') }}
                  </NuxtLink>
                </div>

                <div class="border-t border-gray-100 dark:border-gray-700 mt-2 pt-2">
                  <NuxtLink to="/register" @click="loginDropdownOpen = false"
                    class="flex items-center w-full px-4 py-3 text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors text-sm font-medium">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                    {{ $t('appHeader.createAccount') }}
                  </NuxtLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  </ClientOnly>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useThemeStore } from '~/stores/theme'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useRoute } from '#imports'

const themeStore = useThemeStore()
const authStore = useAuthStore()
const uiStore = useUIStore()
const route = useRoute()
const { t } = useI18n()

const userMenuOpen = ref(false)
const loginDropdownOpen = ref(false)

// Computed properties
const isDark = computed(() => themeStore.isDark)
const themeIcon = computed(() => themeStore.icon)
const isAuthenticated = computed(() => authStore.isAuthenticated)
const userInitials = computed(() => authStore.userInitials)
const username = computed(() => authStore.user?.username || '')
const userEmail = computed(() => authStore.user?.email || '')
const isLoading = computed(() => authStore.isLoading)

// Methods
const toggleSidebar = () => {
  uiStore.toggleSidebar()
}

const toggleTheme = () => {
  themeStore.toggleTheme()
}

const toggleUserMenu = () => {
  userMenuOpen.value = !userMenuOpen.value
}

const toggleLoginDropdown = () => {
  loginDropdownOpen.value = !loginDropdownOpen.value
}

// Debug: Watch authentication state changes
watch(isAuthenticated, (newVal, oldVal) => {
  console.log('[AppHeader] Authentication state changed:', { old: oldVal, new: newVal })
  console.log('[AppHeader] User:', authStore.user)
  console.log('[AppHeader] Token:', authStore.token ? 'present' : 'null')
})

// Also watch user and token directly
watch(() => authStore.user, (newVal, oldVal) => {
  console.log('[AppHeader] User changed:', { old: oldVal?.username, new: newVal?.username })
}, { deep: true })

watch(() => authStore.token, (newVal, oldVal) => {
  console.log('[AppHeader] Token changed:', { old: oldVal ? 'present' : 'null', new: newVal ? 'present' : 'null' })
})

const closeUserMenu = (event?: Event) => {
  userMenuOpen.value = false
}

const handleAvatarError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  // The parent div will show the fallback initials automatically
  // because we're using v-if/v-else
}

const loginWithGitHub = () => {
  loginDropdownOpen.value = false
  authStore.loginWithGitHub()
}

const loginWithGoogle = () => {
  loginDropdownOpen.value = false
  authStore.loginWithGoogle()
}

const handleLogout = async () => {
  await authStore.logout()
  userMenuOpen.value = false
  uiStore.showSuccess('Successfully logged out')
}
</script>