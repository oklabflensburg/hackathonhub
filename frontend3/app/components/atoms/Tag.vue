<template>
  <span :class="tagClasses">
    <slot>{{ text }}</slot>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  text?: string
  color?: 'primary' | 'success' | 'warning' | 'danger' | 'neutral'
  size?: 'sm' | 'md'
}

const props = withDefaults(defineProps<Props>(), {
  text: '',
  color: 'neutral',
  size: 'md',
})

const colorMap = {
  primary: 'bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-300',
  success: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
  warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
  danger: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
  neutral: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300',
}

const sizeMap = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-3 py-1 text-sm',
}

const tagClasses = computed(() => ['inline-flex items-center rounded-full font-medium', colorMap[props.color], sizeMap[props.size]])
</script>
