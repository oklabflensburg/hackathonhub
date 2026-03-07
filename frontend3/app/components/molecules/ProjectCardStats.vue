<template>
  <div class="grid grid-cols-3 gap-4 py-4 border-t border-gray-100 dark:border-gray-800">
    <div class="text-center">
      <div class="text-xl font-bold text-gray-900 dark:text-white">{{ votes }}</div>
      <div class="text-xs text-gray-500 dark:text-gray-400">{{ votesLabel }}</div>
    </div>
    <div class="text-center">
      <div class="text-xl font-bold text-gray-900 dark:text-white">{{ comments }}</div>
      <div class="text-xs text-gray-500 dark:text-gray-400">{{ commentsLabel }}</div>
    </div>
    <div class="text-center">
      <div class="text-xl font-bold text-gray-900 dark:text-white">{{ views }}</div>
      <div class="text-xs text-gray-500 dark:text-gray-400">{{ viewsLabel }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  votes: number | string
  votesLabel?: string
  comments: number | string
  commentsLabel?: string
  views: number | string
  viewsLabel?: string
}

withDefaults(defineProps<Props>(), {
  votesLabel: 'Votes',
  commentsLabel: 'Comments',
  viewsLabel: 'Views'
})
</script>