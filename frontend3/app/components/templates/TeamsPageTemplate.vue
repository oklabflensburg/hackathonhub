<template>
  <div class="teams-page-template">
    <!-- Page Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
            {{ title || $t('teams.page.title') }}
          </h1>
          <p
            v-if="description"
            class="text-gray-600 dark:text-gray-400 mt-2"
          >
            {{ description }}
          </p>
        </div>
        <div class="flex items-center space-x-4">
          <!-- Search Input -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg
                class="h-5 w-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
            <input
              v-model="searchQuery"
              type="search"
              :placeholder="$t('teams.page.searchPlaceholder')"
              class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              @input="handleSearch"
            />
          </div>

          <!-- Create Team Button -->
          <button
            v-if="showCreateButton"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center"
            @click="handleCreateTeam"
          >
            <svg
              class="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
            {{ $t('teams.page.createTeam') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Filters and Controls -->
    <div class="mb-8">
      <div class="flex flex-col md:flex-row md:items-center justify-between space-y-4 md:space-y-0">
        <!-- Filter Tabs -->
        <div class="flex space-x-2 overflow-x-auto">
          <button
            v-for="filter in filters"
            :key="filter.id"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap',
              activeFilter === filter.id
                ? 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-300'
                : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
            ]"
            @click="handleFilterChange(filter.id)"
          >
            {{ filter.label }}
            <span
              v-if="filter.count !== undefined"
              :class="[
                'ml-2 px-2 py-0.5 text-xs rounded-full',
                activeFilter === filter.id
                  ? 'bg-blue-200 dark:bg-blue-800 text-blue-900 dark:text-blue-200'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-400'
              ]"
            >
              {{ filter.count }}
            </span>
          </button>
        </div>

        <!-- Sort and View Controls -->
        <div class="flex items-center space-x-4">
          <!-- Sort Dropdown -->
          <div class="relative">
            <select
              v-model="sortOption"
              class="appearance-none bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg px-4 py-2 pr-8 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              @change="handleSortChange"
            >
              <option
                v-for="option in sortOptions"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
            <div class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
              <svg
                class="h-5 w-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </div>
          </div>

          <!-- View Toggle -->
          <div class="flex items-center space-x-1 bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
            <button
              :class="[
                'p-2 rounded transition-colors',
                viewMode === 'grid'
                  ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
              ]"
              @click="viewMode = 'grid'"
              :aria-label="$t('teams.page.gridView')"
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
                'p-2 rounded transition-colors',
                viewMode === 'list'
                  ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
              ]"
              @click="viewMode = 'list'"
              :aria-label="$t('teams.page.listView')"
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
      </div>
    </div>

    <!-- Main Content -->
    <div class="mb-8">
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
          {{ emptyTitle || $t('teams.page.emptyTitle') }}
        </h3>
        <p class="text-gray-500 dark:text-gray-400 mb-6 max-w-md mx-auto">
          {{ emptyMessage || $t('teams.page.emptyMessage') }}
        </p>
        <slot name="empty-actions">
          <button
            v-if="showCreateButton"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
            @click="handleCreateTeam"
          >
            {{ $t('teams.page.createTeam') }}
          </button>
        </slot>
      </div>

      <!-- Teams List -->
      <div v-else>
        <TeamList
          :teams="teams"
          :team-members="teamMembers"
          :team-members-map="teamMembersMap"
          :loading="loading"
          :current-user-id="currentUserId"
          :columns="viewMode === 'grid' ? 3 : 1"
          :show-view-toggle="false"
          :show-join-buttons="showJoinButtons"
          :show-members-preview="showMembersPreview"
          :show-more-actions="showMoreActions"
          :show-create-button="false"
          :show-pagination="showPagination"
          :clickable="true"
          :current-page="currentPage"
          :total-pages="totalPages"
          :total-count="totalCount"
          :has-next-page="hasNextPage"
          :has-previous-page="hasPreviousPage"
          @team-click="handleTeamClick"
          @team-join="handleTeamJoin"
          @team-leave="handleTeamLeave"
          @team-cancel="handleTeamCancel"
          @team-more-actions="handleTeamMoreActions"
          @view-team="handleViewTeam"
          @create-team="handleCreateTeam"
          @previous-page="handlePreviousPage"
          @next-page="handleNextPage"
        />
      </div>
    </div>

    <!-- Stats Section -->
    <div
      v-if="showStats && stats"
      class="bg-gray-50 dark:bg-gray-900 rounded-lg p-6 mb-8"
    >
      <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4">
        {{ $t('teams.page.stats') }}
      </h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        <div class="text-center">
          <div class="text-3xl font-bold text-gray-900 dark:text-gray-100">
            {{ stats.totalTeams || 0 }}
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400">
            {{ $t('teams.page.totalTeams') }}
          </div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-gray-900 dark:text-gray-100">
            {{ stats.totalMembers || 0 }}
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400">
            {{ $t('teams.page.totalMembers') }}
          </div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-gray-900 dark:text-gray-100">
            {{ stats.activeTeams || 0 }}
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400">
            {{ $t('teams.page.activeTeams') }}
          </div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-gray-900 dark:text-gray-100">
            {{ stats.publicTeams || 0 }}
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400">
            {{ $t('teams.page.publicTeams') }}
          </div>
        </div>
      </div>
    </div>

    <!-- Sidebar Slot -->
    <div v-if="$slots.sidebar" class="lg:grid lg:grid-cols-4 lg:gap-8">
      <div class="lg:col-span-3">
        <slot />
      </div>
      <div class="lg:col-span-1 mt-8 lg:mt-0">
        <slot name="sidebar" />
      </div>
    </div>
    <div v-else>
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { Team, TeamMember, TeamSortOption, TeamFilterOption } from '~/types/team-types'
import TeamList from '~/components/organisms/teams/TeamList.vue'

interface Props {
  title?: string
  description?: string
  teams: Team[]
  teamMembers?: TeamMember[]
  teamMembersMap?: Record<string, TeamMember[]>
  loading?: boolean
  currentUserId?: string | null
  filters?: Array<{
    id: TeamFilterOption | string
    label: string
    count?: number
  }>
  sortOptions?: Array<{
    value: TeamSortOption | string
    label: string
  }>
  showCreateButton?: boolean
  showJoinButtons?: boolean
  showMembersPreview?: boolean
  showMoreActions?: boolean
  showPagination?: boolean
  showStats?: boolean
  emptyTitle?: string
  emptyMessage?: string
  // Pagination props
  currentPage?: number
  totalPages?: number
  totalCount?: number
  hasNextPage?: boolean
  hasPreviousPage?: boolean
  // Stats
  stats?: {
    totalTeams: number
    totalMembers: number
    activeTeams: number
    publicTeams: number
  }
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  description: '',
  teams: () => [],
  teamMembers: () => [],
  teamMembersMap: () => ({}),
  loading: false,
  currentUserId: null,
  filters: () => [
    { id: 'all', label: 'All Teams' },
    { id: 'public', label: 'Public' },
    { id: 'private', label: 'Private' },
    { id: 'active', label: 'Active' }
  ],
  sortOptions: () => [
    { value: 'name_asc', label: 'Name (A-Z)' },
    { value: 'name_desc', label: 'Name (Z-A)' },
    { value: 'created_at_desc', label: 'Newest' },
    { value: 'member_count_desc', label: 'Most Members' }
  ],
  showCreateButton: true,
  showJoinButtons: true,
  showMembersPreview: true,
  showMoreActions: true,
  showPagination: true,
  showStats: true,
  emptyTitle: '',
  emptyMessage: '',
  currentPage: 1,
  totalPages: 1,
  totalCount: 0,
  hasNextPage: false,
  hasPreviousPage: false,
  stats: undefined
})

interface Emits {
  (e: 'search', query: string): void
  (e: 'filter-change', filter: TeamFilterOption | string): void
  (e: 'sort-change', sort: TeamSortOption | string): void
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
const searchQuery = ref('')
const activeFilter = ref(props.filters[0]?.id || 'all')
const sortOption = ref(props.sortOptions[0]?.value || 'name_asc')
const viewMode = ref<'grid' | 'list'>('grid')

// Computed properties
const defaultFilters = computed(() => [
  { id: 'all', label: t('teams.filters.all') },
  { id: 'public', label: t('teams.filters.public') },
  { id: 'private', label: t('teams.filters.private') },
  { id: 'active', label: t('teams.filters.active') }
])

const defaultSortOptions = computed(() => [
  { value: 'name_asc', label: t('teams.sort.nameAsc') },
  { value: 'name_desc', label: t('teams.sort.nameDesc') },
  { value: 'created_at_desc', label: t('teams.sort.newest') },
  { value: 'member_count_desc', label: t('teams.sort.mostMembers') }
])

// Methods
const handleSearch = () => {
  emit('search', searchQuery.value)
}

const handleFilterChange = (filter: TeamFilterOption | string) => {
  activeFilter.value = filter
  emit('filter-change', filter)
}

const handleSortChange = () => {
  emit('sort-change', sortOption.value)
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

const handleCreateTeam = () => {
  emit('create-team')
}

const handlePreviousPage = () => {
  emit('previous-page')
}

const handleNextPage = () => {
  emit('next-page')
}
</script>

<style scoped>
.teams-page-template {
  max-width: 1200px;
  margin: 0 auto;
}
</style>