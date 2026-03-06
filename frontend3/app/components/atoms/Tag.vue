<template>
  <span :class="tagClasses">
    <span class="tag-content flex items-center gap-1.5">
      <slot>{{ text }}</slot>
      <button
        v-if="closable"
        type="button"
        class="tag-remove ml-1 p-0.5 rounded-full hover:bg-gray-200 dark:hover:bg-gray-800 focus:outline-none focus:ring-1 focus:ring-gray-300 dark:focus:ring-gray-700 transition-colors"
        :aria-label="removeAriaLabel"
        @click.stop="handleClose"
        @keydown.enter.stop="handleClose"
        @keydown.space.stop="handleClose"
      >
        <span class="remove-icon" aria-hidden="true">
          <svg
            class="w-3 h-3"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </span>
      </button>
    </span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  text?: string
  color?: 'primary' | 'success' | 'warning' | 'danger' | 'neutral'
  size?: 'sm' | 'md'
  closable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  text: '',
  color: 'neutral',
  size: 'md',
  closable: false,
})

const emit = defineEmits<{
  'close': []
}>()

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

const removeAriaLabel = computed(() => {
  return `Tag "${props.text}" entfernen`
})

const handleClose = (event: Event) => {
  event.stopPropagation()
  emit('close')
}
</script>
