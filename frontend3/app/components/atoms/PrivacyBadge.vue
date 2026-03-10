<template>
  <span
    :class="[
      'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
      variantClasses
    ]"
  >
    <slot>{{ label }}</slot>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

type PrivacyLevel = 'public' | 'private' | 'friends' | 'team' | 'custom'

interface Props {
  level?: PrivacyLevel
  label?: string
}

const props = withDefaults(defineProps<Props>(), {
  level: 'public',
  label: undefined
})

const variantClasses = computed(() => {
  const variants: Record<PrivacyLevel, string> = {
    public: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    private: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
    friends: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
    team: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
    custom: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
  }
  return variants[props.level]
})

const label = computed(() => {
  if (props.label) return props.label
  
  const labels: Record<PrivacyLevel, string> = {
    public: 'Public',
    private: 'Private',
    friends: 'Friends Only',
    team: 'Team Only',
    custom: 'Custom'
  }
  return labels[props.level]
})
</script>