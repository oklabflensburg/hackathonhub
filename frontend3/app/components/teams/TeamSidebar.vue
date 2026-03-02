<template>
  <div class="space-y-6">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ t('teams.teamInfo') }}</h3>
      <div class="space-y-3">
        <div>
          <p class="text-sm text-gray-500 dark:text-gray-400">{{ t('teams.hackathon') }}</p>
          <p class="font-medium text-gray-900 dark:text-white">{{ team.hackathon?.name || t('teams.unknown') }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500 dark:text-gray-400">{{ t('teams.teamSize') }}</p>
          <p class="font-medium text-gray-900 dark:text-white">{{ members.length }} / {{ team.max_members }} {{ t('teams.members') }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500 dark:text-gray-400">{{ t('teams.status') }}</p>
          <p class="font-medium text-gray-900 dark:text-white">{{ team.is_open ? t('teams.openDescription') : t('teams.closedDescription') }}</p>
        </div>
      </div>
    </div>

    <div v-if="isOwner" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ t('teams.teamManagement') }}</h3>
      <div class="space-y-3">
        <button @click="$emit('edit')" class="w-full btn btn-outline justify-start">{{ t('teams.editTeamDetails') }}</button>
        <button @click="$emit('delete')" class="w-full btn btn-outline justify-start text-red-600 dark:text-red-400 border-red-300 dark:border-red-700 hover:bg-red-50 dark:hover:bg-red-900/20">{{ t('teams.deleteTeam') }}</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

defineProps<{ team: any; members: any[]; isOwner: boolean }>()
defineEmits<{ (e: 'edit'): void; (e: 'delete'): void }>()
</script>
