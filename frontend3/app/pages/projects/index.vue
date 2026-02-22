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

    <!-- Projects Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="project in filteredProjects"
        :key="project.id"
        class="card-hover group cursor-pointer"
        @click="$router.push(`/projects/${project.id}`)"
      >
        <!-- Project Header -->
        <div class="flex items-start justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400">
              {{ project.name }}
            </h3>
            <div class="flex items-center space-x-2 mt-1">
              <div class="flex items-center">
                <div class="w-6 h-6 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mr-2">
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-400">
                    {{ project.author.charAt(0) }}
                  </span>
                </div>
                <span class="text-sm text-gray-600 dark:text-gray-400">{{ project.author }}</span>
              </div>
              <span class="text-xs text-gray-500 dark:text-gray-400">•</span>
              <span class="text-sm text-gray-600 dark:text-gray-400">{{ project.hackathon }}</span>
            </div>
          </div>
          <span :class="[
            'badge',
            project.status === 'Winner' ? 'badge-success' :
            project.status === 'Finalist' ? 'badge-warning' :
            project.status === 'Submitted' ? 'badge-info' : 'badge-primary'
          ]">
            {{ project.status }}
          </span>
        </div>

        <!-- Project Description -->
        <p class="text-gray-600 dark:text-gray-400 mb-4 text-sm line-clamp-3">
          {{ project.description }}
        </p>

        <!-- Tech Stack -->
        <div class="flex flex-wrap gap-2 mb-4">
          <button
            v-for="tech in project.tech"
            :key="tech"
            @click.stop="toggleTag(tech)"
            :class="[
              'px-2 py-1 text-xs rounded transition-all duration-200',
              selectedTags.includes(tech)
                ? 'bg-primary-500 text-white shadow-sm'
                : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
            ]"
            :title="selectedTags.includes(tech) ? 'Click to remove filter' : 'Click to filter by this tag'"
          >
            {{ tech }}
            <span v-if="selectedTags.includes(tech)" class="ml-1">✓</span>
          </button>
        </div>

        <!-- Project Image -->
        <div class="relative h-48 mb-4 rounded-lg overflow-hidden">
          <img
            :src="project.image"
            :alt="project.name"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
          <div class="absolute bottom-4 left-4 right-4">
            <div class="flex items-center justify-between">
              <span class="text-white text-sm font-medium">
                {{ project.demo ? $t('projects.projectStatus.liveDemo') : $t('projects.projectStatus.prototype') }}
              </span>
              <a
                v-if="project.github"
                :href="project.github"
                target="_blank"
                class="text-white hover:text-gray-200"
                :title="$t('projects.viewOnGitHub')"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                </svg>
              </a>
            </div>
          </div>
        </div>

        <!-- Stats and Actions -->
        <div class="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-800">
          <div class="flex items-center space-x-6">
               <div class="text-center">
              <div class="text-lg font-bold text-gray-900 dark:text-white">{{ project.views }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">{{ $t('projects.stats.views') }}</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-bold text-gray-900 dark:text-white">{{ project.comments }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">{{ $t('projects.stats.comments') }}</div>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <VoteButtons
              :project-id="project.id"
              :initial-upvotes="project.upvotes"
              :initial-downvotes="project.downvotes"
              :initial-user-vote="project.userVote"
            />
          </div>
        </div>

        <!-- Team Members -->
        <div v-if="project.team && project.team.length > 0" class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-800">
           <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-600 dark:text-gray-400">{{ $t('projects.team.team') }}</span>
            <span class="text-xs text-gray-500 dark:text-gray-400">{{ $t('projects.detail.teamMembersCount', { count: project.team.length }) }}</span>
          </div>
          <div class="flex -space-x-2">
            <div
              v-for="member in project.team.slice(0, 4)"
              :key="member.id"
              class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 border-2 border-white dark:border-gray-800 flex items-center justify-center"
              :title="member.name"
            >
              <span class="text-xs font-medium text-gray-600 dark:text-gray-400">
                {{ member.name.charAt(0) }}
              </span>
            </div>
            <div
              v-if="project.team.length > 4"
              class="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-800 border-2 border-white dark:border-gray-800 flex items-center justify-center"
               :title="$t('projects.team.moreTeamMembers')"
            >
              <span class="text-xs font-medium text-gray-600 dark:text-gray-400">
                +{{ project.team.length - 4 }}
              </span>
            </div>
          </div>
        </div>
      </div>
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
import { useRoute } from '#imports'
import { useUIStore } from '~/stores/ui'

const { t } = useI18n()
const route = useRoute()
const uiStore = useUIStore()
const searchQuery = ref('')
const selectedTags = ref<string[]>([])
const sortBy = ref('popular')
const loading = ref(false)
const projects = ref<any[]>([])
const error = ref<string | null>(null)
const hasMore = ref(true)

const config = useRuntimeConfig()
const apiUrl = config.public.apiUrl

// Initialize search query from URL parameter
onMounted(() => {
  if (route.query.q) {
    searchQuery.value = route.query.q as string
  }
  fetchProjects()
})

// Watch for URL changes to update search query
watch(() => route.query.q, (newQ) => {
  if (newQ !== undefined) {
    searchQuery.value = newQ as string
  }
})

// Watch for search query changes to refetch projects
watch(searchQuery, () => {
  fetchProjects()
})

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
    
    const response = await fetch(`${apiUrl}/api/projects?${params.toString()}`)
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
       image: project.image_path || 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80',
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
    uiStore.showError('Failed to load projects', 'Unable to load projects. Please try again later.')
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

  // Apply tag filter (AND logic - project must have ALL selected tags)
  if (selectedTags.value.length > 0) {
    filtered = filtered.filter(p =>
      selectedTags.value.every(tag =>
        p.tech.some((tech: string) => tech.toLowerCase() === tag.toLowerCase())
      )
    )
  }

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

const loadMore = async () => {
  loading.value = true
  try {
    // Calculate skip based on current number of projects
    const skip = projects.value.length
    const limit = 12 // Load 12 more projects
    
    const response = await fetch(`${apiUrl}/api/projects?skip=${skip}&limit=${limit}`)
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
      image: project.image_path || 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80',
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