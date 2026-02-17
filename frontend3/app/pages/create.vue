<template>
  <div class="max-w-4xl mx-auto">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Create</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        Submit a new project or create a hackathon
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
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">Submit New Project</h2>
        
        <form @submit.prevent="submitProject" class="space-y-6">
          <!-- Project Name -->
          <div>
            <label class="label">Project Name</label>
            <input
              v-model="projectForm.name"
              type="text"
              required
              class="input"
              placeholder="Enter your project name"
            />
          </div>

          <!-- Description -->
          <div>
            <label class="label">Description</label>
            <textarea
              v-model="projectForm.description"
              required
              rows="4"
              class="input"
              placeholder="Describe your project, what problem it solves, and how it works"
            ></textarea>
          </div>

          <!-- Hackathon Selection -->
          <div>
            <label class="label">Hackathon</label>
            <div v-if="hackathonsLoading" class="input flex items-center">
              <div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary-600 mr-2"></div>
              <span class="text-gray-500">Loading hackathons...</span>
            </div>
            <div v-else-if="hackathonsError" class="input text-red-600 bg-red-50 dark:bg-red-900/20">
              Error loading hackathons: {{ hackathonsError }}
              <button @click="fetchHackathons" class="ml-2 text-primary-600 hover:text-primary-800">Retry</button>
            </div>
            <select v-else v-model="projectForm.hackathonId" class="input" required>
              <option value="">Select a hackathon</option>
              <option v-for="hackathon in hackathons" :key="hackathon.id" :value="hackathon.id">
                {{ hackathon.name }} ({{ hackathon.status }})
              </option>
            </select>
          </div>

          <!-- Tech Stack -->
          <div>
            <label class="label">Tech Stack</label>
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
                placeholder="Add a technology (e.g., React, Python)"
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
              <label class="label">GitHub Repository</label>
              <input
                v-model="projectForm.githubUrl"
                type="url"
                class="input"
                placeholder="https://github.com/username/project"
              />
            </div>
            <div>
              <label class="label">Live Demo URL</label>
              <input
                v-model="projectForm.demoUrl"
                type="url"
                class="input"
                placeholder="https://demo.example.com"
              />
            </div>
          </div>

          <!-- Team Members -->
          <div>
            <label class="label">Team Members</label>
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
                  placeholder="Team member name"
                  required
                />
                <input
                  v-model="member.email"
                  type="email"
                  class="input flex-1"
                  placeholder="Email address"
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
              Add Team Member
            </button>
          </div>

          <!-- Image Upload -->
          <div>
            <label class="label">Project Image</label>
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
                  Click to upload project image
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">
                  PNG, JPG, GIF up to 5MB
                </p>
              </div>
              <div v-else class="space-y-2">
                <div class="w-32 h-32 mx-auto rounded-lg overflow-hidden">
                  <img :src="projectForm.image" alt="Project preview" class="w-full h-full object-cover" />
                </div>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  Image uploaded successfully
                </p>
                <button
                  type="button"
                  @click.stop="removeImage"
                  class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300"
                >
                  Remove image
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
              Reset
            </button>
            <button type="submit" :disabled="submitting" class="btn btn-primary">
              <svg v-if="submitting" class="w-5 h-5 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Submit Project
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Hackathon Form -->
    <div v-else class="space-y-6">
      <div class="card">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">Create New Hackathon</h2>
        
        <form @submit.prevent="submitHackathon" class="space-y-6">
          <!-- Hackathon Name -->
          <div>
            <label class="label">Hackathon Name</label>
            <input
              v-model="hackathonForm.name"
              type="text"
              required
              class="input"
              placeholder="Enter hackathon name"
            />
          </div>

          <!-- Description -->
          <div>
            <label class="label">Description</label>
            <textarea
              v-model="hackathonForm.description"
              required
              rows="4"
              class="input"
              placeholder="Describe the hackathon theme, goals, and target audience"
            ></textarea>
          </div>

          <!-- Organization -->
          <div>
            <label class="label">Organization</label>
            <input
              v-model="hackathonForm.organization"
              type="text"
              required
              class="input"
              placeholder="Organization or company name"
            />
          </div>

          <!-- Dates -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="label">Start Date & Time</label>
              <input
                v-model="hackathonForm.startDate"
                type="datetime-local"
                required
                class="input"
              />
            </div>
            <div>
              <label class="label">End Date & Time</label>
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
            <label class="label">Location</label>
            <div class="flex space-x-4">
              <label class="flex items-center">
                <input
                  v-model="hackathonForm.locationType"
                  type="radio"
                  value="online"
                  class="mr-2"
                />
                <span class="text-gray-700 dark:text-gray-300">Online</span>
              </label>
              <label class="flex items-center">
                <input
                  v-model="hackathonForm.locationType"
                  type="radio"
                  value="in-person"
                  class="mr-2"
                />
                <span class="text-gray-700 dark:text-gray-300">In-person</span>
              </label>
              <label class="flex items-center">
                <input
                  v-model="hackathonForm.locationType"
                  type="radio"
                  value="hybrid"
                  class="mr-2"
                />
                <span class="text-gray-700 dark:text-gray-300">Hybrid</span>
              </label>
            </div>
            <input
              v-if="hackathonForm.locationType !== 'online'"
              v-model="hackathonForm.location"
              type="text"
              class="input mt-3"
              placeholder="Enter location (city, venue)"
            />
          </div>

          <!-- Prize Pool -->
          <div>
            <label class="label">Prize Pool</label>
            <input
              v-model="hackathonForm.prizePool"
              type="text"
              class="input"
              placeholder="e.g., $50,000 or TBD"
            />
          </div>

          <!-- Tags -->
          <div>
            <label class="label">Tags</label>
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
                placeholder="Add a tag (e.g., AI, Web3, Sustainability)"
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
            <label class="label">Rules & Guidelines</label>
            <textarea
              v-model="hackathonForm.rules"
              rows="4"
              class="input"
              placeholder="List any rules, guidelines, or requirements for participants"
            ></textarea>
          </div>

          <!-- Contact Information -->
          <div>
            <label class="label">Contact Email</label>
            <input
              v-model="hackathonForm.contactEmail"
              type="email"
              required
              class="input"
              placeholder="contact@example.com"
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

const uiStore = useUIStore()
const route = useRoute()
const config = useRuntimeConfig()

const activeTab = ref<'project' | 'hackathon'>('project')
const tabs = [
  { id: 'project' as const, label: 'Submit Project' },
  { id: 'hackathon' as const, label: 'Create Hackathon' }
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
  contactEmail: ''
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
    const response = await fetch(`${config.public.apiUrl}/api/hackathons`)
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

const handleImageUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    const reader = new FileReader()
    reader.onload = (e) => {
      projectForm.value.image = e.target?.result as string
    }
    reader.readAsDataURL(input.files[0])
  }
}

const removeImage = () => {
  projectForm.value.image = ''
  if (imageInput.value) {
    imageInput.value.value = ''
  }
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
    const response = await authStore.fetchWithAuth('/api/projects/', {
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
    resetProjectForm()
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
      // owner_id will be set by backend based on current user
    }
    
    // Make real API call with authentication using fetchWithAuth for auto-refresh
    const response = await authStore.fetchWithAuth('/api/hackathons/', {
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
    resetHackathonForm()
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
    contactEmail: ''
  }
  newTag.value = ''
}
</script>