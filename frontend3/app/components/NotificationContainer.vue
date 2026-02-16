<template>
  <div class="fixed top-4 right-4 z-50 space-y-3 w-full sm:w-96 max-w-full px-4 sm:px-0">
    <TransitionGroup name="notification">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-4 animate-slide-in"
        :class="{
          'border-green-200 dark:border-green-800': notification.type === 'success',
          'border-red-200 dark:border-red-800': notification.type === 'error',
          'border-yellow-200 dark:border-yellow-800': notification.type === 'warning',
          'border-blue-200 dark:border-blue-800': notification.type === 'info'
        }"
      >
        <div class="flex items-start justify-between">
          <div class="flex items-start space-x-3">
            <!-- Icon -->
            <div
              class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center"
              :class="{
                'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400': notification.type === 'success',
                'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400': notification.type === 'error',
                'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400': notification.type === 'warning',
                'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400': notification.type === 'info'
              }"
            >
              <svg v-if="notification.type === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else-if="notification.type === 'error'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <svg v-else-if="notification.type === 'warning'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.998-.833-2.732 0L4.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>

            <!-- Content -->
            <div class="flex-1">
              <h4 class="font-semibold text-gray-900 dark:text-white mb-1">
                {{ notification.title }}
              </h4>
              <p class="text-sm text-gray-600 dark:text-gray-300">
                {{ notification.message }}
              </p>
              
              <!-- Action Button -->
              <button
                v-if="notification.action"
                @click="notification.action.onClick"
                class="mt-2 text-sm font-medium"
                :class="{
                  'text-green-600 dark:text-green-400 hover:text-green-700 dark:hover:text-green-300': notification.type === 'success',
                  'text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300': notification.type === 'error',
                  'text-yellow-600 dark:text-yellow-400 hover:text-yellow-700 dark:hover:text-yellow-300': notification.type === 'warning',
                  'text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300': notification.type === 'info'
                }"
              >
                {{ notification.action.label }}
              </button>
            </div>
          </div>

          <!-- Close Button -->
          <button
            @click="removeNotification(notification.id)"
            class="flex-shrink-0 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            aria-label="Close notification"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Progress Bar -->
        <div
          v-if="notification.duration"
          class="mt-3 h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden"
        >
          <div
            class="h-full transition-all duration-linear"
            :class="{
              'bg-green-500': notification.type === 'success',
              'bg-red-500': notification.type === 'error',
              'bg-yellow-500': notification.type === 'warning',
              'bg-blue-500': notification.type === 'info'
            }"
            :style="{ width: '100%' }"
            @animationend="removeNotification(notification.id)"
          >
            <div class="h-full w-full animate-progress"></div>
          </div>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { useUIStore } from '~/stores/ui'

const uiStore = useUIStore()

const notifications = computed(() => uiStore.notifications)

const removeNotification = (id: string) => {
  uiStore.removeNotification(id)
}
</script>

<style scoped>
@keyframes progress {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

.animate-progress {
  animation: progress var(--duration, 5s) linear forwards;
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from,
.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.3s ease;
}
</style>