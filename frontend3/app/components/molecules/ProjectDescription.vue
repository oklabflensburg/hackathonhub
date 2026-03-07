<template>
  <Card>
    <template v-if="title" #header>
      <h3 class="text-lg font-medium text-gray-900">{{ title }}</h3>
    </template>
    <div class="space-y-4">
      <div class="prose prose-gray max-w-none">
        <div v-if="html" v-html="html" />
        <p v-else class="text-gray-700 whitespace-pre-line">{{ content }}</p>
      </div>
      <div v-if="features && features.length > 0" class="space-y-2">
        <h4 class="font-medium text-gray-900">Key Features</h4>
        <ul class="space-y-1">
          <li v-for="feature in features" :key="feature" class="flex items-start gap-2">
            <Icon name="check-circle" size="16" class="text-green-500 mt-0.5 flex-shrink-0" />
            <span class="text-gray-700">{{ feature }}</span>
          </li>
        </ul>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { Icon, Card } from '~/components/atoms'

interface Props {
  content?: string
  html?: string
  title?: string
  features?: string[]
}

withDefaults(defineProps<Props>(), {
  title: 'Description'
})
</script>
