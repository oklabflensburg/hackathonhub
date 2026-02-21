<template>
  <div class="py-8">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">{{ $t('profile.publicProfile') }}</h1>
      <p class="text-gray-600 dark:text-gray-400">{{ $t('profile.viewingPublicProfile') }}</p>
    </div>

    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <div v-else-if="error" class="text-center py-8">
      <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400 mb-4">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">{{ $t('profile.errorLoadingProfile') }}</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
      <button @click="loadUserProfile" class="btn btn-outline">{{ $t('common.tryAgain') }}</button>
    </div>

    <div v-else-if="user" class="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8">
      <!-- Left Column: Profile Info -->
      <div class="lg:col-span-2">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6 mb-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">{{ $t('profile.profileInformation') }}</h2>

          <div class="space-y-6">
             <div class="flex items-start space-x-6">
              <div class="relative">
                <div v-if="user?.avatar_url"
                  class="w-24 h-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg">
                  <img :src="user.avatar_url" :alt="user.username" class="w-full h-full object-cover object-top" style="object-position: top"
                    @error="handleAvatarError" />
                </div>
                <div v-else
                  class="w-24 h-24 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center border-4 border-white dark:border-gray-800 shadow-lg">
                  <span class="text-3xl font-bold text-primary-600 dark:text-primary-300">
                    {{ userInitials }}
                  </span>
                </div>
              </div>
              <div>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ user.username }}</h3>
                <p v-if="user.name" class="text-gray-600 dark:text-gray-400">{{ user.name }}</p>
                <p v-if="user.bio" class="text-gray-600 dark:text-gray-400 mt-2">{{ user.bio }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">{{ $t('profile.memberSince') }} {{
                  formatDate(user.created_at) }}</p>
              </div>
            </div>

            <div
              class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 pt-6 border-t border-gray-200 dark:border-gray-700">
              <div v-if="user.location">
                <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ $t('profile.location') }}</h4>
                <p class="text-gray-900 dark:text-white">{{ user.location }}</p>
              </div>
              
              <div v-if="user.company">
                <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ $t('profile.company') }}</h4>
                <p class="text-gray-900 dark:text-white">{{ user.company }}</p>
              </div>
              
              <div v-if="user.blog">
                <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ $t('profile.website') }}</h4>
                <a :href="user.blog" target="_blank" rel="noopener noreferrer"
                  class="text-primary-600 dark:text-primary-400 hover:underline">
                  {{ user.blog }}
                </a>
              </div>
              
              <div v-if="user.twitter_username">
                <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ $t('profile.twitter') }}</h4>
                <a :href="`https://twitter.com/${user.twitter_username}`" target="_blank" rel="noopener noreferrer"
                  class="text-primary-600 dark:text-primary-400 hover:underline">
                  @{{ user.twitter_username }}
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4 md:gap-6">
          <!-- Hackathons Created Card -->
          <ImprovedStatsCard :label="$t('profile.hackathonsCreated')" :value="stats.hackathonsCreated || 0"
            :link="`/hackathons?user=${user.id}`" :actionText="$t('profile.viewHackathons')" :icon="HackathonIcon"
            iconBackground="gradient-blue" />

          <!-- Projects Submitted Card -->
          <ImprovedStatsCard :label="$t('profile.projectsSubmitted')" :value="stats.projectsSubmitted || 0"
            :link="`/projects?user=${user.id}`" :actionText="$t('profile.viewProjects')" :icon="ProjectIcon"
            iconBackground="gradient-green" />

          <!-- Total Votes Card -->
          <ImprovedStatsCard :label="$t('profile.totalVotes')" :value="stats.totalVotes || 0"
            :link="`/projects?voted_by=${user.id}`" :actionText="$t('profile.viewVotes')" :icon="VoteIcon"
            iconBackground="gradient-purple" />
        </div>

        <!-- Public Projects Section -->
        <div v-if="user.projects && user.projects.length > 0" class="mt-8">
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6">
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">{{ $t('profile.publicProjects') }}</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="project in user.projects.slice(0, 4)" :key="project.id"
                class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50">
                <NuxtLink :to="`/projects/${project.id}`" class="block">
                  <h4 class="font-medium text-gray-900 dark:text-white mb-2">{{ project.title }}</h4>
                  <p class="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">{{ project.description }}</p>
                  <div class="mt-3 flex items-center text-sm text-gray-500 dark:text-gray-400">
                    <span class="inline-flex items-center">
                      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                      </svg>
                      {{ project.vote_score || 0 }}
                    </span>
                    <span class="mx-2">•</span>
                    <span class="inline-flex items-center">
                      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                      </svg>
                      {{ project.comment_count || 0 }}
                    </span>
                  </div>
                </NuxtLink>
              </div>
            </div>
            <div v-if="user.projects.length > 4" class="mt-4 text-center">
              <NuxtLink :to="`/projects?user=${user.id}`" class="text-primary-600 dark:text-primary-400 hover:underline">
                {{ $t('profile.viewAllProjects') }} ({{ user.projects.length }})
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- Teams Section -->
        <div v-if="user.teams && user.teams.length > 0" class="mt-8">
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6">
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">{{ $t('profile.teams') }}</h3>
            <div class="space-y-4">
              <div v-for="teamMember in user.teams.slice(0, 5)" :key="teamMember.id"
                class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50">
                <div class="flex items-center justify-between">
                  <div>
                    <NuxtLink :to="`/teams/${teamMember.team.id}`" class="font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400">
                      {{ teamMember.team.name }}
                    </NuxtLink>
                    <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {{ $t('profile.role') }}: {{ teamMember.role === 'owner' ? $t('teams.owner') : $t('teams.member') }}
                    </p>
                  </div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">
                    {{ formatDate(teamMember.joined_at) }}
                  </div>
                </div>
              </div>
            </div>
            <div v-if="user.teams.length > 5" class="mt-4 text-center">
              <NuxtLink :to="`/teams?member=${user.id}`" class="text-primary-600 dark:text-primary-400 hover:underline">
                {{ $t('profile.viewAllTeams') }} ({{ user.teams.length }})
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Additional Info -->
      <div class="space-y-6">
        <!-- View Own Profile Button -->
        <div v-if="isOwnProfile" class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ $t('profile.yourProfile') }}</h3>
          <p class="text-gray-600 dark:text-gray-400 mb-4">{{ $t('profile.viewingOwnProfile') }}</p>
          <NuxtLink to="/profile" class="w-full btn btn-primary">
            {{ $t('profile.goToMyProfile') }}
          </NuxtLink>
        </div>

        <!-- Member Since Card -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ $t('profile.memberInfo') }}</h3>
          <div class="space-y-3">
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ $t('profile.memberSince') }}</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ formatDate(user.created_at) }}</p>
            </div>
            <div v-if="user.last_login">
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ $t('profile.lastActive') }}</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ formatDate(user.last_login) }}</p>
            </div>
          </div>
        </div>

        <!-- Contact Info (if available) -->
        <div v-if="user.email && isOwnProfile" class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ $t('profile.contactInfo') }}</h3>
          <div class="space-y-3">
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ $t('profile.email') }}</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ user.email }}</p>
            </div>
            <div v-if="user.github_id">
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ $t('profile.githubAccount') }}</p>
              <div class="flex items-center">
                <svg class="w-5 h-5 text-gray-700 dark:text-gray-300 mr-2" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                </svg>
                <span class="text-gray-900 dark:text-white">{{ user.username }}</span>
                <span class="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                  {{ $t('profile.connected') }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, h } from 'vue'
import { format } from 'date-fns'
import { useI18n } from 'vue-i18n'
import { useRoute } from '#app'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import ImprovedStatsCard from '~/components/ImprovedStatsCard.vue'

const { t } = useI18n()
const route = useRoute()
const authStore = useAuthStore()
const uiStore = useUIStore()

// Icon components for stats cards using render function
const HackathonIcon = {
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24'
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10'
      })
    ])
  }
}

const ProjectIcon = {
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24'
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
      })
    ])
  }
}

const VoteIcon = {
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24'
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5'
      })
    ])
  }
}

const loading = ref(false)
const error = ref<string | null>(null)
const user = ref<any>(null)
const stats = ref({
  hackathonsCreated: 0,
  projectsSubmitted: 0,
  totalVotes: 0
})

const userId = computed(() => Number(route.params.id))
const isOwnProfile = computed(() => {
  return authStore.user?.id === userId.value
})

const userInitials = computed(() => {
  if (!user.value) return ''
  const name = user.value.name || user.value.username || ''
  return name.charAt(0).toUpperCase()
})

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  try {
    return format(new Date(dateString), 'MMM dd, yyyy')
  } catch {
    return dateString
  }
}

const handleAvatarError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
}

const loadUserProfile = async () => {
  loading.value = true
  error.value = null
  
  try {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    
    const response = await authStore.fetchWithAuth(`/api/users/${userId.value}`)
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error(t('profile.userNotFound'))
      }
      throw new Error(t('profile.failedToLoadProfile'))
    }
    
    user.value = await response.json()
    
    // Calculate stats from user data
    stats.value = {
      hackathonsCreated: user.value.hackathon_registrations?.length || 0,
      projectsSubmitted: user.value.projects?.length || 0,
      totalVotes: user.value.votes?.length || 0
    }
    
  } catch (err) {
    error.value = err instanceof Error ? err.message : t('profile.failedToLoadProfile')
    console.error('Failed to load user profile:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUserProfile()
})
</script>