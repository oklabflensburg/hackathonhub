<template>
  <div class="max-w-4xl mx-auto py-8">
    <!-- Loading State -->
    <LoadingState
      v-if="loading"
      :message="t('common.loading')"
    />

    <!-- Error State -->
    <ErrorState
      v-else-if="error"
      :title="t('projects.edit.errorTitle')"
      :message="error"
      :retry-label="t('common.tryAgain')"
      @retry="fetchProject"
    >
      <template #action>
        <NuxtLink
          :to="`/projects/${route.params.id}`"
          class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          {{ t('projects.edit.backToProject') }}
        </NuxtLink>
      </template>
    </ErrorState>

    <!-- Edit Form -->
    <div v-else-if="project" class="space-y-8">
      <!-- Page Header -->
      <PageHeader
        :title="t('projects.edit.title')"
        :subtitle="t('projects.edit.subtitle')"
      />

      <!-- Form Card -->
      <Card>
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">{{ t('projects.edit.formTitle') }}</h2>
        <ProjectForm
          v-model="formData"
          :hackathons="hackathons"
          :hackathons-loading="hackathonsLoading"
          :hackathons-error="hackathonsError"
          :submitting="submitting"
          :disabled="submitting"
          :errors="{}"
          @submit="submitForm"
          @reset="resetForm"
          @retry-hackathons="fetchHackathons"
          @image-upload="handleProjectImageUpload"
          @remove-image="removeProjectImage"
        />

        <!-- Delete Project Button (outside form) -->
        <div class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ t('projects.edit.dangerZone') }}</h3>
          <p class="text-gray-600 dark:text-gray-400 mb-4">{{ t('projects.edit.deleteWarning') }}</p>
          <button
            type="button"
            @click="deleteProject"
            class="px-6 py-3 bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded-lg hover:bg-red-200 dark:hover:bg-red-900/30 transition-colors"
          >
            {{ t('projects.edit.deleteButton') }}
          </button>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from '#imports'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useFileUpload } from '~/composables/useFileUpload'
import { createPreviewUrl } from '~/utils/fileUpload'
import PageHeader from '~/components/molecules/PageHeader.vue'
import Card from '~/components/atoms/Card.vue'
import LoadingState from '~/components/molecules/LoadingState.vue'
import ErrorState from '~/components/molecules/ErrorState.vue'
import ProjectForm from '~/components/organisms/forms/ProjectForm.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()
const { t } = useI18n()
const { uploadSingle, validateFile: validateFileComposable } = useFileUpload({ 
  type: 'project',
  autoErrorHandling: false, // Wir behandeln Errors selbst
  trackProgress: false // Kein Progress-Tracking für einfache Uploads
})

const loading = ref(true)
const error = ref<string | null>(null)
const submitting = ref(false)
const project = ref<any>(null)
const hackathons = ref<any[]>([])
const hackathonsLoading = ref(false)
const hackathonsError = ref<string | undefined>(undefined)

// Form data compatible with ProjectForm component
const formData = ref({
  name: '',
  description: '',
  hackathonId: '',
  teamId: null as number | null,
  techStack: [] as string[],
  githubUrl: '',
  demoUrl: '',
  teamMembers: [] as Array<{ name: string, email: string }>,
  image_url: ''
})

// Fetch project details
const fetchProject = async () => {
  try {
    loading.value = true
    error.value = null

    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    const response = await authStore.fetchWithAuth(`/api/projects/${projectId}`)

    if (!response.ok) {
      if (response.status === 404) {
        error.value = t('projects.edit.notFound')
      } else {
        error.value = t('projects.edit.loadError', { status: response.status })
      }
      return
    }

    const data = await response.json()
    project.value = data

    // Check if user is authorized to edit
    if (authStore.user?.id !== data.owner_id) {
      error.value = t('projects.edit.unauthorized')
      return
    }

    // Transform API data to ProjectForm format
    formData.value = {
      name: data.title || '',
      description: data.description || '',
      hackathonId: data.hackathon_id ? String(data.hackathon_id) : '',
      teamId: data.team_id || null,
      techStack: data.technologies ? data.technologies.split(',').map((t: string) => t.trim()).filter((t: string) => t) : [],
      githubUrl: data.repository_url || '',
      demoUrl: data.live_url || '',
      teamMembers: data.team_members && Array.isArray(data.team_members) && data.team_members.length > 0
        ? data.team_members.map((member: any) => ({
            name: member.name || '',
            email: member.email || ''
          }))
        : [{ name: '', email: '' }],
      image_url: data.image_path || ''
    }

  } catch (err) {
    console.error('Error fetching project:', err)
    error.value = t('projects.edit.loadErrorGeneric')
  } finally {
    // Fetch hackathons for the dropdown
    await fetchHackathons()
    loading.value = false
  }
}

// Fetch hackathons
const fetchHackathons = async () => {
  try {
    hackathonsLoading.value = true
    hackathonsError.value = undefined
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    const response = await authStore.fetchWithAuth(`/api/hackathons`)

    if (response.ok) {
      hackathons.value = await response.json()
    } else {
      hackathonsError.value = t('projects.edit.hackathonsLoadError')
    }
  } catch (err) {
    console.error('Error fetching hackathons:', err)
    hackathonsError.value = t('projects.edit.hackathonsLoadError')
  } finally {
    hackathonsLoading.value = false
  }
}

// Handle image upload
const handleProjectImageUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files || !input.files[0]) {
    return
  }

  const file = input.files[0]
  const validationError = validateFileComposable(file)
  if (validationError) {
    uiStore.showError(validationError, t('projects.edit.uploadError'))
    return
  }

  submitting.value = true
  try {
    // Create preview for immediate display
    const previewUrl = await createPreviewUrl(file)
    formData.value.image_url = previewUrl

    // Upload file to backend via useFileUpload composable
    const response = await uploadSingle(file, {
      type: 'project'
    })

    // Update with actual file path from backend
    formData.value.image_url = response.url
    uiStore.showSuccess(t('projects.edit.uploadSuccess'))
  } catch (err) {
    uiStore.showError(t('projects.edit.uploadFailed'), t('projects.edit.uploadError'))
    console.error('Project image upload failed:', err)
  } finally {
    submitting.value = false
  }
}

const removeProjectImage = () => {
  formData.value.image_url = ''
}

const resetForm = () => {
  // Reset to original project data
  if (project.value) {
    formData.value = {
      name: project.value.title || '',
      description: project.value.description || '',
      hackathonId: project.value.hackathon_id ? String(project.value.hackathon_id) : '',
      teamId: project.value.team_id || null,
      techStack: project.value.technologies ? project.value.technologies.split(',').map((t: string) => t.trim()).filter((t: string) => t) : [],
      githubUrl: project.value.repository_url || '',
      demoUrl: project.value.live_url || '',
      teamMembers: project.value.team_members && Array.isArray(project.value.team_members) && project.value.team_members.length > 0
        ? project.value.team_members.map((member: any) => ({
            name: member.name || '',
            email: member.email || ''
          }))
        : [{ name: '', email: '' }],
      image_url: project.value.image_path || ''
    }
  }
}

// Submit form
const submitForm = async (data: any) => {
  if (submitting.value) return

  try {
    submitting.value = true

    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      uiStore.showWarning(t('projects.edit.authRequired'), t('projects.edit.authTitle'))
      return
    }

    // Transform form data to API payload
    const payload: any = {
      title: data.name,
      description: data.description,
      technologies: data.techStack.join(','),
      repository_url: data.githubUrl,
      live_url: data.demoUrl,
      hackathon_id: data.hackathonId ? parseInt(data.hackathonId) : null,
      team_id: data.teamId,
      image_path: data.image_url || null
    }

    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (response.ok) {
      uiStore.showSuccess(t('projects.edit.updateSuccess'))
      router.push(`/projects/${projectId}`)
    } else {
      if (response.status === 401) {
        uiStore.showError(t('projects.edit.sessionExpired'), t('projects.edit.authError'))
      } else if (response.status === 403) {
        uiStore.showError(t('projects.edit.unauthorizedEdit'), t('projects.edit.authError'))
      } else {
        uiStore.showError(t('projects.edit.updateFailed'), t('projects.edit.updateError'))
      }
    }
  } catch (err) {
    console.error('Error updating project:', err)
    uiStore.showError(t('projects.edit.updateErrorGeneric'), t('projects.edit.updateError'))
  } finally {
    submitting.value = false
  }
}

// Delete project
const deleteProject = async () => {
  if (!confirm(t('projects.edit.deleteConfirm'))) {
    return
  }

  try {
    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      uiStore.showWarning(t('projects.edit.authRequired'), t('projects.edit.authTitle'))
      return
    }

    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      uiStore.showSuccess(t('projects.edit.deleteSuccess'))
      router.push('/projects')
    } else {
      if (response.status === 401) {
        uiStore.showError(t('projects.edit.sessionExpired'), t('projects.edit.authError'))
      } else if (response.status === 403) {
        uiStore.showError(t('projects.edit.unauthorizedDelete'), t('projects.edit.authError'))
      } else {
        uiStore.showError(t('projects.edit.deleteFailed'), t('projects.edit.deleteError'))
      }
    }
  } catch (err) {
    console.error('Error deleting project:', err)
    uiStore.showError(t('projects.edit.deleteErrorGeneric'), t('projects.edit.deleteError'))
  }
}

onMounted(() => {
  fetchProject()
})
</script>