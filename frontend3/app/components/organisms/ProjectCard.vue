<template>
  <article
    class="project-card group relative bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden"
    :class="cardClasses"
    :data-project-id="project.id"
    :data-project-status="project.status"
    :aria-labelledby="`project-title-${project.id}`"
    :aria-describedby="`project-description-${project.id}`"
  >
    <!-- Featured Image -->
    <div
      v-if="showFeaturedImage && project.featuredImage"
      class="project-card-image relative h-48 overflow-hidden bg-gray-100 dark:bg-gray-800"
    >
      <img
        :src="project.featuredImage"
        :alt="`Featured image for ${project.title}`"
        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
        loading="lazy"
        @error="handleImageError"
      />
      
      <!-- Image Overlay -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
      
      <!-- Status Badge on Image -->
      <div class="absolute top-3 left-3">
        <ProjectStatusBadge
          :status="project.status"
          :size="imageBadgeSize"
          :show-label="showStatusLabel"
        />
      </div>
      
      <!-- Bookmark Button on Image -->
      <button
        v-if="showBookmarkButton"
        type="button"
        class="absolute top-3 right-3 p-2 bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm rounded-full shadow-sm hover:bg-white dark:hover:bg-gray-800 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
        :aria-label="isBookmarked ? 'Remove bookmark' : 'Bookmark project'"
        @click="handleBookmarkToggle"
      >
        <svg
          class="h-5 w-5"
          :class="isBookmarked ? 'text-yellow-500' : 'text-gray-400'"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
          />
        </svg>
      </button>
    </div>
    
    <!-- Card Content -->
    <div class="project-card-content p-5">
      <!-- Header -->
      <ProjectCardHeader
        :project="project"
        :show-author="showAuthor"
        :show-date="showDate"
        :show-team="showTeam"
        :show-hackathon="showHackathon"
        :compact="compact"
        class="mb-4"
      />
      
      <!-- Content -->
      <ProjectCardContent
        :project="project"
        :show-description="showDescription"
        :show-tags="showTags"
        :show-technologies="showTechnologies"
        :show-team="showTeam"
        :show-deadline="showDeadline"
        :compact="compact"
        :max-tags="maxTags"
        :max-technologies="maxTechnologies"
        class="mb-4"
      />
      
      <!-- Footer -->
      <ProjectCardFooter
        :project="project"
        :show-stats="showStats"
        :show-actions="showActions"
        :show-tags="showTagsInFooter"
        :show-technologies="showTechnologiesInFooter"
        :compact="compact"
        :max-tags="maxTags"
        :max-technologies="maxTechnologies"
        @vote="(projectId, voteType) => handleVote(projectId, voteType)"
        @comment="(projectId) => handleComment(projectId)"
        @bookmark="(projectId, bookmarked) => handleBookmark(projectId, bookmarked)"
        @share="(projectId) => handleShare(projectId)"
      />
    </div>
    
    <!-- Interactive Overlay -->
    <a
      v-if="clickable"
      :href="projectUrl"
      class="absolute inset-0 z-10"
      :aria-label="`View project: ${project.title}`"
      @click.prevent="handleCardClick"
    />
    
    <!-- Loading State -->
    <div
      v-if="loading"
      class="absolute inset-0 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm flex items-center justify-center z-20"
    >
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 dark:border-blue-400" />
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Project } from '../../types/project-types'
import ProjectStatusBadge from '../atoms/ProjectStatusBadge.vue'
import ProjectCardHeader from '../molecules/ProjectCardHeader.vue'
import ProjectCardContent from '../molecules/ProjectCardContent.vue'
import ProjectCardFooter from '../molecules/ProjectCardFooter.vue'

interface Props {
  /** Projekt-Daten */
  project: Project
  /** Klickbar (zeigt Overlay-Link) */
  clickable?: boolean
  /** Projekt-URL (für Link) */
  projectUrl?: string
  /** Ladezustand */
  loading?: boolean
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
  /** Ist gebookmarked */
  isBookmarked?: boolean
  /** Variante */
  variant?: 'default' | 'elevated' | 'minimal'
}

const props = withDefaults(defineProps<Props>(), {
  clickable: true,
  projectUrl: '',
  loading: false,
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
  isBookmarked: false,
  variant: 'default',
})

const emit = defineEmits<{
  (e: 'click', project: Project): void
  (e: 'vote', project: Project, voteType: 'up' | 'down'): void
  (e: 'comment', project: Project): void
  (e: 'bookmark', project: Project, bookmarked: boolean): void
  (e: 'share', project: Project): void
  (e: 'image-error', project: Project): void
}>()

// Computed Properties
const cardClasses = computed(() => {
  const classes: string[] = []
  
  // Variant
  switch (props.variant) {
    case 'elevated':
      classes.push('shadow-lg hover:shadow-xl')
      break
    case 'minimal':
      classes.push('shadow-none border-gray-100 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600')
      break
    case 'default':
    default:
      // Default classes already applied
      break
  }
  
  // Compact mode
  if (props.compact) {
    classes.push('p-4')
  }
  
  // Loading state
  if (props.loading) {
    classes.push('opacity-70')
  }
  
  // Clickable
  if (props.clickable) {
    classes.push('cursor-pointer hover:-translate-y-1')
  }
  
  return classes.join(' ')
})

// Methods
const handleCardClick = () => {
  if (props.clickable && !props.loading) {
    emit('click', props.project)
  }
}

const handleVote = (projectId: string, voteType: 'up' | 'down') => {
  emit('vote', props.project, voteType)
}

const handleComment = (projectId: string) => {
  emit('comment', props.project)
}

const handleBookmarkToggle = () => {
  emit('bookmark', props.project, !props.isBookmarked)
}

const handleBookmark = (projectId: string, bookmarked: boolean) => {
  emit('bookmark', props.project, bookmarked)
}

const handleShare = (project: Project) => {
  emit('share', project)
}

const handleImageError = () => {
  emit('image-error', props.project)
}
</script>

<style scoped>
.project-card {
  position: relative;
  transition: all 0.2s ease-in-out;
}

.project-card:hover {
  transform: translateY(-2px);
}

.project-card-image img {
  transition: transform 0.3s ease;
}

.project-card:hover .project-card-image img {
  transform: scale(1.05);
}

/* Focus styles for accessibility */
.project-card:focus-within {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
  .project-card {
    background-color: #111827;
    border-color: #374151;
  }
  
  .project-card:hover {
    border-color: #4b5563;
  }
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .project-card {
    border-radius: 0.75rem;
  }
  
  .project-card-content {
    padding: 1rem;
  }
}
</style>