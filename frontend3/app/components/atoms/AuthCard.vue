<template>
  <div :class="[
    'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl shadow-sm',
    paddingClass,
    widthClass,
    className
  ]">
    <!-- Card Header (optional) -->
    <div v-if="$slots.header || title" class="border-b border-gray-200 dark:border-gray-700 px-6 py-4">
      <slot name="header">
        <h3 v-if="title" class="text-lg font-semibold text-gray-900 dark:text-white">
          {{ title }}
        </h3>
        <p v-if="subtitle" class="mt-1 text-sm text-gray-600 dark:text-gray-400">
          {{ subtitle }}
        </p>
      </slot>
    </div>

    <!-- Card Content -->
    <div :class="contentClass">
      <slot />
    </div>

    <!-- Card Footer (optional) -->
    <div v-if="$slots.footer" class="border-t border-gray-200 dark:border-gray-700 px-6 py-4">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  subtitle?: string
  padding?: 'none' | 'sm' | 'md' | 'lg'
  width?: 'full' | 'md' | 'lg' | 'xl'
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  padding: 'md',
  width: 'md',
  className: ''
})

const paddingClass = computed(() => {
  switch (props.padding) {
    case 'none': return 'p-0'
    case 'sm': return 'p-4'
    case 'md': return 'p-6'
    case 'lg': return 'p-8'
    default: return 'p-6'
  }
})

const widthClass = computed(() => {
  switch (props.width) {
    case 'full': return 'w-full'
    case 'md': return 'max-w-md'
    case 'lg': return 'max-w-lg'
    case 'xl': return 'max-w-xl'
    default: return 'max-w-md'
  }
})

const contentClass = computed(() => {
  switch (props.padding) {
    case 'none': return 'p-0'
    case 'sm': return 'p-4'
    case 'md': return 'p-6'
    case 'lg': return 'p-8'
    default: return 'p-6'
  }
})
</script>