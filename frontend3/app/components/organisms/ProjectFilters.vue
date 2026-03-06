<template>
  <div class="project-filters" :class="filtersClasses">
    <!-- Filters Header -->
    <div class="filters-header mb-6">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
            {{ title }}
          </h3>
          <p
            v-if="subtitle"
            class="mt-1 text-sm text-gray-500 dark:text-gray-400"
          >
            {{ subtitle }}
          </p>
        </div>
        
        <div class="flex items-center gap-3">
          <!-- Active Filters Count -->
          <div
            v-if="showActiveCount && activeFilterCount > 0"
            class="active-filters-count inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300"
          >
            <span class="mr-1">{{ activeFilterCount }}</span>
            active
          </div>
          
          <!-- Clear All Button -->
          <button
            v-if="showClearAll && activeFilterCount > 0"
            type="button"
            class="clear-all-button text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300 focus:outline-none"
            @click="handleClearAll"
          >
            Clear all
          </button>
          
          <!-- Toggle Button (Mobile) -->
          <button
            v-if="collapsible"
            type="button"
            class="toggle-button md:hidden p-2 -mr-2 text-gray-400 dark:text-gray-500 hover:text-gray-500 dark:hover:text-gray-400 focus:outline-none"
            :aria-label="isCollapsed ? 'Expand filters' : 'Collapse filters'"
            @click="toggleCollapsed"
          >
            <svg
              class="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                v-if="isCollapsed"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 9l-7 7-7-7"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 15l7-7 7 7"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Filters Content -->
    <div
      v-if="!isCollapsed"
      class="filters-content"
    >
      <!-- Search Filter -->
      <div
        v-if="showSearch"
        class="filter-section mb-6"
      >
        <ProjectFilterItem
          v-model="searchValue"
          type="search"
          label="Search projects"
          placeholder="Search by title, description, or tags..."
          :show-label="showFilterLabels"
          :show-search-icon="true"
          :show-clear-button="true"
          size="md"
          variant="filled"
          @input="handleSearchInput"
          @clear="handleSearchClear"
          @enter="handleSearchEnter"
        />
      </div>
      
      <!-- Status Filter -->
      <div
        v-if="showStatusFilter && statusOptions.length > 0"
        class="filter-section mb-6"
      >
        <ProjectFilterItem
          v-model="statusValue"
          type="checkbox"
          label="Status"
          :options="statusOptions"
          :show-label="showFilterLabels"
          :show-selected-values="true"
          :show-clear-button="true"
          size="md"
          @change="handleStatusChange"
          @clear="handleStatusClear"
        />
      </div>
      
      <!-- Technology Filter -->
      <div
        v-if="showTechnologyFilter && technologyOptions.length > 0"
        class="filter-section mb-6"
      >
        <ProjectFilterItem
          v-model="technologyValue"
          type="checkbox"
          label="Technologies"
          :options="technologyOptions"
          :show-label="showFilterLabels"
          :show-selected-values="true"
          :show-clear-button="true"
          size="md"
          @change="handleTechnologyChange"
          @clear="handleTechnologyClear"
        />
      </div>
      
      <!-- Tag Filter -->
      <div
        v-if="showTagFilter && tagOptions.length > 0"
        class="filter-section mb-6"
      >
        <ProjectFilterItem
          v-model="tagValue"
          type="checkbox"
          label="Tags"
          :options="tagOptions"
          :show-label="showFilterLabels"
          :show-selected-values="true"
          :show-clear-button="true"
          size="md"
          @change="handleTagChange"
          @clear="handleTagClear"
        />
      </div>
      
      <!-- Date Range Filter -->
      <div
        v-if="showDateFilter"
        class="filter-section mb-6"
      >
        <div class="date-range-filter">
          <div class="flex items-center justify-between mb-2">
            <label class="text-sm font-medium text-gray-700 dark:text-gray-300">
              Date Range
            </label>
            <button
              v-if="dateFrom || dateTo"
              type="button"
              class="text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
              @click="handleDateClear"
            >
              Clear
            </button>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <ProjectFilterItem
              v-model="dateFrom"
              type="date"
              label="From"
              :show-label="false"
              placeholder="Start date"
              size="md"
              @change="handleDateFromChange"
            />
            <ProjectFilterItem
              v-model="dateTo"
              type="date"
              label="To"
              :show-label="false"
              placeholder="End date"
              size="md"
              @change="handleDateToChange"
            />
          </div>
        </div>
      </div>
      
      <!-- Team Size Filter -->
      <div
        v-if="showTeamSizeFilter"
        class="filter-section mb-6"
      >
        <ProjectFilterItem
          v-model="teamSizeValue"
          type="range"
          label="Team Size"
          :min="teamSizeMin"
          :max="teamSizeMax"
          :step="1"
          :show-label="showFilterLabels"
          size="md"
          @change="handleTeamSizeChange"
        />
        <div class="mt-2 text-xs text-gray-500 dark:text-gray-400">
          {{ teamSizeLabel }}
        </div>
      </div>
      
      <!-- Sort Options -->
      <div
        v-if="showSortOptions"
        class="filter-section mb-6"
      >
        <ProjectSortOptionComponent
          v-model="sortValue"
          v-model:sort-direction="sortDirection"
          :label="sortLabel"
          :show-label="showFilterLabels"
          :show-direction-toggle="true"
          :show-selected-display="true"
          :show-clear-button="true"
          size="md"
          @change="handleSortChange"
          @clear="handleSortClear"
        />
      </div>
      
      <!-- Apply/Cancel Buttons -->
      <div
        v-if="showApplyButtons"
        class="filter-actions mt-8 pt-6 border-t border-gray-200 dark:border-gray-800"
      >
        <div class="flex gap-3">
          <button
            type="button"
            class="apply-button flex-1 px-4 py-2.5 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="!hasChanges"
            @click="handleApply"
          >
            Apply Filters
          </button>
          <button
            type="button"
            class="cancel-button flex-1 px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
            @click="handleCancel"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
    
    <!-- Collapsed State -->
    <div
      v-else
      class="collapsed-state p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700"
    >
      <p class="text-sm text-gray-600 dark:text-gray-400 text-center">
        {{ activeFilterCount > 0 
          ? `${activeFilterCount} active filter${activeFilterCount !== 1 ? 's' : ''} applied` 
          : 'No filters applied' 
        }}
      </p>
      <button
        v-if="activeFilterCount > 0"
        type="button"
        class="mt-2 w-full text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
        @click="handleClearAll"
      >
        Clear all filters
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { ProjectStatus, ProjectTechnology } from '../../types/project-types'
import { ProjectSortOption } from '../../types/project-types'
import ProjectFilterItem from '../molecules/ProjectFilterItem.vue'
import ProjectSortOptionComponent from '../molecules/ProjectSortOption.vue'

interface FilterOption {
  value: string
  label: string
  count?: number
  disabled?: boolean
}

interface Props {
  /** Filter-Titel */
  title?: string
  /** Filter-Subtitle */
  subtitle?: string
  /** Collapsible (für Mobile) */
  collapsible?: boolean
  /** Initial collapsed state */
  initialCollapsed?: boolean
  /** Filter-Labels anzeigen */
  showFilterLabels?: boolean
  /** Active Count anzeigen */
  showActiveCount?: boolean
  /** Clear All Button anzeigen */
  showClearAll?: boolean
  /** Apply Buttons anzeigen */
  showApplyButtons?: boolean
  
  // Filter Visibility
  showSearch?: boolean
  showStatusFilter?: boolean
  showTechnologyFilter?: boolean
  showTagFilter?: boolean
  showDateFilter?: boolean
  showTeamSizeFilter?: boolean
  showSortOptions?: boolean
  
  // Filter Options
  statusOptions?: FilterOption[]
  technologyOptions?: FilterOption[]
  tagOptions?: FilterOption[]
  sortOptions?: any[] // Wird von ProjectSortOption verwendet
  
  // Team Size Range
  teamSizeMin?: number
  teamSizeMax?: number
  
  // Initial Values
  initialSearch?: string
  initialStatus?: string[]
  initialTechnologies?: string[]
  initialTags?: string[]
  initialDateFrom?: string
  initialDateTo?: string
  initialTeamSize?: number
  initialSort?: ProjectSortOption | null
  initialSortDirection?: 'asc' | 'desc'
  
  // Sort Label
  sortLabel?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Filters',
  subtitle: '',
  collapsible: true,
  initialCollapsed: false,
  showFilterLabels: true,
  showActiveCount: true,
  showClearAll: true,
  showApplyButtons: false,
  
  showSearch: true,
  showStatusFilter: true,
  showTechnologyFilter: true,
  showTagFilter: true,
  showDateFilter: true,
  showTeamSizeFilter: true,
  showSortOptions: true,
  
  statusOptions: () => [
    { value: 'active', label: 'Active', count: 0 },
    { value: 'draft', label: 'Draft', count: 0 },
    { value: 'completed', label: 'Completed', count: 0 },
    { value: 'archived', label: 'Archived', count: 0 },
    { value: 'under_review', label: 'Under Review', count: 0 },
  ],
  technologyOptions: () => [],
  tagOptions: () => [],
  
  teamSizeMin: 1,
  teamSizeMax: 10,
  
  initialSearch: '',
  initialStatus: () => [],
  initialTechnologies: () => [],
  initialTags: () => [],
  initialDateFrom: '',
  initialDateTo: '',
  initialTeamSize: 1,
  initialSort: null,
  initialSortDirection: 'desc',
  
  sortLabel: 'Sort by',
})

const emit = defineEmits<{
  (e: 'search', value: string): void
  (e: 'status-change', values: string[]): void
  (e: 'technology-change', values: string[]): void
  (e: 'tag-change', values: string[]): void
  (e: 'date-change', from: string, to: string): void
  (e: 'team-size-change', value: number): void
  (e: 'sort-change', sortBy: ProjectSortOption | null, direction: 'asc' | 'desc'): void
  (e: 'apply'): void
  (e: 'cancel'): void
  (e: 'clear-all'): void
}>()

// Reactive State
const isCollapsed = ref(props.initialCollapsed)
const searchValue = ref(props.initialSearch)
const statusValue = ref<string[]>(props.initialStatus)
const technologyValue = ref<string[]>(props.initialTechnologies)
const tagValue = ref<string[]>(props.initialTags)
const dateFrom = ref(props.initialDateFrom)
const dateTo = ref(props.initialDateTo)
const teamSizeValue = ref(props.initialTeamSize)
const sortValue = ref<ProjectSortOption | null>(props.initialSort)
const sortDirection = ref<'asc' | 'desc'>(props.initialSortDirection)

// Computed Properties
const filtersClasses = computed(() => {
  const classes: string[] = []
  
  if (props.collapsible) {
    classes.push('collapsible-filters')
  }
  
  return classes.join(' ')
})

const activeFilterCount = computed(() => {
  let count = 0
  
  if (searchValue.value) count++
  if (statusValue.value.length > 0) count++
  if (technologyValue.value.length > 0) count++
  if (tagValue.value.length > 0) count++
  if (dateFrom.value || dateTo.value) count++
  if (teamSizeValue.value !== props.teamSizeMin) count++
  if (sortValue.value) count++
  
  return count
})

const hasChanges = computed(() => {
  return activeFilterCount.value > 0
})

const teamSizeLabel = computed(() => {
  if (teamSizeValue.value === props.teamSizeMin) {
    return 'Any team size'
  }
  return `Up to ${teamSizeValue.value} members`
})

// Methods
const toggleCollapsed = () => {
  isCollapsed.value = !isCollapsed.value
}

const handleSearchInput = (value: string) => {
  searchValue.value = value
  emit('search', value)
}

const handleSearchClear = () => {
  searchValue.value = ''
  emit('search', '')
}

const handleSearchEnter = (value: string) => {
  emit('search', value)
}

const handleStatusClear = () => {
  statusValue.value = []
  emit('status-change', [])
}

const handleTechnologyClear = () => {
  technologyValue.value = []
  emit('technology-change', [])
}

const handleTagClear = () => {
  tagValue.value = []
  emit('tag-change', [])
}

const handleDateClear = () => {
  dateFrom.value = ''
  dateTo.value = ''
  emit('date-change', '', '')
}



const handleSortClear = () => {
  sortValue.value = null
  sortDirection.value = 'desc'
  emit('sort-change', null, 'desc')
}

const handleApply = () => {
  emit('apply')
}

const handleCancel = () => {
  // Reset to initial values
  searchValue.value = props.initialSearch
  statusValue.value = [...props.initialStatus]
  technologyValue.value = [...props.initialTechnologies]
  tagValue.value = [...props.initialTags]
  dateFrom.value = props.initialDateFrom
  dateTo.value = props.initialDateTo
  teamSizeValue.value = props.initialTeamSize
  sortValue.value = props.initialSort
  sortDirection.value = props.initialSortDirection
  
  emit('cancel')
}

const handleClearAll = () => {
  searchValue.value = ''
  statusValue.value = []
  technologyValue.value = []
  tagValue.value = []
  dateFrom.value = ''
  dateTo.value = ''
  teamSizeValue.value = props.teamSizeMin
  sortValue.value = null
  sortDirection.value = 'desc'
  
  emit('clear-all')
}

// Type-safe event handlers for ProjectFilterItem
const handleStatusChange = (value: string | number | string[] | number[] | null) => {
  const values = Array.isArray(value) ? value.map(v => String(v)) : []
  statusValue.value = values
  emit('status-change', values)
}

const handleTechnologyChange = (value: string | number | string[] | number[] | null) => {
  const values = Array.isArray(value) ? value.map(v => String(v)) : []
  technologyValue.value = values
  emit('technology-change', values)
}

const handleTagChange = (value: string | number | string[] | number[] | null) => {
  const values = Array.isArray(value) ? value.map(v => String(v)) : []
  tagValue.value = values
  emit('tag-change', values)
}

const handleDateFromChange = (value: string | number | string[] | number[] | null) => {
  dateFrom.value = typeof value === 'string' ? value : ''
  emit('date-change', dateFrom.value, dateTo.value)
}

const handleDateToChange = (value: string | number | string[] | number[] | null) => {
  dateTo.value = typeof value === 'string' ? value : ''
  emit('date-change', dateFrom.value, dateTo.value)
}

const handleTeamSizeChange = (value: string | number | string[] | number[] | null) => {
  const numValue = typeof value === 'number' ? value : props.teamSizeMin
  teamSizeValue.value = numValue
  emit('team-size-change', numValue)
}

const handleSortChange = (value: { sortBy: ProjectSortOption | null, direction: 'asc' | 'desc' }) => {
  sortValue.value = value.sortBy
  sortDirection.value = value.direction
  emit('sort-change', value.sortBy, value.direction)
}
</script>

<style scoped>
.project-filters {
  transition: all 0.2s ease-in-out;
}

.collapsible-filters {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

@media (prefers-color-scheme: dark) {
  .collapsible-filters {
    border-color: #374151;
    background-color: #1f2937;
  }
}

.filter-section:last-child {
  margin-bottom: 0;
}

.date-range-filter {
  background-color: #f9fafb;
  padding: 1rem;
  border-radius: 0.5rem;
}

@media (prefers-color-scheme: dark) {
  .date-range-filter {
    background-color: #374151;
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .collapsible-filters {
    padding: 1rem;
  }
  
  .filters-header {
    margin-bottom: 1rem;
  }
}

/* Animation for collapsible state */
.filters-content {
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>