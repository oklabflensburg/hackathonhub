<template>
  <div class="team-projects-panel bg-white dark:bg-gray-900 rounded-lg shadow-sm border border-gray-200 dark:border-gray-800">
    <!-- Panel Header -->
    <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            Team Projects
          </h3>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {{ projects.length }} projects in this team
          </p>
        </div>
        
        <div class="flex items-center space-x-3">
          <!-- Add Project Button -->
          <button
            v-if="canAddProject"
            @click="$emit('add-project')"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-800 text-white rounded-lg font-medium transition-colors flex items-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            Add Project
          </button>
        </div>
      </div>
    </div>
    
    <!-- Projects List -->
    <div class="p-6">
      <!-- Empty State -->
      <div
        v-if="projects.length === 0"
        class="text-center py-12"
      >
        <div class="mx-auto w-16 h-16 text-gray-300 dark:text-gray-700 mb-4">
          <svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
          No projects yet
        </h3>
        <p class="text-gray-500 dark:text-gray-400 mb-6 max-w-md mx-auto">
          This team doesn't have any projects yet. Create the first project to get started.
        </p>
        <button
          v-if="canAddProject"
          @click="$emit('add-project')"
          class="px-6 py-3 bg-blue-600 hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-800 text-white rounded-lg font-medium transition-colors"
        >
          Create First Project
        </button>
      </div>
      
      <!-- Projects Grid -->
      <div
        v-else
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        <div
          v-for="project in projects"
          :key="project.id"
          class="bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 transition-colors overflow-hidden"
        >
          <!-- Project Header -->
          <div class="p-4 border-b border-gray-200 dark:border-gray-700">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h4 class="font-semibold text-gray-900 dark:text-white truncate">
                  {{ project.name }}
                </h4>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">
                  {{ project.description || 'No description' }}
                </p>
              </div>
              <div class="ml-4">
                <span
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    project.status === 'active' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                    project.status === 'completed' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' :
                    'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
                  ]"
                >
                  {{ project.status }}
                </span>
              </div>
            </div>
          </div>
          
          <!-- Project Stats -->
          <div class="p-4">
            <div class="grid grid-cols-3 gap-4 text-center">
              <div>
                <div class="text-lg font-semibold text-gray-900 dark:text-white">
                  {{ project.voteCount || 0 }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  Votes
                </div>
              </div>
              <div>
                <div class="text-lg font-semibold text-gray-900 dark:text-white">
                  {{ project.commentCount || 0 }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  Comments
                </div>
              </div>
              <div>
                <div class="text-lg font-semibold text-gray-900 dark:text-white">
                  {{ project.memberCount || 0 }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  Members
                </div>
              </div>
            </div>
            
            <!-- Project Actions -->
            <div class="mt-4 flex justify-between items-center">
              <div class="text-sm text-gray-500 dark:text-gray-400">
                {{ formatDate(project.createdAt) }}
              </div>
              <div class="flex space-x-2">
                <button
                  @click="$emit('view-project', project)"
                  class="px-3 py-1 text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium"
                >
                  View
                </button>
                <button
                  v-if="canEditProject"
                  @click="$emit('edit-project', project)"
                  class="px-3 py-1 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-300 font-medium"
                >
                  Edit
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

// Props
const props = defineProps<{
  projects: Array<{
    id: string
    name: string
    description?: string
    status: string
    voteCount?: number
    commentCount?: number
    memberCount?: number
    createdAt: string
    tags?: string[]
  }>
  canAddProject?: boolean
  canEditProject?: boolean
}>()

// Emits
const emit = defineEmits<{
  'add-project': []
  'view-project': [project: any]
  'edit-project': [project: any]
}>()

// Reactive state
const searchQuery = ref('')
const statusFilter = ref('all')
const sortBy = ref('created_at')
const showFilterDropdown = ref(false)
const showSortDropdown = ref(false)
const currentPage = ref(1)
const itemsPerPage = ref(9)

// Computed properties
const filteredProjects = computed(() => {
  let filtered = [...props.projects]
  
  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(project => 
      project.name.toLowerCase().includes(query) ||
      project.description?.toLowerCase().includes(query)
    )
  }
  
  // Filter by status
  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(project => project.status === statusFilter.value)
  }
  
  // Sort
  filtered.sort((a, b) => {
    if (sortBy.value === 'name') {
      return a.name.localeCompare(b.name)
    } else if (sortBy.value === 'created_at') {
      return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    } else if (sortBy.value === 'votes') {
      return (b.voteCount || 0) - (a.voteCount || 0)
    } else if (sortBy.value === 'comments') {
      return (b.commentCount || 0) - (a.commentCount || 0)
    }
    return 0
  })
  
  return filtered
})

const paginatedProjects = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredProjects.value.slice(start, end)
})

// Methods
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
