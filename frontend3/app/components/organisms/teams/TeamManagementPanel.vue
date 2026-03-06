<template>
  <div class="team-management-panel">
    <div class="panel-header mb-6">
      <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">
        Team Management
      </h2>
      <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
        Manage your team settings, members, and visibility
      </p>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-state text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">Loading team settings...</p>
    </div>
    
    <!-- Content -->
    <div v-else class="panel-content">
      <!-- Form Sections -->
      <div class="space-y-8">
        <!-- Basic Information -->
        <div class="form-section bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Basic Information
          </h3>
          
          <div class="space-y-4">
            <!-- Team Name -->
            <div class="form-group">
              <label for="team-name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Team Name *
              </label>
              <input
                id="team-name"
                v-model="formData.name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
                :class="{ 'border-red-300 dark:border-red-600': errors.name }"
                placeholder="Enter team name"
              />
              <p v-if="errors.name" class="mt-1 text-sm text-red-600 dark:text-red-400">
                {{ errors.name }}
              </p>
            </div>
            
            <!-- Team Description -->
            <div class="form-group">
              <label for="team-description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Description
              </label>
              <textarea
                id="team-description"
                v-model="formData.description"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
                :class="{ 'border-red-300 dark:border-red-600': errors.description }"
                placeholder="Describe your team's purpose, goals, and interests"
              />
              <p v-if="errors.description" class="mt-1 text-sm text-red-600 dark:text-red-400">
                {{ errors.description }}
              </p>
              <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                Optional. Describe what your team is about.
              </p>
            </div>
            
            <!-- Team Tags -->
            <div class="form-group">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Tags
              </label>
              <div class="flex flex-wrap gap-2 mb-2">
                <span
                  v-for="(tag, index) in formData.tags"
                  :key="index"
                  class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200"
                >
                  {{ tag }}
                  <button
                    type="button"
                    class="ml-1.5 text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-200"
                    @click="removeTag(index)"
                  >
                    ×
                  </button>
                </span>
              </div>
              <div class="flex">
                <input
                  v-model="newTag"
                  type="text"
                  class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-l-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
                  placeholder="Add a tag (press Enter)"
                  @keyup.enter="addTag"
                />
                <button
                  type="button"
                  class="px-4 py-2 border border-l-0 border-gray-300 dark:border-gray-600 rounded-r-md bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600"
                  @click="addTag"
                >
                  Add
                </button>
              </div>
              <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                Add tags to help others find your team (e.g., "react", "python", "design")
              </p>
            </div>
          </div>
        </div>
        
        <!-- Team Settings -->
        <div class="form-section bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Team Settings
          </h3>
          
          <div class="space-y-4">
            <!-- Visibility -->
            <div class="form-group">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Visibility *
              </label>
              <div class="space-y-2">
                <div class="flex items-center">
                  <input
                    id="visibility-public"
                    v-model="formData.visibility"
                    type="radio"
                    value="public"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600"
                  />
                  <label for="visibility-public" class="ml-3 block text-sm font-medium text-gray-700 dark:text-gray-300">
                    <span class="font-semibold">Public</span>
                    <span class="text-gray-500 dark:text-gray-400 block text-xs mt-1">
                      Anyone can see the team and request to join
                    </span>
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    id="visibility-private"
                    v-model="formData.visibility"
                    type="radio"
                    value="private"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600"
                  />
                  <label for="visibility-private" class="ml-3 block text-sm font-medium text-gray-700 dark:text-gray-300">
                    <span class="font-semibold">Private</span>
                    <span class="text-gray-500 dark:text-gray-400 block text-xs mt-1">
                      Only invited members can see and join the team
                    </span>
                  </label>
                </div>
              </div>
              <p v-if="errors.visibility" class="mt-1 text-sm text-red-600 dark:text-red-400">
                {{ errors.visibility }}
              </p>
            </div>
            
            <!-- Max Members -->
            <div class="form-group">
              <label for="max-members" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Maximum Members
              </label>
              <div class="flex items-center space-x-4">
                <input
                  id="max-members"
                  v-model="formData.maxMembers"
                  type="number"
                  min="1"
                  max="100"
                  class="w-32 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
                  :class="{ 'border-red-300 dark:border-red-600': errors.maxMembers }"
                  placeholder="Unlimited"
                />
                <span class="text-sm text-gray-600 dark:text-gray-400">
                  Leave empty for unlimited members
                </span>
              </div>
              <p v-if="errors.maxMembers" class="mt-1 text-sm text-red-600 dark:text-red-400">
                {{ errors.maxMembers }}
              </p>
            </div>
            
            <!-- Hackathon -->
            <div class="form-group">
              <label for="hackathon" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Associated Hackathon
              </label>
              <input
                id="hackathon"
                v-model="formData.hackathonId"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
                :class="{ 'border-red-300 dark:border-red-600': errors.hackathonId }"
                placeholder="Hackathon ID (optional)"
              />
              <p v-if="errors.hackathonId" class="mt-1 text-sm text-red-600 dark:text-red-400">
                {{ errors.hackathonId }}
              </p>
              <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                Optional. Associate this team with a specific hackathon.
              </p>
            </div>
          </div>
        </div>
        
        <!-- Danger Zone -->
        <div class="form-section bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800 p-6">
          <h3 class="text-lg font-semibold text-red-800 dark:text-red-300 mb-4">
            Danger Zone
          </h3>
          
          <div class="space-y-4">
            <!-- Delete Team -->
            <div class="danger-item">
              <div class="flex items-start justify-between">
                <div>
                  <h4 class="text-md font-medium text-red-800 dark:text-red-300">
                    Delete Team
                  </h4>
                  <p class="text-sm text-red-700 dark:text-red-400 mt-1">
                    Once you delete a team, there is no going back. This will permanently delete the team and all associated data.
                  </p>
                </div>
                <button
                  type="button"
                  class="px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  @click="confirmDelete"
                >
                  Delete Team
                </button>
              </div>
            </div>
            
            <!-- Archive Team -->
            <div v-if="team.status !== 'archived'" class="danger-item">
              <div class="flex items-start justify-between">
                <div>
                  <h4 class="text-md font-medium text-red-800 dark:text-red-300">
                    Archive Team
                  </h4>
                  <p class="text-sm text-red-700 dark:text-red-400 mt-1">
                    Archive the team to hide it from public view. Archived teams can be restored later.
                  </p>
                </div>
                <button
                  type="button"
                  class="px-4 py-2 border border-red-300 dark:border-red-700 text-sm font-medium rounded-md shadow-sm text-red-700 dark:text-red-300 bg-white dark:bg-gray-800 hover:bg-red-50 dark:hover:bg-red-900/30 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  @click="archiveTeam"
                >
                  Archive Team
                </button>
              </div>
            </div>
            
            <!-- Restore Team -->
            <div v-if="team.status === 'archived'" class="danger-item">
              <div class="flex items-start justify-between">
                <div>
                  <h4 class="text-md font-medium text-green-800 dark:text-green-300">
                    Restore Team
                  </h4>
                  <p class="text-sm text-green-700 dark:text-green-400 mt-1">
                    Restore the team to make it active again.
                  </p>
                </div>
                <button
                  type="button"
                  class="px-4 py-2 border border-green-300 dark:border-green-700 text-sm font-medium rounded-md shadow-sm text-green-700 dark:text-green-300 bg-white dark:bg-gray-800 hover:bg-green-50 dark:hover:bg-green-900/30 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                  @click="restoreTeam"
                >
                  Restore Team
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Action Buttons -->
        <div class="action-buttons flex justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
          <button
            type="button"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            @click="resetForm"
          >
            Reset
          </button>
          <button
            type="button"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            :disabled="saving || !hasChanges"
            @click="saveChanges"
          >
            <span v-if="saving" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Saving...
            </span>
            <span v-else>
              Save Changes
            </span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-500 dark:bg-gray-900 bg-opacity-75 dark:bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg max-w-md w-full p-6">
        <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4">
          Delete Team
        </h3>
        <p class="text-gray-700 dark:text-gray-300 mb-6">
          Are you sure you want to delete "<strong>{{ team.name }}</strong>"? This action cannot be undone.
        </p>
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
            @click="showDeleteModal = false"
          >
            Cancel
          </button>
          <button
            type="button"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            @click="deleteTeam"
          >
            Delete Team
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import type { Team, TeamVisibility } from '~/types/team-types'

const props = withDefaults(defineProps<{
  team: Team
  loading?: boolean
}>(), {
  loading: false,
})

const emit = defineEmits<{
  update: [team: Partial<Team>]
  delete: [teamId: string]
  archive: [teamId: string]
  restore: [teamId: string]
}>()

// Form state
const formData = reactive({
  name: props.team.name,
  description: props.team.description || '',
  visibility: props.team.visibility,
  maxMembers: props.team.maxMembers || null,
  hackathonId: props.team.hackathonId || '',
  tags: [...(props.team.tags || [])],
})

// UI state
const newTag = ref('')
const saving = ref(false)
const showDeleteModal = ref(false)
const errors = reactive<Record<string, string>>({})

// Computed properties
const hasChanges = computed(() => {
  return (
    formData.name !== props.team.name ||
    formData.description !== (props.team.description || '') ||
    formData.visibility !== props.team.visibility ||
    formData.maxMembers !== props.team.maxMembers ||
    formData.hackathonId !== (props.team.hackathonId || '') ||
    JSON.stringify(formData.tags) !== JSON.stringify(props.team.tags || [])
  )
})

// Methods
const addTag = () => {
  const tag = newTag.value.trim()
  if (tag && !formData.tags.includes(tag)) {
    formData.tags.push(tag)
    newTag.value = ''
  }
}

const removeTag = (index: number) => {
  formData.tags.splice(index, 1)
}

const validateForm = (): boolean => {
  // Clear previous errors
  Object.keys(errors).forEach(key => delete errors[key])
  
  let isValid = true
  
  // Validate name
  if (!formData.name.trim()) {
    errors.name = 'Team name is required'
    isValid = false
  } else if (formData.name.length < 3) {
    errors.name = 'Team name must be at least 3 characters'
    isValid = false
  } else if (formData.name.length > 100) {
    errors.name = 'Team name must be less than 100 characters'
    isValid = false
  }
  
  // Validate description
  if (formData.description && formData.description.length > 500) {
    errors.description = 'Description must be less than 500 characters'
    isValid = false
  }
  
  // Validate max members
  if (formData.maxMembers !== null) {
    const maxMembers = Number(formData.maxMembers)
    if (isNaN(maxMembers) || maxMembers < 1 || maxMembers > 100) {
      errors.maxMembers = 'Maximum members must be between 1 and 100'
      isValid = false
    }
  }
  
  // Validate hackathon ID
  if (formData.hackathonId && !formData.hackathonId.match(/^[a-zA-Z0-9_-]+$/)) {
    errors.hackathonId = 'Invalid hackathon ID format'
    isValid = false
  }
  
  return isValid
}

const saveChanges = async () => {
  if (!validateForm()) {
    return
  }
  
  saving.value = true
  
  try {
    // Prepare update data
    const updateData: Partial<Team> = {
      name: formData.name,
      description: formData.description || null,
      visibility: formData.visibility,
      maxMembers: formData.maxMembers,
      hackathonId: formData.hackathonId || null,
      tags: formData.tags,
    }
    
    // Emit update event
    emit('update', updateData)
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
  } catch (error) {
    console.error('Failed to save team:', error)
    errors.general = 'Failed to save changes. Please try again.'
  } finally {
    saving.value = false
  }
}

const resetForm = () => {
  formData.name = props.team.name
  formData.description = props.team.description || ''
  formData.visibility = props.team.visibility
  formData.maxMembers = props.team.maxMembers || null
  formData.hackathonId = props.team.hackathonId || ''
  formData.tags = [...(props.team.tags || [])]
  
  // Clear errors
  Object.keys(errors).forEach(key => delete errors[key])
}

const confirmDelete = () => {
  showDeleteModal.value = true
}

const deleteTeam = () => {
  emit('delete', props.team.id)
  showDeleteModal.value = false
}

const archiveTeam = () => {
  emit('archive', props.team.id)
}

const restoreTeam = () => {
  emit('restore', props.team.id)
}

// Watch for team changes
watch(() => props.team, (newTeam) => {
  resetForm()
}, { deep: true })
</script>

<style scoped>
.form-section {
  transition: all 0.2s ease;
}

.danger-item {
  padding: 1rem;
  border-radius: 0.5rem;
  background-color: rgba(254, 226, 226, 0.5);
}

.dark .danger-item {
  background-color: rgba(127, 29, 29, 0.2);
}

.action-buttons button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>