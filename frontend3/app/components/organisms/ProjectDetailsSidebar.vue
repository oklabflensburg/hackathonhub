<template>
  <aside class="project-details-sidebar" :class="sidebarClasses">
    <!-- Sidebar Header -->
    <div v-if="showHeader" class="sidebar-header mb-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
        {{ headerTitle }}
      </h3>
      <p v-if="headerDescription" class="mt-1 text-sm text-gray-500 dark:text-gray-400">
        {{ headerDescription }}
      </p>
    </div>
    
    <!-- Quick Actions -->
    <div v-if="showQuickActions" class="quick-actions mb-6">
      <h4 class="mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">
        Quick Actions
      </h4>
      <div class="space-y-2">
        <!-- Vote Button -->
        <ProjectVoteButton
          v-if="showVoteButton"
          :project-id="project.id"
          :initial-vote="project.userVote"
          :vote-count="project.stats.votes"
          size="md"
          variant="primary"
          class="w-full"
          @vote="handleVote"
        />
        
        <!-- Comment Button -->
        <ProjectCommentButton
          v-if="showCommentButton"
          :project-id="project.id"
          :comment-count="project.stats.comments"
          size="md"
          variant="secondary"
          class="w-full"
          @click="handleComment"
        />
        
        <!-- Share Button -->
        <ProjectShareButton
          v-if="showShareButton"
          :project="project"
          size="md"
          variant="secondary"
          class="w-full"
          @click="handleShare"
        />
        
        <!-- Bookmark Button -->
        <button
          v-if="showBookmarkButton"
          type="button"
          class="bookmark-button w-full inline-flex items-center justify-center px-4 py-2 border rounded-lg text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2"
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
          {{ isBookmarked ? 'Saved' : 'Save for later' }}
        </button>
      </div>
    </div>
    
    <!-- Project Stats -->
    <div v-if="showStats" class="project-stats mb-6">
      <h4 class="mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">
        Project Stats
      </h4>
      <div class="stats-grid grid grid-cols-2 gap-3">
        <!-- Views -->
        <div class="stat-item p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <div class="stat-value text-xl font-bold text-gray-900 dark:text-gray-100">
            {{ formatNumber(project.stats.views) }}
          </div>
          <div class="stat-label text-xs text-gray-500 dark:text-gray-400">
            Views
          </div>
        </div>
        
        <!-- Votes -->
        <div class="stat-item p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <div class="stat-value text-xl font-bold text-gray-900 dark:text-gray-100">
            {{ formatNumber(project.stats.votes) }}
          </div>
          <div class="stat-label text-xs text-gray-500 dark:text-gray-400">
            Votes
          </div>
        </div>
        
        <!-- Comments -->
        <div class="stat-item p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <div class="stat-value text-xl font-bold text-gray-900 dark:text-gray-100">
            {{ formatNumber(project.stats.comments) }}
          </div>
          <div class="stat-label text-xs text-gray-500 dark:text-gray-400">
            Comments
          </div>
        </div>
        
        <!-- Bookmarks -->
        <div class="stat-item p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <div class="stat-value text-xl font-bold text-gray-900 dark:text-gray-100">
            {{ formatNumber(project.stats.bookmarks) }}
          </div>
          <div class="stat-label text-xs text-gray-500 dark:text-gray-400">
            Saves
          </div>
        </div>
      </div>
    </div>
    
    <!-- Project Metadata -->
    <div v-if="showMetadata" class="project-metadata mb-6">
      <h4 class="mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">
        Project Details
      </h4>
      <div class="metadata-list space-y-3">
        <!-- Status -->
        <div class="metadata-item flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-400">
            Status
          </span>
          <ProjectStatusBadge
            :status="project.status"
            size="sm"
            :show-label="true"
          />
        </div>
        
        <!-- Visibility -->
        <div v-if="showVisibility" class="metadata-item flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-400">
            Visibility
          </span>
          <span
            class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
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
        </div>
        
        <!-- Created Date -->
        <div class="metadata-item flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-400">
            Created
          </span>
          <span class="text-sm text-gray-900 dark:text-gray-300">
            {{ formatDate(project.createdAt) }}
          </span>
        </div>
        
        <!-- Updated Date -->
        <div v-if="project.updatedAt" class="metadata-item flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-400">
            Updated
          </span>
          <span class="text-sm text-gray-900 dark:text-gray-300">
            {{ formatDate(project.updatedAt) }}
          </span>
        </div>
        
        <!-- Deadline -->
        <div v-if="project.deadline" class="metadata-item flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-400">
            Deadline
          </span>
          <span class="text-sm text-gray-900 dark:text-gray-300">
            {{ formatDate(project.deadline) }}
          </span>
        </div>
        
        <!-- Hackathon -->
        <div v-if="project.hackathonName" class="metadata-item flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-400">
            Hackathon
          </span>
          <span class="text-sm text-gray-900 dark:text-gray-300">
            {{ project.hackathonName }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- Team Members -->
    <div v-if="showTeam && project.team && project.team.length > 0" class="team-members mb-6">
      <h4 class="mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">
        Team Members
      </h4>
      <div class="team-list space-y-3">
        <div
          v-for="(member, index) in project.team"
          :key="member.user?.id || index"
          class="team-member flex items-center"
        >
          <!-- Avatar -->
          <div class="avatar mr-3">
            <img
              v-if="member.user?.avatarUrl || member.user?.avatar_url"
              :src="member.user?.avatarUrl || member.user?.avatar_url"
              :alt="member.user.username"
              class="h-8 w-8 rounded-full"
            />
            <div
              v-else
              class="h-8 w-8 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center"
            >
              <span class="text-xs text-gray-600 dark:text-gray-300 font-medium">
                {{ getInitials(member.user?.username || '') }}
              </span>
            </div>
          </div>
          
          <!-- Member Info -->
          <div class="member-info flex-1">
            <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
              {{ member.user?.username || 'Unknown User' }}
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              {{ member.role }}
            </p>
          </div>
          
          <!-- Joined Date -->
          <div class="joined-date text-xs text-gray-500 dark:text-gray-400">
            {{ formatDateShort(member.joinedAt) }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- Technologies -->
    <div v-if="showTechnologies && project.technologies && project.technologies.length > 0" class="technologies mb-6">
      <h4 class="mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">
        Technologies
      </h4>
      <div class="tech-list flex flex-wrap gap-2">
        <ProjectTag
          v-for="tech in project.technologies"
          :key="tech.id"
          :tag="tech"
          :removable="false"
          size="sm"
        />
      </div>
    </div>
    
    <!-- Related Projects -->
    <div v-if="showRelatedProjects && relatedProjects && relatedProjects.length > 0" class="related-projects">
      <h4 class="mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">
        Related Projects
      </h4>
      <div class="related-list space-y-3">
        <div
          v-for="relatedProject in relatedProjects"
          :key="relatedProject.id"
          class="related-project p-3 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors cursor-pointer"
          @click="handleRelatedProjectClick(relatedProject)"
        >
          <p class="text-sm font-medium text-gray-900 dark:text-gray-100 mb-1">
            {{ relatedProject.title }}
          </p>
          <div class="flex items-center justify-between">
            <ProjectStatusBadge
              :status="relatedProject.status"
              size="sm"
              :show-label="true"
            />
            <span class="text-xs text-gray-500 dark:text-gray-400">
              {{ formatNumber(relatedProject.stats.views) }} views
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Sidebar Footer -->
    <div v-if="showFooter" class="sidebar-footer mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
      <div class="footer-content text-xs text-gray-500 dark:text-gray-400">
        <p v-if="footerText">{{ footerText }}</p>
        <div class="footer-links mt-2 space-x-3">
          <button
            v-if="showReportButton"
            type="button"
            class="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300"
            @click="handleReport"
          >
            Report
          </button>
          <button
            v-if="showEditButton && canEdit"
            type="button"
            class="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
            @click="handleEdit"
          >
            Edit
          </button>
          <button
            v-if="showDuplicateButton && canEdit"
            type="button"
            class="text-green-600 dark:text-green-400 hover:text-green-800 dark:hover:text-green-300"
            @click="handleDuplicate"
          >
            Duplicate
          </button>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Project } from '../../types/project-types'
import ProjectVoteButton from '../atoms/ProjectVoteButton.vue'
import ProjectCommentButton from '../atoms/ProjectCommentButton.vue'
import ProjectShareButton from '../atoms/ProjectShareButton.vue'
import ProjectStatusBadge from '../atoms/ProjectStatusBadge.vue'
import ProjectTag from '../atoms/ProjectTag.vue'

// Props
interface Props {
  project: Project
  relatedProjects?: Project[]
  showHeader?: boolean
  showQuickActions?: boolean
  showStats?: boolean
  showMetadata?: boolean
  showTeam?: boolean
  showTechnologies?: boolean
  showRelatedProjects?: boolean
  showFooter?: boolean
  showVoteButton?: boolean
  showCommentButton?: boolean
  showShareButton?: boolean
  showBookmarkButton?: boolean
  showVisibility?: boolean
  showReportButton?: boolean
  showEditButton?: boolean
  showDuplicateButton?: boolean
  headerTitle?: string
  headerDescription?: string
  footerText?: string
  canEdit?: boolean
  isBookmarked?: boolean
  variant?: 'default' | 'compact' | 'sticky'
}

const props = withDefaults(defineProps<Props>(), {
  relatedProjects: () => [],
  showHeader: true,
  showQuickActions: true,
  showStats: true,
  showMetadata: true,
  showTeam: true,
  showTechnologies: true,
  showRelatedProjects: false,
  showFooter: true,
  showVoteButton: true,
  showCommentButton: true,
  showShareButton: true,
  showBookmarkButton: true,
  showVisibility: true,
  showReportButton: true,
  showEditButton: true,
  showDuplicateButton: true,
  headerTitle: 'Project Details',
  headerDescription: '',
  footerText: '',
  canEdit: false,
  isBookmarked: false,
  variant: 'default'
})

// Emits
const emit = defineEmits<{
  vote: [project: Project, voteValue: 1 | -1 | null]
  comment: [project: Project]
  share: [project: Project]
  bookmarkToggle: [project: Project, isBookmarked: boolean]
  report: [project: Project]
  edit: [project: Project]
  duplicate: [project: Project]
  relatedProjectClick: [project: Project]
}>()

// Computed
const sidebarClasses = computed(() => ({
  'project-details-sidebar--compact': props.variant === 'compact',
  'project-details-sidebar--sticky': props.variant === 'sticky',
  'sticky top-6': props.variant === 'sticky'
}))

const bookmarkButtonClasses = computed(() => {
  const base = 'w-full inline-flex items-center justify-center px-4 py-2 border rounded-lg text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2'
  if (props.isBookmarked) {
    return `${base} border-blue-300 dark:border-blue-700 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 hover:bg-blue-100 dark:hover:bg-blue-800/40 focus:ring-blue-500`
  }
  return `${base} border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 focus:ring-gray-500`
})

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

// Methods
const formatDate = (dateString: string | Date): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const formatDateShort = (dateString: string | Date): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
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

// Event Handlers
const handleVote = (_projectId: string, voteType: 'up' | 'down') => {
  emit('vote', props.project, voteType === 'up' ? 1 : -1)
}

const handleComment = () => {
  emit('comment', props.project)
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

const handleEdit = () => {
  emit('edit', props.project)
}

const handleDuplicate = () => {
  emit('duplicate', props.project)
}

const handleRelatedProjectClick = (relatedProject: Project) => {
  emit('relatedProjectClick', relatedProject)
}
</script>
