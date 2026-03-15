<template>
  <div class="notifications-page">
    <!-- Header -->
    <div class="page-header mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            {{ t('notifications.title') }}
          </h1>
          <p class="mt-2 text-gray-600 dark:text-gray-400">
            {{ t('notifications.description') }}
          </p>
        </div>
        <div class="flex items-center space-x-4">
          <button v-if="hasUnreadNotifications" @click="markAllAsRead" :disabled="isMarkingAllAsRead"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed">
            <svg v-if="isMarkingAllAsRead" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none"
              viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            {{ t('notifications.markAllAsRead') }}
          </button>
          <button @click="refreshNotifications" :disabled="isRefreshingNotifications"
            class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md shadow-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            <svg v-if="isRefreshingNotifications" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none"
              viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            <svg v-else class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ t('notifications.refresh') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-3 mb-8">
      <div class="stats-card bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="rounded-md bg-blue-500 p-3">
                <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                  {{ t('notifications.totalNotifications') }}
                </dt>
                <dd class="text-lg font-medium text-gray-900 dark:text-white">
                  {{ totalNotifications }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="stats-card bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="rounded-md bg-green-500 p-3">
                <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                  {{ t('notifications.readNotifications') }}
                </dt>
                <dd class="text-lg font-medium text-gray-900 dark:text-white">
                  {{ readNotificationsCount }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="stats-card bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="rounded-md bg-yellow-500 p-3">
                <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                  {{ t('notifications.unreadNotifications') }}
                </dt>
                <dd class="text-lg font-medium text-gray-900 dark:text-white">
                  {{ unreadNotificationsCount }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="mt-8 mb-8">
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="-mb-px flex space-x-8">
          <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key" :class="[
            'py-4 px-1 border-b-2 font-medium text-sm',
            activeTab === tab.key
              ? 'border-primary-500 text-primary-600 dark:text-primary-400'
              : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
          ]">
            {{ tab.label }}
            <span v-if="tab.count !== undefined" :class="[
              'ml-2 py-0.5 px-2 text-xs rounded-full',
              activeTab === tab.key
                ? 'bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
            ]">
              {{ tab.count }}
            </span>
          </button>
        </nav>
      </div>
    </div>

    <!-- Content -->
    <div class="mt-8">
      <template v-if="activeTab === 'preferences'">
        <!-- Preferences Tab -->
        <div>
          <NotificationSettingsPanel
            :title="t('notificationSettings.title')"
            :description="t('notificationSettings.description')"
            :loading="isLoadingPreferences"
            :loading-text="t('notificationSettings.loading')"
            :error="preferencesError || undefined"
            :error-title="t('notificationSettings.errorTitle')"
            :global-enabled="globalNotificationsEnabled"
            :global-settings-title="t('notificationSettings.globalSettings')"
            :global-settings-description="t('notificationSettings.globalDescription')"
            :enable-all-label="t('notificationSettings.enableAllNotifications')"
            :enable-all-description="t('notificationSettings.enableAllDescription')"
            :disable-all-label="t('notificationSettings.disableAllNotifications')"
            :quiet-hours="quietHours"
            :quiet-hours-title="t('notificationSettings.quietHours')"
            :quiet-hours-description="t('notificationSettings.quietHoursDescription')"
            :quiet-hours-start-label="t('notificationSettings.quietHoursStart')"
            :quiet-hours-end-label="t('notificationSettings.quietHoursEnd')"
            :enable-quiet-hours-label="t('notificationSettings.enableQuietHours')"
            :disable-quiet-hours-label="t('notificationSettings.disableQuietHours')"
            :channels="notificationChannels"
            :channel-preferences-title="t('notificationSettings.channelPreferences')"
            :channel-preferences-description="t('notificationSettings.channelDescription')"
            :email-label="t('notificationSettings.emailNotifications')"
            :email-description="t('notificationSettings.emailDescription')"
            :enable-email-label="t('notificationSettings.enableEmailNotifications')"
            :disable-email-label="t('notificationSettings.disableEmailNotifications')"
            :push-label="t('notificationSettings.pushNotifications')"
            :push-description="t('notificationSettings.pushDescription')"
            :enable-push-label="t('notificationSettings.enablePushNotifications')"
            :disable-push-label="t('notificationSettings.disablePushNotifications')"
            :in-app-label="t('notificationSettings.inAppNotifications')"
            :in-app-description="t('notificationSettings.inAppDescription')"
            :enable-in-app-label="t('notificationSettings.enableInAppNotifications')"
            :disable-in-app-label="t('notificationSettings.disableInAppNotifications')"
            :is-push-supported="isPushSupported"
            :push-enabled="pushEnabled"
            :push-not-supported-text="t('notificationSettings.pushNotSupported')"
            :enable-push-button-text="t('notificationSettings.enablePushButton')"
            :categories="notificationCategories"
            @toggle-global="handleToggleGlobal"
            @toggle-category="handleToggleCategory"
            @toggle-channel="handleToggleChannel"
            @toggle-type="handleToggleType"
            @toggle-quiet-hours="handleToggleQuietHours"
            @update-quiet-hours="handleUpdateQuietHours"
            @enable-push="enablePushNotifications"
          />
        </div>
      </template>
      <template v-else>
        <!-- Atomic Design Notifications Components -->
        <div>
          <!-- Notification Filters Component -->
          <NotificationFilters
            :filters="notificationFiltersState"
            :sort-field="notificationSortField"
            :sort-direction="notificationSortDirection"
            :available-types="['all', AtomicNotificationType.SYSTEM, AtomicNotificationType.TEAM_INVITATION, AtomicNotificationType.PROJECT_COMMENT, AtomicNotificationType.HACKATHON_REGISTRATION, AtomicNotificationType.COMMENT_REPLY, AtomicNotificationType.PROJECT_VOTE, AtomicNotificationType.NEWSLETTER, AtomicNotificationType.HACKATHON_STARTING_SOON]"
            :available-statuses="['all', AtomicNotificationStatus.READ, AtomicNotificationStatus.UNREAD, AtomicNotificationStatus.ARCHIVED]"
            @update-filters="handleNotificationFiltersUpdate"
            @update-sort="handleNotificationSortUpdate"
            @reset-filters="handleNotificationFiltersReset"
            class="mb-6"
          />

          <!-- Notification List Component -->
          <NotificationList
            :notifications="atomicNotificationsForList"
            :loading="atomicNotificationsLoading"
            :error="atomicNotificationsErrorMessage"
            :empty-title="t('notifications.noNotifications')"
            :empty-description="t('notifications.noNotificationsDescription')"
            :empty-action-text="t('notifications.refresh')"
            :show-mark-as-read="true"
            :show-mark-all-read="true"
            :show-archive="false"
            :show-delete="true"
            :show-filters="false"
            @mark-as-read="handleMarkAsRead"
            @mark-all-read="handleMarkAllRead"
            @archive="handleArchiveNotification"
            @delete="handleDeleteNotification"
            @refresh="() => fetchAtomicNotifications(true)"
          />

          <!-- Legacy Notification Center (for compatibility) -->
          <div v-if="false" class="hidden">
            <NotificationCenter
              :notifications="legacyNotificationsForCenter"
              :unread-count="unreadNotificationsCount"
              :loading="isLoading"
              :empty-title="t('notifications.noNotifications')"
              :empty-description="t('notifications.noNotificationsDescription')"
              :empty-action-text="t('notifications.refresh')"
              :filters="notificationFilters"
              :show-mark-as-read="true"
              :show-dismiss="true"
              :show-settings="false"
              :variant="'default'"
              :title="t('notifications.title')"
              :subtitle="t('notifications.description')"
              :footer-text="hasMoreNotifications ? t('notifications.loadMore') : ''"
              @notification-click="handleNotificationClick"
              @notification-read="handleNotificationRead"
              @notification-dismiss="handleNotificationDismiss"
              @notification-action="handleNotificationAction"
              @filter-selected="handleFilterSelected"
              @empty-action="refreshNotifications"
              @settings="activeTab = 'preferences'"
            />
          </div>

          <!-- Load More -->
          <div v-if="atomicNotifications.length > 0 && !atomicNotificationsLoading" class="mt-8 text-center">
            <button @click="() => fetchAtomicNotifications()" :disabled="atomicNotificationsLoading"
              class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md shadow-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed">
              <svg v-if="atomicNotificationsLoading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-500" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              {{ t('notifications.loadMore') }}
            </button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationStore } from '~/stores/notification'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'
import NotificationCenter from '~/components/organisms/notifications/NotificationCenter.vue'
import NotificationSettingsPanel from '~/components/organisms/notifications/NotificationSettingsPanel.vue'
import NotificationList from '~/components/organisms/notifications/NotificationList.vue'
import NotificationFilters from '~/components/organisms/notifications/NotificationFilters.vue'
import { useNotifications } from '~/composables/useNotifications'
import {
  NotificationStatus as AtomicNotificationStatus,
  NotificationType as AtomicNotificationType
} from '~/types/notification-types'
import type {
  Notification as AtomicNotification,
  NotificationFilterOptions,
  NotificationSortField,
  NotificationSortDirection
} from '~/types/notification-types'
import type { Notification, NotificationFilter } from '~/components/organisms/notifications/NotificationCenter.vue'
import type { NotificationCategory, NotificationChannels, NotificationType } from '~/components/organisms/notifications/NotificationSettingsPanel.vue'
import type { UserNotification } from '~/stores/notification'

const router = useRouter()
const notificationStore = useNotificationStore()
const uiStore = useUIStore()
const { t } = useI18n()

// State
const activeTab = ref<'all' | 'unread' | 'read' | 'preferences'>('all')
const isMarkingAllAsRead = ref(false)
const isLoadingMore = ref(false)
const isLoadingPreferences = ref(false)
const preferencesError = ref<string | null>(null)
const pageSize = 20
const currentPage = ref(1)

// New atomic design notification components state
const notificationFiltersState = ref<NotificationFilterOptions>({
  search: undefined,
  type: undefined,
  status: undefined,
  sortBy: 'createdAt',
  sortDirection: 'desc'
})
const notificationSortField = ref<NotificationSortField>('createdAt')
const notificationSortDirection = ref<NotificationSortDirection>('desc')

// Use atomic design composables
const { 
  notifications: atomicNotifications, 
  loading: atomicNotificationsLoading, 
  error: atomicNotificationsError,
  unreadCount: atomicUnreadCount,
  fetchNotifications: fetchAtomicNotifications,
  markAsRead: markAtomicAsRead,
  markAllAsRead: markAllAtomicAsRead,
  updateFilters: updateAtomicFilters,
  updateSort: updateAtomicSort,
  resetFilters: resetAtomicFilters
} = useNotifications({ userId: 'current-user', autoFetch: true })

const atomicNotificationsForList = computed<AtomicNotification[]>(() => atomicNotifications.value)
const atomicNotificationsErrorMessage = computed(() => atomicNotificationsError.value?.message || null)

// Legacy store for compatibility
const isLoading = computed(() => notificationStore.isLoading)
const notifications = computed(() => notificationStore.sortedNotifications)
const hasUnreadNotifications = computed(() => notificationStore.hasUnreadNotifications)
const totalNotifications = computed(() => notifications.value.length)
const readNotificationsCount = computed(() => notificationStore.readNotifications.length)
const unreadNotificationsCount = computed(() => atomicUnreadCount.value)
const isRefreshingNotifications = computed(() => isLoading.value || atomicNotificationsLoading.value)

const tabs = computed(() => [
  { key: 'all' as const, label: t('notifications.tabs.all'), count: totalNotifications.value },
  { key: 'unread' as const, label: t('notifications.tabs.unread'), count: unreadNotificationsCount.value },
  { key: 'read' as const, label: t('notifications.tabs.read'), count: readNotificationsCount.value },
  { key: 'preferences' as const, label: t('notifications.tabs.preferences'), count: undefined }
])

const filteredNotifications = computed(() => {
  switch (activeTab.value) {
    case 'unread':
      return notificationStore.unreadNotifications
    case 'read':
      return notificationStore.readNotifications
    default:
      return notifications.value
  }
})

const legacyNotificationsForCenter = computed<Notification[]>(() =>
  filteredNotifications.value.map((notification) => ({
    id: notification.id,
    message: notification.message,
    timestamp: notification.created_at,
    type: 'system',
    read: notification.read,
    data: notification.data
  }))
)

const hasMoreNotifications = computed(() => {
  return notifications.value.length >= currentPage.value * pageSize
})

// Notification Center filters
const notificationFilters = computed<NotificationFilter[]>(() => [
  { id: 'all', label: t('notifications.filters.all') },
  { id: 'unread', label: t('notifications.filters.unread') },
  { id: 'read', label: t('notifications.filters.read') }
])

// Notification Settings
const globalNotificationsEnabled = computed(() => {
  return notificationStore.preferences.global_enabled === true
})

const notificationChannels = computed<NotificationChannels>(() => ({
  email: notificationStore.preferences.channels?.email === true,
  push: notificationStore.preferences.channels?.push === true,
  in_app: notificationStore.preferences.channels?.in_app === true
}))

const quietHours = computed(() => ({
  enabled: notificationStore.preferences.quiet_hours?.enabled === true,
  start: notificationStore.preferences.quiet_hours?.start || '22:00',
  end: notificationStore.preferences.quiet_hours?.end || '08:00'
}))

const isPushSupported = computed(() => notificationStore.isPushSupported)
const pushEnabled = computed(() => notificationStore.pushSubscriptions.length > 0)

const notificationCategories = computed<NotificationCategory[]>(() => {
  return Object.entries(notificationStore.preferences.categories || {}).map(([categoryKey, categoryValue]) => ({
    id: categoryKey,
    title: t(`notificationSettings.categories.${categoryKey}`, categoryKey),
    description: t(`notificationSettings.categoryDescriptions.${categoryKey}`, ''),
    enabled: categoryValue.enabled === true,
    channels: categoryValue.channels,
    types: Object.entries(categoryValue.types || {}).map(([typeKey, typeValue]) => ({
      type_key: typeKey,
      description: typeValue.description || typeKey,
      help_text: typeValue.help_text || '',
      enabled: typeValue.enabled === true
    }))
  }))
})

// Methods
const markAllAsRead = async () => {
  isMarkingAllAsRead.value = true
  try {
    await Promise.all([
      notificationStore.markAllAsRead(),
      markAllAtomicAsRead()
    ])
    await Promise.all([
      notificationStore.fetchNotifications(),
      notificationStore.fetchUnreadCount(),
      fetchAtomicNotifications(true)
    ])
  } catch (error) {
    console.error('Failed to mark all as read:', error)
  } finally {
    isMarkingAllAsRead.value = false
  }
}

const refreshNotifications = async () => {
  await Promise.all([
    notificationStore.fetchNotifications(),
    notificationStore.fetchUnreadCount(),
    fetchAtomicNotifications(true)
  ])
}

const loadMoreNotifications = async () => {
  isLoadingMore.value = true
  try {
    currentPage.value += 1
    await fetchAtomicNotifications()
  } catch (error) {
    console.error('Failed to load more notifications:', error)
  } finally {
    isLoadingMore.value = false
  }
}

// Wrapper functions for event signature conversion
const handleToggleGlobal = () => {
  const newEnabled = !globalNotificationsEnabled.value
  toggleGlobalNotifications(newEnabled)
}

const handleToggleCategory = (categoryId: string) => {
  const category = notificationStore.preferences.categories?.[categoryId]
  const newEnabled = !(category?.enabled === true)
  toggleCategory(categoryId, newEnabled)
}

const handleToggleChannel = (channel: string) => {
  const channelKey = channel as keyof NotificationChannels
  const newEnabled = !notificationChannels.value[channelKey]
  toggleChannel(channelKey, newEnabled)
}

const handleToggleType = (typeKey: string) => {
  const type = notificationStore.preferences.types?.[typeKey]
  const newEnabled = !(type?.enabled === true)
  toggleNotificationType(typeKey, newEnabled)
}

const toggleGlobalNotifications = async (enabled: boolean) => {
  isLoadingPreferences.value = true
  preferencesError.value = null
  try {
    await notificationStore.updatePreferences({ global_enabled: enabled })
  } catch (error) {
    preferencesError.value = error instanceof Error ? error.message : 'Failed to update global notifications'
  } finally {
    isLoadingPreferences.value = false
  }
}

const toggleCategory = async (categoryId: string, enabled: boolean) => {
  isLoadingPreferences.value = true
  preferencesError.value = null
  try {
    await notificationStore.updatePreferences({
      categories: {
        [categoryId]: {
          enabled
        }
      }
    })
  } catch (error) {
    preferencesError.value = error instanceof Error ? error.message : `Failed to update ${categoryId} category`
  } finally {
    isLoadingPreferences.value = false
  }
}

const toggleChannel = async (channel: keyof NotificationChannels, enabled: boolean) => {
  isLoadingPreferences.value = true
  preferencesError.value = null
  try {
    await notificationStore.updatePreferences({
      channels: {
        [channel]: enabled
      }
    })
  } catch (error) {
    preferencesError.value = error instanceof Error ? error.message : `Failed to update ${channel} channel`
  } finally {
    isLoadingPreferences.value = false
  }
}

const toggleNotificationType = async (typeKey: string, enabled: boolean) => {
  isLoadingPreferences.value = true
  preferencesError.value = null
  try {
    await notificationStore.updatePreferences({
      types: {
        [typeKey]: {
          enabled
        }
      }
    })
  } catch (error) {
    preferencesError.value = error instanceof Error ? error.message : `Failed to update ${typeKey} preference`
  } finally {
    isLoadingPreferences.value = false
  }
}

const handleToggleQuietHours = async () => {
  isLoadingPreferences.value = true
  preferencesError.value = null
  try {
    await notificationStore.updateQuietHours({
      enabled: !quietHours.value.enabled
    })
  } catch (error) {
    preferencesError.value = error instanceof Error ? error.message : 'Failed to update quiet hours'
  } finally {
    isLoadingPreferences.value = false
  }
}

const handleUpdateQuietHours = async (payload: { start?: string; end?: string }) => {
  isLoadingPreferences.value = true
  preferencesError.value = null
  try {
    await notificationStore.updateQuietHours(payload)
  } catch (error) {
    preferencesError.value = error instanceof Error ? error.message : 'Failed to update quiet hours'
  } finally {
    isLoadingPreferences.value = false
  }
}

const enablePushNotifications = async () => {
  try {
    // Check if push is supported
    if (!notificationStore.isPushSupported) {
      console.warn('Push notifications not supported')
      return
    }
    
    // Request permission
    const permission = await Notification.requestPermission()
    if (permission === 'granted') {
      console.log('Push notification permission granted')
      // In a real implementation, you would subscribe to push notifications here
    }
  } catch (error) {
    console.error('Failed to enable push notifications:', error)
  }
}

const handleNotificationClick = (notification: Notification) => {
  // Check if notification has data with a link
  if (notification.data?.link) {
    router.push(notification.data.link)
  }
}

const handleNotificationRead = async (notification: Notification) => {
  try {
    // Ensure id is a number
    const notificationId = typeof notification.id === 'string' ? parseInt(notification.id, 10) : notification.id
    await notificationStore.markAsRead(notificationId)
  } catch (error) {
    console.error('Failed to mark notification as read:', error)
  }
}

const handleNotificationDismiss = async (notification: Notification) => {
  try {
    // There's no dismissNotification method in the store, so we'll mark as read instead
    const notificationId = typeof notification.id === 'string' ? parseInt(notification.id, 10) : notification.id
    await notificationStore.markAsRead(notificationId)
  } catch (error) {
    console.error('Failed to dismiss notification:', error)
  }
}

const handleNotificationAction = (notification: Notification, action: { label: string }) => {
  console.log('Notification action:', notification, action)
  // Handle notification action based on action type
  if (action.label === 'mark-as-read') {
    handleNotificationRead(notification)
  } else if (action.label === 'dismiss') {
    handleNotificationDismiss(notification)
  } else if (action.label === 'view') {
    handleNotificationClick(notification)
  }
}

// Event handlers for atomic design notification components
const handleNotificationFiltersUpdate = (filters: NotificationFilterOptions) => {
  console.log('Notification filters updated:', filters)
  updateAtomicFilters(filters)
}

const handleNotificationSortUpdate = (field: NotificationSortField, direction: NotificationSortDirection) => {
  console.log('Notification sort updated:', field, direction)
  updateAtomicSort(field, direction)
}

const handleNotificationFiltersReset = () => {
  console.log('Notification filters reset')
  resetAtomicFilters()
}

const handleMarkAsRead = (notificationId: string) => {
  console.log('Mark as read:', notificationId)
  markAtomicAsRead(notificationId)
}

const handleMarkAllRead = () => {
  console.log('Mark all as read')
  markAllAtomicAsRead()
}

const handleArchiveNotification = (notificationId: string) => {
  console.log('Archive notification:', notificationId)
  // In a real implementation, you would call API to archive
  // For now, just remove from list
  // atomicNotifications.value = atomicNotifications.value.filter(n => n.id !== notificationId)
}

const handleDeleteNotification = (notificationId: string) => {
  console.log('Delete notification:', notificationId)
  // In a real implementation, you would call API to delete
  // For now, just remove from list
  // atomicNotifications.value = atomicNotifications.value.filter(n => n.id !== notificationId)
}

const handleFilterSelected = (filter: NotificationFilter) => {
  if (filter.id === 'all') activeTab.value = 'all'
  else if (filter.id === 'unread') activeTab.value = 'unread'
  else if (filter.id === 'read') activeTab.value = 'read'
}

// Lifecycle
onMounted(() => {
  notificationStore.fetchNotifications()
  notificationStore.fetchNotificationTypes()
  notificationStore.fetchPreferences()
})
</script>
