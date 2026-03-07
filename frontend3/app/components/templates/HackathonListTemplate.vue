<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header Section -->
    <header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <div class="container mx-auto px-4 py-6">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 class="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
              Hackathons
            </h1>
            <p class="text-gray-600 dark:text-gray-400 mt-1">
              Entdecke spannende Hackathons und nimm an innovativen Projekten teil
            </p>
          </div>
          
          <div class="flex items-center gap-3">
            <Button
              variant="primary"
              size="lg"
              @click="emit('create-hackathon')"
              class="whitespace-nowrap"
            >
              <Icon name="plus" class="w-5 h-5 mr-2" />
              Hackathon erstellen
            </Button>
            
            <Button
              variant="outline"
              size="lg"
              @click="emit('refresh')"
              :loading="loading"
            >
              <Icon name="refresh-cw" class="w-5 h-5 mr-2" />
              Aktualisieren
            </Button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <!-- Filters and Search Section -->
      <div class="mb-8">
        <HackathonFilterBar
          :initial-search="filters.search"
          :initial-status="filters.status"
          :initial-location="filters.location"
          :initial-sort="filters.sort"
          @search="handleSearch"
          @status-change="handleStatusChange"
          @location-change="handleLocationChange"
          @sort-change="handleSortChange"
          @clear-filters="handleClearFilters"
        />
      </div>

      <!-- Sort Options -->
      <div class="mb-6">
        <HackathonSortOptions
          v-model="filters.sort"
          v-model:direction="filters.direction"
          @change="handleSortChange"
        />
      </div>

      <!-- Content Area -->
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Left Sidebar (Filters on large screens) -->
        <aside class="lg:col-span-1">
          <div class="sticky top-6 space-y-6">
            <!-- Status Filter -->
            <Card class="p-4">
              <h3 class="font-semibold text-gray-900 dark:text-white mb-3">
                Status
              </h3>
              <div class="space-y-2">
                <Checkbox
                  v-for="status in statusOptions"
                  :key="status.value"
                  v-model="selectedStatuses"
                  :value="status.value"
                  :label="status.label"
                  :badge="status.count"
                />
              </div>
            </Card>

            <!-- Location Filter -->
            <Card class="p-4">
              <h3 class="font-semibold text-gray-900 dark:text-white mb-3">
                Veranstaltungsort
              </h3>
              <div class="space-y-2">
                <Checkbox
                  v-for="location in locationOptions"
                  :key="location.value"
                  v-model="selectedLocations"
                  :value="location.value"
                  :label="location.label"
                  :badge="location.count"
                />
              </div>
            </Card>

            <!-- Date Range Filter -->
            <Card class="p-4">
              <h3 class="font-semibold text-gray-900 dark:text-white mb-3">
                Zeitraum
              </h3>
              <DateRangePicker
                v-model="dateRange"
                @change="handleDateRangeChange"
              />
            </Card>
          </div>
        </aside>

        <!-- Main Content Area -->
        <div class="lg:col-span-3">
          <!-- Loading State -->
          <div v-if="loading" class="space-y-4">
            <Skeleton v-for="i in 3" :key="i" class="h-48 w-full" />
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="text-center py-12">
            <Alert variant="error" :title="error.title" :message="error.message">
              <template #actions>
                <Button @click="emit('retry')" variant="outline">
                  Erneut versuchen
                </Button>
              </template>
            </Alert>
          </div>

          <!-- Empty State -->
          <div v-else-if="hackathons.length === 0" class="text-center py-12">
            <EmptyState
              title="Keine Hackathons gefunden"
              description="Es wurden keine Hackathons gefunden, die deinen Filterkriterien entsprechen."
              icon="search"
            >
              <template #actions>
                <Button @click="handleClearFilters" variant="primary">
                  Filter zurücksetzen
                </Button>
                <Button @click="emit('create-hackathon')" variant="outline">
                  Hackathon erstellen
                </Button>
              </template>
            </EmptyState>
          </div>

          <!-- Hackathon List -->
          <div v-else class="space-y-6">
            <!-- Stats Summary -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <StatItem
                v-for="stat in stats"
                :key="stat.label"
                :label="stat.label"
                :value="stat.value"
                :icon="stat.icon"
                :trend="stat.trend"
              />
            </div>

            <!-- Hackathon Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <HackathonListCard
                v-for="hackathon in hackathons"
                :key="hackathon.id"
                :hackathon="hackathon"
                @click="emit('select-hackathon', hackathon)"
                @register="emit('register', hackathon)"
                @share="emit('share', hackathon)"
              />
            </div>

            <!-- Pagination -->
            <div v-if="pagination && pagination.totalPages > 1" class="mt-8">
              <Pagination
                :current-page="pagination.currentPage"
                :total-pages="pagination.totalPages"
                :total-items="pagination.totalItems"
                @page-change="handlePageChange"
              />
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="mt-12 border-t border-gray-200 dark:border-gray-700 py-6">
      <div class="container mx-auto px-4 text-center text-gray-600 dark:text-gray-400">
        <p>Zeigt {{ hackathons.length }} von {{ pagination?.totalItems || 0 }} Hackathons</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import Icon from '~/components/atoms/Icon.vue'
import Button from '~/components/atoms/Button.vue'

interface Hackathon {
  id: string | number
  title: string
  description: string
  status: string
  location: string
  startDate: string
  endDate: string
  participants: number
  prize: string
  image?: string
}

interface Stat {
  label: string
  value: string | number
  icon: string
  trend?: 'up' | 'down' | 'neutral'
}

interface Pagination {
  currentPage: number
  totalPages: number
  totalItems: number
  itemsPerPage: number
}

interface Props {
  hackathons?: Hackathon[]
  loading?: boolean
  error?: {
    title: string
    message: string
  }
  pagination?: Pagination
  stats?: Stat[]
  initialFilters?: {
    search?: string
    status?: string
    location?: string
    sort?: string
    direction?: 'asc' | 'desc'
  }
}

interface Emits {
  (e: 'search', value: string): void
  (e: 'status-change', value: string): void
  (e: 'location-change', value: string): void
  (e: 'sort-change', payload: { sort: string; direction: 'asc' | 'desc' }): void
  (e: 'date-range-change', payload: { start: Date | null; end: Date | null }): void
  (e: 'page-change', page: number): void
  (e: 'select-hackathon', hackathon: Hackathon): void
  (e: 'register', hackathon: Hackathon): void
  (e: 'share', hackathon: Hackathon): void
  (e: 'create-hackathon'): void
  (e: 'refresh'): void
  (e: 'retry'): void
  (e: 'clear-filters'): void
}

const props = withDefaults(defineProps<Props>(), {
  hackathons: () => [],
  loading: false,
  error: undefined,
  pagination: undefined,
  stats: () => [
    { label: 'Aktive Hackathons', value: 0, icon: 'activity', trend: 'up' },
    { label: 'Teilnehmer gesamt', value: 0, icon: 'users', trend: 'up' },
    { label: 'Preisgeld gesamt', value: '€0', icon: 'award', trend: 'neutral' }
  ],
  initialFilters: () => ({
    search: '',
    status: 'all',
    location: 'all',
    sort: 'newest',
    direction: 'desc'
  })
})

const emit = defineEmits<Emits>()

// Filters
const filters = ref({
  search: props.initialFilters.search || '',
  status: props.initialFilters.status || 'all',
  location: props.initialFilters.location || 'all',
  sort: props.initialFilters.sort || 'newest',
  direction: props.initialFilters.direction || 'desc'
})

// Multi-select filters
const selectedStatuses = ref<string[]>([])
const selectedLocations = ref<string[]>([])
const dateRange = ref<{ start: Date | null; end: Date | null }>({
  start: null,
  end: null
})

// Filter options
const statusOptions = computed(() => [
  { value: 'upcoming', label: 'Bevorstehend', count: 12 },
  { value: 'active', label: 'Aktiv', count: 8 },
  { value: 'past', label: 'Vergangen', count: 24 }
])

const locationOptions = computed(() => [
  { value: 'virtual', label: 'Virtual', count: 18 },
  { value: 'physical', label: 'Vor Ort', count: 14 },
  { value: 'hybrid', label: 'Hybrid', count: 12 }
])

// Event handlers
function handleSearch(value: string) {
  filters.value.search = value
  emit('search', value)
}

function handleStatusChange(value: string) {
  filters.value.status = value
  emit('status-change', value)
}

function handleLocationChange(value: string) {
  filters.value.location = value
  emit('location-change', value)
}

function handleSortChange(payload: { sort: string; direction: 'asc' | 'desc' }) {
  filters.value.sort = payload.sort
  filters.value.direction = payload.direction
  emit('sort-change', payload)
}

function handleDateRangeChange(range: { start: Date | null; end: Date | null }) {
  dateRange.value = range
  emit('date-range-change', range)
}

function handlePageChange(page: number) {
  emit('page-change', page)
}

function handleClearFilters() {
  filters.value = {
    search: '',
    status: 'all',
    location: 'all',
    sort: 'newest',
    direction: 'desc'
  }
  selectedStatuses.value = []
  selectedLocations.value = []
  dateRange.value = { start: null, end: null }
  emit('clear-filters')
}

// Watch for multi-select changes
watch(selectedStatuses, (newStatuses) => {
  if (newStatuses.length === 0) {
    filters.value.status = 'all'
  } else if (newStatuses.length === 1) {
    filters.value.status = newStatuses[0] || 'all'
  } else {
    filters.value.status = 'multiple'
  }
  emit('status-change', filters.value.status)
})

watch(selectedLocations, (newLocations) => {
  if (newLocations.length === 0) {
    filters.value.location = 'all'
  } else if (newLocations.length === 1) {
    filters.value.location = newLocations[0] || 'all'
  } else {
    filters.value.location = 'multiple'
  }
  emit('location-change', filters.value.location)
})
</script>

<style scoped>
/* Additional styling if needed */
</style>