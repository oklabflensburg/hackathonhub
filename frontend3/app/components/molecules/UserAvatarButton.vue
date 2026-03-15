<template>
  <button
    type="button"
    class="flex items-center space-x-1 sm:space-x-2 p-1.5 sm:p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
    :aria-label="menuLabel"
    @click="$emit('toggle')"
  >
    <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-full overflow-hidden border border-gray-200 dark:border-gray-700 shadow-sm">
      <img v-if="avatarUrl" :src="avatarUrl" :alt="username" class="w-full h-full object-cover" />
      <div v-else class="w-full h-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center">
        <span class="text-primary-600 dark:text-primary-300 font-bold text-sm">{{ initials }}</span>
      </div>
    </div>
    <span class="hidden sm:inline text-sm sm:text-base font-medium text-gray-700 dark:text-gray-300">
      {{ username }}
    </span>
    <svg
      class="w-4 h-4 sm:w-5 sm:h-5 text-gray-500 dark:text-gray-400 transition-transform"
      :class="{ 'rotate-180': open }"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
    </svg>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  avatarUrl?: string | null
  username: string
  subtitle: string
  menuLabel: string
  open?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  avatarUrl: null,
  open: false,
})

defineEmits<{ toggle: [] }>()

const initials = computed(() => props.username?.charAt(0)?.toUpperCase() || 'U')
</script>
