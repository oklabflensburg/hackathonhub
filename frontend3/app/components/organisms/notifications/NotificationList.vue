<template>
  <div class="notification-list">
    <!-- Loading State -->
    <div v-if="loading" class="space-y-4 p-4">
      <div v-for="i in 3" :key="i" class="animate-pulse">
        <div class="h-20 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="notifications.length === 0"
      class="text-center py-12"
    >
      <slot name="empty-state">
        <svg class="w-16 h-16 mx-auto text-gray-400 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        <h3 class="mt-4 text-lg font-medium text-gray-900 dark:text-white">
          {{ emptyTitle }}
        </h3>
        <p class="mt-2 text-gray-600 dark:text-gray-400 max-w-md mx-auto">
          {{ emptyMessage }}
        </p>
        <div v-if="showRefreshEmpty" class="mt-6">
          <button
            class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
            @click="$emit('refresh')"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Aktualisieren
          </button>
        </div>
      </slot>
    </div>

    <!-- Notifications List -->
    <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
      <div
        v-for="notification in filteredNotifications"
        :key="notification.id"
        class="notification-item p-4 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors cursor-pointer"
        :class="{
          'bg-gray-50 dark:bg-gray-800': notification.status === 'unread',
          'opacity-75': notification.status === 'archived'
        }"
        @click="handleNotificationClick(notification)"
      >
        <slot name="notification-item" :notification="notification">
          <!-- Default Notification Item -->
          <div class="flex gap-3">
            <!-- Icon/Avatar -->
            <div class="flex-shrink-0">
              <slot name="icon" :notification="notification">
                <div
                  v-if="notification.avatarUrl || notification.userAvatar"
                  class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden"
                >
                  <img
                    :src="notification.avatarUrl || notification.userAvatar"
                    :alt="notification.userName || 'Notification'"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div
                  v-else
                  class="w-10 h-10 rounded-full flex items-center justify-center bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300"
                >
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
              </slot>
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between">
                <div>
                  <h4 class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ notification.title }}
                  </h4>
                  <p class="mt-1 text-sm text-gray-600 dark:text-gray-300">
                    {{ notification.message }}
                  </p>
                </div>
                <div class="flex items-center gap-2 ml-2">
                  <!-- Status Badge -->
                  <span
                    v-if="notification.status === 'unread'"
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
                  >
                    Neu
                  </span>
                </div>
              </div>

              <!-- Metadata -->
              <div class="mt-2 flex items-center text-xs text-gray-500 dark:text-gray-400">
                <span class="flex items-center gap-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ formatDate(notification.createdAt) }}
                </span>
              </div>

              <!-- Action Buttons -->
              <div class="mt-3 flex items-center gap-3">
                <button
                  v-if="showMarkAsRead && notification.status === 'unread'"
                  class="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
                  @click.stop="$emit('notification-read', notification, true)"
                >
                  Als gelesen markieren
                </button>
                <button
                  v-if="showDismiss"
                  class="text-xs text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
                  @click.stop="$emit('notification-dismiss', notification)"
                >
                  Ausblenden
                </button>
              </div>
            </div>
          </div>
        </slot>
      </div>
    </div>

    <!-- Load More -->
    <div v-if="hasMore && !loading" class="p-4 text-center border-t border-gray-200 dark:border-gray-700">
      <button
        class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
        @click="$emit('load-more')"
      >
        Mehr laden
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Notification, NotificationFilterOptions } from '~/types/notification-types'

interface NotificationListProps {
  notifications: Notification[]
  loading?: boolean
  emptyTitle?: string
  emptyMessage?: string
  showRefreshEmpty?: boolean
  showMarkAsRead?: boolean
  showDismiss?: boolean
  hasMore?: boolean
  filterOptions?: NotificationFilterOptions
}

const props = withDefaults(defineProps<NotificationListProps>(), {
  loading: false,
  emptyTitle: 'Keine Benachrichtigungen',
  emptyMessage: 'Du bist auf dem neuesten Stand!',
  showRefreshEmpty: true,
  showMarkAsRead: true,
  showDismiss: true,
  hasMore: false,
  filterOptions: () => ({})
})

const emit = defineEmits<{
  'refresh': []
  'load-more': []
  'notification-click': [notification: Notification]
  'notification-read': [notification: Notification, read: boolean]
  'notification-dismiss': [notification: Notification]
  'notification-action': [notification: Notification, action: any]
}>()

// Filtered notifications based on filter options
const filteredNotifications = computed(() => {
  let filtered = [...props.notifications]

  // Apply filters
  const filters = props.filterOptions
  if (filters.type && filters.type.length > 0) {
    filtered = filtered.filter(n => filters.type!.includes(n.type))
  }
  if (filters.status && filters.status.length > 0) {
    filtered = filtered.filter(n => filters.status!.includes(n.status))
  }
  if (filters.search) {
    const search = filters.search.toLowerCase()
    filtered = filtered.filter(n => 
      n.title.toLowerCase().includes(search) ||
      n.message.toLowerCase().includes(search)
    )
  }

  // Apply sorting
  const sortBy = filters.sortBy || 'createdAt'
  const sortDirection = filters.sortDirection || 'desc'

  return filtered.sort((a, b) => {
    let aValue: any
    let bValue: any

    if (sortBy === 'type') {
      aValue = a.type
      bValue = b.type
    } else {
      aValue = new Date(a.createdAt).getTime()
      bValue = new Date(b.createdAt).getTime()
    }

    if (sortDirection === 'asc') {
      return aValue > bValue ? 1 : -1
    } else {
      return aValue < bValue ? 1 : -1
    }
  })
})

// Helper functions
const handleNotificationClick = (notification: Notification) => {
  emit('notification-click', notification)
}

const handleAction = (notification: Notification, action: any) => {
  emit('notification-action', notification, action)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.notification-list {
  @apply bg-white dark:bg-gray-900 rounded-lg shadow-sm;
}

.notification-item {
  @apply transition-colors duration-150;
}
</style>