<template>
  <div v-if="prizes && prizes.length > 0" class="mb-8">
    <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ title }}</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="(prize, idx) in prizes"
        :key="idx"
        class="bg-gradient-to-br from-primary-50 to-purple-50 dark:from-gray-700 dark:to-gray-800 p-4 sm:p-5 lg:p-6 rounded-xl border border-primary-100 dark:border-gray-700"
      >
        <div class="flex items-center mb-3">
          <div class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center mr-3">
            <span class="text-primary-600 dark:text-primary-300 font-bold">{{ idx + 1 }}</span>
          </div>
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">{{ prize.name }}</h3>
        </div>
        <p class="text-gray-700 dark:text-gray-300">{{ prize.description }}</p>
        <div class="mt-3 text-primary-600 dark:text-primary-400 font-bold">{{ prize.value }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ title: string; prizes: Array<{ name: string; description: string; value: string }> }>()
</script>
