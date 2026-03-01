<template>
  <div class="max-w-4xl mx-auto">
    <!-- Page Header -->
    <PageHeader
      :title="$t('create.title')"
      :subtitle="$t('create.subtitle')"
    />

    <!-- Hackathon Form -->
    <div class="card">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">{{ $t('create.hackathonForm.title') }}</h2>
      <HackathonForm
        v-model="hackathonForm"
        :submitting="submitting"
        :disabled="submitting"
        :errors="{}"
        @submit="submitHackathon"
        @reset="resetHackathonForm"
        @image-upload="handleHackathonImageUpload"
        @remove-image="removeHackathonImage"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from '#imports'
import HackathonForm from '@/components/organisms/forms/HackathonForm.vue'
import PageHeader from '@/components/molecules/PageHeader.vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'

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
const newTag = ref('')

// Refs for file inputs
const hackathonImageInput = ref<HTMLInputElement | null>(null)

// Composables
const { t } = useI18n()
const authStore = useAuthStore()
const uiStore = useUIStore()

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
const resetHackathonForm = () => {
  console.log('resetHackathonForm called')
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

<style scoped>
.card {
  @apply bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6;
}
</style>