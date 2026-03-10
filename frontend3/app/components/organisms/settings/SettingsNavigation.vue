<template>
  <nav class="settings-navigation" aria-label="Settings navigation">
    <div class="mb-6">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
        Einstellungen
      </h2>
       <p class="text-sm text-gray-500 dark:text-gray-400">
        Verwalte deine Kontoeinstellungen und Präferenzen
      </p>
    </div>
    
    <ul class="space-y-1">
      <li v-for="tab in tabs" :key="tab.id">
        <button
          type="button"
          :class="[
            'w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
            'focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-primary-500/20',
            activeTab === tab.id
              ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300'
              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
          ]"
          @click="$emit('tab-change', tab.id)"
        >
          <component
            :is="tab.icon"
            class="w-5 h-5 mr-3"
            :class="activeTab === tab.id ? 'text-primary-500' : 'text-gray-400 dark:text-gray-500'"
          />
          <span class="flex-1 text-left">{{ tab.label }}</span>
          <span
            v-if="tab.badge"
            class="ml-2 px-2 py-0.5 text-xs font-medium rounded-full"
            :class="[
              tab.badge.type === 'info' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' :
              tab.badge.type === 'warning' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
              tab.badge.type === 'success' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
              'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
            ]"
          >
            {{ tab.badge.text }}
          </span>
        </button>
      </li>
    </ul>
    
    <div class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
      <div class="px-3">
        <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">
          Letzte Änderung: {{ lastUpdated }}
        </p>
        <div class="flex items-center text-xs text-gray-500 dark:text-gray-400">
          <div
            class="w-2 h-2 rounded-full mr-2"
            :class="hasUnsavedChanges ? 'bg-yellow-500 animate-pulse' : 'bg-green-500'"
          />
          <span>{{ hasUnsavedChanges ? 'Ungespeicherte Änderungen' : 'Alle Änderungen gespeichert' }}</span>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { User, ShieldCheck, Bell, Lock, Settings as SettingsIcon } from 'lucide-vue-next'

interface TabBadge {
  text: string
  type: 'info' | 'warning' | 'success' | 'neutral'
}

interface SettingsTab {
  id: string
  label: string
  icon: any // Vue component
  description?: string
  badge?: TabBadge
}

interface Props {
  activeTab: string
  hasUnsavedChanges?: boolean
  lastUpdated?: string
}

withDefaults(defineProps<Props>(), {
  hasUnsavedChanges: false,
  lastUpdated: 'Vor 2 Stunden'
})

defineEmits<{
  'tab-change': [tabId: string]
}>()

const tabs: SettingsTab[] = [
  {
    id: 'profile',
    label: 'Profil',
    icon: User,
    description: 'Persönliche Informationen und Kontaktdaten'
  },
  {
    id: 'security',
    label: 'Sicherheit',
    icon: ShieldCheck,
    description: 'Passwort, 2FA und Sitzungen',
    badge: {
      text: '2FA empfohlen',
      type: 'warning'
    }
  },
  {
    id: 'notifications',
    label: 'Benachrichtigungen',
    icon: Bell,
    description: 'Email, Push und In-App Benachrichtigungen'
  },
  {
    id: 'privacy',
    label: 'Datenschutz',
    icon: Lock,
    description: 'Privatsphäre und Datenfreigabe'
  },
  {
    id: 'platform',
    label: 'Plattform',
    icon: SettingsIcon,
    description: 'Erscheinungsbild und Sprache'
  }
]
</script>

<style scoped>
.settings-navigation {
  @apply w-full md:w-64;
}
</style>