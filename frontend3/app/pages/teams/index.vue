<template>
  <div class="container mx-auto px-4 py-8">
    <TeamsPageTemplate
      :teams="paginatedTeams"
      :loading="loading"
      :error="error"
      :current-user-id="currentUserId"
      :team-members-map="teamMembersMap"
      :total-count="filteredTeams.length"
      :current-page="currentPage"
      :total-pages="totalPages"
      :has-next-page="hasNextPage"
      :has-previous-page="hasPreviousPage"
      :search-query="searchQuery"
      :selected-filters="selectedFilters"
      :stats="stats"
      @search="handleSearch"
      @filter-change="handleFilterChange"
      @sort-change="handleSortChange"
      @previous-page="handlePreviousPage"
      @next-page="handleNextPage"
      @create-team="handleCreateTeam"
      @team-click="handleTeamClick"
      @team-join="handleTeamJoin"
      @team-leave="handleTeamLeave"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from '#app'
import { useAuthStore } from '~/stores/auth'
import { useTeamStore } from '~/stores/team'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'
import {
  TeamSortOption,
  TeamStatus,
  TeamVisibility,
  type Team,
  type TeamFilterState,
  type TeamMember
} from '~/types/team-types'
import TeamsPageTemplate from '~/components/templates/TeamsPageTemplate.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const teamStore = useTeamStore()
const uiStore = useUIStore()
const { t } = useI18n()

const loading = ref(false)
const error = ref<string | null>(null)
const allTeams = ref<Team[]>([])
const searchQuery = ref('')
const selectedFilters = ref<Partial<TeamFilterState>>({})
const currentPage = ref(1)
const pageSize = ref(12)
const sortOption = ref<TeamSortOption>(TeamSortOption.CREATED_AT_DESC)

const currentUserId = computed(() => authStore.user?.id?.toString() || null)
const isAuthenticated = computed(() => authStore.isAuthenticated)

function mapTeam(raw: any): Team {
  return {
    id: String(raw.id),
    name: raw.name,
    description: raw.description || null,
    slug: raw.slug || raw.name?.toLowerCase().replace(/\s+/g, '-') || '',
    avatarUrl: raw.avatar_url || null,
    bannerUrl: raw.banner_url || null,
    visibility: raw.is_open ? TeamVisibility.PUBLIC : TeamVisibility.PRIVATE,
    status: TeamStatus.ACTIVE,
    maxMembers: raw.max_members ?? null,
    createdAt: raw.created_at,
    updatedAt: raw.updated_at || raw.created_at,
    createdBy: String(raw.created_by),
    hackathonId: raw.hackathon_id ? String(raw.hackathon_id) : null,
    tags: raw.tags || [],
    stats: {
      memberCount: raw.member_count ?? raw._member_count ?? 0,
      projectCount: raw.project_count ?? 0,
      activeProjectCount: raw.active_project_count ?? 0,
      completedProjectCount: raw.completed_project_count ?? 0,
      totalVotes: raw.total_votes ?? 0,
      totalComments: raw.total_comments ?? 0,
      averageRating: raw.average_rating ?? null,
      lastActivityAt: raw.last_activity_at ?? null,
      viewCount: raw.view_count ?? 0,
      engagementScore: raw.engagement_score ?? 0,
      engagementLevel: raw.engagement_level ?? 'low'
    }
  }
}

function mapMember(raw: any): TeamMember {
  return {
    id: String(raw.id),
    userId: String(raw.user_id),
    teamId: String(raw.team_id),
    role: raw.role,
    joinedAt: raw.joined_at,
    user: raw.user ? {
      id: String(raw.user.id),
      username: raw.user.username || '',
      displayName: raw.user.name || raw.user.display_name || null,
      avatarUrl: raw.user.avatar_url || null,
      email: raw.user.email || null,
      bio: raw.user.bio || null,
      skills: raw.user.skills || []
    } : undefined
  }
}

const teamMembersMap = computed<Record<string, TeamMember[]>>(() => {
  return Object.fromEntries(
    Array.from(teamStore.teamMembers.entries()).map(([teamId, members]) => [
      String(teamId),
      members.map(mapMember)
    ])
  )
})

const filteredTeams = computed(() => {
  let teams = [...allTeams.value]

  if (searchQuery.value.trim()) {
    const search = searchQuery.value.trim().toLowerCase()
    teams = teams.filter(team =>
      team.name.toLowerCase().includes(search) ||
      (team.description || '').toLowerCase().includes(search)
    )
  }

  if (selectedFilters.value.visibility && selectedFilters.value.visibility !== 'all') {
    teams = teams.filter(team => team.visibility === selectedFilters.value.visibility)
  }

  if (selectedFilters.value.status && selectedFilters.value.status !== 'all') {
    teams = teams.filter(team => team.status === selectedFilters.value.status)
  }

  teams.sort((a, b) => {
    switch (sortOption.value) {
      case TeamSortOption.NAME_ASC:
        return a.name.localeCompare(b.name)
      case TeamSortOption.NAME_DESC:
        return b.name.localeCompare(a.name)
      case TeamSortOption.CREATED_AT_ASC:
        return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      case TeamSortOption.MEMBER_COUNT_ASC:
        return (a.stats?.memberCount || 0) - (b.stats?.memberCount || 0)
      case TeamSortOption.MEMBER_COUNT_DESC:
        return (b.stats?.memberCount || 0) - (a.stats?.memberCount || 0)
      case TeamSortOption.CREATED_AT_DESC:
      default:
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    }
  })

  return teams
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredTeams.value.length / pageSize.value)))
const hasNextPage = computed(() => currentPage.value < totalPages.value)
const hasPreviousPage = computed(() => currentPage.value > 1)

const paginatedTeams = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredTeams.value.slice(start, start + pageSize.value)
})

const stats = computed(() => ({
  totalTeams: filteredTeams.value.length,
  totalMembers: filteredTeams.value.reduce((sum, team) => sum + (team.stats?.memberCount || 0), 0),
  activeTeams: filteredTeams.value.length,
  publicTeams: filteredTeams.value.filter(team => team.visibility === TeamVisibility.PUBLIC).length
}))

const refreshTeams = async () => {
  try {
    loading.value = true
    error.value = null

    await teamStore.fetchTeams({
      hackathon_id: route.query.hackathon_id ? Number(route.query.hackathon_id) : undefined,
      limit: 100
    })

    allTeams.value = teamStore.teams.map(mapTeam)
    currentPage.value = Math.min(currentPage.value, totalPages.value)
  } catch (err: any) {
    error.value = err?.message || t('teams.loadTeamsError')
  } finally {
    loading.value = false
  }
}

const handleSearch = (query: string) => {
  searchQuery.value = query
  currentPage.value = 1
}

const handleFilterChange = (filter: string) => {
  if (filter === 'public') {
    selectedFilters.value = { visibility: TeamVisibility.PUBLIC }
  } else if (filter === 'private') {
    selectedFilters.value = { visibility: TeamVisibility.PRIVATE }
  } else if (filter === 'active') {
    selectedFilters.value = { status: TeamStatus.ACTIVE }
  } else {
    selectedFilters.value = {}
  }
  currentPage.value = 1
}

const handleSortChange = (sort: string) => {
  sortOption.value = sort as TeamSortOption
  currentPage.value = 1
}

const handlePreviousPage = () => {
  if (hasPreviousPage.value) currentPage.value -= 1
}

const handleNextPage = () => {
  if (hasNextPage.value) currentPage.value += 1
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
    await teamStore.joinTeam(Number(team.id))
    uiStore.showSuccess(t('teams.joinedTeamSuccess'))
    await refreshTeams()
  } catch (err: any) {
    uiStore.showError(err?.message || t('teams.joinTeamError'))
  } finally {
    loading.value = false
  }
}

const handleTeamLeave = async (team: Team) => {
  if (!isAuthenticated.value) return

  try {
    if (!confirm(t('teams.confirmLeaveTeam'))) return
    loading.value = true
    await teamStore.leaveTeam(Number(team.id))
    uiStore.showSuccess(t('teams.leftTeamSuccess'))
    await refreshTeams()
  } catch (err: any) {
    uiStore.showError(err?.message || t('teams.leaveTeamError'))
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  refreshTeams()
})
</script>

<style scoped>
.container {
  max-width: 1280px;
}
</style>
