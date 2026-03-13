import { computed, ref } from 'vue'
import { useAuthStore } from '~/stores/auth'

export interface HackathonTeamReportSummary {
  id: number
  team_id: number
  reason: string
  status: 'pending' | 'reviewed' | 'resolved' | 'dismissed'
  reporter_id: number
  reviewed_by?: number | null
  reviewed_at?: string | null
  resolution_note?: string | null
  created_at: string
  team?: {
    id: number
    name: string
    hackathon_id?: number
  } | null
  reporter?: {
    id: number
    username: string
    name?: string | null
    avatar_url?: string | null
  } | null
  reviewer?: {
    id: number
    username: string
    name?: string | null
    avatar_url?: string | null
  } | null
}

export interface TeamReportFilters {
  status?: string
  teamId?: number | null
}

export function useHackathonTeamReports() {
  const authStore = useAuthStore()
  const reports = ref<HackathonTeamReportSummary[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const forbidden = ref(false)

  const teams = computed(() => {
    const seen = new Map<number, { id: number; name: string }>()
    reports.value.forEach((report) => {
      if (report.team?.id && report.team?.name) {
        seen.set(report.team.id, { id: report.team.id, name: report.team.name })
      }
    })
    return Array.from(seen.values())
  })

  async function fetchReports(hackathonId: string | number, filters: TeamReportFilters = {}) {
    loading.value = true
    error.value = null
    forbidden.value = false

    try {
      const params = new URLSearchParams()
      if (filters.status) params.set('status', filters.status)
      if (filters.teamId) params.set('team_id', String(filters.teamId))

      const query = params.toString()
      const response = await authStore.fetchWithAuth(`/api/hackathons/${hackathonId}/team-reports${query ? `?${query}` : ''}`)

      if (response.status === 403) {
        forbidden.value = true
        reports.value = []
        return []
      }
      if (!response.ok) {
        throw new Error('Failed to load team reports')
      }

      const data = await response.json()
      reports.value = Array.isArray(data) ? data : []
      return reports.value
    } catch (err: any) {
      error.value = err?.message || 'Failed to load team reports'
      reports.value = []
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateReport(reportId: number, payload: { status: string; resolution_note?: string | null }) {
    const response = await authStore.fetchWithAuth(`/api/team-reports/${reportId}`, {
      method: 'PATCH',
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      const data = await response.json().catch(() => ({}))
      throw new Error(data.detail || 'Failed to update team report')
    }

    const updated = await response.json()
    reports.value = reports.value.map(report => report.id === updated.id ? updated : report)
    return updated as HackathonTeamReportSummary
  }

  return {
    reports,
    teams,
    loading,
    error,
    forbidden,
    fetchReports,
    updateReport,
  }
}
