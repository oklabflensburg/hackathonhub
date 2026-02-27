<template>
  <Card>
    <template #header>
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ title }}</h2>
    </template>
    <div class="grid grid-cols-2 gap-4 sm:grid-cols-3">
      <div v-for="item in stats" :key="item.label" class="text-center">
        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ item.value }}</p>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ item.label }}</p>
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
  { label: props.labels.upvotes, value: props.upvotes },
  { label: props.labels.downvotes, value: props.downvotes },
  { label: props.labels.score, value: props.score },
  { label: props.labels.comments, value: props.comments },
  { label: props.labels.views, value: props.views },
])
</script>
