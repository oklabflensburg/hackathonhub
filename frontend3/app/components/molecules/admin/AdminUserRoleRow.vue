<template>
  <div class="grid gap-4 rounded-2xl border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-800 lg:grid-cols-[minmax(0,1.5fr)_minmax(0,1fr)_auto] lg:items-center">
    <div class="min-w-0">
      <div class="font-semibold text-gray-900 dark:text-white">{{ user.name || user.username }}</div>
      <div class="truncate text-sm text-gray-500 dark:text-gray-400">@{{ user.username }}<span v-if="user.email"> · {{ user.email }}</span></div>
    </div>

    <div class="flex flex-wrap gap-2">
      <AdminRoleBadge v-for="role in user.roles" :key="role" :label="role" />
      <span v-if="user.roles.length === 0" class="text-sm text-gray-400">No roles</span>
    </div>

    <button class="btn btn-outline justify-self-start lg:justify-self-end" @click="$emit('manage', user)">
      Manage Roles
    </button>
  </div>
</template>

<script setup lang="ts">
import AdminRoleBadge from '~/components/molecules/admin/AdminRoleBadge.vue'
import type { AdminUserSummary } from '~/composables/useAdminUserRoles'

defineProps<{ user: AdminUserSummary }>()
defineEmits<{ (e: 'manage', user: AdminUserSummary): void }>()
</script>
