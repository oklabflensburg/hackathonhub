<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden aspect-ratio-16-9">
    <img
      v-if="!hasError"
      :src="src"
      :alt="alt"
      :title="title"
      class="img-cover"
      loading="lazy"
      @error="hasError = true"
    />

    <div v-else class="w-full h-full flex items-center justify-center bg-gray-100 dark:bg-gray-700">
      <div class="text-center px-4">
        <svg class="w-10 h-10 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-10h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <p class="text-sm text-gray-500 dark:text-gray-300">{{ placeholderText }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  src: string
  alt?: string
  title?: string
  placeholderText?: string
}

const props = withDefaults(defineProps<Props>(), {
  alt: 'Project image',
  title: '',
  placeholderText: 'No image available',
})

const hasError = ref(false)

watch(() => props.src, () => {
  hasError.value = false
})
</script>
