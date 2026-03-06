<template>
  <div class="team-card-content" :class="contentClasses">
    <!-- Team Description -->
    <div v-if="showDescription && team.description" class="team-description mb-4">
      <p class="description-text" :class="descriptionClasses">
        {{ displayDescription }}
      </p>
      
      <!-- Read More Link (if text is truncated) -->
      <button
        v-if="showReadMore && isTruncated && interactive"
        type="button"
        class="read-more-link mt-2 text-sm font-medium text-primary-600 dark:text-primary-400 hover:underline focus:outline-none"
        @click="toggleReadMore"
        :aria-expanded="!isTruncated"
        :aria-label="isTruncated ? 'Read more about this team' : 'Read less about this team'"
      >
        {{ isTruncated ? $t('teams.actions.readMore') : $t('teams.actions.readLess') }}
      </button>
    </div>
    
    <!-- Team Stats (if showStats is true) -->
    <div v-if="showStats" class="team-stats mb-4">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <!-- Member Count -->
        <div class="stat-item">
          <div class="stat-label text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">
            {{ $t('teams.stats.members') }}
          </div>
          <div class="stat-value text-lg font-semibold text-gray-900 dark:text-white">
            {{ team.stats?.memberCount || 0 }}
          </div>
        </div>
        
        <!-- Project Count -->
        <div class="stat-item">
          <div class="stat-label text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">
            {{ $t('teams.stats.projects') }}
          </div>
          <div class="stat-value text-lg font-semibold text-gray-900 dark:text-white">
            {{ team.stats?.projectCount || 0 }}
          </div>
        </div>
        
        <!-- Active Projects -->
        <div class="stat-item">
          <div class="stat-label text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">
            {{ $t('teams.stats.active') }}
          </div>
          <div class="stat-value text-lg font-semibold text-gray-900 dark:text-white">
            {{ team.stats?.activeProjectCount || 0 }}
          </div>
        </div>
        
        <!-- Total Votes -->
        <div class="stat-item">
          <div class="stat-label text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">
            {{ $t('teams.stats.votes') }}
          </div>
          <div class="stat-value text-lg font-semibold text-gray-900 dark:text-white">
            {{ team.stats?.totalVotes || 0 }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- Team Tags -->
    <div v-if="team.tags && team.tags.length > 0" class="team-tags mb-4">
      <div class="flex flex-wrap gap-2">
        <span
          v-for="tag in displayTags"
          :key="tag"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300"
        >
          {{ tag }}
        </span>
        <span
          v-if="team.tags.length > maxVisibleTags"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-400"
        >
          +{{ team.tags.length - maxVisibleTags }}
        </span>
      </div>
    </div>
    
    <!-- Hackathon Info (if team belongs to a hackathon) -->
    <div v-if="team.hackathonId" class="hackathon-info mb-4">
      <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <span>{{ $t('teams.hackathonTeam') }} (ID: {{ team.hackathonId }})</span>
      </div>
    </div>
    
    <!-- Created Date -->
    <div v-if="team.createdAt" class="created-date text-sm text-gray-500 dark:text-gray-400">
      {{ $t('teams.created') }}: {{ formatDate(team.createdAt) }}
    </div>
    
    <!-- Slot for additional content -->
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { TeamCardContentProps } from '~/types/team-types'

const props = withDefaults(defineProps<TeamCardContentProps & {
  interactive?: boolean
  showReadMore?: boolean
  maxVisibleTags?: number
}>(), {
  showDescription: true,
  showStats: true,
  maxDescriptionLength: 150,
  interactive: true,
  showReadMore: true,
  maxVisibleTags: 3
})

const isExpanded = ref(false)

// Computed properties
const displayDescription = computed(() => {
  if (!props.team.description) return ''
  
  if (isExpanded.value || !props.interactive) {
    return props.team.description
  }
  
  if (props.team.description.length <= props.maxDescriptionLength) {
    return props.team.description
  }
  
  return props.team.description.substring(0, props.maxDescriptionLength) + '...'
})

const isTruncated = computed(() => {
  if (!props.team.description || !props.interactive) return false
  return props.team.description.length > props.maxDescriptionLength && !isExpanded.value
})

const displayTags = computed(() => {
  if (!props.team.tags) return []
  return props.team.tags.slice(0, props.maxVisibleTags)
})

const contentClasses = computed(() => [
  'p-4',
  props.interactive ? 'cursor-default' : ''
])

const descriptionClasses = computed(() => [
  'text-gray-700 dark:text-gray-300 leading-relaxed',
  isTruncated.value ? 'line-clamp-3' : ''
])

// Methods
const toggleReadMore = () => {
  isExpanded.value = !isExpanded.value
}

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
.team-card-content {
  border-top: 1px solid #e5e7eb;
}

.dark .team-card-content {
  border-top-color: #374151;
}

.description-text {
  transition: all 0.3s ease;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  background-color: #f9fafb;
  border-radius: 0.5rem;
}

.dark .stat-item {
  background-color: #1f2937;
}

.stat-label {
  margin-bottom: 0.25rem;
}

.stat-value {
  line-height: 1;
}

.read-more-link {
  transition: color 0.2s ease;
}

.read-more-link:hover {
  text-decoration: underline;
}

.read-more-link:focus {
  outline: 2px solid transparent;
  outline-offset: 2px;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
}
</style>