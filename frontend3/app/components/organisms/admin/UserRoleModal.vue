<template>
  <Modal :model-value="modelValue" @update:model-value="onModelUpdate" title="Manage User Roles" size="lg">
    <div v-if="user" class="space-y-5">
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ user.name || user.username }}</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400">@{{ user.username }}<span v-if="user.email"> · {{ user.email }}</span></p>
      </div>

      <div class="grid gap-3">
        <label v-for="role in roles" :key="role.id" class="flex items-start gap-3 rounded-xl border border-gray-200 p-3 dark:border-gray-700">
          <input v-model="selectedRoleIds" :value="role.id" type="checkbox" class="mt-1 rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
          <div>
            <div class="font-medium text-gray-900 dark:text-white">{{ role.name }}</div>
            <div v-if="role.description" class="text-sm text-gray-500 dark:text-gray-400">{{ role.description }}</div>
          </div>
        </label>
      </div>

      <div class="flex justify-end gap-3">
        <button class="btn btn-outline" @click="$emit('update:modelValue', false)">Cancel</button>
        <button class="btn btn-primary" :disabled="saving" @click="$emit('save', selectedRoleIds)">
          {{ saving ? 'Saving...' : 'Save Roles' }}
        </button>
      </div>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Modal from '~/components/molecules/Modal.vue'
import type { AdminRole, AdminUserSummary } from '~/composables/useAdminUserRoles'

const props = defineProps<{
  modelValue: boolean
  user: AdminUserSummary | null
  roles: AdminRole[]
  saving?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'save', roleIds: number[]): void
}>()

const selectedRoleIds = ref<number[]>([])

watch(() => props.user, (user) => {
  selectedRoleIds.value = user?.roleIds ? [...user.roleIds] : []
}, { immediate: true })

function onModelUpdate(value: boolean) {
  emit('update:modelValue', value)
}
</script>
