<template>
  <div class="notification-settings">
    <div class="settings-header">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
        {{ $t('notificationSettings.title') }}
      </h2>
      <p class="mt-2 text-gray-600 dark:text-gray-400">
        {{ $t('notificationSettings.description') }}
      </p>
    </div>

    <div class="mt-8 space-y-8">
      <!-- Global Settings -->
      <div class="global-settings card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">
            {{ $t('notificationSettings.globalSettings') }}
          </h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {{ $t('notificationSettings.globalDescription') }}
          </p>
        </div>
        
        <div class="mt-6 space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <label class="text-sm font-medium text-gray-900 dark:text-white">
                {{ $t('notificationSettings.enableAllNotifications') }}
              </label>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ $t('notificationSettings.enableAllDescription') }}
              </p>
            </div>
            <button
              @click="toggleGlobalNotifications"
              :class="[
                'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                globalNotificationsEnabled ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
              ]"
              :aria-label="globalNotificationsEnabled ? $t('notificationSettings.disableAllNotifications') : $t('notificationSettings.enableAllNotifications')"
            >
              <span
                :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  globalNotificationsEnabled ? 'translate-x-5' : 'translate-x-0'
                ]"
              />
            </button>
          </div>
        </div>
      </div>

      <!-- Channel Preferences -->
      <div class="channel-preferences card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">
            {{ $t('notificationSettings.channelPreferences') }}
          </h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {{ $t('notificationSettings.channelDescription') }}
          </p>
        </div>
        
        <div class="mt-6 space-y-6">
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
                    {{ $t('notificationSettings.emailNotifications') }}
                  </label>
                  <p class="text-sm text-gray-500 dark:text-gray-400">
                    {{ $t('notificationSettings.emailDescription') }}
                  </p>
                </div>
              </div>
              <button
                @click="toggleChannel('email')"
                :class="[
                  'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                  channelEnabled('email') ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
                ]"
                :aria-label="channelEnabled('email') ? $t('notificationSettings.disableEmailNotifications') : $t('notificationSettings.enableEmailNotifications')"
              >
                <span
                  :class="[
                    'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                    channelEnabled('email') ? 'translate-x-5' : 'translate-x-0'
                  ]"
                />
              </button>
            </div>
          </div>

          <div class="channel-item">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="channel-icon bg-green-100 dark:bg-green-900 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                  </svg>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ $t('notificationSettings.pushNotifications') }}
                  </label>
                  <p class="text-sm text-gray-500 dark:text-gray-400">
                    {{ $t('notificationSettings.pushDescription') }}
                  </p>
                </div>
              </div>
              <div class="flex items-center space-x-4">
                <button
                  @click="toggleChannel('push')"
                  :class="[
                    'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                    channelEnabled('push') ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700',
                    !isPushSupported ? 'opacity-50 cursor-not-allowed' : ''
                  ]"
                  :disabled="!isPushSupported"
                  :aria-label="channelEnabled('push') ? $t('notificationSettings.disablePushNotifications') : $t('notificationSettings.enablePushNotifications')"
                >
                  <span
                    :class="[
                      'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                      channelEnabled('push') ? 'translate-x-5' : 'translate-x-0'
                    ]"
                  />
                </button>
                <button
                  v-if="isPushSupported && !pushEnabled"
                  @click="enablePushNotifications"
                  class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  {{ $t('notificationSettings.enablePush') }}
                </button>
              </div>
            </div>
            <div v-if="!isPushSupported" class="mt-2 text-sm text-yellow-600 dark:text-yellow-400">
              {{ $t('notificationSettings.pushNotSupported') }}
            </div>
          </div>

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
                    {{ $t('notificationSettings.inAppNotifications') }}
                  </label>
                  <p class="text-sm text-gray-500 dark:text-gray-400">
                    {{ $t('notificationSettings.inAppDescription') }}
                  </p>
                </div>
              </div>
              <button
                @click="toggleChannel('in_app')"
                :class="[
                  'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                  channelEnabled('in_app') ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
                ]"
                :aria-label="channelEnabled('in_app') ? $t('notificationSettings.disableInAppNotifications') : $t('notificationSettings.enableInAppNotifications')"
              >
                <span
                  :class="[
                    'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                    channelEnabled('in_app') ? 'translate-x-5' : 'translate-x-0'
                  ]"
                />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Notification Types by Category -->
      <div v-for="category in notificationCategories" :key="category" class="category-settings card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">
            {{ $t(`notificationSettings.categories.${category}`) }}
          </h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {{ $t(`notificationSettings.categoryDescriptions.${category}`) }}
          </p>
        </div>
        
        <div class="mt-6 space-y-4">
          <div v-for="type in notificationTypesByCategory(category)" :key="type.type_key" class="type-item">
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ type.description }}
                </label>
                <div class="mt-1 flex items-center space-x-4">
                  <div v-for="channel in ['email', 'push', 'in_app']" :key="channel" class="flex items-center space-x-1">
                    <input
                      :id="`${type.type_key}-${channel}`"
                      type="checkbox"
                      :checked="type.user_preferences[channel as keyof typeof type.user_preferences]"
                      @change="updateTypePreference(type.type_key, channel as 'email' | 'push' | 'in_app', ($event.target as HTMLInputElement).checked)"
                      :disabled="!channelEnabled(channel as 'email' | 'push' | 'in_app')"
                      class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    />
                    <label :for="`${type.type_key}-${channel}`" class="text-xs text-gray-500 dark:text-gray-400">
                      {{ $t(`notificationSettings.channels.${channel}`) }}
                    </label>
                  </div>
                </div>
              </div>
              <button
                @click="toggleType(type.type_key)"
                :class="[
                  'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                  typeEnabled(type.type_key) ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
                ]"
                :aria-label="typeEnabled(type.type_key) ? $t('notificationSettings.disableNotificationType', { type: type.description }) : $t('notificationSettings.enableNotificationType', { type: type.description })"
              >
                <span
                  :class="[
                    'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                    typeEnabled(type.type_key) ? 'translate-x-5' : 'translate-x-0'
                  ]"
                />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Save Button -->
      <div class="flex justify-end">
        <button
          @click="saveSettings"
          :disabled="isSaving"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg v-if="isSaving" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          {{ $t('notificationSettings.saveSettings') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useNotificationStore } from '~/stores/notification'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'

const notificationStore = useNotificationStore()
const uiStore = useUIStore()
const { t } = useI18n()

const isSaving = ref(false)
const pushEnabled = ref(false)

// Computed properties
const globalNotificationsEnabled = computed(() => {
  return notificationStore.preferences.global_enabled !== false
})

const isPushSupported = computed(() => notificationStore.isPushSupported)

const notificationCategories = computed(() => {
  const categories = new Set<string>()
  notificationStore.notificationTypes.forEach(type => {
    if (type.category) {
      categories.add(type.category)
    }
  })
  return Array.from(categories).sort()
})

// Methods
function notificationTypesByCategory(category: string) {
  return notificationStore.notificationTypes.filter(type => type.category === category)
}

function channelEnabled(channel: 'email' | 'push' | 'in_app') {
  if (!notificationStore.preferences.channels) return true
  return notificationStore.preferences.channels[channel] !== false
}

function typeEnabled(typeKey: string) {
  const type = notificationStore.notificationTypes.find(t => t.type_key === typeKey)
  if (!type) return true
  
  // Check if any channel is enabled for this type
  return Object.values(type.user_preferences).some(enabled => enabled)
}

async function toggleGlobalNotifications() {
  const newValue = !globalNotificationsEnabled.value
  // Update local state immediately for responsive UI
  notificationStore.preferences.global_enabled = newValue
  try {
    await notificationStore.updatePreferences({
      ...notificationStore.preferences,
      global_enabled: newValue
    })
  } catch (error) {
    // Revert on error
    notificationStore.preferences.global_enabled = !newValue
    console.error('Failed to update global notifications:', error)
  }
}

async function toggleChannel(channel: 'email' | 'push' | 'in_app') {
  const newValue = !channelEnabled(channel)
  // Update local state immediately for responsive UI
  if (!notificationStore.preferences.channels) {
    notificationStore.preferences.channels = { email: true, push: true, in_app: true }
  }
  notificationStore.preferences.channels[channel] = newValue
  
  try {
    const newChannels = {
      ...notificationStore.preferences.channels,
      [channel]: newValue
    }
    
    await notificationStore.updatePreferences({
      ...notificationStore.preferences,
      channels: newChannels
    })
  } catch (error) {
    // Revert on error
    if (notificationStore.preferences.channels) {
      notificationStore.preferences.channels[channel] = !newValue
    }
    console.error('Failed to update channel:', error)
  }
}

async function toggleType(typeKey: string) {
  const type = notificationStore.notificationTypes.find(t => t.type_key === typeKey)
  if (!type) return
  
  const currentlyEnabled = typeEnabled(typeKey)
  const newValue = !currentlyEnabled
  
  // Update local state immediately for responsive UI
  Object.keys(type.user_preferences).forEach(channel => {
    type.user_preferences[channel as keyof typeof type.user_preferences] = newValue
  })
  
  try {
    const newPreferences = { ...type.user_preferences }
    
    // Toggle all channels for this type
    Object.keys(newPreferences).forEach(channel => {
      newPreferences[channel as keyof typeof newPreferences] = newValue
    })
    
    // Update each preference individually
    for (const [channel, enabled] of Object.entries(newPreferences)) {
      await notificationStore.updatePreference(typeKey, channel as any, enabled)
    }
  } catch (error) {
    // Revert on error
    Object.keys(type.user_preferences).forEach(channel => {
      type.user_preferences[channel as keyof typeof type.user_preferences] = currentlyEnabled
    })
    console.error('Failed to update notification type:', error)
  }
}

async function updateTypePreference(typeKey: string, channel: 'email' | 'push' | 'in_app', enabled: boolean) {
  await notificationStore.updatePreference(typeKey, channel, enabled)
}

async function enablePushNotifications() {
  try {
    // Request permission
    const permissionGranted = await notificationStore.requestPushPermission()
    if (!permissionGranted) return
    
    // Register service worker
    await notificationStore.registerServiceWorker()
    
    // Subscribe to push notifications
    const subscription = await notificationStore.subscribeToPushNotifications()
    if (subscription) {
      pushEnabled.value = true
      uiStore.showSuccess(t('notificationSettings.pushEnabledSuccess'))
    }
  } catch (error) {
    console.error('Failed to enable push notifications:', error)
    uiStore.showError(t('notificationSettings.pushEnableError'))
  }
}

async function saveSettings() {
  isSaving.value = true
  try {
    // Save current preferences to ensure consistency
    await notificationStore.updatePreferences(notificationStore.preferences)
    uiStore.showSuccess(t('notificationSettings.settingsSaved'))
  } catch (error) {
    console.error('Failed to save settings:', error)
    uiStore.showError(t('notificationSettings.saveError'))
  } finally {
    isSaving.value = false
  }
}

// Lifecycle
onMounted(async () => {
  await notificationStore.fetchNotificationTypes()
  await notificationStore.fetchPreferences()
  await notificationStore.checkPushSupport()
  
  // Check if push is already enabled
  if (notificationStore.isPushSupported) {
    await notificationStore.fetchPushSubscriptions()
    pushEnabled.value = notificationStore.pushSubscriptions.length > 0
  }
})
</script>

<style scoped>
.notification-settings {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  @apply bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6;
}

.card-header {
  @apply border-b border-gray-200 dark:border-gray-700 pb-4 mb-4;
}

.channel-item {
  @apply py-4 border-b border-gray-200 dark:border-gray-700 last:border-0;
}

.type-item {
  @apply py-3 border-b border-gray-100 dark:border-gray-700 last:border-0;
}

.channel-icon {
  @apply flex-shrink-0;
}
</style>