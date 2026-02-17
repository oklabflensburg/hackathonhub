<template>
  <!-- Modern Stats Card Component -->
  <NuxtLink
    :to="link"
    class="group block focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
  >
    <div
      class="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm 
             rounded-lg shadow-md p-4 sm:p-5 lg:p-6
             border border-gray-100 dark:border-gray-700
             group-hover:border-primary-200 dark:group-hover:border-primary-800
             transition-all duration-200 hover:shadow-lg
             hover:-translate-y-0.5"
    >
      <!-- Stack vertically on mobile, horizontal on tablet+ -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        
        <!-- Icon with gradient background -->
        <div
          :class="[
            'w-10 h-10 sm:w-12 sm:h-12 rounded-lg flex items-center justify-center mb-3 sm:mb-0 sm:mr-4',
            iconBackground
          ]"
        >
          <component
            :is="icon"
            class="w-5 h-5 sm:w-6 sm:h-6 text-white"
          />
        </div>
        
        <!-- Content -->
        <div class="text-center sm:text-left flex-1">
          <!-- Label -->
          <p class="text-xs font-medium text-gray-500 dark:text-gray-400 
                    uppercase tracking-wide mb-1">
            {{ label }}
          </p>
          
          <!-- Value with responsive sizing -->
          <p class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
            {{ value }}
          </p>
          
          <!-- Optional description -->
          <p v-if="description" class="text-xs text-gray-600 dark:text-gray-400 mt-1">
            {{ description }}
          </p>
        </div>
        
        <!-- Arrow indicator (hidden on mobile) -->
        <div class="hidden sm:block ml-4">
          <svg
            class="w-5 h-5 text-gray-400 group-hover:text-primary-500 
                   dark:text-gray-500 dark:group-hover:text-primary-400
                   transition-colors"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </div>
      </div>
      
      <!-- Action link (simplified on mobile) -->
      <div class="mt-3 sm:mt-4 text-center sm:text-left">
        <span
          class="text-xs font-medium text-primary-600 dark:text-primary-400 
                 group-hover:text-primary-700 dark:group-hover:text-primary-300 
                 transition-colors inline-flex items-center"
        >
          {{ actionText }}
          <svg
            class="w-3 h-3 ml-1 hidden sm:inline-block"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </span>
      </div>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
interface Props {
  label: string
  value: string | number
  description?: string
  link: string
  actionText: string
  icon: any // Vue component
  iconBackground: string // Tailwind classes for icon background
}

defineProps<Props>()
</script>

<style scoped>
/* Custom gradient backgrounds for different stat types */
.gradient-blue {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
}

.gradient-green {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.gradient-purple {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.gradient-orange {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

/* Glass effect enhancement */
.glass-effect {
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}
</style>
