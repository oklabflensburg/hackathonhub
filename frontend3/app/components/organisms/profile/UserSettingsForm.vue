<template>
  <div class="space-y-6">
    <!-- Avatar Section -->
    <div class="flex items-start space-x-6 pb-4 border-b border-gray-200 dark:border-gray-700">
      <div class="relative">
        <div v-if="avatarUrl && !avatarPreview"
          class="w-24 h-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg">
          <img :src="avatarUrl" :alt="username" class="w-full h-full object-cover object-top"
            style="object-position: top" @error="$emit('avatar-error', $event)" />
        </div>
        <div v-else-if="avatarPreview"
          class="w-24 h-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg">
          <img :src="avatarPreview" :alt="username" class="w-full h-full object-cover object-top" />
        </div>
        <div v-else
          class="w-24 h-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
          <span class="text-3xl font-bold text-gray-500 dark:text-gray-400">{{ usernameInitial }}</span>
        </div>
        
        <label v-if="allowAvatarUpload" for="avatar-upload"
          class="absolute bottom-0 right-0 bg-primary-600 text-white p-2 rounded-full cursor-pointer hover:bg-primary-700 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <input id="avatar-upload" type="file" accept="image/*" class="hidden" @change="$emit('avatar-change', $event)" />
        </label>
      </div>
      
      <div class="flex-1">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">{{ username }}</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">{{ email }}</p>
        <p v-if="allowAvatarUpload" class="text-xs text-gray-500 dark:text-gray-400">
          Click the camera icon to upload a new profile picture
        </p>
      </div>
    </div>

    <!-- Form Fields -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <FormField :label="usernameLabel" :required="true" :error="errors.username">
        <Input
          v-model="formData.username"
          :error="!!errors.username"
          placeholder="Your username"
        />
      </FormField>
      
      <FormField :label="displayNameLabel">
        <Input
          v-model="formData.name"
          placeholder="Your full name"
        />
      </FormField>
      
      <FormField :label="bioLabel" class="md:col-span-2">
        <textarea
          v-model="formData.bio"
          rows="3"
          class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          :placeholder="bioPlaceholder"
        />
      </FormField>
      
      <FormField :label="locationLabel">
        <Input
          v-model="formData.location"
          placeholder="City, Country"
        />
      </FormField>
      
      <FormField :label="companyLabel">
        <Input
          v-model="formData.company"
          placeholder="Your company or organization"
        />
      </FormField>
    </div>

    <!-- GitHub Connection -->
    <div class="pt-6 border-t border-gray-200 dark:border-gray-700">
      <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">{{ githubConnectionLabel }}</h4>
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="currentColor" viewBox="0 0 24 24">
            <path
              d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
          </svg>
          <div>
            <p class="text-sm font-medium text-gray-900 dark:text-white">
              {{ isGitHubConnected ? connectedToGitHubLabel : notConnectedToGitHubLabel }}
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              {{ isGitHubConnected ? connectedAsLabel : connectGitHubToLinkIdentityLabel }}
            </p>
          </div>
        </div>
        
        <Button
          v-if="!isGitHubConnected"
          variant="secondary"
          size="sm"
          @click="$emit('connect-github')"
        >
          <template #icon>
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path
                d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
            </svg>
          </template>
          {{ connectGitHubButtonLabel }}
        </Button>
        
        <span v-else
          class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
          {{ connectedLabel }}
        </span>
      </div>
    </div>

    <!-- Form Actions -->
    <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
      <Button
        variant="secondary"
        :disabled="saving"
        @click="$emit('cancel')"
      >
        {{ cancelButtonLabel }}
      </Button>
      
      <Button
        variant="primary"
        :loading="saving"
        :disabled="saving"
        @click="$emit('save')"
      >
        {{ saveButtonLabel }}
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Button from '../../atoms/Button.vue'
import Input from '../../atoms/Input.vue'
import FormField from '../../molecules/FormField.vue'

interface Props {
  username: string
  email: string
  avatarUrl?: string
  avatarPreview?: string
  formData: {
    username: string
    name: string
    bio: string
    location: string
    company: string
  }
  errors?: {
    username?: string
  }
  isGitHubConnected?: boolean
  allowAvatarUpload?: boolean
  saving?: boolean
  
  // Labels
  usernameLabel?: string
  displayNameLabel?: string
  bioLabel?: string
  bioPlaceholder?: string
  locationLabel?: string
  companyLabel?: string
  githubConnectionLabel?: string
  connectedToGitHubLabel?: string
  notConnectedToGitHubLabel?: string
  connectedAsLabel?: string
  connectGitHubToLinkIdentityLabel?: string
  connectGitHubButtonLabel?: string
  connectedLabel?: string
  cancelButtonLabel?: string
  saveButtonLabel?: string
}

const props = withDefaults(defineProps<Props>(), {
  avatarUrl: '',
  avatarPreview: '',
  errors: () => ({}),
  isGitHubConnected: false,
  allowAvatarUpload: true,
  saving: false,
  
  usernameLabel: 'Username',
  displayNameLabel: 'Display Name',
  bioLabel: 'Bio',
  bioPlaceholder: 'Tell us about yourself',
  locationLabel: 'Location',
  companyLabel: 'Company',
  githubConnectionLabel: 'GitHub Connection',
  connectedToGitHubLabel: 'Connected to GitHub',
  notConnectedToGitHubLabel: 'Not connected to GitHub',
  connectedAsLabel: 'Connected as {username}',
  connectGitHubToLinkIdentityLabel: 'Connect GitHub to link your identity',
  connectGitHubButtonLabel: 'Connect with GitHub',
  connectedLabel: 'Connected',
  cancelButtonLabel: 'Cancel',
  saveButtonLabel: 'Save',
})

const usernameInitial = computed(() => {
  return props.username?.charAt(0).toUpperCase() || 'U'
})

defineEmits<{
  'avatar-change': [event: Event]
  'avatar-error': [event: Event]
  'connect-github': []
  cancel: []
  save: []
}>()
</script>