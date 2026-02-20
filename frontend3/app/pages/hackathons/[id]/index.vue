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
      <!-- Header with image or gradient -->
      <div class="h-48 relative">
        <!-- Background image if available -->
        <div v-if="hackathon.image_url" class="absolute inset-0 bg-cover bg-center"
          :style="{ backgroundImage: `url(${hackathon.image_url})` }">
          <div class="absolute inset-0 bg-black/40"></div>
        </div>
        <!-- Fallback gradient if no image -->
        <div v-else class="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-600">
          <div class="absolute inset-0 bg-black/20"></div>
        </div>

        <div class="relative h-full flex items-center justify-center p-8">
          <div class="text-center">
            <h1 class="text-4xl font-bold text-white mb-2">{{ hackathon.name }}</h1>
            <div class="flex items-center justify-center space-x-4 text-white/90">
              <span class="flex items-center">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {{ formatDateTime(hackathon.start_date) }} - {{ formatDateTime(hackathon.end_date) }}
              </span>
              <span class="flex items-center">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {{ hackathon.location || 'Virtual' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Content -->
      <div class="p-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Main content -->
          <div class="lg:col-span-2">
            <!-- Description -->
            <div class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ $t('hackathons.details.description')
                }}</h2>
              <div class="prose dark:prose-invert max-w-none">
                <p class="text-gray-700 dark:text-gray-300">{{ hackathon.description }}</p>
              </div>
            </div>

            <!-- Prizes -->
            <div class="mb-8" v-if="hackathon.prizes && hackathon.prizes.length > 0">
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ $t('hackathons.details.prizes') }}
              </h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-for="(prize, idx) in hackathon.prizes" :key="idx"
                  class="bg-gradient-to-br from-primary-50 to-purple-50 dark:from-gray-700 dark:to-gray-800 p-4 sm:p-5 lg:p-6 rounded-xl border border-primary-100 dark:border-gray-700">
                  <div class="flex items-center mb-3">
                    <div
                      class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center mr-3">
                      <span class="text-primary-600 dark:text-primary-300 font-bold">{{ +idx + 1 }}</span>
                    </div>
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white">{{ prize.name }}</h3>
                  </div>
                  <p class="text-gray-700 dark:text-gray-300">{{ prize.description }}</p>
                  <div class="mt-3 text-primary-600 dark:text-primary-400 font-bold">
                    {{ prize.value }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Rules -->
            <div v-if="hackathon.rules">
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{
                $t('hackathons.details.rulesAndGuidelines') }}</h2>
              <div class="bg-gray-50 dark:bg-gray-700/50 p-4 sm:p-5 lg:p-6 rounded-xl">
                <div class="prose dark:prose-invert max-w-none">
                  <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line">{{ hackathon.rules }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="lg:col-span-1">
            <!-- Stats -->
            <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4 sm:p-5 lg:p-6 mb-6">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">{{
                $t('hackathons.details.hackathonStats') }}</h3>
              <div class="space-y-4">
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 dark:text-gray-400">{{ $t('hackathons.details.status') }}</span>
                  <span :class="{
                    'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300': hackathon.status === 'active',
                    'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300': hackathon.status === 'upcoming',
                    'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300': hackathon.status === 'completed'
                  }" class="px-3 py-1 rounded-full text-sm font-medium capitalize">
                    {{ hackathon.status }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 dark:text-gray-400">{{ $t('hackathons.details.participants') }}</span>
                  <span class="font-bold text-gray-900 dark:text-white">{{ hackathon.participant_count || 0 }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 dark:text-gray-400">{{ $t('hackathons.details.projects') }}</span>
                  <span class="font-bold text-gray-900 dark:text-white">{{ hackathon.project_count || 0 }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 dark:text-gray-400">{{ $t('hackathons.details.registrationDeadline')
                    }}</span>
                  <span class="font-bold text-gray-900 dark:text-white">{{
                    formatDateTime(hackathon.registration_deadline) }}</span>
                </div>
              </div>
            </div>

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

            <!-- Actions -->
            <div class="space-y-4">
              <div>
                <!-- Registration section - always shown -->
                <div v-if="hackathon.status === 'completed'">
                  <!-- For completed hackathons, show registered status or closed message -->
                  <div v-if="isRegistered"
                    class="w-full p-4 bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-800 rounded-xl text-center">
                    <div class="flex items-center justify-center text-green-600 dark:text-green-400 mb-2">
                      <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span class="font-bold">{{ $t('hackathons.details.registered') }}</span>
                    </div>
                    <p class="text-sm text-green-700 dark:text-green-300">
                      {{ $t('hackathons.details.hackathonCompleted') }}
                    </p>
                  </div>
                  <div v-else
                    class="w-full p-4 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl text-center">
                    <div class="flex items-center justify-center text-gray-600 dark:text-gray-400 mb-2">
                      <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span class="font-bold">{{ $t('hackathons.details.registrationClosed') }}</span>
                    </div>
                    <p class="text-sm text-gray-700 dark:text-gray-300">
                      {{ $t('hackathons.details.hackathonCompleted') }}
                    </p>
                  </div>
                </div>
                <div v-else>
                  <!-- For active/upcoming hackathons -->
                  <button v-if="!isRegistered" class="w-full btn btn-primary" @click="registerForHackathon"
                    :disabled="registrationLoading">
                    <svg v-if="registrationLoading" class="w-5 h-5 mr-2 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                      <path class="opacity-75" fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                    {{ registrationLoading ? $t('hackathons.details.registering') : $t('hackathons.details.registerNow')
                    }}
                  </button>
                  <div v-else
                    class="w-full p-4 bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-800 rounded-xl text-center">
                    <div class="flex items-center justify-center text-green-600 dark:text-green-400 mb-2">
                      <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span class="font-bold">{{ $t('hackathons.details.registered') }}</span>
                    </div>
                    <p class="text-sm text-green-700 dark:text-green-300">
                      {{ $t('hackathons.details.alreadyRegistered') }}
                    </p>
                  </div>
                </div>
              </div>

              <!-- Edit button for hackathon owner -->
              <button v-if="isHackathonOwner" class="w-full btn btn-outline flex items-center justify-center"
                @click="editHackathon">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                {{ $t('hackathons.details.editHackathon') }}
              </button>

              <NuxtLink :to="`/hackathons/${id}/projects`"
                class="w-full btn btn-outline flex items-center justify-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                {{ $t('hackathons.details.viewProjects') }}
              </NuxtLink>

              <button class="w-full btn btn-outline flex items-center justify-center" @click="shareHackathon">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                </svg>
                {{ $t('hackathons.details.share') }}
              </button>
            </div>

            <!-- Organizers -->
            <div class="mt-6" v-if="hackathon.organizers && hackathon.organizers.length > 0">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">{{ $t('hackathons.details.organizers') }}
              </h3>
              <div class="space-y-3">
                <div v-for="organizer in hackathon.organizers" :key="organizer.id"
                  class="flex items-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                  <div
                    class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center mr-3">
                    <span class="text-primary-600 dark:text-primary-300 font-bold">
                      {{ organizer.name.charAt(0) }}
                    </span>
                  </div>
                  <div>
                    <p class="font-medium text-gray-900 dark:text-white">{{ organizer.name }}</p>
                    <p class="text-sm text-gray-600 dark:text-gray-400">{{ organizer.role }}</p>
                  </div>
                </div>
              </div>
            </div>
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

    const response = await fetch(`${backendUrl}/api/hackathons/${id}`)

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

    // Only use defaults if prizes is null/undefined/empty string (not if it's empty array)
    if (!apiData.prizes && prizes.length === 0) {
      prizes = [
        { name: 'First Place', description: 'Grand prize for the winning team', value: '$5,000' },
        { name: 'Second Place', description: 'Runner-up prize', value: '$2,500' },
        { name: 'Best Design', description: 'Award for best UI/UX design', value: '$1,000' }
      ]
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

    // Only use defaults if organizers is null/undefined/empty string (not if it's empty array)
    if (!apiData.organizers && organizers.length === 0) {
      organizers = [
        { id: 1, name: 'Hackathon Organizer', role: 'Lead Organizer' },
        { id: 2, name: 'Technical Committee', role: 'Technical Lead' }
      ]
    }

    hackathon.value = {
      id: apiData.id,
      name: apiData.name,
      description: apiData.description || 'No description available.',
      start_date: apiData.start_date,
      end_date: apiData.end_date,
      location: apiData.location || 'Virtual',
      latitude: apiData.latitude || null,
      longitude: apiData.longitude || null,
      status,
      participant_count: apiData.participant_count || 0,
      project_count: Math.floor((apiData.participant_count || 0) / 3), // Estimate projects
      registration_deadline: apiData.registration_deadline || apiData.start_date,
      prizes: prizes,
      rules: apiData.rules || `1. All code must be written during the hackathon period.\n2. Teams can have 1-4 members.\n3. Use of third-party APIs and libraries is allowed.\n4. Projects must be submitted by the deadline.\n5. Be respectful to all participants and organizers.`,
      organizers: organizers,
      owner_id: apiData.owner_id || null,  // Include owner_id from API
      image_url: apiData.image_url || null,  // Include image_url from API
      prize_pool: apiData.prize_pool || null  // Include prize_pool from API
    }

    // Check ownership after hackathon data is loaded
    checkHackathonOwnership()
  } catch (err) {
    console.error('Error fetching hackathon:', err)
    error.value = true
    uiStore.showError('Failed to load hackathon', 'Unable to load hackathon details. Please try again later.')
  } finally {
    loading.value = false
  }
}

const checkRegistrationStatus = async () => {
  if (!authStore.isAuthenticated) {
    isRegistered.value = false
    return
  }

  try {
    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth('/api/me/registrations')

    if (response.ok) {
      const registrations = await response.json()
      // Check if user is registered for this hackathon
      isRegistered.value = registrations.some((reg: any) =>
        reg.hackathon_id === parseInt(id)
      )
    }
  } catch (error) {
    console.error('Error checking registration status:', error)
    // This is a background operation, so we don't show a prominent error
    // uiStore.showError('Registration status check failed', 'Unable to check your registration status. Please refresh the page.')
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

    if (result.is_new) {
      uiStore.showSuccess(t('hackathons.details.registrationSuccess'))
      isRegistered.value = true
      // Update hackathon participant count
      if (hackathon.value) {
        hackathon.value.participant_count = (hackathon.value.participant_count || 0) + 1
      }
    } else {
      uiStore.showInfo(t('hackathons.details.alreadyRegistered'), t('common.alreadyRegistered'))
      isRegistered.value = true
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

    // Initialize edit form with fresh API data
    editForm.value = {
      name: apiData.name,
      description: apiData.description || '',
      start_date: formatDateForInput(apiData.start_date),
      end_date: formatDateForInput(apiData.end_date),
      location: apiData.location || '',
      image_url: apiData.image_url || '',
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