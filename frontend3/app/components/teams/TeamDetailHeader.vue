<template>
  <div class="flex flex-col md:flex-row md:items-start justify-between mb-8">
    <div>
      <div class="flex items-center mb-2">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ team.name }}</h1>
        <span :class="['ml-3 px-2 py-1 text-xs font-medium rounded-full', team.is_open ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300']">
          {{ team.is_open ? labels.open : labels.closed }}
        </span>
      </div>
      <p class="text-gray-600 dark:text-gray-400">
        {{ labels.teamFor }}
        <NuxtLink v-if="team.hackathon" :to="`/hackathons/${team.hackathon.id}`" class="text-primary-600 dark:text-primary-400 hover:underline">{{ team.hackathon.name }}</NuxtLink>
        <span v-else class="text-gray-500 dark:text-gray-400">{{ labels.unknownHackathon }}</span>
      </p>
    </div>

    <div class="mt-4 md:mt-0 flex space-x-3">
      <button v-if="isOwner" @click="$emit('edit')" class="btn btn-outline">{{ labels.editTeam }}</button>
      <button v-if="isMember" @click="$emit('leave')" class="btn btn-outline text-red-600 dark:text-red-400 border-red-300 dark:border-red-700 hover:bg-red-50 dark:hover:bg-red-900/20">{{ labels.leaveTeam }}</button>
      <button v-else-if="team.is_open && !isFull" @click="$emit('join')" class="btn btn-primary">{{ labels.joinTeam }}</button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ team: any; isOwner: boolean; isMember: boolean; isFull: boolean; labels: Record<string, string> }>()
defineEmits<{ (e: 'edit'): void; (e: 'leave'): void; (e: 'join'): void }>()
</script>
