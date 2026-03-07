<template>
  <div class="text-center py-8">
    <div
      :class="[
        'inline-flex items-center justify-center w-12 h-12 rounded-full mb-4',
        'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400'
      ]"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
      </svg>
    </div>

    <p class="text-gray-600 dark:text-gray-400">{{ error }}</p>

    <div>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">{{ authHint }}</p>
      <button @click="$emit('loginGithub')" class="mt-2 btn btn-primary">{{ githubLabel }}</button>
      <button @click="$emit('loginGoogle')" class="mt-2 ml-2 btn btn-outline">{{ googleLabel }}</button>
      <NuxtLink to="/login" class="mt-2 ml-2 btn btn-outline">{{ emailLabel }}</NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  error: string
  authHint: string
  githubLabel: string
  googleLabel: string
  emailLabel: string
}

defineProps<Props>()

defineEmits<{
  loginGithub: []
  loginGoogle: []
}>()
</script>