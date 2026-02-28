<template>
  <div>
    <h3 class="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4">{{ title }}</h3>
    <p class="text-gray-600 dark:text-gray-400 mb-4">{{ description }}</p>

    <form class="flex flex-col sm:flex-row" @submit.prevent="$emit('submit')">
      <input
        :value="email"
        type="email"
        :placeholder="placeholder"
        class="flex-1 min-w-0 px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-t-lg sm:rounded-l-lg sm:rounded-tr-none bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
        @input="$emit('update:email', ($event.target as HTMLInputElement).value)"
      >
      <button
        type="submit"
        :disabled="disabled"
        class="inline-flex items-center justify-center px-4 py-2 text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-b-lg sm:rounded-r-lg sm:rounded-bl-none"
      >
        {{ buttonLabel }}
      </button>
    </form>

    <p v-if="validationMessage" class="mt-2 text-sm" :class="validationClass">{{ validationMessage }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description: string
  placeholder: string
  email: string
  buttonLabel: string
  disabled: boolean
  validationMessage?: string
  validationClass?: string
}>()

defineEmits<{
  submit: []
  'update:email': [value: string]
}>()
</script>
