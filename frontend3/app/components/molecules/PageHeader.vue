<template>
  <div class="mb-8">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          {{ title }}
        </h1>
        <p v-if="subtitle" class="mt-2 text-gray-600 dark:text-gray-300">
          {{ subtitle }}
        </p>
      </div>
      
      <div class="flex items-center gap-3">
        <slot name="actions">
          <Button
            v-if="showBackButton"
            variant="outline"
            size="sm"
            @click="$emit('back')"
          >
            <template #icon>
              <Icon name="arrow-left" size="sm" />
            </template>
            Back
          </Button>
          
          <Button
            v-if="primaryAction"
            :variant="primaryAction.variant || 'primary'"
            size="sm"
            @click="$emit('primary-action')"
          >
            <template v-if="primaryAction.icon" #icon>
              <Icon :name="primaryAction.icon" size="sm" />
            </template>
            {{ primaryAction.label }}
          </Button>
        </slot>
      </div>
    </div>
    
    <div v-if="breadcrumbs && breadcrumbs.length > 0" class="mt-4">
      <nav class="flex items-center text-sm">
        <NuxtLink
          v-for="(crumb, index) in breadcrumbs"
          :key="index"
          :to="crumb.to"
          class="text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
        >
          {{ crumb.label }}
        </NuxtLink>
        <span class="mx-2 text-gray-400">/</span>
        <span class="text-gray-900 dark:text-white font-medium">
          {{ title }}
        </span>
      </nav>
    </div>
    
    <div v-if="stats && stats.length > 0" class="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div
        v-for="(stat, index) in stats"
        :key="index"
        class="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg"
      >
        <div class="text-2xl font-bold" :class="stat.valueClass || 'text-primary-600 dark:text-primary-400'">
          {{ stat.value }}
        </div>
        <div class="text-sm text-gray-600 dark:text-gray-300 mt-1">
          {{ stat.label }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from '@/components/atoms/Button.vue'
import Icon from '@/components/atoms/Icon.vue'

interface Breadcrumb {
  label: string
  to: string
}

interface Stat {
  value: string | number
  label: string
  valueClass?: string
}

interface PrimaryAction {
  label: string
  variant?: string
  icon?: string
}

interface Props {
  title: string
  subtitle?: string
  breadcrumbs?: Breadcrumb[]
  stats?: Stat[]
  showBackButton?: boolean
  primaryAction?: PrimaryAction
}

const props = defineProps<Props>()
defineEmits<{
  'back': []
  'primary-action': []
}>()
</script>

<style scoped>
/* Add any custom styles if needed */
</style>