<template>
  <div class="card-hover group cursor-pointer" @click="$emit('open', project.id)">
    <div class="flex items-start justify-between mb-4">
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400">
          {{ project.name }}
        </h3>
        <div class="flex items-center space-x-2 mt-1">
          <div class="flex items-center">
            <div class="w-6 h-6 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mr-2">
              <span class="text-xs font-medium text-gray-600 dark:text-gray-400">{{ project.author.charAt(0) }}</span>
            </div>
            <span class="text-sm text-gray-600 dark:text-gray-400">{{ project.author }}</span>
          </div>
        </div>
      </div>
      <span class="px-2 py-1 text-xs font-medium rounded-full bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300">
        {{ project.status }}
      </span>
    </div>

    <p class="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-3">{{ project.description }}</p>

    <div class="flex flex-wrap gap-2 mb-4">
      <span v-for="tech in project.tech.slice(0, 4)" :key="tech" class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-xs rounded-md text-gray-700 dark:text-gray-300">
        {{ tech }}
      </span>
    </div>

    <div class="relative h-40 rounded-xl overflow-hidden mb-4">
      <img :src="project.image" :alt="project.name" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
      <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
      <div class="absolute bottom-4 left-4 right-4 flex items-center justify-between">
        <span class="text-white text-sm font-medium">
          {{ project.demo ? liveDemoLabel : prototypeLabel }}
        </span>
        <a
          v-if="project.github"
          :href="project.github"
          target="_blank"
          class="text-white hover:text-gray-200"
          :title="githubTitle"
          @click.stop
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
          </svg>
        </a>
      </div>
    </div>

    <div class="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-800">
      <div class="flex items-center space-x-6">
        <div class="text-center">
          <div class="text-lg font-bold text-gray-900 dark:text-white">{{ project.views }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">{{ viewsLabel }}</div>
        </div>
        <div class="text-center">
          <div class="text-lg font-bold text-gray-900 dark:text-white">{{ project.comments }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">{{ commentsLabel }}</div>
        </div>
      </div>
      <VoteButtons
        :project-id="project.id"
        :initial-upvotes="project.upvotes"
        :initial-downvotes="project.downvotes"
        :initial-user-vote="project.userVote"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import VoteButtons from '~/components/molecules/VoteButtons.vue'

defineProps<{
  project: any
  liveDemoLabel: string
  prototypeLabel: string
  githubTitle: string
  viewsLabel: string
  commentsLabel: string
}>()

defineEmits<{
  (e: 'open', id: number): void
}>()
</script>
