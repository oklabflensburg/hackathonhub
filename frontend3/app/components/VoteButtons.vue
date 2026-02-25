<template>
  <div class="flex items-center space-x-2">
    <!-- Upvote Button -->
    <button
      @click="debouncedHandleVote('up')"
      :disabled="isVotingInProgress"
      :class="[
        'vote-button-up',
        userVote === 'up' ? 'vote-button-up-active' : '',
        isVotingInProgress ? 'opacity-50 cursor-not-allowed' : ''
      ]"
       :title="userVote === 'up' ? $t('votes.removeUpvote') : $t('votes.upvote')"
       :aria-label="$t('votes.upvote')"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
      </svg>
      <span class="ml-1 font-medium">{{ upvotes }}</span>
    </button>

    <!-- Downvote Button -->
    <button
      @click="debouncedHandleVote('down')"
      :disabled="isVotingInProgress"
      :class="[
        'vote-button-down',
        userVote === 'down' ? 'vote-button-down-active' : '',
        isVotingInProgress ? 'opacity-50 cursor-not-allowed' : ''
      ]"
       :title="userVote === 'down' ? $t('votes.removeDownvote') : $t('votes.downvote')"
       :aria-label="$t('votes.downvote')"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
      <span class="ml-1 font-medium">{{ downvotes }}</span>
    </button>

    <!-- Score Display -->
    <div
      class="px-3 py-1 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 font-bold"
      :class="{
        'text-green-600 dark:text-green-400': totalScore > 0,
        'text-red-600 dark:text-red-400': totalScore < 0,
        'text-gray-600 dark:text-gray-400': totalScore === 0
      }"
    >
      {{ totalScore >= 0 ? '+' : '' }}{{ totalScore }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useVotingStore } from '~/stores/voting'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'

const props = defineProps<{
  projectId: number
  initialUpvotes?: number
  initialDownvotes?: number
  initialUserVote?: string | null
}>()

const votingStore = useVotingStore()
const authStore = useAuthStore()
const uiStore = useUIStore()
const { t } = useI18n()

// Simple debounce implementation
const debounceTimers = new Map<string, NodeJS.Timeout>()

function debounce<T extends (...args: any[]) => any>(
  key: string,
  fn: T,
  delay: number = 500
): (...args: Parameters<T>) => void {
  return (...args: Parameters<T>) => {
    if (debounceTimers.has(key)) {
      clearTimeout(debounceTimers.get(key)!)
    }
    
    debounceTimers.set(key, setTimeout(() => {
      fn(...args)
      debounceTimers.delete(key)
    }, delay))
  }
}

// Computed properties
const upvotes = computed(() => {
  const stats = votingStore.projectStats.get(props.projectId)
  return stats?.upvotes || props.initialUpvotes || 0
})

const downvotes = computed(() => {
  const stats = votingStore.projectStats.get(props.projectId)
  return stats?.downvotes || props.initialDownvotes || 0
})

const totalScore = computed(() => {
  const stats = votingStore.projectStats.get(props.projectId)
  return stats?.total_score || (upvotes.value - downvotes.value)
})

const userVote = computed(() => {
  const vote = votingStore.votes.get(props.projectId)
  if (!vote || vote.user_id !== authStore.user?.id) {
    // Fallback to initialUserVote
    if (props.initialUserVote) {
      if (props.initialUserVote === 'upvote' || props.initialUserVote === 'up') return 'up'
      if (props.initialUserVote === 'downvote' || props.initialUserVote === 'down') return 'down'
    }
    return null
  }
  // Map backend vote_type ('upvote'/'downvote') to frontend ('up'/'down')
  if (vote.vote_type === 'upvote') return 'up'
  if (vote.vote_type === 'downvote') return 'down'
  return vote.vote_type
})

// Use store's loading state instead of local state
const isVotingInProgress = computed(() => {
  return votingStore.isVotingInProgress(props.projectId)
})

// Methods
const handleVote = async (voteType: 'up' | 'down') => {
  if (!authStore.isAuthenticated) {
    uiStore.showError(t('votes.pleaseLogin'))
    return
  }

  // Use store loading state to prevent multiple clicks
  if (isVotingInProgress.value) {
    uiStore.showWarning(t('votes.voteInProgress'), t('votes.pleaseWait'))
    return
  }

  try {
    // If user is clicking the same vote type again, remove the vote
    if (userVote.value === voteType) {
      await votingStore.removeVote(props.projectId)
      uiStore.showSuccess(t('votes.voteRemoved'))
    } else {
      await votingStore.voteForProject(props.projectId, voteType)
      uiStore.showSuccess(voteType === 'up' ? t('votes.upvotedSuccessfully') : t('votes.downvotedSuccessfully'))
    }
  } catch (error) {
    // Handle specific error messages
    const errorMessage = error instanceof Error ? error.message : t('votes.failedToVote')
    
    // Check for specific error messages from backend
    if (errorMessage.includes('Already voted') || errorMessage.includes('vote_conflict')) {
      uiStore.showWarning(t('votes.alreadyVoted'), t('votes.voteAlreadyRecorded'))
      // Refresh vote stats to get current state
      await votingStore.getProjectVoteStats(props.projectId)
    } else if (errorMessage.includes('vote conflict')) {
      uiStore.showWarning(t('votes.concurrentVote'), t('votes.pleaseTryAgain'))
    } else {
      uiStore.showError(errorMessage)
    }
  }
}

// Debounced version of handleVote to prevent rapid clicking
const debouncedHandleVote = debounce(`vote-${props.projectId}`, handleVote, 500)

// Fetch vote stats on mount
onMounted(async () => {
  await votingStore.getProjectVoteStats(props.projectId)
})
</script>

<style scoped>
.vote-button {
  @apply flex items-center justify-center p-2 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 dark:focus:ring-offset-gray-900;
}

.vote-button-up {
  @apply vote-button text-green-600 hover:bg-green-50 dark:hover:bg-green-900/20 focus:ring-green-500;
}

.vote-button-down {
  @apply vote-button text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 focus:ring-red-500;
}

.vote-button-up-active {
  @apply bg-green-100 dark:bg-green-900/40;
}

.vote-button-down-active {
  @apply bg-red-100 dark:bg-red-900/40;
}
</style>