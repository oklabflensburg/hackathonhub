<template>
  <div class="h-48 relative">
    <!-- Background image or gradient -->
    <div v-if="hackathon.image_url" class="absolute inset-0 bg-cover bg-center" :style="{ backgroundImage: `url(${hackathon.image_url})` }">
      <div class="absolute inset-0 bg-black/40"></div>
    </div>
    <div v-else class="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-600">
      <div class="absolute inset-0 bg-black/20"></div>
    </div>

    <!-- Status badge in top-right corner -->
    <div class="absolute top-4 right-4 z-10">
      <HackathonStatusBadge 
        :status="hackathon.status" 
        size="lg"
        :rounded="true"
        :shadow="true"
        :tooltip="getStatusTooltip(hackathon.status)"
      />
    </div>

    <!-- Main content -->
    <div class="relative h-full flex items-center justify-center p-8">
      <div class="text-center">
        <h1 class="text-4xl font-bold text-white mb-4">{{ hackathon.name }}</h1>
        
        <!-- Date and location with icons -->
        <div class="flex flex-wrap items-center justify-center gap-4 text-white/90">
          <div class="flex items-center space-x-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span>{{ formatDateTime(hackathon.start_date) }} - {{ formatDateTime(hackathon.end_date) }}</span>
          </div>
          
          <div class="flex items-center space-x-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span>{{ hackathon.location || virtualLabel }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { HackathonHeroProps } from '~/types/hackathon-types'
import HackathonStatusBadge from '~/components/atoms/HackathonStatusBadge.vue'

const props = defineProps<HackathonHeroProps>()

const getStatusTooltip = (status: string) => {
  switch (status) {
    case 'active': return 'This hackathon is currently running'
    case 'upcoming': return 'This hackathon will start soon'
    case 'completed': return 'This hackathon has ended'
    default: return `Status: ${status}`
  }
}
</script>