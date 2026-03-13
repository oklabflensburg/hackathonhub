<template>
  <div class="fixed top-4 right-4 z-[100] space-y-2 w-96 max-w-full">
    <Alert
      v-for="notification in notifications"
      :key="notification.id"
      :type="notification.type"
      :title="notification.title"
      :message="notification.message"
      dismissible
      @dismiss="removeNotification(notification.id)"
    />
  </div>
</template>

<script setup lang="ts">
import { useUIStore } from '~/stores/ui'
import { Alert } from '~/components/atoms'

const uiStore = useUIStore()
const notifications = uiStore.notifications

const removeNotification = (id: string) => {
  uiStore.removeNotification(id)
}
</script>

<style scoped>
/* Optional: Add transition animations */
.alert-enter-active,
.alert-leave-active {
  transition: all 0.3s ease;
}
.alert-enter-from,
.alert-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>