<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
    <div class="flex flex-col md:flex-row md:items-start justify-between">
      <div class="mb-4 md:mb-0">
        <div class="flex items-center mb-2">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">{{ invitation.team?.name || labels.unknownTeam }}</h3>
          <Tag class="ml-3" :text="statusLabel" :color="statusColor" size="sm" />
        </div>

        <div class="space-y-2">
          <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span>{{ labels.invited }} {{ formatDate(invitation.created_at) }}</span>
          </div>

          <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span>{{ labels.invitedBy }} {{ invitation.inviter?.username || labels.unknownUser }}</span>
          </div>

          <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            <span>{{ labels.hackathonLabel }} {{ invitation.team?.hackathon?.name || labels.unknown }}</span>
          </div>
        </div>

        <div v-if="invitation.message" class="mt-4 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            <span class="font-medium">{{ labels.messageLabel }}</span> {{ invitation.message }}
          </p>
        </div>
      </div>

      <div v-if="invitation.status === 'pending'" class="flex space-x-3">
        <button
          class="btn btn-outline text-red-600 dark:text-red-400 border-red-300 dark:border-red-700 hover:bg-red-50 dark:hover:bg-red-900/20"
          :disabled="isProcessing"
          @click="$emit('decline', invitation.id)"
        >
          <span v-if="isProcessing && actionType === 'decline'">
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            {{ labels.declining }}
          </span>
          <span v-else>{{ labels.decline }}</span>
        </button>
        <button class="btn btn-primary" :disabled="isProcessing" @click="$emit('accept', invitation.id)">
          <span v-if="isProcessing && actionType === 'accept'">
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            {{ labels.accepting }}
          </span>
          <span v-else>{{ labels.acceptInvitationButton }}</span>
        </button>
      </div>

      <div v-else class="text-sm text-gray-600 dark:text-gray-400">
        <p>
          {{ invitation.status === 'accepted' ? labels.youAcceptedThisInvitation : labels.youDeclinedThisInvitation }}
          {{ formatDate(invitation.updated_at) }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

defineEmits<{ (e: 'accept', id: number): void; (e: 'decline', id: number): void }>()

const props = defineProps<{
  invitation: any
  processingInvitation: number | null
  actionType: 'accept' | 'decline' | null
  labels: Record<string, string>
  formatDate: (v: string) => string
}>()

const isProcessing = computed(() => props.processingInvitation === props.invitation.id)

const statusColor = computed(() => {
  if (props.invitation.status === 'pending') return 'warning'
  if (props.invitation.status === 'accepted') return 'success'
  return 'neutral'
})

const statusLabel = computed(() => {
  if (props.invitation.status === 'pending') return props.labels.pending
  if (props.invitation.status === 'accepted') return props.labels.accepted
  return props.labels.declined
})
</script>
