<template>
  <svg
    v-if="isSvgIcon"
    :class="iconClasses"
    :style="iconStyles"
    :aria-label="ariaLabel"
    :role="role"
    :viewBox="viewBox"
    :fill="fill"
    :stroke="stroke"
    v-bind="$attrs"
    v-html="svgContent"
  />
  <component
    v-else-if="lucideIcon"
    :is="lucideIcon"
    :class="iconClasses"
    :style="iconStyles"
    :aria-label="ariaLabel"
    :role="role"
    v-bind="$attrs"
  />
  <span
    v-else
    :class="iconClasses"
    :style="iconStyles"
    :aria-label="ariaLabel"
    :role="role"
    v-bind="$attrs"
  >
    {{ name }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import * as LucideIcons from 'lucide-vue-next'

export interface IconProps {
  /** Name of the icon or SVG content */
  name: string
  /** Size of the icon in pixels or Tailwind class */
  size?: number | string
  /** Color of the icon (CSS color or Tailwind class) */
  color?: string
  /** Whether the icon is an SVG icon */
  isSvg?: boolean
  /** SVG viewBox attribute */
  viewBox?: string
  /** SVG fill color */
  fill?: string
  /** SVG stroke color */
  stroke?: string
  /** Additional CSS classes */
  class?: string
  /** ARIA label for accessibility */
  ariaLabel?: string
  /** Role for accessibility */
  role?: string
}

const props = withDefaults(defineProps<IconProps>(), {
  size: 24,
  color: 'currentColor',
  isSvg: false,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  role: 'img',
})

// Check if this is an SVG icon (contains SVG tags)
const isSvgIcon = computed(() => {
  return props.isSvg || props.name.includes('<svg') || props.name.includes('<path')
})

// Extract SVG content (remove <svg> tags if present)
const svgContent = computed(() => {
  if (!isSvgIcon.value) return ''
  
  const svg = props.name
  // Remove <svg> tags and extract inner content
  // Use [\s\S]*? instead of .*? with /s flag for cross-browser compatibility
  const match = svg.match(/<svg[^>]*>([\s\S]*?)<\/svg>/)
  return match ? match[1] : svg
})

// Map icon name to Lucide icon component
const lucideIcon = computed(() => {
  if (isSvgIcon.value) return null
  
  const iconName = props.name
  if (!iconName) return null
  
  // Convert kebab-case to PascalCase (e.g., check-circle -> CheckCircle)
  const pascalName = iconName
    .split('-')
    .map(part => part.charAt(0).toUpperCase() + part.slice(1))
    .join('')
  
  // Special cases for icon name mappings
  const iconMap: Record<string, string> = {
    'file-text': 'FileText',
    'check-circle': 'CheckCircle',
    'alert-circle': 'AlertCircle',
    'loader': 'Loader',
    'search': 'Search',
    'x': 'X',
    'users': 'Users',
    'clock': 'Clock',
    'shield': 'Shield',
    'copy': 'Copy',
    'download': 'Download',
    'printer': 'Printer',
    'github': 'Github',
    'mail': 'Mail',
    'arrow-right': 'ArrowRight',
    'calendar': 'Calendar',
    'eye': 'Eye',
    'heart': 'Heart',
    'user': 'User',
    'chevron-left': 'ChevronLeft',
    'chevron-right': 'ChevronRight',
    'chevron-up': 'ChevronUp',
    'chevron-down': 'ChevronDown',
    'arrow-left': 'ArrowLeft',
    'arrow-up': 'ArrowUp',
    'arrow-down': 'ArrowDown',
    'plus': 'Plus',
    'minus': 'Minus',
    'edit': 'Edit',
    'trash-2': 'Trash2',
    'star': 'Star',
    'bookmark': 'Bookmark',
    'bookmark-filled': 'Bookmark',
    'flag': 'Flag',
    'share-2': 'Share2',
    'message-square': 'MessageSquare',
    'thumbs-up': 'ThumbsUp',
    'thumbs-up-filled': 'ThumbsUp',
    'thumbs-down': 'ThumbsDown',
    'external-link': 'ExternalLink',
    'compass': 'Compass',
    'award': 'Award',
    'crown': 'Crown',
    'dollar-sign': 'DollarSign',
    'map-pin': 'MapPin',
    'globe': 'Globe',
    'twitter': 'Twitter',
    'linkedin': 'Linkedin',
    'refresh-cw': 'RefreshCw',
    'sort': 'Sort',
    'material-symbols:location-on': 'MapPin', // Map to MapPin as fallback
  }
  
  const mappedName = iconMap[iconName] || pascalName
  // Type assertion to handle dynamic property access
  const lucideIconsAny = LucideIcons as Record<string, any>
  return lucideIconsAny[mappedName] || null
})

// Map size strings to Tailwind classes
const sizeMapping: Record<string, string> = {
  'xs': 'w-3 h-3',
  'sm': 'w-4 h-4',
  'md': 'w-5 h-5',
  'lg': 'w-6 h-6',
  'xl': 'w-8 h-8',
  '2xl': 'w-10 h-10',
  '3xl': 'w-12 h-12',
  '4xl': 'w-16 h-16'
}

// Generate icon classes based on props
const iconClasses = computed(() => {
  const classes = ['icon', 'inline-block', 'align-middle', 'flex-shrink-0']
  
  // Handle size - if it's a string, check if it's a mapped size
  if (typeof props.size === 'string') {
    const mappedSize = sizeMapping[props.size]
    if (mappedSize) {
      // Add width and height classes
      classes.push(...mappedSize.split(' '))
    } else if (props.size.includes('w-') || props.size.includes('h-')) {
      // If it already contains width/height classes, add them
      classes.push(...props.size.split(' '))
    } else {
      // Otherwise assume it's a Tailwind class
      classes.push(props.size)
    }
  }
  
  // Handle color - if it starts with text- assume Tailwind
  if (props.color && props.color.startsWith('text-')) {
    classes.push(props.color)
  }
  
  // Add custom classes
  if (props.class) {
    classes.push(props.class)
  }
  
  return classes.join(' ')
})

// Generate inline styles for size and color
const iconStyles = computed(() => {
  const styles: Record<string, string> = {}
  
  // Set size if it's a number
  if (typeof props.size === 'number') {
    styles.width = `${props.size}px`
    styles.height = `${props.size}px`
  }
  
  // Set color if it's not a Tailwind class
  if (props.color && !props.color.startsWith('text-')) {
    styles.color = props.color
  }
  
  return styles
})
</script>

<style scoped>
.icon {
  display: inline-block;
  vertical-align: middle;
  flex-shrink: 0;
}

/* Animation for loading/spinner icons */
.icon.spin {
  animation: icon-spin 1s linear infinite;
}

@keyframes icon-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>