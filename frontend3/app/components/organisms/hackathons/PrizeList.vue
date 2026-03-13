<template>
  <div v-if="prizes && prizes.length > 0" class="mb-8">
    <!-- Header with Icon -->
    <div class="flex items-center gap-3 mb-6">
      <Icon name="award" class="w-6 h-6 text-primary-600 dark:text-primary-400" />
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ title }}</h2>
      <Badge variant="primary" size="sm">
        {{ prizes.length }}
      </Badge>
    </div>

    <!-- Prize Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card
        v-for="(prize, idx) in prizes"
        :key="idx"
        class="p-4 sm:p-5 lg:p-6 bg-gradient-to-br from-primary-50 to-purple-50 dark:from-gray-700 dark:to-gray-800 border-primary-100 dark:border-gray-700"
      >
        <!-- Prize Header -->
        <div class="flex items-center mb-4">
          <!-- Position Badge -->
          <div class="relative mr-4">
            <div class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center">
              <span class="text-primary-600 dark:text-primary-300 font-bold">{{ idx + 1 }}</span>
            </div>
            <Badge
              v-if="idx === 0"
              variant="success"
              size="sm"
              class="absolute -top-1 -right-1"
            >
              <Icon name="crown" class="w-3 h-3" />
            </Badge>
          </div>

          <!-- Prize Name -->
          <div class="flex-1">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white">{{ prize.name }}</h3>
            <!-- Optional category/sponsor badges could be added if Prize interface is extended -->
            <div class="flex items-center gap-2 mt-1">
              <Badge
                v-if="idx === 0"
                variant="success"
                size="sm"
              >
                Grand Prize
              </Badge>
              <Badge
                v-else-if="idx === 1"
                variant="warning"
                size="sm"
              >
                Runner-up
              </Badge>
              <Badge
                v-else
                variant="gray"
                size="sm"
              >
                Prize
              </Badge>
            </div>
          </div>
        </div>

        <!-- Prize Description -->
        <p class="text-gray-700 dark:text-gray-300 mb-4">{{ prize.description }}</p>

        <!-- Prize Value -->
        <div class="flex items-center gap-2">
          <Icon name="dollar-sign" class="w-4 h-4 text-primary-600 dark:text-primary-400" />
          <span class="text-primary-600 dark:text-primary-400 font-bold text-lg">{{ prize.value }}</span>
        </div>
      </Card>
    </div>
  </div>
  <!-- Empty State -->
  <div v-else-if="prizes && prizes.length === 0" class="mb-8 text-center py-8">
    <Icon name="award" class="w-12 h-12 text-gray-400 dark:text-gray-600 mx-auto mb-4" />
    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
      No prizes yet
    </h3>
    <p class="text-gray-600 dark:text-gray-400">
      Check back later for prize announcements
    </p>
  </div>
</template>

<script setup lang="ts">
import type { PrizeListProps } from '~/types/hackathon-types'
import Card from '~/components/atoms/Card.vue'
import Icon from '~/components/atoms/Icon.vue'
import Badge from '~/components/atoms/Badge.vue'

defineProps<PrizeListProps>()
</script>
