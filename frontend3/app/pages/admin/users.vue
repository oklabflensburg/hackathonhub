<template>
  <div class="mx-auto max-w-6xl space-y-6 px-4 py-8 sm:px-6 lg:px-8">
    <div v-if="!authStore.isAuthenticated" class="rounded-2xl border border-amber-200 bg-amber-50 p-6 text-sm text-amber-800 dark:border-amber-500/30 dark:bg-amber-500/10 dark:text-amber-200">
      You need to sign in to access user role management.
    </div>

    <div v-else-if="!authStore.isSuperuser" class="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700 dark:border-red-500/30 dark:bg-red-500/10 dark:text-red-200">
      Only superusers can manage backend roles.
    </div>

    <div v-else-if="loading" class="py-16 text-center text-gray-500 dark:text-gray-400">Loading role management...</div>

    <div v-else-if="error" class="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700 dark:border-red-500/30 dark:bg-red-500/10 dark:text-red-200">
      {{ error }}
    </div>

    <AdminRoleManagementList v-else :users="users" @manage="openModal" />

    <UserRoleModal
      v-model="roleModalOpen"
      :user="selectedUser"
      :roles="roles"
      :saving="saving"
      @save="saveRoles"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { navigateTo } from '#imports'
import AdminRoleManagementList from '~/components/organisms/admin/AdminRoleManagementList.vue'
import UserRoleModal from '~/components/organisms/admin/UserRoleModal.vue'
import { useAdminUserRoles, type AdminUserSummary } from '~/composables/useAdminUserRoles'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

const authStore = useAuthStore()
const uiStore = useUIStore()
const { users, roles, loading, saving, error, fetchInitialData, updateUserRoles } = useAdminUserRoles()

const roleModalOpen = ref(false)
const selectedUser = ref<AdminUserSummary | null>(null)

if (!authStore.isAuthenticated) {
  navigateTo('/login')
} else if (authStore.isSuperuser) {
  await fetchInitialData().catch(() => undefined)
}

function openModal(user: AdminUserSummary) {
  selectedUser.value = user
  roleModalOpen.value = true
}

async function saveRoles(roleIds: number[]) {
  if (!selectedUser.value) return
  try {
    await updateUserRoles(selectedUser.value.id, roleIds)
    uiStore.showSuccess('User roles updated', 'Admin')
    roleModalOpen.value = false
  } catch (err: any) {
    uiStore.showError(err?.message || 'Failed to update user roles', 'Admin')
  }
}
</script>
