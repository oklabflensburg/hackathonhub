<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6 mb-6">
    <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">{{ profileInfoLabel }}</h2>
    <div class="space-y-6">
      <div class="flex items-start space-x-6">
        <Avatar :src="user?.avatar_url" :fallback-text="userInitials" size="xl" :alt="user.username" />
        <div>
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ user.username }}</h3>
          <p v-if="user.name" class="text-gray-600 dark:text-gray-400">{{ user.name }}</p>
          <p v-if="user.bio" class="text-gray-600 dark:text-gray-400 mt-2">{{ user.bio }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">{{ memberSinceLabel }} {{ formatDate(user.created_at) }}</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 pt-6 border-t border-gray-200 dark:border-gray-700">
        <div v-if="user.location"><h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ locationLabel }}</h4><p class="text-gray-900 dark:text-white">{{ user.location }}</p></div>
        <div v-if="user.company"><h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ companyLabel }}</h4><p class="text-gray-900 dark:text-white">{{ user.company }}</p></div>
        <div v-if="user.blog"><h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ websiteLabel }}</h4><a :href="user.blog" target="_blank" rel="noopener noreferrer" class="text-primary-600 dark:text-primary-400 hover:underline">{{ user.blog }}</a></div>
        <div v-if="user.twitter_username"><h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ twitterLabel }}</h4><a :href="`https://twitter.com/${user.twitter_username}`" target="_blank" rel="noopener noreferrer" class="text-primary-600 dark:text-primary-400 hover:underline">@{{ user.twitter_username }}</a></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Avatar from '~/components/atoms/Avatar.vue'
defineProps<{ user:any; userInitials:string; formatDate:(d:string)=>string; profileInfoLabel:string; memberSinceLabel:string; locationLabel:string; companyLabel:string; websiteLabel:string; twitterLabel:string }>()
</script>
