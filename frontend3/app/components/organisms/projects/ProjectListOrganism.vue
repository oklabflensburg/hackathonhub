<template>
  <div class="project-list-organism">
    <!-- Header with search and actions -->
    <div class="mb-6">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div class="flex-1">
          <SearchBar
            :model-value="searchQuery"
            :placeholder="searchPlaceholder"
            :debounce="300"
            class="w-full md:w-auto"
            @update:model-value="$emit('update:searchQuery', $event)"
            @search="handleSearch"
          />
        </div>
        
        <div class="flex items-center gap-3">
          <slot name="actions">
            <!-- Default action: Submit Project button -->
            <Button
              v-if="showSubmitButton"
              variant="primary"
              size="md"
              :loading="submitting"
              @click="handleSubmitProject"
            >
              <template #icon>
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </template>
              {{ submitButtonText }}
            </Button>
          </slot>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="py-12">
      <div class="flex flex-col items-center justify-center">
        <LoadingSpinner size="lg" />
        <p class="mt-4 text-gray-600 dark:text-gray-400">{{ loadingText }}</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="py-12">
      <div class="text-center">
        <div class="mx-auto w-16 h-16 text-red-500 mb-4">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">{{ errorTitle }}</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
        <Button variant="secondary" @click="handleRetry">
          {{ retryButtonText }}
        </Button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredProjects.length === 0" class="py-12">
      <div class="text-center">
        <div class="mx-auto w-16 h-16 text-gray-400 mb-4">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">{{ emptyTitle }}</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">{{ emptyDescription }}</p>
        <Button v-if="showSubmitButton" variant="primary" @click="handleSubmitProject">
          {{ submitButtonText }}
        </Button>
      </div>
    </div>

    <!-- Projects Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <slot name="project-card" :projects="filteredProjects" :can-edit="canEditProject">
        <!-- Default project card slot -->
        <ProjectListCard
          v-for="project in filteredProjects"
          :key="project.id"
          :project="{
            id: project.id,
            name: project.name,
            description: project.description,
            image: project.image,
            status: project.status,
            author: project.team?.[0]?.name || 'Unknown',
            tech: project.techStack,
            views: project.views,
            comments: project.comments,
            upvotes: project.votes,
            downvotes: 0,
            userVote: null,
            demo: false,
            github: ''
          }"
          :liveDemoLabel="'Live Demo'"
          :prototypeLabel="'Prototype'"
          :githubTitle="'GitHub Repository'"
          :viewsLabel="'Views'"
          :commentsLabel="'Comments'"
          @open="handleViewProject"
        />
      </slot>
    </div>

    <!-- Pagination -->
    <div v-if="showPagination && totalPages > 1" class="mt-8">
      <Pagination
        :total="totalItems"
        :per-page="itemsPerPage"
        :current-page="currentPage"
        @page-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Button, Input, LoadingSpinner } from '@/components/atoms'
import { SearchBar, Pagination } from '@/components/molecules'
import ProjectListCard from './ProjectListCard.vue'

// Props
interface Project {
  id: number
  name: string
  description: string
  image: string
  status: string
  team: Array<{ id: number; name: string }>
  techStack: string[]
  votes: number
  comments: number
  views: number
  owner_id?: number
  hackathon_id?: number
}

interface Props {
  projects: Project[]
  loading?: boolean
  error?: string | null
  searchQuery?: string
  searchPlaceholder?: string
  showSubmitButton?: boolean
  submitButtonText?: string
  loadingText?: string
  errorTitle?: string
  retryButtonText?: string
  emptyTitle?: string
  emptyDescription?: string
  showPagination?: boolean
  totalItems?: number
  itemsPerPage?: number
  currentPage?: number
  userId?: number | null
  hackathonId?: number | null
  isHackathonMember?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  projects: () => [],
  loading: false,
  error: null,
  searchQuery: '',
  searchPlaceholder: 'Search projects...',
  showSubmitButton: true,
  submitButtonText: 'Submit Project',
  loadingText: 'Loading projects...',
  errorTitle: 'Failed to load projects',
  retryButtonText: 'Try Again',
  emptyTitle: 'No projects found',
  emptyDescription: 'Be the first to submit a project for this hackathon!',
  showPagination: false,
  totalItems: 0,
  itemsPerPage: 12,
  currentPage: 1,
  userId: null,
  hackathonId: null,
  isHackathonMember: false
})

// Emits
const emit = defineEmits<{
  'update:searchQuery': [value: string]
  'search': [query: string]
  'submit-project': []
  'retry': []
  'view-project': [projectId: number]
  'edit-project': [project: Project]
  'page-change': [page: number]
}>()

// Local state
const localSearchQuery = ref(props.searchQuery)
const submitting = ref(false)

// Computed
const filteredProjects = computed(() => {
  if (!localSearchQuery.value) return props.projects

  const query = localSearchQuery.value.toLowerCase()
  return props.projects.filter(project =>
    project.name.toLowerCase().includes(query) ||
    project.description.toLowerCase().includes(query) ||
    project.techStack.some(tech => tech.toLowerCase().includes(query))
  )
})

const totalPages = computed(() => {
  return Math.ceil(props.totalItems / props.itemsPerPage)
})

// Methods
const handleSearch = (query: string) => {
  emit('search', query)
}

const handleSubmitProject = () => {
  submitting.value = true
  emit('submit-project')
  // Reset loading state after a short delay (simulate async)
  setTimeout(() => {
    submitting.value = false
  }, 500)
}

const handleRetry = () => {
  emit('retry')
}

const handleViewProject = (projectId: number) => {
  emit('view-project', projectId)
}

const handleEditProject = (project: Project) => {
  emit('edit-project', project)
}

const handlePageChange = (page: number) => {
  emit('page-change', page)
}

const canEditProject = (project: Project): boolean => {
  if (!props.userId || !project) return false

  // Check if user is the project owner
  const isOwner = props.userId === project.owner_id
  if (isOwner) return true

  // Check if user is a hackathon team member
  if (project.hackathon_id && props.hackathonId && 
      project.hackathon_id === props.hackathonId) {
    return props.isHackathonMember
  }
  
  return false
}

// Watch for prop changes
watch(() => props.searchQuery, (newVal) => {
  localSearchQuery.value = newVal
})

watch(localSearchQuery, (newVal) => {
  emit('update:searchQuery', newVal)
})
</script>

<style scoped>
.project-list-organism {
  @apply w-full;
}
</style>