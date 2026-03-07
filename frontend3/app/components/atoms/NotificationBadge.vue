<template>
  <div class="relative">
    <button
      type="button"
      class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200 relative"
      :aria-label="unreadCount > 0 ? t('notifications.unreadCount', { count: unreadCount }) : t('notifications.noUnread')"
      @click="handleClick"
    >
      <svg
        class="w-5 h-5 sm:w-6 sm:h-6 text-gray-700 dark:text-gray-300"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
        />
      </svg>
      
      <!-- Unread count badge -->
      <span
        v-if="unreadCount > 0"
        class="absolute -top-1 -right-1 flex items-center justify-center min-w-5 h-5 px-1 text-xs font-bold text-white bg-red-500 rounded-full"
      >
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useNotificationStore } from '~/stores/notification'
import { useRouter } from '#imports'

const { t } = useI18n()
const notificationStore = useNotificationStore()
const router = useRouter()

const unreadCount = computed(() => notificationStore.unreadNotifications.length)

function handleClick() {
  router.push('/notifications')
}
</script>