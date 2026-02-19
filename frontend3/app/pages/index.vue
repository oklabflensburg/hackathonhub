<template>
  <div class="space-y-8">
    <!-- Hero Section -->
    <section
      class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary-500 to-purple-600 p-8 md:p-12 text-white">
      <div class="relative z-10 max-w-3xl">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">
          {{ t('home.hero.title') }}
        </h1>
        <p class="text-xl mb-8 opacity-90">
          {{ t('home.hero.description') }}
        </p>
        <div class="flex flex-wrap gap-4">
          <NuxtLink to="/hackathons" class="btn bg-white text-primary-600 hover:bg-gray-100">
            {{ t('home.hero.exploreHackathons') }}
          </NuxtLink>
          <NuxtLink to="/create" class="btn bg-transparent border-2 border-white hover:bg-white/10">
            {{ t('home.hero.createProject') }}
          </NuxtLink>
        </div>
      </div>
      <div
        class="absolute top-0 right-0 w-32 h-32 sm:w-48 sm:h-48 md:w-64 md:h-64 bg-white/10 rounded-full -translate-y-16 sm:-translate-y-24 md:-translate-y-32 translate-x-16 sm:translate-x-24 md:translate-x-32">
      </div>
      <div
        class="absolute bottom-0 left-0 w-48 h-48 sm:w-64 sm:h-64 md:w-96 md:h-96 bg-white/5 rounded-full translate-y-24 sm:translate-y-32 md:translate-y-48 -translate-x-24 sm:-translate-x-32 md:-translate-x-48">
      </div>
    </section>

    <!-- Loading and Error States -->
    <div v-if="loading" class="space-y-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div v-for="i in 4" :key="i" class="card text-center">
          <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded animate-pulse mb-2 mx-auto w-16"></div>
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-24 mx-auto"></div>
        </div>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <div v-for="i in 3" :key="i" class="card-hover">
          <div class="h-6 bg-gray-200 dark:bg-gray-700 rounded animate-pulse mb-2 w-3/4"></div>
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse mb-4 w-1/2"></div>
          <div class="h-16 bg-gray-200 dark:bg-gray-700 rounded animate-pulse mb-4"></div>
          <div class="flex justify-between">
            <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-20"></div>
            <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-24"></div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="error" class="card bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-6">
      <div class="flex items-center">
        <svg class="w-6 h-6 text-red-600 dark:text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h3 class="font-semibold text-red-800 dark:text-red-300">{{ t('errors.dashboardLoadFailed') }}</h3>
          <p class="text-red-700 dark:text-red-400 text-sm mt-1">{{ error?.message || t('errors.unknownError') }}</p>
          <button @click="() => fetchDashboardData()"
            class="mt-3 text-sm text-red-600 dark:text-red-400 hover:underline">
            {{ t('common.tryAgain') }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="!loading && !error">
      <!-- Stats Section -->
      <section class="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
        <div class="card text-center">
          <div class="text-3xl font-bold text-primary-600 dark:text-primary-400 mb-2">{{ stats.activeHackathons }}</div>
          <div class="text-gray-600 dark:text-gray-400">{{ t('home.stats.activeHackathons') }}</div>
        </div>
        <div class="card text-center">
          <div class="text-3xl font-bold text-green-600 dark:text-green-400 mb-2">{{ stats.projectsSubmitted }}</div>
          <div class="text-gray-600 dark:text-gray-400">{{ t('home.stats.projectsSubmitted') }}</div>
        </div>
        <div class="card text-center">
          <div class="text-3xl font-bold text-purple-600 dark:text-purple-400 mb-2">{{ stats.totalVotes }}</div>
          <div class="text-gray-600 dark:text-gray-400">{{ t('home.stats.totalVotes') }}</div>
        </div>
        <div class="card text-center">
          <div class="text-3xl font-bold text-orange-600 dark:text-orange-400 mb-2">{{ stats.activeParticipants }}</div>
          <div class="text-gray-600 dark:text-gray-400">{{ t('home.stats.activeParticipants') }}</div>
        </div>
      </section>

      <!-- Featured Hackathons -->
      <section class="py-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ t('home.featuredHackathons.title') }}</h2>
          <NuxtLink to="/hackathons" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">
            {{ t('common.viewAll') }} →
          </NuxtLink>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          <div v-for="hackathon in featuredHackathons" :key="hackathon.id" class="card-hover">
            <!-- Hackathon Image -->
            <div class="w-full overflow-hidden rounded-t-lg mb-4 aspect-ratio-16-9">
              <img :src="hackathon.imageUrl" :alt="hackathon.name" class="img-cover" />
            </div>
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                  {{ hackathon.name }}
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">{{ hackathon.organization }}</p>
              </div>
              <span class="badge badge-primary">{{ hackathon.status }}</span>
            </div>
            <p class="text-gray-600 dark:text-gray-400 mb-4 text-sm">
              {{ hackathon.description }}
            </p>
            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center space-x-4">
                <span class="flex items-center text-gray-500 dark:text-gray-400">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ hackathon.duration }}
                </span>
                <span class="flex items-center text-gray-500 dark:text-gray-400">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  {{ hackathon.participants }}
                </span>
              </div>
              <NuxtLink :to="`/hackathons/${hackathon.id}`"
                class="text-primary-600 dark:text-primary-400 hover:underline font-medium">
                {{ t('common.viewDetails') }}
              </NuxtLink>
            </div>
          </div>
        </div>
      </section>

      <!-- Top Projects -->
      <section class="py-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ t('home.topProjects.title') }}</h2>
          <NuxtLink to="/projects" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">
            {{ t('common.viewAll') }} →
          </NuxtLink>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          <div v-for="project in topProjects" :key="project.id" class="card-hover">
            <NuxtLink :to="'/projects/' + project.id" class="block">
              <!-- Project Image -->
              <div class="relative w-full mb-4 overflow-hidden rounded-lg aspect-ratio-4-3">
                <img :src="project.imageUrl" :alt="project.name"
                  class="img-cover transition-transform duration-300 hover:scale-105" />
                <div class="absolute top-2 right-2">
                  <span class="badge badge-success">{{ project.hackathon }}</span>
                </div>
              </div>

              <div class="flex items-start justify-between mb-3">
                <div>
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                    {{ project.name }}
                  </h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('common.by') }} {{ project.author }}</p>
                </div>
              </div>
              <p class="text-gray-600 dark:text-gray-400 mb-4 text-sm line-clamp-2">
                {{ project.description }}
              </p>
            </NuxtLink>

            <div class="flex items-center justify-between">
              <VoteButtons :project-id="project.id" :initial-upvotes="project.upvotes"
                :initial-downvotes="project.downvotes" :initial-user-vote="project.userVote" />
              <div class="flex items-center space-x-2">
                <span class="text-sm text-gray-500 dark:text-gray-400">
                  {{ project.tech.join(', ') }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="text-center py-12">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          {{ t('home.cta.title') }}
        </h2>
        <p class="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
          {{ t('home.cta.description') }}
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <NuxtLink to="/create" class="btn btn-primary px-8 py-3 text-lg">
            {{ t('home.cta.createProject') }}
          </NuxtLink>
          <button v-if="!isAuthenticated" @click="loginWithGitHub" class="btn btn-outline px-8 py-3 text-lg">
            {{ t('auth.signUpWithGitHub') }}
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const authStore = useAuthStore()
const config = useRuntimeConfig()
const apiUrl = config.public.apiUrl

const isAuthenticated = computed(() => authStore.isAuthenticated)

const loginWithGitHub = () => {
  authStore.loginWithGitHub()
}

// Use Nuxt's useAsyncData for SSR-compatible data fetching
const { data: dashboardData, pending: loading, error, refresh: fetchDashboardData } = useAsyncData(
  'dashboard',
  async () => {
    try {
      // Fetch hackathons using fetchWithAuth for automatic token refresh
      const hackathonsResponse = await authStore.fetchWithAuth(`${apiUrl}/api/hackathons`)
      if (!hackathonsResponse.ok) {
        throw new Error(`${t('errors.fetchHackathonsFailed')}: ${hackathonsResponse.status}`)
      }
      const hackathonsData = await hackathonsResponse.json()

      // Fetch projects using fetchWithAuth for automatic token refresh
      const projectsResponse = await authStore.fetchWithAuth(`${apiUrl}/api/projects`)
      if (!projectsResponse.ok) {
        throw new Error(`${t('errors.fetchProjectsFailed')}: ${projectsResponse.status}`)
      }
      const projectsData = await projectsResponse.json()

      // Transform hackathons data
      const featuredHackathons = hackathonsData.slice(0, 3).map((hackathon: any) => {
        // Handle hackathon image URL
        let imageUrl = 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80'
        const imageSource = hackathon.image_url || hackathon.banner_path
        if (imageSource) {
          if (imageSource.startsWith('http')) {
            // Already a full URL
            imageUrl = imageSource
          } else if (imageSource.startsWith('/')) {
            // Relative path, prepend backend URL
            imageUrl = `${apiUrl}${imageSource}`
          } else {
            // Assume it's a relative path without leading slash
            imageUrl = `${apiUrl}/${imageSource}`
          }
        }

        return {
          id: hackathon.id,
          name: hackathon.name,
          organization: hackathon.organization || t('common.unknown'),
          status: hackathon.is_active ? t('common.active') : t('common.upcoming'),
          description: hackathon.description || t('common.noDescription'),
          duration: `${hackathon.duration_hours || 48} ${t('common.hours')}`,
          participants: `${hackathon.participant_count || 0}+`,
          prize: hackathon.prize ? `$${hackathon.prize.toLocaleString()}` : t('common.noPrize'),
          imageUrl
        }
      })

      // Transform projects data and sort by vote score
      const transformedProjects = projectsData.map((project: any) => {
        // Handle project image URL
        let imageUrl = 'https://images.unsplash.com/photo-1551650975-87deedd944c3?auto=format&fit=crop&w=800&q=80'
        if (project.image_path) {
          if (project.image_path.startsWith('http')) {
            // Already a full URL
            imageUrl = project.image_path
          } else if (project.image_path.startsWith('/')) {
            // Relative path, prepend backend URL
            imageUrl = `${apiUrl}${project.image_path}`
          } else {
            // Assume it's a relative path without leading slash
            imageUrl = `${apiUrl}/${project.image_path}`
          }
        }

        return {
          id: project.id,
          name: project.title,
          author: project.owner?.name || t('common.unknown'),
          hackathon: project.hackathon?.name || t('common.unknownHackathon'),
          description: project.description || t('common.noDescription'),
          upvotes: project.upvote_count || 0,
          downvotes: project.downvote_count || 0,
          userVote: null, // Would need to check user's vote from separate endpoint
          tech: project.technologies ? project.technologies.split(',').map((t: string) => t.trim()) : [],
          imageUrl
        }
      })

      // Sort by vote score (upvotes - downvotes) and take top 3
      const topProjects = transformedProjects
        .sort((a: any, b: any) => (b.upvotes - b.downvotes) - (a.upvotes - a.downvotes))
        .slice(0, 3)

      // Calculate stats
      const activeHackathonsCount = hackathonsData.filter((h: any) => h.is_active).length
      const totalProjects = projectsData.length
      const totalVotes = projectsData.reduce((sum: number, p: any) => sum + (p.upvote_count || 0) + (p.downvote_count || 0), 0)
      const totalParticipants = hackathonsData.reduce((sum: number, h: any) => sum + (h.participant_count || 0), 0)

      const stats = {
        activeHackathons: activeHackathonsCount,
        projectsSubmitted: totalProjects,
        totalVotes,
        activeParticipants: totalParticipants
      }

      return {
        featuredHackathons,
        topProjects,
        stats
      }
    } catch (err: any) {
      console.error('Error fetching dashboard data:', err)
      throw err
    }
  },
  {
    server: true, // Fetch on server side for SSR
    lazy: false, // Fetch immediately
    default: () => ({
      featuredHackathons: [],
      topProjects: [],
      stats: {
        activeHackathons: 0,
        projectsSubmitted: 0,
        totalVotes: 0,
        activeParticipants: 0
      }
    })
  }
)

// Destructure the data for template use
const featuredHackathons = computed(() => dashboardData.value?.featuredHackathons || [])
const topProjects = computed(() => dashboardData.value?.topProjects || [])
const stats = computed(() => dashboardData.value?.stats || {
  activeHackathons: 0,
  projectsSubmitted: 0,
  totalVotes: 0,
  activeParticipants: 0
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