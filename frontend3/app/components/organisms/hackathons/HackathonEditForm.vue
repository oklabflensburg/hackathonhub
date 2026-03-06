<template>
  <div v-if="visible" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
      <div class="p-4 sm:p-5 lg:p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ $t('hackathons.details.editHackathon') }}</h2>
          <button @click="$emit('cancel')"
            class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Use the enhanced HackathonForm component -->
        <HackathonForm
          v-model="formData"
          :submitting="loading"
          :disabled="loading"
          :errors="{}"
          @submit="handleSave"
          @reset="handleReset"
          @image-upload="handleImageUpload"
          @remove-image="removeImage"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import HackathonForm from '~/components/organisms/forms/HackathonForm.vue'

interface Prize {
  name: string
  description: string
  value: string
}

interface Organizer {
  name: string
  role: string
}

interface Props {
  visible: boolean
  formData: {
    name: string
    description: string
    organization?: string
    start_date: string
    end_date: string
    location_type?: 'online' | 'in-person'
    location: string
    prize_pool?: string
    tags?: string[]
    rules?: string
    contact_email?: string
    image_url?: string
    prizes?: Prize[]
    organizers?: Organizer[]
  }
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  formData: () => ({
    name: '',
    description: '',
    organization: '',
    start_date: '',
    end_date: '',
    location_type: 'online',
    location: '',
    prize_pool: '',
    tags: [],
    rules: '',
    contact_email: '',
    image_url: '',
    prizes: [],
    organizers: []
  })
})

const emit = defineEmits<{
  save: [data: any]
  cancel: []
}>()

// Transform props.formData to HackathonForm format
const formData = ref({
  name: props.formData.name,
  description: props.formData.description,
  organization: props.formData.organization || '',
  startDate: props.formData.start_date,
  endDate: props.formData.end_date,
  locationType: props.formData.location_type || 'online',
  location: props.formData.location,
  prizePool: props.formData.prize_pool || '',
  tags: props.formData.tags || [],
  rules: props.formData.rules || '',
  contactEmail: props.formData.contact_email || '',
  image_url: props.formData.image_url || '',
  prizes: props.formData.prizes || [],
  organizers: props.formData.organizers || []
})

// Update formData when props.formData changes
watch(() => props.formData, (newData) => {
  formData.value = {
    name: newData.name,
    description: newData.description,
    organization: newData.organization || '',
    startDate: newData.start_date,
    endDate: newData.end_date,
    locationType: newData.location_type || 'online',
    location: newData.location,
    prizePool: newData.prize_pool || '',
    tags: newData.tags || [],
    rules: newData.rules || '',
    contactEmail: newData.contact_email || '',
    image_url: newData.image_url || '',
    prizes: newData.prizes || [],
    organizers: newData.organizers || []
  }
}, { deep: true })

// Emit save event with transformed data
const handleSave = () => {
  // Transform back to original format
  const saveData = {
    name: formData.value.name,
    description: formData.value.description,
    organization: formData.value.organization,
    start_date: formData.value.startDate,
    end_date: formData.value.endDate,
    location_type: formData.value.locationType,
    location: formData.value.location,
    prize_pool: formData.value.prizePool,
    tags: formData.value.tags,
    rules: formData.value.rules,
    contact_email: formData.value.contactEmail,
    image_url: formData.value.image_url,
    prizes: formData.value.prizes,
    organizers: formData.value.organizers
  }
  emit('save', saveData)
}

const handleReset = () => {
  // Reset to original props.formData
  formData.value = {
    name: props.formData.name,
    description: props.formData.description,
    organization: props.formData.organization || '',
    startDate: props.formData.start_date,
    endDate: props.formData.end_date,
    locationType: props.formData.location_type || 'online',
    location: props.formData.location,
    prizePool: props.formData.prize_pool || '',
    tags: props.formData.tags || [],
    rules: props.formData.rules || '',
    contactEmail: props.formData.contact_email || '',
    image_url: props.formData.image_url || '',
    prizes: props.formData.prizes || [],
    organizers: props.formData.organizers || []
  }
}

// Image upload functionality (passed to HackathonForm)
const handleImageUpload = (event: Event) => {
  // Forward to parent if needed
  console.log('Image upload event', event)
}

const removeImage = () => {
  formData.value.image_url = ''
}
</script>