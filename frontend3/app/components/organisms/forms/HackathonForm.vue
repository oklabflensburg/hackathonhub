<template>
  <form @submit.prevent="$emit('submit', formData)" class="space-y-6">
    <!-- Hackathon Name -->
    <FormField :label="t('create.hackathonForm.fields.hackathonName')" :required="true" :error="errors.name">
      <Input
        v-model="formData.name"
        type="text"
        :placeholder="t('create.hackathonForm.fields.namePlaceholder')"
        :error="!!errors.name"
        required
      />
    </FormField>

    <!-- Description -->
    <FormField :label="t('create.hackathonForm.fields.description')" :required="true" :error="errors.description">
      <textarea
        v-model="formData.description"
        rows="4"
        class="input"
        :placeholder="t('create.hackathonForm.fields.descriptionPlaceholder')"
        :class="{ 'input-error': errors.description }"
        required
      />
    </FormField>

    <!-- Organization -->
    <FormField :label="t('create.hackathonForm.fields.organizer')" :required="true" :error="errors.organization">
      <Input
        v-model="formData.organization"
        type="text"
        :placeholder="t('create.hackathonForm.fields.organizerPlaceholder')"
        :error="!!errors.organization"
        required
      />
    </FormField>

    <!-- Dates -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <FormField :label="t('create.hackathonForm.fields.startDate')" :required="true" :error="errors.startDate">
        <Input
          v-model="formData.startDate"
          type="datetime-local"
          :error="!!errors.startDate"
          required
        />
      </FormField>
      <FormField :label="t('create.hackathonForm.fields.endDate')" :required="true" :error="errors.endDate">
        <Input
          v-model="formData.endDate"
          type="datetime-local"
          :error="!!errors.endDate"
          required
        />
      </FormField>
    </div>

    <!-- Location -->
    <FormField :label="t('create.hackathonForm.fields.location')" :required="true" :error="errors.locationType">
      <div class="flex space-x-4">
        <label class="flex items-center">
          <input
            v-model="formData.locationType"
            type="radio"
            value="online"
            class="mr-2"
            :disabled="disabled"
          />
          <span class="text-gray-700 dark:text-gray-300">{{ t('hackathons.filters.online') }}</span>
        </label>
        <label class="flex items-center">
          <input
            v-model="formData.locationType"
            type="radio"
            value="in-person"
            class="mr-2"
            :disabled="disabled"
          />
          <span class="text-gray-700 dark:text-gray-300">{{ t('hackathons.filters.inPerson') }}</span>
        </label>
      </div>
      <Input
        v-if="formData.locationType === 'in-person'"
        v-model="formData.location"
        type="text"
        :placeholder="t('create.hackathonForm.fields.locationPlaceholder')"
        :error="!!errors.location"
        class="mt-3"
        required
      />
    </FormField>

    <!-- Prize Pool -->
    <FormField :label="t('create.hackathonForm.fields.prizePool')" :error="errors.prizePool">
      <Input
        v-model="formData.prizePool"
        type="text"
        :placeholder="t('create.hackathonForm.fields.prizePoolPlaceholder')"
        :error="!!errors.prizePool"
        :disabled="disabled"
      />
    </FormField>

    <!-- Prizes -->
    <FormField :label="t('hackathons.details.prizes')" :error="errors.prizes">
      <div class="space-y-3">
        <div v-for="(prize, index) in formData.prizes" :key="index"
          class="p-3 border border-gray-300 dark:border-gray-600 rounded-lg">
          <div class="flex justify-between items-start mb-2">
            <span class="font-medium text-gray-700 dark:text-gray-300">{{ t('hackathons.details.prizeNumber', {
              number: Number(index) + 1 }) }}</span>
            <button type="button" @click="removePrize(index)"
              class="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300"
              :disabled="disabled">
              {{ t('hackathons.details.remove') }}
            </button>
          </div>

          <div class="space-y-2">
            <div>
              <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">{{
                t('hackathons.details.prizeName') }}</label>
              <input v-model="prize.name" type="text"
                :placeholder="t('hackathons.details.prizeNamePlaceholder')"
                class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                :disabled="disabled" />
            </div>
            <div>
              <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">{{ t('common.description')
                }}</label>
              <input v-model="prize.description" type="text"
                :placeholder="t('hackathons.details.prizeDescriptionPlaceholder')"
                class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                :disabled="disabled" />
            </div>
            <div>
              <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">{{
                t('hackathons.details.value') }}</label>
              <input v-model="prize.value" type="text"
                :placeholder="t('hackathons.details.prizeAmountPlaceholder')"
                class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                :disabled="disabled" />
            </div>
          </div>
        </div>

        <div v-if="formData.prizes.length === 0"
          class="text-center py-4 text-gray-500 dark:text-gray-400 border border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
          {{ t('hackathons.details.noPrizesAdded') }}
        </div>

        <Button type="button" @click="addPrize" variant="secondary" size="sm" :disabled="disabled" class="w-full">
          + {{ t('hackathons.details.addPrize') }}
        </Button>
      </div>
    </FormField>

    <!-- Organizers -->
    <FormField :label="t('hackathons.details.organizers')" :error="errors.organizers">
      <div class="space-y-3">
        <div v-for="(organizer, index) in formData.organizers" :key="index"
          class="p-3 border border-gray-300 dark:border-gray-600 rounded-lg">
          <div class="flex justify-between items-start mb-2">
            <span class="font-medium text-gray-700 dark:text-gray-300">{{
              t('hackathons.details.organizerNumber', { number: Number(index) + 1 }) }}</span>
            <button type="button" @click="removeOrganizer(index)"
              class="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300"
              :disabled="disabled">
              {{ t('hackathons.details.remove') }}
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div>
              <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">{{
                t('hackathons.details.name') }}</label>
              <input v-model="organizer.name" type="text"
                :placeholder="t('hackathons.details.organizerNamePlaceholder')"
                class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                :disabled="disabled" />
            </div>
            <div>
              <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">{{
                t('hackathons.details.role') }}</label>
              <input v-model="organizer.role" type="text"
                :placeholder="t('hackathons.details.organizerRolePlaceholder')"
                class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                :disabled="disabled" />
            </div>
          </div>
        </div>

        <div v-if="formData.organizers.length === 0"
          class="text-center py-4 text-gray-500 dark:text-gray-400 border border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
          {{ t('hackathons.details.noOrganizersAdded') }}
        </div>

        <Button type="button" @click="addOrganizer" variant="secondary" size="sm" :disabled="disabled" class="w-full">
          + {{ t('hackathons.details.addOrganizer') }}
        </Button>
      </div>
    </FormField>

    <!-- Tags -->
    <FormField :label="t('create.hackathonForm.fields.tags')">
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
          :placeholder="t('create.hackathonForm.fields.tagsPlaceholder')"
          :disabled="disabled"
          class="rounded-r-none flex-1"
          @keydown.enter.prevent="addTag"
        />
        <Button
          type="button"
          @click.prevent="addTag"
          variant="primary"
          class="rounded-l-none"
          :disabled="disabled || !newTag.trim()"
        >
          {{ t('create.hackathonForm.fields.add') }}
        </Button>
      </div>
    </FormField>

    <!-- Rules & Guidelines -->
    <FormField :label="t('create.hackathonForm.fields.rules')" :error="errors.rules">
      <textarea
        v-model="formData.rules"
        rows="4"
        class="input"
        :placeholder="t('create.hackathonForm.fields.rulesPlaceholder')"
        :class="{ 'input-error': errors.rules }"
        :disabled="disabled"
      />
    </FormField>

    <!-- Image Upload -->
    <FormField :label="t('create.hackathonForm.fields.hackathonImage')">
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
            {{ t('create.hackathonForm.fields.clickToUpload') }}
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">
            {{ t('create.hackathonForm.fields.imageRequirements') }}
          </p>
        </div>
        <div v-else class="space-y-2">
          <div class="w-32 h-32 mx-auto rounded-lg overflow-hidden">
            <img :src="formData.image_url" :alt="t('create.hackathonForm.fields.imageAlt')" class="w-full h-full object-cover" />
          </div>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            {{ t('create.hackathonForm.fields.imageUploaded') }}
          </p>
          <Button
            type="button"
            @click.stop="$emit('remove-image')"
            variant="ghost"
            size="sm"
            class="text-red-600 dark:text-red-400"
            :disabled="disabled"
          >
            {{ t('create.hackathonForm.fields.removeImage') }}
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
    <FormField :label="t('create.hackathonForm.fields.contactEmail')" :required="true" :error="errors.contactEmail">
      <Input
        v-model="formData.contactEmail"
        type="email"
        :placeholder="t('create.hackathonForm.fields.emailPlaceholder')"
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
        {{ t('create.projectForm.buttons.reset') }}
      </Button>
      <Button
        type="submit"
        :loading="submitting"
        :disabled="disabled"
        variant="primary"
      >
        {{ t('create.hackathonForm.buttons.submit') }}
      </Button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import FormField from '@/components/molecules/FormField.vue'
import Input from '@/components/atoms/Input.vue'
import Button from '@/components/atoms/Button.vue'
import Tag from '@/components/atoms/Tag.vue'

// Props
interface Prize {
  name: string
  description: string
  value: string
}

interface Organizer {
  name: string
  role: string
}

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
  prizes: Prize[]
  organizers: Organizer[]
}

interface Props {
  // Form data
  modelValue: HackathonFormData
  // States
  submitting?: boolean
  disabled?: boolean
  errors?: Record<string, string>
}

const props = withDefaults(defineProps<Props>(), {
  submitting: false,
  disabled: false,
  errors: () => ({})
})

const { t } = useI18n()

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
const formData = ref({
  ...props.modelValue,
  prizes: props.modelValue.prizes || [],
  organizers: props.modelValue.organizers || []
})
const imageInput = ref<HTMLInputElement | null>(null)
let isUpdatingFromParent = false

// Watch for prop changes
watch(() => props.modelValue, (newValue) => {
  console.log('Parent modelValue changed:', newValue)
  isUpdatingFromParent = true
  // Create a deep copy to avoid sharing references, especially for arrays
  formData.value = {
    ...newValue,
    tags: [...newValue.tags]
  }
  // Use nextTick to reset flag after potential emit from formData watch
  nextTick(() => {
    isUpdatingFromParent = false
  })
}, { deep: true })

// Emit updates
watch(formData, (newValue, oldValue) => {
  if (isUpdatingFromParent) {
    console.log('Skipping emit because update is from parent')
    return
  }
  // Prevent infinite loop by checking if value actually changed
  if (JSON.stringify(newValue) !== JSON.stringify(oldValue)) {
    console.log('formData changed, emitting update:', newValue)
    emit('update:modelValue', newValue)
  } else {
    console.log('formData changed but identical, skipping emit')
  }
}, { deep: true })

// Debug: log tags changes
watch(() => formData.value.tags, (newTags, oldTags) => {
  console.log('Tags changed:', oldTags, '->', newTags)
}, { deep: true })

// Methods
const addTag = (event?: Event) => {
  if (event) event.preventDefault()
  console.log('addTag called, newTag:', newTag.value)
  if (newTag.value.trim() && !formData.value.tags.includes(newTag.value.trim())) {
    console.log('Adding tag:', newTag.value.trim())
    // Use immutable update for the entire formData to avoid reactivity issues
    const updatedTags = [...formData.value.tags, newTag.value.trim()]
    formData.value = {
      ...formData.value,
      tags: updatedTags
    }
    newTag.value = ''
    console.log('Tags after add:', formData.value.tags)
  } else {
    console.log('Tag not added (empty or duplicate)')
  }
}

const removeTag = (tag: string) => {
  if (props.disabled) return
  const updatedTags = formData.value.tags.filter(t => t !== tag)
  formData.value = {
    ...formData.value,
    tags: updatedTags
  }
}

// Prize methods
const addPrize = () => {
  if (props.disabled) return
  formData.value = {
    ...formData.value,
    prizes: [...formData.value.prizes, { name: '', description: '', value: '' }]
  }
}

const removePrize = (index: number) => {
  if (props.disabled) return
  const updatedPrizes = [...formData.value.prizes]
  updatedPrizes.splice(index, 1)
  formData.value = {
    ...formData.value,
    prizes: updatedPrizes
  }
}

// Organizer methods
const addOrganizer = () => {
  if (props.disabled) return
  formData.value = {
    ...formData.value,
    organizers: [...formData.value.organizers, { name: '', role: '' }]
  }
}

const removeOrganizer = (index: number) => {
  if (props.disabled) return
  const updatedOrganizers = [...formData.value.organizers]
  updatedOrganizers.splice(index, 1)
  formData.value = {
    ...formData.value,
    organizers: updatedOrganizers
  }
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