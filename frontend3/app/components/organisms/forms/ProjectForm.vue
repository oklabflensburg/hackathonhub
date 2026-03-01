<template>
  <form @submit.prevent="$emit('submit', formData)" class="space-y-6">
    <!-- Project Name -->
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

    <!-- Hackathon Selection -->
    <FormField :label="hackathonLabel" :required="true" :error="errors.hackathonId">
      <div v-if="hackathonsLoading" class="input flex items-center">
        <LoadingSpinner size="sm" />
        <span class="ml-2 text-gray-500">{{ loadingHackathonsText }}</span>
      </div>
      <div v-else-if="hackathonsError" class="input text-red-600 bg-red-50 dark:bg-red-900/20">
        {{ errorLoadingHackathonsText }}: {{ hackathonsError }}
        <Button @click="$emit('retry-hackathons')" variant="ghost" size="sm" class="ml-2">
          {{ retryText }}
        </Button>
      </div>
      <select
        v-else
        v-model="formData.hackathonId"
        class="input"
        :class="{ 'input-error': errors.hackathonId }"
        required
      >
        <option value="">{{ selectHackathonText }}</option>
        <option v-for="hackathon in hackathons" :key="hackathon.id" :value="hackathon.id">
          {{ hackathon.name }} ({{ hackathon.status }})
        </option>
      </select>
    </FormField>

    <!-- Team Selection (only show when hackathon is selected) -->
    <div v-if="formData.hackathonId">
      <FormField :label="teamLabel" :error="errors.teamId">
        <TeamSelection
          :hackathon-id="formData.hackathonId"
          v-model="formData.teamId"
          :disabled="disabled"
        />
      </FormField>
    </div>

    <!-- Tech Stack -->
    <FormField :label="techStackLabel">
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
          :placeholder="techPlaceholder"
          :disabled="disabled"
          class="rounded-r-none"
          @keydown.enter.prevent="addTech"
        />
        <Button
          type="button"
          @click="addTech"
          variant="primary"
          class="rounded-l-none"
          :disabled="disabled || !newTech.trim()"
        >
          {{ addText }}
        </Button>
      </div>
    </FormField>

    <!-- Links -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <FormField :label="githubRepositoryLabel" :error="errors.githubUrl">
        <Input
          v-model="formData.githubUrl"
          type="url"
          :placeholder="githubPlaceholder"
          :error="!!errors.githubUrl"
          :disabled="disabled"
        />
      </FormField>
      <FormField :label="liveDemoUrlLabel" :error="errors.demoUrl">
        <Input
          v-model="formData.demoUrl"
          type="url"
          :placeholder="demoPlaceholder"
          :error="!!errors.demoUrl"
          :disabled="disabled"
        />
      </FormField>
    </div>

    <!-- Team Members (only show when no team is selected) -->
    <div v-if="!formData.teamId">
      <FormField :label="teamMembersLabel">
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-3">
          {{ teamMembersHelpText }}
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
              :placeholder="memberNamePlaceholder"
              :disabled="disabled"
              required
              class="flex-1"
            />
            <Input
              v-model="member.email"
              type="email"
              :placeholder="emailPlaceholder"
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
          {{ addTeamMemberText }}
        </Button>
      </FormField>
    </div>

    <!-- Team Info (show when team is selected) -->
    <div v-else class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
      <div class="flex items-center mb-2">
        <svg class="w-5 h-5 text-blue-600 dark:text-blue-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <span class="font-medium text-blue-800 dark:text-blue-300">{{ teamSelectedText }}</span>
      </div>
      <p class="text-sm text-blue-700 dark:text-blue-400">
        {{ teamSelectedHelpText }}
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
  // Labels
  nameLabel?: string
  namePlaceholder?: string
  descriptionLabel?: string
  descriptionPlaceholder?: string
  hackathonLabel?: string
  loadingHackathonsText?: string
  errorLoadingHackathonsText?: string
  retryText?: string
  selectHackathonText?: string
  teamLabel?: string
  techStackLabel?: string
  techPlaceholder?: string
  addText?: string
  githubRepositoryLabel?: string
  githubPlaceholder?: string
  liveDemoUrlLabel?: string
  demoPlaceholder?: string
  teamMembersLabel?: string
  teamMembersHelpText?: string
  memberNamePlaceholder?: string
  emailPlaceholder?: string
  addTeamMemberText?: string
  teamSelectedText?: string
  teamSelectedHelpText?: string
  resetText?: string
  submitText?: string
}

const props = withDefaults(defineProps<Props>(), {
  hackathons: () => [],
  hackathonsLoading: false,
  hackathonsError: '',
  submitting: false,
  disabled: false,
  errors: () => ({}),
  nameLabel: 'Project Name',
  namePlaceholder: 'Enter project name',
  descriptionLabel: 'Description',
  descriptionPlaceholder: 'Describe your project...',
  hackathonLabel: 'Hackathon',
  loadingHackathonsText: 'Loading hackathons...',
  errorLoadingHackathonsText: 'Error loading hackathons',
  retryText: 'Retry',
  selectHackathonText: 'Select a hackathon',
  teamLabel: 'Team',
  techStackLabel: 'Tech Stack',
  techPlaceholder: 'Add a technology',
  addText: 'Add',
  githubRepositoryLabel: 'GitHub Repository',
  githubPlaceholder: 'https://github.com/username/repo',
  liveDemoUrlLabel: 'Live Demo URL',
  demoPlaceholder: 'https://demo.example.com',
  teamMembersLabel: 'Team Members',
  teamMembersHelpText: 'Add team members if you\'re not part of a team yet',
  memberNamePlaceholder: 'Member name',
  emailPlaceholder: 'Email (optional)',
  addTeamMemberText: 'Add Team Member',
  teamSelectedText: 'Team Selected',
  teamSelectedHelpText: 'You\'re submitting as part of a team. Team members will be automatically added.',
  resetText: 'Reset',
  submitText: 'Create Project'
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: ProjectFormData]
  'submit': [data: ProjectFormData]
  'reset': []
  'retry-hackathons': []
}>()

// Local state
const newTech = ref('')
const formData = ref({ ...props.modelValue })
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