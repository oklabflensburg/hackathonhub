<template>
  <div class="notifications-page px-1 sm:px-0">
    <!-- Header -->
    <div class="page-header mb-6 sm:mb-8">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div class="min-w-0">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white sm:text-3xl">
            {{ t('notifications.title') }}
          </h1>
          <p class="mt-2 max-w-2xl text-sm text-gray-600 dark:text-gray-400 sm:text-base">
            {{ t('notifications.description') }}
          </p>
        </div>
        <div class="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:flex lg:flex-wrap lg:justify-end lg:gap-3">
          <button
            @click="router.push('/settings')"
            class="inline-flex min-h-10 items-center justify-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-lg shadow-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Einstellungen
          </button>
          <button v-if="hasUnreadNotifications" @click="markAllAsRead" :disabled="isMarkingAllAsRead"
            class="inline-flex min-h-10 items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed">
            <svg v-if="isMarkingAllAsRead" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none"
              viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            {{ t('notifications.markAllAsRead') }}
          </button>
          <button @click="refreshNotifications" :disabled="isRefreshingNotifications"
            class="inline-flex min-h-10 items-center justify-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-lg shadow-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:col-span-2 lg:col-span-1">
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
    <div class="mt-6 mb-6 grid grid-cols-1 gap-3 sm:mt-8 sm:mb-8 sm:grid-cols-3 sm:gap-5">
      <div class="stats-card overflow-hidden rounded-xl bg-white shadow dark:bg-gray-800">
        <div class="p-4 sm:p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="rounded-md bg-blue-500 p-2.5 sm:p-3">
                <svg class="h-5 w-5 text-white sm:h-6 sm:w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
              </div>
            </div>
            <div class="ml-4 w-0 flex-1 sm:ml-5">
              <dl>
                <dt class="truncate text-xs font-medium text-gray-500 dark:text-gray-400 sm:text-sm">
                  {{ t('notifications.totalNotifications') }}
                </dt>
                <dd class="text-base font-medium text-gray-900 dark:text-white sm:text-lg">
                  {{ totalNotifications }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="stats-card overflow-hidden rounded-xl bg-white shadow dark:bg-gray-800">
        <div class="p-4 sm:p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="rounded-md bg-green-500 p-2.5 sm:p-3">
                <svg class="h-5 w-5 text-white sm:h-6 sm:w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4 w-0 flex-1 sm:ml-5">
              <dl>
                <dt class="truncate text-xs font-medium text-gray-500 dark:text-gray-400 sm:text-sm">
                  {{ t('notifications.readNotifications') }}
                </dt>
                <dd class="text-base font-medium text-gray-900 dark:text-white sm:text-lg">
                  {{ readNotificationsCount }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="stats-card overflow-hidden rounded-xl bg-white shadow dark:bg-gray-800">
        <div class="p-4 sm:p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="rounded-md bg-yellow-500 p-2.5 sm:p-3">
                <svg class="h-5 w-5 text-white sm:h-6 sm:w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4 w-0 flex-1 sm:ml-5">
              <dl>
                <dt class="truncate text-xs font-medium text-gray-500 dark:text-gray-400 sm:text-sm">
                  {{ t('notifications.unreadNotifications') }}
                </dt>
                <dd class="text-base font-medium text-gray-900 dark:text-white sm:text-lg">
                  {{ unreadNotificationsCount }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="mb-6 mt-6 sm:mb-8 sm:mt-8">
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="-mb-px flex gap-6 overflow-x-auto whitespace-nowrap pb-1 scrollbar-none sm:gap-8">
          <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key" :class="[
            'border-b-2 px-1 py-3 text-sm font-medium sm:py-4',
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
    <div class="mt-6 sm:mt-8">
      <template>
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
          <div v-if="atomicNotifications.length > 0 && !atomicNotificationsLoading" class="mt-6 text-center sm:mt-8">
            <button @click="() => fetchAtomicNotifications()" :disabled="atomicNotificationsLoading"
              class="inline-flex min-h-10 items-center justify-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-lg shadow-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed">
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
import type { UserNotification } from '~/stores/notification'

const router = useRouter()
const notificationStore = useNotificationStore()
const uiStore = useUIStore()
const { t } = useI18n()

// State
const activeTab = ref<'all' | 'unread' | 'read'>('all')
const isMarkingAllAsRead = ref(false)
const isLoadingMore = ref(false)
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
  { key: 'read' as const, label: t('notifications.tabs.read'), count: readNotificationsCount.value }
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
})
</script>

<style scoped>
.scrollbar-none {
  scrollbar-width: none;
}

.scrollbar-none::-webkit-scrollbar {
  display: none;
}
</style>
