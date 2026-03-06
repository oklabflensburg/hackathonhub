<template>
  <component
    :is="asLink ? (to ? 'NuxtLink' : 'a') : 'div'"
    :to="asLink && to ? to : undefined"
    :href="asLink && external && to ? to : undefined"
    :target="asLink && external ? '_blank' : undefined"
    :rel="asLink && external ? 'noopener noreferrer' : undefined"
    class="logo inline-flex items-center focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded"
    :class="[
      sizeClasses,
      { 'cursor-pointer hover:opacity-90 transition-opacity': asLink }
    ]"
    @click="$emit('click', $event)"
  >
    <!-- SVG Logo -->
    <svg
      v-if="!textLogo"
      :class="svgClasses"
      viewBox="0 0 40 40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <!-- Hackathon Dashboard Logo -->
      <path
        d="M20 0C8.954 0 0 8.954 0 20s8.954 20 20 20 20-8.954 20-20S31.046 0 20 0zm0 36c-8.837 0-16-7.163-16-16S11.163 4 20 4s16 7.163 16 16-7.163 16-16 16z"
        :class="logoPathClasses"
      />
      <path
        d="M20 8c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm0 20c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8z"
        :class="logoPathClasses"
      />
      <path
        d="M20 12c-4.418 0-8 3.582-8 8s3.582 8 8 8 8-3.582 8-8-3.582-8-8-8zm0 12c-2.209 0-4-1.791-4-4s1.791-4 4-4 4 1.791 4 4-1.791 4-4 4z"
        :class="logoInnerPathClasses"
      />
    </svg>

    <!-- Text Logo (falls gewünscht oder als Fallback) -->
    <div
      v-else
      :class="textClasses"
      class="font-bold tracking-tight"
    >
      <slot>
        Hackathon Dashboard
      </slot>
    </div>

    <!-- Badge für Beta/Version -->
    <span
      v-if="showBadge"
      class="ml-2 inline-flex items-center rounded-full bg-primary-100 dark:bg-primary-900 px-2 py-0.5 text-xs font-medium text-primary-800 dark:text-primary-200"
    >
      {{ badgeText }}
    </span>
  </component>
</template>

<script setup lang="ts">
import type { LogoProps } from '~/types/layout-types'

interface Props extends LogoProps {
  /** Text-Logo anstelle von SVG */
  textLogo?: boolean
  /** Zeige Badge */
  showBadge?: boolean
  /** Badge Text */
  badgeText?: string
  /** Externer Link (öffnet in neuem Tab) */
  external?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  darkMode: undefined,
  asLink: false,
  to: '/',
  textLogo: false,
  showBadge: false,
  badgeText: 'Beta',
  external: false,
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

// Größenklassen basierend auf Prop
const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'h-6 w-6'
    case 'md':
      return 'h-8 w-8'
    case 'lg':
      return 'h-12 w-12'
    case 'xl':
      return 'h-16 w-16'
    default:
      return 'h-8 w-8'
  }
})

// SVG Klassen
const svgClasses = computed(() => {
  return `block ${sizeClasses.value}`
})

// Logo Path Farbklassen
const logoPathClasses = computed(() => {
  if (props.darkMode !== undefined) {
    return props.darkMode
      ? 'fill-gray-200'
      : 'fill-gray-800'
  }
  // Automatisch basierend auf Theme
  return 'fill-gray-800 dark:fill-gray-200'
})

// Logo Inner Path Farbklassen
const logoInnerPathClasses = computed(() => {
  if (props.darkMode !== undefined) {
    return props.darkMode
      ? 'fill-primary-400'
      : 'fill-primary-600'
  }
  // Automatisch basierend auf Theme
  return 'fill-primary-600 dark:fill-primary-400'
})

// Text Klassen
const textClasses = computed(() => {
  const sizeMap = {
    sm: 'text-sm',
    md: 'text-lg',
    lg: 'text-2xl',
    xl: 'text-4xl',
  }
  
  const colorClasses = props.darkMode !== undefined
    ? props.darkMode
      ? 'text-gray-200'
      : 'text-gray-800'
    : 'text-gray-800 dark:text-gray-200'
  
  return `${sizeMap[props.size] || sizeMap.md} ${colorClasses}`
})
</script>

<style scoped>
.logo {
  transition: opacity 0.2s ease;
}

.logo:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-primary-500);
}
</style>