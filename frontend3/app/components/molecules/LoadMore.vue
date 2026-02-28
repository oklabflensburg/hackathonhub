<template>
  <div class="text-center pt-8">
    <button
      @click="$emit('load')"
      :disabled="loading"
      class="btn btn-outline px-8"
    >
      <svg v-if="loading" class="w-5 h-5 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
      </svg>
      {{ label }}
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  label?: string
  loading?: boolean
}

withDefaults(defineProps<Props>(), {
  label: 'Load more',
  loading: false,
})

defineEmits<{
  load: []
}>()
</script>