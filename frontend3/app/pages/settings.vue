<template>
  <div class="settings-page">
    <!-- Breadcrumb Navigation -->
    <nav class="mb-6">
      <ol class="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
        <li>
          <NuxtLink to="/" class="hover:text-gray-900 dark:hover:text-gray-300 transition-colors">
            Startseite
          </NuxtLink>
        </li>
        <li class="flex items-center">
          <svg class="w-4 h-4 mx-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
          </svg>
        </li>
        <li class="text-gray-900 dark:text-gray-300 font-medium">
          Einstellungen
        </li>
      </ol>
    </nav>

    <!-- Settings Page Template -->
    <SettingsPageTemplate />

    <!-- Help Section -->
    <div class="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
            Benötigst du Hilfe?
          </h3>
          <p class="text-gray-600 dark:text-gray-400">
            Lies unsere Dokumentation oder kontaktiere unseren Support.
          </p>
        </div>
        <div class="flex flex-wrap gap-3">
          <NuxtLink
            to="/help/settings"
            class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          >
            Dokumentation
          </NuxtLink>
          <NuxtLink
            to="/support"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 transition-colors"
          >
            Support kontaktieren
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import SettingsPageTemplate from '~/components/templates/settings/SettingsPageTemplate.vue'

// Set page metadata
useHead({
  title: 'Einstellungen - Hackathon Hub',
  meta: [
    {
      name: 'description',
      content: 'Verwalte deine Kontoeinstellungen, Benachrichtigungen, Datenschutz und Plattformpräferenzen.'
    }
  ]
})

// Add breadcrumb structured data
useSeoMeta({
  ogTitle: 'Einstellungen - Hackathon Hub',
  ogDescription: 'Verwalte deine Kontoeinstellungen, Benachrichtigungen, Datenschutz und Plattformpräferenzen.',
  ogType: 'website'
})
</script>

<style scoped>
.settings-page {
  @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8;
}
</style>