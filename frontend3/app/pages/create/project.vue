<template>
  <div class="max-w-4xl mx-auto">
    <!-- Page Header -->
    <PageHeader
      :title="$t('create.title')"
      :subtitle="$t('create.subtitle')"
    />

    <!-- Project Form -->
    <Card>
      <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">{{ $t('create.projectForm.title') }}</h2>
      <ProjectForm
        v-model="projectForm"
        :hackathons="hackathons"
        :hackathons-loading="hackathonsLoading"
        :hackathons-error="hackathonsError"
        :submitting="submitting"
        :disabled="submitting"
        :errors="{}"
        @submit="submitProject"
        @reset="resetProjectForm"
        @retry-hackathons="fetchHackathons"
        @image-upload="handleProjectImageUpload"
        @remove-image="removeProjectImage"
      />
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from '#imports'
import ProjectForm from '@/components/organisms/forms/ProjectForm.vue'
import PageHeader from '@/components/molecules/PageHeader.vue'
import Card from '@/components/atoms/Card.vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { uploadFile } from '@/utils/fileUpload'

// Project form
const projectForm = ref({
  name: '',
  description: '',
  hackathonId: '',
  teamId: null as number | null,
  techStack: ['React', 'Node.js', 'TypeScript'],
  githubUrl: '',
  demoUrl: '',
  teamMembers: [
    { name: '', email: '' }
  ],
  image_url: ''
})

// State
const submitting = ref(false)
const hackathons = ref<any[]>([])
const hackathonsLoading = ref(false)
const hackathonsError = ref('')
const newTech = ref('')

// Composables
const { t } = useI18n()
const authStore = useAuthStore()
const uiStore = useUIStore()

// Fetch hackathons on mount
onMounted(() => {
  fetchHackathons()
})

const fetchHackathons = async () => {
  hackathonsLoading.value = true
  hackathonsError.value = ''
  try {
    const response = await authStore.fetchWithAuth('/api/hackathons')
    if (!response.ok) {
      throw new Error(`Failed to fetch hackathons: ${response.status}`)
    }
    hackathons.value = await response.json()
  } catch (error) {
    console.error('Error fetching hackathons:', error)
    hackathonsError.value = error instanceof Error ? error.message : 'Unknown error'
  } finally {
    hackathonsLoading.value = false
  }
}

// Image upload handling
const uploadingImage = ref(false)

const handleProjectImageUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  uploadingImage.value = true
  try {
    // Upload file to backend via upload endpoint
    const result = await uploadFile(file, { type: 'project' })
    projectForm.value.image_url = result.url
    uiStore.showSuccess('Bild hochgeladen', 'Das Bild wurde erfolgreich hochgeladen.')
  } catch (error) {
    console.error('Image upload failed:', error)
    let errorMessage = 'Unbekannter Fehler beim Hochladen'
    if (error instanceof Error) {
      errorMessage = error.message
    }
    uiStore.showError('Upload fehlgeschlagen', errorMessage)
    // Reset file input to allow re-selection
    if (target) target.value = ''
  } finally {
    uploadingImage.value = false
  }
}

const removeProjectImage = () => {
  projectForm.value.image_url = ''
}

// Form submission
const submitProject = async (formData: any) => {
  submitting.value = true
  try {
    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      uiStore.showError('Authentication required', 'Please log in to create a project.')
      submitting.value = false
      return
    }
    
    // Refresh user to ensure token is valid
    await authStore.refreshUser()
    
    // Check again after refresh
    if (!authStore.isAuthenticated || !authStore.token) {
      uiStore.showError('Session expired', 'Please log in again.')
      submitting.value = false
      return
    }
    
    const projectData = {
      title: formData.name,
      description: formData.description,
      hackathon_id: parseInt(formData.hackathonId) || null,
      team_id: formData.teamId || null,
      technologies: formData.techStack.join(','),
      github_url: formData.githubUrl,
      demo_url: formData.demoUrl,
      // team_members would be handled separately in a real app
      image_path: formData.image_url || null,
      // owner_id will be set by backend based on current user
    }
    
    // Make real API call with authentication using fetchWithAuth for auto-refresh
    const response = await authStore.fetchWithAuth('/api/projects', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(projectData)
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      
      // Extract error message from response
      let errorMessage = `Failed to create project: ${response.status}`
      if (errorData.detail) {
        if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail
        } else if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map((err: any) => {
            if (typeof err === 'object' && err.msg) return err.msg
            return JSON.stringify(err)
          }).join(', ')
        } else if (typeof errorData.detail === 'object') {
          errorMessage = JSON.stringify(errorData.detail)
        }
      }
      
      throw new Error(errorMessage)
    }
    
    const createdProject = await response.json()
    
    uiStore.showSuccess('Project submitted successfully!', `"${createdProject.title}" is now live on the platform.`)
    // Navigate to project detail page
    navigateTo(`/projects/${createdProject.id}`)
  } catch (error) {
    console.error('Error creating project:', error)
    let errorMessage = 'Unknown error occurred'
    if (error instanceof Error) {
      errorMessage = error.message
      // Ensure errorMessage is a string (not [object Object])
      if (errorMessage.includes('[object Object]')) {
        errorMessage = 'Validation error occurred. Please check your input.'
      }
    }
    uiStore.showError('Failed to submit project. Please try again.', errorMessage)
  } finally {
    submitting.value = false
  }
}

// Form reset
const resetProjectForm = () => {
  projectForm.value = {
    name: '',
    description: '',
    hackathonId: '',
    teamId: null as number | null,
    techStack: ['React', 'Node.js', 'TypeScript'],
    githubUrl: '',
    demoUrl: '',
    teamMembers: [
      { name: '', email: '' }
    ],
    image_url: ''
  }
  newTech.value = ''
}
</script>

<style scoped>
/* No custom card styles needed - using Card component */
</style>