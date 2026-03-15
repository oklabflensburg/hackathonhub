/**
 * File Upload Composable
 * Bietet eine reaktive Schnittstelle für Datei-Uploads mit Progress-Tracking,
 * Error-Handling und Validation.
 * 
 * Migriert auf ApiClient und zentrale Typen.
 */

import { ref, computed } from 'vue'
import { useApiClient } from '~/utils/api-client'
import { useUIStore } from '~/stores/ui'
import type { ApiUploadResponse } from '~/types/file-upload-types'
import { mapApiUploadResponseToFileMetadata } from '~/utils/api-mappers'

export interface UseFileUploadOptions {
  /** Upload-Typ (project, hackathon, avatar) */
  type?: 'project' | 'hackathon' | 'avatar'
  /** Maximale Dateigröße in MB */
  maxSizeMB?: number
  /** Maximale Anzahl gleichzeitiger Uploads */
  maxConcurrentUploads?: number
  /** Automatisches Error-Handling (Notifications) */
  autoErrorHandling?: boolean
  /** Automatisches Progress-Tracking */
  trackProgress?: boolean
}

export interface UploadProgress {
  loaded: number
  total: number
  percentage: number
}

export interface UploadItem {
  id: string
  file: File
  progress: UploadProgress
  status: 'pending' | 'uploading' | 'completed' | 'error' | 'cancelled'
  result?: ApiUploadResponse
  error?: string
}

/**
 * File Upload Composable
 */
export function useFileUpload(options: UseFileUploadOptions = {}) {
  const {
    maxConcurrentUploads = 3,
    autoErrorHandling = true,
    trackProgress = true,
    ...uploadOptions
  } = options

  // Stores
  const uiStore = useUIStore()

  // State
  const uploads = ref<UploadItem[]>([])
  const isUploading = ref(false)
  const activeUploadCount = ref(0)

  // Computed Properties
  const pendingUploads = computed(() => uploads.value.filter(u => u.status === 'pending'))
  const uploadingUploads = computed(() => uploads.value.filter(u => u.status === 'uploading'))
  const completedUploads = computed(() => uploads.value.filter(u => u.status === 'completed'))
  const failedUploads = computed(() => uploads.value.filter(u => u.status === 'error' || u.status === 'cancelled'))
  const totalProgress = computed(() => {
    if (uploads.value.length === 0) return 0

    const total = uploads.value.reduce((sum, item) => sum + item.progress.total, 0)
    const loaded = uploads.value.reduce((sum, item) => sum + item.progress.loaded, 0)
    
    return total > 0 ? Math.round((loaded / total) * 100) : 0
  })

  /**
   * Einzelne Datei hochladen
   */
  async function uploadSingle(file: File, itemOptions?: UseFileUploadOptions): Promise<ApiUploadResponse> {
    const uploadId = generateUploadId()
    
    // Upload-Item erstellen
    const uploadItem: UploadItem = {
      id: uploadId,
      file,
      progress: { loaded: 0, total: file.size, percentage: 0 },
      status: 'pending'
    }
    
    uploads.value.push(uploadItem)
    
    try {
      // Status aktualisieren
      uploadItem.status = 'uploading'
      isUploading.value = true
      activeUploadCount.value++
      
      // Datei validieren
      const validationError = validateFile(file, { 
        maxSizeMB: itemOptions?.maxSizeMB || uploadOptions.maxSizeMB 
      })
      if (validationError) {
        throw new Error(validationError)
      }
      
      // FormData erstellen
      const formData = new FormData()
      formData.append('file', file)
      
      // Query-Parameter
      const params: Record<string, any> = {}
      const type = itemOptions?.type || uploadOptions.type || 'project'
      params.type = type
      
      // ApiClient für Upload verwenden
      const apiClient = useApiClient()
      
      let result: ApiUploadResponse
      
      // Progress-Tracking Simulation (wenn aktiviert)
      if (trackProgress) {
        // Simuliere Progress in 10% Schritten
        const simulateProgress = () => {
          let progress = 0
          const interval = setInterval(() => {
            if (progress < 90) {
              progress += 10
              uploadItem.progress.percentage = progress
              uploadItem.progress.loaded = Math.round((progress / 100) * file.size)
            } else {
              clearInterval(interval)
            }
          }, 200)
          return interval
        }
        
        const progressInterval = simulateProgress()
        
        try {
          // Upload durchführen (POST mit FormData)
          result = await apiClient.post<ApiUploadResponse>('/api/upload', formData, {
            params,
            headers: {
              // Content-Type wird automatisch mit boundary gesetzt
            }
          })
          
          clearInterval(progressInterval)
          uploadItem.progress.percentage = 100
          uploadItem.progress.loaded = file.size
          uploadItem.status = 'completed'
          uploadItem.result = result
          
        } catch (error) {
          clearInterval(progressInterval)
          throw error
        }
      } else {
        // Ohne Progress-Tracking
        result = await apiClient.post<ApiUploadResponse>('/api/upload', formData, {
          params,
          headers: {
            // Content-Type wird automatisch mit boundary gesetzt
          }
        })
        
        // Erfolg
        uploadItem.status = 'completed'
        uploadItem.result = result
        uploadItem.progress.percentage = 100
        uploadItem.progress.loaded = file.size
      }
      
      // Success Notification
      if (autoErrorHandling) {
        uiStore.showSuccess('Datei erfolgreich hochgeladen', 'Upload')
      }
      
      return result
      
    } catch (error: any) {
      // Error
      uploadItem.status = 'error'
      uploadItem.error = error.message || 'Upload fehlgeschlagen'
      
      // Error Notification
      if (autoErrorHandling && uploadItem.error) {
        uiStore.showError(uploadItem.error, 'Upload Fehler')
      }
      
      throw error
      
    } finally {
      activeUploadCount.value--
      isUploading.value = activeUploadCount.value > 0
    }
  }

  /**
   * Mehrere Dateien hochladen (parallel mit Limit)
   */
  async function uploadMultiple(files: File[], itemOptions?: UseFileUploadOptions): Promise<ApiUploadResponse[]> {
    const results: ApiUploadResponse[] = []
    
    // Upload-Items für alle Dateien erstellen
    const uploadItems = files.map(file => ({
      id: generateUploadId(),
      file,
      progress: { loaded: 0, total: file.size, percentage: 0 },
      status: 'pending' as const
    }))
    
    uploads.value.push(...uploadItems)
    
    // Parallel uploaden mit Limit
    const uploadPromises: Promise<ApiUploadResponse>[] = []
    const activeUploads: UploadItem[] = []
    
    for (const uploadItem of uploadItems) {
      // Warten, wenn maximale Anzahl erreicht
      while (activeUploads.length >= maxConcurrentUploads) {
        await Promise.race(activeUploads.map(item => {
          const promise = new Promise<void>((resolve) => {
            const checkStatus = () => {
              if (item.status === 'completed' || item.status === 'error' || item.status === 'cancelled') {
                const index = activeUploads.indexOf(item)
                if (index > -1) activeUploads.splice(index, 1)
                resolve()
              }
            }
            // Polling (einfache Implementierung)
            const interval = setInterval(checkStatus, 100)
            setTimeout(() => {
              clearInterval(interval)
              resolve()
            }, 5000)
          })
          return promise
        }))
      }
      
      // Upload starten
      activeUploads.push(uploadItem)
      const promise = uploadSingle(uploadItem.file, itemOptions)
        .then(result => {
          results.push(result)
          return result
        })
        .finally(() => {
          const index = activeUploads.indexOf(uploadItem)
          if (index > -1) activeUploads.splice(index, 1)
        })
      
      uploadPromises.push(promise)
    }
    
    // Auf alle Uploads warten
    await Promise.allSettled(uploadPromises)
    return results
  }

  /**
   * Upload abbrechen
   */
  function cancelUpload(uploadId: string): void {
    const uploadItem = uploads.value.find(u => u.id === uploadId)
    if (uploadItem && (uploadItem.status === 'pending' || uploadItem.status === 'uploading')) {
      uploadItem.status = 'cancelled'
      uploadItem.error = 'Upload abgebrochen'
      
      // TODO: Aktuell können wir den tatsächlichen Fetch-Request nicht abbrechen
      // In einer zukünftigen Version könnten wir AbortController verwenden
    }
  }

  /**
   * Alle Uploads abbrechen
   */
  function cancelAllUploads(): void {
    uploads.value.forEach(item => {
      if (item.status === 'pending' || item.status === 'uploading') {
        item.status = 'cancelled'
        item.error = 'Upload abgebrochen'
      }
    })
  }

  /**
   * Upload-Item entfernen
   */
  function removeUpload(uploadId: string): void {
    const index = uploads.value.findIndex(u => u.id === uploadId)
    if (index > -1) {
      uploads.value.splice(index, 1)
    }
  }

  /**
   * Alle abgeschlossenen Uploads entfernen
   */
  function clearCompletedUploads(): void {
    uploads.value = uploads.value.filter(u => u.status !== 'completed')
  }

  /**
   * Alle Uploads entfernen
   */
  function clearAllUploads(): void {
    uploads.value = []
    isUploading.value = false
    activeUploadCount.value = 0
  }

  /**
   * Datei validieren
   */
  function validateFile(file: File, customOptions?: { maxSizeMB?: number; allowedTypes?: string[] }): string | null {
    const { maxSizeMB = uploadOptions.maxSizeMB || 10, allowedTypes } = customOptions || {}
    
    // Größe validieren
    const maxSizeBytes = maxSizeMB * 1024 * 1024
    if (file.size > maxSizeBytes) {
      return `Datei zu groß. Maximale Größe: ${maxSizeMB} MB.`
    }
    
    // Typ validieren
    if (allowedTypes && allowedTypes.length > 0) {
      if (!allowedTypes.includes(file.type)) {
        return `Ungültiger Dateityp. Erlaubte Typen: ${allowedTypes.join(', ')}.`
      }
    } else {
      // Standard-Image-Typen
      const defaultAllowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
      if (!defaultAllowedTypes.includes(file.type)) {
        return 'Ungültiger Dateityp. Erlaubte Typen: JPEG, PNG, GIF, WebP.'
      }
    }
    
    return null
  }

  /**
   * Upload-Status abrufen
   */
  function getUploadStatus(uploadId: string): UploadItem | undefined {
    return uploads.value.find(u => u.id === uploadId)
  }

  /**
   * Eindeutige Upload-ID generieren
   */
  function generateUploadId(): string {
    return `upload_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  /**
   * Vorschau-URL für eine Datei erstellen (für Anzeige vor dem Upload)
   */
  function createPreviewUrl(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = (e) => {
        resolve(e.target?.result as string)
      }
      reader.onerror = () => {
        reject(new Error('Failed to create preview'))
      }
      reader.readAsDataURL(file)
    })
  }

  return {
    // State
    uploads: computed(() => uploads.value),
    isUploading: computed(() => isUploading.value),
    activeUploadCount: computed(() => activeUploadCount.value),
    
    // Computed
    pendingUploads,
    uploadingUploads,
    completedUploads,
    failedUploads,
    totalProgress,
    
    // Methods
    uploadSingle,
    uploadMultiple,
    cancelUpload,
    cancelAllUploads,
    removeUpload,
    clearCompletedUploads,
    clearAllUploads,
    validateFile,
    createPreviewUrl,
    getUploadStatus,
    
    // Utilities
    reset: clearAllUploads
  }
}
