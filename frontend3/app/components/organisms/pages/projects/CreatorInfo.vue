<template>
  <Card>
    <template #header>
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ title }}</h2>
    </template>
    <div class="flex items-center space-x-3">
      <Avatar :src="avatarUrl" :fallback-text="creatorName" size="md" :alt="creatorName" />
      <div>
        <NuxtLink v-if="creatorId" :to="`/users/${creatorId}`" class="font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
          {{ creatorName }}
        </NuxtLink>
        <p v-else class="font-medium text-gray-900 dark:text-white">{{ creatorName }}</p>
        <p class="text-sm text-gray-500 dark:text-gray-400">{{ subtitle }}</p>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Avatar from '~/components/atoms/Avatar.vue'
import Card from '~/components/atoms/Card.vue'

const props = defineProps<{ project: any; title: string; subtitle: string }>()

const creatorName = computed(() => props.project.owner?.username || props.project.team?.creator?.username || 'Unknown')
const creatorId = computed(() => props.project.owner?.id || props.project.team?.creator?.id)
const avatarUrl = computed(() => props.project.owner?.avatar_url || props.project.team?.creator?.avatar_url)
</script>
