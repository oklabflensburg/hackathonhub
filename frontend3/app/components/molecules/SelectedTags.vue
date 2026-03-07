<template>
  <div v-if="tags.length > 0" class="flex flex-wrap gap-2 items-center">
    <span class="text-sm text-gray-600">{{ label }}</span>
    <div class="flex flex-wrap gap-2">
      <Badge
        v-for="tag in tags"
        :key="tag"
        :label="tag"
        variant="primary"
        closable
        @close="removeTag(tag)"
      />
    </div>
    <Button
      v-if="showClearAll"
      variant="ghost"
      size="sm"
      @click="clearAll"
      class="text-sm text-gray-500 hover:text-gray-700"
    >
      {{ clearLabel }}
    </Button>
  </div>
</template>

<script setup lang="ts">
import Badge from '~/components/atoms/Badge.vue'
import Button from '~/components/atoms/Button.vue'

interface Props {
  tags: string[]
  label?: string
  showClearAll?: boolean
  clearLabel?: string
}

const props = withDefaults(defineProps<Props>(), {
  label: 'Selected:',
  showClearAll: true,
  clearLabel: 'Clear all'
})

const emit = defineEmits<{
  'update:tags': [string[]]
  'remove': [string]
  'clear': []
}>()

const removeTag = (tag: string) => {
  const newTags = props.tags.filter(t => t !== tag)
  emit('update:tags', newTags)
  emit('remove', tag)
}

const clearAll = () => {
  emit('update:tags', [])
  emit('clear')
}
</script>