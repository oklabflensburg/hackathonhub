<template>
  <aside
    class="app-sidebar"
    :class="sidebarClasses"
    :aria-label="sidebarAriaLabel"
  >
    <!-- Sidebar Header -->
    <div class="sidebar-header" :class="headerClasses">
      <!-- Logo -->
      <div class="sidebar-logo">
        <Logo
          :size="logoSize"
          :as-link="true"
          to="/"
          :text-logo="!collapsed"
          @click="$emit('logo-click', $event)"
        />
      </div>

      <!-- Toggle Button (nur wenn toggleable) -->
      <Button
        v-if="toggleable"
        type="button"
        variant="ghost"
        size="sm"
        :aria-label="toggleAriaLabel"
        :title="toggleTitle"
        :class="['sidebar-toggle', toggleButtonClasses]"
        @click="toggleSidebar"
      >
        <template #icon-left>
          <svg
            class="toggle-icon"
            :class="{ 'rotate-180': collapsed }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
            />
          </svg>
        </template>
      </Button>
    </div>

    <!-- Navigation -->
    <nav class="sidebar-navigation" :class="navigationClasses" aria-label="Main navigation">
      <div class="navigation-content">
        <!-- Navigation Items -->
        <ul class="navigation-list" role="list">
          <li
            v-for="item in filteredNavigationItems"
            :key="item.id"
            class="navigation-list-item"
          >
            <NavigationItemComponent
              :item="item"
              :active="isItemActive(item)"
              :size="navigationItemSize"
              :full-width="!collapsed"
              :variant="navigationItemVariant"
              :padding="navigationItemPadding"
              :children-visible="expandedItems.includes(item.id)"
              @click="handleItemClick(item, $event)"
              @child-click="handleChildClick"
              @toggle-children="toggleItemChildren(item.id)"
            />
          </li>
        </ul>

        <!-- Divider -->
        <div v-if="showDivider" class="sidebar-divider" />

        <!-- Additional Navigation (falls vorhanden) -->
        <div v-if="additionalNavigationItems?.length" class="additional-navigation">
          <ul class="navigation-list" role="list">
            <li
              v-for="item in additionalNavigationItems"
              :key="item.id"
              class="navigation-list-item"
            >
              <NavigationItemComponent
                :item="item"
                :active="isItemActive(item)"
                :size="navigationItemSize"
                :full-width="!collapsed"
                :variant="navigationItemVariant"
                :padding="navigationItemPadding"
                @click="handleItemClick(item, $event)"
              />
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Sidebar Footer -->
    <div v-if="showFooter" class="sidebar-footer" :class="footerClasses">
      <!-- Theme Toggle -->
      <div v-if="showThemeToggle" class="sidebar-theme-toggle">
        <ThemeToggle
          :size="themeToggleSize"
          :variant="collapsed ? 'simple' : 'select'"
          :show-label="!collapsed"
          @theme-change="$emit('theme-change', $event)"
        />
      </div>

      <!-- User Menu -->
      <div v-if="showUserMenu && user" class="sidebar-user-menu">
        <UserMenu
          :user="user"
          :avatar-size="userMenuAvatarSize"
          :variant="collapsed ? 'avatar-only' : 'with-info'"
          :show-user-info="!collapsed"
          :show-email="!collapsed"
          :placement="userMenuPlacement"
          @option-click="$emit('user-menu-option-click', $event)"
          @avatar-click="$emit('user-menu-avatar-click', $event)"
          @theme-change="$emit('theme-change', $event)"
        />
      </div>

      <!-- Custom Footer Slot -->
      <slot name="footer" :collapsed="collapsed" />
    </div>

    <!-- Collapsed Overlay (für mobile) -->
    <div
      v-if="collapsed && showCollapsedOverlay"
      class="sidebar-collapsed-overlay"
      @click="toggleSidebar"
    >
      <div class="overlay-content">
        <svg
          class="overlay-icon"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 5l7 7-7 7M5 5l7 7-7 7"
          />
        </svg>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import type { SidebarProps, NavigationItem as NavigationItemType } from '~/types/layout-types'
import { DEFAULT_NAVIGATION_ITEMS, filterNavigationItems } from '~/types/layout-types'
import { useLayoutNavigation } from '~/composables/useLayoutNavigation'

import Logo from '~/components/atoms/Logo.vue'
import NavigationItemComponent from '~/components/molecules/NavigationItem.vue'
import ThemeToggle from '~/components/molecules/ThemeToggle.vue'
import UserMenu from '~/components/molecules/UserMenu.vue'
import Button from '~/components/atoms/Button.vue'

interface Props extends SidebarProps {
  /** Zusammengeklappter Zustand */
  collapsed?: boolean
  /** Kann zusammengeklappt werden */
  toggleable?: boolean
  /** Zeige Toggle Button */
  showToggleButton?: boolean
  /** Zeige Divider */
  showDivider?: boolean
  /** Zeige Footer */
  showFooter?: boolean
  /** Zeige Theme Toggle */
  showThemeToggle?: boolean
  /** Zeige User Menu */
  showUserMenu?: boolean
  /** Zusätzliche Navigationselemente */
  additionalNavigationItems?: NavigationItemType[]
  /** Navigation Item Größe */
  navigationItemSize?: 'sm' | 'md' | 'lg'
  /** Navigation Item Variante */
  navigationItemVariant?: 'default' | 'primary' | 'secondary' | 'ghost'
  /** Navigation Item Padding */
  navigationItemPadding?: 'none' | 'sm' | 'md' | 'lg'
  /** Theme Toggle Größe */
  themeToggleSize?: 'sm' | 'md' | 'lg'
  /** User Menu Avatar Größe */
  userMenuAvatarSize?: 'sm' | 'md' | 'lg'
  /** User Menu Platzierung */
  userMenuPlacement?: 'bottom-start' | 'bottom-end' | 'top-start' | 'top-end'
  /** Logo Größe */
  logoSize?: 'sm' | 'md' | 'lg' | 'xl'
  /** Zeige zusammengeklapptes Overlay */
  showCollapsedOverlay?: boolean
  /** Sticky Sidebar */
  sticky?: boolean
  /** Sidebar Breite (wenn nicht collapsed) */
  width?: string
  /** Zusammengeklappte Breite */
  collapsedWidth?: string
}

const props = withDefaults(defineProps<Props>(), {
  navigationItems: () => DEFAULT_NAVIGATION_ITEMS,
  currentRoute: '/',
  user: undefined,
  collapsed: false,
  toggleable: true,
  showToggleButton: true,
  showDivider: true,
  showFooter: true,
  showThemeToggle: true,
  showUserMenu: true,
  additionalNavigationItems: () => [],
  navigationItemSize: 'md',
  navigationItemVariant: 'ghost',
  navigationItemPadding: 'md',
  themeToggleSize: 'md',
  userMenuAvatarSize: 'md',
  userMenuPlacement: 'top-end',
  logoSize: 'md',
  showCollapsedOverlay: true,
  sticky: true,
  width: '16rem',
  collapsedWidth: '4rem',
  mobileBreakpoint: 768,
})

const emit = defineEmits<{
  'toggle': [collapsed: boolean]
  'item-click': [item: NavigationItemType, event: MouseEvent]
  'child-click': [child: NavigationItemType, event: MouseEvent]
  'logo-click': [event: MouseEvent]
  'theme-change': [theme: string]
  'user-menu-option-click': [option: any]
  'user-menu-avatar-click': [event: MouseEvent]
}>()

const { t } = useI18n()
const expandedItems = ref<string[]>([])

// Navigation Composable
const navigation = useLayoutNavigation(props.navigationItems, {
  mobileBreakpoint: props.mobileBreakpoint,
  initialSidebarCollapsed: props.collapsed,
  initialRoute: props.currentRoute,
})

// Gefilterte Navigationselemente
const filteredNavigationItems = computed(() => {
  // In einer echten Implementierung würden wir Auth-Status verwenden
  // Für jetzt zeigen wir alle Items
  return props.navigationItems
})

// Sidebar Klassen
const sidebarClasses = computed(() => {
  const classes = [
    'flex flex-col h-full transition-all duration-300 ease-in-out',
    props.sticky ? 'sticky top-0' : '',
  ]
  
  if (props.collapsed) {
    classes.push('sidebar-collapsed')
  } else {
    classes.push('sidebar-expanded')
  }
  
  return classes.join(' ')
})

// Header Klassen
const headerClasses = computed(() => {
  return 'flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700'
})

// Navigation Klassen
const navigationClasses = computed(() => {
  return 'flex-1 overflow-y-auto py-4'
})

// Footer Klassen
const footerClasses = computed(() => {
  return 'p-4 border-t border-gray-200 dark:border-gray-700 space-y-4'
})

// Toggle Button Klassen (zusätzliche Klassen für das Button Atom)
const toggleButtonClasses = computed(() => {
  const base = 'sidebar-toggle'
  
  return props.collapsed
    ? `${base} rotate-180`
    : base
})

// Labels
const sidebarAriaLabel = computed(() => {
  return t('sidebar.mainNavigation')
})

const toggleAriaLabel = computed(() => {
  return props.collapsed
    ? t('sidebar.expandSidebar')
    : t('sidebar.collapseSidebar')
})

const toggleTitle = computed(() => {
  return props.collapsed
    ? t('sidebar.expandSidebar')
    : t('sidebar.collapseSidebar')
})

// Methods
function toggleSidebar() {
  const newCollapsed = !props.collapsed
  emit('toggle', newCollapsed)
  
  if (newCollapsed) {
    // Alle expandierten Items schließen wenn Sidebar collapsed
    expandedItems.value = []
  }
}

function isItemActive(item: NavigationItemType): boolean {
  return navigation.isRouteActive(item.to)
}

function handleItemClick(item: NavigationItemType, event: MouseEvent) {
  emit('item-click', item, event)
  
  // Wenn Item Children hat und Sidebar collapsed ist, expandieren
  if (item.children?.length && props.collapsed) {
    toggleSidebar()
  }
}

function handleChildClick(child: NavigationItemType, event: MouseEvent) {
  emit('child-click', child, event)
}

function toggleItemChildren(itemId: string) {
  const index = expandedItems.value.indexOf(itemId)
  if (index > -1) {
    expandedItems.value.splice(index, 1)
  } else {
    expandedItems.value.push(itemId)
  }
}

// Watch für Route-Änderungen
watch(
  () => props.currentRoute,
  (newRoute) => {
    navigation.setActiveRoute(newRoute)
  }
)

// Watch für Navigation Items Änderungen
watch(
  () => props.navigationItems,
  (newItems) => {
    navigation.setNavigationItems(newItems)
  }
)

// Inline Styles für Width
const sidebarStyle = computed(() => {
  return {
    width: props.collapsed ? props.collapsedWidth : props.width,
    minWidth: props.collapsed ? props.collapsedWidth : props.width,
  }
})
</script>

<style scoped>
.app-sidebar {
  background-color: var(--color-white);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  z-index: 40;
}

.dark .app-sidebar {
  background-color: var(--color-gray-800);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.3), 0 1px 2px 0 rgba(0, 0, 0, 0.2);
}

.sidebar-header {
  min-height: 4rem;
}

.sidebar-toggle {
  transition: all 0.3s ease;
}

.sidebar-toggle:hover {
  transform: scale(1.1);
}

.toggle-icon {
  width: 1.25rem;
  height: 1.25rem;
  transition: transform 0.3s ease;
}

.navigation-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.navigation-list-item {
  margin: 0;
  padding: 0;
}

.sidebar-divider {
  height: 1px;
  background-color: var(--color-gray-200);
  margin: 1rem 0;
}

.dark .sidebar-divider {
  background-color: var(--color-gray-700);
}

.sidebar-footer {
  min-height: 4rem;
}

.sidebar-collapsed-overlay {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 3rem;
  background-color: rgba(0, 0, 0, 0.1);
  z-index: 30;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.sidebar-collapsed-overlay:hover {
  background-color: rgba(0, 0, 0, 0.2);
}

.dark .sidebar-collapsed-overlay {
  background-color: rgba(255, 255, 255, 0.1);
}

.dark .sidebar-collapsed-overlay:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.overlay-content {
  background-color: var(--color-white);
  border-radius: 0.375rem;
  padding: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.dark .overlay-content {
  background-color: var(--color-gray-800);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.3), 0 1px 2px 0 rgba(0, 0, 0, 0.2);
}

.overlay-icon {
  width: 1rem;
  height: 1rem;
  color: var(--color-gray-600);
}

.dark .overlay-icon {
  color: var(--color-gray-400);
}

/* Responsive Anpassungen */
@media (max-width: 768px) {
  .app-sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 50;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .app-sidebar.sidebar-expanded {
    transform: translateX(0);
  }

  .sidebar-collapsed-overlay {
    display: none;
  }
}
</style>