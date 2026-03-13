<template>
  <Modal :model-value="visible" @update:model-value="value => { if (!value) $emit('close') }" @close="$emit('close')">
    <div class="space-y-5">
      <div>
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">{{ title }}</h3>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">{{ description }}</p>
      </div>

      <label class="block space-y-2 text-sm">
        <span class="font-medium text-gray-700 dark:text-gray-200">Reason</span>
        <textarea v-model="localReason" rows="5" class="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 dark:border-gray-600 dark:bg-gray-900 dark:text-white" :placeholder="placeholder"></textarea>
      </label>

      <div class="flex justify-end gap-3">
        <button class="btn btn-outline" @click="$emit('close')">Cancel</button>
        <button class="btn btn-primary" :disabled="loading" @click="submit">{{ loading ? 'Submitting...' : submitLabel }}</button>
      </div>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Modal from '~/components/molecules/Modal.vue'

const props = withDefaults(defineProps<{
  visible: boolean
  title?: string
  description?: string
  placeholder?: string
  submitLabel?: string
  loading?: boolean
}>(), {
  title: 'Report content',
  description: 'Describe why you are reporting this content.',
  placeholder: 'Provide the reason for this report',
  submitLabel: 'Send report',
  loading: false,
})

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'submit', reason: string): void
}>()

const localReason = ref('')

watch(() => props.visible, (visible) => {
  if (visible) {
    localReason.value = ''
  }
})

function submit() {
  emit('submit', localReason.value.trim())
}
</script>
