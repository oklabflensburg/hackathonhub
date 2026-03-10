<template>
  <div class="user-projects">
    <!-- Header mit Titel und Filter -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
          Projekte
        </h2>
        <p v-if="!loading" class="text-sm text-gray-600 dark:text-gray-400 mt-1">
          {{ filteredProjects.length }} von {{ projects.length }} Projekten
        </p>
      </div>

      <div class="flex gap-3">
        <Button
          variant="primary"
          size="sm"
          @click="$emit('create-project')"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Neues Projekt
        </Button>
      </div>
    </div>

    <!-- Filter und Sortierung -->
    <div class="mb-8 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Status Filter -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Status
          </label>
          <select
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            :value="filters.status && filters.status.length > 0 ? filters.status[0] : ''"
            @change="toggleStatusFilter(($event.target as HTMLSelectElement).value as ProjectStatus)"
          >
            <option value="">Alle</option>
            <option value="draft">Entwurf</option>
            <option value="active">Aktiv</option>
            <option value="completed">Abgeschlossen</option>
            <option value="archived">Archiviert</option>
            <option value="under_review">In Prüfung</option>
          </select>
        </div>

        <!-- Sortierung -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Sortieren nach
          </label>
          <select
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            :value="currentSortOption"
            @change="setSortOption(($event.target as HTMLSelectElement).value as ProjectSortOption)"
          >
            <option v-for="option in sortOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
        </div>

        <!-- Suchfeld -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Suche
          </label>
          <input
            type="text"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            placeholder="Projekte durchsuchen..."
            :value="searchQuery"
            @input="searchQuery = ($event.target as HTMLInputElement).value"
          />
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="animate-pulse">
        <div class="h-32 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="filteredProjects.length === 0"
      class="text-center py-12 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg"
    >
      <slot name="empty-state">
        <svg class="w-16 h-16 mx-auto text-gray-400 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-4 text-lg font-medium text-gray-900 dark:text-white">
          Keine Projekte gefunden
        </h3>
        <p class="mt-2 text-gray-600 dark:text-gray-400 max-w-md mx-auto">
          {{ emptyMessage || 'Es wurden keine Projekte mit den aktuellen Filtern gefunden.' }}
        </p>
        <div class="mt-6">
          <Button
            variant="primary"
            @click="$emit('create-project')"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Erstes Projekt erstellen
          </Button>
        </div>
      </slot>
    </div>

    <!-- Projects Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="project in filteredProjects"
        :key="project.id"
        class="project-card bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow cursor-pointer"
        @click="$emit('project-click', project.id)"
      >
        <slot name="project-card" :project="project">
          <!-- Default Project Card -->
          <div class="p-5">
            <!-- Header mit Status und Aktionen -->
            <div class="flex justify-between items-start mb-3">
              <div>
                <span
                  class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                  :class="{
                    'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200': project.status === 'draft',
                    'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200': project.status === 'active',
                    'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200': project.status === 'completed',
                    'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200': project.status === 'archived',
                    'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200': project.status === 'under_review'
                  }"
                >
                  {{ formatStatus(project.status) }}
                </span>
              </div>
              <div class="flex gap-2">
                <button
                  class="p-1 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
                  @click.stop="$emit('edit-project', project.id)"
                  title="Projekt bearbeiten"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Projekt-Titel und Beschreibung -->
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {{ project.title }}
            </h3>
            <p v-if="project.shortDescription || project.description" class="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-2">
              {{ project.shortDescription || project.description }}
            </p>

            <!-- Technologien -->
            <div v-if="project.technologies && project.technologies.length > 0" class="mb-4">
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="tech in project.technologies.slice(0, 3)"
                  :key="tech.id"
                  class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                  :style="{ backgroundColor: tech.color + '20', color: tech.color }"
                >
                  {{ tech.name }}
                </span>
                <span
                  v-if="project.technologies.length > 3"
                  class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200"
                >
                  +{{ project.technologies.length - 3 }}
                </span>
              </div>
            </div>

            <!-- Metadaten -->
            <div class="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
              <div class="flex items-center gap-4">
                <div class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span>{{ project.team?.length || 0 }}</span>
                </div>
                <div class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                  </svg>
                  <span>{{ project.stats?.views || 0 }}</span>
                </div>
              </div>
              <div class="text-xs">
                {{ formatDate(project.createdAt) }}
              </div>
            </div>
          </div>
        </slot>
      </div>
    </div>

    <!-- Load More -->
    <div v-if="hasMore && !loading" class="mt-8 text-center">
      <Button
        variant="outline"
        @click="$emit('load-more')"
      >
        Mehr laden
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ProjectStatus, ProjectSortOption } from '~/types/project-types'
import type { Project, ProjectFilterOptions } from '~/types/project-types'
import Button from '~/components/atoms/Button.vue'
import { useProjectFilters } from '~/composables/useProjectFilters'

interface UserProjectsProps {
  projects: Project[]
  loading?: boolean
  emptyMessage?: string
  hasMore?: boolean
  initialFilters?: ProjectFilterOptions
}

const props = withDefaults(defineProps<UserProjectsProps>(), {
  loading: false,
  emptyMessage: '',
  hasMore: false,
  initialFilters: () => ({})
})

const emit = defineEmits<{
  'project-click': [projectId: string]
  'create-project': []
  'edit-project': [projectId: string]
  'load-more': []
  'filters-change': [filters: ProjectFilterOptions]
}>()

// Projekt-Filter Composable
const {
  filters,
  sortOption,
  searchQuery,
  hasActiveFilters,
  activeFilterCount,
  filterSummary,
  sortOptions,
  currentSortOption,
  setFilters,
  clearFilters,
  clearFilter,
  setSortOption,
  toggleStatusFilter,
  setBookmarkedFilter,
  setVotedFilter,
  setTeamSizeFilter,
  setDateRangeFilter,
  validateFilters,
  resetToDefaults,
  getFilterPreset,
  applyPreset
} = useProjectFilters()

// Initiale Filter übernehmen
watch(() => props.initialFilters, (newFilters) => {
  if (newFilters) {
    setFilters(newFilters)
  }
}, { immediate: true })

// Filter-Änderungen nach außen melden
watch(filters, (newFilters) => {
  emit('filters-change', newFilters)
}, { deep: true })

// Gefilterte und sortierte Projekte
const filteredProjects = computed(() => {
  let filtered = [...props.projects]

  // Status-Filter
  if (filters.value.status && filters.value.status.length > 0) {
    filtered = filtered.filter(project => filters.value.status!.includes(project.status))
  }

  // Suchfilter
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter(project => 
      project.title?.toLowerCase().includes(query) ||
      project.description?.toLowerCase().includes(query) ||
      project.shortDescription?.toLowerCase().includes(query)
    )
  }

  // Sortierung basierend auf sortOption
  const currentSort = sortOption.value
  
  return filtered.sort((a, b) => {
    switch (currentSort) {
      case ProjectSortOption.NEWEST:
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      
      case ProjectSortOption.OLDEST:
        return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      
      case ProjectSortOption.ALPHABETICAL:
        return (a.title || '').localeCompare(b.title || '')
      
      case ProjectSortOption.MOST_VIEWED:
        return (b.stats?.views || 0) - (a.stats?.views || 0)
      
      case ProjectSortOption.MOST_VOTED:
        return (b.stats?.votes || 0) - (a.stats?.votes || 0)
      
      case ProjectSortOption.MOST_COMMENTED:
        return (b.stats?.comments || 0) - (a.stats?.comments || 0)
      
      case ProjectSortOption.TRENDING:
        // Einfache Trending-Berechnung basierend auf Views und Votes
        const aScore = (a.stats?.views || 0) * 0.7 + (a.stats?.votes || 0) * 0.3
        const bScore = (b.stats?.views || 0) * 0.7 + (b.stats?.votes || 0) * 0.3
        return bScore - aScore
      
      default:
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    }
  })
})

const formatStatus = (status: ProjectStatus) => {
  const statusMap = {
    [ProjectStatus.DRAFT]: 'Entwurf',
    [ProjectStatus.ACTIVE]: 'Aktiv',
    [ProjectStatus.COMPLETED]: 'Abgeschlossen',
    [ProjectStatus.ARCHIVED]: 'Archiviert',
    [ProjectStatus.UNDER_REVIEW]: 'In Prüfung'
  } as Record<string, string>
  return statusMap[status] || status
}

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}
</script>

<style scoped>
.project-card {
  transition: all 0.2s ease;
}

.project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}
</style>