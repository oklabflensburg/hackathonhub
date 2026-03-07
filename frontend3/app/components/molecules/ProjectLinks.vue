<template>
  <Card>
    <template v-if="title" #header>
      <h3 class="text-lg font-medium text-gray-900">{{ title }}</h3>
    </template>
    <div v-if="effectiveLinks.length > 0" class="space-y-2">
      <div v-for="link in effectiveLinks" :key="link.url" class="flex items-center gap-2">
        <Icon :name="getIcon(link.type)" size="20" class="text-gray-500" />
        <a
          :href="link.url"
          target="_blank"
          rel="noopener noreferrer"
          class="text-blue-600 hover:text-blue-800 hover:underline truncate"
        >
          {{ link.label || link.url }}
        </a>
        <Badge v-if="link.type" variant="secondary" size="sm">
          {{ link.type }}
        </Badge>
      </div>
    </div>
    <div v-else class="text-gray-500 text-sm">
      {{ emptyLabel }}
    </div>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Icon, Badge, Card } from '@/components/atoms'

interface ProjectLink {
  url: string
  label?: string
  type?: 'github' | 'demo' | 'website' | 'docs' | 'video' | 'other'
}

interface Props {
  links?: ProjectLink[]
  title?: string
  repositoryUrl?: string
  liveUrl?: string
  repositoryLabel?: string
  liveLabel?: string
  emptyLabel?: string
}

const props = withDefaults(defineProps<Props>(), {
  links: () => [],
  title: 'Project Links',
  repositoryLabel: 'GitHub Repository',
  liveLabel: 'Live Demo',
  emptyLabel: 'No links provided for this project'
})

const effectiveLinks = computed(() => {
  if (props.links && props.links.length > 0) {
    return props.links
  }
  const links: ProjectLink[] = []
  if (props.repositoryUrl) {
    links.push({
      url: props.repositoryUrl,
      label: props.repositoryLabel,
      type: 'github'
    })
  }
  if (props.liveUrl) {
    links.push({
      url: props.liveUrl,
      label: props.liveLabel,
      type: 'demo'
    })
  }
  return links
})

const getIcon = (type?: string) => {
  switch (type) {
    case 'github': return 'github'
    case 'demo': return 'external-link'
    case 'website': return 'globe'
    case 'docs': return 'file-text'
    case 'video': return 'video'
    default: return 'link'
  }
}
</script>