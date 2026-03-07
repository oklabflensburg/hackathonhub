<template>
  <NotificationCenter :notifications="notifications" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import NotificationCenter from '~/components/organisms/notifications/NotificationCenter.vue'
import type { Notification } from '~/components/organisms/notifications/NotificationCenter.vue'

const notifications = ref<Notification[]>([])
</script>