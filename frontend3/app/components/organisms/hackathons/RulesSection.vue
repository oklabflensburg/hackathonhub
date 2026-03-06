<template>
  <div v-if="rules">
    <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ title }}</h2>
    <div class="bg-gray-50 dark:bg-gray-700/50 p-4 sm:p-5 lg:p-6 rounded-xl">
      <div class="prose dark:prose-invert max-w-none">
        <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line">{{ rules }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { RulesSectionProps } from '~/types/hackathon-types'

defineProps<RulesSectionProps>()
</script>