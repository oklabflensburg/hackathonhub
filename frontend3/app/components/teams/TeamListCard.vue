<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-lg transition-shadow duration-200">
    <div class="p-6">
      <div class="flex items-start justify-between mb-4">
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ team.name }}</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">{{ labels.inHackathon }}: {{ team.hackathon?.name || labels.unknown }}</p>
        </div>
        <span :class="['px-2 py-1 text-xs font-medium rounded-full', team.is_open ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300']">
          {{ team.is_open ? labels.open : labels.closed }}
        </span>
      </div>

      <p class="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">{{ team.description || labels.noDescription }}</p>

      <div class="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mb-4">
        <span>{{ team.member_count || 0 }} / {{ team.max_members }} {{ labels.members }}</span>
        <span>{{ formatDate(team.created_at) }}</span>
      </div>

      <div v-if="members.length > 0" class="mb-4 flex -space-x-2">
        <div v-for="member in members.slice(0, 5)" :key="member.id" class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 border-2 border-white dark:border-gray-800 flex items-center justify-center overflow-hidden" :title="member.user?.name || member.user?.username">
          <img v-if="member.user?.avatar_url" :src="member.user.avatar_url" :alt="member.user?.name || member.user?.username" class="w-full h-full object-cover" @error="$emit('avatar-error', $event)" />
          <span v-else class="text-xs font-medium text-primary-600 dark:text-primary-400">{{ (member.user?.name || member.user?.username || '?').charAt(0).toUpperCase() }}</span>
        </div>
      </div>

      <div class="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-700">
        <button @click="$emit('view', team.id)" class="text-sm font-medium text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300">{{ labels.viewDetails }}</button>
        <div class="flex items-center space-x-2">
          <button v-if="isMember" @click="$emit('leave', team.id)" class="text-sm px-3 py-1.5 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700">{{ labels.leaveTeam }}</button>
          <button v-else-if="team.is_open && !isFull" @click="$emit('join', team.id)" class="text-sm px-3 py-1.5 rounded-lg bg-primary-600 text-white hover:bg-primary-700">{{ labels.joinTeam }}</button>
          <span v-else-if="isFull" class="text-sm px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400">{{ labels.teamFull }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  team: any
  members: any[]
  isMember: boolean
  isFull: boolean
  formatDate: (v: string) => string
  labels: Record<string, string>
}>()

defineEmits<{ (e: 'view', id: number): void; (e: 'join', id: number): void; (e: 'leave', id: number): void; (e: 'avatar-error', ev: Event): void }>()
</script>
