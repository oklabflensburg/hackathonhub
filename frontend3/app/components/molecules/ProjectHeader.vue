<template>
  <div class="space-y-4">
    <div class="flex items-start justify-between">
      <div class="space-y-2">
        <h1 class="text-3xl font-bold text-gray-900">{{ title }}</h1>
        <div v-if="subtitle" class="text-lg text-gray-600">{{ subtitle }}</div>
        <div v-if="tags && tags.length > 0" class="flex flex-wrap gap-2">
          <Badge
            v-for="tag in tags"
            :key="tag"
            :label="tag"
            variant="secondary"
          />
        </div>
      </div>
      <div v-if="showActions" class="flex gap-2">
        <slot name="actions">
          <Button v-if="editLabel" variant="outline" @click="edit">
            {{ editLabel }}
          </Button>
          <Button v-if="deleteLabel" variant="danger" @click="deleteProject">
            {{ deleteLabel }}
          </Button>
        </slot>
      </div>
    </div>
    <div v-if="meta" class="flex flex-wrap gap-4 text-sm text-gray-500">
      <div v-if="meta.author" class="flex items-center gap-1">
        <Icon name="user" size="16" />
        <span>{{ meta.author }}</span>
      </div>
      <div v-if="meta.date" class="flex items-center gap-1">
        <Icon name="calendar" size="16" />
        <span>{{ meta.date }}</span>
      </div>
      <div v-if="meta.views" class="flex items-center gap-1">
        <Icon name="eye" size="16" />
        <span>{{ meta.views }} views</span>
      </div>
      <div v-if="meta.likes" class="flex items-center gap-1">
        <Icon name="heart" size="16" />
        <span>{{ meta.likes }} likes</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Badge from '~/components/atoms/Badge.vue'
import Button from '~/components/atoms/Button.vue'
import Icon from '~/components/atoms/Icon.vue'

interface Meta {
  author?: string
  date?: string
  views?: number
  likes?: number
}

interface Props {
  title: string
  subtitle?: string
  tags?: string[]
  showActions?: boolean
  editLabel?: string
  deleteLabel?: string
  meta?: Meta
}

const props = defineProps<Props>()

const emit = defineEmits<{
  edit: []
  delete: []
}>()

const edit = () => {
  emit('edit')
}

const deleteProject = () => {
  emit('delete')
}
</script>