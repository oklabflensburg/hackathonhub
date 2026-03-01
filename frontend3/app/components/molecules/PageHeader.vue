<template>
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
    <div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ title }}</h1>
      <p v-if="subtitle" class="text-gray-600 dark:text-gray-400 mt-2">
        {{ subtitle }}
      </p>
    </div>
    <div class="flex items-center space-x-4">
      <slot name="controls">
        <!-- Default controls slot -->
      </slot>
      <NuxtLink v-if="actionLink && actionLabel" :to="actionLink" class="btn btn-primary">
        <svg v-if="actionIcon" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        {{ actionLabel }}
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  subtitle?: string
  actionLabel?: string
  actionLink?: string
  actionIcon?: boolean
}

withDefaults(defineProps<Props>(), {
  subtitle: '',
  actionLabel: '',
  actionLink: '',
  actionIcon: true,
})
</script>