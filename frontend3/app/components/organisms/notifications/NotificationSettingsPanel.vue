<template>
  <div class="notification-settings-panel">
    <!-- Header -->
    <div class="settings-header mb-8">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
        {{ title }}
      </h2>
      <p class="mt-2 text-gray-600 dark:text-gray-400">
        {{ description }}
      </p>
    </div>

    <!-- Global Settings -->
    <div class="global-settings card mb-8">
      <div class="card-header mb-6">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">
          {{ globalSettingsTitle }}
        </h3>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          {{ globalSettingsDescription }}
        </p>
      </div>
      
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <label class="text-sm font-medium text-gray-900 dark:text-white">
              {{ enableAllLabel }}
            </label>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              {{ enableAllDescription }}
            </p>
          </div>
          <button
            @click="$emit('toggle-global')"
            :class="[
              'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900',
              globalEnabled ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'
            ]"
            :aria-label="globalEnabled ? disableAllLabel : enableAllLabel"
          >
            <span
              :class="[
                'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                globalEnabled ? 'translate-x-5' : 'translate-x-0'
              ]"
            />
          </button>
        </div>
      </div>
    </div>

    <!-- Channel Preferences -->
    <div class="channel-preferences card mb-8">
      <div class="card-header mb-6">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">
          {{ channelPreferencesTitle }}
        </h3>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          {{ channelPreferencesDescription }}
        </p>
      </div>
      
      <div class="space-y-6">
        <!-- Email Channel -->
        <div class="channel-item">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="channel-icon bg-blue-100 dark:bg-blue-900 p-2 rounded-lg">
                <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ emailLabel }}
                </label>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  {{ emailDescription }}
                </p>
              </div>
            </div>
            <button
              @click="$emit('toggle-channel', 'email')"
              :class="[
                'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900',
                channels.email ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'
              ]"
              :aria-label="channels.email ? disableEmailLabel : enableEmailLabel"
            >
              <span
                :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  channels.email ? 'translate-x-5' : 'translate-x-0'
                ]"
              />
            </button>
          </div>
        </div>

        <!-- Push Channel -->
        <div class="channel-item">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="channel-icon bg-green-100 dark:bg-green-900 p-2 rounded-lg">
                <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ pushLabel }}
                </label>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  {{ pushDescription }}
                </p>
              </div>
            </div>
            <button
              @click="$emit('toggle-channel', 'push')"
              :class="[
                'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900',
                channels.push ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'
              ]"
              :disabled="!isPushSupported"
              :aria-label="channels.push ? disablePushLabel : enablePushLabel"
            >
              <span
                :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  channels.push ? 'translate-x-5' : 'translate-x-0'
                ]"
              />
            </button>
          </div>
          <div v-if="!isPushSupported" class="mt-2 text-sm text-amber-600 dark:text-amber-400">
            {{ pushNotSupportedText }}
          </div>
          <button
            v-if="isPushSupported && !pushEnabled && channels.push"
            @click="$emit('enable-push')"
            class="mt-3 inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            {{ enablePushButtonText }}
          </button>
        </div>

        <!-- In-App Channel -->
        <div class="channel-item">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="channel-icon bg-purple-100 dark:bg-purple-900 p-2 rounded-lg">
                <svg class="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ inAppLabel }}
                </label>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  {{ inAppDescription }}
                </p>
              </div>
            </div>
            <button
              @click="$emit('toggle-channel', 'in_app')"
              :class="[
                'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900',
                channels.in_app ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'
              ]"
              :aria-label="channels.in_app ? disableInAppLabel : enableInAppLabel"
            >
              <span
                :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  channels.in_app ? 'translate-x-5' : 'translate-x-0'
                ]"
              />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Notification Types by Category -->
    <div v-for="category in categories" :key="category.id" class="category-settings card mb-8">
      <div class="card-header mb-6">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">
          {{ category.title }}
        </h3>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          {{ category.description }}
        </p>
      </div>
      
      <div class="space-y-4">
        <div v-for="type in category.types" :key="type.type_key" class="type-item">
          <div class="flex items-center justify-between">
            <div>
              <label class="text-sm font-medium text-gray-900 dark:text-white">
                {{ type.description }}
              </label>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ type.help_text }}
              </p>
            </div>
            <button
              @click="$emit('toggle-type', type.type_key)"
              :class="[
                'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900',
                type.enabled ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'
              ]"
              :aria-label="type.enabled ? type.disableLabel : type.enableLabel"
            >
              <span
                :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  type.enabled ? 'translate-x-5' : 'translate-x-0'
                ]"
              />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">{{ loadingText }}</p>
    </div>

    <!-- Error State -->
    <div v-if="error" class="error-state bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-8">
      <div class="flex">
        <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800 dark:text-red-300">{{ errorTitle }}</h3>
          <div class="mt-2 text-sm text-red-700 dark:text-red-400">
            <p>{{ error }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface NotificationType {
  type_key: string
  description: string
  help_text: string
  enabled: boolean
  enableLabel?: string
  disableLabel?: string
}

export interface NotificationCategory {
  id: string
  title: string
  description: string
  types: NotificationType[]
}

export interface NotificationChannels {
  email: boolean
  push: boolean
  in_app: boolean
}

export interface NotificationSettingsPanelProps {
  // Basic props
  title?: string
  description?: string
  loading?: boolean
  loadingText?: string
  error?: string
  errorTitle?: string
  
  // Global settings
  globalEnabled?: boolean
  globalSettingsTitle?: string
  globalSettingsDescription?: string
  enableAllLabel?: string
  enableAllDescription?: string
  disableAllLabel?: string
  
  // Channel preferences
  channels?: NotificationChannels
  channelPreferencesTitle?: string
  channelPreferencesDescription?: string
  emailLabel?: string
  emailDescription?: string
  enableEmailLabel?: string
  disableEmailLabel?: string
  pushLabel?: string
  pushDescription?: string
  enablePushLabel?: string
  disablePushLabel?: string
  inAppLabel?: string
  inAppDescription?: string
  enableInAppLabel?: string
  disableInAppLabel?: string
  
  // Push notifications
  isPushSupported?: boolean
  pushEnabled?: boolean
  pushNotSupportedText?: string
  enablePushButtonText?: string
  
  // Categories
  categories?: NotificationCategory[]
}

const props = withDefaults(defineProps<NotificationSettingsPanelProps>(), {
  title: 'Notification Settings',
  description: 'Manage your notification preferences',
  loading: false,
  loadingText: 'Loading settings...',
  errorTitle: 'Error loading settings',
  
  globalEnabled: true,
  globalSettingsTitle: 'Global Settings',
  globalSettingsDescription: 'Control all notifications at once',
  enableAllLabel: 'Enable all notifications',
  enableAllDescription: 'Turn all notifications on or off',
  disableAllLabel: 'Disable all notifications',
  
  channels: () => ({
    email: true,
    push: false,
    in_app: true
  }),
  channelPreferencesTitle: 'Channel Preferences',
  channelPreferencesDescription: 'Choose how you want to receive notifications',
  emailLabel: 'Email notifications',
  emailDescription: 'Receive notifications via email',
  enableEmailLabel: 'Enable email notifications',
  disableEmailLabel: 'Disable email notifications',
  pushLabel: 'Push notifications',
  pushDescription: 'Receive browser push notifications',
  enablePushLabel: 'Enable push notifications',
  disablePushLabel: 'Disable push notifications',
  inAppLabel: 'In-app notifications',
  inAppDescription: 'Receive notifications within the application',
  enableInAppLabel: 'Enable in-app notifications',
  disableInAppLabel: 'Disable in-app notifications',
  
  isPushSupported: false,
  pushEnabled: false,
  pushNotSupportedText: 'Push notifications are not supported in your browser',
  enablePushButtonText: 'Enable push notifications',
  
  categories: () => []
})

const emit = defineEmits<{
  'toggle-global': []
  'toggle-channel': [channel: string]
  'toggle-type': [typeKey: string]
  'enable-push': []
}>()
</script>

<style scoped>
.notification-settings-panel {
  @apply max-w-4xl mx-auto;
}

.card {
  @apply bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6;
}

.card-header {
  @apply border-b border-gray-200 dark:border-gray-700 pb-4;
}

.channel-icon {
  @apply flex-shrink-0;
}

.error-state {
  @apply animate-pulse;
}
</style>