<template>
  <header class="sticky top-0 z-50 bg-white/95 dark:bg-gray-900/95 backdrop-blur-lg border-b border-gray-200/50 dark:border-gray-800/50 shadow-soft">
    <div class="container mx-auto px-3 sm:px-4 py-3 sm:py-4">
      <div class="flex items-center justify-between">
        <!-- Logo -->
        <div class="flex items-center space-x-3 sm:space-x-4">
          <button
            @click="toggleSidebar"
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 lg:hidden transition-colors duration-200"
            aria-label="Toggle sidebar"
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
              <h1 class="text-lg sm:text-xl font-bold text-gray-900 dark:text-white">Hackathon Hub</h1>
              <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">Build. Collaborate. Win.</p>
            </div>
            <div class="sm:hidden">
              <h1 class="text-lg font-bold text-gray-900 dark:text-white">HH</h1>
            </div>
          </NuxtLink>
        </div>

        <!-- Desktop Navigation -->
        <nav class="hidden lg:flex items-center space-x-8">
          <NuxtLink 
            to="/" 
            class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors"
            :class="{ 'text-primary-600 dark:text-primary-400': route.path === '/' }"
          >
            Dashboard
          </NuxtLink>
          <NuxtLink 
            to="/hackathons" 
            class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors"
            :class="{ 'text-primary-600 dark:text-primary-400': route.path === '/hackathons' }"
          >
            Hackathons
          </NuxtLink>
          <NuxtLink 
            to="/projects" 
            class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors"
            :class="{ 'text-primary-600 dark:text-primary-400': route.path === '/projects' }"
          >
            Projects
          </NuxtLink>
          <NuxtLink 
            to="/create" 
            class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors"
            :class="{ 'text-primary-600 dark:text-primary-400': route.path === '/create' }"
          >
            Create
          </NuxtLink>

          <!-- User-specific navigation (only shown when authenticated) -->

        </nav>

        <!-- Right Side Actions -->
        <div class="flex items-center space-x-2 sm:space-x-4">
          <!-- Theme Toggle -->
          <button
            @click="toggleTheme"
            class="p-1.5 sm:p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
            :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
            aria-label="Toggle theme"
          >
            <span class="text-lg sm:text-xl">{{ themeIcon }}</span>
          </button>

          <!-- User Menu -->
          <div v-if="isAuthenticated" class="relative">
            <button
              @click="toggleUserMenu"
              class="flex items-center space-x-1 sm:space-x-3 p-1.5 sm:p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
              aria-label="User menu"
            >
              <div class="relative">
                <div v-if="authStore.user?.avatar_url" class="w-8 h-8 sm:w-10 sm:h-10 rounded-full overflow-hidden border-2 border-white dark:border-gray-800 shadow-sm">
                  <img
                    :src="authStore.user.avatar_url"
                    :alt="username"
                    class="w-full h-full object-cover"
                    @error="handleAvatarError"
                  />
                </div>
                <div v-else class="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center border-2 border-white dark:border-gray-800 shadow-sm">
                  <span class="text-primary-600 dark:text-primary-300 font-bold text-sm sm:text-base">
                    {{ userInitials }}
                  </span>
                </div>
              </div>
              <div class="hidden md:block text-left">
                <p class="font-medium text-gray-900 dark:text-white text-sm sm:text-base">{{ username }}</p>
                <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">View profile</p>
              </div>
              <svg
                class="w-4 h-4 sm:w-5 sm:h-5 text-gray-500 dark:text-gray-400 transition-transform"
                :class="{ 'rotate-180': userMenuOpen }"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <!-- Dropdown Menu -->
            <div
              v-if="userMenuOpen"
              class="absolute right-0 mt-2 w-48 sm:w-56 md:w-64 bg-white dark:bg-gray-800 rounded-xl shadow-elevated border border-gray-200 dark:border-gray-700 py-2 z-50 animate-slide-in glass-effect"
            >
              <div class="px-3 sm:px-4 py-2 sm:py-3 border-b border-gray-100 dark:border-gray-700">
                <p class="font-medium text-gray-900 dark:text-white text-sm sm:text-base">{{ username }}</p>
                <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 truncate">{{ userEmail }}</p>
              </div>
              
              <div @click="userMenuOpen = false">
                <NuxtLink
                  to="/profile"
                  class="flex items-center px-3 sm:px-4 py-2 sm:py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm sm:text-base"
                >
                  <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2 sm:mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  My Profile
                </NuxtLink>
              </div>
              
              <div @click="userMenuOpen = false">
                <NuxtLink
                  to="/my-projects"
                  class="flex items-center px-3 sm:px-4 py-2 sm:py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm sm:text-base"
                >
                  <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2 sm:mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                  My Projects
                </NuxtLink>
              </div>
              
              <div @click="userMenuOpen = false">
                <NuxtLink
                  to="/my-votes"
                  class="flex items-center px-3 sm:px-4 py-2 sm:py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm sm:text-base"
                >
                  <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2 sm:mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                  </svg>
                  My Votes
                </NuxtLink>
              </div>
              
              <div class="border-t border-gray-100 dark:border-gray-700 mt-2 pt-2">
                <button
                  @click="handleLogout"
                  class="flex items-center w-full px-3 sm:px-4 py-2 sm:py-3 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors text-sm sm:text-base"
                >
                  <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2 sm:mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Logout
                </button>
              </div>
            </div>
          </div>

          <!-- Login Button -->
          <button
            v-else
            @click="loginWithGitHub"
            :disabled="isLoading"
            class="btn btn-primary flex items-center space-x-1 sm:space-x-2 px-3 py-1.5 sm:px-4 sm:py-2 text-sm sm:text-base"
          >
            <svg v-if="isLoading" class="w-4 h-4 sm:w-5 sm:h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            <svg v-else class="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
            </svg>
            <span class="hidden sm:inline">Login with GitHub</span>
            <span class="sm:hidden">Login</span>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useThemeStore } from '~/stores/theme'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useRoute } from '#imports'

const themeStore = useThemeStore()
const authStore = useAuthStore()
const uiStore = useUIStore()
const route = useRoute()

const userMenuOpen = ref(false)

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
  authStore.loginWithGitHub()
}

const handleLogout = async () => {
  await authStore.logout()
  userMenuOpen.value = false
  uiStore.showSuccess('Successfully logged out')
}
</script>