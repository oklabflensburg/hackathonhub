<template>
  <div class="projects-page-template" :class="templateClasses">
    <!-- Page Header -->
    <header v-if="showHeader" class="page-header mb-8">
      <div class="header-content">
        <h1 class="page-title text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          {{ pageTitle }}
        </h1>
        <p v-if="pageDescription" class="page-description text-lg text-gray-600 dark:text-gray-400 mb-6">
          {{ pageDescription }}
        </p>
        
        <!-- Header Actions -->
        <div v-if="showHeaderActions" class="header-actions flex flex-wrap items-center justify-between gap-4">
          <!-- Search and Filter Controls -->
          <div class="controls-left flex flex-wrap items-center gap-4">
            <!-- Search Input -->
            <div v-if="showSearch" class="search-container w-full md:w-auto">
              <div class="relative">
                <input
                  v-model="searchQuery"
                  type="search"
                  placeholder="Search projects..."
                  class="search-input pl-10 pr-4 py-2 w-full md:w-64 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  @input="handleSearch"
                />
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg
                    class="h-5 w-5 text-gray-400 dark:text-gray-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                  </svg>
                </div>
              </div>
            </div>
            
            <!-- Create Project Button -->
            <button
              v-if="showCreateButton && canCreate"
              type="button"
              class="create-button inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              @click="handleCreate"
            >
              <svg
                class="mr-2 h-4 w-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 4v16m8-8H4"
                />
              </svg>
              Create Project
            </button>
          </div>
          
          <!-- View Toggle and Sort -->
          <div v-if="showViewControls" class="controls-right flex items-center gap-3">
            <!-- View Toggle -->
            <div v-if="showViewToggle" class="view-toggle flex items-center bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
              <button
                type="button"
                class="view-button grid-view px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
                :class="viewMode === 'grid' ? 'bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 shadow-sm' : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300'"
                @click="setViewMode('grid')"
              >
                <svg
                  class="h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
                  />
                </svg>
              </button>
              <button
                type="button"
                class="view-button list-view px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
                :class="viewMode === 'list' ? 'bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 shadow-sm' : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300'"
                @click="setViewMode('list')"
              >
                <svg
                  class="h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              </button>
            </div>
            
            <!-- Sort Dropdown -->
            <div v-if="showSort" class="sort-dropdown relative">
              <button
                type="button"
                class="sort-button inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                @click="toggleSortDropdown"
              >
                <svg
                  class="mr-2 h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4"
                  />
                </svg>
                {{ sortLabel }}
                <svg
                  class="ml-2 h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>
              
              <!-- Sort Options -->
              <div
                v-if="showSortOptions"
                class="sort-options absolute right-0 mt-2 w-48 rounded-lg shadow-lg bg-white dark:bg-gray-900 ring-1 ring-black ring-opacity-5 focus:outline-none z-10"
              >
                <div class="py-1">
                  <button
                    v-for="option in sortOptions"
                    :key="option.value"
                    type="button"
                    class="w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-800"
                    :class="currentSort === option.value ? 'text-blue-600 dark:text-blue-400 font-medium' : 'text-gray-700 dark:text-gray-300'"
                    @click="handleSortChange(option.value)"
                  >
                    {{ option.label }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
    
    <!-- Main Content -->
    <div class="main-content">
      <div class="content-wrapper" :class="contentWrapperClasses">
        <!-- Filters Sidebar -->
        <aside
          v-if="showFilters"
          class="filters-sidebar"
          :class="filtersSidebarClasses"
        >
          <ProjectFilters
            v-if="showProjectFilters"
            :filters="filters"
            :sort-option="currentSort"
            @filter-change="handleFilterChange"
            @sort-change="handleSortChange"
            @clear-filters="handleClearFilters"
          />
          
          <!-- Additional Filters -->
          <div v-if="showAdditionalFilters" class="additional-filters mt-6">
            <slot name="additional-filters" />
          </div>
        </aside>
        
        <!-- Projects Content -->
        <main class="projects-content flex-1">
          <!-- Loading State -->
          <div v-if="loading" class="loading-state">
            <slot name="loading">
              <div class="flex flex-col items-center justify-center py-12">
                <div class="loading-spinner mb-4">
                  <svg
                    class="animate-spin h-8 w-8 text-blue-600 dark:text-blue-400"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    />
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                </div>
                <p class="text-gray-600 dark:text-gray-400">
                  Loading projects...
                </p>
              </div>
            </slot>
          </div>
          
          <!-- Error State -->
          <div v-else-if="error" class="error-state">
            <slot name="error" :error="error">
              <div class="error-message p-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <div class="flex items-center">
                  <svg
                    class="h-5 w-5 text-red-600 dark:text-red-400 mr-3"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <h3 class="text-lg font-medium text-red-800 dark:text-red-300">
                    Error loading projects
                  </h3>
                </div>
                <p class="mt-2 text-sm text-red-700 dark:text-red-400">
                  {{ error }}
                </p>
                <button
                  type="button"
                  class="mt-4 inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 dark:text-red-300 dark:bg-red-900/30 dark:hover:bg-red-800/40 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  @click="handleRetry"
                >
                  Try again
                </button>
              </div>
            </slot>
          </div>
          
          <!-- Empty State -->
          <div v-else-if="isEmpty" class="empty-state">
            <slot name="empty">
              <div class="empty-message flex flex-col items-center justify-center py-12 text-center">
                <svg
                  class="h-12 w-12 text-gray-400 dark:text-gray-500 mb-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                  No projects found
                </h3>
                <p class="text-gray-600 dark:text-gray-400 mb-6 max-w-md">
                  {{ emptyMessage }}
                </p>
                <button
                  v-if="showCreateButton && canCreate"
                  type="button"
                  class="create-button-empty inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  @click="handleCreate"
                >
                  <svg
                    class="mr-2 h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 4v16m8-8H4"
                    />
                  </svg>
                  Create your first project
                </button>
              </div>
            </slot>
          </div>
          
          <!-- Projects List -->
          <div v-else class="projects-list">
            <!-- Projects Grid/List -->
            <ProjectList
              :projects="projects"
              :view-mode="viewMode"
              :loading="loading"
              :empty="isEmpty"
              :error="error"
              :columns="viewMode === 'grid' ? gridColumns : 1"
              :gap="viewMode === 'grid' ? 6 : 4"
              @project-click="handleProjectClick"
              @project-vote="handleProjectVote"
              @project-comment="handleProjectComment"
              @project-share="handleProjectShare"
              @project-bookmark="handleProjectBookmark"
            />
            
            <!-- Pagination -->
            <div v-if="showPagination && totalPages > 1" class="pagination mt-8">
              <div class="flex items-center justify-between">
                <!-- Page Info -->
                <div class="page-info text-sm text-gray-700 dark:text-gray-300">
                  Showing <span class="font-medium">{{ startItem }}</span> to
                  <span class="font-medium">{{ endItem }}</span> of
                  <span class="font-medium">{{ totalItems }}</span> projects
                </div>
                
                <!-- Page Navigation -->
                <nav class="page-navigation flex items-center space-x-2">
                  <!-- Previous Button -->
                  <button
                    type="button"
                    class="previous-button inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
                    :disabled="currentPage === 1"
                    @click="handlePageChange(currentPage - 1)"
                  >
                    <svg
                      class="mr-2 h-4 w-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15 19l-7-7 7-7"
                      />
                    </svg>
                    Previous
                  </button>
                  
                  <!-- Page Numbers -->
                  <div class="page-numbers hidden sm:flex space-x-1">
                    <button
                      v-for="page in visiblePages"
                      :key="page"
                      type="button"
                      class="page-button inline-flex items-center px-3 py-2 border text-sm font-medium rounded-lg"
                      :class="page === currentPage ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' : 'border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'"
                      @click="handlePageChange(page)"
                    >
                      {{ page }}
                    </button>
                    
                    <!-- Ellipsis -->
                    <span
                      v-if="showStartEllipsis"
                      class="ellipsis inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium text-gray-500 dark:text-gray-400"
                    >
                      ...
                    </span>
                    
                    <span
                      v-if="showEndEllipsis"
                      class="ellipsis inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium text-gray-500 dark:text-gray-400"
                    >
                      ...
                    </span>
                  </div>
                  
                  <!-- Next Button -->
                  <button
                    type="button"
                    class="next-button inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
                    :disabled="currentPage === totalPages"
                    @click="handlePageChange(currentPage + 1)"
                  >
                    Next
                    <svg
                      class="ml-2 h-4 w-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
    
    <!-- Page Footer -->
    <footer v-if="showFooter" class="page-footer mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
      <slot name="footer">
        <div class="footer-content text-center text-sm text-gray-500 dark:text-gray-400">
          <p>{{ footerText }}</p>
        </div>
      </slot>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { Project, ProjectFilterOptions } from '../../types/project-types'
import ProjectList from '../organisms/ProjectList.vue'
import ProjectFilters from '../organisms/ProjectFilters.vue'

// Props
interface Props {
  // Page Configuration
  pageTitle?: string
  pageDescription?: string
  footerText?: string
  
  // Data
  projects: Project[]
  loading?: boolean
  error?: string | null
  totalItems?: number
  itemsPerPage?: number
  
  // Filters and Sorting
  filters?: ProjectFilterOptions
  sortOptions?: Array<{ value: string; label: string }>
  currentSort?: string
  
  // Configuration Flags
  showHeader?: boolean
  showHeaderActions?: boolean
  showSearch?: boolean
  showCreateButton?: boolean
  showViewControls?: boolean
  showViewToggle?: boolean
  showSort?: boolean
  showFilters?: boolean
  showProjectFilters?: boolean
  showAdditionalFilters?: boolean
  showPagination?: boolean
  showFooter?: boolean
  
  // User Permissions
  canCreate?: boolean
  
  // View Configuration
  defaultViewMode?: 'grid' | 'list'
  gridColumns?: number
  
  // Empty State
  emptyMessage?: string
  
  // Layout Variant
  variant?: 'default' | 'sidebar-left' | 'sidebar-right' | 'full-width'
}

const props = withDefaults(defineProps<Props>(), {
  pageTitle: 'Projects',
  pageDescription: '',
  footerText: 'Showing all projects',
  
  projects: () => [],
  loading: false,
  error: null,
  totalItems: 0,
  itemsPerPage: 12,
  
  filters: () => ({}),
  sortOptions: () => [
    { value: 'newest', label: 'Newest' },
    { value: 'most_viewed', label: 'Most Viewed' },
    { value: 'most_voted', label: 'Most Voted' },
    { value: 'most_commented', label: 'Most Commented' },
    { value: 'trending', label: 'Trending' },
    { value: 'deadline', label: 'Deadline' },
  ],
  currentSort: 'newest',
  
  showHeader: true,
  showHeaderActions: true,
  showSearch: true,
  showCreateButton: true,
  showViewControls: true,
  showViewToggle: true,
  showSort: true,
  showFilters: true,
  showProjectFilters: true,
  showAdditionalFilters: false,
  showPagination: true,
  showFooter: false,
  
  canCreate: false,
  
  defaultViewMode: 'grid',
  gridColumns: 3,
  
  emptyMessage: 'No projects match your filters. Try adjusting your search or filters.',
  
  variant: 'default'
})

// Emits
const emit = defineEmits<{
  search: [query: string]
  create: []
  viewModeChange: [mode: 'grid' | 'list']
  sortChange: [sortOption: string]
  filterChange: [filters: ProjectFilterOptions]
  clearFilters: []
  pageChange: [page: number]
  retry: []
  projectClick: [project: Project]
  projectVote: [project: Project, voteValue: 1 | -1 | null]
  projectComment: [project: Project]
  projectShare: [project: Project]
  projectBookmark: [project: Project, isBookmarked: boolean]
}>()

// State
const searchQuery = ref('')
const viewMode = ref<'grid' | 'list'>(props.defaultViewMode)
const showSortOptions = ref(false)
const currentPage = ref(1)

// Computed
const templateClasses = computed(() => ({
  'projects-page-template--sidebar-left': props.variant === 'sidebar-left',
  'projects-page-template--sidebar-right': props.variant === 'sidebar-right',
  'projects-page-template--full-width': props.variant === 'full-width'
}))

const contentWrapperClasses = computed(() => ({
  'flex flex-col lg:flex-row gap-8': props.showFilters,
  'flex flex-col': !props.showFilters
}))

const filtersSidebarClasses = computed(() => ({
  'lg:w-64': props.variant === 'sidebar-left' || props.variant === 'sidebar-right',
  'lg:w-80': props.variant === 'default'
}))

const sortLabel = computed(() => {
  const option = props.sortOptions.find(opt => opt.value === props.currentSort)
  return option?.label || 'Sort by'
})

const isEmpty = computed(() => {
  return !props.loading && !props.error && props.projects.length === 0
})

const totalPages = computed(() => {
  if (props.totalItems === 0) return 1
  return Math.ceil(props.totalItems / props.itemsPerPage)
})

const startItem = computed(() => {
  return (currentPage.value - 1) * props.itemsPerPage + 1
})

const endItem = computed(() => {
  const end = currentPage.value * props.itemsPerPage
  return Math.min(end, props.totalItems || props.projects.length)
})

const visiblePages = computed(() => {
  const pages: number[] = []
  const maxVisible = 5
  
  if (totalPages.value <= maxVisible) {
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i)
    }
  } else {
    let start = Math.max(1, currentPage.value - 2)
    let end = Math.min(totalPages.value, start + maxVisible - 1)
    
    if (end - start + 1 < maxVisible) {
      start = Math.max(1, end - maxVisible + 1)
    }
    
    for (let i = start; i <= end; i++) {
      pages.push(i)
    }
  }
  
  return pages
})

const showStartEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[0] > 1
})

const showEndEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[visiblePages.value.length - 1] < totalPages.value
})

// Methods
const handleSearch = () => {
  emit('search', searchQuery.value)
}

const handleCreate = () => {
  emit('create')
}

const setViewMode = (mode: 'grid' | 'list') => {
  viewMode.value = mode
  emit('viewModeChange', mode)
}

const toggleSortDropdown = () => {
  showSortOptions.value = !showSortOptions.value
}

const handleSortChange = (sortOption: string) => {
  showSortOptions.value = false
  emit('sortChange', sortOption)
}

const handleFilterChange = (filters: ProjectFilterOptions) => {
  emit('filterChange', filters)
}

const handleClearFilters = () => {
  emit('clearFilters')
}

const handlePageChange = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    emit('pageChange', page)
  }
}

const handleRetry = () => {
  emit('retry')
}

const handleProjectClick = (project: Project) => {
  emit('projectClick', project)
}

const handleProjectVote = (project: Project, voteValue: 1 | -1 | null) => {
  emit('projectVote', project, voteValue)
}

const handleProjectComment = (project: Project) => {
  emit('projectComment', project)
}

const handleProjectShare = (project: Project) => {
  emit('projectShare', project)
}

const handleProjectBookmark = (project: Project, isBookmarked: boolean) => {
  emit('projectBookmark', project, isBookmarked)
}

// Close sort dropdown when clicking outside
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.sort-dropdown')) {
    showSortOptions.value = false
  }
}

// Add event listener for click outside
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Watch for external sort changes
watch(() => props.currentSort, () => {
  showSortOptions.value = false
})

// Watch for external page changes
watch(() => props.totalItems, () => {
  // Reset to page 1 if total items change significantly
  if (currentPage.value > totalPages.value) {
    currentPage.value = 1
  }
})
</script>

<style scoped>
.projects-page-template {
  @apply min-h-screen bg-gray-50 dark:bg-gray-900;
}

.page-header {
  @apply bg-white dark:bg-gray-900 rounded-lg p-6 shadow-sm;
}

.projects-page-template--sidebar-left .content-wrapper {
  @apply flex flex-col lg:flex-row-reverse gap-8;
}

.projects-page-template--sidebar-right .content-wrapper {
  @apply flex flex-col lg:flex-row gap-8;
}

.projects-page-template--full-width .filters-sidebar {
  @apply hidden;
}

.filters-sidebar {
  @apply lg:w-64 flex-shrink-0;
}

.projects-content {
  @apply min-w-0;
}

.loading-state,
.error-state,
.empty-state {
  @apply min-h-[400px] flex items-center justify-center;
}

.stats-grid {
  @apply grid grid-cols-2 gap-3;
}

@media (min-width: 640px) {
  .stats-grid {
    @apply grid-cols-4;
  }
}

.page-footer {
  @apply mt-12 pt-8 border-t border-gray-200 dark:border-gray-700;
}
</style>
