<template>
  <div class="max-w-4xl mx-auto">
    <!-- Page Header -->
    <PageHeader
      :title="$t('create.title')"
      :subtitle="$t('create.subtitle')"
    />

    <!-- Hackathon Form -->
    <Card>
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
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref } from '#imports'
import { useI18n } from 'vue-i18n'

// Components
import HackathonForm from '@/components/organisms/forms/HackathonForm.vue'
import PageHeader from '@/components/molecules/PageHeader.vue'
import { Card } from '@/components/atoms'

// Types
import type { Prize, Organizer } from '@/types/hackathon-types'

// Stores
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'

// Composables
import { useFileUpload } from '~/composables/useFileUpload'
import { useHackathons } from '~/composables/useHackathons'

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
  image_url: '',
  prizes: [] as Prize[],
  organizers: [] as Organizer[]
})

// State
const submitting = ref(false)
const uploadingImage = ref(false)

// Refs for file inputs
const hackathonImageInput = ref<HTMLInputElement | null>(null)

// Composables
const { t } = useI18n()
const authStore = useAuthStore()
const uiStore = useUIStore()
const { uploadSingle } = useFileUpload({ 
  type: 'hackathon',
  autoErrorHandling: false, // Wir behandeln Errors selbst
  trackProgress: false // Kein Progress-Tracking für einfache Uploads
})
const { createHackathon, isLoading: hackathonLoading } = useHackathons({
  autoErrorHandling: false, // Wir behandeln Errors selbst
  autoSuccessHandling: false // Wir zeigen eigene Success-Messages
})

const handleHackathonImageUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  uploadingImage.value = true
  try {
    // Upload file to backend via useFileUpload composable
    const result = await uploadSingle(file, { type: 'hackathon' })
    hackathonForm.value.image_url = result.url
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
    
    // Prepare data for API using HackathonCreateData format
    // Convert datetime-local inputs to full ISO format (YYYY-MM-DDTHH:mm:ss)
    const formatDateTime = (datetimeStr: string | null) => {
      if (!datetimeStr) return null
      // datetime-local returns YYYY-MM-DDTHH:mm, add seconds if missing
      if (datetimeStr.length === 16) { // YYYY-MM-DDTHH:mm
        return `${datetimeStr}:00`
      }
      return datetimeStr
    }
    
    const hackathonData: any = {
      name: formData.name,
      description: formData.description,
      startDate: formatDateTime(formData.startDate) || '',
      endDate: formatDateTime(formData.endDate) || '',
      location: formData.locationType === 'online' ? 'Virtual' : formData.location,
      prizePool: formData.prizePool,
      rules: formData.rules,
      imageUrl: formData.image_url || undefined,
      // Additional fields that will be passed through to API
      tags: formData.tags.join(','),
      contactEmail: formData.contactEmail,
      organization: formData.organization,
      prizes: formData.prizes,
      organizers: formData.organizers,
    }
    
    // Use the composable to create hackathon
    const createdHackathon = await createHackathon(hackathonData)
    
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
    image_url: '',
    prizes: [] as Prize[],
    organizers: [] as Organizer[]
  }
}
</script>
