<template>
  <div class="relative">
    <img
      :src="src"
      :alt="alt"
      class="w-full h-auto rounded-lg shadow-lg"
      :class="{ 'cursor-pointer': clickable }"
      @click="clickable ? $emit('click') : null"
    />
    <div v-if="showOverlay" class="absolute inset-0 bg-black bg-opacity-30 rounded-lg flex items-center justify-center">
      <Button v-if="showViewButton" variant="primary" @click="$emit('view')">
        View Full Image
      </Button>
    </div>
    <div v-if="caption" class="mt-2 text-sm text-gray-500 text-center">{{ caption }}</div>
  </div>
</template>

<script setup lang="ts">
import Button from '~/components/atoms/Button.vue'

interface Props {
  src: string
  alt: string
  caption?: string
  clickable?: boolean
  showOverlay?: boolean
  showViewButton?: boolean
}

withDefaults(defineProps<Props>(), {
  clickable: false,
  showOverlay: false,
  showViewButton: false
})

defineEmits<{
  click: []
  view: []
}>()
</script>
