<template>
  <button
    type="button"
    class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
    :aria-label="menuLabel"
    @click="$emit('toggle')"
  >
    <div class="w-9 h-9 rounded-full overflow-hidden border-2 border-white dark:border-gray-800 shadow-sm">
      <img v-if="avatarUrl" :src="avatarUrl" :alt="username" class="w-full h-full object-cover" />
      <div v-else class="w-full h-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center">
        <span class="text-primary-600 dark:text-primary-300 font-bold text-sm">{{ initials }}</span>
      </div>
    </div>
    <div class="hidden md:block text-left">
      <p class="font-medium text-gray-900 dark:text-white text-sm">{{ username }}</p>
      <p class="text-xs text-gray-500 dark:text-gray-400">{{ subtitle }}</p>
    </div>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  avatarUrl?: string | null
  username: string
  subtitle: string
  menuLabel: string
}

const props = withDefaults(defineProps<Props>(), {
  avatarUrl: null,
})

defineEmits<{ toggle: [] }>()

const initials = computed(() => props.username?.charAt(0)?.toUpperCase() || 'U')
</script>
