<template>
  <div class="settings-actions">
    <div class="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
      <!-- Left side: Status indicators -->
      <div class="flex items-center gap-4">
        <!-- Auto-save indicator -->
        <div v-if="autoSaveEnabled" class="flex items-center gap-2">
          <div 
            class="w-2 h-2 rounded-full"
            :class="{
              'bg-green-500 animate-pulse': isSaving,
              'bg-green-500': !isSaving && hasUnsavedChanges,
              'bg-gray-400': !hasUnsavedChanges
            }"
          ></div>
          <span class="text-sm text-gray-600 dark:text-gray-400">
            {{ autoSaveStatusText }}
          </span>
        </div>

        <!-- Last saved time -->
        <div v-if="lastSavedAt" class="text-sm text-gray-500 dark:text-gray-500">
          Zuletzt gespeichert: {{ formatTime(lastSavedAt) }}
        </div>
      </div>

      <!-- Right side: Action buttons -->
      <div class="flex flex-wrap gap-3">
        <!-- Reset button -->
        <button
          v-if="hasUnsavedChanges"
          type="button"
          @click="handleReset"
          class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-gray-900 transition-colors"
          :disabled="isSaving"
        >
          Zurücksetzen
        </button>

        <!-- Save button (only shown when auto-save is disabled) -->
        <button
          v-if="!autoSaveEnabled && hasUnsavedChanges"
          type="button"
          @click="handleSave"
          class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-gray-900 transition-colors"
          :disabled="isSaving"
        >
          <span v-if="isSaving" class="flex items-center gap-2">
            <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Speichern...
          </span>
          <span v-else>
            Speichern
          </span>
        </button>

        <!-- Auto-save toggle -->
        <button
          type="button"
          @click="toggleAutoSave"
          class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-gray-900 transition-colors flex items-center gap-2"
        >
          <svg v-if="autoSaveEnabled" class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <svg v-else class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          {{ autoSaveEnabled ? 'Auto-Save an' : 'Auto-Save aus' }}
        </button>

        <!-- Export button -->
        <button
          type="button"
          @click="handleExport"
          class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-gray-900 transition-colors flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          Exportieren
        </button>
      </div>
    </div>

    <!-- Error message -->
    <div v-if="error" class="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
      <div class="flex items-start gap-3">
        <svg class="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <div>
          <p class="text-sm font-medium text-red-800 dark:text-red-300">
            Fehler beim Speichern
          </p>
          <p class="text-sm text-red-700 dark:text-red-400 mt-1">
            {{ error }}
          </p>
        </div>
      </div>
    </div>

    <!-- Success message -->
    <div v-if="successMessage" class="mt-4 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
      <div class="flex items-start gap-3">
        <svg class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <div>
          <p class="text-sm font-medium text-green-800 dark:text-green-300">
            Erfolgreich gespeichert
          </p>
          <p class="text-sm text-green-700 dark:text-green-400 mt-1">
            {{ successMessage }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

interface Props {
  hasUnsavedChanges: boolean
  isSaving: boolean
  autoSaveEnabled: boolean
  lastSavedAt?: string
  error?: string
  successMessage?: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  save: []
  reset: []
  'toggle-auto-save': [enabled: boolean]
  export: []
}>()

const autoSaveStatusText = computed(() => {
  if (props.isSaving) return 'Speichern...'
  if (props.hasUnsavedChanges) return 'Ungespeicherte Änderungen'
  return 'Alle Änderungen gespeichert'
})

const formatTime = (dateString: string) => {
  try {
    const date = new Date(dateString)
    return date.toLocaleTimeString('de-DE', {
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateString
  }
}

const handleSave = () => {
  emit('save')
}

const handleReset = () => {
  emit('reset')
}

const toggleAutoSave = () => {
  emit('toggle-auto-save', !props.autoSaveEnabled)
}

const handleExport = () => {
  emit('export')
}
</script>

<style scoped>
.settings-actions {
  @apply mt-8 pt-6 border-t border-gray-200 dark:border-gray-700;
}
</style>