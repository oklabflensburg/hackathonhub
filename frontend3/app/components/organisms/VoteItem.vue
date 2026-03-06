<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
    <div class="md:flex">
      <!-- Project Image -->
      <div class="md:w-1/3 lg:w-1/4">
        <div class="relative h-48 md:h-full overflow-hidden">
          <img
            :src="imageUrl"
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
              {{ voteTypeLabel }}
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
                        {{ authorInitial }}
                      </span>
                    </div>
                    <span>{{ authorLabel }}</span>&nbsp;
                    <NuxtLink v-if="vote.project_author_id" :to="`/users/${vote.project_author_id}`" class="hover:underline">
                      {{ vote.project_author || unknownAuthorLabel }}
                    </NuxtLink>
                    <span v-else>{{ vote.project_author || unknownAuthorLabel }}</span>
                  </div>
                  <span>•</span>
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    <NuxtLink v-if="vote.hackathon_id" :to="`/hackathons/${vote.hackathon_id}`" class="hover:underline">
                      {{ vote.hackathon_name || hackathonLabel }}
                    </NuxtLink>
                    <span v-else>{{ vote.hackathon_name || hackathonLabel }}</span>
                  </div>
                  <span>•</span>
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{{ formattedDate }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Project Description -->
            <p class="text-gray-700 dark:text-gray-300 mb-4 line-clamp-3">
              {{ vote.project_description || noDescriptionLabel }}
            </p>
          </div>

          <!-- Technology Tags -->
          <div v-if="hasTechnologies" class="mb-4">
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tech in displayedTechnologies"
                :key="tech"
                @click="$emit('tag-click', tech)"
                class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-xs hover:underline cursor-pointer"
              >
                {{ tech }}
              </span>
              <span
                v-if="hasMoreTechnologies"
                class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-xs"
              >
                {{ moreTechnologiesLabel }}
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
                  <div class="text-xs text-gray-500 dark:text-gray-400">{{ totalVotesLabel }}</div>
                </div>
                <div class="text-center">
                  <div class="text-lg font-bold text-gray-900 dark:text-white">
                    {{ vote.project_comment_count || 0 }}
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400">{{ commentsLabel }}</div>
                </div>
                <div class="text-center">
                  <div class="text-lg font-bold text-gray-900 dark:text-white">
                    {{ vote.project_view_count || 0 }}
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400">{{ viewsLabel }}</div>
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
                  {{ viewDetailsLabel }}
                </NuxtLink>
                <button
                  @click="$emit('remove-vote', vote)"
                  class="inline-flex items-center px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors text-sm font-medium"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  {{ removeVoteLabel }}
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
import { computed } from 'vue'
import { format } from 'date-fns'
import { useI18n } from 'vue-i18n'
import { generateProjectPlaceholder } from '~/utils/placeholderImages'

const props = defineProps<{
  vote: {
    id: number
    project_id: number
    project_name: string
    project_description?: string
    project_author?: string
    project_author_id?: number
    hackathon_id?: number
    hackathon_name?: string
    project_image?: string
    project_technologies?: string[]
    project_vote_count?: number
    project_comment_count?: number
    project_view_count?: number
    vote_type: 'upvote' | 'downvote'
    created_at: string
  }
}>()

const emit = defineEmits<{
  'tag-click': [tag: string]
  'remove-vote': [vote: any]
}>()

const { t } = useI18n()

const imageUrl = computed(() => {
  if (props.vote.project_image) {
    return props.vote.project_image
  }
  return generateProjectPlaceholder({
    id: props.vote.project_id || 0,
    title: props.vote.project_name || 'Project'
  })
})

const voteTypeLabel = computed(() => {
  return props.vote.vote_type === 'upvote'
    ? t('myVotes.voteType.upvoted')
    : t('myVotes.voteType.downvoted')
})

const authorInitial = computed(() => {
  return props.vote.project_author?.charAt(0)?.toUpperCase() || 'U'
})

const authorLabel = t('myVotes.projectDetails.by')
const unknownAuthorLabel = t('myVotes.projectDetails.unknownAuthor')
const hackathonLabel = t('myVotes.projectDetails.hackathon')
const noDescriptionLabel = t('myVotes.projectDetails.noDescription')
const totalVotesLabel = t('myVotes.projectDetails.totalVotes')
const commentsLabel = t('myVotes.projectDetails.comments')
const viewsLabel = t('myVotes.projectDetails.views')
const viewDetailsLabel = t('myVotes.projectDetails.viewDetails')
const removeVoteLabel = t('myVotes.projectDetails.removeVote')

const formattedDate = computed(() => {
  if (!props.vote.created_at) return t('myVotes.notAvailable')
  try {
    return format(new Date(props.vote.created_at), 'MMM dd, yyyy HH:mm')
  } catch {
    return props.vote.created_at
  }
})

const hasTechnologies = computed(() => {
  return props.vote.project_technologies && props.vote.project_technologies.length > 0
})

const displayedTechnologies = computed(() => {
  return props.vote.project_technologies?.slice(0, 5) || []
})

const hasMoreTechnologies = computed(() => {
  return (props.vote.project_technologies?.length || 0) > 5
})

const moreTechnologiesLabel = computed(() => {
  const count = (props.vote.project_technologies?.length || 0) - 5
  return t('myVotes.projectDetails.moreTechnologies', { count })
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>