<template>
  <section class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
    <div class="mb-4 flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
      <div class="min-w-0 flex-1">
        <h3 class="text-sm font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">
          Filter
        </h3>
        <div class="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-12">
          <label class="block lg:col-span-6">
            <span class="mb-1 block text-xs font-medium text-gray-600 dark:text-gray-300">Suche</span>
            <div class="relative">
              <svg class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                v-model="localFilters.search"
                type="text"
                class="w-full rounded-lg border border-gray-300 bg-white py-2 pl-9 pr-3 text-sm text-gray-900 outline-none transition focus:border-primary-500 focus:ring-2 focus:ring-primary-100 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:ring-primary-950"
                placeholder="Benachrichtigungen durchsuchen"
                @input="updateFilters"
              />
            </div>
          </label>

          <label class="block lg:col-span-3">
            <span class="mb-1 block text-xs font-medium text-gray-600 dark:text-gray-300">Sortieren</span>
            <select
              v-model="localFilters.sortBy"
              class="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 outline-none transition focus:border-primary-500 focus:ring-2 focus:ring-primary-100 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:ring-primary-950"
              @change="updateFilters"
            >
              <option value="createdAt">Datum</option>
              <option value="type">Typ</option>
            </select>
          </label>

          <label class="block lg:col-span-3">
            <span class="mb-1 block text-xs font-medium text-gray-600 dark:text-gray-300">Reihenfolge</span>
            <select
              v-model="localFilters.sortDirection"
              class="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 outline-none transition focus:border-primary-500 focus:ring-2 focus:ring-primary-100 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:ring-primary-950"
              @change="updateFilters"
            >
              <option value="desc">Neueste zuerst</option>
              <option value="asc">Aelteste zuerst</option>
            </select>
          </label>
        </div>
      </div>

      <button
        v-if="showReset"
        class="inline-flex h-10 items-center justify-center rounded-lg border border-gray-300 px-3 text-sm font-medium text-gray-700 transition hover:bg-gray-50 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-800"
        @click="resetFilters"
      >
        Zuruecksetzen
      </button>
    </div>

    <div class="grid gap-4 lg:grid-cols-2">
      <div class="rounded-lg bg-gray-50 p-3 dark:bg-gray-800/60">
        <div class="mb-2 flex items-center justify-between">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white">Typ</h4>
          <span class="text-xs text-gray-500 dark:text-gray-400">{{ selectedTypeCount }} aktiv</span>
        </div>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="type in notificationTypes"
            :key="type.value"
            type="button"
            :class="[
              'inline-flex items-center gap-2 rounded-md border px-2.5 py-1.5 text-xs font-medium transition',
              isTypeSelected(type.value)
                ? 'border-primary-500 bg-primary-50 text-primary-700 dark:border-primary-500 dark:bg-primary-950/40 dark:text-primary-200'
                : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-gray-800'
            ]"
            @click="toggleType(type.value)"
          >
            <span>{{ type.label }}</span>
            <span v-if="type.count !== undefined" class="text-[11px] opacity-70">{{ type.count }}</span>
          </button>
        </div>
      </div>

      <div class="rounded-lg bg-gray-50 p-3 dark:bg-gray-800/60">
        <div class="mb-2 flex items-center justify-between">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white">Status</h4>
          <span class="text-xs text-gray-500 dark:text-gray-400">{{ selectedStatusCount }} aktiv</span>
        </div>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="status in notificationStatuses"
            :key="status.value"
            type="button"
            :class="[
              'inline-flex items-center gap-2 rounded-md border px-2.5 py-1.5 text-xs font-medium transition',
              isStatusSelected(status.value)
                ? 'border-primary-500 bg-primary-50 text-primary-700 dark:border-primary-500 dark:bg-primary-950/40 dark:text-primary-200'
                : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-gray-800'
            ]"
            @click="toggleStatus(status.value)"
          >
            <span>{{ status.label }}</span>
            <span v-if="status.count !== undefined" class="text-[11px] opacity-70">{{ status.count }}</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="activeFilterCount > 0" class="mt-4 border-t border-gray-200 pt-3 dark:border-gray-800">
      <div class="mb-2 flex items-center justify-between">
        <h4 class="text-sm font-medium text-gray-900 dark:text-white">Aktive Filter</h4>
        <span class="text-xs text-gray-500 dark:text-gray-400">{{ activeFilterCount }}</span>
      </div>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="filter in activeFilters"
          :key="filter.id"
          class="inline-flex items-center gap-2 rounded-md bg-gray-100 px-2.5 py-1 text-xs text-gray-700 dark:bg-gray-800 dark:text-gray-300"
        >
          {{ filter.label }}
          <button
            type="button"
            class="inline-flex h-4 w-4 items-center justify-center rounded-full text-gray-500 transition hover:bg-gray-200 hover:text-gray-800 dark:hover:bg-gray-700 dark:hover:text-white"
            @click="removeFilter(filter)"
          >
            <span class="sr-only">Entfernen</span>
            <svg class="h-2.5 w-2.5" stroke="currentColor" fill="none" viewBox="0 0 8 8">
              <path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6m0-6L1 7" />
            </svg>
          </button>
        </span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import {
  NotificationStatus,
  NotificationType
} from '~/types/notification-types'
import type {
  NotificationFilterOptions,
  NotificationSortDirection,
  NotificationSortField
} from '~/types/notification-types'

interface NotificationFiltersProps {
  filters: NotificationFilterOptions
  sortField?: NotificationSortField
  sortDirection?: NotificationSortDirection
  availableTypes?: Array<'all' | NotificationType>
  availableStatuses?: Array<'all' | NotificationStatus>
  showReset?: boolean
  typeCounts?: Partial<Record<NotificationType, number>>
  statusCounts?: Partial<Record<NotificationStatus, number>>
}

const props = withDefaults(defineProps<NotificationFiltersProps>(), {
  showReset: true,
  typeCounts: () => ({}),
  statusCounts: () => ({})
})

const emit = defineEmits<{
  'update:filters': [filters: NotificationFilterOptions]
  'update-filters': [filters: NotificationFilterOptions]
  'update-sort': [field: NotificationSortField, direction: NotificationSortDirection]
  'reset': []
  'reset-filters': []
}>()

const localFilters = ref<NotificationFilterOptions>({
  ...props.filters,
  type: props.filters.type ? [...props.filters.type] : [],
  status: props.filters.status ? [...props.filters.status] : [],
  search: props.filters.search || '',
  sortBy: props.filters.sortBy || 'createdAt',
  sortDirection: props.filters.sortDirection || 'desc'
})

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

const notificationTypes = computed<Array<{ value: NotificationType; label: string; count?: number }>>(() => [
  { value: NotificationType.SYSTEM, label: 'System', count: props.typeCounts[NotificationType.SYSTEM] },
  { value: NotificationType.TEAM_INVITATION, label: 'Team', count: props.typeCounts[NotificationType.TEAM_INVITATION] },
  { value: NotificationType.PROJECT_COMMENT, label: 'Projekt', count: props.typeCounts[NotificationType.PROJECT_COMMENT] },
  { value: NotificationType.HACKATHON_REGISTRATION, label: 'Hackathon', count: props.typeCounts[NotificationType.HACKATHON_REGISTRATION] },
  { value: NotificationType.COMMENT_REPLY, label: 'Kommentar', count: props.typeCounts[NotificationType.COMMENT_REPLY] },
  { value: NotificationType.PROJECT_VOTE, label: 'Abstimmung', count: props.typeCounts[NotificationType.PROJECT_VOTE] },
  { value: NotificationType.NEWSLETTER, label: 'Ankuendigung', count: props.typeCounts[NotificationType.NEWSLETTER] },
  { value: NotificationType.HACKATHON_STARTING_SOON, label: 'Erinnerung', count: props.typeCounts[NotificationType.HACKATHON_STARTING_SOON] }
])

const notificationStatuses = computed<Array<{ value: NotificationStatus; label: string; count?: number }>>(() => [
  { value: NotificationStatus.UNREAD, label: 'Ungelesen', count: props.statusCounts[NotificationStatus.UNREAD] },
  { value: NotificationStatus.READ, label: 'Gelesen', count: props.statusCounts[NotificationStatus.READ] },
  { value: NotificationStatus.ARCHIVED, label: 'Archiviert', count: props.statusCounts[NotificationStatus.ARCHIVED] }
])

const activeFilters = computed(() => {
  const filters: Array<{ id: string; label: string; type: 'search' | 'type' | 'status' }> = []

  if (localFilters.value.search) {
    filters.push({ id: 'search', label: `Suche: "${localFilters.value.search}"`, type: 'search' })
  }

  if (localFilters.value.type?.length) {
    localFilters.value.type.forEach(type => {
      const typeLabel = notificationTypes.value.find(t => t.value === type)?.label || type
      filters.push({ id: `type-${type}`, label: `Typ: ${typeLabel}`, type: 'type' })
    })
  }

  if (localFilters.value.status?.length) {
    localFilters.value.status.forEach(status => {
      const statusLabel = notificationStatuses.value.find(s => s.value === status)?.label || status
      filters.push({ id: `status-${status}`, label: `Status: ${statusLabel}`, type: 'status' })
    })
  }

  return filters
})

const activeFilterCount = computed(() => activeFilters.value.length)
const selectedTypeCount = computed(() => localFilters.value.type?.length || 0)
const selectedStatusCount = computed(() => localFilters.value.status?.length || 0)

const updateFilters = () => {
  emit('update:filters', { ...localFilters.value })
  emit('update-filters', { ...localFilters.value })
  const sortField: NotificationSortField =
    localFilters.value.sortBy === 'priority' || localFilters.value.sortBy === 'type'
      ? localFilters.value.sortBy
      : 'createdAt'
  emit('update-sort', sortField, localFilters.value.sortDirection || 'desc')
}

const resetFilters = () => {
  localFilters.value = {
    type: [],
    status: [],
    search: '',
    sortBy: 'createdAt',
    sortDirection: 'desc'
  }
  emit('reset')
  emit('reset-filters')
  updateFilters()
}

const isTypeSelected = (value: NotificationType) => (localFilters.value.type || []).includes(value)
const isStatusSelected = (value: NotificationStatus) => (localFilters.value.status || []).includes(value)

const toggleType = (value: NotificationType) => {
  const current = localFilters.value.type || []
  localFilters.value.type = current.includes(value)
    ? current.filter(type => type !== value)
    : [...current, value]
  updateFilters()
}

const toggleStatus = (value: NotificationStatus) => {
  const current = localFilters.value.status || []
  localFilters.value.status = current.includes(value)
    ? current.filter(status => status !== value)
    : [...current, value]
  updateFilters()
}

const removeFilter = (filter: { id: string, type: string }) => {
  switch (filter.type) {
    case 'search':
      localFilters.value.search = ''
      break
    case 'type':
      localFilters.value.type = localFilters.value.type?.filter(t => t !== filter.id.replace('type-', '') as NotificationType) || []
      break
    case 'status':
      localFilters.value.status = localFilters.value.status?.filter(s => s !== filter.id.replace('status-', '') as NotificationStatus) || []
      break
  }
  updateFilters()
}
</script>
