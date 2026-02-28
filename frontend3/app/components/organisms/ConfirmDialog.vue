<template>
  <Modal
    :model-value="modelValue"
    :title="title"
    :description="description"
    :size="size"
    :show-close-button="false"
    :close-on-overlay-click="false"
    @update:model-value="$emit('update:modelValue', $event)"
    @close="$emit('cancel')"
  >
    <template #footer>
      <Button
        variant="secondary"
        :class="{ 'order-2 sm:order-1': destructive }"
        @click="$emit('cancel')"
      >
        {{ cancelText }}
      </Button>
      <Button
        :variant="destructive ? 'danger' : 'primary'"
        :class="{ 'order-1 sm:order-2': destructive }"
        :loading="loading"
        @click="$emit('confirm')"
      >
        {{ confirmText }}
      </Button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '~/components/molecules/Modal.vue'
import Button from '~/components/atoms/Button.vue'

interface Props {
  modelValue: boolean
  title: string
  description?: string
  confirmText?: string
  cancelText?: string
  destructive?: boolean
  loading?: boolean
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

withDefaults(defineProps<Props>(), {
  confirmText: 'Confirm',
  cancelText: 'Cancel',
  destructive: false,
  loading: false,
  size: 'md',
})

defineEmits<{
  'update:modelValue': [value: boolean]
  confirm: []
  cancel: []
}>()
</script>