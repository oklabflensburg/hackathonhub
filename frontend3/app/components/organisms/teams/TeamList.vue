<template>
  <div class="team-list">
    <!-- Loading State -->
    <div v-if="loading" class="space-y-6">
      <div
        v-for="i in 3"
        :key="i"
        class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 animate-pulse"
      >
        <div class="flex items-center space-x-4">
          <div class="w-16 h-16 bg-gray-300 dark:bg-gray-700 rounded-full"></div>
          <div class="flex-1 space-y-2">
            <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-1/4"></div>
            <div class="h-3 bg-gray-300 dark:bg-gray-700 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="!loading && teams.length === 0"
      class="text-center py-12"
    >
      <div class="mx-auto w-24 h-24 text-gray-400 dark:text-gray-600 mb-4">
        <svg
          class="w-full h-full"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
          />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
        {{ emptyTitle || $t('teams.list.emptyTitle') }}
      </h3>
      <p class="text-gray-500 dark:text-gray-400 mb-6 max-w-md mx-auto">
        {{ emptyMessage || $t('teams.list.emptyMessage') }}
      </p>
      <slot name="empty-actions">
        <button
          v-if="showCreateButton"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
          @click="handleCreateTeam"
        >
          {{ $t('teams.list.createTeam') }}
        </button>
      </slot>
    </div>

    <!-- Team Grid/List -->
    <div v-else>
      <!-- View Toggle -->
      <div
        v-if="showViewToggle"
        class="flex items-center justify-between mb-6"
      >
        <div class="text-sm text-gray-500 dark:text-gray-400">
          {{ $t('teams.list.showing', { count: teams.length, total: totalCount || teams.length }) }}
        </div>
        <div class="flex items-center space-x-2">
          <button
            :class="[
              'p-2 rounded-lg',
              viewMode === 'grid'
                ? 'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300'
                : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
            ]"
            @click="viewMode = 'grid'"
            :aria-label="$t('teams.list.gridView')"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
              />
            </svg>
          </button>
          <button
            :class="[
              'p-2 rounded-lg',
              viewMode === 'list'
                ? 'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300'
                : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
            ]"
            @click="viewMode = 'list'"
            :aria-label="$t('teams.list.listView')"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Grid View -->
      <div
        v-if="viewMode === 'grid'"
        :class="[
          'grid gap-6',
          {
            'grid-cols-1': columns === 1,
            'grid-cols-1 sm:grid-cols-2': columns === 2,
            'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3': columns === 3,
            'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4': columns === 4
          }
        ]"
      >
        <TeamCard
          v-for="team in teams"
          :key="team.id"
          :team="team"
          :current-user-id="currentUserId"
          :team-members="getTeamMembers(team.id)"
          :show-join-button="showJoinButtons"
          :show-members-preview="showMembersPreview"
          :show-more-actions="showMoreActions"
          :clickable="clickable"
          @click="handleTeamClick(team)"
          @join="handleTeamJoin(team)"
          @leave="handleTeamLeave(team)"
          @cancel="handleTeamCancel(team)"
          @more-actions="handleTeamMoreActions(team)"
          @view-team="handleViewTeam(team)"
        />
      </div>

      <!-- List View -->
      <div v-else class="space-y-4">
        <div
          v-for="team in teams"
          :key="team.id"
          class="bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200 dark:border-gray-700"
          :class="{ 'cursor-pointer': clickable }"
          @click="() => clickable && handleTeamClick(team)"
        >
          <div class="p-4">
            <div class="flex items-center justify-between">
              <!-- Team Info -->
              <div class="flex items-center space-x-4">
                <!-- Avatar -->
                <div class="relative">
                  <div
                    v-if="team.avatarUrl"
                    class="w-12 h-12 rounded-full border-2 border-white dark:border-gray-800 bg-white dark:bg-gray-700 overflow-hidden"
                  >
                    <img
                      :src="team.avatarUrl"
                      :alt="team.name"
                      class="w-full h-full object-cover"
                    />
                  </div>
                  <div
                    v-else
                    class="w-12 h-12 rounded-full border-2 border-white dark:border-gray-800 bg-gradient-to-r from-blue-400 to-purple-500 flex items-center justify-center"
                  >
                    <span class="text-white text-sm font-bold">
                      {{ getInitials(team.name) }}
                    </span>
                  </div>
                </div>

                <!-- Team Details -->
                <div>
                  <div class="flex items-center space-x-2">
                    <h3 class="font-medium text-gray-900 dark:text-gray-100">
                      {{ team.name }}
                    </h3>
                    <TeamBadge
                      :visibility="team.visibility"
                      :status="team.status"
                      size="sm"
                    />
                  </div>
                  <p
                    v-if="team.description"
                    class="text-sm text-gray-600 dark:text-gray-400 line-clamp-1"
                  >
                    {{ team.description }}
                  </p>
                  <div class="flex items-center space-x-4 mt-1">
                    <span class="text-xs text-gray-500 dark:text-gray-500">
                      {{ $t('teams.members') }}: {{ team.stats?.memberCount || 0 }}
                    </span>
                    <span class="text-xs text-gray-500 dark:text-gray-500">
                      {{ $t('teams.projects') }}: {{ team.stats?.projectCount || 0 }}
                    </span>
                    <span class="text-xs text-gray-500 dark:text-gray-500">
                      {{ formatDate(team.createdAt) }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex items-center space-x-2">
                <TeamJoinButton
                  v-if="showJoinButtons"
                  :team="team"
                  :current-user-id="currentUserId"
                  :is-member="isTeamMember(team.id)"
                  :is-pending="isTeamPending(team.id)"
                  size="sm"
                  @join="handleTeamJoin(team)"
                  @leave="handleTeamLeave(team)"
                  @cancel="handleTeamCancel(team)"
                />
                <button
                  v-if="showMoreActions"
                  class="p-1 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
                  @click.stop="handleTeamMoreActions(team)"
                  :aria-label="$t('common.moreActions')"
                >
                  <svg
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Tags -->
            <div
              v-if="team.tags && team.tags.length > 0"
              class="mt-3 flex flex-wrap gap-1"
            >
              <span
                v-for="tag in team.tags.slice(0, 3)"
                :key="tag"
                class="px-2 py-0.5 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded"
              >
                {{ tag }}
              </span>
              <span
                v-if="team.tags.length > 3"
                class="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded"
              >
                +{{ team.tags.length - 3 }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div
        v-if="showPagination && (hasNextPage || hasPreviousPage)"
        class="mt-8 flex items-center justify-between"
      >
        <button
          :disabled="!hasPreviousPage || loading"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors',
            hasPreviousPage && !loading
              ? 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
              : 'bg-gray-50 dark:bg-gray-900 text-gray-400 dark:text-gray-600 cursor-not-allowed'
          ]"
          @click="handlePreviousPage"
        >
          {{ $t('common.previous') }}
        </button>
        <div class="text-sm text-gray-500 dark:text-gray-400">
          {{ $t('common.pageOf', { page: currentPage, total: totalPages }) }}
        </div>
        <button
          :disabled="!hasNextPage || loading"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors',
            hasNextPage && !loading
              ? 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
              : 'bg-gray-50 dark:bg-gray-900 text-gray-400 dark:text-gray-600 cursor-not-allowed'
          ]"
          @click="handleNextPage"
        >
          {{ $t('common.next') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { Team, TeamMember } from '~/types/team-types'
import TeamCard from '~/components/organisms/teams/TeamCard.vue'
import TeamBadge from '~/components/atoms/teams/TeamBadge.vue'
import TeamJoinButton from '~/components/atoms/teams/TeamJoinButton.vue'

interface Props {
  teams: Team[]
  teamMembers?: TeamMember[]
  teamMembersMap?: Record<string, TeamMember[]>
  loading?: boolean
  currentUserId?: string | null
  columns?: 1 | 2 | 3 | 4
  showViewToggle?: boolean
  showJoinButtons?: boolean
  showMembersPreview?: boolean
  showMoreActions?: boolean
  showCreateButton?: boolean
  showPagination?: boolean
  clickable?: boolean
  emptyTitle?: string
  emptyMessage?: string
  // Pagination props
  currentPage?: number
  totalPages?: number
  totalCount?: number
  hasNextPage?: boolean
  hasPreviousPage?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  teams: () => [],
  teamMembers: () => [],
  teamMembersMap: () => ({}),
  loading: false,
  currentUserId: null,
  columns: 3,
  showViewToggle: true,
  showJoinButtons: true,
  showMembersPreview: true,
  showMoreActions: true,
  showCreateButton: false,
  showPagination: false,
  clickable: true,
  emptyTitle: '',
  emptyMessage: '',
  currentPage: 1,
  totalPages: 1,
  totalCount: 0,
  hasNextPage: false,
  hasPreviousPage: false
})

interface Emits {
  (e: 'team-click', team: Team): void
  (e: 'team-join', team: Team): void
  (e: 'team-leave', team: Team): void
  (e: 'team-cancel', team: Team): void
  (e: 'team-more-actions', team: Team): void
  (e: 'view-team', team: Team): void
  (e: 'create-team'): void
  (e: 'previous-page'): void
  (e: 'next-page'): void
}

const emit = defineEmits<Emits>()

const { t } = useI18n()

// Reactive state
const viewMode = ref<'grid' | 'list'>('grid')

// Computed properties
const isTeamMember = (teamId: string): boolean => {
  if (!props.currentUserId) return false
  const members = props.teamMembersMap?.[teamId] || props.teamMembers.filter(m => m.teamId === teamId)
  return members.some(member => member.userId === props.currentUserId)
}

const isTeamPending = (teamId: string): boolean => {
  // In a real implementation, we would check pending invitations
  return false
}

const getTeamMembers = (teamId: string): TeamMember[] => {
  return props.teamMembersMap?.[teamId] || props.teamMembers.filter(m => m.teamId === teamId)
}

// Methods
const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const handleCreateTeam = () => {
  emit('create-team')
}

const handleTeamClick = (team: Team) => {
  emit('team-click', team)
}

const handleTeamJoin = (team: Team) => {
  emit('team-join', team)
}

const handleTeamLeave = (team: Team) => {
  emit('team-leave', team)
}

const handleTeamCancel = (team: Team) => {
  emit('team-cancel', team)
}

const handleTeamMoreActions = (team: Team) => {
  emit('team-more-actions', team)
}

const handleViewTeam = (team: Team) => {
  emit('view-team', team)
}

const handlePreviousPage = () => {
  emit('previous-page')
}

const handleNextPage = () => {
  emit('next-page')
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>