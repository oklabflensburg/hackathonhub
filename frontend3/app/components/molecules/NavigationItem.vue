<template>
  <div class="navigation-item group">
    <!-- Main Navigation Link -->
    <NavigationLink
      :to="to"
      :active="active"
      :icon="icon"
      :external="external"
      :disabled="disabled"
      :label="label"
      :size="size"
      :icon-position="iconPosition"
      :full-width="fullWidth"
      :variant="variant"
      class="navigation-item-link"
      :class="[
        paddingClasses,
        { 'justify-between': badgeCount !== undefined }
      ]"
      @click="handleLinkClick"
    >
      <!-- Left Content Slot -->
      <template #icon>
        <slot name="icon" />
      </template>

      <!-- Default Content -->
      <span class="flex items-center">
        <span class="truncate">
          {{ label }}
        </span>

        <!-- Badge -->
        <span
          v-if="showBadge"
          class="ml-2 flex-shrink-0"
          :class="badgeClasses"
          aria-hidden="true"
        >
          {{ badgeCount }}
        </span>
      </span>

      <!-- Right Content Slot -->
      <template #icon-right>
        <slot name="icon-right" />
        
        <!-- Chevron für Dropdown -->
        <svg
          v-if="hasChildren"
          class="w-4 h-4 ml-1 transition-transform duration-200"
          :class="{
            'rotate-90': childrenVisible,
            'group-hover:rotate-90': !childrenVisible && showChildrenOnHover
          }"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </template>
    </NavigationLink>

    <!-- Children (Dropdown) -->
    <div
      v-if="hasChildren && childrenVisible"
      class="navigation-item-children"
      :class="childrenClasses"
    >
      <div class="py-1">
        <NavigationItem
          v-for="child in children"
          :key="child.id"
          :to="child.to"
          :active="isChildActive(child)"
          :icon="child.icon"
          :label="child.label"
          :badge-count="child.badgeCount"
          :size="childSize"
          variant="ghost"
          class="navigation-item-child"
          @click="handleChildClick(child, $event)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NavigationItem as NavigationItemType } from '~/types/layout-types'
import NavigationLink from '~/components/atoms/NavigationLink.vue'

interface Props {
  /** Navigation Item Daten */
  item?: NavigationItemType
  /** Route oder URL */
  to?: string
  /** Aktiver Zustand */
  active?: boolean
  /** Icon */
  icon?: string
  /** Label */
  label?: string
  /** Badge Anzahl */
  badgeCount?: number
  /** Zeige Badge nur wenn > 0 */
  showBadgeOnlyWhenPositive?: boolean
  /** Größe */
  size?: 'sm' | 'md' | 'lg'
  /** Icon Position */
  iconPosition?: 'left' | 'right'
  /** Vollständige Breite */
  fullWidth?: boolean
  /** Variante */
  variant?: 'default' | 'primary' | 'secondary' | 'ghost'
  /** Children Items */
  children?: NavigationItemType[]
  /** Children sichtbar */
  childrenVisible?: boolean
  /** Zeige Children on Hover */
  showChildrenOnHover?: boolean
  /** Children Größe */
  childSize?: 'sm' | 'md' | 'lg'
  /** Padding */
  padding?: 'none' | 'sm' | 'md' | 'lg'
  /** Externer Link */
  external?: boolean
  /** Deaktiviert */
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  item: undefined,
  to: '#',
  active: false,
  icon: undefined,
  label: '',
  badgeCount: undefined,
  showBadgeOnlyWhenPositive: true,
  size: 'md',
  iconPosition: 'left',
  fullWidth: false,
  variant: 'default',
  children: () => [],
  childrenVisible: false,
  showChildrenOnHover: true,
  childSize: 'sm',
  padding: 'md',
  external: false,
  disabled: false,
})

const emit = defineEmits<{
  click: [event: MouseEvent]
  'child-click': [child: NavigationItemType, event: MouseEvent]
  'toggle-children': [visible: boolean]
}>()

// Verwende Item-Props falls vorhanden
const itemProps = computed(() => {
  if (props.item) {
    return {
      to: props.item.to,
      active: props.active,
      icon: props.item.icon,
      label: props.item.label,
      badgeCount: props.item.badgeCount,
      external: props.item.external,
      children: props.item.children,
    }
  }
  return {
    to: props.to,
    active: props.active,
    icon: props.icon,
    label: props.label,
    badgeCount: props.badgeCount,
    external: props.external,
    children: props.children,
  }
})

// Hat Children?
const hasChildren = computed(() => {
  return (itemProps.value.children?.length || 0) > 0
})

// Zeige Badge?
const showBadge = computed(() => {
  if (itemProps.value.badgeCount === undefined) {
    return false
  }
  
  if (props.showBadgeOnlyWhenPositive) {
    return itemProps.value.badgeCount > 0
  }
  
  return true
})

// Badge Klassen
const badgeClasses = computed(() => {
  const base = 'inline-flex items-center justify-center rounded-full text-xs font-medium min-w-[1.25rem] h-5 px-1.5'
  
  if (props.active) {
    return `${base} bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200`
  }
  
  return `${base} bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200`
})

// Padding Klassen
const paddingClasses = computed(() => {
  switch (props.padding) {
    case 'none':
      return 'px-0 py-0'
    case 'sm':
      return 'px-2 py-1'
    case 'md':
      return 'px-3 py-2'
    case 'lg':
      return 'px-4 py-3'
    default:
      return 'px-3 py-2'
  }
})

// Children Klassen
const childrenClasses = computed(() => {
  const classes = ['absolute z-10 mt-1 w-48 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 dark:ring-gray-700']
  
  if (props.fullWidth) {
    classes.push('w-full')
  }
  
  return classes.join(' ')
})

// Prüft ob Child aktiv ist
function isChildActive(child: NavigationItemType): boolean {
  // Einfache Implementierung: Prüfe ob aktuelle Route mit Child Route übereinstimmt
  // In einer echten Implementierung würden wir den Router verwenden
  const currentRoute = useRoute()
  return currentRoute.path === child.to || currentRoute.path.startsWith(child.to + '/')
}

// Link Click Handler
function handleLinkClick(event: MouseEvent) {
  if (props.disabled) {
    event.preventDefault()
    return
  }
  
  // Toggle Children wenn vorhanden
  if (hasChildren.value) {
    emit('toggle-children', !props.childrenVisible)
    event.preventDefault()
  }
  
  emit('click', event)
}

// Child Click Handler
function handleChildClick(child: NavigationItemType, event: MouseEvent) {
  emit('child-click', child, event)
}
</script>

<style scoped>
.navigation-item {
  position: relative;
}

.navigation-item-link {
  transition: all 0.2s ease;
}

.navigation-item-link:hover {
  transform: translateX(2px);
}

.navigation-item-child {
  transition: all 0.15s ease;
}

.navigation-item-child:hover {
  background-color: var(--color-gray-100);
  transform: translateX(4px);
}

.dark .navigation-item-child:hover {
  background-color: var(--color-gray-800);
}

.navigation-item-children {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>