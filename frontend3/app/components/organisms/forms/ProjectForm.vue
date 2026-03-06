<template>
  <form @submit.prevent="$emit('submit', formData)" class="space-y-6">
    <!-- Project Name -->
    <FormField :label="t('create.projectForm.fields.projectName')" :required="true" :error="errors.name">
      <Input
        v-model="formData.name"
        type="text"
        :placeholder="t('create.projectForm.fields.projectNamePlaceholder')"
        :error="!!errors.name"
        required
      />
    </FormField>

    <!-- Description -->
    <FormField :label="t('create.projectForm.fields.description')" :required="true" :error="errors.description">
      <textarea
        v-model="formData.description"
        rows="4"
        class="input"
        :placeholder="t('create.projectForm.fields.descriptionPlaceholder')"
        :class="{ 'input-error': errors.description }"
        required
      />
    </FormField>

    <!-- Hackathon Selection -->
    <FormField :label="t('create.projectForm.fields.hackathon')" :required="true" :error="errors.hackathonId">
      <div v-if="hackathonsLoading" class="input flex items-center">
        <LoadingSpinner size="sm" />
        <span class="ml-2 text-gray-500">{{ t('create.projectForm.fields.loadingHackathons') }}</span>
      </div>
      <div v-else-if="hackathonsError" class="input text-red-600 bg-red-50 dark:bg-red-900/20">
        {{ t('create.projectForm.fields.errorLoadingHackathons') }}: {{ hackathonsError }}
        <Button @click="$emit('retry-hackathons')" variant="ghost" size="sm" class="ml-2">
          {{ t('create.projectForm.fields.retry') }}
        </Button>
      </div>
      <select
        v-else
        v-model="formData.hackathonId"
        class="input"
        :class="{ 'input-error': errors.hackathonId }"
        required
      >
        <option value="">{{ t('create.projectForm.fields.selectHackathon') }}</option>
        <option v-for="hackathon in hackathons" :key="hackathon.id" :value="hackathon.id">
          {{ hackathon.name }} ({{ hackathon.status }})
        </option>
      </select>
    </FormField>

    <!-- Team Selection (only show when hackathon is selected) -->
    <div v-if="formData.hackathonId">
      <FormField :label="t('create.projectForm.fields.team')" :error="errors.teamId">
        <TeamSelection
          :hackathon-id="formData.hackathonId"
          v-model="formData.teamId"
          :disabled="disabled"
        />
      </FormField>
    </div>

    <!-- Tech Stack -->
    <FormField :label="t('create.projectForm.fields.techStack')">
      <div class="flex flex-wrap gap-2 mb-2">
        <Tag
          v-for="tech in formData.techStack"
          :key="tech"
          :closable="!disabled"
          @close="removeTech(tech)"
          variant="primary"
        >
          {{ tech }}
        </Tag>
      </div>
      <div class="flex">
        <Input
          v-model="newTech"
          type="text"
          :placeholder="t('create.projectForm.fields.techPlaceholder')"
          :disabled="disabled"
          class="rounded-r-none flex-1"
          @keydown.enter.prevent="addTech"
        />
        <Button
          type="button"
          @click="addTech"
          variant="primary"
          class="rounded-l-none"
          :disabled="disabled || !newTech.trim()"
        >
          {{ t('create.projectForm.fields.add') }}
        </Button>
      </div>
    </FormField>

    <!-- Image Upload -->
    <FormField :label="t('create.projectForm.fields.projectImage')">
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
            {{ t('create.projectForm.fields.clickToUpload') }}
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">
            {{ t('create.projectForm.fields.imageRequirements') }}
          </p>
        </div>
        <div v-else class="space-y-2">
          <div class="w-32 h-32 mx-auto rounded-lg overflow-hidden">
            <img :src="formData.image_url" :alt="t('create.projectForm.fields.projectImage')" class="w-full h-full object-cover" />
          </div>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            {{ t('create.projectForm.fields.imageUploaded') }}
          </p>
          <Button
            type="button"
            @click.stop="$emit('remove-image')"
            variant="ghost"
            size="sm"
            class="text-red-600 dark:text-red-400"
            :disabled="disabled"
          >
            {{ t('create.projectForm.fields.removeImage') }}
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

    <!-- Links -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <FormField :label="t('create.projectForm.fields.githubRepository')" :error="errors.githubUrl">
        <Input
          v-model="formData.githubUrl"
          type="url"
          :placeholder="t('create.projectForm.fields.githubPlaceholder')"
          :error="!!errors.githubUrl"
          :disabled="disabled"
        />
      </FormField>
      <FormField :label="t('create.projectForm.fields.liveDemoUrl')" :error="errors.demoUrl">
        <Input
          v-model="formData.demoUrl"
          type="url"
          :placeholder="t('create.projectForm.fields.demoPlaceholder')"
          :error="!!errors.demoUrl"
          :disabled="disabled"
        />
      </FormField>
    </div>

    <!-- Team Members (only show when no team is selected) -->
    <div v-if="!formData.teamId">
      <FormField :label="t('create.projectForm.fields.teamMembers')">
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-3">
          {{ t('create.projectForm.fields.teamMembersHelp') }}
        </p>
        <div class="space-y-3">
          <div
            v-for="(member, index) in formData.teamMembers"
            :key="index"
            class="flex items-center space-x-3"
          >
            <Input
              v-model="member.name"
              type="text"
              :placeholder="t('create.projectForm.fields.memberNamePlaceholder')"
              :disabled="disabled"
              required
              class="flex-1"
            />
            <Input
              v-model="member.email"
              type="email"
              :placeholder="t('create.projectForm.fields.emailPlaceholder')"
              :disabled="disabled"
              class="flex-1"
            />
            <Button
              type="button"
              @click="removeTeamMember(index)"
              variant="ghost"
              size="sm"
              :disabled="disabled || formData.teamMembers.length === 1"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </Button>
          </div>
        </div>
        <Button
          type="button"
          @click="addTeamMember"
          variant="secondary"
          class="mt-3"
          :disabled="disabled"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          {{ t('create.projectForm.fields.addTeamMember') }}
        </Button>
      </FormField>
    </div>

    <!-- Team Info (show when team is selected) -->
    <div v-else class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
      <div class="flex items-center mb-2">
        <svg class="w-5 h-5 text-blue-600 dark:text-blue-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <span class="font-medium text-blue-800 dark:text-blue-300">{{ t('create.projectForm.fields.teamSelected') }}</span>
      </div>
      <p class="text-sm text-blue-700 dark:text-blue-400">
        {{ t('create.projectForm.fields.teamSelectedHelp') }}
      </p>
    </div>

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
        {{ t('create.projectForm.buttons.submitProject') }}
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
import LoadingSpinner from '@/components/atoms/LoadingSpinner.vue'
import TeamSelection from '@/components/TeamSelection.vue'

// Props
interface TeamMember {
  name: string
  email: string
}

interface ProjectFormData {
  name: string
  description: string
  hackathonId: string
  teamId: number | null
  techStack: string[]
  githubUrl: string
  demoUrl: string
  teamMembers: TeamMember[]
  image_url: string
}

interface Hackathon {
  id: number
  name: string
  status: string
}

interface Props {
  // Form data
  modelValue: ProjectFormData
  // Options
  hackathons: Hackathon[]
  hackathonsLoading?: boolean
  hackathonsError?: string
  // States
  submitting?: boolean
  disabled?: boolean
  errors?: Record<string, string>
}

const props = withDefaults(defineProps<Props>(), {
  hackathons: () => [],
  hackathonsLoading: false,
  hackathonsError: '',
  submitting: false,
  disabled: false,
  errors: () => ({})
})

const { t } = useI18n()

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: ProjectFormData]
  'submit': [data: ProjectFormData]
  'reset': []
  'retry-hackathons': []
  'image-upload': [event: Event]
  'remove-image': []
}>()

// Local state
const newTech = ref('')
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

// Debug: log tech stack changes
watch(() => formData.value.techStack, (newTechStack, oldTechStack) => {
  console.log('Tech stack changed:', oldTechStack, '->', newTechStack)
}, { deep: true })

// Methods
const addTech = () => {
  if (newTech.value.trim() && !formData.value.techStack.includes(newTech.value.trim())) {
    formData.value.techStack.push(newTech.value.trim())
    newTech.value = ''
  }
}

const removeTech = (tech: string) => {
  if (props.disabled) return
  formData.value.techStack = formData.value.techStack.filter(t => t !== tech)
}

const addTeamMember = () => {
  if (props.disabled) return
  formData.value.teamMembers.push({ name: '', email: '' })
}

const removeTeamMember = (index: number) => {
  if (props.disabled || formData.value.teamMembers.length <= 1) return
  formData.value.teamMembers.splice(index, 1)
}

const triggerImageUpload = () => {
  console.log('triggerImageUpload called, disabled:', props.disabled, 'imageInput:', imageInput.value)
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