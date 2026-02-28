<template>
  <Card>
    <template #header>
      <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">{{ title }}</h2>
    </template>

    <div class="space-y-4">
      <div v-for="item in stats" :key="item.label">
        <p>{{ item.value }} {{ item.label }}</p>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Card from '~/components/atoms/Card.vue'

interface Props {
  title: string
  upvotes: number
  downvotes: number
  score: number
  comments: number
  views: number
  labels: {
    upvotes: string
    downvotes: string
    score: string
    comments: string
    views: string
  }
}

const props = defineProps<Props>()

const stats = computed(() => [
  { label: props.labels.upvotes, value: props.upvotes, type: 'upvotes' },
  { label: props.labels.downvotes, value: props.downvotes, type: 'downvotes' },
  { label: props.labels.score, value: props.score, type: 'score' },
  { label: props.labels.comments, value: props.comments, type: 'comments' },
  { label: props.labels.views, value: props.views, type: 'views' },
])
</script>
