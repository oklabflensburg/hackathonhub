<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
    <!-- Back button -->
    <div class="mb-6">
      <NuxtLink to="/hackathons"
        class="inline-flex items-center text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        {{ $t('hackathons.details.backToHackathons') }}
      </NuxtLink>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">{{ $t('hackathons.details.loadingDetails') }}</p>
    </div>

    <!-- Hackathon details -->
    <div v-else-if="hackathon" class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg overflow-hidden">
      <HackathonHero
        :hackathon="hackathon"
        :format-date-time="formatDateTime"
        :virtual-label="$t('common.virtual')"
        :is-registered="isRegistered"
        :registration-loading="registrationLoading"
        :on-register="handleRegister"
      />

      <!-- Content -->
      <div class="p-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Main content -->
          <div class="lg:col-span-2">
            <HackathonDescription
              :title="$t('hackathons.details.description')"
              :description="hackathon.description"
            />

            <PrizeList
              :title="$t('hackathons.details.prizes')"
              :prizes="hackathon.prizes || []"
            />

            <!-- Rules -->
            <RulesSection
              :title="$t('hackathons.details.rulesAndGuidelines')"
              :rules="hackathon.rules"
            />

            <ParticipantList
              :title="$t('hackathons.details.teams') || 'Teams'"
              :items="teams.slice(0, 5)"
              :loading="loadingTeams"
              :error="teamsError"
              :requires-auth="teamsRequiresAuth"
              :loading-label="$t('teams.loading')"
              :auth-hint="$t('teams.loginRequiredToJoin')"
              :github-label="$t('auth.loginWithGitHub')"
              :google-label="$t('auth.loginWithGoogle')"
              :email-label="$t('auth.loginWithEmail')"
              :retry-label="$t('errors.tryAgain')"
              :empty-label="$t('hackathons.details.noTeamsYet') || 'No teams have joined yet.'"
              :empty-action-label="$t('teams.createTeam')"
              :empty-action-path="`/teams/create?hackathon_id=${id}`"
              :open-label="$t('common.open')"
              :closed-label="$t('common.closed')"
              :no-description-label="$t('common.noDescription')"
              :members-label="$t('teams.members')"
              created-prefix="Created"
              :view-all-label="$t('hackathons.details.viewAllTeams')"
              :view-all-path="`/teams?hackathon_id=${id}`"
              :format-date="formatDate"
              @retry="fetchTeams"
              @login-github="authStore.loginWithGitHub()"
              @login-google="authStore.loginWithGoogle()"
            />
          </div>

          <!-- Sidebar -->
          <div class="lg:col-span-1">
            <HackathonStats
              :hackathon="hackathon"
              :title="$t('hackathons.details.hackathonStats')"
              :format-date-time="formatDateTime"
              :labels="hackathonStatsLabels"
            />

            <!-- Location Map -->
            <div v-if="hackathon.latitude && hackathon.longitude"
              class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4 sm:p-5 lg:p-6 mb-6">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">{{ $t('hackathons.details.location') }}
              </h3>
              <div class="aspect-video rounded-lg overflow-hidden border border-gray-300 dark:border-gray-600">
                <iframe width="100%" height="100%" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
                  :src="`https://www.openstreetmap.org/export/embed.html?bbox=${hackathon.longitude - 0.01},${hackathon.latitude - 0.01},${hackathon.longitude + 0.01},${hackathon.latitude + 0.01}&layer=mapnik&marker=${hackathon.latitude},${hackathon.longitude}`"
                  :title="`Map of ${hackathon.name} location`" class="w-full h-full">
                </iframe>
              </div>
              <div class="mt-3 text-sm text-gray-600 dark:text-gray-400">
                <a :href="`https://www.openstreetmap.org/?mlat=${hackathon.latitude}&mlon=${hackathon.longitude}#map=16/${hackathon.latitude}/${hackathon.longitude}`"
                  target="_blank" class="text-primary-600 dark:text-primary-400 hover:underline">
                  {{ $t('hackathons.details.viewLargerMap') }}
                </a>
              </div>
            </div>

            <HackathonActions
              :id="id"
              :hackathon="hackathon"
              :is-registered="isRegistered"
              :registration-loading="registrationLoading"
              :is-hackathon-owner="isHackathonOwner"
              :can-view-team-reports="canViewTeamReports"
              :can-view-reports="canViewReports"
              :labels="{
                registered: $t('hackathons.details.registered'),
                registrationClosed: $t('hackathons.details.registrationClosed'),
                hackathonCompleted: $t('hackathons.details.hackathonCompleted'),
                registering: $t('hackathons.details.registering'),
                registerNow: $t('hackathons.details.registerNow'),
                alreadyRegistered: $t('hackathons.details.alreadyRegistered'),
                editHackathon: $t('hackathons.details.editHackathon'),
                viewProjects: $t('hackathons.details.viewProjects'),
                teamReports: 'Team Reports',
                reports: 'Reports',
                reportHackathon: 'Report Hackathon',
                shareHackathon: $t('hackathons.details.shareHackathon')
              }"
              @register="handleRegister"
              @edit="handleEdit"
              @share="handleShare"
              @report="openReportModal"
            />
          </div>
        </div>
      </div>
    </div>

    <ReportModal
      :visible="reportModalOpen"
      title="Report hackathon"
      :description="`Describe why you are reporting ${hackathon?.name || 'this hackathon'}.`"
      :loading="reportLoading"
      @close="closeReportModal"
      @submit="submitHackathonReport"
    />

    <!-- Edit Form Modal -->
    <HackathonEditForm 
      v-if="editing"
      :visible="editing"
      :form-data="editForm"
      :loading="editLoading"
      @save="handleSaveEdit"
      @cancel="handleCancelEdit"
    />

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-12">
      <div
        class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 mb-4">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">{{ $t('hackathons.details.notFoundTitle') }}</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">{{ $t('hackathons.details.notFoundDescription') }}</p>
      <NuxtLink to="/hackathons" class="btn btn-primary">
        {{ $t('hackathons.details.browseHackathons') }}
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { format } from 'date-fns'
import { computed, ref } from 'vue'
import { useRoute } from '#imports'

// Stores
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'

// Components
import HackathonEditForm from '~/components/organisms/hackathons/HackathonEditForm.vue'
import HackathonHero from '~/components/organisms/hackathons/HackathonHero.vue'
import HackathonDescription from '~/components/organisms/hackathons/HackathonDescription.vue'
import PrizeList from '~/components/organisms/hackathons/PrizeList.vue'
import RulesSection from '~/components/organisms/hackathons/RulesSection.vue'
import HackathonStats from '~/components/organisms/hackathons/HackathonStats.vue'
import HackathonActions from '~/components/organisms/hackathons/HackathonActions.vue'
import ParticipantList from '~/components/organisms/hackathons/ParticipantList.vue'
import ReportModal from '~/components/organisms/reports/ReportModal.vue'

// Composables
import { useHackathonLabels } from '~/composables/useHackathonLabels'
import { useHackathonData } from '~/composables/useHackathonData'
import { useReports } from '~/composables/useReports'

const route = useRoute()
const id = route.params.id as string
const authStore = useAuthStore()
const uiStore = useUIStore()
const { t } = useI18n()
const { labels: hackathonStatsLabels } = useHackathonLabels()
const { createReport } = useReports()
const reportModalOpen = ref(false)
const reportLoading = ref(false)

// Verwende das erweiterte Composable für alle Daten und Logik
const {
  // State
  hackathon,
  loading,
  error,
  participants,
  projects,
  teams,
  
  // Computed Properties
  isUpcoming,
  isActive,
  isCompleted,
  daysRemaining,
  daysActive,
  totalDays,
  progressPercentage,
  registrationOpen,
  prizePoolTotal,
  
  // Methods
  fetchHackathon,
  fetchParticipants,
  fetchProjects,
  fetchTeams,
  registerForHackathon,
  
  // Neue erweiterte State und Methods
  isRegistered,
  registrationLoading: registrationLoadingState,
  isHackathonOwner,
  editing,
  editLoading,
  editForm,
  teamsError,
  loadingTeams,
  teamsRequiresAuth,
  
  // Neue erweiterte Methods
  handleEdit,
  handleCancelEdit,
  handleSaveEdit,
  handleShare
} = useHackathonData({ 
  hackathonId: id, 
  autoFetch: true 
})

// Hilfsfunktionen für Datumsformatierung (könnten auch ins Composable verschoben werden)
const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  try {
    return format(new Date(dateString), 'MMM dd, yyyy')
  } catch {
    return dateString
  }
}

const formatDateTime = (dateString: string) => {
  if (!dateString) return 'N/A'
  try {
    return format(new Date(dateString), 'MMM dd, yyyy HH:mm')
  } catch {
    return dateString
  }
}

const canViewTeamReports = computed(() => {
  if (!authStore.isAuthenticated || !authStore.user) return false
  if (isHackathonOwner.value) return true
  return authStore.isSuperuser || authStore.hasPermission('team_reports:view')
})

const canViewReports = computed(() => {
  if (!authStore.isAuthenticated || !authStore.user) return false
  if (isHackathonOwner.value) return true
  return authStore.isSuperuser || authStore.hasPermission('reports:view')
})

function openReportModal() {
  if (!authStore.isAuthenticated) {
    uiStore.showWarning(t('hackathons.details.loginToRegister'), t('common.authenticationRequired'))
    return
  }
  reportModalOpen.value = true
}

function closeReportModal() {
  reportModalOpen.value = false
}

async function submitHackathonReport(reason: string) {
  if (!reason) {
    uiStore.showError('Please provide a reason for the report')
    return
  }
  try {
    reportLoading.value = true
    await createReport('hackathon', id, reason)
    uiStore.showSuccess('Hackathon report submitted')
    closeReportModal()
  } catch (err: any) {
    uiStore.showError(err?.message || 'Failed to report hackathon')
  } finally {
    reportLoading.value = false
  }
}

// Wrapper für Registrierung, um UI-Feedback zu geben
const handleRegister = async () => {
  if (!authStore.isAuthenticated) {
    uiStore.showWarning(t('hackathons.details.loginToRegister'), t('common.authenticationRequired'))
    return
  }

  if (isRegistered.value) {
    uiStore.showInfo(t('hackathons.details.alreadyRegistered'), t('common.alreadyRegistered'))
    return
  }

  const success = await registerForHackathon(authStore.user?.id?.toString() || '', undefined)
  if (success) {
    // Erfolgsmeldung wird bereits im Composable angezeigt
    // Zustand wird automatisch aktualisiert
  }
}

// Alias für bessere Lesbarkeit im Template
const registrationLoading = registrationLoadingState
</script>

<style scoped>
/* Behalte vorhandene Stile bei */
</style>