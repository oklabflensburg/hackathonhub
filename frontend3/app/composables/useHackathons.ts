/**
 * Hackathons Composable
 * Bietet eine konsistente Schnittstelle für alle Hackathon-Operationen
 * Kapselt API-Aufrufe und bietet reaktiven State, Loading-States und Error-Handling
 * 
 * Vollständig migriert zur Verwendung zentraler Typ-Definitionen (hackathon-types.ts)
 * und API-Response Mapper (api-mappers.ts)
 */

import { ref, computed } from 'vue'
import { useApiClient } from '~/utils/api-client'
import { useUIStore } from '~/stores/ui'
import type {
  Hackathon,
  HackathonCreateData,
  HackathonUpdateData,
  HackathonRegistration,
  HackathonRegistrationStatus,
  HackathonStatus,
  ApiHackathon,
  ApiHackathonCreateData,
  ApiHackathonUpdateData,
  ApiHackathonRegistration,
  ApiHackathonRegistrationStatus
} from '~/types/hackathon-types'
import {
  snakeToCamel,
  mapApiHackathonToHackathon,
  mapApiHackathonRegistrationToHackathonRegistration,
  mapApiHackathonRegistrationStatusToHackathonRegistrationStatus,
  mapHackathonCreateUpdateDataToApi,
  idToNumber,
  idToString,
  mapPaginatedResponse
} from '~/utils/api-mappers'

export interface UseHackathonsOptions {
  /** Automatisches Error-Handling (Notifications) */
  autoErrorHandling?: boolean
  /** Automatisches Success-Handling (Notifications) */
  autoSuccessHandling?: boolean
  /** Initiale Hackathon-ID für Single-Hackathon-Operationen */
  initialHackathonId?: string
}

/**
 * Hackathons Composable
 */
export function useHackathons(options: UseHackathonsOptions = {}) {
  const {
    autoErrorHandling = true,
    autoSuccessHandling = true,
    initialHackathonId
  } = options

  // Stores und Services
  const uiStore = useUIStore()
  const apiClient = useApiClient()

  // State
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const hackathons = ref<Hackathon[]>([])
  const currentHackathon = ref<Hackathon | null>(null)
  const hackathonRegistrations = ref<HackathonRegistration[]>([])
  const registrationStatus = ref<Record<string, HackathonRegistrationStatus>>({})

  // Computed Properties
  const hasHackathons = computed(() => hackathons.value.length > 0)
  const hackathonCount = computed(() => hackathons.value.length)
  const activeHackathons = computed(() => hackathons.value.filter(h => h.isActive))
  const upcomingHackathons = computed(() => {
    const now = new Date()
    return hackathons.value.filter(h => {
      const startDate = new Date(h.startDate)
      return startDate > now && h.isActive
    })
  })
  const ongoingHackathons = computed(() => {
    const now = new Date()
    return hackathons.value.filter(h => {
      const startDate = new Date(h.startDate)
      const endDate = new Date(h.endDate)
      return startDate <= now && endDate >= now && h.isActive
    })
  })

  /**
   * Alle Hackathons abrufen
   */
  async function fetchHackathons(filters?: {
    skip?: number
    limit?: number
    activeOnly?: boolean
    search?: string
  }): Promise<Hackathon[]> {
    try {
      isLoading.value = true
      error.value = null

      const queryParams = new URLSearchParams()
      if (filters?.skip) queryParams.append('skip', filters.skip.toString())
      if (filters?.limit) queryParams.append('limit', filters.limit.toString())
      if (filters?.search) queryParams.append('search', filters.search)

      const url = `/api/hackathons${queryParams.toString() ? `?${queryParams.toString()}` : ''}`
      const response = await apiClient.get<ApiHackathon[]>(url)

      // API-Response zu Frontend-Typen mappen
      const mappedHackathons = response.map(mapApiHackathonToHackathon)

      // Wenn activeOnly gefiltert werden soll
      if (filters?.activeOnly) {
        hackathons.value = mappedHackathons.filter(h => h.isActive)
      } else {
        hackathons.value = mappedHackathons
      }
      
      return mappedHackathons
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Abrufen der Hackathons'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Hackathons Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Einzelnes Hackathon abrufen
   */
  async function fetchHackathon(hackathonId: string): Promise<Hackathon> {
    try {
      isLoading.value = true
      error.value = null

      const numericId = idToNumber(hackathonId)
      const response = await apiClient.get<ApiHackathon>(`/api/hackathons/${numericId}`)
      const hackathon = mapApiHackathonToHackathon(response)
      currentHackathon.value = hackathon

      // Registrierungsstatus prüfen
      await checkRegistrationStatus(hackathonId)

      return hackathon
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Abrufen des Hackathons'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Hackathon Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Hackathon erstellen
   */
  async function createHackathon(hackathonData: HackathonCreateData): Promise<Hackathon> {
    try {
      isLoading.value = true
      error.value = null

      // Frontend-Daten zu API-Payload mappen
      const apiPayload = mapHackathonCreateUpdateDataToApi(hackathonData)
      const response = await apiClient.post<ApiHackathon>('/api/hackathons', apiPayload, {
        skipErrorNotification: true
      })

      // API-Response zu Frontend-Typ mappen
      const hackathon = mapApiHackathonToHackathon(response)

      // Zum lokalen State hinzufügen
      hackathons.value = [hackathon, ...hackathons.value]
      currentHackathon.value = hackathon

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Hackathon erfolgreich erstellt', 'Hackathon')
      }

      return hackathon
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Erstellen des Hackathons'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Hackathon Erstellung Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Hackathon aktualisieren
   */
  async function updateHackathon(hackathonId: string, hackathonData: HackathonUpdateData): Promise<Hackathon> {
    try {
      isLoading.value = true
      error.value = null

      // Frontend-Daten zu API-Payload mappen
      const apiPayload = mapHackathonCreateUpdateDataToApi(hackathonData)
      const numericId = idToNumber(hackathonId)
      const response = await apiClient.put<ApiHackathon>(`/api/hackathons/${numericId}`, apiPayload, {
        skipErrorNotification: true
      })

      // API-Response zu Frontend-Typ mappen
      const hackathon = mapApiHackathonToHackathon(response)

      // Lokalen State aktualisieren
      if (currentHackathon.value?.id === hackathonId) {
        currentHackathon.value = hackathon
      }

      // In der Hackathons-Liste aktualisieren
      const index = hackathons.value.findIndex(h => h.id === hackathonId)
      if (index !== -1) {
        hackathons.value[index] = hackathon
      }

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Hackathon erfolgreich aktualisiert', 'Hackathon')
      }

      return hackathon
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Aktualisieren des Hackathons'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Hackathon Update Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Hackathon löschen
   */
  async function deleteHackathon(hackathonId: string): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      const numericId = idToNumber(hackathonId)
      await apiClient.delete(`/api/hackathons/${numericId}`, {
        skipErrorNotification: true
      })

      // Aus lokalem State entfernen
      hackathons.value = hackathons.value.filter(h => h.id !== hackathonId)
      if (currentHackathon.value?.id === hackathonId) {
        currentHackathon.value = null
      }

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Hackathon erfolgreich gelöscht', 'Hackathon')
      }
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Löschen des Hackathons'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Hackathon Löschung Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Für Hackathon registrieren
   */
  async function registerForHackathon(hackathonId: string): Promise<HackathonRegistration> {
    try {
      isLoading.value = true
      error.value = null

      const numericId = idToNumber(hackathonId)
      const response = await apiClient.post<ApiHackathonRegistration>(`/api/hackathons/${numericId}/register`, {}, {
        skipErrorNotification: true
      })

      // API-Response zu Frontend-Typ mappen
      const registration = mapApiHackathonRegistrationToHackathonRegistration(response)

      // Zum lokalen State hinzufügen
      hackathonRegistrations.value = [...hackathonRegistrations.value, registration]

      // Registrierungsstatus aktualisieren
      registrationStatus.value[hackathonId] = mapApiHackathonRegistrationStatusToHackathonRegistrationStatus({
        is_registered: true,
        hackathon_id: numericId,
        registration_id: response.id,
        status: response.status,
        registered_at: response.registered_at
      })

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Erfolgreich für Hackathon registriert', 'Hackathon')
      }

      return registration
    } catch (err: any) {
      error.value = err.message || 'Fehler bei der Registrierung für den Hackathon'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Hackathon Registrierung Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Von Hackathon abmelden
   */
  async function unregisterFromHackathon(hackathonId: string): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      const numericId = idToNumber(hackathonId)
      await apiClient.delete(`/api/hackathons/${numericId}/register`, {
        skipErrorNotification: true
      })

      // Aus lokalem State entfernen
      hackathonRegistrations.value = hackathonRegistrations.value.filter(r => r.hackathonId !== hackathonId)

      // Registrierungsstatus aktualisieren
      registrationStatus.value[hackathonId] = mapApiHackathonRegistrationStatusToHackathonRegistrationStatus({
        is_registered: false,
        hackathon_id: numericId
      })

      // Success Notification
      if (autoSuccessHandling) {
        uiStore.showSuccess('Erfolgreich vom Hackathon abgemeldet', 'Hackathon')
      }
    } catch (err: any) {
      error.value = err.message || 'Fehler beim Abmelden vom Hackathon'
      
      if (autoErrorHandling && error.value) {
        uiStore.showError(error.value, 'Hackathon Abmeldung Fehler')
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Registrierungsstatus prüfen
   */
  async function checkRegistrationStatus(hackathonId: string): Promise<HackathonRegistrationStatus> {
    try {
      const numericId = idToNumber(hackathonId)
      const response = await apiClient.get<ApiHackathonRegistrationStatus>(`/api/hackathons/${numericId}/registration-status`)
      const status = mapApiHackathonRegistrationStatusToHackathonRegistrationStatus(response)
      registrationStatus.value[hackathonId] = status
      return status
    } catch (err: any) {
      console.error('Fehler beim Prüfen des Registrierungsstatus:', err)
      throw err
    }
  }

  /**
   * Hackathon-Registrierungen abrufen
   */
  async function fetchHackathonRegistrations(hackathonId: string): Promise<HackathonRegistration[]> {
    try {
      const numericId = idToNumber(hackathonId)
      const response = await apiClient.get<ApiHackathonRegistration[]>(`/api/hackathons/${numericId}/registrations`)
      const registrations = response.map(mapApiHackathonRegistrationToHackathonRegistration)
      hackathonRegistrations.value = registrations
      return registrations
    } catch (err: any) {
      console.error('Fehler beim Abrufen der Hackathon-Registrierungen:', err)
      throw err
    }
  }

  /**
   * Hackathon-Teams abrufen
   */
  async function fetchHackathonTeams(hackathonId: string): Promise<any[]> {
    try {
      const numericId = idToNumber(hackathonId)
      const response = await apiClient.get<any[]>(`/api/hackathons/${numericId}/teams`)
      return response
    } catch (err: any) {
      console.error('Fehler beim Abrufen der Hackathon-Teams:', err)
      throw err
    }
  }

  /**
   * Hackathon-Projekte abrufen
   */
  async function fetchHackathonProjects(hackathonId: string): Promise<any[]> {
    try {
      const numericId = idToNumber(hackathonId)
      const response = await apiClient.get<any[]>(`/api/hackathons/${numericId}/projects`)
      return response
    } catch (err: any) {
      console.error('Fehler beim Abrufen der Hackathon-Projekte:', err)
      throw err
    }
  }

  /**
   * Error zurücksetzen
   */
  function clearError(): void {
    error.value = null
  }

  /**
   * Loading-State zurücksetzen
   */
  function clearLoading(): void {
    isLoading.value = false
  }

  /**
   * Composable zurücksetzen
   */
  function reset(): void {
    isLoading.value = false
    error.value = null
    hackathons.value = []
    currentHackathon.value = null
    hackathonRegistrations.value = []
    registrationStatus.value = {}
  }

  return {
    // State
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    hackathons: computed(() => hackathons.value),
    currentHackathon: computed(() => currentHackathon.value),
    hackathonRegistrations: computed(() => hackathonRegistrations.value),
    registrationStatus: computed(() => registrationStatus.value),
    
    // Computed
    hasHackathons,
    hackathonCount,
    activeHackathons,
    upcomingHackathons,
    ongoingHackathons,
    
    // Methods
    fetchHackathons,
    fetchHackathon,
    createHackathon,
    updateHackathon,
    deleteHackathon,
    registerForHackathon,
    unregisterFromHackathon,
    checkRegistrationStatus,
    fetchHackathonRegistrations,
    fetchHackathonTeams,
    fetchHackathonProjects,
    
    // Utilities
    clearError,
    clearLoading,
    reset
  }
}