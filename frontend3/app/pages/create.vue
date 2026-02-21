<template>
  <div class="max-w-4xl mx-auto">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ $t('create.title') }}</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        {{ $t('create.subtitle') }}
      </p>
    </div>

    <!-- Tabs -->
    <div class="flex border-b border-gray-200 dark:border-gray-700 mb-8">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="[
          'px-6 py-3 font-medium text-sm transition-colors',
          activeTab === tab.id
            ? 'border-b-2 border-primary-600 text-primary-600 dark:text-primary-400'
            : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300'
        ]"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Project Form -->
    <div v-if="activeTab === 'project'" class="space-y-6">
      <div class="card">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">{{ $t('create.projectForm.title') }}</h2>
        
        <form @submit.prevent="submitProject" class="space-y-6">
          <!-- Project Name -->
          <div>
            <label class="label">{{ $t('create.projectForm.fields.projectName') }}</label>
            <input
              v-model="projectForm.name"
              type="text"
              required
              class="input"
              :placeholder="$t('create.projectForm.fields.projectNamePlaceholder')"
            />
          </div>

          <!-- Description -->
          <div>
            <label class="label">{{ $t('create.projectForm.fields.description') }}</label>
            <textarea
              v-model="projectForm.description"
              required
              rows="4"
              class="input"
              :placeholder="$t('create.projectForm.fields.descriptionPlaceholder')"
            ></textarea>
          </div>

          <!-- Hackathon Selection -->
          <div>
            <label class="label">{{ $t('create.projectForm.fields.hackathon') }}</label>
            <div v-if="hackathonsLoading" class="input flex items-center">
              <div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary-600 mr-2"></div>
              <span class="text-gray-500">{{ $t('create.projectForm.fields.loadingHackathons') }}</span>
            </div>
            <div v-else-if="hackathonsError" class="input text-red-600 bg-red-50 dark:bg-red-900/20">
              {{ $t('create.projectForm.fields.errorLoadingHackathons') }}: {{ hackathonsError }}
              <button @click="fetchHackathons" class="ml-2 text-primary-600 hover:text-primary-800">{{ $t('create.projectForm.fields.retry') }}</button>
            </div>
            <select v-else v-model="projectForm.hackathonId" class="input" required>
               <option value="">{{ $t('create.projectForm.fields.selectHackathon') }}</option>
              <option v-for="hackathon in hackathons" :key="hackathon.id" :value="hackathon.id">
                {{ hackathon.name }} ({{ hackathon.status }})
              </option>
            </select>
          </div>

          <!-- Tech Stack -->
          <div>
            <label class="label">{{ $t('create.projectForm.fields.techStack') }}</label>
            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="tech in projectForm.techStack"
                :key="tech"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary-100 dark:bg-primary-900/30 text-primary-800 dark:text-primary-300"
              >
                {{ tech }}
                <button
                  type="button"
                  @click="removeTech(tech)"
                  class="ml-2 text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-200"
                >
                  ×
                </button>
              </span>
            </div>
            <div class="flex">
              <input
                v-model="newTech"
                type="text"
                class="input rounded-r-none"
                :placeholder="$t('create.projectForm.fields.techPlaceholder')"
                @keydown.enter.prevent="addTech"
              />
              <button
                type="button"
                @click="addTech"
                class="btn btn-primary rounded-l-none"
              >
                Add
              </button>
            </div>
          </div>

          <!-- Links -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="label">{{ $t('create.projectForm.fields.githubRepository') }}</label>
              <input
                v-model="projectForm.githubUrl"
                type="url"
                class="input"
                :placeholder="$t('create.projectForm.fields.githubPlaceholder')"
              />
            </div>
            <div>
              <label class="label">{{ $t('create.projectForm.fields.liveDemoUrl') }}</label>
              <input
                v-model="projectForm.demoUrl"
                type="url"
                class="input"
                :placeholder="$t('create.projectForm.fields.demoPlaceholder')"
              />
            </div>
          </div>

          <!-- Team Members -->
          <div>
            <label class="label">{{ $t('create.projectForm.fields.teamMembers') }}</label>
            <div class="space-y-3">
              <div
                v-for="(member, index) in projectForm.teamMembers"
                :key="index"
                class="flex items-center space-x-3"
              >
                <input
                  v-model="member.name"
                  type="text"
                  class="input flex-1"
                   :placeholder="$t('create.projectForm.fields.memberNamePlaceholder')"
                  required
                />
                <input
                  v-model="member.email"
                  type="email"
                  class="input flex-1"
                   :placeholder="$t('create.projectForm.fields.emailPlaceholder')"
                />
                <button
                  type="button"
                  @click="removeTeamMember(index)"
                  class="p-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg"
                  :disabled="projectForm.teamMembers.length === 1"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            <button
              type="button"
              @click="addTeamMember"
              class="mt-3 btn btn-outline"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
               {{ $t('create.projectForm.fields.addTeamMember') }}
            </button>
          </div>

          <!-- Image Upload -->
          <div>
            <label class="label">{{ $t('create.projectForm.fields.projectImage') }}</label>
            <div
              @click="triggerImageUpload"
              class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center cursor-pointer hover:border-primary-500 dark:hover:border-primary-400 transition-colors"
              :class="{ 'border-primary-500 dark:border-primary-400': projectForm.image }"
            >
              <div v-if="!projectForm.image">
                <svg class="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
                   {{ $t('create.projectForm.fields.clickToUpload') }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">
                   {{ $t('create.projectForm.fields.imageRequirements') }}
                </p>
              </div>
              <div v-else class="space-y-2">
                <div class="w-32 h-32 mx-auto rounded-lg overflow-hidden">
                  <img :src="projectForm.image" alt="Project preview" class="w-full h-full object-cover" />
                </div>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                   {{ $t('create.projectForm.fields.imageUploaded') }}
                </p>
                <button
                  type="button"
                  @click.stop="removeImage"
                  class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300"
                >
                   {{ $t('create.projectForm.fields.removeImage') }}
                </button>
              </div>
              <input
                ref="imageInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleImageUpload"
              />
            </div>
          </div>

          <!-- Submit Button -->
           <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
            <button type="button" @click="resetProjectForm" class="btn btn-outline">
              {{ $t('create.projectForm.buttons.reset') }}
            </button>
            <button type="submit" :disabled="submitting" class="btn btn-primary">
              <svg v-if="submitting" class="w-5 h-5 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              {{ $t('create.projectForm.buttons.submitProject') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Hackathon Form -->
    <div v-else class="space-y-6">
      <div class="card">
         <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">{{ $t('create.hackathonForm.title') }}</h2>
        
        <form @submit.prevent="submitHackathon" class="space-y-6">
          <!-- Hackathon Name -->
          <div>
            <label class="label">{{ $t('create.hackathonForm.fields.hackathonName') }}</label>
            <input
              v-model="hackathonForm.name"
              type="text"
              required
              class="input"
              :placeholder="$t('create.hackathonForm.fields.namePlaceholder')"
            />
          </div>

          <!-- Description -->
          <div>
            <label class="label">{{ $t('create.hackathonForm.fields.description') }}</label>
            <textarea
              v-model="hackathonForm.description"
              required
              rows="4"
              class="input"
              :placeholder="$t('create.hackathonForm.fields.descriptionPlaceholder')"
            ></textarea>
          </div>

          <!-- Organization -->
          <div>
            <label class="label">{{ $t('create.hackathonForm.fields.organizer') }}</label>
            <input
              v-model="hackathonForm.organization"
              type="text"
              required
              class="input"
              :placeholder="$t('create.hackathonForm.fields.organizerPlaceholder')"
            />
          </div>

          <!-- Dates -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="label">{{ $t('create.hackathonForm.fields.startDate') }}</label>
              <input
                v-model="hackathonForm.startDate"
                type="datetime-local"
                required
                class="input"
              />
            </div>
            <div>
              <label class="label">{{ $t('create.hackathonForm.fields.endDate') }}</label>
              <input
                v-model="hackathonForm.endDate"
                type="datetime-local"
                required
                class="input"
              />
            </div>
          </div>

          <!-- Location -->
          <div>
            <label class="label">{{ $t('create.hackathonForm.fields.location') }}</label>
            <div class="flex space-x-4">
              <label class="flex items-center">
                <input
                  v-model="hackathonForm.locationType"
                  type="radio"
                  value="online"
                  class="mr-2"
                />
                <span class="text-gray-700 dark:text-gray-300">{{ $t('hackathons.filters.online') }}</span>
              </label>
              <label class="flex items-center">
                <input
                  v-model="hackathonForm.locationType"
                  type="radio"
                  value="in-person"
                  class="mr-2"
                />
                <span class="text-gray-700 dark:text-gray-300">{{ $t('hackathons.filters.inPerson') }}</span>
              </label>
              <label class="flex items-center">
                <input
                  v-model="hackathonForm.locationType"
                  type="radio"
                  value="hybrid"
                  class="mr-2"
                />
                <span class="text-gray-700 dark:text-gray-300">{{ $t('hackathons.filters.hybrid') }}</span>
              </label>
            </div>
            <input
              v-if="hackathonForm.locationType !== 'online'"
              v-model="hackathonForm.location"
              type="text"
              class="input mt-3"
              :placeholder="$t('create.hackathonForm.fields.locationPlaceholder')"
            />
          </div>

          <!-- Prize Pool -->
          <div>
            <label class="label">{{ $t('create.hackathonForm.fields.prizePool') }}</label>
            <input
              v-model="hackathonForm.prizePool"
              type="text"
              class="input"
              :placeholder="$t('create.hackathonForm.fields.prizePlaceholder')"
            />
          </div>

          <!-- Tags -->
          <div>
            <label class="label">{{ $t('create.hackathonForm.fields.tags') }}</label>
            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="tag in hackathonForm.tags"
                :key="tag"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary-100 dark:bg-primary-900/30 text-primary-800 dark:text-primary-300"
              >
                {{ tag }}
                <button
                  type="button"
                  @click="removeTag(tag)"
                  class="ml-2 text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-200"
                >
                  ×
                </button>
              </span>
            </div>
            <div class="flex">
              <input
                v-model="newTag"
                type="text"
                class="input rounded-r-none"
                :placeholder="$t('create.hackathonForm.fields.tagsPlaceholder')"
                @keydown.enter.prevent="addTag"
              />
              <button
                type="button"
                @click="addTag"
                class="btn btn-primary rounded-l-none"
              >
                Add
              </button>
            </div>
          </div>

          <!-- Rules & Guidelines -->
          <div>
            <label class="label">{{ $t('create.hackathonForm.fields.rules') }}</label>
            <textarea
              v-model="hackathonForm.rules"
              rows="4"
              class="input"
              :placeholder="$t('create.hackathonForm.fields.rulesPlaceholder')"
            ></textarea>
          </div>

          <!-- Image Upload -->
          <div>
            <label class="label">{{ $t('create.hackathonForm.fields.hackathonImage') }}</label>
            <div
              @click="triggerHackathonImageUpload"
              class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center cursor-pointer hover:border-primary-500 dark:hover:border-primary-400 transition-colors"
              :class="{ 'border-primary-500 dark:border-primary-400': hackathonForm.image_url }"
            >
              <div v-if="!hackathonForm.image_url">
                <svg class="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
                  {{ $t('create.hackathonForm.fields.clickToUpload') }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">
                  {{ $t('create.hackathonForm.fields.imageRequirements') }}
                </p>
              </div>
              <div v-else class="space-y-2">
                <div class="w-32 h-32 mx-auto rounded-lg overflow-hidden">
                  <img :src="hackathonForm.image_url" alt="Hackathon preview" class="w-full h-full object-cover" />
                </div>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  {{ $t('create.hackathonForm.fields.imageUploaded') }}
                </p>
                <button
                  type="button"
                  @click.stop="removeHackathonImage"
                  class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300"
                >
                  {{ $t('create.hackathonForm.fields.removeImage') }}
                </button>
              </div>
              <input
                ref="hackathonImageInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleHackathonImageUpload"
              />
            </div>
          </div>

          <!-- Contact Information -->
          <div>
            <label class="label">{{ $t('create.hackathonForm.fields.contactEmail') }}</label>
            <input
              v-model="hackathonForm.contactEmail"
              type="email"
              required
              class="input"
              :placeholder="$t('create.hackathonForm.fields.emailPlaceholder')"
            />
          </div>

          <!-- Submit Button -->
          <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
            <button type="button" @click="resetHackathonForm" class="btn btn-outline">
              Reset
            </button>
            <button type="submit" :disabled="submitting" class="btn btn-primary">
              <svg v-if="submitting" class="w-5 h-5 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Create Hackathon
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUIStore } from '~/stores/ui'

definePageMeta({
  middleware: 'auth'
})

const { t } = useI18n()
const uiStore = useUIStore()
const route = useRoute()
const config = useRuntimeConfig()

const activeTab = ref<'project' | 'hackathon'>('project')
const tabs = [
  { id: 'project' as const, label: t('create.tabs.project') },
  { id: 'hackathon' as const, label: t('create.tabs.hackathon') }
]

// Set active tab based on query parameter
onMounted(() => {
  const tabParam = route.query.tab as string
  if (tabParam === 'hackathon') {
    activeTab.value = 'hackathon'
  }
})

const submitting = ref(false)
const newTech = ref('')
const newTag = ref('')
const imageInput = ref<HTMLInputElement>()
const hackathonImageInput = ref<HTMLInputElement>()

// Import auth store
const authStore = useAuthStore()

// Project form
const projectForm = ref({
  name: '',
  description: '',
  hackathonId: '',
  techStack: ['React', 'Node.js', 'TypeScript'],
  githubUrl: '',
  demoUrl: '',
  teamMembers: [
    { name: '', email: '' }
  ],
  image: ''
})

// Hackathon form
const hackathonForm = ref({
  name: '',
  description: '',
  organization: '',
  startDate: '',
  endDate: '',
  locationType: 'online',
  location: '',
  prizePool: '',
  tags: ['Technology', 'Innovation'],
  rules: '',
  contactEmail: '',
  image_url: ''
})

// Real hackathons from API
interface HackathonOption {
  id: string
  name: string
  status: string
}

const hackathons = ref<HackathonOption[]>([])
const hackathonsLoading = ref(false)
const hackathonsError = ref<string | null>(null)

// Fetch hackathons from API
const fetchHackathons = async () => {
  hackathonsLoading.value = true
  hackathonsError.value = null
  try {
    const response = await authStore.fetchWithAuth(`${config.public.apiUrl}/api/hackathons`)
    if (!response.ok) {
      throw new Error(`Failed to fetch hackathons: ${response.status}`)
    }
    const data = await response.json()
    
    // Transform API data to match our format
    hackathons.value = data.map((h: any) => {
      const startDate = new Date(h.start_date)
      const endDate = new Date(h.end_date)
      const now = new Date()
      
      // Determine status based on dates and is_active
      let status = 'Upcoming'
      if (h.is_active === false) {
        status = 'Completed'
      } else if (startDate <= now && endDate >= now) {
        status = 'Active'
      } else if (endDate < now) {
        status = 'Completed'
      }
      
      return {
        id: h.id.toString(),
        name: h.name,
        status
      }
    })
  } catch (err: any) {
    hackathonsError.value = err.message || 'Failed to load hackathons'
    console.error('Error fetching hackathons:', err)
  } finally {
    hackathonsLoading.value = false
  }
}

// Fetch hackathons on component mount
onMounted(() => {
  fetchHackathons()
})

// Methods for project form
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
  if (projectForm.value.teamMembers.length > 1) {
    projectForm.value.teamMembers.splice(index, 1)
  }
}

const triggerImageUpload = () => {
  imageInput.value?.click()
}

// Import file upload utilities
import { uploadFile, createPreviewUrl, validateFile } from '~/utils/fileUpload'

const projectUploading = ref(false)
const projectUploadError = ref<string | null>(null)
const hackathonUploading = ref(false)
const hackathonUploadError = ref<string | null>(null)

const handleImageUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files || !input.files[0]) {
    return
  }
  
  const file = input.files[0]
  
  // Validate file
  const validationError = validateFile(file)
  if (validationError) {
    projectUploadError.value = validationError
    return
  }
  
  projectUploading.value = true
  projectUploadError.value = null
  
  try {
    // Create preview for immediate display
    const previewUrl = await createPreviewUrl(file)
    projectForm.value.image = previewUrl
    
    // Upload file to backend
    const response = await uploadFile(file, {
      type: 'project'
    })
    
    // Update with actual file path from backend
    projectForm.value.image = response.url
    
  } catch (error) {
    projectUploadError.value = error instanceof Error ? error.message : 'Upload failed'
    console.error('Project image upload failed:', error)
  } finally {
    projectUploading.value = false
  }
}

const removeImage = () => {
  projectForm.value.image = ''
  if (imageInput.value) {
    imageInput.value.value = ''
  }
  projectUploadError.value = null
}

const triggerHackathonImageUpload = () => {
  hackathonImageInput.value?.click()
}

const handleHackathonImageUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files || !input.files[0]) {
    return
  }
  
  const file = input.files[0]
  
  // Validate file
  const validationError = validateFile(file)
  if (validationError) {
    hackathonUploadError.value = validationError
    return
  }
  
  hackathonUploading.value = true
  hackathonUploadError.value = null
  
  try {
    // Create preview for immediate display
    const previewUrl = await createPreviewUrl(file)
    hackathonForm.value.image_url = previewUrl
    
    // Upload file to backend
    const response = await uploadFile(file, {
      type: 'hackathon'
    })
    
    // Update with actual file path from backend
    hackathonForm.value.image_url = response.url
    
  } catch (error) {
    hackathonUploadError.value = error instanceof Error ? error.message : 'Upload failed'
    console.error('Hackathon image upload failed:', error)
  } finally {
    hackathonUploading.value = false
  }
}

const removeHackathonImage = () => {
  hackathonForm.value.image_url = ''
  if (hackathonImageInput.value) {
    hackathonImageInput.value.value = ''
  }
  hackathonUploadError.value = null
}

// Methods for hackathon form
const addTag = () => {
  if (newTag.value.trim() && !hackathonForm.value.tags.includes(newTag.value.trim())) {
    hackathonForm.value.tags.push(newTag.value.trim())
    newTag.value = ''
  }
}

const removeTag = (tag: string) => {
  hackathonForm.value.tags = hackathonForm.value.tags.filter(t => t !== tag)
}

// Form submission
const submitProject = async () => {
  submitting.value = true
  try {
    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      uiStore.showError('Authentication required', 'Please log in to submit a project.')
      submitting.value = false
      return
    }
    
    // Prepare data for API
    const projectData = {
      title: projectForm.value.name,
      description: projectForm.value.description,
      hackathon_id: parseInt(projectForm.value.hackathonId) || null,
      technologies: projectForm.value.techStack.join(','),
      github_url: projectForm.value.githubUrl,
      demo_url: projectForm.value.demoUrl,
      // team_members would be handled separately in a real app
      image_path: projectForm.value.image || null,
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

const submitHackathon = async () => {
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
      name: hackathonForm.value.name,
      description: hackathonForm.value.description,
      organization: hackathonForm.value.organization,
      start_date: formatDateTime(hackathonForm.value.startDate),
      end_date: formatDateTime(hackathonForm.value.endDate),
      location: hackathonForm.value.locationType === 'online' ? 'Virtual' : hackathonForm.value.location,
      prize_pool: hackathonForm.value.prizePool,
      tags: hackathonForm.value.tags.join(','),
      rules: hackathonForm.value.rules,
      contact_email: hackathonForm.value.contactEmail,
      image_url: hackathonForm.value.image_url || null,
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
    techStack: ['React', 'Node.js', 'TypeScript'],
    githubUrl: '',
    demoUrl: '',
    teamMembers: [
      { name: '', email: '' }
    ],
    image: ''
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
    locationType: 'online',
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