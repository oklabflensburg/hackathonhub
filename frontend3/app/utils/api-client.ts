/**
 * API Client Abstraktion für konsistente HTTP-Requests
 * Bietet eine einfache Schnittstelle für alle API-Aufrufe mit automatischem
 * Error-Handling, TypeScript-Unterstützung und Authentication-Integration.
 */

import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { useRuntimeConfig } from '#imports'

export interface ApiError extends Error {
  status?: number
  data?: any
}

export interface ApiRequestOptions extends RequestInit {
  params?: Record<string, any>
  skipAuth?: boolean
  skipErrorNotification?: boolean
}

export class ApiClient {
  private authStore = useAuthStore()
  private uiStore = useUIStore()
  private backendUrl: string

  constructor(backendUrl: string) {
    this.backendUrl = backendUrl
  }

  /**
   * Führt einen GET-Request aus
   */
  async get<T = any>(url: string, options: ApiRequestOptions = {}): Promise<T> {
    return this.request<T>('GET', url, options)
  }

  /**
   * Führt einen POST-Request aus
   */
  async post<T = any>(url: string, body?: any, options: ApiRequestOptions = {}): Promise<T> {
    return this.request<T>('POST', url, { ...options, body })
  }

  /**
   * Führt einen PUT-Request aus
   */
  async put<T = any>(url: string, body?: any, options: ApiRequestOptions = {}): Promise<T> {
    return this.request<T>('PUT', url, { ...options, body })
  }

  /**
   * Führt einen PATCH-Request aus
   */
  async patch<T = any>(url: string, body?: any, options: ApiRequestOptions = {}): Promise<T> {
    return this.request<T>('PATCH', url, { ...options, body })
  }

  /**
   * Führt einen DELETE-Request aus
   */
  async delete<T = any>(url: string, options: ApiRequestOptions = {}): Promise<T> {
    return this.request<T>('DELETE', url, options)
  }

  /**
   * Generische Request-Methode
   */
  private async request<T = any>(method: string, url: string, options: ApiRequestOptions = {}): Promise<T> {
    try {
      // URL mit Query-Parametern erstellen
      const urlWithParams = this.buildUrl(url, options.params)

      // Request-Optionen vorbereiten
      const requestOptions = this.prepareRequestOptions(method, options)

      // Request ausführen
      let response: Response
      if (options.skipAuth) {
        // Direkter fetch ohne Authentication
        response = await this.fetchWithoutAuth(urlWithParams, requestOptions)
      } else {
        // fetch mit Authentication
        response = await this.authStore.fetchWithAuth(urlWithParams, requestOptions)
      }

      // Response verarbeiten
      return await this.handleResponse<T>(response, options)
    } catch (error) {
      return this.handleError(error, options)
    }
  }

  /**
   * URL mit Query-Parametern erstellen
   */
  private buildUrl(url: string, params?: Record<string, any>): string {
    if (!params || Object.keys(params).length === 0) {
      return url
    }

    const searchParams = new URLSearchParams()
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== null) {
        if (Array.isArray(value)) {
          value.forEach(v => searchParams.append(key, v.toString()))
        } else {
          searchParams.append(key, value.toString())
        }
      }
    }

    const queryString = searchParams.toString()
    return queryString ? `${url}?${queryString}` : url
  }

  /**
   * Request-Optionen vorbereiten
   */
  private prepareRequestOptions(method: string, options: ApiRequestOptions): RequestInit {
    const { body, params, skipAuth, skipErrorNotification, ...restOptions } = options

    const headers = new Headers(restOptions.headers || {})

    // Content-Type setzen, wenn nicht bereits gesetzt und Body vorhanden
    if (body && !headers.has('Content-Type') && !(body instanceof FormData)) {
      headers.set('Content-Type', 'application/json')
    }

    // Body serialisieren, wenn es JSON ist
    let serializedBody = body
    if (body && !(body instanceof FormData) && !(body instanceof URLSearchParams)) {
      serializedBody = JSON.stringify(body)
    }

    return {
      method,
      headers,
      body: serializedBody,
      credentials: restOptions.credentials ?? 'include',
      ...restOptions,
    }
  }

  /**
   * fetch ohne Authentication (für öffentliche Endpunkte)
   */
  private async fetchWithoutAuth(url: string, options: RequestInit): Promise<Response> {
    const fullUrl = url.startsWith('http') ? url : `${this.backendUrl}${url}`

    return fetch(fullUrl, options)
  }

  /**
   * Response verarbeiten
   */
  private async handleResponse<T>(response: Response, options: ApiRequestOptions): Promise<T> {
    // Leere Response (z.B. bei 204 No Content)
    if (response.status === 204) {
      return undefined as T
    }

    // Response parsen
    const contentType = response.headers.get('content-type')
    let data: any

    if (contentType && contentType.includes('application/json')) {
      data = await response.json()
    } else {
      data = await response.text()
    }

    // Error werfen, wenn Response nicht ok ist
    if (!response.ok) {
      const error: ApiError = new Error(data?.detail || data?.message || `HTTP error ${response.status}`)
      error.status = response.status
      error.data = data
      throw error
    }

    return data as T
  }

  /**
   * Error verarbeiten
   */
  private handleError(error: any, options: ApiRequestOptions): never {
    // Error logging
    console.error('API Request failed:', {
      error,
      options,
    })

    // User-friendly Error-Message erstellen
    let userMessage = 'Ein unerwarteter Fehler ist aufgetreten'

    if (error instanceof Error) {
      const apiError = error as ApiError
      
      if (apiError.status === 401) {
        userMessage = 'Ihre Sitzung ist abgelaufen. Bitte melden Sie sich erneut an.'
      } else if (apiError.status === 403) {
        userMessage = 'Sie haben keine Berechtigung für diese Aktion.'
      } else if (apiError.status === 404) {
        userMessage = 'Die angeforderte Ressource wurde nicht gefunden.'
      } else if (apiError.status === 422) {
        userMessage = 'Ungültige Eingabedaten. Bitte überprüfen Sie Ihre Eingaben.'
      } else if (apiError.status === 429) {
        userMessage = 'Zu viele Anfragen. Bitte versuchen Sie es später erneut.'
      } else if (apiError.status && apiError.status >= 500) {
        userMessage = 'Ein Serverfehler ist aufgetreten. Bitte versuchen Sie es später erneut.'
      } else if (apiError.message) {
        userMessage = apiError.message
      }
    }

    // Notification anzeigen (wenn nicht deaktiviert)
    if (!options.skipErrorNotification) {
      this.uiStore.showError(userMessage, 'Fehler')
    }

    // Error weiterwerfen
    throw error
  }
}

/**
 * Singleton-Instanz des API-Clients
 */
let apiClientInstance: ApiClient | null = null

export function useApiClient(): ApiClient {
  if (!apiClientInstance) {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl
    apiClientInstance = new ApiClient(backendUrl)
  }
  return apiClientInstance
}
