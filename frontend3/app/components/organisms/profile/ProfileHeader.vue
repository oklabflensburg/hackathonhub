<template>
  <div class="mb-8 flex justify-between items-start">
    <div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">{{ title }}</h1>
      <p v-if="subtitle" class="text-gray-600 dark:text-gray-400">{{ subtitle }}</p>
    </div>
    <div v-if="showEditButton && !isEditing">
      <Button
        :variant="editButtonVariant"
        :size="editButtonSize"
        @click="$emit('edit')"
      >
        <template #icon>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </template>
        {{ editButtonText }}
      </Button>
    </div>
    <div v-else-if="showActions" class="flex space-x-3">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from '../../atoms/Button.vue'

interface Props {
  title: string
  subtitle?: string
  showEditButton?: boolean
  isEditing?: boolean
  editButtonVariant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  editButtonSize?: 'sm' | 'md' | 'lg'
  editButtonText?: string
  showActions?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  subtitle: '',
  showEditButton: false,
  isEditing: false,
  editButtonVariant: 'primary',
  editButtonSize: 'md',
  editButtonText: 'Edit',
  showActions: false,
})

defineEmits<{
  edit: []
}>()
</script>