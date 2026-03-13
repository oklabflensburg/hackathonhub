import { ref } from 'vue'
import { useAuthStore } from '~/stores/auth'

export type ResourceReportStatus = 'pending' | 'reviewed' | 'resolved' | 'dismissed'
export type ResourceType = 'hackathon' | 'project'

export interface ResourceReportSummary {
  id: number
  reporter_id: number
  resource_type: 'team' | 'hackathon' | 'project'
  resource_id: number
  reason: string
  status: ResourceReportStatus
  reviewed_by?: number | null
  reviewed_at?: string | null
  resolution_note?: string | null
  created_at: string
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
  resource?: {
    id: number
    resource_type: 'team' | 'hackathon' | 'project'
    name: string
    hackathon_id?: number | null
  } | null
}

export function useReports() {
  const authStore = useAuthStore()
  const reports = ref<ResourceReportSummary[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const forbidden = ref(false)

  async function createReport(resourceType: ResourceType, resourceId: string | number, reason: string) {
    const response = await authStore.fetchWithAuth(`/api/${resourceType}s/${resourceId}/reports`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason }),
    })
    const data = await response.json().catch(() => ({}))
    if (!response.ok) {
      throw new Error(data.detail || `Failed to report ${resourceType}`)
    }
    return data as ResourceReportSummary
  }

  async function fetchReports(resourceType: ResourceType, resourceId: string | number, filters: { status?: string } = {}) {
    loading.value = true
    error.value = null
    forbidden.value = false
    try {
      const params = new URLSearchParams()
      if (filters.status) params.set('status', filters.status)
      const query = params.toString()
      const response = await authStore.fetchWithAuth(`/api/${resourceType}s/${resourceId}/reports${query ? `?${query}` : ''}`)
      if (response.status === 403) {
        forbidden.value = true
        reports.value = []
        return []
      }
      const data = await response.json().catch(() => ([]))
      if (!response.ok) {
        throw new Error(data.detail || `Failed to load ${resourceType} reports`)
      }
      reports.value = Array.isArray(data) ? data : []
      return reports.value
    } catch (err: any) {
      error.value = err?.message || 'Failed to load reports'
      reports.value = []
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateReport(reportId: number, payload: { status: ResourceReportStatus; resolution_note?: string | null }) {
    const response = await authStore.fetchWithAuth(`/api/reports/${reportId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    const data = await response.json().catch(() => ({}))
    if (!response.ok) {
      throw new Error(data.detail || 'Failed to update report')
    }
    reports.value = reports.value.map((report) => report.id === data.id ? data : report)
    return data as ResourceReportSummary
  }

  return {
    reports,
    loading,
    error,
    forbidden,
    createReport,
    fetchReports,
    updateReport,
  }
}
