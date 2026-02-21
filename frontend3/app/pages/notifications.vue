<template>
  <div class="notifications-page">
    <!-- Header -->
    <div class="page-header">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            {{ $t('notifications.title') }}
          </h1>
          <p class="mt-2 text-gray-600 dark:text-gray-400">
            {{ $t('notifications.description') }}
          </p>
        </div>
        <div class="flex items-center space-x-4">
          <button v-if="hasUnreadNotifications" @click="markAllAsRead" :disabled="isMarkingAllAsRead"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed">
            <svg v-if="isMarkingAllAsRead" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none"
              viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            {{ $t('notifications.markAllAsRead') }}
          </button>
          <button @click="refreshNotifications" :disabled="isLoading"
            class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md shadow-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            <svg class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ $t('notifications.refresh') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-3">
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
                  {{ $t('notifications.totalNotifications') }}
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
                  {{ $t('notifications.readNotifications') }}
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
                  {{ $t('notifications.unreadNotifications') }}
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
    <div class="mt-8">
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="-mb-px flex space-x-8">
          <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key" :class="[
            'py-4 px-1 border-b-2 font-medium text-sm',
            activeTab === tab.key
              ? 'border-blue-500 text-blue-600 dark:text-blue-400'
              : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
          ]">
            {{ tab.label }}
            <span v-if="tab.count !== undefined" :class="[
              'ml-2 py-0.5 px-2 text-xs rounded-full',
              activeTab === tab.key
                ? 'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400'
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
          <NotificationSettings />
        </div>
      </template>
      <template v-else>
        <!-- Notifications List (for other tabs) -->
        <div>
          <!-- Loading State -->
          <div v-if="isLoading && notifications.length === 0" class="text-center py-12">
            <svg class="animate-spin mx-auto h-8 w-8 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            <p class="mt-4 text-gray-500 dark:text-gray-400">
              {{ $t('notifications.loading') }}
            </p>
          </div>

          <!-- Empty State -->
          <div v-else-if="filteredNotifications.length === 0" class="text-center py-12">
            <div class="mx-auto h-12 w-12 text-gray-400">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">
              {{ $t('notifications.noNotifications') }}
            </h3>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              {{ $t('notifications.noNotificationsDescription') }}
            </p>
            <div class="mt-6">
              <button @click="refreshNotifications"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                <svg class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                {{ $t('notifications.refresh') }}
              </button>
            </div>
          </div>

          <!-- Notifications List -->
          <div v-else class="space-y-4">
            <div v-for="notification in filteredNotifications" :key="notification.id" :class="[
              'notification-item bg-white dark:bg-gray-800 shadow-sm rounded-lg border',
              notification.read
                ? 'border-gray-200 dark:border-gray-700'
                : 'border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20'
            ]">
              <div class="p-4">
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <div class="flex items-center">
                      <!-- Notification Icon -->
                      <div :class="[
                        'notification-icon p-2 rounded-lg mr-3',
                        getNotificationIconClass(notification.notification_type)
                      ]">
                        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path :d="getNotificationIcon(notification.notification_type)" stroke-linecap="round"
                            stroke-linejoin="round" stroke-width="2" />
                        </svg>
                      </div>

                      <div class="flex-1">
                        <!-- Notification Header -->
                        <div class="flex items-center justify-between">
                          <h3 class="text-sm font-medium text-gray-900 dark:text-white">
                            {{ notification.title }}
                          </h3>
                          <div class="flex items-center space-x-2">
                            <span class="text-xs text-gray-500 dark:text-gray-400">
                              {{ formatDate(notification.created_at) }}
                            </span>
                            <span v-if="!notification.read"
                              class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">
                              {{ $t('notifications.unread') }}
                            </span>
                          </div>
                        </div>

                        <!-- Notification Message -->
                        <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
                          {{ notification.message }}
                        </p>

                        <!-- Notification Actions -->
                        <div class="mt-3 flex items-center space-x-4">
                          <button v-if="!notification.read" @click="markAsRead(notification.id)"
                            class="inline-flex items-center text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300">
                            <svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            {{ $t('notifications.markAsRead') }}
                          </button>

                          <button v-if="notification.data && hasAction(notification.data)"
                            @click="handleNotificationAction(notification)"
                            class="inline-flex items-center text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-300">
                            <svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                            </svg>
                            {{ getActionLabel(notification.data) }}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Channel Badge -->
                  <div class="ml-4">
                    <span :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      getChannelBadgeClass(notification.channel)
                    ]">
                      {{ getChannelLabel(notification.channel) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Load More -->
            <div v-if="hasMoreNotifications && !isLoading" class="mt-8 text-center">
              <button @click="loadMoreNotifications" :disabled="isLoadingMore"
                class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md shadow-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed">
                <svg v-if="isLoadingMore" class="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-500" fill="none"
                  viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                {{ $t('notifications.loadMore') }}
              </button>
            </div>
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
import NotificationSettings from '~/components/NotificationSettings.vue'

const router = useRouter()
const notificationStore = useNotificationStore()
const uiStore = useUIStore()
const { t } = useI18n()

// State
const activeTab = ref<'all' | 'unread' | 'read' | 'preferences'>('all')
const isMarkingAllAsRead = ref(false)
const isLoadingMore = ref(false)
const pageSize = 20
const currentPage = ref(1)

// Computed properties
const isLoading = computed(() => notificationStore.isLoading)
const notifications = computed(() => notificationStore.sortedNotifications)
const hasUnreadNotifications = computed(() => notificationStore.hasUnreadNotifications)
const totalNotifications = computed(() => notifications.value.length)
const readNotificationsCount = computed(() => notificationStore.readNotifications.length)
const unreadNotificationsCount = computed(() => notificationStore.unreadNotifications.length)

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

const hasMoreNotifications = computed(() => {
  return notifications.value.length >= currentPage.value * pageSize
})

// Methods
async function refreshNotifications() {
  await notificationStore.fetchNotifications()
  currentPage.value = 1
}

async function loadMoreNotifications() {
  isLoadingMore.value = true
  try {
    currentPage.value += 1
    await notificationStore.fetchNotifications({
      skip: (currentPage.value - 1) * pageSize,
      limit: pageSize
    })
  } catch (error) {
    console.error('Failed to load more notifications:', error)
    uiStore.showError(t('notifications.loadMoreError'))
  } finally {
    isLoadingMore.value = false
  }
}

async function markAsRead(notificationId: number) {
  await notificationStore.markAsRead(notificationId)
}

async function markAllAsRead() {
  isMarkingAllAsRead.value = true
  try {
    await notificationStore.markAllAsRead()
  } catch (error) {
    console.error('Failed to mark all notifications as read:', error)
    uiStore.showError(t('notifications.markAllAsReadError'))
  } finally {
    isMarkingAllAsRead.value = false
  }
}

function formatDate(dateString: string) {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) {
    return t('notifications.justNow')
  } else if (diffMins < 60) {
    return t('notifications.minutesAgo', { minutes: diffMins })
  } else if (diffHours < 24) {
    return t('notifications.hoursAgo', { hours: diffHours })
  } else if (diffDays < 7) {
    return t('notifications.daysAgo', { days: diffDays })
  } else {
    return date.toLocaleDateString()
  }
}

function getNotificationIcon(type: string) {
  const iconMap: Record<string, string> = {
    'team_invitation_sent': 'M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z',
    'team_invitation_accepted': 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
    'team_member_added': 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 1.197a6 6 0 00-9-5.197',
    'project_created': 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    'project_commented': 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
    'comment_reply': 'M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6',
    'vote_received': 'M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905a3.61 3.61 0 01-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5',
    'system_announcement': 'M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z',
    'security_alert': 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.998-.833-2.732 0L4.346 16.5c-.77.833.192 2.5 1.732 2.5z'
  }

  return iconMap[type] || 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9'
}

function getNotificationIconClass(type: string) {
  const classMap: Record<string, string> = {
    'team_invitation_sent': 'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400',
    'team_invitation_accepted': 'bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400',
    'team_member_added': 'bg-purple-100 dark:bg-purple-900 text-purple-600 dark:text-purple-400',
    'project_created': 'bg-yellow-100 dark:bg-yellow-900 text-yellow-600 dark:text-yellow-400',
    'project_commented': 'bg-indigo-100 dark:bg-indigo-900 text-indigo-600 dark:text-indigo-400',
    'comment_reply': 'bg-pink-100 dark:bg-pink-900 text-pink-600 dark:text-pink-400',
    'vote_received': 'bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400',
    'system_announcement': 'bg-gray-100 dark:bg-gray-900 text-gray-600 dark:text-gray-400',
    'security_alert': 'bg-orange-100 dark:bg-orange-900 text-orange-600 dark:text-orange-400'
  }

  return classMap[type] || 'bg-gray-100 dark:bg-gray-900 text-gray-600 dark:text-gray-400'
}

function getChannelBadgeClass(channel: string) {
  const classMap: Record<string, string> = {
    'email': 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200',
    'push': 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200',
    'in_app': 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200'
  }

  return classMap[channel] || 'bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200'
}

function getChannelLabel(channel: string) {
  const labelMap: Record<string, string> = {
    'email': t('notifications.channels.email'),
    'push': t('notifications.channels.push'),
    'in_app': t('notifications.channels.in_app')
  }

  return labelMap[channel] || channel
}

function hasAction(data: any) {
  return data && (data.project_id || data.team_id || data.hackathon_id || data.invitation_id)
}

function getActionLabel(data: any) {
  if (data.project_id) {
    return t('notifications.actions.viewProject')
  } else if (data.team_id) {
    return t('notifications.actions.viewTeam')
  } else if (data.hackathon_id) {
    return t('notifications.actions.viewHackathon')
  } else if (data.invitation_id) {
    return t('notifications.actions.viewInvitation')
  }
  return t('notifications.actions.view')
}

function handleNotificationAction(notification: any) {
  const data = notification.data || {}

  if (data.project_id) {
    router.push(`/projects/${data.project_id}`)
  } else if (data.team_id) {
    if (data.invitation_id) {
      router.push(`/teams/${data.team_id}/invitations`)
    } else {
      router.push(`/teams/${data.team_id}`)
    }
  } else if (data.hackathon_id) {
    router.push(`/hackathons/${data.hackathon_id}`)
  } else {
    // Default to notifications page
    router.push('/notifications')
  }

  // Mark as read if not already
  if (!notification.read) {
    markAsRead(notification.id)
  }
}

// Lifecycle
onMounted(async () => {
  await refreshNotifications()
})
</script>

<style scoped>
.notifications-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.page-header {
  @apply mb-8;
}

.stats-card {
  @apply transition-colors duration-200 hover:shadow-md;
}

.notification-item {
  @apply transition-all duration-200 hover:shadow-md;
}

.notification-icon {
  @apply flex-shrink-0;
}
</style>
