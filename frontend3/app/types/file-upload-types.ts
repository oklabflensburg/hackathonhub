/**
 * File Upload TypeScript Types for Atomic Design Components
 * 
 * This file defines all TypeScript interfaces and enums for file upload components
 * Used across atoms, molecules, organisms, templates, and composables
 */

// ==================== ENUMS ====================

/**
 * File upload status enum
 */
export enum FileUploadStatus {
  PENDING = 'pending',
  UPLOADING = 'uploading',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

/**
 * File type enum
 */
export enum FileType {
  IMAGE = 'image',
  DOCUMENT = 'document',
  VIDEO = 'video',
  AUDIO = 'audio',
  ARCHIVE = 'archive',
  OTHER = 'other'
}

/**
 * File validation error enum
 */
export enum FileValidationError {
  SIZE_EXCEEDED = 'size_exceeded',
  TYPE_NOT_ALLOWED = 'type_not_allowed',
  CORRUPTED = 'corrupted',
  DIMENSIONS_INVALID = 'dimensions_invalid',
  DURATION_INVALID = 'duration_invalid',
  RESOLUTION_INVALID = 'resolution_invalid'
}

// ==================== INTERFACES ====================

/**
 * File metadata interface
 */
export interface FileMetadata {
  id: string
  name: string
  size: number
  type: FileType
  mimeType: string
  extension: string
  url: string
  thumbnailUrl?: string | null
  dimensions?: {
    width: number
    height: number
  }
  duration?: number // in seconds, for audio/video
  createdAt: string
  updatedAt: string
  uploadedBy: string
  entityType: 'project' | 'hackathon' | 'team' | 'user' | 'comment'
  entityId: string
  tags: string[]
  description?: string | null
  isPublic: boolean
  metadata?: Record<string, any>
}

/**
 * File upload progress interface
 */
export interface FileUploadProgress {
  fileId: string
  fileName: string
  progress: number // 0-100
  status: FileUploadStatus
  uploadedBytes: number
  totalBytes: number
  speed: number // bytes per second
  estimatedTimeRemaining: number // seconds
  error?: FileValidationError | string | null
}

/**
 * File upload options interface
 */
export interface FileUploadOptions {
  maxFileSize?: number // in bytes
  allowedTypes?: FileType[]
  allowedMimeTypes?: string[]
  maxDimensions?: {
    width: number
    height: number
  }
  minDimensions?: {
    width: number
    height: number
  }
  maxDuration?: number // in seconds, for audio/video
  maxResolution?: number // in pixels, for images
  multiple?: boolean
  maxFiles?: number
  chunkSize?: number // in bytes
  parallelUploads?: number
  autoUpload?: boolean
  showPreview?: boolean
  showProgress?: boolean
  showCancelButton?: boolean
  showRetryButton?: boolean
}

/**
 * File upload request interface
 */
export interface FileUploadRequest {
  file: File
  entityType: 'project' | 'hackathon' | 'team' | 'user' | 'comment'
  entityId: string
  tags?: string[]
  description?: string | null
  isPublic?: boolean
  metadata?: Record<string, any>
  options?: FileUploadOptions
}

/**
 * File upload response interface
 */
export interface FileUploadResponse {
  success: boolean
  file?: FileMetadata
  error?: string | FileValidationError
  validationErrors?: FileValidationError[]
}

/**
 * File validation result interface
 */
export interface FileValidationResult {
  isValid: boolean
  errors: FileValidationError[]
  warnings: string[]
  metadata?: Partial<FileMetadata>
}

// ==================== COMPONENT PROPS ====================

/**
 * File uploader props
 */
export interface FileUploaderProps {
  entityType: 'project' | 'hackathon' | 'team' | 'user' | 'comment'
  entityId: string
  options?: FileUploadOptions
  multiple?: boolean
  disabled?: boolean
  accept?: string
  maxFiles?: number
  showPreview?: boolean
  showProgress?: boolean
  onUploadStart?: (files: File[]) => void
  onUploadProgress?: (progress: FileUploadProgress[]) => void
  onUploadComplete?: (responses: FileUploadResponse[]) => void
  onUploadError?: (error: Error) => void
  onFileSelect?: (files: File[]) => void
  onFileRemove?: (fileId: string) => void
}

/**
 * File upload progress bar props
 */
export interface FileUploadProgressBarProps {
  progress: FileUploadProgress
  showDetails?: boolean
  showCancelButton?: boolean
  showRetryButton?: boolean
  onCancel?: (fileId: string) => void
  onRetry?: (fileId: string) => void
}

/**
 * File preview props
 */
export interface FilePreviewProps {
  file: FileMetadata | File
  showInfo?: boolean
  showActions?: boolean
  previewSize?: 'sm' | 'md' | 'lg' | 'xl'
  onRemove?: () => void
  onDownload?: () => void
  onPreview?: () => void
}

/**
 * File dropzone props
 */
export interface FileDropzoneProps {
  accept?: string
  multiple?: boolean
  disabled?: boolean
  maxFiles?: number
  maxSize?: number
  showInstructions?: boolean
  dragActiveLabel?: string
  dragInactiveLabel?: string
  fileTypeErrorLabel?: string
  fileSizeErrorLabel?: string
  onFilesSelected: (files: File[]) => void
  onDragEnter?: () => void
  onDragLeave?: () => void
  onDrop?: () => void
}

// ==================== COMPOSABLE RETURN TYPES ====================

/**
 * UseFileUpload composable return type
 */
export interface UseFileUploadReturn {
  files: Ref<FileMetadata[]>
  uploads: Ref<FileUploadProgress[]>
  loading: Ref<boolean>
  error: Ref<string | null>
  options: Ref<FileUploadOptions>
  
  uploadFile: (request: FileUploadRequest) => Promise<FileUploadResponse>
  uploadFiles: (requests: FileUploadRequest[]) => Promise<FileUploadResponse[]>
  cancelUpload: (fileId: string) => boolean
  retryUpload: (fileId: string) => Promise<FileUploadResponse>
  removeFile: (fileId: string) => boolean
  validateFile: (file: File) => FileValidationResult
  getFileUrl: (fileId: string) => string | null
  getFileThumbnailUrl: (fileId: string) => string | null
  resetUploads: () => void
}

// ==================== UTILITY TYPES ====================

/**
 * File upload queue item
 */
export interface FileUploadQueueItem {
  id: string
  request: FileUploadRequest
  progress: FileUploadProgress
  promise: Promise<FileUploadResponse>
  controller: AbortController
}

/**
 * File upload manager state
 */
export interface FileUploadManagerState {
  queue: FileUploadQueueItem[]
  activeUploads: number
  completedUploads: number
  failedUploads: number
  totalBytesUploaded: number
  totalBytesToUpload: number
  averageSpeed: number
}

// ==================== UTILITY CONSTANTS ====================

/**
 * File type icons
 */
export const FILE_TYPE_ICONS: Record<FileType, string> = {
  [FileType.IMAGE]: 'i-heroicons-photo',
  [FileType.DOCUMENT]: 'i-heroicons-document',
  [FileType.VIDEO]: 'i-heroicons-video-camera',
  [FileType.AUDIO]: 'i-heroicons-musical-note',
  [FileType.ARCHIVE]: 'i-heroicons-archive-box',
  [FileType.OTHER]: 'i-heroicons-document'
}

/**
 * File type labels
 */
export const FILE_TYPE_LABELS: Record<FileType, string> = {
  [FileType.IMAGE]: 'Bild',
  [FileType.DOCUMENT]: 'Dokument',
  [FileType.VIDEO]: 'Video',
  [FileType.AUDIO]: 'Audio',
  [FileType.ARCHIVE]: 'Archiv',
  [FileType.OTHER]: 'Andere'
}

/**
 * File upload status labels
 */
export const FILE_UPLOAD_STATUS_LABELS: Record<FileUploadStatus, string> = {
  [FileUploadStatus.PENDING]: 'Ausstehend',
  [FileUploadStatus.UPLOADING]: 'Wird hochgeladen',
  [FileUploadStatus.COMPLETED]: 'Abgeschlossen',
  [FileUploadStatus.FAILED]: 'Fehlgeschlagen',
  [FileUploadStatus.CANCELLED]: 'Abgebrochen'
}

/**
 * File upload status colors
 */
export const FILE_UPLOAD_STATUS_COLORS: Record<FileUploadStatus, string> = {
  [FileUploadStatus.PENDING]: 'gray',
  [FileUploadStatus.UPLOADING]: 'blue',
  [FileUploadStatus.COMPLETED]: 'green',
  [FileUploadStatus.FAILED]: 'red',
  [FileUploadStatus.CANCELLED]: 'yellow'
}

/**
 * File validation error labels
 */
export const FILE_VALIDATION_ERROR_LABELS: Record<FileValidationError, string> = {
  [FileValidationError.SIZE_EXCEEDED]: 'Datei zu groß',
  [FileValidationError.TYPE_NOT_ALLOWED]: 'Dateityp nicht erlaubt',
  [FileValidationError.CORRUPTED]: 'Datei beschädigt',
  [FileValidationError.DIMENSIONS_INVALID]: 'Abmessungen ungültig',
  [FileValidationError.DURATION_INVALID]: 'Dauer ungültig',
  [FileValidationError.RESOLUTION_INVALID]: 'Auflösung ungültig'
}

/**
 * Default file upload options
 */
export const DEFAULT_FILE_UPLOAD_OPTIONS: FileUploadOptions = {
  maxFileSize: 10 * 1024 * 1024, // 10MB
  allowedTypes: [FileType.IMAGE, FileType.DOCUMENT],
  multiple: true,
  maxFiles: 10,
  chunkSize: 1024 * 1024, // 1MB
  parallelUploads: 3,
  autoUpload: true,
  showPreview: true,
  showProgress: true,
  showCancelButton: true,
  showRetryButton: true
}

/**
 * Common MIME types by file type
 */
export const COMMON_MIME_TYPES: Record<FileType, string[]> = {
  [FileType.IMAGE]: ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'],
  [FileType.DOCUMENT]: ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'application/rtf'],
  [FileType.VIDEO]: ['video/mp4', 'video/webm', 'video/ogg', 'video/quicktime'],
  [FileType.AUDIO]: ['audio/mpeg', 'audio/ogg', 'audio/wav', 'audio/webm'],
  [FileType.ARCHIVE]: ['application/zip', 'application/x-rar-compressed', 'application/x-tar', 'application/gzip'],
  [FileType.OTHER]: []
}

// ==================== API-SPECIFIC TYPES ====================

/**
 * API-specific upload response (snake_case from backend)
 */
export interface ApiUploadResponse {
  file_path: string
  url: string
  filename: string
  message: string
}

/**
 * API-specific upload options (snake_case for API requests)
 */
export interface ApiUploadOptions {
  type?: 'project' | 'hackathon' | 'avatar'
  max_size_mb?: number
}

/**
 * API-specific file metadata (snake_case from backend)
 */
export interface ApiFileMetadata {
  id: string
  name: string
  size: number
  type: string
  mime_type: string
  extension: string
  url: string
  thumbnail_url?: string | null
  dimensions?: {
    width: number
    height: number
  }
  duration?: number
  created_at: string
  updated_at: string
  uploaded_by: string
  entity_type: 'project' | 'hackathon' | 'team' | 'user' | 'comment'
  entity_id: string
  tags: string[]
  description?: string | null
  is_public: boolean
  metadata?: Record<string, any>
}