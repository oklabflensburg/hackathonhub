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

    <!-- Page Header -->
    <PageHeader
      :title="$t('hackathons.projects.title', { id })"
      :subtitle="$t('hackathons.projects.subtitle')"
    />

    <!-- Project List Organism -->
    <ProjectListOrganism
      :projects="transformedProjects"
      :loading="loading"
      :error="error"
      :search-query="searchQuery"
      :search-placeholder="$t('projects.searchPlaceholder')"
      :submit-button-text="$t('projects.submitProject')"
      :loading-text="$t('hackathons.loadingProjects')"
      :error-title="$t('hackathons.failedToLoad')"
      :retry-button-text="$t('hackathons.tryAgain')"
      :empty-title="$t('projects.emptyState.noProjectsFound')"
      :empty-description="searchQuery ? $t('projects.emptyState.tryAdjustingSearch') : $t('projects.emptyState.beFirstToSubmit')"
      :user-id="authStore.user?.id"
      :hackathon-id="Number(id)"
      :is-hackathon-member="isHackathonMember"
      @update:search-query="searchQuery = $event"
      @submit-project="handleSubmitProject"
      @retry="fetchProjects"
      @view-project="viewProject"
      @edit-project="editProject"
    >
      <!-- Custom project card slot for hackathon-specific cards -->
      <template #project-card="{ projects, canEdit }">
        <HackathonProjectCard
          v-for="project in projects"
          :key="project.id"
          :project="project"
          :can-edit="canEdit(project)"
          :labels="{
            votes: $t('projects.stats.votes'),
            comments: $t('projects.stats.comments'),
            views: $t('projects.stats.views'),
            view: $t('projects.viewProject'),
            edit: $t('projects.editProject')
          }"
          @view="viewProject"
          @edit="editProject"
        />
      </template>
    </ProjectListOrganism>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'
import { generateProjectPlaceholder } from '~/utils/placeholderImages'

import HackathonProjectCard from '~/components/hackathons/HackathonProjectCard.vue'
import PageHeader from '~/components/molecules/PageHeader.vue'
import ProjectListOrganism from '~/components/organisms/projects/ProjectListOrganism.vue'

const route = useRoute()
const config = useRuntimeConfig()
const authStore = useAuthStore()
const uiStore = useUIStore()
const { t } = useI18n()
const id = route.params.id as string
const searchQuery = ref('')
const loading = ref(true)
const error = ref<string | null>(null)
const projects = ref<any[]>([])
const isHackathonMember = ref(false)

// Fetch real projects data from API
const fetchProjects = async () => {
  loading.value = true
  error.value = null

  try {
    // Get projects for this specific hackathon
    const response = await authStore.fetchWithAuth(`/api/hackathons/${id}/projects`)

    if (!response.ok) {
      // If endpoint fails, treat as no projects (empty array)
      projects.value = []
    } else {
      const hackathonProjects = await response.json()
      // API returns { projects: [], hackathon_id: number }
      projects.value = hackathonProjects.projects || []
    }

    // If no projects found, use empty array
    if (!projects.value || projects.value.length === 0) {
      projects.value = []
    }

  } catch (err) {
    console.error('Error fetching projects:', err)
    error.value = err instanceof Error ? err.message : 'Failed to load projects'
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

// Handle submit project action
const handleSubmitProject = () => {
  if (!authStore.isAuthenticated) {
    uiStore.showWarning(t('projects.errors.loginToSubmit'), t('common.authenticationRequired'))
    return
  }
  
  // Navigate to project creation page for this hackathon
  navigateTo(`/projects/create?hackathon=${id}`)
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
