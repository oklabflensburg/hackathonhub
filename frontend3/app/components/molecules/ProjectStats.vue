<template>
  <Card>
    <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">{{ title }}</h3>
    <div class="space-y-4">
      <div class="flex justify-between items-center">
        <span class="text-gray-600 dark:text-gray-400">{{ labels.upvotes }}</span>
        <span class="font-bold text-gray-900 dark:text-white">{{ upvotes }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-600 dark:text-gray-400">{{ labels.downvotes }}</span>
        <span class="font-bold text-gray-900 dark:text-white">{{ downvotes }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-600 dark:text-gray-400">{{ labels.score }}</span>
        <span :class="scoreClass" class="font-bold">{{ score }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-600 dark:text-gray-400">{{ labels.comments }}</span>
        <span class="font-bold text-gray-900 dark:text-white">{{ comments }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-600 dark:text-gray-400">{{ labels.views }}</span>
        <span class="font-bold text-gray-900 dark:text-white">{{ views }}</span>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Card } from '~/components/atoms'

const props = defineProps<{
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
}>()

const scoreClass = computed(() => {
  if (props.score > 0) return 'text-green-600 dark:text-green-400'
  if (props.score < 0) return 'text-red-600 dark:text-red-400'
  return 'text-gray-600 dark:text-gray-400'
})
</script>