<template>
  <div class="flex items-center gap-2 text-gray-700 dark:text-gray-300">
    <Icon name="calendar" class="w-4 h-4" />
    <span class="font-medium">{{ formattedDate }}</span>
    <span v-if="showTime" class="text-sm text-gray-500 dark:text-gray-400">
      {{ formattedTime }}
    </span>
    <Badge v-if="showStatus" :variant="statusVariant" size="sm">
      {{ statusText }}
    </Badge>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { format } from 'date-fns'
import { de } from 'date-fns/locale'
import Icon from '~/components/atoms/Icon.vue'
import Badge from '~/components/atoms/Badge.vue'

interface Props {
  date: Date | string
  showTime?: boolean
  showStatus?: boolean
  format?: 'short' | 'medium' | 'long' | 'relative'
  locale?: string
}

const props = withDefaults(defineProps<Props>(), {
  showTime: false,
  showStatus: false,
  format: 'medium',
  locale: 'de'
})

const dateObj = computed(() => {
  return typeof props.date === 'string' ? new Date(props.date) : props.date
})

const formattedDate = computed(() => {
  const date = dateObj.value
  const locale = props.locale === 'de' ? de : undefined
  
  switch (props.format) {
    case 'short':
      return format(date, 'dd.MM.yy', { locale })
    case 'medium':
      return format(date, 'dd. MMMM yyyy', { locale })
    case 'long':
      return format(date, 'EEEE, dd. MMMM yyyy', { locale })
    case 'relative':
      return getRelativeTime(date)
    default:
      return format(date, 'dd. MMMM yyyy', { locale })
  }
})

const formattedTime = computed(() => {
  const date = dateObj.value
  return format(date, 'HH:mm')
})

const statusVariant = computed(() => {
  const now = new Date()
  const date = dateObj.value
  
  if (date < now) {
    return 'gray' // Vergangen
  }
  
  const oneWeekFromNow = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)
  if (date < oneWeekFromNow) {
    return 'warning' // Bald
  }
  
  return 'success' // Zukunft
})

const statusText = computed(() => {
  const now = new Date()
  const date = dateObj.value
  
  if (date < now) {
    return 'Beendet'
  }
  
  const oneWeekFromNow = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)
  if (date < oneWeekFromNow) {
    return 'Bald'
  }
  
  return 'Kommt'
})

function getRelativeTime(date: Date): string {
  const now = new Date()
  const diffMs = date.getTime() - now.getTime()
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) {
    const daysAgo = Math.abs(diffDays)
    return `vor ${daysAgo} Tag${daysAgo !== 1 ? 'en' : ''}`
  } else if (diffDays === 0) {
    return 'Heute'
  } else if (diffDays === 1) {
    return 'Morgen'
  } else if (diffDays < 7) {
    return `in ${diffDays} Tagen`
  } else if (diffDays < 30) {
    const weeks = Math.floor(diffDays / 7)
    return `in ${weeks} Woche${weeks !== 1 ? 'n' : ''}`
  } else {
    const months = Math.floor(diffDays / 30)
    return `in ${months} Monat${months !== 1 ? 'en' : ''}`
  }
}
</script>

<style scoped>
/* Additional styling if needed */
</style>