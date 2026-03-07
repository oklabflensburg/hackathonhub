<template>
  <div class="hackathon-detail-template">
    <!-- Header section -->
    <header class="mb-8">
      <div class="flex flex-col md:flex-row md:items-start justify-between gap-4">
        <div class="flex-1">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            {{ hackathon?.name || 'Hackathon Details' }}
          </h1>
          
          <div class="flex flex-wrap items-center gap-2 mb-4">
            <Badge
              v-if="hackathon?.status"
              :variant="getStatusVariant(hackathon.status)"
              size="md"
            >
              {{ formatStatus(hackathon.status) }}
            </Badge>
            
            <Badge
              v-if="hackathon?.type"
              variant="gray"
              size="sm"
            >
              {{ hackathon.type }}
            </Badge>
          </div>
        </div>
        
        <div class="flex items-center space-x-3">
          <slot name="header-actions">
            <button
              v-if="showEditButton"
              class="px-4 py-2 text-sm font-medium rounded-md border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
              @click="$emit('edit')"
            >
              Edit
            </button>
            
            <button
              v-if="showRegisterButton"
              class="px-4 py-2 text-sm font-medium rounded-md bg-primary-600 text-white hover:bg-primary-700"
              @click="$emit('register')"
            >
              Register Now
            </button>
          </slot>
        </div>
      </div>
    </header>

    <!-- Main content grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left column: Main content -->
      <div class="lg:col-span-2 space-y-8">
        <!-- Description section -->
        <section class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Description
          </h2>
          
          <div class="prose dark:prose-invert max-w-none">
            <slot name="description">
              <p v-if="hackathon?.description" class="text-gray-700 dark:text-gray-300">
                {{ hackathon.description }}
              </p>
              <p v-else class="text-gray-500 dark:text-gray-400 italic">
                No description provided.
              </p>
            </slot>
          </div>
        </section>

        <!-- Rules section -->
        <section class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Rules & Guidelines
          </h2>
          
          <slot name="rules">
            <div v-if="hackathon?.rules" class="space-y-3">
              <div
                v-for="(rule, index) in hackathon.rules"
                :key="index"
                class="flex items-start"
              >
                <Icon
                  name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M5 13l4 4L19 7' /></svg>"
                  :size="20"
                  is-svg
                  class="text-green-500 mt-0.5 mr-3 flex-shrink-0"
                />
                <span class="text-gray-700 dark:text-gray-300">{{ rule }}</span>
              </div>
            </div>
            <p v-else class="text-gray-500 dark:text-gray-400 italic">
              No rules specified.
            </p>
          </slot>
        </section>

        <!-- Prizes section -->
        <section class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Prizes
          </h2>
          
          <slot name="prizes">
            <div v-if="hackathon?.prizes && hackathon.prizes.length > 0" class="space-y-4">
              <div
                v-for="(prize, index) in hackathon.prizes"
                :key="index"
                class="flex items-center p-4 bg-gradient-to-r from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/30 rounded-lg"
              >
                <div class="flex-shrink-0 w-12 h-12 flex items-center justify-center bg-white dark:bg-gray-700 rounded-full mr-4">
                  <span class="text-xl font-bold text-primary-600 dark:text-primary-400">
                    #{{ index + 1 }}
                  </span>
                </div>
                <div>
                  <h3 class="font-semibold text-gray-900 dark:text-white">
                    {{ prize.title }}
                  </h3>
                  <p class="text-gray-600 dark:text-gray-400">
                    {{ prize.description }}
                  </p>
                  <p v-if="prize.value" class="text-lg font-bold text-primary-600 dark:text-primary-400 mt-1">
                    {{ prize.value }}
                  </p>
                </div>
              </div>
            </div>
            <p v-else class="text-gray-500 dark:text-gray-400 italic">
              No prizes announced yet.
            </p>
          </slot>
        </section>

        <!-- Additional content slot -->
        <slot name="additional-content"></slot>
      </div>

      <!-- Right column: Sidebar -->
      <div class="space-y-6">
        <!-- Stats card -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Statistics
          </h3>
          
          <div class="space-y-4">
            <StatItem
              v-if="hackathon?.participantCount !== undefined"
              label="Participants"
              :value="hackathon.participantCount"
              icon="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0H21m-4.5 0H12m4.5 0h4.5m-4.5 0V9' /></svg>"
              trend="up"
            />
            
            <StatItem
              v-if="hackathon?.projectCount !== undefined"
              label="Projects"
              :value="hackathon.projectCount"
              icon="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' /></svg>"
            />
            
            <StatItem
              v-if="hackathon?.teamCount !== undefined"
              label="Teams"
              :value="hackathon.teamCount"
              icon="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' /></svg>"
            />
            
            <div v-if="!hasStats" class="text-center py-4">
              <p class="text-gray-500 dark:text-gray-400">
                No statistics available yet.
              </p>
            </div>
          </div>
        </div>

        <!-- Organizer info -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Organizer
          </h3>
          
          <slot name="organizer">
            <div v-if="hackathon?.organizer" class="flex items-center">
              <div class="w-12 h-12 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center mr-3">
                <Icon
                  name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' /></svg>"
                  :size="24"
                  is-svg
                  class="text-primary-600 dark:text-primary-400"
                />
              </div>
              <div>
                <h4 class="font-medium text-gray-900 dark:text-white">
                  {{ hackathon.organizer.name }}
                </h4>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  {{ hackathon.organizer.email }}
                </p>
              </div>
            </div>
            <p v-else class="text-gray-500 dark:text-gray-400 italic">
              Organizer information not available.
            </p>
          </slot>
        </div>

        <!-- Additional sidebar slot -->
        <slot name="sidebar-content"></slot>
      </div>
    </div>

    <!-- Footer actions -->
    <footer v-if="showFooterActions" class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
      <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">
          <slot name="footer-info">
            Last updated: {{ new Date().toLocaleDateString() }}
          </slot>
        </div>
        
        <div class="flex items-center space-x-3">
          <slot name="footer-actions">
            <button
              class="px-4 py-2 text-sm font-medium rounded-md border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
              @click="$emit('share')"
            >
              Share
            </button>
            
            <button
              class="px-4 py-2 text-sm font-medium rounded-md bg-primary-600 text-white hover:bg-primary-700"
              @click="$emit('participate')"
            >
              Participate Now
            </button>
          </slot>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Badge from '../atoms/Badge.vue'
import Icon from '../atoms/Icon.vue'
import StatItem from '../molecules/StatItem.vue'

export interface Hackathon {
  id?: string
  name?: string
  description?: string
  status?: 'draft' | 'upcoming' | 'active' | 'completed' | 'cancelled'
  type?: string
  rules?: string[]
  prizes?: Array<{
    title: string
    description: string
    value?: string
  }>
  participantCount?: number
  projectCount?: number
  teamCount?: number
  organizer?: {
    name: string
    email: string
  }
}

export interface HackathonDetailTemplateProps {
  /** Hackathon data */
  hackathon?: Hackathon
  /** Whether to show edit button */
  showEditButton?: boolean
  /** Whether to show register button */
  showRegisterButton?: boolean
  /** Whether to show footer actions */
  showFooterActions?: boolean
}

const props = withDefaults(defineProps<HackathonDetailTemplateProps>(), {
  hackathon: () => ({}),
  showEditButton: false,
  showRegisterButton: true,
  showFooterActions: true,
})

const emit = defineEmits<{
  /** Emitted when edit button is clicked */
  edit: []
  /** Emitted when register button is clicked */
  register: []
  /** Emitted when share button is clicked */
  share: []
  /** Emitted when participate button is clicked */
  participate: []
}>()

// Computed properties
const hasStats = computed(() => {
  return (
    props.hackathon?.participantCount !== undefined ||
    props.hackathon?.projectCount !== undefined ||
    props.hackathon?.teamCount !== undefined
  )
})

// Methods
const getStatusVariant = (status: string): 'secondary' | 'info' | 'success' | 'danger' | 'gray' => {
  const variants: Record<string, 'secondary' | 'info' | 'success' | 'danger' | 'gray'> = {
    draft: 'secondary',
    upcoming: 'info',
    active: 'success',
    completed: 'gray',
    cancelled: 'danger',
  }
  return variants[status] || 'gray'
}

const formatStatus = (status: string): string => {
  const statusMap: Record<string, string> = {
    draft: 'Draft',
    upcoming: 'Upcoming',
    active: 'Active',
    completed: 'Completed',
    cancelled: 'Cancelled',
  }
  return statusMap[status] || status
}
</script>

<style scoped>
.hackathon-detail-template {
  width: 100%;
}
</style>
