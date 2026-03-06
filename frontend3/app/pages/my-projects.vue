<template>
  <div class="max-w-7xl mx-auto py-8">
    <!-- Page Header -->
    <PageHeader
      :title="t('projects.myProjects.title')"
      :subtitle="t('projects.myProjects.subtitle')"
    >
      <template #actions>
        <NuxtLink
          to="/create"
          class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          {{ t('projects.myProjects.submitNewProject') }}
        </NuxtLink>
      </template>
    </PageHeader>

    <!-- Search and Filter Section -->
    <div class="mb-8">
      <div class="flex flex-col md:flex-row gap-4 mb-6">
        <SearchBar
          v-model="searchQuery"
          :placeholder="t('projects.myProjectsSearchPlaceholder')"
          class="flex-1"
          @search="handleSearch"
        />
        <select
          v-model="sortBy"
          class="px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="newest">{{ t('projects.sortOptions.newest') }}</option>
          <option value="oldest">{{ t('projects.sortOptions.oldest') }}</option>
          <option value="votes">{{ t('projects.sortOptions.votes') }}</option>
          <option value="comments">{{ t('projects.sortOptions.comments') }}</option>
        </select>
      </div>

      <!-- Selected Tags -->
      <SelectedTags
        v-if="selectedTags.length > 0"
        :tags="selectedTags"
        @remove-tag="removeTag"
        @clear-all="clearAllTags"
        :title="t('projects.filteringByTags')"
      />
    </div>

    <!-- Loading State -->
    <LoadingState
      v-if="loading"
      :message="t('common.loading')"
    />

    <!-- Error State -->
    <ErrorState
      v-else-if="error"
      :title="t('projects.myProjects.loadErrorTitle')"
      :message="error"
      :retry-label="t('common.tryAgain')"
      @retry="fetchMyProjects"
    />

    <!-- Empty State -->
    <EmptyState
      v-else-if="filteredProjects.length === 0"
      :title="t('projects.myProjects.noProjectsYet')"
      :description="t('projects.myProjects.noProjectsDescription')"
      :action-label="t('projects.myProjects.submitYourFirstProject')"
      action-to="/create"
      icon="document"
    />

    <!-- Projects Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
          tech: project.technologiesArray,
          views: project.view_count || 0,
          comments: project.comment_count || 0,
          upvotes: project.vote_count || 0,
          downvotes: 0,
          userVote: null,
          demo: false,
          github: '',
          hackathon: project.hackathon_name,
          createdAt: project.created_at
        }"
        :live-demo-label="t('projects.projectStatus.liveDemo')"
        :prototype-label="t('projects.projectStatus.prototype')"
        :github-title="t('projects.viewOnGitHub')"
        :views-label="t('projects.stats.views')"
        :comments-label="t('projects.stats.comments')"
        @open="openProject"
        @tag-click="toggleTag"
      />
    </div>

    <!-- Pagination -->
    <Pagination
      v-if="filteredProjects.length > 0 && totalPages > 1"
      :total="totalProjects"
      :per-page="pageSize"
      :current-page="currentPage"
      :show-info="true"
      @page-change="handlePageChange"
      class="mt-8"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { resolveImageUrl } from '~/utils/imageUrl'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import PageHeader from '~/components/molecules/PageHeader.vue'
import SearchBar from '~/components/molecules/SearchBar.vue'
import SelectedTags from '~/components/molecules/SelectedTags.vue'
import LoadingState from '~/components/molecules/LoadingState.vue'
import ErrorState from '~/components/molecules/ErrorState.vue'
import EmptyState from '~/components/molecules/EmptyState.vue'
import ProjectListCard from '~/components/organisms/projects/ProjectListCard.vue'
import Pagination from '~/components/molecules/Pagination.vue'

const { t } = useI18n()
const authStore = useAuthStore()
const config = useRuntimeConfig()
const uiStore = useUIStore()

const loading = ref(true)
const error = ref<string | null>(null)
const projects = ref<any[]>([])
const currentPage = ref(1)
const pageSize = ref(9)
const totalProjects = ref(0)

// Tag search functionality
const searchQuery = ref('')
const selectedTags = ref<string[]>([])
const sortBy = ref('newest')

const totalPages = computed(() => {
  return Math.ceil(totalProjects.value / pageSize.value)
})

const generatePlaceholderImage = (projectId: number, projectName: string) => {
  // Simple color based on project ID
  const colors = ['#667eea', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#a8edea']
  const color = colors[projectId % colors.length] || '#667eea'

  // Get first letter of project name
  const firstLetter = projectName.charAt(0).toUpperCase() || 'P'

  // Simple SVG
  const svg = `<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="${color}" />
    <text x="50%" y="50%" font-family="Arial" font-size="120" font-weight="bold" 
          fill="white" text-anchor="middle" dy=".35em" opacity="0.8">${firstLetter}</text>
  </svg>`

  return 'data:image/svg+xml;base64,' + btoa(svg)
}

const fetchMyProjects = async () => {
  try {
    loading.value = true
    error.value = null
    if (!authStore.isAuthenticated) {
      projects.value = []
      return
    }

    // Fetch user's projects from API using fetchWithAuth for auto-refresh
    const response = await authStore.fetchWithAuth('/api/users/me/projects')

    if (response.ok) {
      const myProjects = await response.json()
      // Transform technologies from comma-separated string to array and add image
      const transformedProjects = myProjects.map((project: any) => ({
        ...project,
        name: project.title, // map title to name for template
        hackathon_name: project.hackathon?.name || 'Hackathon',
        image: project.image_path
          ? resolveImageUrl(project.image_path, config.public.apiUrl || 'http://localhost:8000')
          : generatePlaceholderImage(project.id || 0, project.title || 'Project'),
        technologiesArray: project.technologies
          ? project.technologies.split(',').map((tech: string) => tech.trim()).filter((tech: string) => tech.length > 0)
          : []
      }))
      projects.value = transformedProjects
      totalProjects.value = transformedProjects.length
    } else {
      projects.value = []
      error.value = t('projects.myProjects.loadError')
    }
  } catch (err) {
    console.error('Error fetching my projects:', err)
    projects.value = []
    error.value = t('projects.myProjects.loadErrorGeneric')
    uiStore.showError('Failed to load projects', 'Unable to load your projects. Please try again later.')
  } finally {
    loading.value = false
  }
}

const openProject = (id: number) => {
  navigateTo(`/projects/${id}`)
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchMyProjects()
}

const handleSearch = (query: string) => {
  searchQuery.value = query
}

// Tag handling functions
const toggleTag = (tag: string) => {
  const index = selectedTags.value.indexOf(tag)
  if (index === -1) {
    selectedTags.value.push(tag)
  } else {
    selectedTags.value.splice(index, 1)
  }
}

const removeTag = (tag: string) => {
  const index = selectedTags.value.indexOf(tag)
  if (index !== -1) {
    selectedTags.value.splice(index, 1)
  }
}

const clearAllTags = () => {
  selectedTags.value = []
}

// Filtered projects computed property
const filteredProjects = computed<any[]>(() => {
  let filtered = [...projects.value]

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(p =>
      p.name.toLowerCase().includes(query) ||
      p.description.toLowerCase().includes(query) ||
      (p.technologiesArray && p.technologiesArray.some((tech: string) => tech.toLowerCase().includes(query)))
    )
  }

  // Apply tag filter (AND logic - project must have ALL selected tags)
  if (selectedTags.value.length > 0) {
    filtered = filtered.filter(p =>
      selectedTags.value.every(tag =>
        p.technologiesArray && p.technologiesArray.some((tech: string) => tech.toLowerCase() === tag.toLowerCase())
      )
    )
  }

  // Apply sorting
  if (sortBy.value === 'newest') {
    filtered.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
  } else if (sortBy.value === 'oldest') {
    filtered.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
  } else if (sortBy.value === 'votes') {
    filtered.sort((a, b) => (b.vote_count || 0) - (a.vote_count || 0))
  } else if (sortBy.value === 'comments') {
    filtered.sort((a, b) => (b.comment_count || 0) - (a.comment_count || 0))
  }

  // Pagination
  const startIndex = (currentPage.value - 1) * pageSize.value
  const endIndex = startIndex + pageSize.value
  return filtered.slice(startIndex, endIndex)
})

onMounted(() => {
  fetchMyProjects()
})
</script>