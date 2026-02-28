<template>
  <div class="space-y-8">
    <!-- Page Header -->
    <PageHeader
      :title="$t('projects.title')"
      :subtitle="$t('projects.subtitle')"
      :action-label="$t('projects.submitProject')"
      action-link="/create"
    >
      <template #controls>
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="$t('projects.searchPlaceholder')"
            class="input pl-10"
          />
          <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <select v-model="sortBy" class="input">
          <option value="newest">{{ $t('projects.sortOptions.newest') }}</option>
          <option value="popular">{{ $t('projects.sortOptions.popular') }}</option>
          <option value="votes">{{ $t('projects.sortOptions.votes') }}</option>
          <option value="recent">{{ $t('projects.sortOptions.recent') }}</option>
        </select>
      </template>
    </PageHeader>

    <!-- Selected Tags Section -->
    <SelectedTags
      v-if="selectedTags.length > 0"
      :title="$t('projects.filteringByTags')"
      :tags="selectedTags"
      :clear-label="$t('projects.clearAll')"
      @remove="removeTag"
      @clear="clearAllTags"
    />

    <!-- Loading State -->
    <LoadingState
      v-if="loading && projects.length === 0"
      :message="$t('common.loading')"
    />

    <!-- Error State -->
    <ErrorState
      v-else-if="error"
      :title="$t('projects.errors.failedToLoad')"
      :message="error"
      :retry-label="$t('common.tryAgain')"
      @retry="fetchProjects"
    />

    <!-- Projects Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <ProjectListCard
        v-for="project in filteredProjects"
        :key="project.id"
        :project="project"
        :live-demo-label="$t('projects.projectStatus.liveDemo')"
        :prototype-label="$t('projects.projectStatus.prototype')"
        :github-title="$t('projects.viewOnGitHub')"
        :views-label="$t('projects.stats.views')"
        :comments-label="$t('projects.stats.comments')"
        @open="openProject"
      />
    </div>

    <!-- Empty State -->
    <EmptyState
      v-if="filteredProjects.length === 0"
      :title="$t('projects.emptyState.noProjectsFound')"
      :description="$t('projects.emptyState.description')"
    >
      <template #action>
        <NuxtLink to="/create" class="btn btn-primary">
          {{ $t('projects.submitYourProject') }}
        </NuxtLink>
      </template>
    </EmptyState>

    <!-- Load More -->
    <LoadMore
      v-if="filteredProjects.length > 0 && hasMore"
      :label="$t('projects.loadMore')"
      :loading="loading"
      @load="loadMore"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from '#imports'
import { useUIStore } from '~/stores/ui'
import { useAuthStore } from '~/stores/auth'
import { PageHeader, SelectedTags, LoadingState, ErrorState, EmptyState, LoadMore } from '~/components/molecules'
import { ProjectListCard } from '~/components/organisms'
import { generateProjectPlaceholder } from '~/utils/placeholderImages'
import { resolveImageUrl } from '~/utils/imageUrl'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const uiStore = useUIStore()
const authStore = useAuthStore()
const searchQuery = ref('')
const selectedTags = ref<string[]>([])
const sortBy = ref('popular')
const loading = ref(false)
const projects = ref<any[]>([])
const error = ref<string | null>(null)
const hasMore = ref(true)

const config = useRuntimeConfig()
const apiUrl = config.public.apiUrl

// Initialize search query and tags from URL parameters
onMounted(() => {
  if (route.query.q) {
    searchQuery.value = route.query.q as string
  }
  const newTags: string[] = []
  if (route.query.technology) {
    const tech = Array.isArray(route.query.technology)
      ? route.query.technology[0]
      : route.query.technology
    if (tech) {
      newTags.push(tech)
    }
  }
  if (route.query.technologies) {
    const techs = Array.isArray(route.query.technologies)
      ? route.query.technologies[0]
      : route.query.technologies
    if (techs) {
      const split = techs.split(',').map(t => t.trim()).filter(t => t)
      split.forEach(t => {
        if (!newTags.includes(t)) newTags.push(t)
      })
    }
  }
  selectedTags.value = newTags
  fetchProjects()
})

// Watch for URL changes to update search query
watch(() => route.query.q, (newQ) => {
  if (newQ !== undefined) {
    searchQuery.value = newQ as string
  }
})

// Watch for URL changes to update technology filter and refetch projects
watch([() => route.query.technology, () => route.query.technologies], ([techParam, techsParam]) => {
  const newTags: string[] = []
  // Single technology parameter
  if (techParam !== undefined) {
    const tech = Array.isArray(techParam) ? techParam[0] : techParam
    if (tech) {
      newTags.push(tech)
    }
  }
  // Multiple technologies parameter
  if (techsParam !== undefined) {
    const techs = Array.isArray(techsParam) ? techsParam[0] : techsParam
    if (techs) {
      const split = techs.split(',').map(t => t.trim()).filter(t => t)
      split.forEach(t => {
        if (!newTags.includes(t)) newTags.push(t)
      })
    }
  }
  selectedTags.value = newTags
  // Refetch projects with new filter
  fetchProjects()
})

// Watch for user parameter changes to refetch projects
watch(() => route.query.user, () => {
  fetchProjects()
})

// Watch for search query changes to refetch projects
watch(searchQuery, () => {
  fetchProjects()
})

// Watch selectedTags and update URL
watch(selectedTags, (newTags) => {
  const query = { ...route.query }
  const validTags = newTags.filter(tag => tag)
  // Remove existing technology parameters
  delete query.technology
  delete query.technologies
  
  if (validTags.length === 1) {
    query.technology = validTags[0] as string
  } else if (validTags.length > 1) {
    query.technologies = validTags.join(',')
  }
  router.replace({ query })
}, { deep: true })

// Fetch projects from API with optional search
const fetchProjects = async () => {
  loading.value = true
  error.value = null
  try {
    // Build query parameters
    const params = new URLSearchParams()
    params.append('skip', '0')
    params.append('limit', '24')
    if (searchQuery.value) {
      params.append('search', searchQuery.value)
    }
    // Add user filter if present in URL
    if (route.query.user) {
      const userParam = Array.isArray(route.query.user)
        ? route.query.user[0]
        : route.query.user
      if (userParam) {
        params.append('user', userParam as string)
      }
    }
    // Add technology filter if present
    if (selectedTags.value.length > 0) {
      const validTags = selectedTags.value.filter(tag => tag)
      if (validTags.length === 1) {
        params.append('technology', validTags[0] as string)
      } else if (validTags.length > 1) {
        params.append('technologies', validTags.join(','))
      }
    }
    
    const response = await authStore.fetchWithAuth(`/api/projects?${params.toString()}`)
    if (!response.ok) {
      throw new Error(`${t('projects.errors.failedToFetch')}: ${response.status}`)
    }
    const data = await response.json()
    
    // Check if we got fewer projects than requested (end of data)
    if (data.length < 24) {
      hasMore.value = false
    }
    
    // Transform API data to match frontend structure
    projects.value = data.map((project: any) => ({
      id: project.id,
      name: project.title,
      author: project.owner?.name || t('common.unknown'),
      hackathon: project.hackathon?.name || t('common.unknownHackathon'),
      status: project.status === 'active' ? 'Submitted' :
              project.status === 'winner' ? 'Winner' :
              project.status === 'finalist' ? 'Finalist' : 'Submitted',
       description: project.description || t('common.noDescription'),
       tech: project.technologies ? project.technologies.split(',').map((t: string) => t.trim()) : [],
        image: project.image_path ? resolveImageUrl(project.image_path, config.public.apiUrl || 'http://localhost:8000') : generateProjectPlaceholder({
          id: project.id,
          title: project.title
        }),
       demo: project.live_url || null,
       github: project.repository_url || null,
       views: project.view_count || 0,
       comments: project.comment_count || 0,
       upvotes: project.upvote_count || 0,
       downvotes: project.downvote_count || 0,
       userVote: null, // Would need to check user's vote from separate endpoint
       team: project.owner ? [{ id: project.owner.id, name: project.owner.name }] : []
    }))
   } catch (err: any) {
    error.value = err.message || t('projects.errors.failedToLoad')
    console.error('Error fetching projects:', err)
    uiStore.showError(t('errors.fetchProjectsFailed'), t('errors.projectsLoadError'))
    // Fallback to empty array
    projects.value = []
  } finally {
    loading.value = false
  }
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
const filteredProjects = computed(() => {
  let filtered = [...projects.value]

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(p =>
      p.name.toLowerCase().includes(query) ||
      p.author.toLowerCase().includes(query) ||
      p.description.toLowerCase().includes(query) ||
      p.tech.some((tech: string) => tech.toLowerCase().includes(query))
    )
  }

  // Tag filtering is now handled server-side via technology parameter
  // Client-side tag filtering is disabled to avoid double filtering

  // Apply sorting
  if (sortBy.value === 'popular') {
    filtered.sort((a, b) => b.views - a.views)
  } else if (sortBy.value === 'votes') {
    filtered.sort((a, b) => (b.upvotes - b.downvotes) - (a.upvotes - a.downvotes))
  } else if (sortBy.value === 'recent') {
    // For demo purposes, sort by ID (newer IDs are higher)
    filtered.sort((a, b) => b.id - a.id)
  }

  return filtered
})

const openProject = (projectId: number) => {
  router.push(`/projects/${projectId}`)
}

const loadMore = async () => {
  loading.value = true
  try {
    // Calculate skip based on current number of projects
    const skip = projects.value.length
    const limit = 12 // Load 12 more projects
    
    // Build query parameters including user filter if present
    const params = new URLSearchParams()
    params.append('skip', skip.toString())
    params.append('limit', limit.toString())
    if (route.query.user) {
      const userParam = Array.isArray(route.query.user)
        ? route.query.user[0]
        : route.query.user
      if (userParam) {
        params.append('user', userParam as string)
      }
    }
    
    const response = await authStore.fetchWithAuth(`/api/projects?${params.toString()}`)
    if (!response.ok) {
      throw new Error(`${t('projects.errors.failedToLoadMore')}: ${response.status}`)
    }
    
    const data = await response.json()
    
    // Check if we got fewer projects than requested (end of data)
    if (data.length < limit) {
      hasMore.value = false
    }
    
    // Transform API data to match frontend structure
    const newProjects = data.map((project: any) => ({
      id: project.id,
      name: project.title,
      author: project.owner?.name || t('common.unknown'),
      hackathon: project.hackathon?.name || t('common.unknownHackathon'),
      status: project.status === 'active' ? 'Submitted' : 
              project.status === 'winner' ? 'Winner' :
              project.status === 'finalist' ? 'Finalist' : 'Submitted',
       description: project.description || t('common.noDescription'),
      tech: project.technologies ? project.technologies.split(',').map((t: string) => t.trim()) : [],
        image: project.image_path ? resolveImageUrl(project.image_path, config.public.apiUrl || 'http://localhost:8000') : generateProjectPlaceholder({
          id: project.id,
          title: project.title
        }),
      demo: project.live_url || null,
      github: project.repository_url || null,
      views: project.view_count || 0,
      comments: project.comment_count || 0,
      upvotes: project.upvote_count || 0,
      downvotes: project.downvote_count || 0,
      userVote: null,
      team: project.owner ? [{ id: project.owner.id, name: project.owner.name }] : []
    }))
    
    // Add new projects to existing list
    projects.value = [...projects.value, ...newProjects]
    
  } catch (err: any) {
    console.error('Error loading more projects:', err)
    uiStore.showError('Failed to load more projects', 'Unable to load more projects. Please try again.')
    // Show error to user (could add error state UI)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>