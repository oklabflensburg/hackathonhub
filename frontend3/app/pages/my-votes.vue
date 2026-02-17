<template>
  <div class="py-8">
    <!-- Page Header -->
    <div class="mb-8">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">My Votes</h1>
          <p class="text-gray-600 dark:text-gray-400">View all projects you've voted on</p>
        </div>
      </div>

      <!-- Search and Filter Section -->
      <div class="flex flex-col md:flex-row gap-4 mb-6">
        <div class="relative flex-1">
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="$t('projects.myVotesSearchPlaceholder')"
            class="w-full pl-10 pr-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <div class="flex gap-2">
          <select
            v-model="voteTypeFilter"
            class="px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="all">All Votes</option>
            <option value="upvote">Upvotes Only</option>
            <option value="downvote">Downvotes Only</option>
          </select>
          <select
            v-model="sortBy"
            class="px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="recent">Most Recent</option>
            <option value="oldest">Oldest First</option>
            <option value="project">Project Name A-Z</option>
          </select>
        </div>
      </div>

      <!-- Selected Tags Section -->
      <div v-if="selectedTags.length > 0" class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 mb-6">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-gray-500 dark:text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Filtering by tags:</span>
          </div>
          <button
            @click="clearAllTags"
            class="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 flex items-center"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            Clear all
          </button>
        </div>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="tag in selectedTags"
            :key="tag"
            class="px-3 py-1.5 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 text-sm rounded-full flex items-center"
          >
            {{ tag }}
            <button
              @click="removeTag(tag)"
              class="ml-2 text-primary-500 hover:text-primary-700 dark:hover:text-primary-200"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </span>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredVotes.length === 0" class="text-center py-16">
      <svg class="w-24 h-24 text-gray-400 mx-auto mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
      </svg>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">No votes yet</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">You haven't voted on any projects yet.</p>
      <NuxtLink 
        to="/projects" 
        class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
        </svg>
        Browse Projects
      </NuxtLink>
    </div>

    <!-- Votes List -->
    <div v-else class="space-y-6">
      <div
        v-for="vote in filteredVotes"
        :key="vote.id"
        class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300"
      >
        <div class="md:flex">
          <!-- Project Image -->
          <div class="md:w-1/3 lg:w-1/4">
            <div class="relative h-48 md:h-full overflow-hidden">
              <img
                :src="vote.project_image || 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80'"
                :alt="vote.project_name"
                class="w-full h-full object-cover"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
              <!-- Vote Type Badge -->
              <div class="absolute top-4 left-4">
                <span
                  class="px-3 py-1.5 rounded-full text-xs font-semibold flex items-center"
                  :class="vote.vote_type === 'upvote'
                    ? 'bg-green-500 text-white'
                    : 'bg-red-500 text-white'"
                >
                  <svg
                    class="w-3 h-3 mr-1"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      v-if="vote.vote_type === 'upvote'"
                      fill-rule="evenodd"
                      d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z"
                      clip-rule="evenodd"
                    />
                    <path
                      v-else
                      fill-rule="evenodd"
                      d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  {{ vote.vote_type === 'upvote' ? 'Upvoted' : 'Downvoted' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Project Details -->
          <div class="md:w-2/3 lg:w-3/4 p-6">
            <div class="flex flex-col h-full">
              <!-- Header -->
              <div class="mb-4">
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
                      {{ vote.project_name }}
                    </h3>
                    <div class="flex flex-wrap items-center gap-2 text-sm text-gray-600 dark:text-gray-400 mb-3">
                      <div class="flex items-center">
                        <div class="w-6 h-6 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center mr-2">
                          <span class="text-xs font-medium text-gray-600 dark:text-gray-400">
                            {{ vote.project_author?.charAt(0) || 'U' }}
                          </span>
                        </div>
                        <span>By {{ vote.project_author || 'Unknown' }}</span>
                      </div>
                      <span>•</span>
                      <div class="flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                        <span>{{ vote.hackathon_name || 'Hackathon' }}</span>
                      </div>
                      <span>•</span>
                      <div class="flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span>{{ formatDate(vote.created_at) }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Project Description -->
                <p class="text-gray-700 dark:text-gray-300 mb-4 line-clamp-3">
                  {{ vote.project_description || 'No description available' }}
                </p>
              </div>

              <!-- Technology Tags -->
              <div v-if="vote.project_technologies && vote.project_technologies.length > 0" class="mb-4">
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="tech in vote.project_technologies.slice(0, 5)"
                    :key="tech"
                    class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-xs"
                  >
                    {{ tech }}
                  </span>
                  <span
                    v-if="vote.project_technologies.length > 5"
                    class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-xs"
                  >
                    +{{ vote.project_technologies.length - 5 }} more
                  </span>
                </div>
              </div>

              <!-- Stats and Actions -->
              <div class="mt-auto pt-4 border-t border-gray-200 dark:border-gray-700">
                <div class="flex items-center justify-between">
                  <!-- Stats -->
                  <div class="flex items-center space-x-6">
                    <div class="text-center">
                      <div class="text-lg font-bold text-gray-900 dark:text-white">
                        {{ vote.project_vote_count || 0 }}
                      </div>
                      <div class="text-xs text-gray-500 dark:text-gray-400">Total Votes</div>
                    </div>
                    <div class="text-center">
                      <div class="text-lg font-bold text-gray-900 dark:text-white">
                        {{ vote.project_comment_count || 0 }}
                      </div>
                      <div class="text-xs text-gray-500 dark:text-gray-400">Comments</div>
                    </div>
                    <div class="text-center">
                      <div class="text-lg font-bold text-gray-900 dark:text-white">
                        {{ vote.project_view_count || 0 }}
                      </div>
                      <div class="text-xs text-gray-500 dark:text-gray-400">Views</div>
                    </div>
                  </div>

                  <!-- Actions -->
                  <div class="flex items-center space-x-3">
                    <NuxtLink
                      :to="`/projects/${vote.project_id}`"
                      class="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium"
                    >
                      <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                      View Details
                    </NuxtLink>
                    <button
                      @click="handleRemoveVote(vote)"
                      class="inline-flex items-center px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors text-sm font-medium"
                    >
                      <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                      Remove Vote
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { format } from 'date-fns'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const loading = ref(true)
const votes = ref<any[]>([])

// Search and filter variables
const searchQuery = ref('')
const voteTypeFilter = ref('all')
const sortBy = ref('recent')
const selectedTags = ref<string[]>([])

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  try {
    return format(new Date(dateString), 'MMM dd, yyyy HH:mm')
  } catch {
    return dateString
  }
}

const fetchMyVotes = async () => {
  try {
    loading.value = true
    if (!authStore.isAuthenticated) {
      votes.value = []
      return
    }

    // Use fetchWithAuth for auto-refresh token handling
    const response = await authStore.fetchWithAuth('/api/users/me/votes')

    if (response.ok) {
      const userVotes = await response.json()
      votes.value = userVotes || []
    } else {
      votes.value = []
    }
  } catch (error) {
    console.error('Error fetching my votes:', error)
    votes.value = []
  } finally {
    loading.value = false
  }
}

const handleRemoveVote = async (vote: any) => {
  try {
    if (!authStore.isAuthenticated) return

    // Use fetchWithAuth for auto-refresh token handling
    const response = await authStore.fetchWithAuth(`/api/projects/${vote.project_id}/vote`, {
      method: 'DELETE'
    })

    if (response.ok) {
      // Remove the vote from the list
      votes.value = votes.value.filter(v => v.id !== vote.id)
      
      // Show success message
      console.log('Vote removed successfully')
    }
  } catch (error) {
    console.error('Error removing vote:', error)
  }
}

// Tag handling functions
const toggleTag = (tag: string) => {
  const index = selectedTags.value.indexOf(tag)
  if (index === -1) {
    selectedTags.value.push(tag)
  } else {
    selectedTags.value.splice(index, 1)
  }
}

const removeTag = (tag: string) => {
  const index = selectedTags.value.indexOf(tag)
  if (index !== -1) {
    selectedTags.value.splice(index, 1)
  }
}

const clearAllTags = () => {
  selectedTags.value = []
}

// Filtered votes computed property
const filteredVotes = computed(() => {
  let filtered = [...votes.value]

  // Apply vote type filter
  if (voteTypeFilter.value !== 'all') {
    filtered = filtered.filter(vote => vote.vote_type === voteTypeFilter.value)
  }

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(vote =>
      vote.project_name.toLowerCase().includes(query) ||
      vote.project_author.toLowerCase().includes(query) ||
      vote.project_description.toLowerCase().includes(query) ||
      (vote.project_technologies && vote.project_technologies.some((tech: string) => tech.toLowerCase().includes(query)))
    )
  }

  // Apply tag filter (AND logic - project must have ALL selected tags)
  if (selectedTags.value.length > 0) {
    filtered = filtered.filter(vote =>
      selectedTags.value.every(tag =>
        vote.project_technologies && vote.project_technologies.some((tech: string) => tech.toLowerCase() === tag.toLowerCase())
      )
    )
  }

  // Apply sorting
  if (sortBy.value === 'recent') {
    filtered.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
  } else if (sortBy.value === 'oldest') {
    filtered.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
  } else if (sortBy.value === 'project') {
    filtered.sort((a, b) => a.project_name.localeCompare(b.project_name))
  }

  return filtered
})

onMounted(() => {
  fetchMyVotes()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>