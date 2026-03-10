<template>
  <div class="notification-filters">
    <!-- Filter Header -->
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-medium text-gray-900 dark:text-white">
        Filter
      </h3>
      <button
        v-if="showReset"
        class="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
        @click="resetFilters"
      >
        Zurücksetzen
      </button>
    </div>

    <!-- Search Input -->
    <div class="mb-6">
      <label for="search" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
        Suche
      </label>
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input
          id="search"
          v-model="localFilters.search"
          type="text"
          class="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Nach Benachrichtigungen suchen..."
          @input="updateFilters"
        />
      </div>
    </div>

    <!-- Type Filters -->
    <div class="mb-6">
      <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
        Typ
      </h4>
      <div class="space-y-2">
        <label
          v-for="type in notificationTypes"
          :key="type.value"
          class="flex items-center"
        >
          <input
            v-model="localFilters.type"
            type="checkbox"
            :value="type.value"
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded"
            @change="updateFilters"
          />
          <span class="ml-3 text-sm text-gray-700 dark:text-gray-300">
            {{ type.label }}
          </span>
          <span
            v-if="type.count !== undefined"
            class="ml-auto text-xs text-gray-500 dark:text-gray-400"
          >
            {{ type.count }}
          </span>
        </label>
      </div>
    </div>

    <!-- Status Filters -->
    <div class="mb-6">
      <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
        Status
      </h4>
      <div class="space-y-2">
        <label
          v-for="status in notificationStatuses"
          :key="status.value"
          class="flex items-center"
        >
          <input
            v-model="localFilters.status"
            type="checkbox"
            :value="status.value"
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded"
            @change="updateFilters"
          />
          <span class="ml-3 text-sm text-gray-700 dark:text-gray-300">
            {{ status.label }}
          </span>
          <span
            v-if="status.count !== undefined"
            class="ml-auto text-xs text-gray-500 dark:text-gray-400"
          >
            {{ status.count }}
          </span>
        </label>
      </div>
    </div>

    <!-- Sort Options -->
    <div class="mb-6">
      <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
        Sortieren nach
      </h4>
      <div class="space-y-2">
        <div>
          <select
            v-model="localFilters.sortBy"
            class="block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            @change="updateFilters"
          >
            <option value="createdAt">Erstellungsdatum</option>
            <option value="type">Typ</option>
          </select>
        </div>
        <div>
          <select
            v-model="localFilters.sortDirection"
            class="block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            @change="updateFilters"
          >
            <option value="desc">Absteigend (neueste zuerst)</option>
            <option value="asc">Aufsteigend (älteste zuerst)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Active Filters -->
    <div v-if="activeFilterCount > 0" class="mb-6">
      <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
        Aktive Filter ({{ activeFilterCount }})
      </h4>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="filter in activeFilters"
          :key="filter.id"
          class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
        >
          {{ filter.label }}
          <button
            type="button"
            class="ml-1.5 inline-flex items-center justify-center h-4 w-4 rounded-full hover:bg-blue-200 dark:hover:bg-blue-800"
            @click="removeFilter(filter)"
          >
            <span class="sr-only">Entfernen</span>
            <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
              <path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6m0-6L1 7" />
            </svg>
          </button>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { NotificationFilterOptions, NotificationType, NotificationStatus } from '~/types/notification-types'

interface NotificationFiltersProps {
  filters: NotificationFilterOptions
  showReset?: boolean
  typeCounts?: Record<string, number>
  statusCounts?: Record<string, number>
}

const props = withDefaults(defineProps<NotificationFiltersProps>(), {
  showReset: true,
  typeCounts: () => ({}),
  statusCounts: () => ({})
})

const emit = defineEmits<{
  'update:filters': [filters: NotificationFilterOptions]
  'reset': []
}>()

// Local copy of filters for two-way binding
const localFilters = ref<NotificationFilterOptions>({
  ...props.filters,
  type: props.filters.type ? [...props.filters.type] : [],
  status: props.filters.status ? [...props.filters.status] : [],
  search: props.filters.search || '',
  sortBy: props.filters.sortBy || 'createdAt',
  sortDirection: props.filters.sortDirection || 'desc'
})

// Update local filters when props change
watch(() => props.filters, (newFilters) => {
  localFilters.value = {
    ...newFilters,
    type: newFilters.type ? [...newFilters.type] : [],
    status: newFilters.status ? [...newFilters.status] : [],
    search: newFilters.search || '',
    sortBy: newFilters.sortBy || 'createdAt',
    sortDirection: newFilters.sortDirection || 'desc'
  }
}, { deep: true })

// Notification types with labels
const notificationTypes = computed(() => [
  { value: 'system', label: 'System', count: props.typeCounts.system },
  { value: 'user', label: 'Benutzer', count: props.typeCounts.user },
  { value: 'project', label: 'Projekt', count: props.typeCounts.project },
  { value: 'team', label: 'Team', count: props.typeCounts.team },
  { value: 'hackathon', label: 'Hackathon', count: props.typeCounts.hackathon },
  { value: 'comment', label: 'Kommentar', count: props.typeCounts.comment },
  { value: 'vote', label: 'Abstimmung', count: props.typeCounts.vote },
  { value: 'invitation', label: 'Einladung', count: props.typeCounts.invitation },
  { value: 'announcement', label: 'Ankündigung', count: props.typeCounts.announcement },
  { value: 'reminder', label: 'Erinnerung', count: props.typeCounts.reminder }
])

// Notification statuses with labels
const notificationStatuses = computed(() => [
  { value: 'unread', label: 'Ungelesen', count: props.statusCounts.unread },
  { value: 'read', label: 'Gelesen', count: props.statusCounts.read },
  { value: 'archived', label: 'Archiviert', count: props.statusCounts.archived }
])

// Active filters for display
const activeFilters = computed(() => {
  const filters = []
  
  // Search filter
  if (localFilters.value.search) {
    filters.push({
      id: 'search',
      label: `Suche: "${localFilters.value.search}"`,
      type: 'search'
    })
  }
  
  // Type filters
  if (localFilters.value.type && localFilters.value.type.length > 0) {
    localFilters.value.type.forEach(type => {
      const typeLabel = notificationTypes.value.find(t => t.value === type)?.label || type
      filters.push({
        id: `type-${type}`,
        label: `Typ: ${typeLabel}`,
        type: 'type'
      })
    })
  }
  
  // Status filters
  if (localFilters.value.status && localFilters.value.status.length > 0) {
    localFilters.value.status.forEach(status => {
      const statusLabel = notificationStatuses.value.find(s => s.value === status)?.label || status
      filters.push({
        id: `status-${status}`,
        label: `Status: ${statusLabel}`,
        type: 'status'
      })
    })
  }
  
  return filters
})

// Count of active filters
const activeFilterCount = computed(() => activeFilters.value.length)

// Update filters and emit event
const updateFilters = () => {
  emit('update:filters', { ...localFilters.value })
}

// Reset all filters
const resetFilters = () => {
  localFilters.value = {
    type: [],
    status: [],
    search: '',
    sortBy: 'createdAt',
    sortDirection: 'desc'
  }
  emit('reset')
  emit('update:filters', { ...localFilters.value })
}

// Remove specific filter
const removeFilter = (filter: any) => {
  switch (filter.type) {
    case 'search':
      localFilters.value.search = ''
      break
    case 'type':
      localFilters.value.type = localFilters.value.type?.filter(t => t !== filter.id.replace('type-', '')) || []
      break
    case 'status':
      localFilters.value.status = localFilters.value.status?.filter(s => s !== filter.id.replace('status-', '')) || []
      break
  }
  updateFilters()
}
</script>

<style scoped>
.notification-filters {
  @apply bg-white dark:bg-gray-900 rounded-lg shadow-sm p-4;
}
</style>
