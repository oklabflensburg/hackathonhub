<template>
  <div class="max-w-7xl mx-auto py-8">
    <!-- Page Header -->
    <PageHeader
      :title="t('myVotes.title')"
      :subtitle="t('myVotes.subtitle')"
    />

    <!-- Search and Filter Section -->
    <div class="mb-8">
      <div class="flex flex-col md:flex-row gap-4 mb-6">
        <SearchBar
          v-model="searchQuery"
          :placeholder="t('projects.myVotesSearchPlaceholder')"
          class="flex-1"
          @search="handleSearch"
        />
        <div class="flex gap-2">
          <select
            v-model="voteTypeFilter"
            class="px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="all">{{ t('myVotes.filter.allVotes') }}</option>
            <option value="upvote">{{ t('myVotes.filter.upvotesOnly') }}</option>
            <option value="downvote">{{ t('myVotes.filter.downvotesOnly') }}</option>
          </select>
          <select
            v-model="sortBy"
            class="px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="recent">{{ t('myVotes.sort.recent') }}</option>
            <option value="oldest">{{ t('myVotes.sort.oldest') }}</option>
            <option value="project">{{ t('myVotes.sort.project') }}</option>
          </select>
        </div>
      </div>

      <!-- Selected Tags -->
      <SelectedTags
        v-if="selectedTags.length > 0"
        :tags="selectedTags"
        @remove-tag="removeTag"
        @clear-all="clearAllTags"
        :title="t('myVotes.filteringByTags')"
      />
    </div>

    <!-- Loading State -->
    <LoadingState
      v-if="loading"
      :message="t('common.loading')"
    />

    <!-- Empty State -->
    <EmptyState
      v-else-if="filteredVotes.length === 0"
      :title="t('myVotes.emptyState.noVotes')"
      :description="t('myVotes.emptyState.description')"
      :action-label="t('myVotes.emptyState.browseProjects')"
      action-to="/projects"
      icon="vote"
    />

    <!-- Votes List -->
    <div v-else class="space-y-6">
      <VoteItem
        v-for="vote in filteredVotes"
        :key="vote.id"
        :vote="vote"
        @tag-click="toggleTag"
        @remove-vote="handleRemoveVote"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'
import PageHeader from '~/components/molecules/PageHeader.vue'
import SearchBar from '~/components/molecules/SearchBar.vue'
import SelectedTags from '~/components/molecules/SelectedTags.vue'
import LoadingState from '~/components/molecules/LoadingState.vue'
import EmptyState from '~/components/molecules/EmptyState.vue'
import VoteItem from '~/components/organisms/VoteItem.vue'

const authStore = useAuthStore()
const uiStore = useUIStore()
const { t } = useI18n()
const loading = ref(true)
const votes = ref<any[]>([])

// Search and filter variables
const searchQuery = ref('')
const voteTypeFilter = ref('all')
const sortBy = ref('recent')
const selectedTags = ref<string[]>([])

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
    uiStore.showError('Failed to load votes', 'Unable to load your voting history. Please try again later.')
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
    uiStore.showError('Failed to remove vote', 'Unable to remove your vote. Please try again later.')
  }
}

const handleSearch = (query: string) => {
  searchQuery.value = query
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
const filteredVotes = computed<any[]>(() => {
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