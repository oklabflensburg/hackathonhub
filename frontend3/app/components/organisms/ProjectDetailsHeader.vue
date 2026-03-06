<template>
  <header class="project-details-header" :class="headerClasses">
    <!-- Breadcrumb Navigation -->
    <nav
      v-if="showBreadcrumb"
      class="breadcrumb mb-4"
      aria-label="Breadcrumb"
    >
      <ol class="flex items-center space-x-2 text-sm">
        <li>
          <a
            href="/projects"
            class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
          >
            Projects
          </a>
        </li>
        <li>
          <svg
            class="h-4 w-4 text-gray-400 dark:text-gray-500"
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
        </li>
        <li class="text-gray-700 dark:text-gray-300 font-medium truncate">
          {{ project.title }}
        </li>
      </ol>
    </nav>
    
    <!-- Main Header Content -->
    <div class="header-content">
      <!-- Title and Status Row -->
      <div class="title-row flex items-start justify-between mb-4">
        <div class="title-section flex-1">
          <h1 class="project-title text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            {{ project.title }}
          </h1>
          
          <div class="title-meta flex flex-wrap items-center gap-3">
            <!-- Status Badge -->
            <ProjectStatusBadge
              :status="project.status"
              :size="statusSize"
              :show-label="true"
            />
            
            <!-- Visibility Badge -->
            <span
              v-if="showVisibility && project.visibility"
              class="visibility-badge inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              :class="visibilityClasses"
            >
              <svg
                v-if="project.visibility === 'public'"
                class="mr-1 h-3 w-3"
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
              <svg
                v-else-if="project.visibility === 'private'"
                class="mr-1 h-3 w-3"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
              {{ visibilityLabel }}
            </span>
            
            <!-- Last Updated -->
            <span
              v-if="showLastUpdated && project.updatedAt"
              class="last-updated text-sm text-gray-500 dark:text-gray-400"
            >
              Updated {{ formatDate(project.updatedAt) }}
            </span>
          </div>
        </div>
        
        <!-- Action Buttons -->
        <div
          v-if="showActions"
          class="action-buttons flex items-center gap-2"
        >
          <!-- Edit Button -->
          <button
            v-if="showEditButton && canEdit"
            type="button"
            class="edit-button inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            @click="handleEdit"
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
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
            Edit
          </button>
          
          <!-- Share Button -->
          <ProjectShareButton
            :project="project"
            size="md"
            variant="secondary"
            @click="handleShare"
          />
          
          <!-- Bookmark Button -->
          <button
            v-if="showBookmarkButton"
            type="button"
            class="bookmark-button inline-flex items-center px-3 py-2 border rounded-lg text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2"
            :class="bookmarkButtonClasses"
            @click="handleBookmarkToggle"
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
                d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
              />
            </svg>
            {{ isBookmarked ? 'Saved' : 'Save' }}
          </button>
          
          <!-- More Actions Dropdown -->
          <div
            v-if="showMoreActions"
            class="more-actions relative"
          >
            <button
              type="button"
              class="more-button inline-flex items-center p-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              @click="toggleMoreActions"
            >
              <svg
                class="h-5 w-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"
                />
              </svg>
            </button>
            
            <!-- Dropdown Menu -->
            <div
              v-if="showMoreMenu"
              class="more-menu absolute right-0 mt-2 w-48 rounded-lg shadow-lg bg-white dark:bg-gray-900 ring-1 ring-black ring-opacity-5 focus:outline-none z-10"
            >
              <div class="py-1">
                <button
                  v-if="showReportButton"
                  type="button"
                  class="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
                  @click="handleReport"
                >
                  Report
                </button>
                <button
                  v-if="showDuplicateButton && canEdit"
                  type="button"
                  class="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
                  @click="handleDuplicate"
                >
                  Duplicate
                </button>
                <button
                  v-if="showArchiveButton && canEdit"
                  type="button"
                  class="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
                  @click="handleArchive"
                >
                  {{ project.status === 'archived' ? 'Unarchive' : 'Archive' }}
                </button>
                <button
                  v-if="showDeleteButton && canDelete"
                  type="button"
                  class="w-full text-left px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-800"
                  @click="handleDelete"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
        <!-- Author and Metadata Row -->
        <div class="metadata-row flex flex-wrap items-center justify-between gap-4 mb-6">
          <div class="author-section flex items-center gap-3">
            <!-- Author Avatar -->
            <div
              v-if="showAuthor && projectTeamOwner"
              class="author-avatar flex items-center"
            >
              <img
                v-if="projectTeamOwner.user?.avatarUrl"
                :src="projectTeamOwner.user.avatarUrl"
                :alt="projectTeamOwner.user.username"
                class="h-10 w-10 rounded-full"
              />
              <div
                v-else
                class="h-10 w-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center"
              >
                <span class="text-gray-500 dark:text-gray-400 font-medium">
                  {{ getInitials(projectTeamOwner.user?.username || '') }}
                </span>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {{ projectTeamOwner.user?.username || 'Unknown User' }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  {{ formatDate(project.createdAt) }}
                </p>
              </div>
            </div>
            
            <!-- Team Info -->
            <div
              v-if="showTeam && project.team && project.team.length > 0"
              class="team-info flex items-center"
            >
              <div class="flex -space-x-2">
                <div
                  v-for="(member, index) in visibleTeamMembers"
                  :key="member.user?.id || index"
                  class="team-member-avatar"
                >
                  <img
                    v-if="member.user?.avatarUrl"
                    :src="member.user.avatarUrl"
                    :alt="member.user.username"
                    class="h-8 w-8 rounded-full border-2 border-white dark:border-gray-900"
                  />
                  <div
                    v-else
                    class="h-8 w-8 rounded-full border-2 border-white dark:border-gray-900 bg-gray-300 dark:bg-gray-600 flex items-center justify-center"
                  >
                    <span class="text-xs text-gray-600 dark:text-gray-300 font-medium">
                      {{ getInitials(member.user?.username || '') }}
                    </span>
                  </div>
                </div>
                <div
                  v-if="hasMoreTeamMembers"
                  class="more-members h-8 w-8 rounded-full border-2 border-white dark:border-gray-900 bg-gray-100 dark:bg-gray-800 flex items-center justify-center"
                >
                  <span class="text-xs text-gray-600 dark:text-gray-300 font-medium">
                    +{{ moreMembersCount }}
                  </span>
                </div>
              </div>
              <span class="ml-2 text-sm text-gray-600 dark:text-gray-400">
                {{ teamSizeLabel }}
              </span>
            </div>
          </div>
        
        <!-- Stats Section -->
        <div
          v-if="showStats"
          class="stats-section flex items-center gap-6"
        >
          <!-- Views -->
          <div class="stat-item">
            <div class="stat-value text-lg font-semibold text-gray-900 dark:text-gray-100">
              {{ formatNumber(project.stats.views) }}
            </div>
            <div class="stat-label text-xs text-gray-500 dark:text-gray-400">
              Views
            </div>
          </div>
          
          <!-- Votes -->
          <div class="stat-item">
            <div class="stat-value text-lg font-semibold text-gray-900 dark:text-gray-100">
              {{ formatNumber(project.stats.votes) }}
            </div>
            <div class="stat-label text-xs text-gray-500 dark:text-gray-400">
              Votes
            </div>
          </div>
          
          <!-- Comments -->
          <div class="stat-item">
            <div class="stat-value text-lg font-semibold text-gray-900 dark:text-gray-100">
              {{ formatNumber(project.stats.comments) }}
            </div>
            <div class="stat-label text-xs text-gray-500 dark:text-gray-400">
              Comments
            </div>
          </div>
          
          <!-- Bookmarks -->
          <div class="stat-item">
            <div class="stat-value text-lg font-semibold text-gray-900 dark:text-gray-100">
              {{ formatNumber(project.stats.bookmarks) }}
            </div>
            <div class="stat-label text-xs text-gray-500 dark:text-gray-400">
              Saves
            </div>
          </div>
        </div>
      </div>
      
          <!-- Tags and Technologies -->
          <div
            v-if="showTags && (project.tags?.length > 0 || project.technologies?.length > 0)"
            class="tags-row mb-6"
          >
            <div class="flex flex-wrap gap-2">
              <!-- Technologies -->
              <ProjectTag
                v-for="tech in project.technologies"
                :key="tech.id"
                :tag="tech"
                :removable="false"
                size="md"
                class="technology-tag"
              />
              
              <!-- Tags -->
              <span
                v-for="tag in project.tags"
                :key="tag.id"
                class="tag inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300"
              >
                {{ tag.name }}
              </span>
            </div>
          </div>
      
      <!-- Description -->
      <div
        v-if="showDescription && project.description"
        class="description-row mb-6"
      >
        <p class="project-description text-gray-700 dark:text-gray-300 leading-relaxed">
          {{ project.description }}
        </p>
        <button
          v-if="showReadMore && project.description.length > 200"
          type="button"
          class="read-more mt-2 text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
          @click="toggleDescription"
        >
          {{ showFullDescription ? 'Show less' : 'Read more' }}
        </button>
      </div>
      
      <!-- Hackathon Info -->
      <div
        v-if="showHackathon && project.hackathonName"
        class="hackathon-row mb-6"
      >
        <div class="hackathon-card inline-flex items-center px-4 py-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-100 dark:border-blue-800">
          <svg
            class="mr-3 h-5 w-5 text-blue-600 dark:text-blue-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
          <div>
            <p class="text-sm font-medium text-blue-800 dark:text-blue-300">
              {{ project.hackathonName }}
            </p>
            <p
              v-if="project.deadline"
              class="text-xs text-blue-600 dark:text-blue-400"
            >
              Deadline: {{ formatDate(project.deadline) }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import type { Project, ProjectTeamMember, User } from '../../types/project-types'
import ProjectStatusBadge from '../atoms/ProjectStatusBadge.vue'
import ProjectShareButton from '../atoms/ProjectShareButton.vue'
import ProjectTag from '../atoms/ProjectTag.vue'

// Props
interface Props {
  project: Project
  showBreadcrumb?: boolean
  showVisibility?: boolean
  showLastUpdated?: boolean
  showActions?: boolean
  showEditButton?: boolean
  showBookmarkButton?: boolean
  showMoreActions?: boolean
  showReportButton?: boolean
  showDuplicateButton?: boolean
  showArchiveButton?: boolean
  showDeleteButton?: boolean
  showAuthor?: boolean
  showTeam?: boolean
  showStats?: boolean
  showTags?: boolean
  showDescription?: boolean
  showReadMore?: boolean
  showHackathon?: boolean
  canEdit?: boolean
  canDelete?: boolean
  isBookmarked?: boolean
  statusSize?: 'sm' | 'md' | 'lg'
  variant?: 'default' | 'compact' | 'expanded'
}

const props = withDefaults(defineProps<Props>(), {
  showBreadcrumb: true,
  showVisibility: true,
  showLastUpdated: true,
  showActions: true,
  showEditButton: true,
  showBookmarkButton: true,
  showMoreActions: true,
  showReportButton: true,
  showDuplicateButton: true,
  showArchiveButton: true,
  showDeleteButton: true,
  showAuthor: true,
  showTeam: true,
  showStats: true,
  showTags: true,
  showDescription: true,
  showReadMore: true,
  showHackathon: true,
  canEdit: false,
  canDelete: false,
  isBookmarked: false,
  statusSize: 'md',
  variant: 'default'
})

// Emits
const emit = defineEmits<{
  edit: [project: Project]
  share: [project: Project]
  bookmarkToggle: [project: Project, isBookmarked: boolean]
  report: [project: Project]
  duplicate: [project: Project]
  archive: [project: Project]
  delete: [project: Project]
}>()

// State
const showMoreMenu = ref(false)
const showFullDescription = ref(false)

// Computed
const headerClasses = computed(() => ({
  'project-details-header--compact': props.variant === 'compact',
  'project-details-header--expanded': props.variant === 'expanded'
}))

const visibilityClasses = computed(() => {
  if (props.project.visibility === 'public') {
    return 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
  } else if (props.project.visibility === 'private') {
    return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300'
  }
  return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300'
})

const visibilityLabel = computed(() => {
  if (props.project.visibility === 'public') return 'Public'
  if (props.project.visibility === 'private') return 'Private'
  return 'Restricted'
})

const bookmarkButtonClasses = computed(() => {
  const base = 'inline-flex items-center px-3 py-2 border rounded-lg text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2'
  if (props.isBookmarked) {
    return `${base} border-blue-300 dark:border-blue-700 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 hover:bg-blue-100 dark:hover:bg-blue-800/40 focus:ring-blue-500`
  }
  return `${base} border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 focus:ring-gray-500`
})

// Team-related computed properties
const projectTeamOwner = computed(() => {
  if (!props.project.team || props.project.team.length === 0) return null
  return props.project.team.find(member => member.role === 'owner') || props.project.team[0]
})

const visibleTeamMembers = computed(() => {
  if (!props.project.team || props.project.team.length === 0) return []
  return props.project.team.slice(0, 3)
})

const hasMoreTeamMembers = computed(() => {
  if (!props.project.team) return false
  return props.project.team.length > 3
})

const moreMembersCount = computed(() => {
  if (!props.project.team) return 0
  return props.project.team.length - 3
})

const teamSizeLabel = computed(() => {
  if (!props.project.team || props.project.team.length === 0) return 'No team'
  const count = props.project.team.length
  return `${count} member${count !== 1 ? 's' : ''}`
})

// Methods
const formatDate = (dateString: string | Date): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const formatNumber = (num: number): string => {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}

const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const toggleMoreActions = () => {
  showMoreMenu.value = !showMoreMenu.value
}

const toggleDescription = () => {
  showFullDescription.value = !showFullDescription.value
}

const handleEdit = () => {
  emit('edit', props.project)
}

const handleShare = () => {
  emit('share', props.project)
}

const handleBookmarkToggle = () => {
  emit('bookmarkToggle', props.project, !props.isBookmarked)
}

const handleReport = () => {
  emit('report', props.project)
}

const handleDuplicate = () => {
  emit('duplicate', props.project)
}

const handleArchive = () => {
  emit('archive', props.project)
}

const handleDelete = () => {
  emit('delete', props.project)
}

// Close dropdown when clicking outside
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.more-actions')) {
    showMoreMenu.value = false
  }
}

// Add event listener for click outside
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>