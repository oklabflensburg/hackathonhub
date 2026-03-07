<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
    <div class="container mx-auto px-4 max-w-6xl">
      <!-- Header -->
      <header class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
              {{ isEditMode ? 'Hackathon bearbeiten' : 'Neuen Hackathon erstellen' }}
            </h1>
            <p class="text-gray-600 dark:text-gray-400 mt-1">
              {{ isEditMode ? 'Aktualisiere die Details deines Hackathons' : 'Erstelle einen neuen Hackathon und lade Teilnehmer ein' }}
            </p>
          </div>
          
          <div class="flex items-center gap-3">
            <Button
              variant="outline"
              @click="emit('cancel')"
            >
              Abbrechen
            </Button>
            <Button
              variant="primary"
              :loading="submitting"
              @click="handleSubmit"
            >
              {{ isEditMode ? 'Speichern' : 'Hackathon erstellen' }}
            </Button>
          </div>
        </div>
      </header>

      <!-- Main Form -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column - Main Form -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Basic Information Card -->
          <Card class="p-6">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Grundinformationen
            </h2>
            
            <div class="space-y-4">
              <!-- Title -->
              <FormField label="Titel" required>
                <Input
                  v-model="formData.title"
                  placeholder="z.B. AI Innovation Challenge 2026"
                  :error="errors.title"
                  @input="clearError('title')"
                />
                <template #hint>
                  Wähle einen aussagekräftigen Titel für deinen Hackathon
                </template>
              </FormField>

              <!-- Description -->
              <FormField label="Beschreibung" required>
                <Textarea
                  v-model="formData.description"
                  placeholder="Beschreibe deinen Hackathon, Ziele, Themen und Erwartungen..."
                  rows="4"
                  :error="errors.description"
                  @input="clearError('description')"
                />
                <template #hint>
                  Markdown wird unterstützt. Beschreibe detailliert, worum es geht.
                </template>
              </FormField>

              <!-- Tags -->
              <FormField label="Tags">
                <div class="space-y-2">
                  <Input
                    v-model="tagInput"
                    placeholder="z.B. AI, Web3, Sustainability"
                    @keydown.enter="addTag"
                  />
                  <div class="flex flex-wrap gap-2 mt-2">
                    <Badge
                      v-for="tag in formData.tags"
                      :key="tag"
                      variant="neutral"
                      size="sm"
                      closable
                      @close="removeTag(tag)"
                    >
                      {{ tag }}
                    </Badge>
                  </div>
                </div>
                <template #hint>
                  Tags helfen Teilnehmern, deinen Hackathon zu finden
                </template>
              </FormField>
            </div>
          </Card>

          <!-- Date & Location Card -->
          <Card class="p-6">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Zeitraum und Ort
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Start Date -->
              <FormField label="Startdatum" required>
                <Input
                  v-model="formData.startDate"
                  type="datetime-local"
                  :error="errors.startDate"
                  @input="clearError('startDate')"
                />
              </FormField>

              <!-- End Date -->
              <FormField label="Enddatum" required>
                <Input
                  v-model="formData.endDate"
                  type="datetime-local"
                  :error="errors.endDate"
                  @input="clearError('endDate')"
                />
              </FormField>

              <!-- Location Type -->
              <FormField label="Veranstaltungsart" required>
                <Select
                  v-model="formData.locationType"
                  :error="errors.locationType"
                  @change="clearError('locationType')"
                >
                  <option value="virtual">Virtual</option>
                  <option value="physical">Vor Ort</option>
                  <option value="hybrid">Hybrid</option>
                </Select>
              </FormField>

              <!-- Location Details -->
              <FormField
                :label="locationLabel"
                :required="formData.locationType !== 'virtual'"
              >
                <Input
                  v-model="formData.location"
                  :placeholder="locationPlaceholder"
                  :error="errors.location"
                  @input="clearError('location')"
                />
              </FormField>
            </div>
          </Card>

          <!-- Prizes & Rules Card -->
          <Card class="p-6">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Preise und Regeln
            </h2>
            
            <div class="space-y-4">
              <!-- Prizes -->
              <FormField label="Preise">
                <div class="space-y-3">
                  <div
                    v-for="(prize, index) in formData.prizes"
                    :key="index"
                    class="flex items-center gap-3"
                  >
                    <Input
                      v-model="formData.prizes[index]"
                      :placeholder="`Preis ${index + 1} (z.B. €1000)`"
                      class="flex-1"
                    />
                    <Button
                      variant="ghost"
                      size="sm"
                      @click="removePrize(index)"
                      :disabled="formData.prizes.length <= 1"
                    >
                      <Icon name="trash-2" class="w-4 h-4" />
                    </Button>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    @click="addPrize"
                  >
                    <Icon name="plus" class="w-4 h-4 mr-2" />
                    Preis hinzufügen
                  </Button>
                </div>
              </FormField>

              <!-- Rules -->
              <FormField label="Regeln">
                <div class="space-y-3">
                  <div
                    v-for="(rule, index) in formData.rules"
                    :key="index"
                    class="flex items-center gap-3"
                  >
                    <Input
                      v-model="formData.rules[index]"
                      :placeholder="`Regel ${index + 1}`"
                      class="flex-1"
                    />
                    <Button
                      variant="ghost"
                      size="sm"
                      @click="removeRule(index)"
                      :disabled="formData.rules.length <= 1"
                    >
                      <Icon name="trash-2" class="w-4 h-4" />
                    </Button>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    @click="addRule"
                  >
                    <Icon name="plus" class="w-4 h-4 mr-2" />
                    Regel hinzufügen
                  </Button>
                </div>
              </FormField>
            </div>
          </Card>
        </div>

        <!-- Right Column - Sidebar -->
        <div class="space-y-6">
          <!-- Status & Visibility Card -->
          <Card class="p-6">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Status & Sichtbarkeit
            </h2>
            
            <div class="space-y-4">
              <!-- Status -->
              <FormField label="Status">
                <Select v-model="formData.status">
                  <option value="draft">Entwurf</option>
                  <option value="published">Veröffentlicht</option>
                  <option value="private">Privat</option>
                </Select>
              </FormField>

              <!-- Max Participants -->
              <FormField label="Maximale Teilnehmer">
                <Input
                  v-model="formData.maxParticipants"
                  type="number"
                  min="0"
                  placeholder="Unbegrenzt (leer lassen)"
                />
              </FormField>

              <!-- Registration Deadline -->
              <FormField label="Anmeldefrist">
                <Input
                  v-model="formData.registrationDeadline"
                  type="datetime-local"
                />
              </FormField>
            </div>
          </Card>

          <!-- Image Upload Card -->
          <Card class="p-6">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Hackathon-Bild
            </h2>
            
            <FileUpload
              v-model="formData.image"
              accept="image/*"
              :max-size="5242880"
              :preview="true"
              @error="handleUploadError"
            />
            
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-3">
              Empfohlene Größe: 1200×600px. Max. 5MB.
            </p>
          </Card>

          <!-- Preview Card -->
          <Card class="p-6">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Vorschau
            </h2>
            
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-gray-600 dark:text-gray-400">Titel:</span>
                <span class="font-medium text-gray-900 dark:text-white truncate max-w-[150px]">
                  {{ formData.title || '(Kein Titel)' }}
                </span>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-gray-600 dark:text-gray-400">Zeitraum:</span>
                <span class="font-medium text-gray-900 dark:text-white">
                  {{ formatDateRange(formData.startDate, formData.endDate) }}
                </span>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-gray-600 dark:text-gray-400">Ort:</span>
                <span class="font-medium text-gray-900 dark:text-white">
                  {{ formatLocation(formData.locationType, formData.location) }}
                </span>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-gray-600 dark:text-gray-400">Preise:</span>
                <span class="font-medium text-gray-900 dark:text-white">
                  {{ formData.prizes.length }}
                </span>
              </div>
            </div>
          </Card>

          <!-- Actions Card -->
          <Card class="p-6">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Aktionen
            </h2>
            
            <div class="space-y-3">
              <Button
                variant="outline"
                class="w-full justify-center"
                @click="emit('preview')"
                :disabled="!formData.title"
              >
                <Icon name="eye" class="w-4 h-4 mr-2" />
                Vorschau anzeigen
              </Button>
              
              <Button
                variant="outline"
                class="w-full justify-center"
                @click="handleSaveDraft"
                :loading="savingDraft"
              >
                <Icon name="save" class="w-4 h-4 mr-2" />
                Als Entwurf speichern
              </Button>
              
              <Button
                variant="ghost"
                class="w-full justify-center text-red-600 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20"
                @click="emit('delete')"
                v-if="isEditMode"
              >
                <Icon name="trash-2" class="w-4 h-4 mr-2" />
                Hackathon löschen
              </Button>
            </div>
          </Card>
        </div>
      </div>

      <!-- Form Actions Footer -->
      <footer class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
        <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div class="text-sm text-gray-500 dark:text-gray-400">
            <p v-if="lastSaved">
              Zuletzt gespeichert: {{ formatLastSaved(lastSaved) }}
            </p>
            <p v-else>
              Noch nicht gespeichert
            </p>
          </div>
          
          <div class="flex items-center gap-3">
            <Button
              variant="outline"
              @click="emit('cancel')"
            >
              Abbrechen
            </Button>
            <Button
              variant="primary"
              :loading="submitting"
              @click="handleSubmit"
              :disabled="!isFormValid"
            >
              {{ isEditMode ? 'Änderungen speichern' : 'Hackathon veröffentlichen' }}
            </Button>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { format } from 'date-fns'
import { de } from 'date-fns/locale'
import Icon from '~/components/atoms/Icon.vue'
import Button from '~/components/atoms/Button.vue'

interface FormData {
  title: string
  description: string
  tags: string[]
  startDate: string
  endDate: string
  locationType: 'virtual' | 'physical' | 'hybrid'
  location: string
  prizes: string[]
  rules: string[]
  status: 'draft' | 'published' | 'private'
  maxParticipants: string
  registrationDeadline: string
  image: File | string | null
}

interface Props {
  initialData?: Partial<FormData>
  isEditMode?: boolean
  submitting?: boolean
  savingDraft?: boolean
  lastSaved?: Date | string | null
  errors?: Record<string, string>
}

interface Emits {
  (e: 'submit', data: FormData): void
  (e: 'save-draft', data: FormData): void
  (e: 'cancel'): void
  (e: 'preview'): void
  (e: 'delete'): void
  (e: 'update:modelValue', data: Partial<FormData>): void
}

const props = withDefaults(defineProps<Props>(), {
  initialData: () => ({}),
  isEditMode: false,
  submitting: false,
  savingDraft: false,
  lastSaved: null,
  errors: () => ({})
})

const emit = defineEmits<Emits>()

// Form data
const formData = ref<FormData>({
  title: props.initialData.title || '',
  description: props.initialData.description || '',
  tags: props.initialData.tags || [],
  startDate: props.initialData.startDate || '',
  endDate: props.initialData.endDate || '',
  locationType: props.initialData.locationType || 'virtual',
  location: props.initialData.location || '',
  prizes: props.initialData.prizes || [''],
  rules: props.initialData.rules || [''],
  status: props.initialData.status || 'draft',
  maxParticipants: props.initialData.maxParticipants || '',
  registrationDeadline: props.initialData.registrationDeadline || '',
  image: props.initialData.image || null
})

const tagInput = ref('')
const errors = ref<Record<string, string>>({ ...props.errors })

// Computed properties
const locationLabel = computed(() => {
  switch (formData.value.locationType) {
    case 'virtual':
      return 'Virtueller Link (optional)'
    case 'physical':
      return 'Adresse'
    case 'hybrid':
      return 'Adresse & Virtueller Link'
    default:
      return 'Ort'
  }
})

const locationPlaceholder = computed(() => {
  switch (formData.value.locationType) {
    case 'virtual':
      return 'https://meet.example.com/hackathon'
    case 'physical':
      return 'Musterstraße 123, 10115 Berlin'
    case 'hybrid':
      return 'Adresse und/oder Link'
    default:
      return ''
  }
})

const isFormValid = computed(() => {
  return (
    formData.value.title.trim().length > 0 &&
    formData.value.description.trim().length > 0 &&
    formData.value.startDate &&
    formData.value.endDate &&
    formData.value.locationType
  )
})

// Methods
function addTag() {
  const tag = tagInput.value.trim()
  if (tag && !formData.value.tags.includes(tag)) {
    formData.value.tags.push(tag)
    tagInput.value = ''
  }
}

function removeTag(tag: string) {
  formData.value.tags = formData.value.tags.filter(t => t !== tag)
}

function addPrize() {
  formData.value.prizes.push('')
}

function removePrize(index: number) {
  if (formData.value.prizes.length > 1) {
    formData.value.prizes.splice(index, 1)
  }
}

function addRule() {
  formData.value.rules.push('')
}

function removeRule(index: number) {
  if (formData.value.rules.length > 1) {
    formData.value.rules.splice(index, 1)
  }
}

function handleSubmit() {
  if (isFormValid.value) {
    emit('submit', formData.value)
  } else {
    // Set validation errors
    errors.value = {
      title: !formData.value.title.trim() ? 'Titel ist erforderlich' : '',
      description: !formData.value.description.trim() ? 'Beschreibung ist erforderlich' : '',
      startDate: !formData.value.startDate ? 'Startdatum ist erforderlich' : '',
      endDate: !formData.value.endDate ? 'Enddatum ist erforderlich' : '',
      locationType: !formData.value.locationType ? 'Veranstaltungsart ist erforderlich' : ''
    }
  }
}

function handleSaveDraft() {
  emit('save-draft', formData.value)
}

function handleUploadError(error: string) {
  console.error('Upload error:', error)
  // Could show an alert or set an error state
}

function clearError(field: string) {
  if (errors.value[field]) {
    errors.value[field] = ''
  }
}

function formatDateRange(start: string, end: string): string {
  if (!start || !end) return 'Nicht festgelegt'
  
  try {
    const startDate = new Date(start)
    const endDate = new Date(end)
    return `${format(startDate, 'dd.MM.yyyy')} - ${format(endDate, 'dd.MM.yyyy')}`
  } catch {
    return 'Ungültiges Datum'
  }
}

function formatLocation(type: string, location: string): string {
  if (type === 'virtual') return 'Virtual'
  if (type === 'physical' && location) return location
  if (type === 'hybrid' && location) return 'Hybrid: ' + location
  return 'Nicht angegeben'
}

function formatLastSaved(date: Date | string): string {
  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date
    return format(dateObj, 'dd.MM.yyyy HH:mm', { locale: de })
  } catch {
    return 'Unbekannt'
  }
}

// Watch for external error updates
watch(() => props.errors, (newErrors) => {
  errors.value = { ...newErrors }
}, { deep: true })

// Emit updates when form data changes
watch(formData, (newData) => {
  emit('update:modelValue', newData)
}, { deep: true })
</script>