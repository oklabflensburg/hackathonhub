<template>
  <div class="inline-flex items-center gap-2 px-3 py-1.5 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-100 dark:border-blue-800">
    <Icon name="material-symbols:location-on" class="w-4 h-4 text-blue-500 dark:text-blue-400" />
    <div class="flex flex-col">
      <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ location }}</span>
      <span v-if="format" class="text-xs text-gray-500 dark:text-gray-400">{{ format }}</span>
    </div>
    <Badge v-if="isOnline" variant="success" size="sm">Online</Badge>
    <Badge v-else-if="isHybrid" variant="warning" size="sm">Hybrid</Badge>
  </div>
</template>

<script setup lang="ts">
import Icon from '~/components/atoms/Icon.vue'
import Badge from '~/components/atoms/Badge.vue'

interface Props {
  location: string
  format?: 'In-person' | 'Online' | 'Hybrid'
  isOnline?: boolean
  isHybrid?: boolean
}

withDefaults(defineProps<Props>(), {
  format: 'In-person',
  isOnline: false,
  isHybrid: false
})
</script>