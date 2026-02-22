<template>
  <div class="py-8">
    <!-- Page Header -->
    <div class="mb-8">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">{{ $t('projects.myProjects.title') }}</h1>
          <p class="text-gray-600 dark:text-gray-400">{{ $t('projects.myProjects.subtitle') }}</p>
        </div>
        <NuxtLink
          to="/create"
          class="inline-flex items-center px-4 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          {{ $t('projects.myProjects.submitNewProject') }}
        </NuxtLink>
      </div>

      <!-- Search and Filter Section -->
      <div class="flex flex-col md:flex-row gap-4 mb-6">
        <div class="relative flex-1">
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="$t('projects.myProjectsSearchPlaceholder')"
            class="w-full pl-10 pr-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <select
          v-model="sortBy"
          class="px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="newest">{{ $t('projects.sortOptions.newest') }}</option>
          <option value="oldest">{{ $t('projects.sortOptions.oldest') }}</option>
          <option value="votes">{{ $t('projects.sortOptions.votes') }}</option>
          <option value="comments">{{ $t('projects.sortOptions.comments') }}</option>
        </select>
      </div>

      <!-- Selected Tags Section -->
      <div v-if="selectedTags.length > 0" class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 mb-6">
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
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredProjects.length === 0" class="text-center py-16">
      <svg class="w-24 h-24 text-gray-400 mx-auto mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">{{ $t('projects.myProjects.noProjectsYet') }}</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">{{ $t('projects.myProjects.noProjectsDescription') }}</p>
      <NuxtLink 
        to="/create" 
        class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        {{ $t('projects.myProjects.submitYourFirstProject') }}
      </NuxtLink>
    </div>

    <!-- Projects Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="project in filteredProjects"
        :key="project.id"
        class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
      >
        <!-- Project Image -->
        <div class="relative h-48 overflow-hidden bg-gray-200 dark:bg-gray-700">
          <img
            :src="project.image"
            :alt="project.name"
            class="w-full h-full object-cover"
          />
        </div>

        <!-- Project Header -->
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-start justify-between">
            <div>
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">{{ project.name }}</h3>
              <div class="flex items-center space-x-2">
                 <span class="text-sm text-gray-500 dark:text-gray-400">{{ $t('projects.myProjects.submittedTo') }}</span>
                <NuxtLink 
                  :to="`/hackathons/${project.hackathon_id}`"
                  class="text-sm font-medium text-primary-600 dark:text-primary-400 hover:underline"
                >
                   {{ project.hackathon_name || $t('projects.myProjects.hackathon') }}
                </NuxtLink>
              </div>
            </div>
            <span 
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
              :class="{
                'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300': project.status === 'approved',
                'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300': project.status === 'pending',
                'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300': project.status === 'rejected'
              }"
            >
              {{ project.status || 'pending' }}
            </span>
          </div>
        </div>

        <!-- Project Content -->
        <div class="p-6">
          <p class="text-gray-700 dark:text-gray-300 mb-4 line-clamp-3">{{ project.description }}</p>
          
          <div class="space-y-4">
            <!-- Tech Stack -->
            <div v-if="project.technologiesArray && project.technologiesArray.length > 0">
               <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ $t('projects.detail.technologies') }}</h4>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="tech in project.technologiesArray.slice(0, 3)"
                  :key="tech"
                  @click="toggleTag(tech)"
                  :class="[
                    'px-3 py-1 rounded-full text-sm transition-all duration-200',
                    selectedTags.includes(tech)
                      ? 'bg-primary-500 text-white shadow-sm'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  ]"
                   :title="selectedTags.includes(tech) ? $t('projects.myProjects.clickToRemoveFilter') : $t('projects.myProjects.clickToFilterByTag')"
                >
                  {{ tech }}
                  <span v-if="selectedTags.includes(tech)" class="ml-1">✓</span>
                </button>
                <span
                  v-if="project.technologiesArray.length > 3"
                  class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-sm"
                >
                  +{{ project.technologiesArray.length - 3 }} more
                </span>
              </div>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
               <div class="text-center">
                 <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ project.vote_count || 0 }}</p>
                 <p class="text-xs text-gray-500 dark:text-gray-400">{{ $t('projects.projects.votes') }}</p>
               </div>
               <div class="text-center">
                 <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ project.comment_count || 0 }}</p>
                 <p class="text-xs text-gray-500 dark:text-gray-400">{{ $t('projects.projects.comments') }}</p>
               </div>
               <div class="text-center">
                 <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ project.view_count || 0 }}</p>
                 <p class="text-xs text-gray-500 dark:text-gray-400">{{ $t('projects.projects.views') }}</p>
               </div>
            </div>
          </div>
        </div>

        <!-- Project Footer -->
        <div class="px-6 py-4 bg-gray-50 dark:bg-gray-700/50 border-t border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500 dark:text-gray-400">
              {{ formatDate(project.created_at) }}
            </span>
            <div class="flex items-center space-x-3">
              <NuxtLink 
                :to="`/projects/${project.id}`"
                class="text-sm font-medium text-primary-600 dark:text-primary-400 hover:underline"
              >
                 {{ $t('common.viewDetails') }}
              </NuxtLink>
              <button 
                v-if="project.status === 'pending'"
                @click="handleEdit(project)"
                class="text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300"
              >
                 {{ $t('common.edit') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="filteredProjects.length > 0 && totalPages > 1" class="mt-8 flex justify-center">
      <div class="flex items-center space-x-2">
        <button 
          @click="prevPage"
          :disabled="currentPage === 1"
          class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ $t('common.previous') }}
        </button>
        <span class="px-4 py-2 text-gray-700 dark:text-gray-300">
           {{ $t('projects.myProjects.pageInfo', { currentPage, totalPages }) }}
        </span>
        <button 
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ $t('common.next') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { format } from 'date-fns'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'

const authStore = useAuthStore()
const uiStore = useUIStore()
const { t } = useI18n()
const loading = ref(true)
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

const formatDate = (dateString: string) => {
  if (!dateString) return t('projects.myProjects.notAvailable')
  try {
    return format(new Date(dateString), 'MMM dd, yyyy')
  } catch {
    return dateString
  }
}

const fetchMyProjects = async () => {
  try {
    loading.value = true
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
        image: project.image_path || 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80',
        technologiesArray: project.technologies
          ? project.technologies.split(',').map((tech: string) => tech.trim()).filter((tech: string) => tech.length > 0)
          : []
      }))
      projects.value = transformedProjects
      totalProjects.value = transformedProjects.length
    } else {
      projects.value = []
    }
  } catch (error) {
    console.error('Error fetching my projects:', error)
    projects.value = []
    uiStore.showError('Failed to load projects', 'Unable to load your projects. Please try again later.')
  } finally {
    loading.value = false
  }
}

const handleEdit = (project: any) => {
  // Navigate to edit page or show edit modal
  console.log('Edit project:', project)
  // In a real implementation, you would navigate to an edit page
  // navigateTo(`/projects/${project.id}/edit`)
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchMyProjects()
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchMyProjects()
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

// Filtered projects computed property
const filteredProjects = computed(() => {
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

  return filtered
})

onMounted(() => {
  fetchMyProjects()
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>