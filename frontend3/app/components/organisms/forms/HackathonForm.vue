<template>
  <form @submit.prevent="$emit('submit', formData)" class="space-y-6">
    <!-- Hackathon Name -->
    <FormField :label="nameLabel" :required="true" :error="errors.name">
      <Input
        v-model="formData.name"
        type="text"
        :placeholder="namePlaceholder"
        :error="!!errors.name"
        required
      />
    </FormField>

    <!-- Description -->
    <FormField :label="descriptionLabel" :required="true" :error="errors.description">
      <textarea
        v-model="formData.description"
        rows="4"
        class="input"
        :placeholder="descriptionPlaceholder"
        :class="{ 'input-error': errors.description }"
        required
      />
    </FormField>

    <!-- Organization -->
    <FormField :label="organizerLabel" :required="true" :error="errors.organization">
      <Input
        v-model="formData.organization"
        type="text"
        :placeholder="organizerPlaceholder"
        :error="!!errors.organization"
        required
      />
    </FormField>

    <!-- Dates -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <FormField :label="startDateLabel" :required="true" :error="errors.startDate">
        <Input
          v-model="formData.startDate"
          type="datetime-local"
          :error="!!errors.startDate"
          required
        />
      </FormField>
      <FormField :label="endDateLabel" :required="true" :error="errors.endDate">
        <Input
          v-model="formData.endDate"
          type="datetime-local"
          :error="!!errors.endDate"
          required
        />
      </FormField>
    </div>

    <!-- Location -->
    <FormField :label="locationLabel" :required="true" :error="errors.locationType">
      <div class="flex space-x-4">
        <label class="flex items-center">
          <input
            v-model="formData.locationType"
            type="radio"
            value="online"
            class="mr-2"
            :disabled="disabled"
          />
          <span class="text-gray-700 dark:text-gray-300">{{ onlineText }}</span>
        </label>
        <label class="flex items-center">
          <input
            v-model="formData.locationType"
            type="radio"
            value="in-person"
            class="mr-2"
            :disabled="disabled"
          />
          <span class="text-gray-700 dark:text-gray-300">{{ inPersonText }}</span>
        </label>
      </div>
      <Input
        v-if="formData.locationType === 'in-person'"
        v-model="formData.location"
        type="text"
        :placeholder="locationPlaceholder"
        :error="!!errors.location"
        class="mt-3"
        required
      />
    </FormField>

    <!-- Prize Pool -->
    <FormField :label="prizePoolLabel" :error="errors.prizePool">
      <Input
        v-model="formData.prizePool"
        type="text"
        :placeholder="prizePoolPlaceholder"
        :error="!!errors.prizePool"
        :disabled="disabled"
      />
    </FormField>

    <!-- Tags -->
    <FormField :label="tagsLabel">
      <div class="flex flex-wrap gap-2 mb-2">
        <Tag
          v-for="tag in formData.tags"
          :key="tag"
          :closable="!disabled"
          @close="removeTag(tag)"
          variant="primary"
        >
          {{ tag }}
        </Tag>
      </div>
      <div class="flex">
        <Input
          v-model="newTag"
          type="text"
          :placeholder="tagsPlaceholder"
          :disabled="disabled"
          class="rounded-r-none"
          @keydown.enter.prevent="addTag"
        />
        <Button
          type="button"
          @click="addTag"
          variant="primary"
          class="rounded-l-none"
          :disabled="disabled || !newTag.trim()"
        >
          {{ addText }}
        </Button>
      </div>
    </FormField>

    <!-- Rules & Guidelines -->
    <FormField :label="rulesLabel" :error="errors.rules">
      <textarea
        v-model="formData.rules"
        rows="4"
        class="input"
        :placeholder="rulesPlaceholder"
        :class="{ 'input-error': errors.rules }"
        :disabled="disabled"
      />
    </FormField>

    <!-- Image Upload -->
    <FormField :label="hackathonImageLabel">
      <div
        @click="triggerImageUpload"
        class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center cursor-pointer hover:border-primary-500 dark:hover:border-primary-400 transition-colors"
        :class="{ 'border-primary-500 dark:border-primary-400': formData.image_url }"
      >
        <div v-if="!formData.image_url">
          <svg class="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            {{ clickToUploadText }}
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">
            {{ imageRequirementsText }}
          </p>
        </div>
        <div v-else class="space-y-2">
          <div class="w-32 h-32 mx-auto rounded-lg overflow-hidden">
            <img :src="formData.image_url" :alt="imageAltText" class="w-full h-full object-cover" />
          </div>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            {{ imageUploadedText }}
          </p>
          <Button
            type="button"
            @click.stop="$emit('remove-image')"
            variant="ghost"
            size="sm"
            class="text-red-600 dark:text-red-400"
            :disabled="disabled"
          >
            {{ removeImageText }}
          </Button>
        </div>
        <input
          ref="imageInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="$emit('image-upload', $event)"
        />
      </div>
    </FormField>

    <!-- Contact Information -->
    <FormField :label="contactEmailLabel" :required="true" :error="errors.contactEmail">
      <Input
        v-model="formData.contactEmail"
        type="email"
        :placeholder="emailPlaceholder"
        :error="!!errors.contactEmail"
        required
        :disabled="disabled"
      />
    </FormField>

    <!-- Submit & Reset Buttons -->
    <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
      <Button
        type="button"
        @click="$emit('reset')"
        variant="secondary"
        :disabled="disabled"
      >
        {{ resetText }}
      </Button>
      <Button
        type="submit"
        :loading="submitting"
        :disabled="disabled"
        variant="primary"
      >
        {{ submitText }}
      </Button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import FormField from '@/components/molecules/FormField.vue'
import Input from '@/components/atoms/Input.vue'
import Button from '@/components/atoms/Button.vue'
import Tag from '@/components/atoms/Tag.vue'

// Props
interface HackathonFormData {
  name: string
  description: string
  organization: string
  startDate: string
  endDate: string
  locationType: 'online' | 'in-person'
  location: string
  prizePool: string
  tags: string[]
  rules: string
  contactEmail: string
  image_url: string
}

interface Props {
  // Form data
  modelValue: HackathonFormData
  // States
  submitting?: boolean
  disabled?: boolean
  errors?: Record<string, string>
  // Labels
  nameLabel?: string
  namePlaceholder?: string
  descriptionLabel?: string
  descriptionPlaceholder?: string
  organizerLabel?: string
  organizerPlaceholder?: string
  startDateLabel?: string
  endDateLabel?: string
  locationLabel?: string
  onlineText?: string
  inPersonText?: string
  locationPlaceholder?: string
  prizePoolLabel?: string
  prizePoolPlaceholder?: string
  tagsLabel?: string
  tagsPlaceholder?: string
  addText?: string
  rulesLabel?: string
  rulesPlaceholder?: string
  hackathonImageLabel?: string
  clickToUploadText?: string
  imageRequirementsText?: string
  imageAltText?: string
  imageUploadedText?: string
  removeImageText?: string
  contactEmailLabel?: string
  emailPlaceholder?: string
  resetText?: string
  submitText?: string
}

const props = withDefaults(defineProps<Props>(), {
  submitting: false,
  disabled: false,
  errors: () => ({}),
  nameLabel: 'Hackathon Name',
  namePlaceholder: 'Enter hackathon name',
  descriptionLabel: 'Description',
  descriptionPlaceholder: 'Describe your hackathon...',
  organizerLabel: 'Organizer',
  organizerPlaceholder: 'Organization or company name',
  startDateLabel: 'Start Date',
  endDateLabel: 'End Date',
  locationLabel: 'Location',
  onlineText: 'Online',
  inPersonText: 'In-person',
  locationPlaceholder: 'Enter location (city, venue, etc.)',
  prizePoolLabel: 'Prize Pool',
  prizePoolPlaceholder: 'e.g., $10,000',
  tagsLabel: 'Tags',
  tagsPlaceholder: 'Add a tag',
  addText: 'Add',
  rulesLabel: 'Rules & Guidelines',
  rulesPlaceholder: 'Add rules and guidelines for participants...',
  hackathonImageLabel: 'Hackathon Image',
  clickToUploadText: 'Click to upload image',
  imageRequirementsText: 'PNG, JPG, GIF up to 5MB',
  imageAltText: 'Hackathon preview',
  imageUploadedText: 'Image uploaded',
  removeImageText: 'Remove Image',
  contactEmailLabel: 'Contact Email',
  emailPlaceholder: 'contact@example.com',
  resetText: 'Reset',
  submitText: 'Create Hackathon'
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: HackathonFormData]
  'submit': [data: HackathonFormData]
  'reset': []
  'image-upload': [event: Event]
  'remove-image': []
}>()

// Local state
const newTag = ref('')
const formData = ref({ ...props.modelValue })
const imageInput = ref<HTMLInputElement | null>(null)
let isUpdatingFromParent = false

// Watch for prop changes
watch(() => props.modelValue, (newValue) => {
  isUpdatingFromParent = true
  formData.value = { ...newValue }
  // Use nextTick to reset flag after potential emit from formData watch
  nextTick(() => {
    isUpdatingFromParent = false
  })
}, { deep: true })

// Emit updates
watch(formData, (newValue, oldValue) => {
  if (isUpdatingFromParent) return
  // Prevent infinite loop by checking if value actually changed
  if (JSON.stringify(newValue) !== JSON.stringify(oldValue)) {
    emit('update:modelValue', newValue)
  }
}, { deep: true })

// Methods
const addTag = () => {
  if (newTag.value.trim() && !formData.value.tags.includes(newTag.value.trim())) {
    formData.value.tags.push(newTag.value.trim())
    newTag.value = ''
  }
}

const removeTag = (tag: string) => {
  if (props.disabled) return
  formData.value.tags = formData.value.tags.filter(t => t !== tag)
}

const triggerImageUpload = () => {
  if (props.disabled) return
  imageInput.value?.click()
}
</script>

<style scoped>
.input {
  @apply w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors;
}

.input-error {
  @apply border-red-500 dark:border-red-500 focus:ring-red-500;
}

.label {
  @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2;
}

.card {
  @apply bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6;
}
</style>