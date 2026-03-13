<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200 overflow-x-hidden">
    <GlobalNotifications />
    <AppHeader />
    <div class="flex">
      <AppSidebar />
      <main class="flex-1">
        <Container class="px-3 sm:px-4 md:px-6 py-6 sm:py-8 pb-20 lg:pb-6" :size="'2xl'">
          <NuxtPage />
        </Container>
      </main>
    </div>
    <MobileBottomNav />
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import AppHeader from '~/components/AppHeader.vue'
import AppSidebar from '~/components/AppSidebar.vue'
import AppFooter from '~/components/AppFooter.vue'
import MobileBottomNav from '~/components/MobileBottomNav.vue'
import Container from '~/components/atoms/Container.vue'
import GlobalNotifications from '~/components/GlobalNotifications.vue'

const authStore = useAuthStore()
const themeCookie = useCookie<'light' | 'dark' | null>('theme')
const ssrTheme = computed(() => themeCookie.value === 'dark' ? 'dark' : 'light')

useHead(() => ({
  htmlAttrs: {
    class: ssrTheme.value === 'dark' ? 'dark' : undefined,
    'data-theme': ssrTheme.value
  }
}))

onMounted(async () => {
  await authStore.initializeAuth()
})
</script>
