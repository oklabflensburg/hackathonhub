<template>
  <div class="project-card-footer" :class="footerClasses">
    <!-- Statistiken -->
    <div v-if="showStats" class="footer-stats" :class="statsClasses">
      <!-- Views -->
      <div v-if="showViews" class="stat-item views" :class="statItemClasses">
        <span class="stat-icon" aria-hidden="true">
          <slot name="views-icon">
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
              />
            </svg>
          </slot>
        </span>
        <span class="stat-value" :class="statValueClasses">
          {{ formatNumber(project.stats.views) }}
        </span>
        <span class="stat-label sr-only">
          Views
        </span>
      </div>
      
      <!-- Votes -->
      <div v-if="showVotes" class="stat-item votes" :class="statItemClasses">
        <ProjectVoteButton
          :project-id="project.id"
          :has-voted="project.userVote !== null && project.userVote !== undefined"
          :vote-count="project.stats.votes"
          size="sm"
          variant="secondary"
          :show-count="true"
          :disabled="!interactive"
          @vote="handleVote"
          @unvote="handleUnvote"
        />
      </div>
      
      <!-- Comments -->
      <div v-if="showComments" class="stat-item comments" :class="statItemClasses">
        <ProjectCommentButton
          :project-id="project.id"
          :comment-count="project.stats.comments"
          size="sm"
          variant="secondary"
          :show-count="true"
          :disabled="!interactive"
          @click="handleCommentClick"
        />
      </div>
      
      <!-- Bookmarks -->
      <div v-if="showBookmarks" class="stat-item bookmarks" :class="statItemClasses">
        <button
          type="button"
          class="bookmark-button inline-flex items-center gap-1.5 px-2 py-1 rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1"
          :class="bookmarkButtonClasses"
          :aria-label="bookmarkAriaLabel"
          :disabled="!interactive"
          @click="handleBookmarkToggle"
        >
          <span class="bookmark-icon" aria-hidden="true">
            <slot name="bookmark-icon">
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  v-if="project.isBookmarked"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
                  fill="currentColor"
                />
                <path
                  v-else
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
                />
              </svg>
            </slot>
          </span>
          <span class="bookmark-count" :class="bookmarkCountClasses">
            {{ formatNumber(project.stats.bookmarks) }}
          </span>
        </button>
      </div>
      
      <!-- Shares -->
      <div v-if="showShares" class="stat-item shares" :class="statItemClasses">
        <ProjectShareButton
          :project="project"
          size="sm"
          variant="secondary"
          :show-text="false"
          :disabled="!interactive"
          @click="handleShareClick"
        />
        <span class="share-count ml-1 text-xs text-gray-500 dark:text-gray-400">
          {{ formatNumber(project.stats.shares) }}
        </span>
      </div>
    </div>
    
    <!-- Aktionen -->
    <div v-if="showActions" class="footer-actions" :class="actionsClasses">
      <slot name="actions">
        <!-- Default Actions -->
        <button
          v-if="showViewButton"
          type="button"
          class="view-button px-3 py-1.5 text-sm font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1"
          :class="viewButtonClasses"
          @click="handleViewClick"
        >
          View Project
        </button>
        
        <button
          v-if="showEditButton"
          type="button"
          class="edit-button px-3 py-1.5 text-sm font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1"
          :class="editButtonClasses"
          @click="handleEditClick"
        >
          Edit
        </button>
        
        <button
          v-if="showDeleteButton"
          type="button"
          class="delete-button px-3 py-1.5 text-sm font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1"
          :class="deleteButtonClasses"
          @click="handleDeleteClick"
        >
          Delete
        </button>
      </slot>
    </div>
    
    <!-- Tags (optional) -->
    <div v-if="showTags && project.tags?.length > 0" class="footer-tags" :class="tagsClasses">
      <div class="tags-label text-xs text-gray-500 dark:text-gray-400 mb-1">
        Tags:
      </div>
      <div class="tags-list flex flex-wrap gap-1">
        <ProjectTag
          v-for="tag in visibleTags"
          :key="tag.id"
          :tag="tag"
          size="sm"
          :clickable="interactive"
          @click="handleTagClick"
        />
        <button
          v-if="hasMoreTags && interactive"
          type="button"
          class="more-tags-button text-xs text-blue-600 dark:text-blue-400 hover:underline focus:outline-none"
          @click="handleShowAllTags"
        >
          +{{ project.tags.length - maxVisibleTags }} more
        </button>
      </div>
    </div>
    
    <!-- Technologies (optional) -->
    <div v-if="showTechnologies && project.technologies?.length > 0" class="footer-technologies" :class="technologiesClasses">
      <div class="technologies-label text-xs text-gray-500 dark:text-gray-400 mb-1">
        Technologies:
      </div>
      <div class="technologies-list flex flex-wrap gap-1">
        <span
          v-for="tech in visibleTechnologies"
          :key="tech.id"
          class="technology-badge inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
          :class="technologyBadgeClasses(tech)"
          :style="{ backgroundColor: `${tech.color}20`, color: tech.color }"
        >
          <span
            v-if="tech.icon"
            class="technology-icon mr-1"
            aria-hidden="true"
          >
            {{ tech.icon }}
          </span>
          {{ tech.name }}
        </span>
        <button
          v-if="hasMoreTechnologies && interactive"
          type="button"
          class="more-technologies-button text-xs text-blue-600 dark:text-blue-400 hover:underline focus:outline-none"
          @click="handleShowAllTechnologies"
        >
          +{{ project.technologies.length - maxVisibleTechnologies }} more
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Project, ProjectTechnology } from '~/types/project-types'
import ProjectVoteButton from '~/components/atoms/ProjectVoteButton.vue'
import ProjectCommentButton from '~/components/atoms/ProjectCommentButton.vue'
import ProjectShareButton from '~/components/atoms/ProjectShareButton.vue'
import ProjectTag from '~/components/atoms/ProjectTag.vue'

interface Props {
  /** Projekt-Daten */
  project: Project
  /** Interaktive Elemente */
  interactive?: boolean
  /** Statistiken anzeigen */
  showStats?: boolean
  /** Views anzeigen */
  showViews?: boolean
  /** Votes anzeigen */
  showVotes?: boolean
  /** Comments anzeigen */
  showComments?: boolean
  /** Bookmarks anzeigen */
  showBookmarks?: boolean
  /** Shares anzeigen */
  showShares?: boolean
  /** Aktionen anzeigen */
  showActions?: boolean
  /** View-Button anzeigen */
  showViewButton?: boolean
  /** Edit-Button anzeigen */
  showEditButton?: boolean
  /** Delete-Button anzeigen */
  showDeleteButton?: boolean
  /** Tags anzeigen */
  showTags?: boolean
  /** Technologies anzeigen */
  showTechnologies?: boolean
  /** Maximale sichtbare Tags */
  maxVisibleTags?: number
  /** Maximale sichtbare Technologies */
  maxVisibleTechnologies?: number
  /** Kompakte Variante */
  compact?: boolean
  /** Ausrichtung */
  align?: 'left' | 'center' | 'right' | 'between'
}

const props = withDefaults(defineProps<Props>(), {
  interactive: true,
  showStats: true,
  showViews: true,
  showVotes: true,
  showComments: true,
  showBookmarks: true,
  showShares: false,
  showActions: false,
  showViewButton: true,
  showEditButton: false,
  showDeleteButton: false,
  showTags: true,
  showTechnologies: true,
  maxVisibleTags: 3,
  maxVisibleTechnologies: 3,
  compact: false,
  align: 'between',
})

const emit = defineEmits<{
  'vote': [projectId: string, voteType: 'up' | 'down']
  'unvote': [projectId: string]
  'comment': [projectId: string]
  'bookmark': [projectId: string, bookmarked: boolean]
  'share': [project: Project]
  'view': [project: Project]
  'edit': [project: Project]
  'delete': [project: Project]
  'tag-click': [tag: any]
  'technology-click': [technology: ProjectTechnology]
  'show-all-tags': []
  'show-all-technologies': []
}>()

// Computed Properties
const footerClasses = computed(() => {
  const classes: string[] = []
  
  if (props.compact) {
    classes.push('compact')
  }
  
  switch (props.align) {
    case 'center':
      classes.push('text-center')
      break
    case 'right':
      classes.push('text-right')
      break
    case 'between':
      classes.push('flex justify-between items-center')
      break
    case 'left':
    default:
      classes.push('text-left')
  }
  
  return classes.join(' ')
})

const statsClasses = computed(() => {
  const classes: string[] = [
    'flex items-center gap-4',
    props.compact ? 'gap-2' : 'gap-4',
  ]
  
  return classes.join(' ')
})

const statItemClasses = computed(() => {
  return 'flex items-center gap-1.5'
})

const statValueClasses = computed(() => {
  return 'text-sm font-medium text-gray-700 dark:text-gray-300'
})

const bookmarkAriaLabel = computed(() => {
  return props.project.isBookmarked
    ? `Remove bookmark from ${props.project.title}`
    : `Bookmark ${props.project.title}`
})

const bookmarkButtonClasses = computed(() => {
  const base = 'hover:bg-gray-100 dark:hover:bg-gray-800 focus:ring-gray-300 dark:focus:ring-gray-700'
  
  if (props.project.isBookmarked) {
    return `${base} text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30`
  }
  
  return `${base} text-gray-600 dark:text-gray-400 bg-transparent`
})

const bookmarkCountClasses = computed(() => {
  return props.project.isBookmarked
    ? 'text-blue-600 dark:text-blue-400'
    : 'text-gray-600 dark:text-gray-400'
})

const actionsClasses = computed(() => {
  return 'flex items-center gap-2 mt-3'
})

const viewButtonClasses = computed(() => {
  return 'bg-blue-600 hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-800 text-white focus:ring-blue-500'
})

const editButtonClasses = computed(() => {
  return 'bg-gray-200 hover:bg-gray-300 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-800 dark:text-gray-200 focus:ring-gray-300 dark:focus:ring-gray-700'
})

const deleteButtonClasses = computed(() => {
  return 'bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 text-red-700 dark:text-red-400 focus:ring-red-300 dark:focus:ring-red-700'
})

const tagsClasses = computed(() => {
  return 'mt-3'
})

const technologiesClasses = computed(() => {
  return 'mt-3'
})

const visibleTags = computed(() => {
  if (!props.project.tags) return []
  return props.project.tags.slice(0, props.maxVisibleTags)
})

const hasMoreTags = computed(() => {
  if (!props.project.tags) return false
  return props.project.tags.length > props.maxVisibleTags
})

const visibleTechnologies = computed(() => {
  if (!props.project.technologies) return []
  return props.project.technologies.slice(0, props.maxVisibleTechnologies)
})

const hasMoreTechnologies = computed(() => {
  if (!props.project.technologies) return false
  return props.project.technologies.length > props.maxVisibleTechnologies
})

// Helper Functions
const formatNumber = (num: number) => {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`
  }
  if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}k`
  }
  return num.toString()
}

const technologyBadgeClasses = (tech: ProjectTechnology) => {
  return 'border border-current/20'
}

// Event Handlers
const handleVote = (projectId: string, voteType: 'up' | 'down') => {
  emit('vote', projectId, voteType)
}

const handleUnvote = (projectId: string) => {
  emit('unvote', projectId)
}

const handleCommentClick = (projectId: string) => {
  emit('comment', projectId)
}

const handleBookmarkToggle = () => {
  if (props.interactive) {
    emit('bookmark', props.project.id, !props.project.isBookmarked)
  }
}

const handleShareClick = (project: Project) => {
  emit('share', project)
}

const handleViewClick = () => {
  emit('view', props.project)
}

const handleEditClick = () => {
  emit('edit', props.project)
}

const handleDeleteClick = () => {
  emit('delete', props.project)
}

const handleTagClick = (tag: any) => {
  if (props.interactive) {
    emit('tag-click', tag)
  }
}

const handleShowAllTags = () => {
  emit('show-all-tags')
}

const handleShowAllTechnologies = () => {
  emit('show-all-technologies')
}
</script>

<style scoped>
.project-card-footer {
  transition: all 0.2s ease;
}

/* Compact Variante */
.project-card-footer.compact .footer-stats {
  gap: 0.5rem;
}

.project-card-footer.compact .stat-item {
  font-size: 0.75rem;
}

.project-card-footer.compact .footer-actions button {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

/* Responsive Anpassungen */
@media (max-width: 640px) {
  .project-card-footer:not(.compact) .footer-stats {
    flex-wrap: wrap;
    gap: 0.75rem;
  }
  
  .footer-actions {
    flex-wrap: wrap;
  }
  
  .tags-list,
  .technologies-list {
    flex-wrap: wrap;
  }
}

/* Dark Mode Optimierungen */
@media (prefers-color-scheme: dark) {
  .technology-badge {
    border-color: rgba(255, 255, 255, 0.1);
  }
}

/* Accessibility */
button:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 2px;
  border-radius: 0.25rem;
}

/* Loading State (für zukünftige Erweiterungen) */
.project-card-footer.loading .stat-value,
.project-card-footer.loading .bookmark-count {
  position: relative;
  overflow: hidden;
}

.project-card-footer.loading .stat-value::after,
.project-card-footer.loading .bookmark-count::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  .project-card-footer * {
    transition: none;
  }
  
  @keyframes shimmer {
    0%, 100% {
      opacity: 0.5;
    }
  }
}</style>
