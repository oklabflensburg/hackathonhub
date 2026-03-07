<template>
  <Card v-if="technologies.length > 0">
    <template v-if="title" #header>
      <h3 class="text-lg font-medium text-gray-900">{{ title }}</h3>
    </template>
    <div class="flex flex-wrap gap-2">
      <Badge
        v-for="tech in technologies"
        :key="tech"
        variant="secondary"
      >
        {{ tech }}
      </Badge>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { Badge, Card } from '~/components/atoms'

interface Props {
  technologies: string[]
  title?: string
  icon?: string
}

withDefaults(defineProps<Props>(), {
  title: 'Technologies'
})
</script>