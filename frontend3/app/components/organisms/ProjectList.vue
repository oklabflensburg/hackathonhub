<template>
  <div class="project-list" :class="listClasses">
    <!-- Loading State -->
    <div
      v-if="loading && (!projects || projects.length === 0)"
      class="loading-state py-12 text-center"
    >
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400 mx-auto mb-4" />
      <p class="text-gray-600 dark:text-gray-400">
        Loading projects...
      </p>
    </div>
    
    <!-- Empty State -->
    <div
      v-else-if="!loading && (!projects || projects.length === 0)"
      class="empty-state py-12 text-center"
    >
      <div class="empty-icon mx-auto mb-4 text-gray-400 dark:text-gray-500">
        <svg
          class="h-16 w-16 mx-auto"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
          />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
        {{ emptyTitle }}
      </h3>
      <p class="text-gray-600 dark:text-gray-400 max-w-md mx-auto mb-6">
        {{ emptyMessage }}
      </p>
      <slot name="empty-actions">
        <button
          v-if="showCreateButton"
          type="button"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          @click="handleCreateClick"
        >
          <svg
            class="-ml-1 mr-2 h-5 w-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
          Create Project
        </button>
      </slot>
    </div>
    
    <!-- Projects Grid/List -->
    <div
      v-else
      class="projects-container"
      :class="containerClasses"
    >
      <!-- Grid Layout -->
      <div
        v-if="layout === 'grid'"
        class="grid gap-6"
        :class="gridClasses"
      >
        <ProjectCard
          v-for="project in projects"
          :key="project.id"
          :project="project"
          :clickable="clickable"
          :project-url="getProjectUrl(project)"
          :loading="loading"
          :compact="compact"
          :show-featured-image="showFeaturedImage"
          :show-status-label="showStatusLabel"
          :show-author="showAuthor"
          :show-date="showDate"
          :show-team="showTeam"
          :show-hackathon="showHackathon"
          :show-description="showDescription"
          :show-tags="showTags"
          :show-technologies="showTechnologies"
          :show-deadline="showDeadline"
          :show-stats="showStats"
          :show-actions="showActions"
          :show-tags-in-footer="showTagsInFooter"
          :show-technologies-in-footer="showTechnologiesInFooter"
          :show-bookmark-button="showBookmarkButton"
          :max-tags="maxTags"
          :max-technologies="maxTechnologies"
          :image-badge-size="imageBadgeSize"
          :is-bookmarked="isBookmarked(project)"
          :variant="cardVariant"
          @click="handleProjectClick(project)"
          @vote="(projectId, voteType) => handleProjectVote(project, voteType)"
          @comment="(projectId) => handleProjectComment(project)"
          @bookmark="(projectId, bookmarked) => handleProjectBookmark(project, bookmarked)"
          @share="(project) => handleProjectShare(project)"
          @image-error="handleProjectImageError(project)"
        />
      </div>
      
      <!-- List Layout -->
      <div
        v-else-if="layout === 'list'"
        class="space-y-4"
      >
        <div
          v-for="project in projects"
          :key="project.id"
          class="project-list-item"
        >
          <ProjectCard
            :project="project"
            :clickable="clickable"
            :project-url="getProjectUrl(project)"
            :loading="loading"
            :compact="true"
            :show-featured-image="showFeaturedImage"
            :show-status-label="showStatusLabel"
            :show-author="showAuthor"
            :show-date="showDate"
            :show-team="showTeam"
            :show-hackathon="showHackathon"
            :show-description="showDescription"
            :show-tags="showTags"
            :show-technologies="showTechnologies"
            :show-deadline="showDeadline"
            :show-stats="showStats"
            :show-actions="showActions"
            :show-tags-in-footer="showTagsInFooter"
            :show-technologies-in-footer="showTechnologiesInFooter"
            :show-bookmark-button="showBookmarkButton"
            :max-tags="maxTags"
            :max-technologies="maxTechnologies"
            :image-badge-size="imageBadgeSize"
            :is-bookmarked="isBookmarked(project)"
            :variant="cardVariant"
            @click="handleProjectClick(project)"
          @vote="(projectId, voteType) => handleProjectVote(project, voteType)"
          @comment="(projectId) => handleProjectComment(project)"
          @bookmark="(projectId, bookmarked) => handleProjectBookmark(project, bookmarked)"
          @share="(project) => handleProjectShare(project)"
            @image-error="handleProjectImageError(project)"
          />
        </div>
      </div>
      
      <!-- Masonry Layout -->
      <div
        v-else-if="layout === 'masonry'"
        class="masonry-grid"
        :class="masonryClasses"
      >
        <div
          v-for="project in projects"
          :key="project.id"
          class="masonry-item"
        >
          <ProjectCard
            :project="project"
            :clickable="clickable"
            :project-url="getProjectUrl(project)"
            :loading="loading"
            :compact="compact"
            :show-featured-image="showFeaturedImage"
            :show-status-label="showStatusLabel"
            :show-author="showAuthor"
            :show-date="showDate"
            :show-team="showTeam"
            :show-hackathon="showHackathon"
            :show-description="showDescription"
            :show-tags="showTags"
            :show-technologies="showTechnologies"
            :show-deadline="showDeadline"
            :show-stats="showStats"
            :show-actions="showActions"
            :show-tags-in-footer="showTagsInFooter"
            :show-technologies-in-footer="showTechnologiesInFooter"
            :show-bookmark-button="showBookmarkButton"
            :max-tags="maxTags"
            :max-technologies="maxTechnologies"
            :image-badge-size="imageBadgeSize"
            :is-bookmarked="isBookmarked(project)"
            :variant="cardVariant"
            @click="handleProjectClick(project)"
          @vote="(projectId, voteType) => handleProjectVote(project, voteType)"
          @comment="(projectId) => handleProjectComment(project)"
          @bookmark="(projectId, bookmarked) => handleProjectBookmark(project, bookmarked)"
          @share="(project) => handleProjectShare(project)"
            @image-error="handleProjectImageError(project)"
          />
        </div>
      </div>
    </div>
    
    <!-- Load More -->
    <div
      v-if="showLoadMore && hasMore && !loading"
      class="load-more mt-8 text-center"
    >
      <button
        type="button"
        class="inline-flex items-center px-6 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        :disabled="loadingMore"
        @click="handleLoadMore"
      >
        <svg
          v-if="loadingMore"
          class="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
          />
        </svg>
        {{ loadingMore ? 'Loading...' : 'Load More' }}
      </button>
    </div>
    
    <!-- Loading More Indicator -->
    <div
      v-if="loadingMore"
      class="loading-more mt-6 text-center"
    >
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 dark:border-blue-400 mx-auto" />
    </div>
    
    <!-- Pagination -->
    <div
      v-if="showPagination && pagination && pagination.totalPages > 1"
      class="pagination mt-8"
    >
      <nav class="flex items-center justify-between" aria-label="Pagination">
        <div class="flex-1 flex justify-between sm:justify-start">
          <button
            type="button"
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-lg text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="!pagination.hasPrevious || loading"
            @click="handlePreviousPage"
          >
            Previous
          </button>
          <button
            type="button"
            class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-lg text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="!pagination.hasNext || loading"
            @click="handleNextPage"
          >
            Next
          </button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-end">
          <div>
            <p class="text-sm text-gray-700 dark:text-gray-300">
              Showing
              <span class="font-medium">{{ pagination.startIndex + 1 }}</span>
              to
              <span class="font-medium">{{ pagination.endIndex + 1 }}</span>
              of
              <span class="font-medium">{{ pagination.totalItems }}</span>
              results
            </p>
          </div>
        </div>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Project } from '../../types/project-types'
import ProjectCard from './ProjectCard.vue'

interface Pagination {
  currentPage: number
  totalPages: number
  totalItems: number
  itemsPerPage: number
  hasNext: boolean
  hasPrevious: boolean
  startIndex: number
  endIndex: number
}

interface Props {
  /** Projekte */
  projects?: Project[]
  /** Layout */
  layout?: 'grid' | 'list' | 'masonry'
  /** Grid Columns */
  gridColumns?: number
  /** Ladezustand */
  loading?: boolean
  /** Load More Ladezustand */
  loadingMore?: boolean
  /** Klickbar */
  clickable?: boolean
  /** Kompakt-Modus */
  compact?: boolean
  /** Featured Image anzeigen */
  showFeaturedImage?: boolean
  /** Status-Label anzeigen */
  showStatusLabel?: boolean
  /** Author anzeigen */
  showAuthor?: boolean
  /** Datum anzeigen */
  showDate?: boolean
  /** Team anzeigen */
  showTeam?: boolean
  /** Hackathon anzeigen */
  showHackathon?: boolean
  /** Beschreibung anzeigen */
  showDescription?: boolean
  /** Tags anzeigen */
  showTags?: boolean
  /** Technologies anzeigen */
  showTechnologies?: boolean
  /** Deadline anzeigen */
  showDeadline?: boolean
  /** Statistiken anzeigen */
  showStats?: boolean
  /** Aktionen anzeigen */
  showActions?: boolean
  /** Tags im Footer anzeigen */
  showTagsInFooter?: boolean
  /** Technologies im Footer anzeigen */
  showTechnologiesInFooter?: boolean
  /** Bookmark-Button anzeigen */
  showBookmarkButton?: boolean
  /** Maximale Anzahl Tags */
  maxTags?: number
  /** Maximale Anzahl Technologies */
  maxTechnologies?: number
  /** Bild-Badge Größe */
  imageBadgeSize?: 'sm' | 'md' | 'lg'
  /** Card Variante */
  cardVariant?: 'default' | 'elevated' | 'minimal'
  /** Empty State Titel */
  emptyTitle?: string
  /** Empty State Nachricht */
  emptyMessage?: string
  /** Create Button anzeigen */
  showCreateButton?: boolean
  /** Load More anzeigen */
  showLoadMore?: boolean
  /** Pagination anzeigen */
  showPagination?: boolean
  /** Pagination Daten */
  pagination?: Pagination
  /** Hat mehr Daten */
  hasMore?: boolean
  /** Bookmarked Projects */
  bookmarkedProjects?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  layout: 'grid',
  gridColumns: 3,
  loading: false,
  loadingMore: false,
  clickable: true,
  compact: false,
  showFeaturedImage: true,
  showStatusLabel: true,
  showAuthor: true,
  showDate: true,
  showTeam: true,
  showHackathon: true,
  showDescription: true,
  showTags: true,
  showTechnologies: true,
  showDeadline: true,
  showStats: true,
  showActions: true,
  showTagsInFooter: false,
  showTechnologiesInFooter: false,
  showBookmarkButton: true,
  maxTags: 3,
  maxTechnologies: 3,
  imageBadgeSize: 'md',
  cardVariant: 'default',
  emptyTitle: 'No projects found',
  emptyMessage: 'There are no projects to display at the moment.',
  showCreateButton: false,
  showLoadMore: false,
  showPagination: false,
  hasMore: false,
  bookmarkedProjects: () => [],
})

const emit = defineEmits<{
  (e: 'project-click', project: Project): void
  (e: 'project-vote', project: Project, voteType: 'up' | 'down'): void
  (e: 'project-comment', project: Project): void
  (e: 'project-bookmark', project: Project, bookmarked: boolean): void
  (e: 'project-share', project: Project): void
  (e: 'project-image-error', project: Project): void
  (e: 'create-click'): void
  (e: 'load-more'): void
  (e: 'previous-page'): void
  (e: 'next-page'): void
}>()

// Computed Properties
const listClasses = computed(() => {
  const classes: string[] = []
  
  if (props.loading && (!props.projects || props.projects.length === 0)) {
    classes.push('opacity-70')
  }
  
  return classes.join(' ')
})

const containerClasses = computed(() => {
  const classes: string[] = []
  
  if (props.layout === 'masonry') {
    classes.push('masonry-layout')
  }
  
  return classes.join(' ')
})

const gridClasses = computed(() => {
  switch (props.gridColumns) {
    case 1:
      return 'grid-cols-1'
    case 2:
      return 'grid-cols-1 sm:grid-cols-2'
    case 3:
      return 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'
    case 4:
      return 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
    case 5:
      return 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5'
    default:
      return 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'
  }
})

const masonryClasses = computed(() => {
  return 'columns-1 sm:columns-2 lg:columns-3 gap-6'
})

// Helper Functions
const getProjectUrl = (project: Project) => {
  return `/projects/${project.slug || project.id}`
}

const isBookmarked = (project: Project) => {
  return props.bookmarkedProjects.includes(project.id)
}

// Event Handlers
const handleCreateClick = () => {
  emit('create-click')
}

const handleProjectClick = (project: Project) => {
  emit('project-click', project)
}

const handleProjectVote = (project: Project, voteType: 'up' | 'down') => {
  emit('project-vote', project, voteType)
}

const handleProjectComment = (project: Project) => {
  emit('project-comment', project)
}

const handleProjectBookmark = (project: Project, bookmarked: boolean) => {
  emit('project-bookmark', project, bookmarked)
}

const handleProjectShare = (project: Project) => {
  emit('project-share', project)
}

const handleProjectImageError = (project: Project) => {
  emit('project-image-error', project)
}

const handleLoadMore = () => {
  emit('load-more')
}

const handlePreviousPage = () => {
  emit('previous-page')
}

const handleNextPage = () => {
  emit('next-page')
}
</script>

<style scoped>
.masonry-grid {
  column-gap: 1.5rem;
}

.masonry-item {
  break-inside: avoid;
  margin-bottom: 1.5rem;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .masonry-grid {
    columns: 1 !important;
  }
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
  .project-list {
    color-scheme: dark;
  }
}

/* Loading animation */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.loading-state {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
  }
