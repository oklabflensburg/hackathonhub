<template>
  <div class="project-list-atomic-wrapper">
    <!-- Atomic Design Version -->
    <ProjectsPageTemplate
      v-if="useAtomicComponents"
      ref="atomicTemplateRef"
      :page-title="pageTitle"
      :page-description="pageDescription"
      :projects="atomicProjects"
      :loading="loading"
      :error="error"
      :total-items="totalItems"
      :items-per-page="itemsPerPage"
      :filters="filters"
      :sort-options="sortOptions"
      :current-sort="currentSort"
      :show-header="showHeader"
      :show-header-actions="showHeaderActions"
      :show-search="showSearch"
      :show-create-button="showCreateButton"
      :show-view-controls="showViewControls"
      :show-view-toggle="showViewToggle"
      :show-sort="showSort"
      :show-filters="showFilters"
      :show-project-filters="showProjectFilters"
      :show-additional-filters="showAdditionalFilters"
      :show-pagination="showPagination"
      :show-footer="showFooter"
      :can-create="canCreate"
      :default-view-mode="defaultViewMode"
      :grid-columns="gridColumns"
      :empty-message="emptyMessage"
      :variant="variant"
      @search="handleSearch"
      @create="handleCreate"
      @view-mode-change="handleViewModeChange"
      @sort-change="handleSortChange"
      @filter-change="handleFilterChange"
      @clear-filters="handleClearFilters"
      @page-change="handlePageChange"
      @retry="handleRetry"
      @project-click="handleProjectClick"
      @project-vote="handleProjectVote"
      @project-comment="handleProjectComment"
      @project-share="handleProjectShare"
      @project-bookmark="handleProjectBookmark"
    >
      <!-- Additional Filters Slot -->
      <template v-if="$slots['additional-filters']" #additional-filters>
        <slot name="additional-filters" />
      </template>
      
      <!-- Loading Slot -->
      <template v-if="$slots.loading" #loading="slotProps">
        <slot name="loading" v-bind="slotProps" />
      </template>
      
      <!-- Error Slot -->
      <template v-if="$slots.error" #error="slotProps">
        <slot name="error" v-bind="slotProps" />
      </template>
      
      <!-- Empty Slot -->
      <template v-if="$slots.empty" #empty="slotProps">
        <slot name="empty" v-bind="slotProps" />
      </template>
      
      <!-- Footer Slot -->
      <template v-if="$slots.footer" #footer="slotProps">
        <slot name="footer" v-bind="slotProps" />
      </template>
    </ProjectsPageTemplate>
    
    <!-- Legacy Version -->
    <div v-else class="project-list-legacy-wrapper">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useFeatureFlags } from '~/composables/useFeatureFlags'
import ProjectsPageTemplate from '~/components/templates/ProjectsPageTemplate.vue'
import { 
  ProjectStatus,
  ProjectVisibility,
  type Project, 
  type ProjectFilterOptions,
  type ProjectTechnology
} from '~/types/project-types'

interface Props {
  // Page Configuration
  pageTitle?: string
  pageDescription?: string
  
  // Data
  projects: any[] // Legacy project format
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
  
  // Feature Flag Override
  forceAtomic?: boolean
  forceLegacy?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  pageTitle: 'Projects',
  pageDescription: '',
  
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
  
  variant: 'default',
  
  forceAtomic: false,
  forceLegacy: false
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
  projectClick: [project: any]
  projectVote: [project: any, voteValue: 1 | -1 | null]
  projectComment: [project: any]
  projectShare: [project: any]
  projectBookmark: [project: any, isBookmarked: boolean]
}>()

// Feature Flags
const featureFlags = useFeatureFlags()

// Refs
const atomicTemplateRef = ref<InstanceType<typeof ProjectsPageTemplate> | null>(null)

// Computed
const useAtomicComponents = computed(() => {
  if (props.forceAtomic) return true
  if (props.forceLegacy) return false
  return featureFlags.isEnabled('atomicProjectComponents')
})

// Convert legacy projects to atomic design format
const atomicProjects = computed<Project[]>(() => {
  return props.projects.map(convertLegacyProjectToAtomic)
})

// Methods
const convertLegacyProjectToAtomic = (legacyProject: any): Project => {
  // Map legacy project format to atomic design Project interface
  const status = mapLegacyStatusToProjectStatus(legacyProject.status)
  const visibility = mapLegacyVisibilityToProjectVisibility(legacyProject.visibility)
  
  return {
    id: String(legacyProject.id),
    title: legacyProject.name || legacyProject.title || 'Untitled Project',
    slug: legacyProject.slug || legacyProject.name?.toLowerCase().replace(/\s+/g, '-') || `project-${legacyProject.id}`,
    description: legacyProject.description || 'No description available.',
    shortDescription: legacyProject.shortDescription || legacyProject.description?.substring(0, 150) || '',
    status: status,
    visibility: visibility,
    featuredImage: legacyProject.image || legacyProject.imageUrl || '',
    galleryImages: legacyProject.galleryImages || [],
    
    // Metadaten
    createdAt: legacyProject.createdAt || new Date().toISOString(),
    updatedAt: legacyProject.updatedAt || new Date().toISOString(),
    publishedAt: legacyProject.publishedAt,
    deadline: legacyProject.deadline,
    
    // Beziehungen
    team: legacyProject.team || [],
    technologies: mapLegacyTechStackToTechnologies(legacyProject.techStack),
    tags: legacyProject.tags || [],
    hackathonId: legacyProject.hackathon_id ? String(legacyProject.hackathon_id) : undefined,
    hackathonName: legacyProject.hackathon_name,
    
    // Statistiken
    stats: {
      views: legacyProject.views || 0,
      votes: legacyProject.votes || 0,
      comments: legacyProject.comments || 0,
      shares: legacyProject.shares || 0,
      bookmarks: legacyProject.bookmarks || 0
    },
    
    // User-spezifische Daten
    userVote: legacyProject.hasVoted ? (legacyProject.voteValue || null) : null,
    isBookmarked: legacyProject.isBookmarked || false,
    isFollowing: legacyProject.isFollowing || false,
    
    // SEO
    metaTitle: legacyProject.metaTitle,
    metaDescription: legacyProject.metaDescription,
    keywords: legacyProject.keywords || []
  }
}

// Helper functions
const mapLegacyStatusToProjectStatus = (legacyStatus: string): ProjectStatus => {
  if (!legacyStatus) return ProjectStatus.ACTIVE
  
  const statusMap: Record<string, ProjectStatus> = {
    'draft': ProjectStatus.DRAFT,
    'active': ProjectStatus.ACTIVE,
    'completed': ProjectStatus.COMPLETED,
    'archived': ProjectStatus.ARCHIVED,
    'under_review': ProjectStatus.UNDER_REVIEW,
    'submitted': ProjectStatus.UNDER_REVIEW,
    'winner': ProjectStatus.COMPLETED,
    'finalist': ProjectStatus.COMPLETED
  }
  
  return statusMap[legacyStatus.toLowerCase()] || ProjectStatus.ACTIVE
}

const mapLegacyVisibilityToProjectVisibility = (legacyVisibility: string): ProjectVisibility => {
  if (!legacyVisibility) return ProjectVisibility.PUBLIC
  
  const visibilityMap: Record<string, ProjectVisibility> = {
    'public': ProjectVisibility.PUBLIC,
    'private': ProjectVisibility.PRIVATE,
    'team_only': ProjectVisibility.TEAM_ONLY
  }
  
  return visibilityMap[legacyVisibility.toLowerCase()] || ProjectVisibility.PUBLIC
}

const mapLegacyTechStackToTechnologies = (techStack: string[] | string): ProjectTechnology[] => {
  if (!techStack) return []
  
  const techArray = Array.isArray(techStack) ? techStack : 
                   typeof techStack === 'string' ? techStack.split(',').map(t => t.trim()) : []
  
  return techArray.map((tech, index) => ({
    id: `tech-${index}`,
    name: tech,
    slug: tech.toLowerCase().replace(/\s+/g, '-'),
    color: getColorForTechnology(tech)
  }))
}

const getColorForTechnology = (tech: string): string => {
  const colors = [
    '#3B82F6', // blue
    '#10B981', // emerald
    '#8B5CF6', // violet
    '#EF4444', // red
    '#F59E0B', // amber
    '#EC4899', // pink
    '#14B8A6', // teal
    '#F97316', // orange
    '#6366F1', // indigo
    '#84CC16'  // lime
  ]
  
  const hash = tech.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return colors[hash % colors.length] || '#3B82F6'
}

// Event Handlers
const handleSearch = (query: string) => {
  emit('search', query)
}

const handleCreate = () => {
  emit('create')
}

const handleViewModeChange = (mode: 'grid' | 'list') => {
  emit('viewModeChange', mode)
}

const handleSortChange = (sortOption: string) => {
  emit('sortChange', sortOption)
}

const handleFilterChange = (filters: ProjectFilterOptions) => {
  emit('filterChange', filters)
}

const handleClearFilters = () => {
  emit('clearFilters')
}

const handlePageChange = (page: number) => {
  emit('pageChange', page)
}

const handleRetry = () => {
  emit('retry')
}

const handleProjectClick = (project: Project) => {
  // Convert back to legacy format if needed
  const legacyProject = convertAtomicProjectToLegacy(project)
  emit('projectClick', legacyProject)
}

const handleProjectVote = (project: Project, voteValue: 1 | -1 | null) => {
  const legacyProject = convertAtomicProjectToLegacy(project)
  emit('projectVote', legacyProject, voteValue)
}

const handleProjectComment = (project: Project) => {
  const legacyProject = convertAtomicProjectToLegacy(project)
  emit('projectComment', legacyProject)
}

const handleProjectShare = (project: Project) => {
  const legacyProject = convertAtomicProjectToLegacy(project)
  emit('projectShare', legacyProject)
}

const handleProjectBookmark = (project: Project, isBookmarked: boolean) => {
  const legacyProject = convertAtomicProjectToLegacy(project)
  emit('projectBookmark', legacyProject, isBookmarked)
}

const convertAtomicProjectToLegacy = (atomicProject: Project): any => {
  // Convert atomic project back to legacy format
  const legacyStatus = mapProjectStatusToLegacyStatus(atomicProject.status)
  const legacyVisibility = mapProjectVisibilityToLegacyVisibility(atomicProject.visibility)
  const techStack = atomicProject.technologies.map(tech => tech.name)
  
  return {
    id: Number(atomicProject.id) || atomicProject.id,
    name: atomicProject.title,
    title: atomicProject.title,
    description: atomicProject.description,
    image: atomicProject.featuredImage,
    imageUrl: atomicProject.featuredImage,
    status: legacyStatus,
    team: atomicProject.team,
    techStack: techStack,
    votes: atomicProject.stats.votes,
    comments: atomicProject.stats.comments,
    views: atomicProject.stats.views,
    hasVoted: atomicProject.userVote !== null && atomicProject.userVote !== undefined,
    voteValue: atomicProject.userVote,
    isBookmarked: atomicProject.isBookmarked || false,
    owner_id: atomicProject.team.find(member => member.role === 'owner')?.user.id,
    hackathon_id: atomicProject.hackathonId,
    // Map other fields as needed
    tags: atomicProject.tags,
    links: [], // Not in atomic interface
    visibility: legacyVisibility,
    deadline: atomicProject.deadline,
    repositoryUrl: atomicProject.content?.match(/https?:\/\/[^\s]+/)?.[0] || '',
    demoUrl: '',
    documentationUrl: '',
    createdAt: atomicProject.createdAt,
    updatedAt: atomicProject.updatedAt,
    stats: atomicProject.stats
  }
}

// Helper functions for reverse mapping
const mapProjectStatusToLegacyStatus = (projectStatus: ProjectStatus): string => {
  const reverseMap: Record<ProjectStatus, string> = {
    [ProjectStatus.DRAFT]: 'draft',
    [ProjectStatus.ACTIVE]: 'active',
    [ProjectStatus.COMPLETED]: 'completed',
    [ProjectStatus.ARCHIVED]: 'archived',
    [ProjectStatus.UNDER_REVIEW]: 'submitted'
  }
  
  return reverseMap[projectStatus] || 'active'
}

const mapProjectVisibilityToLegacyVisibility = (projectVisibility: ProjectVisibility): string => {
  const reverseMap: Record<ProjectVisibility, string> = {
    [ProjectVisibility.PUBLIC]: 'public',
    [ProjectVisibility.PRIVATE]: 'private',
    [ProjectVisibility.TEAM_ONLY]: 'team_only'
  }
  
  return reverseMap[projectVisibility] || 'public'
}

// Expose methods if needed
defineExpose({
  getAtomicTemplate: () => atomicTemplateRef.value
})
</script>

<style scoped>
.project-list-atomic-wrapper {
  @apply w-full;
}

.project-list-legacy-wrapper {
  @apply w-full;
}
</style>