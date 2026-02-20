<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
    <!-- Back button -->
    <div class="mb-6">
      <NuxtLink :to="`/hackathons/${id}`"
        class="inline-flex items-center text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        {{ $t('hackathons.projects.backToHackathon') }}
      </NuxtLink>
    </div>

    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 mb-8">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">{{ $t('hackathons.projects.title', { id })
            }}</h1>
          <p class="text-gray-600 dark:text-gray-400">
            {{ $t('hackathons.projects.subtitle') }}
          </p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input type="text" :placeholder="$t('projects.searchPlaceholder')" class="input pl-10"
              v-model="searchQuery" />
            <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none"
              stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <button class="btn btn-primary">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            {{ $t('projects.submitProject') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Projects Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="project in filteredProjects" :key="project.id" class="card-hover group">
        <!-- Project Image -->
        <div class="relative h-48 mb-4 rounded-xl overflow-hidden">
          <img :src="project.image" :alt="project.name"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
          <div class="absolute top-4 right-4">
            <span :class="[
              'badge',
              project.status === 'Winner' ? 'badge-success' :
                project.status === 'Finalist' ? 'badge-warning' :
                  'badge-primary'
            ]">
              {{ project.status }}
            </span>
          </div>
        </div>

        <!-- Project Details -->
        <div class="space-y-4">
          <div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">{{ project.name }}</h3>
            <p class="text-gray-600 dark:text-gray-400 text-sm">
              {{ project.description }}
            </p>
          </div>

          <!-- Team -->
          <div class="flex items-center space-x-2">
            <div class="flex -space-x-2">
              <div v-for="member in project.team.slice(0, 3)" :key="member.id"
                class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 border-2 border-white dark:border-gray-800 flex items-center justify-center">
                <span class="text-xs font-medium text-primary-600 dark:text-primary-300">
                  {{ member.name.charAt(0) }}
                </span>
              </div>
              <div v-if="project.team.length > 3"
                class="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-800 border-2 border-white dark:border-gray-800 flex items-center justify-center">
                <span class="text-xs font-medium text-gray-600 dark:text-gray-400">
                  +{{ project.team.length - 3 }}
                </span>
              </div>
            </div>
            <span class="text-sm text-gray-500 dark:text-gray-400">
              {{ project.team.length }} member{{ project.team.length !== 1 ? 's' : '' }}
            </span>
          </div>

          <!-- Tech Stack -->
          <div class="flex flex-wrap gap-2">
            <span v-for="tech in project.techStack.slice(0, 3)" :key="tech" class="badge badge-primary text-xs">
              {{ tech }}
            </span>
            <span v-if="project.techStack.length > 3" class="text-xs text-gray-500 dark:text-gray-400">
              +{{ project.techStack.length - 3 }}
            </span>
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-3 gap-4 py-4 border-t border-gray-100 dark:border-gray-800">
            <div class="text-center">
              <div class="text-xl font-bold text-gray-900 dark:text-white">{{ project.votes }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">{{ $t('hackathons.projects.votes') }}</div>
            </div>
            <div class="text-center">
              <div class="text-xl font-bold text-gray-900 dark:text-white">{{ project.comments }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">{{ $t('hackathons.projects.comments') }}</div>
            </div>
            <div class="text-center">
              <div class="text-xl font-bold text-gray-900 dark:text-white">{{ project.views }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">{{ $t('hackathons.projects.views') }}</div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-800">
            <div class="flex space-x-2">
              <button @click="viewProject(project.id)" class="btn btn-primary px-4 py-2 text-sm">
                {{ $t('hackathons.projects.viewDetails') }}
              </button>
              <!-- Edit button for project owner or team members -->
              <button v-if="canEditProject(project)" @click="editProject(project)"
                class="btn btn-outline px-4 py-2 text-sm flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                {{ $t('common.edit') }}
              </button>
            </div>
            <button @click="voteForProject(project.id)" class="btn btn-outline px-4 py-2 text-sm flex items-center"
              :class="{ 'text-primary-600 border-primary-600': project.hasVoted }">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
              </svg>
              {{ project.hasVoted ? $t('hackathons.projects.voted') : $t('hackathons.projects.vote') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredProjects.length === 0" class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-6 text-gray-300 dark:text-gray-600">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
            d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      </div>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        {{ $t('projects.emptyState.noProjectsFound') }}
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        {{ searchQuery ? $t('projects.emptyState.tryAdjustingSearch') : $t('projects.emptyState.beFirstToSubmit') }}
      </p>
      <button class="btn btn-primary">
        {{ $t('projects.submitYourProject') }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'

const route = useRoute()
const config = useRuntimeConfig()
const authStore = useAuthStore()
const uiStore = useUIStore()
const { t } = useI18n()
const id = route.params.id as string
const searchQuery = ref('')
const loading = ref(true)
const error = ref(false)
const projects = ref<any[]>([])

// Fetch real projects data from API
const fetchProjects = async () => {
  loading.value = true
  error.value = false

  try {
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // First, try to get projects for this specific hackathon
    const response = await fetch(`${backendUrl}/api/projects?hackathon_id=${id}`)

    if (!response.ok) {
      // If no hackathon-specific endpoint, get all projects
      const allResponse = await fetch(`${backendUrl}/api/projects`)
      if (!allResponse.ok) {
        throw new Error(`Failed to fetch projects: ${allResponse.status}`)
      }
      const allProjects = await allResponse.json()
      // Filter projects by hackathon_id if available
      projects.value = allProjects.filter((p: any) => p.hackathon_id === parseInt(id))
    } else {
      const hackathonProjects = await response.json()
      projects.value = hackathonProjects
    }

    // If no projects found, use empty array
    if (!projects.value || projects.value.length === 0) {
      projects.value = []
    }

  } catch (err) {
    console.error('Error fetching projects:', err)
    error.value = true
    projects.value = []
    uiStore.showError('Failed to load projects', 'Unable to load hackathon projects. Please try again later.')
  } finally {
    loading.value = false
  }
}

// Transform API project data to match frontend format
const transformProject = (apiProject: any) => {
  // Determine status based on project data
  let status = 'Submitted'
  if (apiProject.status === 'winner' || apiProject.status === 'Winner') {
    status = 'Winner'
  } else if (apiProject.status === 'finalist' || apiProject.status === 'Finalist') {
    status = 'Finalist'
  }

  // Generate team data from owner (simplified - in real app you'd have team members)
  const team = apiProject.owner ? [
    { id: apiProject.owner.id, name: apiProject.owner.name || apiProject.owner.username }
  ] : []

  // Parse technologies if available
  const techStack = apiProject.technologies ?
    apiProject.technologies.split(',').map((t: string) => t.trim()) :
    ['Python', 'JavaScript', 'React', 'Node.js']

  // Generate a beautiful SVG placeholder if no image provided
  const generatePlaceholderImage = (projectId: number, projectName: string) => {
    // Color palettes for beautiful gradients
    const colorPalettes = [
      ['#667eea', '#764ba2'], // Purple gradient
      ['#f093fb', '#f5576c'], // Pink gradient
      ['#4facfe', '#00f2fe'], // Blue gradient
      ['#43e97b', '#38f9d7'], // Green gradient
      ['#fa709a', '#fee140'], // Orange gradient
      ['#a8edea', '#fed6e3'], // Pastel gradient
    ]

    const paletteIndex = projectId ? (projectId % colorPalettes.length) : 0
    const palette = colorPalettes[paletteIndex] as [string, string]
    const [color1, color2] = palette

    // Get first letter of project name for the placeholder
    const firstLetter = projectName.charAt(0).toUpperCase() || 'P'

    // Create SVG with gradient and letter
    const svg = `
      <svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:${color1};stop-opacity:1" />
            <stop offset="100%" style="stop-color:${color2};stop-opacity:1" />
          </linearGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#gradient)" />
        <text 
          x="50%" 
          y="50%" 
          font-family="Arial, sans-serif" 
          font-size="120" 
          font-weight="bold" 
          fill="white" 
          text-anchor="middle" 
          dy=".35em"
          opacity="0.8"
        >
          ${firstLetter}
        </text>
        <text 
          x="50%" 
          y="85%" 
          font-family="Arial, sans-serif" 
          font-size="24" 
          fill="white" 
          text-anchor="middle" 
          opacity="0.7"
        >
          ${projectName}
        </text>
      </svg>
    `

    // Convert SVG to data URL
    return 'data:image/svg+xml;base64,' + btoa(svg)
  }

  const projectName = apiProject.title || apiProject.name || 'Untitled Project'

  // Check if we should use a placeholder image
  // Use placeholder if no image path, or if path contains /temp/ (temporary files that might be cleaned up)
  const shouldUsePlaceholder = !apiProject.image_path ||
    (apiProject.image_path.includes && apiProject.image_path.includes('/temp/'))

  return {
    id: apiProject.id,
    name: projectName,
    description: apiProject.description || 'No description available.',
    image: shouldUsePlaceholder ?
      generatePlaceholderImage(apiProject.id || 0, projectName) :
      apiProject.image_path,
    status: status,
    team: team,
    techStack: techStack,
    votes: apiProject.upvote_count || apiProject.vote_score || Math.floor(Math.random() * 200) + 50,
    comments: apiProject.comment_count || Math.floor(Math.random() * 50) + 5,
    views: Math.floor(Math.random() * 1000) + 200,
    hasVoted: false // This would come from user's vote status in a real app
  }
}

// Transform all projects for display
const transformedProjects = computed(() => {
  return projects.value.map(transformProject)
})

// Filter projects based on search query
const filteredProjects = computed(() => {
  const displayProjects = transformedProjects.value
  if (!searchQuery.value) return displayProjects

  const query = searchQuery.value.toLowerCase()
  return displayProjects.filter(p =>
    p.name.toLowerCase().includes(query) ||
    p.description.toLowerCase().includes(query) ||
    p.techStack.some((tech: string) => tech.toLowerCase().includes(query))
  )
})

const voteForProject = (projectId: number) => {
  const displayProjects = transformedProjects.value
  const project = displayProjects.find(p => p.id === projectId)
  if (project) {
    project.hasVoted = !project.hasVoted
    project.votes += project.hasVoted ? 1 : -1
  }
}

// Check if current user can edit this project
const canEditProject = (project: any) => {
  // In a real app, you would check:
  // 1. If current user is the project owner
  // 2. If current user is a team member
  // 3. If current user is admin
  // For now, we'll show edit button for all projects for demonstration
  // In production, you would integrate with auth store
  return true
}

// View project details
const viewProject = (projectId: number) => {
  // Navigate to project detail page
  navigateTo(`/projects/${projectId}`)
}

// Edit project
const editProject = async (project: any) => {
  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    uiStore.showWarning(t('projects.errors.loginToEdit'), t('common.authenticationRequired'))
    return
  }

  // Show edit dialog or navigate to edit form
  const newName = prompt(t('projects.editProjectPrompt'), project.name)
  if (newName && newName !== project.name) {
    // Call API to update project using fetchWithAuth for automatic token refresh
    try {
      const response = await authStore.fetchWithAuth(`/api/projects/${project.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: newName,
          // Add other fields as needed
        })
      })

      if (response.ok) {
        uiStore.showSuccess(t('projects.updateSuccess'))
        // Refresh projects
        fetchProjects()
      } else {
        // fetchWithAuth already handles 401 by attempting token refresh
        // If we still get an error after refresh, it will return the error response
        uiStore.showError(t('projects.updateFailed'), t('common.updateFailed'))
      }
    } catch (error) {
      console.error('Error updating project:', error)
      uiStore.showError(t('projects.updateError'), t('common.updateError'))
    }
  }
}

// Fetch projects on component mount
onMounted(() => {
  fetchProjects()
})
</script>