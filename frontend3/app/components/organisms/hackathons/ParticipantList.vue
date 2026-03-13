<template>
  <section class="mt-8">
    <!-- Header with Icon -->
    <div class="flex items-center gap-3 mb-6">
      <Icon name="users" class="w-6 h-6 text-gray-700 dark:text-gray-300" />
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ title }}</h2>
      <Badge v-if="items.length > 0" variant="gray" size="sm">
        {{ items.length }}
      </Badge>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="py-8">
      <div class="flex flex-col items-center justify-center gap-4">
        <LoadingSpinner size="lg" />
        <p class="text-gray-600 dark:text-gray-400">{{ loadingLabel }}</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="py-6">
      <Alert
        :variant="requiresAuth ? 'warning' : 'error'"
        :title="error"
        :message="requiresAuth ? authHint : error"
      >
        <template #actions>
          <div class="flex flex-wrap gap-2 mt-3">
            <Button
              v-if="requiresAuth"
              variant="outline"
              size="sm"
              @click="$emit('loginGithub')"
            >
              <Icon name="github" class="w-4 h-4 mr-2" />
              {{ githubLabel }}
            </Button>
            <Button
              v-if="requiresAuth"
              variant="outline"
              size="sm"
              @click="$emit('loginGoogle')"
            >
              <Icon name="mail" class="w-4 h-4 mr-2" />
              {{ googleLabel }}
            </Button>
            <Button
              v-if="!requiresAuth"
              variant="outline"
              size="sm"
              @click="$emit('retry')"
            >
              {{ retryLabel }}
            </Button>
          </div>
        </template>
      </Alert>
    </div>

    <!-- Empty State -->
    <div v-else-if="items.length === 0" class="py-8 text-center">
      <div class="max-w-md mx-auto">
        <Icon name="users" class="w-12 h-12 text-gray-400 dark:text-gray-600 mx-auto mb-4" />
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          {{ emptyLabel }}
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">
          {{ emptyLabel }}
        </p>
        <Button
          v-if="emptyActionLabel && emptyActionPath"
          :to="emptyActionPath"
          variant="primary"
        >
          {{ emptyActionLabel }}
        </Button>
      </div>
    </div>

    <!-- Participant List -->
    <div v-else class="space-y-4">
      <Card
        v-for="team in items"
        :key="team.id"
        class="p-4 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
      >
        <div class="flex items-center justify-between">
          <!-- Team Info -->
          <div class="flex items-center gap-3">
            <Avatar
              v-if="team.avatar"
              :src="team.avatar"
              :alt="team.name"
              size="md"
            />
            <div>
              <h3 class="font-semibold text-gray-900 dark:text-white">
                {{ team.name }}
              </h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">
                {{ team.description || noDescriptionLabel }}
              </p>
              <div class="flex items-center gap-2 mt-1">
                <Badge
                  :variant="team.open ? 'success' : 'gray'"
                  size="sm"
                >
                  {{ team.open ? openLabel : closedLabel }}
                </Badge>
                <span class="text-xs text-gray-500 dark:text-gray-500">
                  {{ createdPrefix }} {{ formatDate(team.createdAt) }}
                </span>
              </div>
            </div>
          </div>

          <!-- Team Stats -->
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2">
              <Icon name="users" class="w-4 h-4 text-gray-500" />
              <span class="text-sm text-gray-700 dark:text-gray-300">
                {{ team.memberCount || 0 }} {{ membersLabel }}
              </span>
            </div>
            <Button
              variant="ghost"
              size="sm"
              :to="`/teams/${team.id}`"
            >
              <Icon name="arrow-right" class="w-4 h-4" />
            </Button>
          </div>
        </div>
      </Card>
    </div>

    <!-- View All Link -->
    <div v-if="items.length > 0" class="mt-6 text-center">
      <Button
        :to="viewAllPath"
        variant="outline"
        class="w-full sm:w-auto"
      >
        {{ viewAllLabel }}
        <Icon name="arrow-right" class="w-4 h-4 ml-2" />
      </Button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Icon, Avatar, Badge, Button, Card, Alert, LoadingSpinner } from '~/components/atoms'

defineProps<{
  title: string
  items: any[]
  loading: boolean
  error: string | null
  requiresAuth: boolean
  loadingLabel: string
  authHint: string
  githubLabel: string
  googleLabel: string
  emailLabel: string
  retryLabel: string
  emptyLabel: string
  emptyActionLabel?: string
  emptyActionPath?: string
  openLabel: string
  closedLabel: string
  noDescriptionLabel: string
  membersLabel: string
  createdPrefix: string
  viewAllLabel: string
  viewAllPath: string
  formatDate: (dateString: string) => string
}>()

defineEmits<{
  (e: 'retry'): void
  (e: 'loginGithub'): void
  (e: 'loginGoogle'): void
}>()
</script>
