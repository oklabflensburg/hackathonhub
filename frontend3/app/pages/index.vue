<template>
  <div class="space-y-8">
    <HomeHero
      :title="t('home.hero.title')"
      :description="t('home.hero.description')"
      :explore-label="t('home.hero.exploreHackathons')"
      :create-label="t('home.hero.createProject')"
    />

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
      <HomeStatsSection
        :items="[
          { to: '/hackathons', value: stats.activeHackathons, label: t('home.stats.activeHackathons'), valueClass: 'text-primary-600 dark:text-primary-400' },
          { to: '/projects', value: stats.projectsSubmitted, label: t('home.stats.projectsSubmitted'), valueClass: 'text-green-600 dark:text-green-400' },
          { to: '/projects?sort=votes', value: stats.totalVotes, label: t('home.stats.totalVotes'), valueClass: 'text-purple-600 dark:text-purple-400' },
          { to: '/users', value: stats.activeParticipants, label: t('home.stats.activeParticipants'), valueClass: 'text-orange-600 dark:text-orange-400' }
        ]"
      />

      <!-- Featured Hackathons -->
      <section class="py-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ t('home.featuredHackathons.title') }}</h2>
          <NuxtLink to="/hackathons" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">
            {{ t('common.viewAll') }} →
          </NuxtLink>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          <HomeHackathonCard
            v-for="hackathon in featuredHackathons"
            :key="hackathon.id"
            :hackathon="hackathon"
            :view-details-label="t('common.viewDetails')"
            @open="navigateToHackathon"
          />
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
          <HomeProjectCard
            v-for="project in topProjects"
            :key="project.id"
            :project="project"
            :by-label="t('common.by')"
            @open="handleProjectCardClick"
            @open-direct="navigateToProject"
          />
        </div>
      </section>

      <HomeCtaSection
        :title="t('home.cta.title')"
        :description="t('home.cta.description')"
        :create-label="t('home.cta.createProject')"
        :signup-label="t('auth.signUpWithGitHub')"
        :is-authenticated="isAuthenticated"
        @signup="loginWithGitHub"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { generateProjectPlaceholder, generateHackathonPlaceholder } from '~/utils/placeholderImages'
import { resolveImageUrl } from '~/utils/imageUrl'
import { useRouter } from '#imports'
import HomeHero from '~/components/home/HomeHero.vue'
import HomeStatsSection from '~/components/home/HomeStatsSection.vue'
import HomeHackathonCard from '~/components/home/HomeHackathonCard.vue'
import HomeProjectCard from '~/components/home/HomeProjectCard.vue'
import HomeCtaSection from '~/components/home/HomeCtaSection.vue'

const { t } = useI18n()
const authStore = useAuthStore()
const uiStore = useUIStore()
const router = useRouter()
const config = useRuntimeConfig()
const apiUrl = config.public.apiUrl

const isAuthenticated = computed(() => authStore.isAuthenticated)

const loginWithGitHub = () => {
  authStore.loginWithGitHub()
}

// Navigation functions for clickable cards
const navigateToHackathon = (hackathonId: number) => {
  router.push(`/hackathons/${hackathonId}`)
}

const navigateToProject = (projectId: number) => {
  router.push(`/projects/${projectId}`)
}



// Handle project card click (with vote button exception)
const handleProjectCardClick = (projectId: number, event: MouseEvent) => {
  // Check if click originated from vote buttons
  const target = event.target as HTMLElement
  const isVoteButton = target.closest('.vote-button') || 
                      target.closest('[data-vote-button]') ||
                      target.closest('button')
  
  if (!isVoteButton) {
    navigateToProject(projectId)
  }
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
        let imageUrl = ''
        const imageSource = hackathon.image_url || hackathon.banner_path
        if (imageSource) {
          imageUrl = resolveImageUrl(imageSource, apiUrl)
        } else {
          // Generate placeholder image for hackathon
          imageUrl = generateHackathonPlaceholder({
            id: hackathon.id,
            name: hackathon.name
          })
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
        let imageUrl = ''
        if (project.image_path) {
          imageUrl = resolveImageUrl(project.image_path, apiUrl)
        } else {
          // Generate placeholder image for project
          imageUrl = generateProjectPlaceholder({
            id: project.id,
            title: project.title
          })
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
      // Show UI error on client side
      if (process.client) {
        uiStore.showError(t('errors.dashboardLoadFailed'), t('errors.dashboardLoadErrorDetailed'))
      }
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