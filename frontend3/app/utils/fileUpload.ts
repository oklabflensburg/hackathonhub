/**
 * File upload utility for handling image uploads to the backend
 */

import { useAuthStore } from '~/stores/auth'

export interface UploadResponse {
  file_path: string
  url: string
  filename: string
  message: string
}

export interface UploadOptions {
  type?: 'project' | 'hackathon' | 'avatar'
  entityId?: number
  maxSizeMB?: number
}

/**
 * Upload a file to the backend
 * 
 * @param file - The file to upload
 * @param options - Upload options
 * @returns Promise with upload response
 */
export async function uploadFile(
  file: File,
  options: UploadOptions = {}
): Promise<UploadResponse> {
  const { type = 'project', entityId, maxSizeMB = 10 } = options

  // Validate file size
  const maxSizeBytes = maxSizeMB * 1024 * 1024
  if (file.size > maxSizeBytes) {
    throw new Error(`File too large. Maximum size is ${maxSizeMB}MB.`)
  }

  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    throw new Error(
      'Invalid file type. Allowed types: JPEG, PNG, GIF, WebP'
    )
  }

  // Create FormData
  const formData = new FormData()
  formData.append('file', file)

  // Build query parameters
  const params = new URLSearchParams()
  params.append('type', type)
  if (entityId) {
    params.append('entity_id', entityId.toString())
  }

  // Get auth store for authenticated requests
  const authStore = useAuthStore()
  const token = authStore.token

  try {
    // For file uploads, we need to handle the request specially
    // Use direct fetch instead of fetchWithAuth to avoid header issues

    // Use runtime config for API URL
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    const fullUrl = `/api/upload?${params.toString()}`
    const absoluteUrl = fullUrl.startsWith('http') ? fullUrl : `${backendUrl}${fullUrl}`

    const headers: Record<string, string> = {}
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    // Note: Don't set Content-Type - browser will set it with boundary for FormData

    const response = await fetch(absoluteUrl, {
      method: 'POST',
      body: formData,
      headers
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(
        errorData.detail || `Upload failed with status ${response.status}`
      )
    }

    return await response.json()
  } catch (error) {
    if (error instanceof Error) {
      throw error
    }
    throw new Error('File upload failed')
  }
}

/**
 * Check if a string is a base64 data URL
 */
export function isBase64DataUrl(str: string): boolean {
  return str.startsWith('data:image/') && str.includes('base64,')
}

/**
 * Extract file extension from filename or MIME type
 */
export function getFileExtension(filename: string, mimeType?: string): string {
  // Try to get from filename first
  const lastDotIndex = filename.lastIndexOf('.')
  if (lastDotIndex !== -1) {
    return filename.substring(lastDotIndex).toLowerCase()
  }

  // Fallback to MIME type mapping
  if (mimeType) {
    const mimeToExt: Record<string, string> = {
      'image/jpeg': '.jpg',
      'image/png': '.png',
      'image/gif': '.gif',
      'image/webp': '.webp',
    }
    return mimeToExt[mimeType] || '.jpg'
  }

  return '.jpg'
}

/**
 * Create a preview URL for a file (for display before upload)
 */
export function createPreviewUrl(file: File): Promise<string> {
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

/**
 * Validate file before upload
 */
export function validateFile(file: File, maxSizeMB: number = 10): string | null {
  // Check file size
  const maxSizeBytes = maxSizeMB * 1024 * 1024
  if (file.size > maxSizeBytes) {
    return `File too large. Maximum size is ${maxSizeMB}MB.`
  }

  // Check file type
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    return 'Invalid file type. Allowed types: JPEG, PNG, GIF, WebP'
  }

  return null
}