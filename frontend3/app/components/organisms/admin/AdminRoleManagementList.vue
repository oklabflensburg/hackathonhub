<template>
  <section class="space-y-4">
    <header class="space-y-2">
      <p class="text-sm font-medium uppercase tracking-[0.2em] text-gray-500 dark:text-gray-400">Admin</p>
      <h1 class="text-3xl font-semibold text-gray-900 dark:text-white">User Role Management</h1>
      <p class="text-sm text-gray-600 dark:text-gray-300">Assign backend roles to platform users.</p>
    </header>

    <div class="grid gap-4">
      <AdminUserRoleRow v-for="user in users" :key="user.id" :user="user" @manage="$emit('manage', $event)" />
    </div>
  </section>
</template>

<script setup lang="ts">
import AdminUserRoleRow from '~/components/molecules/admin/AdminUserRoleRow.vue'
import type { AdminUserSummary } from '~/composables/useAdminUserRoles'

defineProps<{ users: AdminUserSummary[] }>()
defineEmits<{ (e: 'manage', user: AdminUserSummary): void }>()
</script>
