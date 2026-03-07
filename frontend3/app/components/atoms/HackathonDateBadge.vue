<template>
  <div class="inline-flex items-center gap-2 px-3 py-1.5 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
    <Icon :name="iconName" class="w-4 h-4 text-gray-500 dark:text-gray-400" />
    <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ formattedDate }}</span>
    <span v-if="showTime" class="text-xs text-gray-500 dark:text-gray-400">{{ formattedTime }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Icon from '~/components/atoms/Icon.vue'

interface Props {
  date: Date | string
  showTime?: boolean
  format?: 'short' | 'long' | 'relative'
  icon?: string
}

const props = withDefaults(defineProps<Props>(), {
  showTime: false,
  format: 'short',
  icon: 'material-symbols:calendar-month'
})

const dateObj = computed(() => {
  return typeof props.date === 'string' ? new Date(props.date) : props.date
})

const formattedDate = computed(() => {
  if (props.format === 'relative') {
    const now = new Date()
    const diff = dateObj.value.getTime() - now.getTime()
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))
    
    if (days === 0) return 'Today'
    if (days === 1) return 'Tomorrow'
    if (days === -1) return 'Yesterday'
    if (days > 0) return `In ${days} days`
    if (days < 0) return `${Math.abs(days)} days ago`
  }
  
  if (props.format === 'long') {
    return dateObj.value.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  }
  
  // short format
  return dateObj.value.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
})

const formattedTime = computed(() => {
  if (!props.showTime) return ''
  return dateObj.value.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  })
})

const iconName = computed(() => {
  if (props.icon) return props.icon
  return props.showTime ? 'material-symbols:calendar-clock' : 'material-symbols:calendar-month'
})
</script>