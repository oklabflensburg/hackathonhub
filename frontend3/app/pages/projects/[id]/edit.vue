<template>
  <div class="max-w-4xl mx-auto py-8">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-16">
      <svg class="w-24 h-24 text-red-400 mx-auto mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Error Loading Project</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
      <NuxtLink 
        :to="`/projects/${route.params.id}`" 
        class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to Project
      </NuxtLink>
    </div>

    <!-- Edit Form -->
    <div v-else-if="project" class="space-y-8">
       <!-- Page Header -->
       <div>
         <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ $t('projects.edit.title') }}</h1>
         <p class="text-gray-600 dark:text-gray-400 mt-2">
           {{ $t('projects.edit.subtitle') }}
         </p>
       </div>

       <!-- Form -->
       <div class="card">
         <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">{{ $t('projects.edit.formTitle') }}</h2>
        
        <form @submit.prevent="submitForm" class="space-y-6">
          <!-- Project Title -->
          <div>
            <label class="label">Project Title *</label>
            <input
              v-model="form.title"
              type="text"
              required
              class="input"
               :placeholder="$t('create.projectForm.fields.projectNamePlaceholder')"
            />
          </div>

          <!-- Description -->
          <div>
            <label class="label">Description *</label>
            <textarea
              v-model="form.description"
              required
              rows="4"
              class="input"
               :placeholder="$t('create.projectForm.fields.descriptionPlaceholder')"
            ></textarea>
          </div>

           <!-- Hackathon Selection -->
           <div>
             <label class="label">Hackathon</label>
             <div v-if="hackathonsLoading" class="input flex items-center">
               <div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary-600 mr-2"></div>
               <span class="text-gray-500">Loading hackathons...</span>
             </div>
             <select v-else v-model="form.hackathon_id" class="input">
               <option :value="null">No hackathon</option>
               <option v-for="hackathon in hackathons" :key="hackathon.id" :value="hackathon.id">
                 {{ hackathon.name }}
               </option>
             </select>
           </div>

           <!-- Team Selection -->
           <div>
             <label class="label">{{ $t('create.projectForm.fields.team') }}</label>
             <TeamSelection
               v-model:team-id="form.team_id"
               :hackathon-id="form.hackathon_id"
               :initial-team-id="project?.team_id"
               :disabled="!form.hackathon_id"
             />
             <p v-if="form.team_id" class="mt-2 text-sm text-gray-600 dark:text-gray-400">
               {{ $t('create.projectForm.fields.teamSelectedHelp') }}
             </p>
           </div>

           <!-- Tech Stack -->
           <div>
             <label class="label">Tech Stack</label>
             <div class="flex flex-wrap gap-2 mb-2">
               <span
                 v-for="tech in techStackArray"
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
                 class="px-4 py-2 bg-primary-600 text-white rounded-r-lg hover:bg-primary-700 transition-colors"
               >
                 Add
               </button>
             </div>
            </div>

           <!-- Team Members (only shown when no team is selected) -->
           <div v-if="showTeamMembers">
             <label class="label">Team Members</label>
             <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
               {{ $t('create.projectForm.teamMembersHelp') }}
             </p>
             <div class="space-y-3">
               <div
                 v-for="(member, index) in teamMembers"
                 :key="index"
                 class="flex items-center space-x-3"
               >
                 <input
                   v-model="member.name"
                   type="text"
                   class="input flex-1"
                    :placeholder="$t('create.projectForm.fields.memberNamePlaceholder')"
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
                   :disabled="teamMembers.length === 1"
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
           
           <!-- Team Selected Info -->
           <div v-if="form.team_id" class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
             <div class="flex items-center space-x-3">
               <div class="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-800 flex items-center justify-center">
                 <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                   <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                 </svg>
               </div>
               <div>
                 <h4 class="font-medium text-gray-900 dark:text-white">{{ $t('create.projectForm.fields.teamSelected') }}</h4>
                 <p class="text-sm text-gray-600 dark:text-gray-400">{{ $t('create.projectForm.fields.teamSelectedHelp') }}</p>
               </div>
             </div>
           </div>

           <!-- Repository URL -->
          <div>
            <label class="label">Repository URL</label>
            <input
              v-model="form.repository_url"
              type="url"
              class="input"
               :placeholder="$t('create.projectForm.fields.githubPlaceholder')"
            />
          </div>

          <!-- Live URL -->
          <div>
            <label class="label">Live Demo URL</label>
            <input
              v-model="form.live_url"
              type="url"
              class="input"
               :placeholder="$t('create.projectForm.fields.demoPlaceholder')"
            />
          </div>

          <!-- Status -->
          <div>
            <label class="label">Status</label>
            <select v-model="form.status" class="input">
              <option value="active">Active</option>
              <option value="completed">Completed</option>
              <option value="archived">Archived</option>
            </select>
          </div>

          <!-- Visibility -->
          <div>
            <label class="flex items-center space-x-3">
              <input
                v-model="form.is_public"
                type="checkbox"
                class="w-5 h-5 text-primary-600 rounded focus:ring-primary-500"
              />
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
                Make project public
              </span>
            </label>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Public projects are visible to everyone. Private projects are only visible to you and team members.
            </p>
          </div>

          <!-- Image Upload -->
          <div>
            <label class="label">Project Image</label>
            <div
              @click="triggerImageUpload"
              class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center cursor-pointer hover:border-primary-500 dark:hover:border-primary-400 transition-colors"
              :class="{ 'border-primary-500 dark:border-primary-400': form.image_path }"
            >
              <div v-if="!form.image_path">
                <svg class="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
                  Click to upload project image
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">
                  PNG, JPG, GIF or WebP. Max 10MB.
                </p>
              </div>
              <div v-else class="space-y-2">
                <div class="w-32 h-32 mx-auto rounded-lg overflow-hidden">
                  <img :src="form.image_path" alt="Project preview" class="w-full h-full object-cover" />
                </div>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  Image uploaded
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
            <div v-if="uploadError" class="mt-2 text-sm text-red-600 dark:text-red-400">
              {{ uploadError }}
            </div>
            <div v-if="uploading" class="mt-2 text-sm text-gray-600 dark:text-gray-400">
              Uploading image...
            </div>
          </div>

          <!-- Form Actions -->
          <div class="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
            <NuxtLink 
              :to="`/projects/${route.params.id}`" 
              class="px-6 py-3 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Cancel
            </NuxtLink>
            
            <div class="flex items-center space-x-4">
              <button
                type="button"
                @click="deleteProject"
                class="px-6 py-3 bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded-lg hover:bg-red-200 dark:hover:bg-red-900/30 transition-colors"
              >
                Delete Project
              </button>
              
              <button
                type="submit"
                :disabled="submitting"
                class="px-8 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <span v-if="submitting">Saving...</span>
                <span v-else>Save Changes</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from '#imports'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { uploadFile, createPreviewUrl, validateFile } from '~/utils/fileUpload'
import TeamSelection from '~/components/TeamSelection.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

const loading = ref(true)
const error = ref<string | null>(null)
const submitting = ref(false)
const project = ref<any>(null)
const hackathons = ref<any[]>([])
const hackathonsLoading = ref(false)
const newTech = ref('')
const teamMembers = ref<Array<{name: string, email: string}>>([{ name: '', email: '' }])
const imageInput = ref<HTMLInputElement>()
const uploading = ref(false)
const uploadError = ref<string | null>(null)

const form = ref({
  title: '',
  description: '',
  technologies: '',
  repository_url: '',
  live_url: '',
  status: 'active',
  is_public: true,
  image_path: '',
  hackathon_id: null as number | null,
  team_id: null as number | null
})

// Computed property to convert technologies string to array for UI
const techStackArray = computed(() => {
  if (!form.value.technologies) return []
  return form.value.technologies.split(',').map(tech => tech.trim()).filter(tech => tech.length > 0)
})

// Computed property to conditionally show team members
const showTeamMembers = computed(() => {
  return !form.value.team_id
})

// Methods for tech stack management
const addTech = () => {
  if (newTech.value.trim() && !techStackArray.value.includes(newTech.value.trim())) {
    const currentTechs = [...techStackArray.value, newTech.value.trim()]
    form.value.technologies = currentTechs.join(',')
    newTech.value = ''
  }
}

const removeTech = (tech: string) => {
  const currentTechs = techStackArray.value.filter(t => t !== tech)
  form.value.technologies = currentTechs.join(',')
}

// Methods for team members management
const addTeamMember = () => {
  teamMembers.value.push({ name: '', email: '' })
}

const removeTeamMember = (index: number) => {
  if (teamMembers.value.length > 1) {
    teamMembers.value.splice(index, 1)
  }
}

// Image upload methods
const triggerImageUpload = () => {
  imageInput.value?.click()
}

const handleImageUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files || !input.files[0]) {
    return
  }
  
  const file = input.files[0]
  
  // Validate file
  const validationError = validateFile(file)
  if (validationError) {
    uploadError.value = validationError
    return
  }
  
  uploading.value = true
  uploadError.value = null
  
  try {
    // Create preview for immediate display
    const previewUrl = await createPreviewUrl(file)
    form.value.image_path = previewUrl
    
    // Upload file to backend
    const response = await uploadFile(file, {
      type: 'project'
    })
    
    // Update with actual file path from backend
    form.value.image_path = response.url
    
  } catch (error) {
    uploadError.value = error instanceof Error ? error.message : 'Upload failed'
    console.error('Project image upload failed:', error)
  } finally {
    uploading.value = false
  }
}

const removeImage = () => {
  form.value.image_path = ''
  if (imageInput.value) {
    imageInput.value.value = ''
  }
  uploadError.value = null
}

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
        error.value = 'Project not found'
      } else {
        error.value = `Failed to load project: ${response.status}`
      }
      return
    }
    
    const data = await response.json()
    project.value = data
    
    // Check if user is authorized to edit
    if (authStore.user?.id !== data.owner_id) {
      error.value = 'You are not authorized to edit this project'
      return
    }
    
    // Populate form
    form.value = {
      title: data.title || '',
      description: data.description || '',
      technologies: data.technologies || '',
      repository_url: data.repository_url || '',
      live_url: data.live_url || '',
      status: data.status || 'active',
      is_public: data.is_public !== false,
      image_path: data.image_path || '',
      hackathon_id: data.hackathon_id || null,
      team_id: data.team_id || null
    }

    // Initialize team members from API data if available, otherwise start with one empty member
    if (data.team_members && Array.isArray(data.team_members) && data.team_members.length > 0) {
      teamMembers.value = data.team_members.map((member: any) => ({
        name: member.name || '',
        email: member.email || ''
      }))
    } else {
      teamMembers.value = [{ name: '', email: '' }]
    }
  } catch (err) {
    console.error('Error fetching project:', err)
    error.value = 'Failed to load project details'
  } finally {
    // Fetch hackathons for the dropdown
    await fetchHackathons()
    
    loading.value = false
  }
}

const fetchHackathons = async () => {
  try {
    hackathonsLoading.value = true
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    
    const response = await authStore.fetchWithAuth(`/api/hackathons`)
    
    if (response.ok) {
      hackathons.value = await response.json()
    }
  } catch (err) {
    console.error('Error fetching hackathons:', err)
  } finally {
    hackathonsLoading.value = false
  }
}

const submitForm = async () => {
  if (submitting.value) return
  
  try {
    submitting.value = true
    
    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    
    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      uiStore.showWarning('Please log in to edit projects.', 'Authentication Required')
      return
    }
    
    // Prepare payload
    const payload: any = {}
    if (form.value.title) payload.title = form.value.title
    if (form.value.description) payload.description = form.value.description
    if (form.value.technologies !== undefined) payload.technologies = form.value.technologies
    if (form.value.repository_url !== undefined) payload.repository_url = form.value.repository_url
    if (form.value.live_url !== undefined) payload.live_url = form.value.live_url
    if (form.value.status) payload.status = form.value.status
    if (form.value.is_public !== undefined) payload.is_public = form.value.is_public
    if (form.value.image_path !== undefined) payload.image_path = form.value.image_path || null
    if (form.value.hackathon_id !== undefined) payload.hackathon_id = form.value.hackathon_id
    if (form.value.team_id !== undefined) payload.team_id = form.value.team_id
    
    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
    
    if (response.ok) {
      uiStore.showSuccess('Project updated successfully!')
      router.push(`/projects/${projectId}`)
    } else {
      if (response.status === 401) {
        // fetchWithAuth should have handled refresh, but if still 401, token is invalid
        uiStore.showError('Session expired. Please log in again.', 'Authentication Error')
      } else if (response.status === 403) {
        uiStore.showError('You are not authorized to edit this project.', 'Authorization Error')
      } else {
        uiStore.showError('Failed to update project', 'Update Failed')
      }
    }
  } catch (err) {
    console.error('Error updating project:', err)
    uiStore.showError('An error occurred while updating the project', 'Update Error')
  } finally {
    submitting.value = false
  }
}

const deleteProject = async () => {
  if (!confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
    return
  }
  
  try {
    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    
    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      uiStore.showWarning('Please log in to delete projects.', 'Authentication Required')
      return
    }
    
    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      uiStore.showSuccess('Project deleted successfully!')
      router.push('/projects')
    } else {
      if (response.status === 401) {
        // fetchWithAuth should have handled refresh, but if still 401, token is invalid
        uiStore.showError('Session expired. Please log in again.', 'Authentication Error')
      } else if (response.status === 403) {
        uiStore.showError('You are not authorized to delete this project.', 'Authorization Error')
      } else {
        uiStore.showError('Failed to delete project', 'Delete Failed')
      }
    }
  } catch (err) {
    console.error('Error deleting project:', err)
    uiStore.showError('An error occurred while deleting the project', 'Delete Error')
  }
}

onMounted(() => {
  fetchProject()
})
</script>