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
              :labels="{
                status: $t('hackathons.details.status'),
                participants: $t('hackathons.details.participants'),
                views: $t('hackathons.details.views'),
                projects: $t('hackathons.details.projects'),
                registrationDeadline: $t('hackathons.details.registrationDeadline')
              }"
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
              :labels="{
                registered: $t('hackathons.details.registered'),
                registrationClosed: $t('hackathons.details.registrationClosed'),
                hackathonCompleted: $t('hackathons.details.hackathonCompleted'),
                registering: $t('hackathons.details.registering'),
                registerNow: $t('hackathons.details.registerNow'),
                alreadyRegistered: $t('hackathons.details.alreadyRegistered'),
                editHackathon: $t('hackathons.details.editHackathon'),
                viewProjects: $t('hackathons.details.viewProjects'),
                shareHackathon: $t('hackathons.details.shareHackathon')
              }"
              @register="registerForHackathon"
              @edit="editHackathon"
              @share="shareHackathon"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Form Modal -->
    <HackathonEditForm 
      v-if="editing"
      :visible="editing"
      :form-data="editForm"
      :loading="editLoading"
      @save="saveEdit"
      @cancel="cancelEdit"
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
import { ref, onMounted } from 'vue'
import { format } from 'date-fns'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'
import HackathonEditForm from '~/components/HackathonEditForm.vue'
import { resolveImageUrl } from '~/utils/imageUrl'
import HackathonHero from '~/components/hackathons/HackathonHero.vue'
import HackathonDescription from '~/components/hackathons/HackathonDescription.vue'
import PrizeList from '~/components/hackathons/PrizeList.vue'
import RulesSection from '~/components/hackathons/RulesSection.vue'
import HackathonStats from '~/components/hackathons/HackathonStats.vue'
import HackathonActions from '~/components/hackathons/HackathonActions.vue'
import ParticipantList from '~/components/hackathons/ParticipantList.vue'

const route = useRoute()
const id = route.params.id as string
const authStore = useAuthStore()
const uiStore = useUIStore()
const { t } = useI18n()

const loading = ref(true)
const error = ref(false)
const hackathon = ref<any>(null)
const isRegistered = ref(false)
const registrationLoading = ref(false)
const isHackathonOwner = ref(false)
const editing = ref(false)
const editLoading = ref(false)
const teams = ref<any[]>([])
const loadingTeams = ref(false)
const teamsError = ref<string | null>(null)
const teamsRequiresAuth = ref(false)
const editForm = ref({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  location: '',
  image_url: '',
  prizes: [] as Array<{ name: string, description: string, value: string }>,
  rules: '',
  organizers: [] as Array<{ name: string, role: string }>,
  prize_pool: ''
})

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

const formatDateForInput = (dateString: string) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    // Convert to local time and format as YYYY-MM-DDTHH:mm
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${year}-${month}-${day}T${hours}:${minutes}`
  } catch {
    return dateString
  }
}

const parseDateFromInput = (dateTimeString: string) => {
  if (!dateTimeString) return ''
  try {
    // dateTimeString is in format YYYY-MM-DDTHH:mm (local time)
    // Create a Date object in local timezone
    const date = new Date(dateTimeString)
    // Convert to ISO string with timezone offset
    return date.toISOString()
  } catch {
    return dateTimeString
  }
}

const fetchHackathon = async () => {
  try {
    loading.value = true
    error.value = false

    // Fetch real hackathon data from API
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    const response = await authStore.fetchWithAuth(`/api/hackathons/${id}`)

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error(`Hackathon with ID ${id} not found`)
      }
      throw new Error(`Failed to fetch hackathon: ${response.status}`)
    }

    const apiData = await response.json()

    // Transform API data to match our frontend format
    const startDate = new Date(apiData.start_date)
    const endDate = new Date(apiData.end_date)
    const now = new Date()

    // Determine status based on dates and is_active
    let status = 'upcoming'
    if (apiData.is_active === false) {
      status = 'completed'
    } else if (startDate <= now && endDate >= now) {
      status = 'active'
    } else if (endDate < now) {
      status = 'completed'
    }

    // Parse prizes JSON if available
    let prizes = []
    try {
      if (apiData.prizes) {
        prizes = JSON.parse(apiData.prizes)
      }
    } catch (e) {
      console.error('Error parsing prizes JSON:', e)
    }


    // Parse organizers JSON if available
    let organizers = []
    try {
      if (apiData.organizers) {
        organizers = JSON.parse(apiData.organizers)
      }
    } catch (e) {
      console.error('Error parsing organizers JSON:', e)
    }


    // Transform image URL to use backend API URL if needed
    let image_url = apiData.image_url || null
    if (image_url) {
      image_url = resolveImageUrl(image_url, backendUrl)
    }

    hackathon.value = {
      id: apiData.id,
      name: apiData.name,
      description: apiData.description || t('common.noDescription'),
      start_date: apiData.start_date,
      end_date: apiData.end_date,
      location: apiData.location || t('common.virtual'),
      latitude: apiData.latitude || null,
      longitude: apiData.longitude || null,
      status,
      participant_count: apiData.participant_count || 0,
      view_count: apiData.view_count || 0,
      project_count: Math.floor((apiData.participant_count || 0) / 3), // Estimate projects
      registration_deadline: apiData.registration_deadline || apiData.start_date,
      prizes: prizes,
      rules: apiData.rules || `1. All code must be written during the hackathon period.\n2. Teams can have 1-4 members.\n3. Use of third-party APIs and libraries is allowed.\n4. Projects must be submitted by the deadline.\n5. Be respectful to all participants and organizers.`,
      organizers: organizers,
      owner_id: apiData.owner_id || null,  // Include owner_id from API
      image_url: image_url,  // Use transformed image URL
      prize_pool: apiData.prize_pool || null  // Include prize_pool from API
    }

    // Check ownership after hackathon data is loaded
    checkHackathonOwnership()
    
    // Fetch teams for this hackathon
    await fetchTeams()
  } catch (err) {
    console.error('Error fetching hackathon:', err)
    error.value = true
    uiStore.showError('Failed to load hackathon', 'Unable to load hackathon details. Please try again later.')
  } finally {
    loading.value = false
  }
}

const fetchTeams = async () => {
  try {
    loadingTeams.value = true
    teamsError.value = null
    teamsRequiresAuth.value = false

    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    const response = await authStore.fetchWithAuth(`/api/hackathons/${id}/teams`)

    if (!response.ok) {
      // Check if error is due to authentication and user is not authenticated
      if ((response.status === 401 || response.status === 403) && !authStore.isAuthenticated) {
        teamsRequiresAuth.value = true
        teamsError.value = t('common.authenticationRequired')
      } else {
        teamsError.value = `${t('errors.failedToLoad')}: ${response.status}`
      }
      throw new Error(`Failed to fetch teams: ${response.status}`)
    }

    const data = await response.json()
    teams.value = data.teams || data
  } catch (err) {
    console.error('Error fetching teams:', err)
    // If teamsError is not set yet (e.g., network error), set generic message
    if (!teamsError.value) {
      teamsError.value = t('errors.failedToLoad')
    }
  } finally {
    loadingTeams.value = false
  }
}

const checkRegistrationStatus = async () => {
  if (!authStore.isAuthenticated) {
    isRegistered.value = false
    return
  }

  try {
    // Use fetchWithAuth for automatic token refresh
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/hackathons/${id}/register`)

    if (response.ok) {
      const registrationStatus = await response.json()
      // Check if user is registered for this hackathon
      isRegistered.value = registrationStatus.is_registered || false
    } else if (response.status === 404) {
      // Hackathon not found or endpoint not available, fall back to old method
      await checkRegistrationStatusFallback()
    }
  } catch (error) {
    console.error('Error checking registration status:', error)
    // Fall back to old method
    await checkRegistrationStatusFallback()
  }
}

const checkRegistrationStatusFallback = async () => {
  try {
    // Fallback to old method using /api/me/registrations
    const response = await authStore.fetchWithAuth('/api/me/registrations')
    if (response.ok) {
      const registrations = await response.json()
      isRegistered.value = registrations.some((reg: any) =>
        reg.hackathon_id === parseInt(id)
      )
    }
  } catch (fallbackError) {
    console.error('Error in fallback registration check:', fallbackError)
    isRegistered.value = false
  }
}

const registerForHackathon = async () => {
  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    uiStore.showWarning(t('hackathons.details.loginToRegister'), t('common.authenticationRequired'))
    return
  }

  // Check if already registered
  if (isRegistered.value) {
    uiStore.showInfo(t('hackathons.details.alreadyRegistered'), t('common.alreadyRegistered'))
    return
  }

  registrationLoading.value = true

  try {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`/api/hackathons/${id}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to register for hackathon')
    }

    const result = await response.json()

    // Successfully registered
    uiStore.showSuccess(t('hackathons.details.registrationSuccess'))
    isRegistered.value = true
    // Update hackathon participant count
    if (hackathon.value) {
      hackathon.value.participant_count = (hackathon.value.participant_count || 0) + 1
    }
  } catch (error) {
    console.error('Registration error:', error)
    uiStore.showError(`${t('hackathons.details.registrationFailed')}: ${error instanceof Error ? error.message : t('common.unknownError')}`, t('common.registrationError'))
  } finally {
    registrationLoading.value = false
  }
}

const shareHackathon = () => {
  if (navigator.share) {
    navigator.share({
      title: hackathon.value?.name,
      text: `Check out ${hackathon.value?.name} on Hackathon Hub!`,
      url: window.location.href
    })
  } else {
    navigator.clipboard.writeText(window.location.href)
    uiStore.showSuccess(t('hackathons.details.linkCopied'))
  }
}

const editHackathon = async () => {
  if (!authStore.isAuthenticated) {
    uiStore.showWarning(t('hackathons.details.loginToEdit'), t('common.authenticationRequired'))
    return
  }

  try {
    // Fetch fresh hackathon data from API for editing
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // Use fetchWithAuth for automatic token refresh since editing requires authentication
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/hackathons/${id}`)

    if (!response.ok) {
      throw new Error(`Failed to fetch hackathon: ${response.status}`)
    }

    const apiData = await response.json()

    // Parse prizes JSON if available
    let prizes = []
    try {
      if (apiData.prizes) {
        prizes = JSON.parse(apiData.prizes)
      }
    } catch (e) {
      console.error('Error parsing prizes JSON:', e)
    }

    // Parse organizers JSON if available
    let organizers = []
    try {
      if (apiData.organizers) {
        organizers = JSON.parse(apiData.organizers)
      }
    } catch (e) {
      console.error('Error parsing organizers JSON:', e)
    }

    // Open edit mode
    editing.value = true

    // Transform image URL to use backend API URL if needed
    let image_url = apiData.image_url || ''
    if (image_url) {
      image_url = resolveImageUrl(image_url, backendUrl)
    }

    // Initialize edit form with fresh API data
    editForm.value = {
      name: apiData.name,
      description: apiData.description || '',
      start_date: formatDateForInput(apiData.start_date),
      end_date: formatDateForInput(apiData.end_date),
      location: apiData.location || '',
      image_url: image_url,
      prizes: prizes || [],
      rules: apiData.rules || '',
      organizers: organizers || [],
      prize_pool: apiData.prize_pool || '' // Use real API data, empty string if not available
    }
  } catch (error) {
    console.error('Error fetching hackathon for editing:', error)
    uiStore.showError(t('hackathons.details.failedToUpdate'), t('common.updateError'))
    // Fall back to using cached data if API fetch fails
    editing.value = true
    editForm.value = {
      name: hackathon.value.name,
      description: hackathon.value.description,
      start_date: formatDateForInput(hackathon.value.start_date),
      end_date: formatDateForInput(hackathon.value.end_date),
      location: hackathon.value.location,
      image_url: hackathon.value.image_url || '',
      prizes: hackathon.value.prizes || [],
      rules: hackathon.value.rules,
      organizers: hackathon.value.organizers || [],
      prize_pool: hackathon.value.prize_pool || '' // Use real API data, empty string if not available
    }
  }
}

const cancelEdit = () => {
  editing.value = false
  editForm.value = {
    name: '',
    description: '',
    start_date: '',
    end_date: '',
    location: '',
    image_url: '',
    prizes: [],
    rules: '',
    organizers: [],
    prize_pool: ''
  }
}

const saveEdit = async (formData: any) => {
  if (!authStore.isAuthenticated) {
    if (confirm(t('hackathons.details.loginToSaveChanges'))) {
      authStore.loginWithGitHub()
    }
    return
  }

  editLoading.value = true

  try {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // Prepare the update data
    const updateData: any = {
      name: formData.name,
      description: formData.description,
      start_date: parseDateFromInput(formData.start_date),
      end_date: parseDateFromInput(formData.end_date),
      location: formData.location,
      image_url: formData.image_url || null,
      rules: formData.rules,
      prize_pool: formData.prize_pool
    }

    // Convert arrays to JSON strings for API
    // Always send prizes and organizers, even if empty, to clear them
    updateData.prizes = JSON.stringify(formData.prizes || [])

    updateData.organizers = JSON.stringify(formData.organizers || [])

    // Send PUT request to update hackathon using fetchWithAuth for auto-refresh
    const response = await authStore.fetchWithAuth(`/api/hackathons/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updateData)
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || t('hackathons.details.failedToUpdate'))
    }

    const updatedHackathon = await response.json()

    // Update local hackathon data
    hackathon.value.name = updatedHackathon.name
    hackathon.value.description = updatedHackathon.description
    hackathon.value.start_date = updatedHackathon.start_date
    hackathon.value.end_date = updatedHackathon.end_date
    hackathon.value.location = updatedHackathon.location

    // Parse and update prizes and organizers
    try {
      // Handle null, undefined, or empty string
      if (updatedHackathon.prizes !== null && updatedHackathon.prizes !== undefined) {
        hackathon.value.prizes = JSON.parse(updatedHackathon.prizes)
      } else {
        hackathon.value.prizes = []
      }
    } catch (e) {
      console.error('Error parsing updated prizes:', e)
      hackathon.value.prizes = []
    }

    try {
      // Handle null, undefined, or empty string
      if (updatedHackathon.organizers !== null && updatedHackathon.organizers !== undefined) {
        hackathon.value.organizers = JSON.parse(updatedHackathon.organizers)
      } else {
        hackathon.value.organizers = []
      }
    } catch (e) {
      console.error('Error parsing updated organizers:', e)
      hackathon.value.organizers = []
    }

    hackathon.value.rules = updatedHackathon.rules
    hackathon.value.prize_pool = updatedHackathon.prize_pool

    uiStore.showSuccess(t('hackathons.details.hackathonUpdated'))
    editing.value = false

  } catch (error) {
    console.error('Error updating hackathon:', error)
    uiStore.showError(`${t('hackathons.details.failedToUpdate')}: ${error instanceof Error ? error.message : t('common.unknownError')}`, t('common.updateError'))
  } finally {
    editLoading.value = false
  }
}

// Check if current user is the hackathon owner
const checkHackathonOwnership = () => {
  if (!authStore.isAuthenticated || !hackathon.value || !authStore.user) {
    isHackathonOwner.value = false
    return
  }

  // Check if current user ID matches hackathon owner_id
  console.log('Checking ownership:', {
    hackathonOwnerId: hackathon.value.owner_id,
    userId: authStore.user.id,
    hackathonData: hackathon.value
  })

  if (hackathon.value.owner_id && authStore.user.id === hackathon.value.owner_id) {
    isHackathonOwner.value = true
    console.log('User is hackathon owner')
  } else if (!hackathon.value.owner_id) {
    // If owner_id is not available in API response (database migration not run yet)
    // Show edit button to authenticated users as temporary workaround
    console.log('owner_id not available in API response, showing edit button as fallback')
    isHackathonOwner.value = true
  } else {
    isHackathonOwner.value = false
    console.log('User is NOT hackathon owner')
  }
}

onMounted(() => {
  fetchHackathon()
  checkRegistrationStatus()
})
</script>