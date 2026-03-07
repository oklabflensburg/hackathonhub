<template>
  <div
    class="card-hover group relative cursor-pointer focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
    role="link"
    :aria-label="`View details for ${hackathon.name}`"
    tabindex="0"
    @click="$emit('open', hackathon.id)"
    @keydown.enter="$emit('open', hackathon.id)"
    @keydown.space.prevent="$emit('open', hackathon.id)"
  >
    <div class="relative h-48 mb-4 rounded-xl overflow-hidden">
      <img :src="hackathon.image" :alt="hackathon.name" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
      <div class="absolute top-4 right-4">
        <Badge :variant="statusBadgeVariant" size="sm">
          {{ hackathon.status }}
        </Badge>
      </div>
      <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
        <h3 class="text-xl font-bold text-white">{{ hackathon.name }}</h3>
      </div>
    </div>

    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <OrganizationAvatar
            :organization-name="hackathon.organization"
            size="md"
          />
          <span class="text-gray-600 dark:text-gray-400">{{ hackathon.organization }}</span>
        </div>
        <div v-if="hackathon.prize" class="text-right">
          <div class="text-lg font-bold text-gray-900 dark:text-white">{{ hackathon.prize }}</div>
          <div class="text-sm text-gray-500 dark:text-gray-400">{{ prizePoolLabel }}</div>
        </div>
      </div>

      <p class="text-gray-600 dark:text-gray-400 text-sm">{{ hackathon.description }}</p>

      <HackathonCardStats
        :participants="hackathon.participants"
        :participants-label="participantsLabel"
        :projects="hackathon.projects"
        :projects-label="projectsLabel"
        :duration="hackathon.duration"
        :duration-label="durationLabel"
      />

      <div class="flex items-center justify-between text-sm">
        <div class="flex items-center text-gray-500 dark:text-gray-400">{{ hackathon.startDate }} - {{ hackathon.endDate }}</div>
        <span class="text-gray-500 dark:text-gray-400">{{ hackathon.location }}</span>
      </div>

      <div class="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-800">
        <div class="flex items-center space-x-2">
          <Badge
            v-for="tag in hackathon.tags.slice(0, 2)"
            :key="tag"
            variant="primary"
            size="sm"
          >
            {{ tag }}
          </Badge>
          <span v-if="hackathon.tags.length > 2" class="text-xs text-gray-500 dark:text-gray-400">+{{ hackathon.tags.length - 2 }}</span>
        </div>
        <NuxtLink :to="`/hackathons/${hackathon.id}`" class="btn btn-primary px-4 py-2 text-sm" @click.stop>
          {{ viewDetailsLabel }}
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Badge from '~/components/atoms/Badge.vue'
import OrganizationAvatar from '~/components/atoms/OrganizationAvatar.vue'
import HackathonCardStats from '~/components/molecules/HackathonCardStats.vue'

const props = defineProps<{
  hackathon: any
  participantsLabel: string
  projectsLabel: string
  durationLabel: string
  prizePoolLabel: string
  viewDetailsLabel: string
}>()

defineEmits<{ (e: 'open', id: number): void }>()

const statusBadgeVariant = computed(() => {
  if (props.hackathon.status === 'Active') return 'success'
  if (props.hackathon.status === 'Upcoming') return 'warning'
  if (props.hackathon.status === 'Completed') return 'info'
  return 'primary'
})
</script>