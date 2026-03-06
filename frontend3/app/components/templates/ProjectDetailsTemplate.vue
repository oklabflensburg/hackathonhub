<template>
  <div class="project-details-template" :class="templateClasses">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <slot name="loading">
        <div class="flex flex-col items-center justify-center min-h-[400px]">
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
            Loading project details...
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
              Error loading project
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
    
    <!-- Project Details Content -->
    <div v-else-if="project" class="project-details-content">
      <!-- Project Header -->
      <div class="project-header mb-8">
        <ProjectDetailsHeader
          :project="project"
          :show-breadcrumb="showBreadcrumb"
          :show-visibility="showVisibility"
          :show-last-updated="showLastUpdated"
          :show-actions="showActions"
          :show-edit-button="showEditButton"
          :show-bookmark-button="showBookmarkButton"
          :show-more-actions="showMoreActions"
          :show-author="showAuthor"
          :show-team="showTeam"
          :show-stats="showStats"
          :show-tags="showTags"
          :show-description="showDescription"
          :show-hackathon="showHackathon"
          :can-edit="canEdit"
          :can-delete="canDelete"
          :is-bookmarked="isBookmarked"
          :variant="headerVariant"
          @edit="handleEdit"
          @share="handleShare"
          @bookmark-toggle="handleBookmarkToggle"
          @report="handleReport"
          @duplicate="handleDuplicate"
          @archive="handleArchive"
          @delete="handleDelete"
        />
      </div>
      
      <!-- Main Content Area -->
      <div class="main-content-area">
        <div class="content-wrapper" :class="contentWrapperClasses">
          <!-- Main Content -->
          <main class="main-content flex-1">
            <!-- Content Tabs -->
            <div v-if="showTabs" class="content-tabs mb-6">
              <nav class="tabs-navigation border-b border-gray-200 dark:border-gray-700">
                <div class="flex space-x-8">
                  <button
                    v-for="tab in tabs"
                    :key="tab.id"
                    type="button"
                    class="tab-button py-3 px-1 border-b-2 text-sm font-medium transition-colors"
                    :class="activeTab === tab.id ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'"
                    @click="setActiveTab(tab.id)"
                  >
                    {{ tab.label }}
                    <span
                      v-if="tab.badge"
                      class="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                      :class="tab.badgeClass"
                    >
                      {{ tab.badge }}
                    </span>
                  </button>
                </div>
              </nav>
            </div>
            
            <!-- Tab Content -->
            <div class="tab-content">
              <!-- Overview Tab -->
              <div v-if="activeTab === 'overview'" class="overview-tab">
                <slot name="overview">
                  <!-- Project Description -->
                  <div v-if="project.content" class="project-description mb-8">
                    <div class="prose dark:prose-invert max-w-none">
                      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
                        Project Description
                      </h2>
                      <div class="content" v-html="project.content" />
                    </div>
                  </div>
                  
                  <!-- Project Gallery -->
                  <div v-if="showGallery && project.galleryImages && project.galleryImages.length > 0" class="project-gallery mb-8">
                    <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
                      Project Gallery
                    </h2>
                    <div class="gallery-grid grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                      <div
                        v-for="(image, index) in project.galleryImages"
                        :key="index"
                        class="gallery-item relative aspect-[16/9] rounded-lg overflow-hidden bg-gray-100 dark:bg-gray-800 cursor-pointer"
                        @click="openGallery(index)"
                      >
                        <img
                          :src="image"
                          :alt="`Project image ${index + 1}`"
                          class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                        />
                        <div class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-10 transition-opacity duration-300" />
                      </div>
                    </div>
                  </div>
                  
                  <!-- Project Timeline -->
                  <div v-if="showTimeline" class="project-timeline mb-8">
                    <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
                      Project Timeline
                    </h2>
                    <div class="timeline">
                      <slot name="timeline">
                        <div class="timeline-item p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                          <p class="text-gray-600 dark:text-gray-400">
                            Timeline content goes here...
                          </p>
                        </div>
                      </slot>
                    </div>
                  </div>
                  
                  <!-- Project Updates -->
                  <div v-if="showUpdates" class="project-updates mb-8">
                    <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
                      Project Updates
                    </h2>
                    <div class="updates-list">
                      <slot name="updates">
                        <div class="update-item p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                          <p class="text-gray-600 dark:text-gray-400">
                            Updates content goes here...
                          </p>
                        </div>
                      </slot>
                    </div>
                  </div>
                </slot>
              </div>
              
              <!-- Team Tab -->
              <div v-else-if="activeTab === 'team'" class="team-tab">
                <slot name="team">
                  <div class="team-content">
                    <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">
                      Project Team
                    </h2>
                    <div class="team-members-list">
                      <slot name="team-members">
                        <div class="team-members-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                          <div
                            v-for="member in project.team"
                            :key="member.user?.id"
                            class="team-member-card p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
                          >
                            <div class="flex items-center mb-4">
                              <div class="avatar mr-4">
                                <img
                                  v-if="member.user?.avatarUrl"
                                  :src="member.user.avatarUrl"
                                  :alt="member.user.username"
                                  class="h-12 w-12 rounded-full"
                                />
                                <div
                                  v-else
                                  class="h-12 w-12 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center"
                                >
                                  <span class="text-gray-600 dark:text-gray-300 font-medium">
                                    {{ getInitials(member.user?.username || '') }}
                                  </span>
                                </div>
                              </div>
                              <div>
                                <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
                                  {{ member.user?.username || 'Unknown User' }}
                                </h3>
                                <p class="text-sm text-gray-500 dark:text-gray-400">
                                  {{ member.role }}
                                </p>
                              </div>
                            </div>
                            <div class="member-meta text-sm text-gray-600 dark:text-gray-400">
                              <p class="mb-1">
                                Joined: {{ formatDate(member.joinedAt) }}
                              </p>
                              <p v-if="member.user?.bio" class="mt-2">
                                {{ member.user.bio }}
                              </p>
                            </div>
                          </div>
                        </div>
                      </slot>
                    </div>
                  </div>
                </slot>
              </div>
              
              <!-- Comments Tab -->
              <div v-else-if="activeTab === 'comments'" class="comments-tab">
                <slot name="comments">
                  <div class="comments-content">
                    <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">
                      Comments ({{ project.stats.comments }})
                    </h2>
                    <div class="comments-section">
                      <slot name="comments-list">
                        <div class="comments-list">
                          <p class="text-gray-600 dark:text-gray-400">
                            Comments functionality would be implemented here...
                          </p>
                        </div>
                      </slot>
                    </div>
                  </div>
                </slot>
              </div>
              
              <!-- Custom Tab Content -->
              <div v-else class="custom-tab">
                <slot :name="`tab-${activeTab}`">
                  <div class="custom-tab-content p-6 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <p class="text-gray-600 dark:text-gray-400">
                      Content for {{ activeTab }} tab
                    </p>
                  </div>
                </slot>
              </div>
            </div>
          </main>
          
          <!-- Sidebar -->
          <aside v-if="showSidebar" class="sidebar" :class="sidebarClasses">
            <ProjectDetailsSidebar
              :project="project"
              :related-projects="relatedProjects"
              :show-header="showSidebarHeader"
              :show-quick-actions="showQuickActions"
              :show-stats="showSidebarStats"
              :show-metadata="showSidebarMetadata"
              :show-team="showSidebarTeam"
              :show-technologies="showSidebarTechnologies"
              :show-related-projects="showRelatedProjects"
              :show-footer="showSidebarFooter"
              :show-vote-button="showVoteButton"
              :show-comment-button="showCommentButton"
              :show-share-button="showShareButton"
              :show-bookmark-button="showBookmarkButton"
              :show-visibility="showSidebarVisibility"
              :show-report-button="showReportButton"
              :show-edit-button="showEditButton"
              :show-duplicate-button="showDuplicateButton"
              :header-title="sidebarHeaderTitle"
              :footer-text="sidebarFooterText"
              :can-edit="canEdit"
              :is-bookmarked="isBookmarked"
              :variant="sidebarVariant"
              @vote="handleVote"
              @comment="handleComment"
              @share="handleShare"
              @bookmark-toggle="handleBookmarkToggle"
              @report="handleReport"
              @edit="handleEdit"
              @duplicate="handleDuplicate"
              @related-project-click="handleRelatedProjectClick"
            />
            
            <!-- Additional Sidebar Content -->
            <div v-if="showAdditionalSidebar" class="additional-sidebar mt-6">
              <slot name="additional-sidebar" />
            </div>
          </aside>
        </div>
      </div>
      
      <!-- Related Projects -->
      <div v-if="showRelatedProjectsSection && relatedProjects && relatedProjects.length > 0" class="related-projects-section mt-12">
        <div class="section-header mb-6">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Related Projects
          </h2>
          <p class="text-gray-600 dark:text-gray-400 mt-2">
            Other projects you might be interested in
          </p>
        </div>
        <ProjectList
          :projects="relatedProjects"
          view-mode="grid"
          :columns="3"
          :gap="6"
          @project-click="handleRelatedProjectClick"
          @project-vote="handleProjectVote"
          @project-comment="handleProjectComment"
          @project-share="handleProjectShare"
          @project-bookmark="handleProjectBookmark"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Project } from '../../types/project-types'
import ProjectDetailsHeader from '../organisms/ProjectDetailsHeader.vue'
import ProjectDetailsSidebar from '../organisms/ProjectDetailsSidebar.vue'
import ProjectList from '../organisms/ProjectList.vue'

// Props
interface Props {
  // Project Data
  project?: Project | null
  relatedProjects?: Project[]
  loading?: boolean
  error?: string | null
  
  // Header Configuration
  showBreadcrumb?: boolean
  showVisibility?: boolean
  showLastUpdated?: boolean
  showActions?: boolean
  showEditButton?: boolean
  showBookmarkButton?: boolean
  showMoreActions?: boolean
  showAuthor?: boolean
  showTeam?: boolean
  showStats?: boolean
  showTags?: boolean
  showDescription?: boolean
  showHackathon?: boolean
  headerVariant?: 'default' | 'compact' | 'expanded'
  
  // Tabs Configuration
  showTabs?: boolean
  tabs?: Array<{
    id: string
    label: string
    badge?: string | number
    badgeClass?: string
  }>
  defaultTab?: string
  
  // Content Configuration
  showGallery?: boolean
  showTimeline?: boolean
  showUpdates?: boolean
  
  // Sidebar Configuration
  showSidebar?: boolean
  showSidebarHeader?: boolean
  showQuickActions?: boolean
  showSidebarStats?: boolean
  showSidebarMetadata?: boolean
  showSidebarTeam?: boolean
  showSidebarTechnologies?: boolean
  showSidebarVisibility?: boolean
  showVoteButton?: boolean
  showCommentButton?: boolean
  showShareButton?: boolean
  showReportButton?: boolean
  showDuplicateButton?: boolean
  showSidebarFooter?: boolean
  showAdditionalSidebar?: boolean
  sidebarHeaderTitle?: string
  sidebarFooterText?: string
  sidebarVariant?: 'default' | 'compact' | 'sticky'
  
  // Related Projects
  showRelatedProjects?: boolean
  showRelatedProjectsSection?: boolean
  
  // User Permissions
  canEdit?: boolean
  canDelete?: boolean
  isBookmarked?: boolean
  
  // Layout Variant
  variant?: 'default' | 'sidebar-left' | 'sidebar-right' | 'full-width'
}

const props = withDefaults(defineProps<Props>(), {
  project: null,
  relatedProjects: () => [],
  loading: false,
  error: null,
  
  showBreadcrumb: true,
  showVisibility: true,
  showLastUpdated: true,
  showActions: true,
  showEditButton: true,
  showBookmarkButton: true,
  showMoreActions: true,
  showAuthor: true,
  showTeam: true,
  showStats: true,
  showTags: true,
  showDescription: true,
  showHackathon: true,
  headerVariant: 'default',
  
  showTabs: true,
  tabs: () => [
    { id: 'overview', label: 'Overview' },
    { id: 'team', label: 'Team' },
    { id: 'comments', label: 'Comments', badgeClass: 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300' },
  ],
  defaultTab: 'overview',
  
  showGallery: true,
  showTimeline: true,
  showUpdates: true,
  
  showSidebar: true,
  showSidebarHeader: true,
  showQuickActions: true,
  showSidebarStats: true,
  showSidebarMetadata: true,
  showSidebarTeam: true,
  showSidebarTechnologies: true,
  showSidebarVisibility: true,
  showVoteButton: true,
  showCommentButton: true,
  showShareButton: true,
  showReportButton: true,
  showDuplicateButton: true,
  showSidebarFooter: true,
  showAdditionalSidebar: false,
  sidebarHeaderTitle: 'Project Details',
  sidebarFooterText: '',
  sidebarVariant: 'sticky',
  
  showRelatedProjects: true,
  showRelatedProjectsSection: true,
  
  canEdit: false,
  canDelete: false,
  isBookmarked: false,
  
  variant: 'default'
})

// Emits
const emit = defineEmits<{
  retry: []
  edit: [project: Project]
  share: [project: Project]
  bookmarkToggle: [project: Project, isBookmarked: boolean]
  report: [project: Project]
  duplicate: [project: Project]
  archive: [project: Project]
  delete: [project: Project]
  vote: [project: Project, voteValue: 1 | -1 | null]
  comment: [project: Project]
  relatedProjectClick: [project: Project]
  projectVote: [project: Project, voteValue: 1 | -1 | null]
  projectComment: [project: Project]
  projectShare: [project: Project]
  projectBookmark: [project: Project, isBookmarked: boolean]
  tabChange: [tabId: string]
  galleryOpen: [index: number]
}>()

// State
const activeTab = ref(props.defaultTab)

// Computed
const templateClasses = computed(() => ({
  'project-details-template--sidebar-left': props.variant === 'sidebar-left',
  'project-details-template--sidebar-right': props.variant === 'sidebar-right',
  'project-details-template--full-width': props.variant === 'full-width'
}))

const contentWrapperClasses = computed(() => ({
  'flex flex-col lg:flex-row gap-8': props.showSidebar,
  'flex flex-col': !props.showSidebar
}))

const sidebarClasses = computed(() => ({
  'lg:w-80': props.variant === 'default' || props.variant === 'sidebar-right',
  'lg:w-64': props.variant === 'sidebar-left'
}))

// Methods
const handleRetry = () => {
  emit('retry')
}

const handleEdit = (project: Project) => {
  emit('edit', project)
}

const handleShare = (project: Project) => {
  emit('share', project)
}

const handleBookmarkToggle = (project: Project, isBookmarked: boolean) => {
  emit('bookmarkToggle', project, isBookmarked)
}

const handleReport = (project: Project) => {
  emit('report', project)
}

const handleDuplicate = (project: Project) => {
  emit('duplicate', project)
}

const handleArchive = () => {
  if (props.project) {
    emit('archive', props.project)
  }
}

const handleDelete = () => {
  if (props.project) {
    emit('delete', props.project)
  }
}

const handleVote = (project: Project, voteValue: 1 | -1 | null) => {
  emit('vote', project, voteValue)
}

const handleComment = (project: Project) => {
  emit('comment', project)
}

const handleRelatedProjectClick = (relatedProject: Project) => {
  emit('relatedProjectClick', relatedProject)
}

const handleProjectVote = (project: Project, voteType: 'up' | 'down') => {
  const voteValue = voteType === 'up' ? 1 : -1
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

const setActiveTab = (tabId: string) => {
  activeTab.value = tabId
  emit('tabChange', tabId)
}

const openGallery = (index: number) => {
  emit('galleryOpen', index)
}

const formatDate = (dateString: string | Date): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}
</script>

<style scoped>
.project-details-template {
  @apply min-h-screen bg-gray-50 dark:bg-gray-900;
}

.project-details-content {
  @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8;
}

.project-details-template--sidebar-left .content-wrapper {
  @apply flex flex-col lg:flex-row-reverse gap-8;
}

.project-details-template--sidebar-right .content-wrapper {
  @apply flex flex-col lg:flex-row gap-8;
}

.project-details-template--full-width .sidebar {
  @apply hidden;
}

.main-content {
  @apply min-w-0;
}

.sidebar {
  @apply lg:w-80 flex-shrink-0;
}

.loading-state,
.error-state {
  @apply min-h-[400px] flex items-center justify-center;
}

.tabs-navigation {
  @apply border-b border-gray-200 dark:border-gray-700;
}

.tab-button {
  @apply py-3 px-1 border-b-2 text-sm font-medium transition-colors;
}

.gallery-grid {
  @apply grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4;
}

.gallery-item {
  @apply relative aspect-[16/9] rounded-lg overflow-hidden bg-gray-100 dark:bg-gray-800 cursor-pointer;
}

.team-members-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6;
}

.team-member-card {
  @apply p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700;
}

.related-projects-section {
  @apply mt-12 pt-8 border-t border-gray-200 dark:border-gray-700;
}
</style>
