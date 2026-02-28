<template>
  <div class="space-y-8">
    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ $t('projects.title') }}</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">
          {{ $t('projects.subtitle') }}
        </p>
      </div>
      <div class="flex items-center space-x-4">
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
        <NuxtLink to="/create" class="btn btn-primary">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          {{ $t('projects.submitProject') }}
        </NuxtLink>
      </div>
    </div>

    <!-- Selected Tags Section -->
    <div v-if="selectedTags.length > 0" class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-gray-500 dark:text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ $t('projects.filteringByTags') }}</span>
        </div>
        <button
          @click="clearAllTags"
          class="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 flex items-center"
        >
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          {{ $t('projects.clearAll') }}
        </button>
      </div>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="tag in selectedTags"
          :key="tag"
          class="px-3 py-1.5 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 text-sm rounded-full flex items-center"
        >
          {{ tag }}
          <button
            @click="removeTag(tag)"
            class="ml-2 text-primary-500 hover:text-primary-700 dark:hover:text-primary-200"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </span>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading && projects.length === 0" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">{{ $t('common.loading') }}</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-6 text-red-400">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.342 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
      </div>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        {{ $t('projects.errors.failedToLoad') }}
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
      <button @click="fetchProjects" class="btn btn-primary">
        {{ $t('common.tryAgain') }}
      </button>
    </div>

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
    <div v-if="filteredProjects.length === 0" class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-6 text-gray-300 dark:text-gray-600">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
       <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        {{ $t('projects.emptyState.noProjectsFound') }}
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        {{ $t('projects.emptyState.description') }}
      </p>
      <NuxtLink to="/create" class="btn btn-primary">
        {{ $t('projects.submitYourProject') }}
      </NuxtLink>
    </div>

    <!-- Load More -->
    <div v-if="filteredProjects.length > 0 && hasMore" class="text-center pt-8">
      <button
        @click="loadMore"
        :disabled="loading"
        class="btn btn-outline px-8"
      >
        <svg v-if="loading" class="w-5 h-5 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
        {{ $t('projects.loadMore') }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from '#imports'
import { useUIStore } from '~/stores/ui'
import { useAuthStore } from '~/stores/auth'
import ProjectListCard from '~/components/projects/ProjectListCard.vue'
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
    query.technology = validTags[0]
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
        params.append('technology', validTags[0])
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