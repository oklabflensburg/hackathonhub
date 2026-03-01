<template>
  <FormWizard
    v-model:active-tab="activeTab"
    v-model:project-form-data="projectForm"
    v-model:hackathon-form-data="hackathonForm"
    :hackathons="hackathons"
    :hackathons-loading="hackathonsLoading"
    :hackathons-error="hackathonsError"
    :submitting="submitting"
    :disabled="submitting"
    :errors="{}"
    :title="$t('create.title')"
    :subtitle="$t('create.subtitle')"
    :project-form-title="$t('create.projectForm.title')"
    :hackathon-form-title="$t('create.hackathonForm.title')"
    :project-name-label="$t('create.projectForm.fields.projectName')"
    :project-name-placeholder="$t('create.projectForm.fields.projectNamePlaceholder')"
    :project-description-label="$t('create.projectForm.fields.description')"
    :project-description-placeholder="$t('create.projectForm.fields.descriptionPlaceholder')"
    :hackathon-label="$t('create.projectForm.fields.hackathon')"
    :loading-hackathons-text="$t('create.projectForm.fields.loadingHackathons')"
    :error-loading-hackathons-text="$t('create.projectForm.fields.errorLoadingHackathons')"
    :retry-text="$t('create.projectForm.fields.retry')"
    :select-hackathon-text="$t('create.projectForm.fields.selectHackathon')"
    :team-label="$t('create.projectForm.fields.team') || 'Team'"
    :tech-stack-label="$t('create.projectForm.fields.techStack')"
    :tech-placeholder="$t('create.projectForm.fields.techPlaceholder')"
    :add-text="'Add'"
    :github-repository-label="$t('create.projectForm.fields.githubRepository')"
    :github-placeholder="$t('create.projectForm.fields.githubPlaceholder')"
    :live-demo-url-label="$t('create.projectForm.fields.liveDemoUrl')"
    :demo-placeholder="$t('create.projectForm.fields.demoPlaceholder')"
    :team-members-label="$t('create.projectForm.fields.teamMembers')"
    :team-members-help-text="$t('create.projectForm.fields.teamMembersHelp')"
    :member-name-placeholder="$t('create.projectForm.fields.memberNamePlaceholder')"
    :team-member-email-placeholder="$t('create.projectForm.fields.emailPlaceholder')"
    :add-team-member-text="$t('create.projectForm.fields.addTeamMember')"
    :team-selected-text="$t('create.projectForm.fields.teamSelected')"
    :team-selected-help-text="$t('create.projectForm.fields.teamSelectedHelp')"
    :hackathon-name-label="$t('create.hackathonForm.fields.hackathonName')"
    :hackathon-name-placeholder="$t('create.hackathonForm.fields.namePlaceholder')"
    :hackathon-description-label="$t('create.hackathonForm.fields.description')"
    :hackathon-description-placeholder="$t('create.hackathonForm.fields.descriptionPlaceholder')"
    :organizer-label="$t('create.hackathonForm.fields.organizer')"
    :organizer-placeholder="$t('create.hackathonForm.fields.organizerPlaceholder')"
    :start-date-label="$t('create.hackathonForm.fields.startDate')"
    :end-date-label="$t('create.hackathonForm.fields.endDate')"
    :location-label="$t('create.hackathonForm.fields.location')"
    :online-text="$t('hackathons.filters.online')"
    :in-person-text="$t('hackathons.filters.inPerson')"
    :location-placeholder="$t('create.hackathonForm.fields.locationPlaceholder')"
    :prize-pool-label="$t('create.hackathonForm.fields.prizePool')"
    :prize-pool-placeholder="$t('create.hackathonForm.fields.prizePoolPlaceholder')"
    :tags-label="$t('create.hackathonForm.fields.tags')"
    :tags-placeholder="$t('create.hackathonForm.fields.tagsPlaceholder')"
    :rules-label="$t('create.hackathonForm.fields.rules')"
    :rules-placeholder="$t('create.hackathonForm.fields.rulesPlaceholder')"
    :hackathon-image-label="$t('create.hackathonForm.fields.hackathonImage')"
    :click-to-upload-text="$t('create.hackathonForm.fields.clickToUpload')"
    :image-requirements-text="$t('create.hackathonForm.fields.imageRequirements')"
    :image-alt-text="'Hackathon preview'"
    :image-uploaded-text="$t('create.hackathonForm.fields.imageUploaded')"
    :remove-image-text="$t('create.hackathonForm.fields.removeImage')"
    :contact-email-label="$t('create.hackathonForm.fields.contactEmail')"
    :contact-email-placeholder="$t('create.hackathonForm.fields.emailPlaceholder')"
    :reset-text="$t('create.projectForm.buttons.reset')"
    :project-submit-text="$t('create.projectForm.buttons.submitProject')"
    :hackathon-submit-text="'Create Hackathon'"
    @project-submit="submitProject"
    @project-reset="resetProjectForm"
    @hackathon-submit="submitHackathon"
    @hackathon-reset="resetHackathonForm"
    @retry-hackathons="fetchHackathons"
    @hackathon-image-upload="handleHackathonImageUpload"
    @hackathon-remove-image="removeHackathonImage"
  />
</template>

<script setup lang="ts">
import { ref, onMounted } from '#imports'
import FormWizard from '@/components/organisms/forms/FormWizard.vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'

// Tabs
const activeTab = ref('project')

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
  ]
})

// Hackathon form
const hackathonForm = ref({
  name: '',
  description: '',
  organization: '',
  startDate: '',
  endDate: '',
  locationType: 'online' as 'online' | 'in-person',
  location: '',
  prizePool: '',
  tags: ['Technology', 'Innovation'],
  rules: '',
  contactEmail: '',
  image_url: ''
})

// State
const submitting = ref(false)
const hackathons = ref<any[]>([])
const hackathonsLoading = ref(false)
const hackathonsError = ref('')
const newTech = ref('')
const newTag = ref('')

// Refs for file inputs
const imageInput = ref<HTMLInputElement | null>(null)
const hackathonImageInput = ref<HTMLInputElement | null>(null)

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

// Project form methods
const addTech = () => {
  if (newTech.value.trim() && !projectForm.value.techStack.includes(newTech.value.trim())) {
    projectForm.value.techStack.push(newTech.value.trim())
    newTech.value = ''
  }
}

const removeTech = (tech: string) => {
  projectForm.value.techStack = projectForm.value.techStack.filter(t => t !== tech)
}

const addTeamMember = () => {
  projectForm.value.teamMembers.push({ name: '', email: '' })
}

const removeTeamMember = (index: number) => {
  if (projectForm.value.teamMembers.length <= 1) return
  projectForm.value.teamMembers.splice(index, 1)
}

// Hackathon form methods
const addTag = () => {
  if (newTag.value.trim() && !hackathonForm.value.tags.includes(newTag.value.trim())) {
    hackathonForm.value.tags.push(newTag.value.trim())
    newTag.value = ''
  }
}

const removeTag = (tag: string) => {
  hackathonForm.value.tags = hackathonForm.value.tags.filter(t => t !== tag)
}

// Image upload methods
const triggerImageUpload = () => {
  imageInput.value?.click()
}

const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    // In a real app, you would upload the file and get a URL
    const reader = new FileReader()
    reader.onload = (e) => {
      // For demo purposes, set a data URL
      // In production, you would upload to a server
      console.log('Image uploaded:', file.name)
    }
    reader.readAsDataURL(file)
  }
}

const removeImage = () => {
  // Clear image
  console.log('Image removed')
}

const triggerHackathonImageUpload = () => {
  hackathonImageInput.value?.click()
}

const handleHackathonImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    // In a real app, you would upload the file and get a URL
    const reader = new FileReader()
    reader.onload = (e) => {
      hackathonForm.value.image_url = e.target?.result as string
    }
    reader.readAsDataURL(file)
  }
}

const removeHackathonImage = () => {
  hackathonForm.value.image_url = ''
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
      image_path: null, // Would be set after image upload
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

const submitHackathon = async (formData: any) => {
  submitting.value = true
  try {
    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      uiStore.showError('Authentication required', 'Please log in to create a hackathon.')
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
    
    // Debug: log token (remove in production)
    console.log('Using token for hackathon creation:', authStore.token ? 'Token present' : 'Token missing')
    
    // Prepare data for API
    // Convert datetime-local inputs to full ISO format (YYYY-MM-DDTHH:mm:ss)
    const formatDateTime = (datetimeStr: string | null) => {
      if (!datetimeStr) return null
      // datetime-local returns YYYY-MM-DDTHH:mm, add seconds if missing
      if (datetimeStr.length === 16) { // YYYY-MM-DDTHH:mm
        return `${datetimeStr}:00`
      }
      return datetimeStr
    }
    
    const hackathonData = {
      name: formData.name,
      description: formData.description,
      organization: formData.organization,
      start_date: formatDateTime(formData.startDate),
      end_date: formatDateTime(formData.endDate),
      location: formData.locationType === 'online' ? 'Virtual' : formData.location,
      prize_pool: formData.prizePool,
      tags: formData.tags.join(','),
      rules: formData.rules,
      contact_email: formData.contactEmail,
      image_url: formData.image_url || null,
      // owner_id will be set by backend based on current user
    }
    
    // Make real API call with authentication using fetchWithAuth for auto-refresh
    const response = await authStore.fetchWithAuth('/api/hackathons', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(hackathonData)
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      
      // Extract error message from response
      let errorMessage = `Failed to create hackathon: ${response.status}`
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
    
    const createdHackathon = await response.json()
    
    uiStore.showSuccess('Hackathon created successfully!', `"${createdHackathon.name}" is now live on the platform.`)
    // Navigate to hackathon detail page
    navigateTo(`/hackathons/${createdHackathon.id}`)
  } catch (error) {
    console.error('Error creating hackathon:', error)
    let errorMessage = 'Unknown error occurred'
    if (error instanceof Error) {
      errorMessage = error.message
      // Ensure errorMessage is a string (not [object Object])
      if (errorMessage.includes('[object Object]')) {
        errorMessage = 'Validation error occurred. Please check your input.'
      }
    }
    uiStore.showError('Failed to create hackathon. Please try again.', errorMessage)
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
    ]
  }
  newTech.value = ''
}

const resetHackathonForm = () => {
  hackathonForm.value = {
    name: '',
    description: '',
    organization: '',
    startDate: '',
    endDate: '',
    locationType: 'online' as 'online' | 'in-person',
    location: '',
    prizePool: '',
    tags: ['Technology', 'Innovation'],
    rules: '',
    contactEmail: '',
    image_url: ''
  }
  newTag.value = ''
}
</script>
