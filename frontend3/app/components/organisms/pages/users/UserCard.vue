<template>
  <div class="card-hover group cursor-pointer" @click="$emit('open', user.id)">
    <div class="flex flex-col items-center text-center p-6">
      <div class="relative mb-4">
        <Avatar :src="user.avatar_url" :fallback-text="initials" size="xl" :alt="user.name || user.username" />
        <div v-if="user.is_admin" class="absolute -bottom-2 left-1/2 transform -translate-x-1/2">
          <span class="badge badge-warning text-xs px-2 py-1">{{ adminLabel }}</span>
        </div>
      </div>

      <h3 class="text-lg font-semibold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 mb-1">{{ user.name || user.username }}</h3>
      <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">@{{ user.username }}</p>
      <p v-if="user.bio" class="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">{{ user.bio }}</p>

      <div class="grid grid-cols-3 gap-4 w-full mt-4 pt-4 border-t border-gray-100 dark:border-gray-800">
        <div class="text-center"><div class="text-lg font-bold text-gray-900 dark:text-white">{{ user.project_count || 0 }}</div><div class="text-xs text-gray-500 dark:text-gray-400">{{ projectsLabel }}</div></div>
        <div class="text-center"><div class="text-lg font-bold text-gray-900 dark:text-white">{{ user.team_count || 0 }}</div><div class="text-xs text-gray-500 dark:text-gray-400">{{ teamsLabel }}</div></div>
        <div class="text-center"><div class="text-lg font-bold text-gray-900 dark:text-white">{{ user.hackathon_count || 0 }}</div><div class="text-xs text-gray-500 dark:text-gray-400">{{ hackathonsLabel }}</div></div>
      </div>

      <div v-if="user.location || user.company" class="flex flex-col items-center gap-2 mt-4 pt-4 border-t border-gray-100 dark:border-gray-800 w-full">
        <div v-if="user.location" class="text-sm text-gray-600 dark:text-gray-400">{{ user.location }}</div>
        <div v-if="user.company" class="text-sm text-gray-600 dark:text-gray-400">{{ user.company }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Avatar from '~/components/atoms/Avatar.vue'

const props = defineProps<{ user:any; adminLabel:string; projectsLabel:string; teamsLabel:string; hackathonsLabel:string }>()
defineEmits<{ (e:'open', id:number):void }>()

const initials = computed(() => {
  if (props.user.name) return props.user.name.split(' ').map((n: string) => n[0]).join('').toUpperCase().substring(0,2)
  return props.user.username.substring(0,2).toUpperCase()
})
</script>
