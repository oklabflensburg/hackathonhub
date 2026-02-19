<template>
  <div class="py-8">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">{{ $t('profile.title') }}</h1>
      <p class="text-gray-600 dark:text-gray-400">{{ $t('profile.subtitle') }}</p>
    </div>

     <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8">
      <!-- Left Column: Profile Info -->
      <div class="lg:col-span-2">
         <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6 mb-6">
           <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">{{ $t('profile.profileInformation') }}</h2>
          
          <!-- Loading State -->
          <div v-if="loading" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>

          <!-- Profile Display -->
          <div v-else-if="user" class="space-y-6">
            <div class="flex items-center space-x-6">
              <div class="relative">
                <div v-if="user?.avatar_url" class="w-24 h-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg">
                  <img
                    :src="user.avatar_url"
                    :alt="user.username"
                    class="w-full h-full object-cover"
                    @error="handleAvatarError"
                  />
                </div>
                <div v-else class="w-24 h-24 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center border-4 border-white dark:border-gray-800 shadow-lg">
                  <span class="text-3xl font-bold text-primary-600 dark:text-primary-300">
                    {{ userInitials }}
                  </span>
                </div>
              </div>
              <div>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ user.username }}</h3>
                <p class="text-gray-600 dark:text-gray-400">{{ user.email }}</p>
                 <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">{{ $t('profile.memberSince') }} {{ formatDate(user.created_at) }}</p>
              </div>
            </div>

             <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 pt-6 border-t border-gray-200 dark:border-gray-700">
               <div>
                 <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ $t('profile.githubAccount') }}</h4>
                <div class="flex items-center justify-start space-x-3">
                   <svg class="w-5 h-5 text-gray-700 dark:text-gray-300 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                  </svg>
                   <span class="text-gray-900 dark:text-white flex-shrink-0">{{ user?.github_id ? user.username : $t('profile.notConnected') }}</span>
                  <span v-if="user?.github_id" class="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                     {{ $t('profile.connected') }}
                  </span>
                </div>
              </div>

              <div>
                 <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ $t('profile.accountType') }}</h4>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-300">
                   {{ (user as any).is_admin ? $t('profile.administrator') : $t('profile.standardUser') }}
                </span>
              </div>
            </div>
          </div>

          <!-- No User State -->
          <div v-else class="text-center py-8">
            <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
             <p class="text-gray-600 dark:text-gray-400 mb-4">{{ $t('profile.pleaseLogin') }}</p>
            <NuxtLink to="/" class="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
               {{ $t('profile.goToLogin') }}
            </NuxtLink>
          </div>
        </div>

        <!-- Stats Cards -->
         <div class="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4 md:gap-6">
          <!-- Hackathons Created Card -->
          <ImprovedStatsCard
            :label="$t('profile.hackathonsCreated')"
            :value="stats.hackathonsCreated || 0"
            link="/hackathons?filter=my"
            :actionText="$t('profile.viewYourHackathons')"
            :icon="HackathonIcon"
            iconBackground="gradient-blue"
          />

          <!-- Projects Submitted Card -->
          <ImprovedStatsCard
            :label="$t('profile.projectsSubmitted')"
            :value="stats.projectsSubmitted || 0"
            link="/my-projects"
            :actionText="$t('profile.viewYourProjects')"
            :icon="ProjectIcon"
            iconBackground="gradient-green"
          />

          <!-- Total Votes Card -->
          <ImprovedStatsCard
            :label="$t('profile.totalVotes')"
            :value="stats.totalVotes || 0"
            link="/my-votes"
            :actionText="$t('profile.viewYourVotes')"
            :icon="VoteIcon"
            iconBackground="gradient-purple"
          />
        </div>
      </div>

      <!-- Right Column: Actions -->
      <div class="space-y-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-5 lg:p-6">
           <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ $t('profile.quickActions') }}</h3>
          <div class="space-y-3">
            <NuxtLink 
              to="/create" 
              class="flex items-center justify-between p-3 rounded-lg bg-primary-50 dark:bg-primary-900/30 hover:bg-primary-100 dark:hover:bg-primary-900/50 transition-colors"
            >
              <div class="flex items-center space-x-3">
                <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                 <span class="font-medium text-primary-700 dark:text-primary-300">{{ $t('profile.createHackathon') }}</span>
              </div>
              <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </NuxtLink>

            <NuxtLink 
              to="/my-projects" 
              class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
            >
              <div class="flex items-center space-x-3">
                <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                 <span class="font-medium text-gray-700 dark:text-gray-300">{{ $t('profile.viewMyProjects') }}</span>
              </div>
              <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </NuxtLink>

            <NuxtLink 
              to="/my-votes" 
              class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
            >
              <div class="flex items-center space-x-3">
                <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                </svg>
                 <span class="font-medium text-gray-700 dark:text-gray-300">{{ $t('profile.viewMyVotes') }}</span>
              </div>
              <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </NuxtLink>
          </div>
        </div>

         <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6">
           <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ $t('profile.accountSettings') }}</h3>
          <div class="space-y-4">
            <button 
              @click="handleLogout"
              class="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
               <span class="font-medium">{{ $t('profile.logOut') }}</span>
            </button>
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
import { useAuthStore } from '~/stores/auth'
import ImprovedStatsCard from '~/components/ImprovedStatsCard.vue'

const { t } = useI18n()

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

const authStore = useAuthStore()
const loading = ref(false)
const user = computed(() => authStore.user)
const stats = ref({
  hackathonsCreated: 0,
  projectsSubmitted: 0,
  totalVotes: 0
})

const userInitials = computed(() => {
  return authStore.userInitials
})

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  try {
    return format(new Date(dateString), 'MMM dd, yyyy')
  } catch {
    return dateString
  }
}

const fetchUserStats = async () => {
  try {
    if (!authStore.isAuthenticated) return

    // Try to fetch user stats from API (endpoint might not exist)
    try {
      const response = await authStore.fetchWithAuth('/api/users/me/stats')

      if (response.ok) {
        stats.value = await response.json()
      } else if (response.status === 404) {
        // Stats endpoint doesn't exist, use placeholder values
        console.warn('Stats endpoint not available, using placeholder values')
        stats.value = {
          hackathonsCreated: 0,
          projectsSubmitted: 0,
          totalVotes: 0
        }
      }
    } catch (error) {
      // Stats endpoint doesn't exist or failed, use placeholder values
      console.warn('Stats endpoint not available, using placeholder values')
      stats.value = {
        hackathonsCreated: 0,
        projectsSubmitted: 0,
        totalVotes: 0
      }
    }
  } catch (error) {
    console.error('Error fetching user stats:', error)
  }
}

const handleAvatarError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  // The parent div will show the fallback initials automatically
  // because we're using v-if/v-else
}

const handleLogout = () => {
  authStore.logout()
  navigateTo('/')
}

onMounted(() => {
  fetchUserStats()
})
</script>