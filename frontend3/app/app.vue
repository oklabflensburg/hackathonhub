<template>
  <div :class="themeStore.isDark ? 'dark' : ''">
    <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200 overflow-x-hidden">
      <AppHeader />
      <div class="flex">
        <AppSidebar />
        <main class="flex-1 container mx-auto px-3 sm:px-4 md:px-6 py-6 sm:py-8 pb-20 lg:pb-6">
          <NuxtPage />
        </main>
      </div>
      <MobileBottomNav />
      <AppFooter />
      <NotificationContainer />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useThemeStore } from '~/stores/theme'
import { useAuthStore } from '~/stores/auth'
import AppHeader from '~/components/AppHeader.vue'
import AppSidebar from '~/components/AppSidebar.vue'
import AppFooter from '~/components/AppFooter.vue'
import NotificationContainer from '~/components/NotificationContainer.vue'
import MobileBottomNav from '~/components/MobileBottomNav.vue'

const themeStore = useThemeStore()
const authStore = useAuthStore()

// Initialize theme from localStorage or system preference
onMounted(() => {
  themeStore.initializeTheme()
  authStore.initializeAuth()
})
</script>