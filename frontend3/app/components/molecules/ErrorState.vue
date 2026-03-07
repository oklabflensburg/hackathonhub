<template>
  <div class="flex flex-col items-center justify-center py-12 text-center">
    <div class="mb-4">
      <Icon name="alert-circle" :size="size === 'lg' ? 48 : size === 'md' ? 32 : 24" class="text-red-500" />
    </div>
    <h3 v-if="title" class="text-lg font-medium text-gray-900 mb-2">{{ title }}</h3>
    <p v-if="message" class="text-gray-600 max-w-md mb-4">{{ message }}</p>
    <div v-if="showRetry" class="flex gap-2">
      <Button variant="primary" @click="retry">
        {{ retryLabel }}
      </Button>
      <Button v-if="showHome" variant="ghost" @click="goHome">
        {{ homeLabel }}
      </Button>
    </div>
    <slot />
  </div>
</template>

<script setup lang="ts">
import Icon from '~/components/atoms/Icon.vue'
import Button from '~/components/atoms/Button.vue'

interface Props {
  title?: string
  message?: string
  showRetry?: boolean
  showHome?: boolean
  retryLabel?: string
  homeLabel?: string
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  showRetry: true,
  showHome: false,
  retryLabel: 'Try again',
  homeLabel: 'Go home',
  size: 'md'
})

const emit = defineEmits<{
  retry: []
  home: []
}>()

const retry = () => {
  emit('retry')
}

const goHome = () => {
  emit('home')
}
</script>