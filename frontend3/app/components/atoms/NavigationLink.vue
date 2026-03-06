<template>
  <component
    :is="componentType"
    :to="!external && to ? to : undefined"
    :href="external && to ? to : undefined"
    :target="external ? '_blank' : undefined"
    :rel="external ? 'noopener noreferrer' : undefined"
    class="navigation-link inline-flex items-center focus:outline-none transition-colors duration-200"
    :class="[
      baseClasses,
      activeClasses,
      disabledClasses,
      sizeClasses,
      iconPositionClasses
    ]"
    :aria-current="active ? 'page' : undefined"
    :aria-disabled="disabled"
    @click="handleClick"
  >
    <!-- Icon (links) -->
    <span
      v-if="icon && iconPosition === 'left'"
      class="flex-shrink-0"
      :class="iconClasses"
      aria-hidden="true"
    >
      <slot name="icon">
        <component
          :is="resolveIconComponent(icon)"
          v-if="isComponentIcon(icon)"
          :class="iconSizeClasses"
        />
        <span v-else :class="icon">{{ icon }}</span>
      </slot>
    </span>

    <!-- Text Content -->
    <span class="truncate">
      <slot>
        {{ label }}
      </slot>
    </span>

    <!-- Icon (rechts) -->
    <span
      v-if="icon && iconPosition === 'right'"
      class="flex-shrink-0 ml-2"
      :class="iconClasses"
      aria-hidden="true"
    >
      <slot name="icon-right">
        <component
          :is="resolveIconComponent(icon)"
          v-if="isComponentIcon(icon)"
          :class="iconSizeClasses"
        />
        <span v-else :class="icon">{{ icon }}</span>
      </slot>
    </span>

    <!-- External Link Indicator -->
    <span
      v-if="external"
      class="ml-1 flex-shrink-0"
      aria-hidden="true"
    >
      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
      </svg>
    </span>
  </component>
</template>

<script setup lang="ts">
import type { NavigationLinkProps } from '~/types/layout-types'

interface Props extends NavigationLinkProps {
  /** Label für den Link */
  label?: string
  /** Größe */
  size?: 'sm' | 'md' | 'lg'
  /** Icon Position */
  iconPosition?: 'left' | 'right'
  /** Vollständige Breite */
  fullWidth?: boolean
  /** Variante */
  variant?: 'default' | 'primary' | 'secondary' | 'ghost'
}

const props = withDefaults(defineProps<Props>(), {
  to: '#',
  active: false,
  icon: undefined,
  external: false,
  disabled: false,
  label: '',
  size: 'md',
  iconPosition: 'left',
  fullWidth: false,
  variant: 'default',
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

// Bestimme Komponententyp basierend auf Props
const componentType = computed(() => {
  if (props.disabled) {
    return 'span'
  }
  if (props.external) {
    return 'a'
  }
  // Für interne Links verwenden wir NuxtLink
  return 'NuxtLink'
})

// Basisklassen
const baseClasses = computed(() => {
  const classes = []
  
  // Width
  if (props.fullWidth) {
    classes.push('w-full justify-center')
  }
  
  // Variant-spezifische Klassen
  switch (props.variant) {
    case 'primary':
      classes.push('text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300')
      break
    case 'secondary':
      classes.push('text-gray-600 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300')
      break
    case 'ghost':
      classes.push('text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded')
      break
    default: // default
      classes.push('text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100')
      break
  }
  
  return classes.join(' ')
})

// Aktive Klassen
const activeClasses = computed(() => {
  if (!props.active) return ''
  
  switch (props.variant) {
    case 'primary':
      return 'font-semibold text-primary-700 dark:text-primary-300'
    case 'secondary':
      return 'font-semibold text-gray-800 dark:text-gray-200'
    case 'ghost':
      return 'font-semibold bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
    default:
      return 'font-semibold text-gray-900 dark:text-gray-100'
  }
})

// Deaktivierte Klassen
const disabledClasses = computed(() => {
  if (!props.disabled) return ''
  return 'opacity-50 cursor-not-allowed pointer-events-none'
})

// Größenklassen
const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'text-sm px-2 py-1'
    case 'md':
      return 'text-base px-3 py-2'
    case 'lg':
      return 'text-lg px-4 py-3'
    default:
      return 'text-base px-3 py-2'
  }
})

// Icon Position Klassen
const iconPositionClasses = computed(() => {
  if (!props.icon) return ''
  
  if (props.iconPosition === 'left') {
    return props.fullWidth ? 'justify-start' : ''
  } else {
    return props.fullWidth ? 'justify-between' : ''
  }
})

// Icon Klassen
const iconClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'w-4 h-4'
    case 'md':
      return 'w-5 h-5'
    case 'lg':
      return 'w-6 h-6'
    default:
      return 'w-5 h-5'
  }
})

// Icon Größenklassen
const iconSizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'w-4 h-4'
    case 'md':
      return 'w-5 h-5'
    case 'lg':
      return 'w-6 h-6'
    default:
      return 'w-5 h-5'
  }
})

// Icon-Helper
function isComponentIcon(icon: string): boolean {
  // Einfache Heuristik: Wenn Icon mit "Icon" endet, ist es eine Komponente
  return icon.endsWith('Icon') || icon.includes('.')
}

function resolveIconComponent(icon: string) {
  // In einer echten Implementierung würden wir hier Icon-Komponenten dynamisch importieren
  // Für jetzt geben wir einen Platzhalter zurück
  return 'span'
}

// Click Handler
function handleClick(event: MouseEvent) {
  if (props.disabled) {
    event.preventDefault()
    return
  }
  
  emit('click', event)
}
</script>

<style scoped>
.navigation-link {
  transition-property: color, background-color, border-color, opacity;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.navigation-link:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-primary-500);
}

.navigation-link[aria-current="page"] {
  position: relative;
}

.navigation-link[aria-current="page"]::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: var(--color-primary-500);
  border-radius: 1px;
}
</style>