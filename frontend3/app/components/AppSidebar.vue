<template>
  <!-- Mobile Sidebar Overlay -->
  <div
    v-if="sidebarOpen"
    class="fixed inset-0 z-40 lg:hidden"
    @click="closeSidebar"
  >
    <div class="absolute inset-0 bg-black/50" />
  </div>

  <!-- Sidebar -->
  <aside
    :class="[
      'fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 transform transition-transform duration-300 ease-in-out lg:hidden',
      sidebarOpen ? 'translate-x-0' : '-translate-x-full'
    ]"
  >
    <div class="h-full flex flex-col">
      <!-- Sidebar Header -->
      <div class="p-6 border-b border-gray-200 dark:border-gray-800">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ t('sidebar.navigation') }}
          </h2>
          <button
            @click="closeSidebar"
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 lg:hidden"
            :aria-label="t('sidebar.close')"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Sidebar Content -->
      <div class="flex-1 overflow-y-auto p-6">
        <nav class="space-y-2">
          <NuxtLink
            to="/"
            @click="closeSidebar"
            class="flex items-center space-x-3 p-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            :class="{ 'bg-gray-100 dark:bg-gray-800 text-primary-600 dark:text-primary-400': route.path === '/' }"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            <span>{{ t('navigation.dashboard') }}</span>
          </NuxtLink>

          <NuxtLink
            to="/hackathons"
            @click="closeSidebar"
            class="flex items-center space-x-3 p-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            :class="{ 'bg-gray-100 dark:bg-gray-800 text-primary-600 dark:text-primary-400': route.path.startsWith('/hackathons') }"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            <span>{{ t('navigation.hackathons') }}</span>
          </NuxtLink>

          <NuxtLink
            to="/projects"
            @click="closeSidebar"
            class="flex items-center space-x-3 p-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            :class="{ 'bg-gray-100 dark:bg-gray-800 text-primary-600 dark:text-primary-400': route.path.startsWith('/projects') }"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <span>{{ t('navigation.projects') }}</span>
          </NuxtLink>

          <NuxtLink
            v-if="isAuthenticated"
            to="/create"
            @click="closeSidebar"
            class="flex items-center space-x-3 p-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            :class="{ 'bg-gray-100 dark:bg-gray-800 text-primary-600 dark:text-primary-400': route.path === '/create' }"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>{{ t('navigation.create') }}</span>
          </NuxtLink>

          <div v-if="isAuthenticated" class="pt-6 border-t border-gray-200 dark:border-gray-800 space-y-2">
            <NuxtLink
              to="/profile"
              @click="closeSidebar"
              class="flex items-center space-x-3 p-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              :class="{ 'bg-gray-100 dark:bg-gray-800 text-primary-600 dark:text-primary-400': route.path === '/profile' }"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span>{{ t('navigation.myProfile') }}</span>
            </NuxtLink>

            <NuxtLink
              to="/my-projects"
              @click="closeSidebar"
              class="flex items-center space-x-3 p-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              :class="{ 'bg-gray-100 dark:bg-gray-800 text-primary-600 dark:text-primary-400': route.path === '/my-projects' }"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              <span>{{ t('navigation.myProjects') }}</span>
            </NuxtLink>

            <NuxtLink
              to="/my-votes"
              @click="closeSidebar"
              class="flex items-center space-x-3 p-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              :class="{ 'bg-gray-100 dark:bg-gray-800 text-primary-600 dark:text-primary-400': route.path === '/my-votes' }"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
              </svg>
              <span>{{ t('navigation.myVotes') }}</span>
            </NuxtLink>
          </div>
        </nav>
      </div>

      <!-- Sidebar Footer -->
      <div v-if="isAuthenticated" class="p-6 border-t border-gray-200 dark:border-gray-800">
        <div class="flex items-center space-x-3 mb-4">
          <div v-if="authStore.user?.avatar_url" class="w-10 h-10 rounded-full overflow-hidden">
            <img
              :src="authStore.user.avatar_url"
              :alt="username"
              class="w-full h-full object-cover"
            />
          </div>
          <div v-else class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center">
            <span class="text-primary-600 dark:text-primary-300 font-bold">
              {{ userInitials }}
            </span>
          </div>
          <div>
            <p class="font-medium text-gray-900 dark:text-white">{{ username }}</p>
            <p class="text-sm text-gray-500 dark:text-gray-400 truncate">{{ userEmail }}</p>
          </div>
        </div>
        <button
          @click="handleLogout"
          class="flex items-center justify-center w-full p-3 rounded-lg text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors border border-red-200 dark:border-red-800"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          {{ t('appHeader.logout') }}
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUIStore } from '~/stores/ui'
import { useAuthStore } from '~/stores/auth'
import { useRoute } from '#imports'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const uiStore = useUIStore()
const authStore = useAuthStore()
const route = useRoute()

const sidebarOpen = computed(() => uiStore.sidebarOpen)
const isAuthenticated = computed(() => authStore.isAuthenticated)
const username = computed(() => authStore.user?.username || '')
const userEmail = computed(() => authStore.user?.email || '')
const userInitials = computed(() => authStore.userInitials)

const closeSidebar = () => {
  uiStore.closeSidebar()
}

const handleLogout = async () => {
  await authStore.logout()
  closeSidebar()
  uiStore.showSuccess('Successfully logged out')
}
</script>