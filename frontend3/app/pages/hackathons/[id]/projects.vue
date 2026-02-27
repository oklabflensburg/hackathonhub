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
      <HackathonProjectCard
        v-for="project in filteredProjects"
        :key="project.id"
        :project="project"
        :can-edit="canEditProject(project)"
        :labels="{
          votes: $t('projects.stats.votes'),
          comments: $t('projects.stats.comments'),
          views: $t('projects.stats.views'),
          view: $t('projects.viewProject'),
          vote: $t('votes.vote'),
          edit: $t('projects.editProject')
        }"
        @view="viewProject"
        @vote="voteForProject"
        @edit="editProject"
      />
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
import { generateProjectPlaceholder } from '~/utils/placeholderImages'
import HackathonProjectCard from '~/components/hackathons/HackathonProjectCard.vue'

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
const isHackathonMember = ref(false)

// Fetch real projects data from API
const fetchProjects = async () => {
  loading.value = true
  error.value = false

  try {
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // First, try to get projects for this specific hackathon
    const response = await authStore.fetchWithAuth(`/api/projects?hackathon_id=${id}`)

    if (!response.ok) {
      // If no hackathon-specific endpoint, get all projects
      const allResponse = await authStore.fetchWithAuth(`/api/projects`)
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

  // Team data - currently shows only project owner
  // TODO: Implement proper team member display when backend supports project-team relationships
  const team = apiProject.owner ? [
    { id: apiProject.owner.id, name: apiProject.owner.name || apiProject.owner.username }
  ] : []

  // Parse technologies if available
  const techStack = apiProject.technologies ?
    apiProject.technologies.split(',').map((t: string) => t.trim()).filter(Boolean) :
    []

  const projectName = apiProject.title || apiProject.name || 'Untitled Project'

  // Use real API data for counts
  const votes = apiProject.upvote_count || apiProject.vote_score || 0
  const comments = apiProject.comment_count || 0
  const views = apiProject.view_count || 0

  // Generate proper image URL if image_path exists
  let imageUrl = ''
  if (apiProject.image_path && !apiProject.image_path.includes('/temp/')) {
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // Handle different image_path formats:
    // 1. Full URL (http://... or https://...) - use as-is
    // 2. Path starting with /static/ - prepend backend URL
    // 3. Path starting with /uploads/ - convert to /static/uploads/ and prepend backend URL
    // 4. Other paths - prepend backend URL and ensure starts with /

    if (apiProject.image_path.startsWith('http://') || apiProject.image_path.startsWith('https://')) {
      // Full URL - use as-is
      imageUrl = apiProject.image_path
    } else if (apiProject.image_path.startsWith('/static/')) {
      // Already in correct format for static serving
      imageUrl = `${backendUrl}${apiProject.image_path}`
    } else if (apiProject.image_path.startsWith('/uploads/')) {
      // Convert /uploads/ to /static/uploads/
      imageUrl = `${backendUrl}/static${apiProject.image_path}`
    } else {
      // Other paths - ensure starts with /
      const imagePath = apiProject.image_path.startsWith('/') ?
        apiProject.image_path : `/${apiProject.image_path}`
      imageUrl = `${backendUrl}${imagePath}`
    }
  } else {
    // Use placeholder only when no real image
    imageUrl = generateProjectPlaceholder({
      id: apiProject.id || 0,
      title: projectName
    })
  }

  return {
    id: apiProject.id,
    name: projectName,
    description: apiProject.description || 'No description available.',
    image: imageUrl,
    status: status,
    team: team,
    techStack: techStack,
    votes: votes,
    comments: comments,
    views: views,
    hasVoted: false, // This would come from user's vote status in a real app
    owner_id: apiProject.owner_id, // Include owner_id for permission checks
    hackathon_id: apiProject.hackathon_id // Include hackathon_id for team member checks
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

const voteForProject = async (projectId: number) => {
  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    uiStore.showWarning(t('votes.pleaseLogin'), t('common.authenticationRequired'))
    return
  }

  const displayProjects = transformedProjects.value
  const project = displayProjects.find(p => p.id === projectId)
  if (!project) return

  try {
    // Determine vote type based on current state
    // Since this is a simple toggle vote (like/unlike), we'll use 'upvote' for like
    const voteType = project.hasVoted ? 'remove' : 'upvote'
    
    if (voteType === 'remove') {
      // Remove vote
      const response = await authStore.fetchWithAuth(`/api/projects/${projectId}/vote`, {
        method: 'DELETE'
      })
      
      if (response.ok) {
        project.hasVoted = false
        project.votes -= 1
        uiStore.showSuccess(t('votes.voteRemoved'))
      } else {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || t('votes.failedToVote'))
      }
    } else {
      // Add upvote
      const response = await authStore.fetchWithAuth(`/api/projects/${projectId}/vote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ vote_type: 'upvote' })
      })
      
      if (response.ok) {
        project.hasVoted = true
        project.votes += 1
        uiStore.showSuccess(t('votes.upvotedSuccessfully'))
      } else {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || t('votes.failedToVote'))
      }
    }
    
    // Refresh project stats from API to ensure consistency
    await fetchProjectVoteStats(projectId)
  } catch (error) {
    console.error('Error voting for project:', error)
    uiStore.showError(
      error instanceof Error ? error.message : t('votes.failedToVote'),
      t('common.error')
    )
  }
}

// Helper function to fetch updated vote stats for a project
const fetchProjectVoteStats = async (projectId: number) => {
  try {
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    const response = await authStore.fetchWithAuth(`/api/projects/${projectId}/vote-stats`)
    
    if (response.ok) {
      const stats = await response.json()
      const displayProjects = transformedProjects.value
      const project = displayProjects.find(p => p.id === projectId)
      if (project) {
        project.votes = stats.upvotes || stats.total_score || 0
        // Note: We don't have hasVoted info from public endpoint
        // Would need user-specific endpoint to get user's vote status
      }
    }
  } catch (err) {
    console.error('Failed to fetch vote stats:', err)
  }
}

// Check if current user can edit this project
const canEditProject = (project: any) => {
  if (!authStore.isAuthenticated || !project) {
    return false
  }

  // Check if user is the project owner
  // Convert both to numbers for comparison
  const userId = Number(authStore.user?.id)
  const ownerId = Number(project.owner_id)
  const isOwner = userId === ownerId

  if (isOwner) return true

  // Check if user is a hackathon team member (for projects belonging to this hackathon)
  if (project.hackathon_id && Number(project.hackathon_id) === Number(id)) {
    return isHackathonMember.value
  }
  
  return false
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
        // Try to parse error message from backend
        try {
          const errorData = await response.json()
          const errorMessage = errorData.detail || t('projects.updateFailed')
          uiStore.showError(errorMessage, t('common.updateFailed'))
        } catch {
          // If we can't parse JSON, show generic error
          uiStore.showError(t('projects.updateFailed'), t('common.updateFailed'))
        }
      }
    } catch (error) {
      console.error('Error updating project:', error)
      uiStore.showError(t('projects.updateError'), t('common.updateError'))
    }
  }
}

// Check if current user is registered/teamed for this hackathon
const checkHackathonMembership = async () => {
  if (!authStore.isAuthenticated) {
    isHackathonMember.value = false
    return
  }

  try {
    const response = await authStore.fetchWithAuth('/api/me/registrations')
    if (!response.ok) {
      isHackathonMember.value = false
      return
    }

    const registrations = await response.json()
    const hackathonId = Number(id)
    isHackathonMember.value = registrations.some((reg: any) => Number(reg.hackathon_id) === hackathonId)
  } catch (err) {
    console.error('Error checking hackathon membership:', err)
    isHackathonMember.value = false
  }
}

// Fetch projects on component mount
onMounted(() => {
  fetchProjects()
  checkHackathonMembership()
})
</script>
