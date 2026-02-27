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
        <UserProfileOverview
          :user="user"
          :user-initials="userInitials"
          :format-date="formatDate"
          :profile-info-label="$t('profile.profileInformation')"
          :member-since-label="$t('profile.memberSince')"
          :location-label="$t('profile.location')"
          :company-label="$t('profile.company')"
          :website-label="$t('profile.website')"
          :twitter-label="$t('profile.twitter')"
        />

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
      <div class="lg:col-span-1">
        <UserProfileSidebar
          :user="user"
          :is-own-profile="isOwnProfile"
          :format-date="formatDate"
          :view-own-profile-label="$t('profile.viewOwnProfile')"
          :member-details-label="$t('profile.memberDetails')"
          :member-since-label="$t('profile.memberSince')"
          :last-active-label="$t('profile.lastActive')"
          :contact-info-label="$t('profile.contactInfo')"
          :email-label="$t('profile.email')"
        />
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
import UserProfileOverview from '~/components/users/UserProfileOverview.vue'
import UserProfileSidebar from '~/components/users/UserProfileSidebar.vue'

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
