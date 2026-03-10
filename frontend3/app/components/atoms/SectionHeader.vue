<template>
  <div class="flex items-center justify-between">
    <div>
      <h3
        :class="[
          'text-lg font-semibold leading-6',
          subtitle ? 'text-gray-900 dark:text-white' : 'text-gray-800 dark:text-gray-200'
        ]"
      >
        <slot name="title">{{ title }}</slot>
      </h3>
      <p
        v-if="subtitle || $slots.subtitle"
        class="mt-1 text-sm text-gray-500 dark:text-gray-400"
      >
        <slot name="subtitle">{{ subtitle }}</slot>
      </p>
    </div>
    <div v-if="$slots.actions" class="flex items-center space-x-2">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  subtitle?: string
}

withDefaults(defineProps<Props>(), {
  title: '',
  subtitle: ''
})
</script>