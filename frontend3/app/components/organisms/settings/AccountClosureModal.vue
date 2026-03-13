<template>
  <Modal
    :model-value="modelValue"
    :title="mode === 'delete' ? 'Konto dauerhaft löschen' : 'Konto deaktivieren'"
    :description="mode === 'delete'
      ? 'Diese Aktion ist endgültig. Bei bestehendem Besitz an Hackathons, Teams oder Projekten wird die Löschung blockiert.'
      : 'Dein Konto wird deaktiviert, du wirst abgemeldet und kannst dich erst nach einer Reaktivierung wieder anmelden.'"
    size="lg"
    @update:model-value="onModelUpdate"
  >
    <div class="space-y-5">
      <div v-if="impact" class="rounded-xl border border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-900/40">
        <p class="text-sm text-gray-700 dark:text-gray-300">
          {{ impact.message }}
        </p>
        <div class="mt-3 grid gap-3 md:grid-cols-3">
          <div>
            <p class="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">Hackathons</p>
            <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ impact.hackathons.length }}</p>
          </div>
          <div>
            <p class="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">Teams</p>
            <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ impact.teams.length }}</p>
          </div>
          <div>
            <p class="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">Projekte</p>
            <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ impact.projects.length }}</p>
          </div>
        </div>
        <div v-if="mode === 'delete' && !impact.can_delete" class="mt-4 space-y-3">
          <p class="text-sm font-medium text-red-600 dark:text-red-400">
            Permanente Löschung ist derzeit blockiert.
          </p>
          <div v-if="impact.hackathons.length" class="text-sm text-gray-700 dark:text-gray-300">
            <p class="font-medium">Owned Hackathons</p>
            <ul class="mt-1 list-disc pl-5">
              <li v-for="item in impact.hackathons" :key="`hackathon-${item.id}`">{{ item.name }}</li>
            </ul>
          </div>
          <div v-if="impact.teams.length" class="text-sm text-gray-700 dark:text-gray-300">
            <p class="font-medium">Owned Teams</p>
            <ul class="mt-1 list-disc pl-5">
              <li v-for="item in impact.teams" :key="`team-${item.id}`">{{ item.name }}</li>
            </ul>
          </div>
          <div v-if="impact.projects.length" class="text-sm text-gray-700 dark:text-gray-300">
            <p class="font-medium">Owned Projects</p>
            <ul class="mt-1 list-disc pl-5">
              <li v-for="item in impact.projects" :key="`project-${item.id}`">{{ item.name }}</li>
            </ul>
          </div>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Deaktiviere das Konto jetzt oder übertrage diese Inhalte später an einen anderen Nutzer.
          </p>
        </div>
      </div>

      <label v-if="requiresPassword" class="block space-y-2 text-sm">
        <span class="font-medium text-gray-700 dark:text-gray-200">Passwort</span>
        <input
          v-model="passwordValue"
          type="password"
          class="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 dark:border-gray-600 dark:bg-gray-900 dark:text-white"
          placeholder="Passwort eingeben"
          autocomplete="current-password"
        >
      </label>

      <label class="block space-y-2 text-sm">
        <span class="font-medium text-gray-700 dark:text-gray-200">
          Bestätigungscode: <code class="rounded bg-gray-100 px-1 py-0.5 dark:bg-gray-800">{{ expectedConfirmation }}</code>
        </span>
        <input
          v-model="confirmationValue"
          type="text"
          class="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 dark:border-gray-600 dark:bg-gray-900 dark:text-white"
          :placeholder="expectedConfirmation"
          autocomplete="off"
        >
      </label>

      <p v-if="error" class="text-sm text-red-600 dark:text-red-400">
        {{ error }}
      </p>

      <div class="flex justify-end gap-3">
        <Button variant="outline" @click="$emit('close')">
          Abbrechen
        </Button>
        <Button
          :variant="mode === 'delete' ? 'danger' : 'outline'"
          :loading="loading"
          :disabled="mode === 'delete' && impact && !impact.can_delete"
          @click="submit"
        >
          {{ mode === 'delete' ? 'Konto löschen' : 'Konto deaktivieren' }}
        </Button>
      </div>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { AccountImpactResponse } from '~/types/settings-types'
import Modal from '~/components/molecules/Modal.vue'
import Button from '~/components/atoms/Button.vue'

const props = defineProps<{
  modelValue: boolean
  mode: 'delete' | 'deactivate'
  authMethod?: string
  impact?: AccountImpactResponse | null
  loading?: boolean
  error?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  close: []
  submit: [payload: { password?: string; confirmation: string }]
}>()

const passwordValue = ref('')
const confirmationValue = ref('')

const requiresPassword = computed(() => props.authMethod === 'email')
const expectedConfirmation = computed(() => (
  props.mode === 'delete' ? 'DELETE MY ACCOUNT' : 'DEACTIVATE ACCOUNT'
))

watch(() => props.modelValue, (visible) => {
  if (visible) {
    passwordValue.value = ''
    confirmationValue.value = ''
  }
})

const onModelUpdate = (value: boolean) => {
  emit('update:modelValue', value)
  if (!value) emit('close')
}

const submit = () => {
  emit('submit', {
    password: passwordValue.value || undefined,
    confirmation: confirmationValue.value.trim()
  })
}
</script>
