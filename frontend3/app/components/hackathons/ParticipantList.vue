<template>
  <section class="mt-8">
    <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ title }}</h2>

    <div v-if="loading" class="text-center py-8">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      <p class="mt-2 text-gray-600 dark:text-gray-400">{{ loadingLabel }}</p>
    </div>

    <div v-else-if="error" class="text-center py-8">
      <div
        :class="[
          'inline-flex items-center justify-center w-12 h-12 rounded-full mb-4',
          requiresAuth
            ? 'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400'
            : 'bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400'
        ]"
      >
        <svg v-if="requiresAuth" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>

      <p class="text-gray-600 dark:text-gray-400">{{ error }}</p>

      <div v-if="requiresAuth">
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">{{ authHint }}</p>
        <button @click="$emit('loginGithub')" class="mt-2 btn btn-primary">{{ githubLabel }}</button>
        <button @click="$emit('loginGoogle')" class="mt-2 ml-2 btn btn-outline">{{ googleLabel }}</button>
        <NuxtLink to="/login" class="mt-2 ml-2 btn btn-outline">{{ emailLabel }}</NuxtLink>
      </div>
      <div v-else>
        <button @click="$emit('retry')" class="mt-4 btn btn-outline">{{ retryLabel }}</button>
      </div>
    </div>

    <div v-else-if="items.length === 0" class="text-center py-8">
      <p class="text-gray-600 dark:text-gray-400">{{ emptyLabel }}</p>
    </div>

    <div v-else class="space-y-4">
      <div v-for="team in items" :key="team.id" class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-5 border border-gray-200 dark:border-gray-600">
        <div class="flex items-start justify-between mb-2">
          <h3 class="font-semibold text-gray-900 dark:text-white">{{ team.name }}</h3>
          <span
            :class="[
              'px-2 py-1 rounded-full text-xs font-medium',
              team.is_open
                ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
            ]"
          >
            {{ team.is_open ? openLabel : closedLabel }}
          </span>
        </div>
        <p class="text-gray-600 dark:text-gray-400 text-sm mb-3 line-clamp-2">{{ team.description || noDescriptionLabel }}</p>
        <div class="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
          <span>{{ team.member_count || 0 }} / {{ team.max_members }} {{ membersLabel }}</span>
          <span class="text-xs">{{ createdPrefix }} {{ formatDate(team.created_at) }}</span>
        </div>
      </div>
    </div>

    <div v-if="items.length > 0" class="mt-6 text-center">
      <NuxtLink :to="viewAllPath" class="btn btn-outline">{{ viewAllLabel }}</NuxtLink>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  items: any[]
  loading: boolean
  error: string | null
  requiresAuth: boolean
  loadingLabel: string
  authHint: string
  githubLabel: string
  googleLabel: string
  emailLabel: string
  retryLabel: string
  emptyLabel: string
  openLabel: string
  closedLabel: string
  noDescriptionLabel: string
  membersLabel: string
  createdPrefix: string
  viewAllLabel: string
  viewAllPath: string
  formatDate: (dateString: string) => string
}>()

defineEmits<{
  (e: 'retry'): void
  (e: 'loginGithub'): void
  (e: 'loginGoogle'): void
}>()
</script>
