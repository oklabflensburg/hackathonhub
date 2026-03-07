<template>
  <div class="notification-center" :class="centerClasses">
    <!-- Header -->
    <div class="notification-header" :class="headerClasses">
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <h3 class="notification-title" :class="titleClasses">
            Notifications
            <span v-if="unreadCount > 0" class="notification-badge">
              {{ unreadCount }}
            </span>
          </h3>
        </div>
        
        <div class="flex items-center space-x-2">
          <!-- Mark all as read -->
          <button
            v-if="showMarkAllAsRead && unreadCount > 0"
            type="button"
            class="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
            @click="$emit('mark-all-read')"
          >
            Mark all as read
          </button>
          
          <!-- Settings -->
          <button
            v-if="showSettings"
            type="button"
            class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            @click="$emit('settings')"
            aria-label="Notification settings"
          >
            <Icon
              name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' /><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15 12a3 3 0 11-6 0 3 3 0 016 0z' /></svg>"
              :size="16"
              is-svg
            />
          </button>
          
          <!-- Close -->
          <button
            v-if="showClose"
            type="button"
            class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            @click="$emit('close')"
            aria-label="Close notifications"
          >
            <Icon
              name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M6 18L18 6M6 6l12 12' /></svg>"
              :size="16"
              is-svg
            />
          </button>
        </div>
      </div>
      
      <!-- Filter tabs -->
      <div v-if="showFilters" class="notification-filters mt-4">
        <div class="flex space-x-2">
          <button
            v-for="filter in filters"
            :key="filter.id"
            class="px-3 py-1.5 text-sm font-medium rounded-full"
            :class="getFilterClasses(filter)"
            @click="selectFilter(filter)"
          >
            {{ filter.label }}
            <span v-if="filter.count !== undefined" class="ml-1">
              ({{ filter.count }})
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="notification-loading" :class="loadingClasses">
      <div class="flex flex-col items-center justify-center py-12">
        <div class="w-12 h-12 mb-4">
          <Skeleton variant="circle" size="lg" />
        </div>
        <Skeleton class="w-32 h-4 mb-2" />
        <Skeleton class="w-24 h-3" />
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="notifications.length === 0" class="notification-empty" :class="emptyClasses">
      <div class="flex flex-col items-center justify-center py-12 text-center">
        <Icon
          name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9' /></svg>"
          :size="48"
          is-svg
          class="text-gray-400 mb-4"
        />
        <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
          {{ emptyTitle || 'No notifications' }}
        </h4>
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          {{ emptyMessage || 'You\'re all caught up!' }}
        </p>
        <button
          v-if="showRefreshEmpty"
          type="button"
          class="px-4 py-2 text-sm font-medium rounded-md border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
          @click="$emit('refresh')"
        >
          Refresh
        </button>
      </div>
    </div>

    <!-- Notifications list -->
    <div v-else class="notification-list" :class="listClasses">
      <div class="divide-y divide-gray-200 dark:divide-gray-700">
        <div
          v-for="notification in filteredNotifications"
          :key="notification.id"
          class="notification-item"
          :class="getNotificationClasses(notification)"
          @click="handleNotificationClick(notification)"
        >
          <div class="flex">
            <!-- Icon -->
            <div class="notification-icon" :class="getIconClasses(notification)">
              <Icon
                :name="getNotificationIcon(notification)"
                :size="20"
                is-svg
              />
            </div>
            
            <!-- Content -->
            <div class="ml-3 flex-1">
              <div class="flex items-start justify-between">
                <div>
                  <p class="notification-message text-sm font-medium text-gray-900 dark:text-white">
                    {{ notification.message }}
                  </p>
                  
                  <div class="mt-1 flex items-center text-xs text-gray-500 dark:text-gray-400">
                    <Icon
                      name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' /></svg>"
                      :size="12"
                      is-svg
                      class="mr-1"
                    />
                    {{ formatTime(notification.timestamp) }}
                    
                    <span v-if="notification.source" class="ml-2">
                      • {{ notification.source }}
                    </span>
                  </div>
                </div>
                
                <!-- Actions -->
                <div class="flex items-center space-x-1 ml-2">
                  <!-- Mark as read/unread -->
                  <button
                    v-if="showMarkAsRead"
                    type="button"
                    class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                    @click.stop="toggleReadStatus(notification)"
                    :aria-label="notification.read ? 'Mark as unread' : 'Mark as read'"
                  >
                    <Icon
                      v-if="notification.read"
                      name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M3 19v-8.93a2 2 0 01.89-1.664l7-4.666a2 2 0 012.22 0l7 4.666A2 2 0 0121 10.07V19M3 19a2 2 0 002 2h14a2 2 0 002-2M3 19l6.75-4.5M21 19l-6.75-4.5M3 10l6.75 4.5M21 10l-6.75 4.5m0 0l-1.14.76a2 2 0 01-2.22 0l-1.14-.76' /></svg>"
                      :size="14"
                      is-svg
                    />
                    <Icon
                      v-else
                      name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' /></svg>"
                      :size="14"
                      is-svg
                    />
                  </button>
                  
                  <!-- Dismiss -->
                  <button
                    v-if="showDismiss"
                    type="button"
                    class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                    @click.stop="dismissNotification(notification)"
                    aria-label="Dismiss notification"
                  >
                    <Icon
                      name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M6 18L18 6M6 6l12 12' /></svg>"
                      :size="14"
                      is-svg
                    />
                  </button>
                </div>
              </div>
              
              <!-- Additional content -->
              <div v-if="notification.additionalContent" class="mt-2">
                <slot name="additional-content" :notification="notification">
                  <div class="text-xs text-gray-600 dark:text-gray-400">
                    {{ notification.additionalContent }}
                  </div>
                </slot>
              </div>
              
              <!-- Actions -->
              <div v-if="notification.actions && notification.actions.length > 0" class="mt-3 flex space-x-2">
                <button
                  v-for="action in notification.actions"
                  :key="action.label"
                  type="button"
                  class="px-3 py-1.5 text-xs font-medium rounded-md"
                  :class="getActionClasses(action)"
                  @click.stop="handleAction(notification, action)"
                >
                  {{ action.label }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div v-if="showFooter" class="notification-footer" :class="footerClasses">
      <slot name="footer">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-500 dark:text-gray-400">
            <slot name="footer-left">
              {{ footerText }}
            </slot>
          </div>
          
          <div class="flex items-center space-x-2">
            <slot name="footer-right">
              <button
                v-if="showViewAll"
                type="button"
                class="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
                @click="$emit('view-all')"
              >
                View All
              </button>
            </slot>
          </div>
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import Icon from '../../atoms/Icon.vue'
import Skeleton from '../../atoms/Skeleton.vue'

export interface NotificationAction {
  label: string
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info'
  handler?: () => void
}

export interface Notification {
  id: string | number
  message: string
  timestamp: Date | string
  type: 'info' | 'success' | 'warning' | 'error' | 'system' | 'user' | 'project' | 'team'
  read: boolean
  source?: string
  additionalContent?: string
  actions?: NotificationAction[]
  data?: any
}

export interface NotificationFilter {
  id: string
  label: string
  count?: number
  type?: string
}

export interface NotificationCenterProps {
  /** Array of notifications */
  notifications: Notification[]
  /** Number of unread notifications */
  unreadCount?: number
  /** Whether the notification center is loading */
  loading?: boolean
  /** Whether to show mark all as read button */
  showMarkAllAsRead?: boolean
  /** Whether to show settings button */
  showSettings?: boolean
  /** Whether to show close button */
  showClose?: boolean
  /** Whether to show filters */
  showFilters?: boolean
  /** Filter options */
  filters?: NotificationFilter[]
  /** Whether to show mark as read button on individual notifications */
  showMarkAsRead?: boolean
  /** Whether to show dismiss button on individual notifications */
  showDismiss?: boolean
  /** Whether to show footer */
  showFooter?: boolean
  /** Whether to show view all button */
  showViewAll?: boolean
  /** Whether to show refresh button in empty state */
  showRefreshEmpty?: boolean
  /** Empty state title */
  emptyTitle?: string
  /** Empty state message */
  emptyMessage?: string
  /** Footer text */
  footerText?: string
  /** Notification center variant */
  variant?: 'default' | 'dropdown' | 'sidebar' | 'modal'
  /** Maximum height for the notification list */
  maxHeight?: string
}

const props = withDefaults(defineProps<NotificationCenterProps>(), {
  notifications: () => [],
  unreadCount: 0,
  loading: false,
  showMarkAllAsRead: true,
  showSettings: true,
  showClose: true,
  showFilters: true,
  filters: () => [
    { id: 'all', label: 'All' },
    { id: 'unread', label: 'Unread' },
    { id: 'system', label: 'System' },
    { id: 'user', label: 'User' },
  ],
  showMarkAsRead: true,
  showDismiss: true,
  showFooter: false,
  showViewAll: true,
  showRefreshEmpty: true,
  emptyTitle: 'No notifications',
  emptyMessage: 'You\'re all caught up!',
  footerText: 'Last updated: Just now',
  variant: 'default',
  maxHeight: '400px',
})

const emit = defineEmits<{
  'mark-all-read': []
  'settings': []
  'close': []
  'refresh': []
  'view-all': []
  'notification-click': [notification: Notification]
  'notification-read': [notification: Notification, read: boolean]
  'notification-dismiss': [notification: Notification]
  'notification-action': [notification: Notification, action: NotificationAction]
  'filter-selected': [filter: NotificationFilter]
}>()

// Reactive state
const selectedFilter = ref<NotificationFilter>(props.filters[0] || { id: 'all', label: 'All' })

// Computed properties
const centerClasses = computed(() => {
  const classes = ['rounded-lg', 'overflow-hidden']
  const variantClasses = {
    default: 'bg-white dark:bg-gray-800 shadow-lg',
    dropdown: 'bg-white dark:bg-gray-800 shadow-xl',
    sidebar: 'bg-white dark:bg-gray-800 h-full',
    modal: 'bg-white dark:bg-gray-800 shadow-2xl'
  }
  classes.push(variantClasses[props.variant] || variantClasses.default)
  if (props.maxHeight) {
    classes.push(`max-h-[${props.maxHeight}]`)
  }
  return classes.join(' ')
})

const headerClasses = computed(() => '')
const titleClasses = computed(() => '')
const loadingClasses = computed(() => '')
const emptyClasses = computed(() => '')
const listClasses = computed(() => '')
const footerClasses = computed(() => '')

const filteredNotifications = computed(() => {
  if (selectedFilter.value.id === 'all') return props.notifications
  if (selectedFilter.value.id === 'unread') return props.notifications.filter(n => !n.read)
  if (selectedFilter.value.type) return props.notifications.filter(n => n.type === selectedFilter.value.type)
  return props.notifications
})

const getFilterClasses = (filter: NotificationFilter) => {
  const isActive = selectedFilter.value.id === filter.id
  return isActive
    ? 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300'
    : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
}

const selectFilter = (filter: NotificationFilter) => {
  selectedFilter.value = filter
  emit('filter-selected', filter)
}

const getNotificationClasses = (notification: Notification) => {
  const classes = ['cursor-pointer transition-colors duration-150']
  if (!notification.read) classes.push('bg-primary-50 dark:bg-primary-900/20')
  return classes.join(' ')
}

const handleNotificationClick = (notification: Notification) => {
  emit('notification-click', notification)
}

const getIconClasses = (notification: Notification) => {
  const typeClasses = {
    info: 'text-blue-500 bg-blue-100 dark:text-blue-400 dark:bg-blue-900/30',
    success: 'text-green-500 bg-green-100 dark:text-green-400 dark:bg-green-900/30',
    warning: 'text-yellow-500 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/30',
    error: 'text-red-500 bg-red-100 dark:text-red-400 dark:bg-red-900/30',
    system: 'text-gray-500 bg-gray-100 dark:text-gray-400 dark:bg-gray-800',
    user: 'text-purple-500 bg-purple-100 dark:text-purple-400 dark:bg-purple-900/30',
    project: 'text-indigo-500 bg-indigo-100 dark:text-indigo-400 dark:bg-indigo-900/30',
    team: 'text-pink-500 bg-pink-100 dark:text-pink-400 dark:bg-pink-900/30'
  }
  return `flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${typeClasses[notification.type] || typeClasses.info}`
}

const getNotificationIcon = (notification: Notification) => {
  const icons = {
    info: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    success: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    warning: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.346 16.5c-.77.833.192 2.5 1.732 2.5z" /></svg>',
    error: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    system: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>',
    user: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>',
    project: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>',
    team: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>'
  }
  return icons[notification.type] || icons.info
}

const formatTime = (timestamp: Date | string) => {
  const date = typeof timestamp === 'string' ? new Date(timestamp) : timestamp
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  
  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  return date.toLocaleDateString()
}

const toggleReadStatus = (notification: Notification) => {
  const newReadStatus = !notification.read
  emit('notification-read', notification, newReadStatus)
}

const dismissNotification = (notification: Notification) => {
  emit('notification-dismiss', notification)
}

const getActionClasses = (action: NotificationAction) => {
  const variantClasses = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600',
    success: 'bg-green-600 text-white hover:bg-green-700',
    warning: 'bg-yellow-600 text-white hover:bg-yellow-700',
    danger: 'bg-red-600 text-white hover:bg-red-700',
    info: 'bg-blue-600 text-white hover:bg-blue-700'
  }
  return `border border-transparent ${variantClasses[action.variant || 'primary']}`
}

const handleAction = (notification: Notification, action: NotificationAction) => {
  if (action.handler) action.handler()
  emit('notification-action', notification, action)
}
</script>