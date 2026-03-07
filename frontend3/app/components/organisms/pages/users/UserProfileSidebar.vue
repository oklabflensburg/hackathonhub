<template>
  <div class="space-y-6">
    <NuxtLink v-if="isOwnProfile" to="/profile" class="w-full btn btn-primary block text-center">{{ viewOwnProfileLabel }}</NuxtLink>

    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ memberDetailsLabel }}</h3>
      <div class="space-y-3">
        <div><p class="text-sm text-gray-500 dark:text-gray-400">{{ memberSinceLabel }}</p><p class="font-medium text-gray-900 dark:text-white">{{ formatDate(user.created_at) }}</p></div>
        <div><p class="text-sm text-gray-500 dark:text-gray-400">{{ lastActiveLabel }}</p><p class="font-medium text-gray-900 dark:text-white">{{ formatDate(user.last_login) }}</p></div>
      </div>
    </div>

    <div v-if="user.email && isOwnProfile" class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ contactInfoLabel }}</h3>
      <div class="space-y-3">
        <div><p class="text-sm text-gray-500 dark:text-gray-400">{{ emailLabel }}</p><p class="font-medium text-gray-900 dark:text-white">{{ user.email }}</p></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ user:any; isOwnProfile:boolean; formatDate:(d:string)=>string; viewOwnProfileLabel:string; memberDetailsLabel:string; memberSinceLabel:string; lastActiveLabel:string; contactInfoLabel:string; emailLabel:string }>()
</script>
