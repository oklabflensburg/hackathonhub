import { ref, computed } from 'vue'
import type { Hackathon } from '~/types/hackathon-types'
import { HackathonStatus } from '~/types/hackathon-types'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'
import { format } from 'date-fns'

interface UseHackathonDataOptions {
  hackathonId?: string | number
  autoFetch?: boolean
}

interface EditFormData {
  name: string
  description: string
  start_date: string
  end_date: string
  location: string
  image_url: string
  prizes: Array<{ name: string, description: string, value: string }>
  rules: string
  organizers: Array<{ name: string, role: string }>
  prize_pool: string
}

export function useHackathonData(options: UseHackathonDataOptions = {}) {
  const { hackathonId, autoFetch = true } = options

  const authStore = useAuthStore()
  const uiStore = useUIStore()
  const { t } = useI18n()

  // State
  const hackathon = ref<Hackathon | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)
  const participants = ref<any[]>([])
  const projects = ref<any[]>([])
  const teams = ref<any[]>([])
  
  // Extended state
  const isRegistered = ref(false)
  const registrationLoading = ref(false)
  const isHackathonOwner = ref(false)
  const loadingTeams = ref(false)
  const teamsError = ref<string | null>(null)
  const teamsRequiresAuth = ref(false)
  const editing = ref(false)
  const editLoading = ref(false)
  const editForm = ref<EditFormData>({
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
  })

  // Computed properties
  const isUpcoming = computed(() => hackathon.value?.status === 'upcoming')
  const isActive = computed(() => hackathon.value?.status === 'active')
  const isCompleted = computed(() => hackathon.value?.status === 'completed')
  
  const daysRemaining = computed(() => {
    if (!hackathon.value || !isUpcoming.value) return 0
    const startDate = new Date(hackathon.value.startDate)
    const today = new Date()
    const diffTime = startDate.getTime() - today.getTime()
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  })

  const daysActive = computed(() => {
    if (!hackathon.value || !isActive.value) return 0
    const startDate = new Date(hackathon.value.startDate)
    const today = new Date()
    const diffTime = today.getTime() - startDate.getTime()
    return Math.floor(diffTime / (1000 * 60 * 60 * 24))
  })

  const totalDays = computed(() => {
    if (!hackathon.value) return 0
    const startDate = new Date(hackathon.value.startDate)
    const endDate = new Date(hackathon.value.endDate)
    const diffTime = endDate.getTime() - startDate.getTime()
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  })

  const progressPercentage = computed(() => {
    if (!hackathon.value) return 0
    if (isUpcoming.value) return 0
    if (isCompleted.value) return 100
    const startDate = new Date(hackathon.value.startDate)
    const endDate = new Date(hackathon.value.endDate)
    const today = new Date()
    const totalDuration = endDate.getTime() - startDate.getTime()
    const elapsedDuration = today.getTime() - startDate.getTime()
    return Math.min(100, Math.max(0, (elapsedDuration / totalDuration) * 100))
  })

  const registrationOpen = computed(() => {
    if (!hackathon.value) return false
    if (hackathon.value.registrationDeadline) {
      const deadline = new Date(hackathon.value.registrationDeadline)
      const today = new Date()
      return today < deadline
    }
    return isUpcoming.value
  })

  const prizePoolTotal = computed(() => {
    if (!hackathon.value?.prizes?.length) return '0'
    if (hackathon.value.prizePool) return hackathon.value.prizePool
    const total = hackathon.value.prizes.reduce((sum, prize) => {
      const value = parseFloat(prize.value.replace(/[^0-9.]/g, '')) || 0
      return sum + value
    }, 0)
    return `$${total.toLocaleString()}`
  })

  // Helper functions
  const transformApiHackathon = (apiHackathon: any): Hackathon => {
    const startDate = new Date(apiHackathon.start_date)
    const endDate = new Date(apiHackathon.end_date)
    const now = new Date()
    let status = 'upcoming'
    if (apiHackathon.is_active === false) status = 'completed'
    else if (startDate <= now && endDate >= now) status = 'active'
    else if (endDate < now) status = 'completed'

    let prizes = []
    try {
      if (apiHackathon.prizes) prizes = JSON.parse(apiHackathon.prizes)
    } catch (e) { console.error('Error parsing prizes JSON:', e) }

    let organizers = []
    try {
      if (apiHackathon.organizers) organizers = JSON.parse(apiHackathon.organizers)
    } catch (e) { console.error('Error parsing organizers JSON:', e) }

    return {
      id: String(apiHackathon.id),
      name: apiHackathon.name,
      description: apiHackathon.description || '',
      shortDescription: null,
      startDate: apiHackathon.start_date,
      endDate: apiHackathon.end_date,
      location: apiHackathon.location || '',
      imageUrl: apiHackathon.image_url || null,
      bannerUrl: null,
      status: status as HackathonStatus,
      isActive: apiHackathon.is_active !== false,
      participantCount: apiHackathon.participant_count || 0,
      viewCount: apiHackathon.view_count || 0,
      projectCount: apiHackathon.project_count || 0,
      registrationDeadline: apiHackathon.registration_deadline || null,
      prizes,
      rules: apiHackathon.rules || '',
      organizers,
      prizePool: apiHackathon.prize_pool || null,
      createdAt: apiHackathon.created_at || new Date().toISOString(),
      updatedAt: apiHackathon.updated_at || new Date().toISOString(),
      tags: [],
      websiteUrl: null,
      contactEmail: null,
      maxParticipants: apiHackathon.max_participants || null,
      isVirtual: apiHackathon.is_virtual || false,
      timezone: null,
      slug: apiHackathon.slug,
      stats: undefined,
      latitude: apiHackathon.latitude || null,
      longitude: apiHackathon.longitude || null,
      ownerId: apiHackathon.owner_id || null
    }
  }

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
      const date = new Date(dateTimeString)
      return date.toISOString()
    } catch {
      return dateTimeString
    }
  }

  // Ownership and registration checks
  const checkHackathonOwnership = () => {
    if (!authStore.isAuthenticated || !hackathon.value || !authStore.user) {
      isHackathonOwner.value = false
      return
    }
    if (hackathon.value.ownerId && authStore.user.id === hackathon.value.ownerId) {
      isHackathonOwner.value = true
    } else if (!hackathon.value.ownerId) {
      isHackathonOwner.value = true // fallback
    } else {
      isHackathonOwner.value = false
    }
  }

  const checkRegistrationStatus = async () => {
    if (!authStore.isAuthenticated) {
      isRegistered.value = false
      return
    }
    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/register`)
      if (response.ok) {
        const registrationStatus = await response.json()
        isRegistered.value = registrationStatus.is_registered || false
      } else if (response.status === 404) {
        await checkRegistrationStatusFallback()
      }
    } catch (error) {
      console.error('Error checking registration status:', error)
      await checkRegistrationStatusFallback()
    }
  }

  const checkRegistrationStatusFallback = async () => {
    try {
      const response = await authStore.fetchWithAuth('/api/me/registrations')
      if (response.ok) {
        const registrations = await response.json()
        isRegistered.value = registrations.some((reg: any) =>
          reg.hackathon_id === parseInt(hackathonId?.toString() || '0')
        )
      }
    } catch (fallbackError) {
      console.error('Error in fallback registration check:', fallbackError)
      isRegistered.value = false
    }
  }

  // Core methods
  const fetchHackathon = async (id?: string | number) => {
    const targetId = id || hackathonId
    if (!targetId) {
      error.value = new Error('Keine Hackathon-ID angegeben')
      return
    }
    loading.value = true
    error.value = null
    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${targetId}`)
      if (!response.ok) throw new Error(`Failed to fetch hackathon: ${response.status}`)
      const data = await response.json()
      hackathon.value = transformApiHackathon(data)
      participants.value = []
      projects.value = []
      teams.value = []
      checkHackathonOwnership()
      checkRegistrationStatus()
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Laden des Hackathons')
      console.error('Fehler beim Laden des Hackathons:', err)
      uiStore.showError('Fehler beim Laden des Hackathons')
    } finally {
      loading.value = false
    }
  }

  const fetchParticipants = async (page = 1, pageSize = 20) => {
    if (!hackathonId) return
    loading.value = true
    error.value = null
    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/participants?page=${page}&pageSize=${pageSize}`)
      if (!response.ok) throw new Error(`Failed to fetch participants: ${response.status}`)
      const data = await response.json()
      participants.value = data.participants || []
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Laden der Teilnehmer')
      console.error('Fehler beim Laden der Teilnehmer:', err)
      uiStore.showError('Fehler beim Laden der Teilnehmer')
    } finally {
      loading.value = false
    }
  }

  const fetchProjects = async (page = 1, pageSize = 20) => {
    if (!hackathonId) return
    loading.value = true
    error.value = null
    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/projects?page=${page}&pageSize=${pageSize}`)
      if (!response.ok) throw new Error(`Failed to fetch projects: ${response.status}`)
      const data = await response.json()
      projects.value = data.projects || []
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler beim Laden der Projekte')
      console.error('Fehler beim Laden der Projekte:', err)
      uiStore.showError('Fehler beim Laden der Projekte')
    } finally {
      loading.value = false
    }
  }

  const fetchTeams = async (page = 1, pageSize = 20) => {
    if (!hackathonId) return
    loadingTeams.value = true
    teamsError.value = null
    teamsRequiresAuth.value = false
    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/teams?page=${page}&pageSize=${pageSize}`)
      if (!response.ok) {
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
      if (!teamsError.value) teamsError.value = t('errors.failedToLoad')
    } finally {
      loadingTeams.value = false
    }
  }

  const registerForHackathon = async (userId: string | number, teamId?: string | number) => {
    if (!hackathonId) return false
    registrationLoading.value = true
    error.value = null
    try {
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, teamId })
      })
      if (!response.ok) throw new Error(`Registration failed: ${response.status}`)
      if (hackathon.value) hackathon.value.participantCount++
      isRegistered.value = true
      uiStore.showSuccess(t('hackathons.details.registrationSuccess'))
      return true
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Fehler bei der Registrierung')
      console.error('Fehler bei der Registrierung für den Hackathon:', err)
      uiStore.showError(`${t('hackathons.details.registrationFailed')}: ${err instanceof Error ? err.message : t('common.unknownError')}`, t('common.registrationError'))
      return false
    } finally {
      registrationLoading.value = false
    }
  }

  // Placeholder methods for editing and sharing
  const handleEdit = async () => {
    if (!authStore.isAuthenticated) {
      uiStore.showWarning(t('hackathons.details.loginToEdit'), t('common.authenticationRequired'))
      return
    }
    editing.value = true
    // In a real implementation, load edit form data
  }

  const handleCancelEdit = () => {
    editing.value = false
  }

  const handleSaveEdit = async (formData: any) => {
    editLoading.value = true
    try {
      // Implementation would update hackathon via API
      console.log('Save edit:', formData)
      editing.value = false
      uiStore.showSuccess(t('hackathons.details.hackathonUpdated'))
    } catch (error) {
      console.error('Error updating hackathon:', error)
      uiStore.showError(t('hackathons.details.failedToUpdate'), t('common.updateError'))
    } finally {
      editLoading.value = false
    }
  }

  const handleShare = () => {
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

  // Auto-fetch if requested
  if (autoFetch && hackathonId) {
    fetchHackathon()
  }

  // Return everything
return {
  // State
  hackathon,
  loading,
  error,
  participants,
  projects,
  teams,
  isRegistered,
  registrationLoading,
  isHackathonOwner,
  loadingTeams,
  teamsError,
  teamsRequiresAuth,
  editing,
  editLoading,
  editForm,
  // Computed
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
  checkRegistrationStatus,
  checkHackathonOwnership,
  handleEdit,
  handleCancelEdit,
  handleSaveEdit,
  handleShare,
  // Helper functions
  formatDate,
  formatDateTime,
  formatDateForInput,
  parseDateFromInput
  }
}
