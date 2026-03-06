<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Use TeamsPageTemplate for consistent layout -->
    <TeamsPageTemplate
      :teams="teams"
      :loading="loading"
      :error="error"
      :current-user-id="currentUserId"
      :total-count="teams.length"
      :page="currentPage"
      :page-size="pageSize"
      :search-query="searchQuery"
      :selected-filters="selectedFilters"
      @search="handleSearch"
      @filter-change="handleFilterChange"
      @sort-change="handleSortChange"
      @page-change="handlePageChange"
      @create-team="handleCreateTeam"
      @team-click="handleTeamClick"
      @team-join="handleTeamJoin"
      @team-leave="handleTeamLeave"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from '#app'
import { useAuthStore } from '~/stores/auth'
import { useTeamStore } from '~/stores/team'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'
import { TeamVisibility, TeamStatus, type Team, type TeamFilterState, type TeamSortOption } from '~/types/team-types'
import TeamsPageTemplate from '~/components/templates/teams/TeamsPageTemplate.vue'

const router = useRouter()
const authStore = useAuthStore()
const teamStore = useTeamStore()
const uiStore = useUIStore()
const { t } = useI18n()

// State
const teams = ref<Team[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')
const selectedFilters = ref<Partial<TeamFilterState>>({})
const currentPage = ref(1)
const pageSize = ref(12)

// Computed
const currentUserId = computed(() => authStore.user?.id?.toString() || null)
const isAuthenticated = computed(() => authStore.isAuthenticated)

// Methods
const handleSearch = (query: string) => {
  searchQuery.value = query
  loadTeams()
}

const handleFilterChange = (filter: string) => {
  // Map filter string to TeamFilterState
  if (filter === 'public') {
    selectedFilters.value = { visibility: TeamVisibility.PUBLIC }
  } else if (filter === 'private') {
    selectedFilters.value = { visibility: TeamVisibility.PRIVATE }
  } else if (filter === 'active') {
    selectedFilters.value = { status: TeamStatus.ACTIVE }
  } else {
    selectedFilters.value = {}
  }
  loadTeams()
}

const handleSortChange = (sort: string) => {
  // Map sort string to sorting logic
  console.log('Sort changed:', sort)
  loadTeams()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadTeams()
}

const handleCreateTeam = () => {
  if (!isAuthenticated.value) {
    uiStore.showError(t('teams.loginRequiredToCreate'), t('common.authenticationRequired'))
    router.push('/login')
    return
  }
  router.push('/teams/create')
}

const handleTeamClick = (team: Team) => {
  router.push(`/teams/${team.id}`)
}

const handleTeamJoin = async (team: Team) => {
  if (!isAuthenticated.value) {
    uiStore.showError(t('teams.loginRequiredToJoin'), t('common.authenticationRequired'))
    router.push('/login')
    return
  }

  try {
    loading.value = true
    // Call API to join team
    await teamStore.joinTeam(Number(team.id))
    uiStore.showSuccess(t('teams.joinedTeamSuccess'))
    await loadTeams()
  } catch (err: any) {
    uiStore.showError(err.message || t('teams.joinTeamError'))
  } finally {
    loading.value = false
  }
}

const handleTeamLeave = async (team: Team) => {
  if (!isAuthenticated.value) return

  try {
    const confirmed = confirm(t('teams.confirmLeaveTeam'))
    if (!confirmed) return

    loading.value = true
    // Call API to leave team
    await teamStore.leaveTeam(Number(team.id))
    uiStore.showSuccess(t('teams.leftTeamSuccess'))
    await loadTeams()
  } catch (err: any) {
    uiStore.showError(err.message || t('teams.leaveTeamError'))
  } finally {
    loading.value = false
  }
}

const loadTeams = async () => {
  try {
    loading.value = true
    error.value = null

    // Build query parameters
    const params: any = {
      page: currentPage.value,
      pageSize: pageSize.value
    }

    if (searchQuery.value) {
      params.query = searchQuery.value
    }

    if (selectedFilters.value.visibility && selectedFilters.value.visibility !== 'all') {
      params.visibility = selectedFilters.value.visibility
    }

    if (selectedFilters.value.status && selectedFilters.value.status !== 'all') {
      params.status = selectedFilters.value.status
    }

    // Fetch teams from API
    const response = await teamStore.fetchTeams(params)
    const rawTeams = response.teams || response
    // Transform store Team objects to match Team interface from team-types.ts
    const transformedTeams = rawTeams.map((team: any) => ({
      ...team,
      visibility: team.is_open ? TeamVisibility.PUBLIC : TeamVisibility.PRIVATE,
      status: team.status || TeamStatus.ACTIVE,
      id: team.id.toString(), // Convert id to string to match Team interface
      createdBy: team.created_by?.toString() || team.created_by,
      hackathonId: team.hackathon_id?.toString() || team.hackathon_id,
      maxMembers: team.max_members,
      avatarUrl: team.avatar_url,
      bannerUrl: team.banner_url,
      createdAt: team.created_at,
      updatedAt: team.updated_at,
      tags: team.tags || [],
      stats: team.stats
    }))
    teams.value = transformedTeams
  } catch (err: any) {
    error.value = err.message || t('teams.loadTeamsError')
    console.error('Failed to load teams:', err)
  } finally {
    loading.value = false
  }
}

const loadHackathons = async () => {
  try {
    // Load hackathons for filters if needed
    // This would be implemented based on your API
  } catch (err) {
    console.error('Failed to load hackathons:', err)
  }
}

// Lifecycle
onMounted(() => {
  loadTeams()
  loadHackathons()
})
</script>

<style scoped>
.container {
  max-width: 1280px;
}
</style>