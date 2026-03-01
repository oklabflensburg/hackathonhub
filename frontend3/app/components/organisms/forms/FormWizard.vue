<template>
  <div class="max-w-4xl mx-auto">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ title }}</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        {{ subtitle }}
      </p>
    </div>

    <!-- Tabs Navigation -->
    <div class="flex border-b border-gray-200 dark:border-gray-700 mb-8">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="[
          'px-6 py-3 font-medium text-sm transition-colors',
          activeTab === tab.id
            ? 'border-b-2 border-primary-600 text-primary-600 dark:text-primary-400'
            : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300'
        ]"
        :disabled="disabled"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Project Form Tab -->
    <div v-if="activeTab === 'project'" class="space-y-6">
      <div class="card">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">{{ projectFormTitle }}</h2>
          <ProjectForm
            :model-value="projectFormData"
            @update:model-value="$emit('update:projectFormData', $event)"
            :hackathons="hackathons"
          :hackathons-loading="hackathonsLoading"
          :hackathons-error="hackathonsError"
          :submitting="submitting"
          :disabled="disabled"
          :errors="errors"
          :name-label="projectNameLabel"
          :name-placeholder="projectNamePlaceholder"
          :description-label="projectDescriptionLabel"
          :description-placeholder="projectDescriptionPlaceholder"
          :hackathon-label="hackathonLabel"
          :loading-hackathons-text="loadingHackathonsText"
          :error-loading-hackathons-text="errorLoadingHackathonsText"
          :retry-text="retryText"
          :select-hackathon-text="selectHackathonText"
          :team-label="teamLabel"
          :tech-stack-label="techStackLabel"
          :tech-placeholder="techPlaceholder"
          :add-text="addText"
          :github-repository-label="githubRepositoryLabel"
          :github-placeholder="githubPlaceholder"
          :live-demo-url-label="liveDemoUrlLabel"
          :demo-placeholder="demoPlaceholder"
          :team-members-label="teamMembersLabel"
          :team-members-help-text="teamMembersHelpText"
          :member-name-placeholder="memberNamePlaceholder"
          :email-placeholder="teamMemberEmailPlaceholder"
          :add-team-member-text="addTeamMemberText"
          :team-selected-text="teamSelectedText"
          :team-selected-help-text="teamSelectedHelpText"
          :reset-text="resetText"
          :submit-text="projectSubmitText"
          @submit="$emit('project-submit', $event)"
          @reset="$emit('project-reset')"
          @retry-hackathons="$emit('retry-hackathons')"
        />
      </div>
    </div>

    <!-- Hackathon Form Tab -->
    <div v-else class="space-y-6">
      <div class="card">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">{{ hackathonFormTitle }}</h2>
        <HackathonForm
          :model-value="hackathonFormData"
          @update:model-value="$emit('update:hackathonFormData', $event)"
          :submitting="submitting"
          :disabled="disabled"
          :errors="errors"
          :name-label="hackathonNameLabel"
          :name-placeholder="hackathonNamePlaceholder"
          :description-label="hackathonDescriptionLabel"
          :description-placeholder="hackathonDescriptionPlaceholder"
          :organizer-label="organizerLabel"
          :organizer-placeholder="organizerPlaceholder"
          :start-date-label="startDateLabel"
          :end-date-label="endDateLabel"
          :location-label="locationLabel"
          :online-text="onlineText"
          :in-person-text="inPersonText"
          :location-placeholder="locationPlaceholder"
          :prize-pool-label="prizePoolLabel"
          :prize-pool-placeholder="prizePoolPlaceholder"
          :tags-label="tagsLabel"
          :tags-placeholder="tagsPlaceholder"
          :add-text="addText"
          :rules-label="rulesLabel"
          :rules-placeholder="rulesPlaceholder"
          :hackathon-image-label="hackathonImageLabel"
          :click-to-upload-text="clickToUploadText"
          :image-requirements-text="imageRequirementsText"
          :image-alt-text="imageAltText"
          :image-uploaded-text="imageUploadedText"
          :remove-image-text="removeImageText"
          :contact-email-label="contactEmailLabel"
          :email-placeholder="contactEmailPlaceholder"
          :reset-text="resetText"
          :submit-text="hackathonSubmitText"
          @submit="$emit('hackathon-submit', $event)"
          @reset="$emit('hackathon-reset')"
          @image-upload="$emit('hackathon-image-upload', $event)"
          @remove-image="$emit('hackathon-remove-image')"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import ProjectForm from './ProjectForm.vue'
import HackathonForm from './HackathonForm.vue'
// Interfaces from ProjectForm.vue
interface ProjectFormData {
  name: string
  description: string
  hackathonId: string
  teamId: number | null
  techStack: string[]
  githubUrl: string
  demoUrl: string
  teamMembers: Array<{ name: string; email: string }>
}

// Interfaces from HackathonForm.vue
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

// Props
interface Tab {
  id: string
  label: string
}

interface Hackathon {
  id: number
  name: string
  status: string
}

interface Props {
  // Tabs
  tabs?: Tab[]
  activeTab?: string
  // Form data
  projectFormData: ProjectFormData
  hackathonFormData: HackathonFormData
  // Options
  hackathons: Hackathon[]
  hackathonsLoading?: boolean
  hackathonsError?: string
  // States
  submitting?: boolean
  disabled?: boolean
  errors?: Record<string, string>
  // Labels
  title?: string
  subtitle?: string
  projectFormTitle?: string
  hackathonFormTitle?: string
  projectNameLabel?: string
  projectNamePlaceholder?: string
  projectDescriptionLabel?: string
  projectDescriptionPlaceholder?: string
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
  teamMemberEmailPlaceholder?: string
  addTeamMemberText?: string
  teamSelectedText?: string
  teamSelectedHelpText?: string
  hackathonNameLabel?: string
  hackathonNamePlaceholder?: string
  hackathonDescriptionLabel?: string
  hackathonDescriptionPlaceholder?: string
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
  rulesLabel?: string
  rulesPlaceholder?: string
  hackathonImageLabel?: string
  clickToUploadText?: string
  imageRequirementsText?: string
  imageAltText?: string
  imageUploadedText?: string
  removeImageText?: string
  contactEmailLabel?: string
  contactEmailPlaceholder?: string
  resetText?: string
  projectSubmitText?: string
  hackathonSubmitText?: string
}

const props = withDefaults(defineProps<Props>(), {
  tabs: () => [
    { id: 'project', label: 'Create Project' },
    { id: 'hackathon', label: 'Create Hackathon' }
  ],
  activeTab: 'project',
  hackathons: () => [],
  hackathonsLoading: false,
  hackathonsError: '',
  submitting: false,
  disabled: false,
  errors: () => ({}),
  title: 'Create',
  subtitle: 'Create a new project or hackathon',
  projectFormTitle: 'Create Project',
  hackathonFormTitle: 'Create Hackathon',
  projectNameLabel: 'Project Name',
  projectNamePlaceholder: 'Enter project name',
  projectDescriptionLabel: 'Description',
  projectDescriptionPlaceholder: 'Describe your project...',
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
  teamMemberEmailPlaceholder: 'Email (optional)',
  addTeamMemberText: 'Add Team Member',
  teamSelectedText: 'Team Selected',
  teamSelectedHelpText: 'You\'re submitting as part of a team. Team members will be automatically added.',
  hackathonNameLabel: 'Hackathon Name',
  hackathonNamePlaceholder: 'Enter hackathon name',
  hackathonDescriptionLabel: 'Description',
  hackathonDescriptionPlaceholder: 'Describe your hackathon...',
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
  rulesLabel: 'Rules & Guidelines',
  rulesPlaceholder: 'Add rules and guidelines for participants...',
  hackathonImageLabel: 'Hackathon Image',
  clickToUploadText: 'Click to upload image',
  imageRequirementsText: 'PNG, JPG, GIF up to 5MB',
  imageAltText: 'Hackathon preview',
  imageUploadedText: 'Image uploaded',
  removeImageText: 'Remove Image',
  contactEmailLabel: 'Contact Email',
  contactEmailPlaceholder: 'contact@example.com',
  resetText: 'Reset',
  projectSubmitText: 'Create Project',
  hackathonSubmitText: 'Create Hackathon'
})

// Emits
const emit = defineEmits<{
  'update:activeTab': [tabId: string]
  'update:projectFormData': [data: ProjectFormData]
  'update:hackathonFormData': [data: HackathonFormData]
  'project-submit': [data: ProjectFormData]
  'project-reset': []
  'hackathon-submit': [data: HackathonFormData]
  'hackathon-reset': []
  'retry-hackathons': []
  'hackathon-image-upload': [event: Event]
  'hackathon-remove-image': []
}>()

// Local state
const activeTab = ref(props.activeTab)

// Watch for prop changes
watch(() => props.activeTab, (newValue) => {
  activeTab.value = newValue
})

// Emit tab changes
watch(activeTab, (newValue) => {
  emit('update:activeTab', newValue)
})
</script>

<style scoped>
.card {
  @apply bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6;
}
</style>