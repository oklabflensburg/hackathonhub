<template>
  <div class="user-teams">
    <!-- Header mit Titel -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
          Teams
        </h2>
        <p v-if="!loading" class="text-sm text-gray-600 dark:text-gray-400 mt-1">
          {{ teams.length }} {{ teams.length === 1 ? 'Team' : 'Teams' }}
        </p>
      </div>

      <div class="flex gap-3">
        <Button
          variant="primary"
          size="sm"
          @click="$emit('create-team')"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Neues Team
        </Button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="animate-pulse">
        <div class="h-24 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="teams.length === 0"
      class="text-center py-12 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg"
    >
      <slot name="empty-state">
        <svg class="w-16 h-16 mx-auto text-gray-400 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <h3 class="mt-4 text-lg font-medium text-gray-900 dark:text-white">
          Keine Teams gefunden
        </h3>
        <p class="mt-2 text-gray-600 dark:text-gray-400 max-w-md mx-auto">
          {{ emptyMessage || 'Dieser Benutzer ist noch keinem Team beigetreten.' }}
        </p>
        <div class="mt-6">
          <Button
            variant="primary"
            @click="$emit('create-team')"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Erstes Team erstellen
          </Button>
        </div>
      </slot>
    </div>

    <!-- Teams Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="team in teams"
        :key="team.id"
        class="team-card bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow cursor-pointer"
        @click="$emit('team-click', team.id)"
      >
        <slot name="team-card" :team="team">
          <!-- Default Team Card -->
          <div class="p-5">
            <!-- Header mit Team-Name und Status -->
            <div class="flex justify-between items-start mb-3">
              <div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                  {{ team.name }}
                </h3>
                <div class="flex items-center gap-2">
                  <span
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                    :class="{
                      'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200': team.visibility === 'public',
                      'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200': team.visibility === 'private'
                    }"
                  >
                    {{ team.visibility === 'public' ? 'Öffentlich' : 'Privat' }}
                  </span>
                  <span
                    v-if="showRole && userRole(team)"
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200"
                  >
                    {{ formatRole(userRole(team)) }}
                  </span>
                </div>
              </div>
              <div class="flex gap-2">
                <button
                  class="p-1 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
                  @click.stop="$emit('edit-team', team.id)"
                  title="Team bearbeiten"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Team-Beschreibung -->
            <p v-if="team.description" class="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-2">
              {{ team.description }}
            </p>

            <!-- Mitglieder -->
            <div class="mb-4">
              <div class="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
                <span>Mitglieder</span>
                <span>{{ team.stats?.memberCount || 0 }} / {{ team.maxMembers || 10 }}</span>
              </div>
              <!-- Note: Team interface doesn't have members property, so we show placeholder avatars -->
              <div class="flex -space-x-2">
                <div
                  v-for="i in Math.min(team.stats?.memberCount || 0, 5)"
                  :key="i"
                  class="relative"
                >
                  <div class="w-8 h-8 rounded-full bg-gray-300 dark:bg-gray-600 border-2 border-white dark:border-gray-800 flex items-center justify-center text-xs text-gray-600 dark:text-gray-400">
                    {{ i }}
                  </div>
                </div>
                <div
                  v-if="(team.stats?.memberCount || 0) > 5"
                  class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 border-2 border-white dark:border-gray-800 flex items-center justify-center text-xs text-gray-600 dark:text-gray-400"
                >
                  +{{ (team.stats?.memberCount || 0) - 5 }}
                </div>
              </div>
            </div>

            <!-- Metadaten -->
            <div class="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
              <div class="flex items-center gap-4">
                <div class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                  <span>{{ team.stats?.projectCount || 0 }}</span>
                </div>
                <div class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span>{{ team.stats?.activeProjectCount || 0 }}</span>
                </div>
              </div>
              <div class="text-xs">
                {{ formatDate(team.createdAt) }}
              </div>
            </div>
          </div>
        </slot>
      </div>
    </div>

    <!-- Load More -->
    <div v-if="hasMore && !loading" class="mt-8 text-center">
      <Button
        variant="outline"
        @click="$emit('load-more')"
      >
        Mehr laden
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Team, TeamMember } from '~/types/team-types'
import Button from '~/components/atoms/Button.vue'

interface UserTeamsProps {
  teams: Team[]
  loading?: boolean
  emptyMessage?: string
  showRole?: boolean
  hasMore?: boolean
}

const props = withDefaults(defineProps<UserTeamsProps>(), {
  loading: false,
  emptyMessage: '',
  showRole: false,
  hasMore: false
})

const emit = defineEmits<{
  'team-click': [teamId: string]
  'create-team': []
  'edit-team': [teamId: string]
  'load-more': []
}>()

// In a real implementation, you would get the user's role from a separate API
// For now, we'll return a placeholder
const userRole = (team: Team): string | undefined => {
  // This is a placeholder - in reality you'd need to fetch team members separately
  return undefined
}

const formatRole = (role?: string) => {
  if (!role) return ''
  const roleMap: Record<string, string> = {
    'owner': 'Owner',
    'admin': 'Admin',
    'member': 'Mitglied',
    'viewer': 'Betrachter'
  }
  return roleMap[role] || role
}

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}
</script>

<style scoped>
.team-card {
  transition: all 0.2s ease;
}

.team-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}
</style>