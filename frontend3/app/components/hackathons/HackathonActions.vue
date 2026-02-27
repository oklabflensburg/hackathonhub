<template>
  <div class="space-y-4">
    <div>
      <div v-if="hackathon.status === 'completed'">
        <div v-if="isRegistered" class="w-full p-4 bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-800 rounded-xl text-center">
          <div class="flex items-center justify-center text-green-600 dark:text-green-400 mb-2">
            <span class="font-bold">{{ labels.registered }}</span>
          </div>
          <p class="text-sm text-green-700 dark:text-green-300">{{ labels.hackathonCompleted }}</p>
        </div>
        <div v-else class="w-full p-4 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl text-center">
          <div class="flex items-center justify-center text-gray-600 dark:text-gray-400 mb-2">
            <span class="font-bold">{{ labels.registrationClosed }}</span>
          </div>
          <p class="text-sm text-gray-700 dark:text-gray-300">{{ labels.hackathonCompleted }}</p>
        </div>
      </div>
      <div v-else>
        <button v-if="!isRegistered" class="w-full btn btn-primary" @click="$emit('register')" :disabled="registrationLoading">
          {{ registrationLoading ? labels.registering : labels.registerNow }}
        </button>
        <div v-else class="w-full p-4 bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-800 rounded-xl text-center">
          <div class="flex items-center justify-center text-green-600 dark:text-green-400 mb-2">
            <span class="font-bold">{{ labels.registered }}</span>
          </div>
          <p class="text-sm text-green-700 dark:text-green-300">{{ labels.alreadyRegistered }}</p>
        </div>
      </div>
    </div>

    <button v-if="isHackathonOwner" class="w-full btn btn-outline flex items-center justify-center" @click="$emit('edit')">
      {{ labels.editHackathon }}
    </button>

    <NuxtLink :to="`/hackathons/${id}/projects`" class="w-full btn btn-outline flex items-center justify-center">
      {{ labels.viewProjects }}
    </NuxtLink>

    <button class="w-full btn btn-outline flex items-center justify-center" @click="$emit('share')">
      {{ labels.shareHackathon }}
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  id: string
  hackathon: any
  isRegistered: boolean
  registrationLoading: boolean
  isHackathonOwner: boolean
  labels: Record<string, string>
}>()

defineEmits<{
  (e: 'register'): void
  (e: 'edit'): void
  (e: 'share'): void
}>()
</script>
