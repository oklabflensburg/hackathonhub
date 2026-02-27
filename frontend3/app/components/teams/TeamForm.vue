<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
    <form @submit.prevent="$emit('submit')">
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{{ labels.teamName }} *</label>
        <input v-model="form.name" type="text" :placeholder="labels.teamNamePlaceholder" class="w-full input" required :disabled="loading" />
        <p v-if="labels.teamNameHelp" class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ labels.teamNameHelp }}</p>
      </div>

      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{{ labels.description }}</label>
        <textarea v-model="form.description" :placeholder="labels.descriptionPlaceholder" rows="4" class="w-full input" :disabled="loading"></textarea>
        <p v-if="labels.descriptionHelp" class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ labels.descriptionHelp }}</p>
      </div>

      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{{ labels.hackathon }} *</label>
        <select v-model="form.hackathon_id" class="w-full input" required :disabled="loading || loadingHackathons || hackathons.length === 0">
          <option value="">{{ labels.selectHackathon }}</option>
          <option v-for="hackathon in hackathons" :key="hackathon.id" :value="hackathon.id">{{ hackathon.name }}</option>
        </select>
        <p v-if="labels.hackathonHelp" class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ labels.hackathonHelp }}</p>
      </div>

      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{{ labels.maxMembers }}</label>
        <div class="flex items-center space-x-4">
          <input v-model="form.max_members" type="range" min="1" max="10" class="w-full" :disabled="loading" />
          <span class="text-lg font-medium text-gray-700 dark:text-gray-300 min-w-[3rem]">{{ form.max_members }}</span>
        </div>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ labels.maxMembersHelp }}</p>
      </div>

      <div class="mb-6">
        <div class="flex items-center">
          <input v-model="form.is_open" type="checkbox" id="is_open" class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" :disabled="loading" />
          <label for="is_open" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">{{ labels.openTeam }}</label>
        </div>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ labels.openTeamHelp }}</p>
      </div>

      <div v-if="error" class="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
        <span class="text-red-600 dark:text-red-400">{{ error }}</span>
      </div>

      <div class="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
        <button type="button" @click="$emit('cancel')" class="btn btn-outline" :disabled="loading">{{ labels.cancel }}</button>
        <div class="flex space-x-3">
          <button v-if="showDelete" type="button" @click="$emit('delete')" class="btn btn-outline text-red-600 dark:text-red-400 border-red-300 dark:border-red-700 hover:bg-red-50 dark:hover:bg-red-900/20" :disabled="loading">{{ labels.delete }}</button>
          <button type="submit" class="btn btn-primary" :disabled="loading || !formValid">{{ loading ? labels.saving : labels.submit }}</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  form: any
  hackathons: any[]
  loading: boolean
  loadingHackathons?: boolean
  error?: string | null
  formValid: boolean
  showDelete?: boolean
  labels: Record<string, string>
}>()

defineEmits<{ (e: 'submit'): void; (e: 'cancel'): void; (e: 'delete'): void }>()
</script>
