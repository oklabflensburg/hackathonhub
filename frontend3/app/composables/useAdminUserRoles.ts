import { computed, ref } from 'vue'
import { useAuthStore } from '~/stores/auth'

export interface AdminRole {
  id: number
  name: string
  description?: string | null
}

export interface AdminUserSummary {
  id: number
  username: string
  name?: string | null
  avatar_url?: string | null
  email?: string | null
  roles: string[]
  roleIds: number[]
}

export function useAdminUserRoles() {
  const authStore = useAuthStore()
  const users = ref<AdminUserSummary[]>([])
  const roles = ref<AdminRole[]>([])
  const loading = ref(false)
  const saving = ref(false)
  const error = ref<string | null>(null)

  const roleOptions = computed(() => roles.value.map(role => ({ label: role.name, value: role.id })))

  async function fetchRoles() {
    const response = await authStore.fetchWithAuth('/api/admin/roles')
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}))
      throw new Error(payload.detail || 'Failed to load roles')
    }
    roles.value = await response.json()
    return roles.value
  }

  async function fetchUsers() {
    const response = await authStore.fetchWithAuth('/api/users?limit=100')
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}))
      throw new Error(payload.detail || 'Failed to load users')
    }
    const data = await response.json()
    users.value = Array.isArray(data) ? data.map((user: any) => ({
      id: user.id,
      username: user.username,
      name: user.name,
      avatar_url: user.avatar_url,
      email: user.email,
      roles: Array.isArray(user.roles) ? user.roles : [],
      roleIds: [],
    })) : []
    return users.value
  }

  async function fetchUserRoles(userId: number) {
    const response = await authStore.fetchWithAuth(`/api/admin/users/${userId}/roles`)
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}))
      throw new Error(payload.detail || 'Failed to load user roles')
    }
    const data = await response.json()
    const user = users.value.find(entry => entry.id === userId)
    if (user) {
      user.roleIds = data.map((role: AdminRole) => role.id)
      user.roles = data.map((role: AdminRole) => role.name)
    }
    return data as AdminRole[]
  }

  async function fetchInitialData() {
    loading.value = true
    error.value = null
    try {
      await fetchRoles()
      await fetchUsers()
      await Promise.all(users.value.map(user => fetchUserRoles(user.id)))
    } catch (err: any) {
      error.value = err?.message || 'Failed to load admin role management data'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateUserRoles(userId: number, roleIds: number[]) {
    saving.value = true
    try {
      const response = await authStore.fetchWithAuth(`/api/admin/users/${userId}/roles`, {
        method: 'PATCH',
        body: JSON.stringify({ role_ids: roleIds }),
      })
      if (!response.ok) {
        const payload = await response.json().catch(() => ({}))
        throw new Error(payload.detail || 'Failed to update user roles')
      }
      const data = await response.json()
      const user = users.value.find(entry => entry.id === userId)
      if (user) {
        user.roleIds = data.map((role: AdminRole) => role.id)
        user.roles = data.map((role: AdminRole) => role.name)
      }
      return data as AdminRole[]
    } finally {
      saving.value = false
    }
  }

  return {
    users,
    roles,
    roleOptions,
    loading,
    saving,
    error,
    fetchInitialData,
    updateUserRoles,
  }
}
