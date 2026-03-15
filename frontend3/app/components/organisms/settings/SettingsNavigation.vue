<template>
  <nav class="settings-navigation" aria-label="Settings navigation">
    <div class="xl:hidden">
      <div class="rounded-2xl border border-gray-200 bg-white/90 p-3 shadow-sm backdrop-blur dark:border-gray-700 dark:bg-gray-900/80">
        <div class="mb-3 flex items-start justify-between gap-3 px-1">
          <div>
            <h2 class="text-base font-semibold text-gray-900 dark:text-gray-100">
              Einstellungen
            </h2>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              Wähle einen Bereich
            </p>
          </div>
          <div class="flex items-center rounded-full bg-gray-100 px-2.5 py-1 text-xs text-gray-600 dark:bg-gray-800 dark:text-gray-300">
            <div
              class="mr-2 h-2 w-2 rounded-full"
              :class="hasUnsavedChanges ? 'bg-yellow-500 animate-pulse' : 'bg-green-500'"
            />
            <span>{{ hasUnsavedChanges ? 'Offen' : 'Gespeichert' }}</span>
          </div>
        </div>

        <div class="scroll-strip -mx-1 flex gap-2 overflow-x-auto px-1 pb-1">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            type="button"
            :class="[
              'min-w-max rounded-xl border px-3 py-2 text-sm font-medium transition-colors',
              'focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-primary-500/20',
              activeTab === tab.id
                ? 'border-primary-200 bg-primary-50 text-primary-700 dark:border-primary-800 dark:bg-primary-900/30 dark:text-primary-300'
                : 'border-gray-200 bg-gray-50 text-gray-700 hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800/70 dark:text-gray-300 dark:hover:bg-gray-800'
            ]"
            @click="$emit('tab-change', tab.id)"
          >
            <span class="flex items-center gap-2">
              <component
                :is="tab.icon"
                class="h-4 w-4"
                :class="activeTab === tab.id ? 'text-primary-500' : 'text-gray-400 dark:text-gray-500'"
              />
              <span>{{ tab.label }}</span>
            </span>
          </button>
        </div>
      </div>
    </div>

    <div class="hidden xl:block">
      <div class="rounded-3xl border border-gray-200 bg-white/90 p-5 shadow-sm backdrop-blur dark:border-gray-700 dark:bg-gray-900/80">
        <div class="mb-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
            Einstellungen
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            Verwalte deine Kontoeinstellungen und Präferenzen
          </p>
        </div>

        <ul class="space-y-1.5">
          <li v-for="tab in tabs" :key="tab.id">
            <button
              type="button"
              :class="[
                'w-full flex items-center px-3 py-2.5 text-sm font-medium rounded-xl transition-colors',
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

        <div class="mt-8 rounded-2xl border border-dashed border-gray-200 bg-gray-50/80 p-4 dark:border-gray-700 dark:bg-gray-800/40">
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
  @apply w-full;
}

.scroll-strip {
  scrollbar-width: none;
}

.scroll-strip::-webkit-scrollbar {
  display: none;
}
</style>
