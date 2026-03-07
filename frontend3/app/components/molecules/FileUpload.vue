<template>
  <div class="file-upload">
    <!-- Drop zone -->
    <div
      ref="dropZoneRef"
      class="drop-zone"
      :class="dropZoneClasses"
      @click="triggerFileInput"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
    >
      <div class="drop-zone-content">
        <Icon
          v-if="icon"
          :name="icon"
          :size="iconSize"
          :is-svg="isSvgIcon"
          class="mb-3 text-gray-400"
        />
        
        <div v-if="!files.length" class="upload-prompt">
          <p class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            {{ promptText }}
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-400 mb-3">
            {{ descriptionText }}
          </p>
          <button
            type="button"
            class="px-4 py-2 text-sm font-medium rounded-md bg-primary-600 text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            @click.stop="triggerFileInput"
          >
            {{ buttonText }}
          </button>
        </div>

        <!-- File list -->
        <div v-if="files.length" class="file-list">
          <div class="space-y-2">
            <div
              v-for="file in files"
              :key="file.id"
              class="file-item"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center min-w-0 flex-1">
                  <Icon
                    :name="getFileIcon(file)"
                    :size="20"
                    :is-svg="true"
                    class="flex-shrink-0 mr-3 text-gray-400"
                  />
                  
                  <div class="min-w-0 flex-1">
                    <p class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                      {{ file.name }}
                    </p>
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                      {{ formatFileSize(file.size) }}
                    </p>
                  </div>
                </div>

                <div class="flex items-center space-x-2 ml-3">
                  <button
                    v-if="removable"
                    type="button"
                    class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                    @click.stop="removeFile(file.id)"
                    aria-label="Remove file"
                  >
                    <Icon
                      name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M6 18L18 6M6 6l12 12' /></svg>"
                      :size="16"
                      is-svg
                    />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Add more files button -->
          <div v-if="multiple" class="mt-4">
            <button
              type="button"
              class="w-full px-4 py-2 text-sm font-medium rounded-md border border-dashed border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              @click.stop="triggerFileInput"
            >
              Add more files
            </button>
          </div>
        </div>
      </div>

      <!-- Hidden file input -->
      <input
        ref="fileInputRef"
        type="file"
        :name="name"
        :multiple="multiple"
        :accept="accept"
        :disabled="disabled"
        @change="handleFileSelect"
        class="hidden"
      />
    </div>

    <!-- Error message -->
    <div v-if="error" class="mt-2 text-sm text-red-600">
      {{ error }}
    </div>

    <!-- Helper text -->
    <div v-if="helperText" class="mt-2 text-sm text-gray-500 dark:text-gray-400">
      {{ helperText }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Icon from '../atoms/Icon.vue'

export interface UploadFile {
  id: string
  file: File
  name: string
  size: number
  type: string
}

export interface FileUploadProps {
  /** Input name attribute */
  name?: string
  /** Current files */
  modelValue?: UploadFile[]
  /** Whether multiple files can be selected */
  multiple?: boolean
  /** Maximum number of files allowed */
  maxFiles?: number
  /** Maximum file size in bytes */
  maxSize?: number
  /** Accepted file types (e.g., 'image/*,.pdf') */
  accept?: string
  /** Whether the upload is disabled */
  disabled?: boolean
  /** Whether files can be removed */
  removable?: boolean
  /** Custom icon (SVG string) */
  icon?: string
  /** Icon size */
  iconSize?: number
  /** Whether icon is SVG */
  isSvgIcon?: boolean
  /** Prompt text */
  prompt?: string
  /** Description text */
  description?: string
  /** Button text */
  buttonText?: string
  /** Helper text */
  helperText?: string
  /** Error message */
  error?: string
}

const props = withDefaults(defineProps<FileUploadProps>(), {
  name: 'file',
  multiple: false,
  removable: true,
  icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>',
  iconSize: 48,
  isSvgIcon: true,
  prompt: 'Drag & drop files here',
  description: 'or click to browse',
  buttonText: 'Browse files',
})

const emit = defineEmits<{
  /** Emitted when files change */
  'update:modelValue': [files: UploadFile[]]
  /** Emitted when files are selected */
  select: [files: File[]]
  /** Emitted when file is removed */
  remove: [file: UploadFile]
}>()

// Refs
const fileInputRef = ref<HTMLInputElement>()
const dropZoneRef = ref<HTMLElement>()
const isDragging = ref(false)
const files = ref<UploadFile[]>(props.modelValue || [])

// Computed
const promptText = computed(() => {
  if (props.maxFiles && props.maxFiles > 1) {
    return `${props.prompt} (max ${props.maxFiles})`
  }
  return props.prompt
})

const descriptionText = computed(() => {
  if (props.maxSize) {
    const maxSizeMB = (props.maxSize / (1024 * 1024)).toFixed(1)
    return `${props.description} • Max size: ${maxSizeMB}MB`
  }
  return props.description
})

const dropZoneClasses = computed(() => {
  const classes = []
  
  if (isDragging.value) {
    classes.push('border-primary-500', 'bg-primary-50', 'dark:bg-primary-900/20')
  } else if (props.error) {
    classes.push('border-red-300', 'bg-red-50', 'dark:bg-red-900/20')
  } else if (props.disabled) {
    classes.push('border-gray-200', 'bg-gray-50', 'dark:bg-gray-800', 'cursor-not-allowed')
  } else {
    classes.push('border-gray-300', 'dark:border-gray-600', 'hover:border-primary-400')
  }
  
  if (props.disabled) {
    classes.push('opacity-60')
  }
  
  return classes
})

// Methods
const triggerFileInput = () => {
  if (props.disabled) return
  fileInputRef.value?.click()
}

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files?.length) return
  
  const selectedFiles = Array.from(input.files)
  processFiles(selectedFiles)
  
  // Reset input to allow selecting same file again
  input.value = ''
}

const handleDragOver = (event: DragEvent) => {
  if (props.disabled) return
  event.preventDefault()
  isDragging.value = true
}

const handleDragLeave = (event: DragEvent) => {
  if (props.disabled) return
  
  // Only set dragging to false if leaving the drop zone
  const relatedTarget = event.relatedTarget as Node
  if (!dropZoneRef.value?.contains(relatedTarget)) {
    isDragging.value = false
  }
}

const handleDrop = (event: DragEvent) => {
  if (props.disabled) return
  
  event.preventDefault()
  isDragging.value = false
  
  const droppedFiles = event.dataTransfer?.files
  if (!droppedFiles?.length) return
  
  const filesArray = Array.from(droppedFiles)
  processFiles(filesArray)
}

const processFiles = (fileList: File[]) => {
  // Check max files limit
  if (props.maxFiles && files.value.length + fileList.length > props.maxFiles) {
    return
  }
  
  const newUploadFiles: UploadFile[] = []
  
  for (const file of fileList) {
    // Check file size
    if (props.maxSize && file.size > props.maxSize) {
      continue
    }
    
    // Check file type if accept is specified
    if (props.accept && !isFileTypeAccepted(file, props.accept)) {
      continue
    }
    
    const uploadFile: UploadFile = {
      id: generateId(),
      file,
      name: file.name,
      size: file.size,
      type: file.type,
    }
    
    newUploadFiles.push(uploadFile)
  }
  
  if (!newUploadFiles.length) return
  
  // Add to files list
  const updatedFiles = [...files.value, ...newUploadFiles]
  files.value = updatedFiles
  emit('update:modelValue', updatedFiles)
  emit('select', newUploadFiles.map(f => f.file))
}

const isFileTypeAccepted = (file: File, accept: string): boolean => {
  if (!accept || accept === '*/*') return true
  
  const acceptTypes = accept.split(',').map(type => type.trim())
  
  for (const type of acceptTypes) {
    if (type.startsWith('.')) {
      // Extension check
      const extension = `.${file.name.split('.').pop()?.toLowerCase()}`
      if (extension === type.toLowerCase()) return true
    } else if (type.endsWith('/*')) {
      // MIME type wildcard check
      const mimePrefix = type.slice(0, -2)
      if (file.type.startsWith(mimePrefix)) return true
    } else {
      // Exact MIME type check
      if (file.type === type) return true
    }
  }
  
  return false
}

const getFileIcon = (file: UploadFile): string => {
  const type = file.type.toLowerCase()
  
  if (type.startsWith('image/')) {
    return '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>'
  } else if (type.startsWith('video/')) {
    return '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>'
  } else if (type.includes('pdf')) {
    return '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>'
  } else if (type.includes('zip') || type.includes('compressed')) {
    return '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8" /></svg>'
  } else {
    return '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>'
  }
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const generateId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substring(2)
}

const removeFile = (fileId: string) => {
  const fileIndex = files.value.findIndex(f => f.id === fileId)
  if (fileIndex === -1) return
  
  const removedFile = files.value[fileIndex]
  const updatedFiles = files.value.filter(f => f.id !== fileId)
  
  files.value = updatedFiles
  emit('update:modelValue', updatedFiles)
  
  if (removedFile) {
    emit('remove', removedFile)
  }
}
</script>

<style scoped>
.file-upload {
  width: 100%;
}

.drop-zone {
  border: 2px dashed;
  border-radius: 0.5rem;
  padding: 2rem;
  text-align: center;
  transition: all 0.2s ease;
  cursor: pointer;
}

.drop-zone:hover:not(.disabled) {
  border-color: var(--primary-400);
}

.drop-zone.is-dragging {
  border-color: var(--primary-500);
  background-color: var(--primary-50);
}

.drop-zone.has-error {
  border-color: var(--red-300);
  background-color: var(--red-50);
}

.drop-zone.disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.upload-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.file-list {
  width: 100%;
}

.file-item {
  padding: 0.75rem;
  border: 1px solid var(--gray-200);
  border-radius: 0.375rem;
  background-color: white;
  transition: all 0.2s ease;
}

.file-item:hover {
  border-color: var(--gray-300);
  background-color: var(--gray-50);
}

@media (prefers-color-scheme: dark) {
  .file-item {
    border-color: var(--gray-700);
    background-color: var(--gray-800);
  }
  
  .file-item:hover {
    border-color: var(--gray-600);
    background-color: var(--gray-700);
  }
}
</style>