<template>
  <div class="profile-overview bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
    <!-- Header mit Avatar und Basisinformationen -->
    <div class="flex flex-col md:flex-row gap-6">
      <!-- Avatar -->
      <div class="flex-shrink-0">
        <div class="relative">
          <img
            :src="user.avatar_url || '/default-avatar.png'"
            :alt="displayName"
            class="w-32 h-32 rounded-full border-4 border-white dark:border-gray-700 shadow-md"
          />
          <div
            v-if="isCurrentUser"
            class="absolute bottom-0 right-0 bg-primary-500 text-white rounded-full p-2 cursor-pointer hover:bg-primary-600 transition-colors"
            @click="$emit('edit-profile')"
            title="Profil bearbeiten"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Benutzerinformationen -->
      <div class="flex-1">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ displayName }}
            </h1>
            <p class="text-gray-600 dark:text-gray-300 mt-1">
              {{ user.email }}
            </p>
            <p v-if="user.bio" class="text-gray-700 dark:text-gray-300 mt-3 max-w-2xl">
              {{ user.bio }}
            </p>
            <slot name="bio">
              <!-- Default bio content -->
            </slot>
          </div>

          <div v-if="isCurrentUser" class="flex gap-3">
            <Button
              variant="outline"
              size="sm"
              @click="$emit('edit-profile')"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Profil bearbeiten
            </Button>
            <Button
              variant="ghost"
              size="sm"
              @click="$emit('settings')"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Einstellungen
            </Button>
          </div>
        </div>

        <!-- Standort und Website -->
        <div class="flex flex-wrap gap-4 mt-4 text-sm text-gray-600 dark:text-gray-400">
          <div v-if="user.location" class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            {{ user.location }}
          </div>
          <div v-if="user.company" class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
            </svg>
            <span>{{ user.company }}</span>
          </div>
        </div>

        <!-- Social Links -->
        <div class="mt-4">
          <slot name="social-links">
            <div class="flex gap-3">
               <a
                v-if="user.github_id"
                :href="`https://github.com/${user.username}`"
                target="_blank"
                class="text-gray-700 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors"
                title="GitHub"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
                </svg>
              </a>
            </div>
          </slot>
        </div>
      </div>
    </div>

    <!-- Statistiken -->
    <div class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
      <slot name="stats">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <div class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ stats?.projectsSubmitted || 0 }}
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Projekte
            </div>
          </div>
          <div class="text-center p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <div class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ stats?.teamCount || 0 }}
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Teams
            </div>
          </div>
          <div class="text-center p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <div class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ stats?.hackathonsCreated || 0 }}
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Hackathons
            </div>
          </div>
          <div class="text-center p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <div class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ stats?.totalVotes || 0 }}
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Votes
            </div>
          </div>
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Button from '../../atoms/Button.vue'
import type { UserProfile, UserStats } from '~/types/user-types'

interface ProfileOverviewProps {
  user: UserProfile
  stats?: UserStats
  isCurrentUser: boolean
}

const props = defineProps<ProfileOverviewProps>()

const emit = defineEmits<{
  'edit-profile': []
  'settings': []
}>()

const displayName = computed(() => {
  return props.user.name || props.user.username || (props.user.email?.split('@')[0] ?? 'Benutzer')
})
</script>

<style scoped>
.profile-overview {
  transition: box-shadow 0.2s ease;
}

.profile-overview:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
</style>
