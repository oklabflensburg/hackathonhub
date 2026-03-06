<template>
  <!-- Mobile Navigation Overlay -->
  <div
    v-if="visible"
    class="mobile-navigation-overlay fixed inset-0 z-50 bg-black/70 transition-opacity duration-300"
    :class="visible ? 'opacity-100' : 'opacity-0 pointer-events-none'"
    @click="closeNavigation"
  >
    <!-- Navigation Panel -->
    <div
      class="mobile-navigation-panel fixed h-full flex flex-col transition-transform duration-300 ease-in-out bg-white dark:bg-gray-900"
      :class="panelClasses"
      @click.stop
    >
      <!-- Panel Header -->
      <div class="panel-header flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <!-- Logo -->
        <div class="panel-logo">
          <Logo
            size="md"
            :as-link="true"
            to="/"
            text-logo
            @click="handleLogoClick"
          />
        </div>

        <!-- Close Button -->
        <button
          type="button"
          class="panel-close p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          :aria-label="t('mobileNav.closeMenu')"
          @click="closeNavigation"
        >
          <svg
            class="close-icon w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- Navigation Content -->
      <div class="panel-content flex-1 overflow-y-auto p-4">
        <!-- Navigation Items -->
        <nav class="navigation-section mb-6" aria-label="Mobile navigation">
          <ul class="navigation-list" role="list">
            <li
              v-for="item in filteredNavigationItems"
              :key="item.id"
              class="navigation-item mb-2"
            >
              <NavigationItemComponent
                :item="item"
                :active="isItemActive(item)"
                :size="navigationItemSize"
                :full-width="true"
                :variant="navigationItemVariant"
                :padding="navigationItemPadding"
                @click="handleItemClick(item, $event)"
              />
            </li>
          </ul>
        </nav>

        <!-- Theme Toggle -->
        <div v-if="showThemeToggle" class="theme-section p-4 border-t border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <span class="theme-label text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ t('theme.theme') }}
            </span>
            <ThemeToggle
              size="sm"
              variant="simple"
              :show-label="false"
              @theme-change="handleThemeChange"
            />
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Mobile Navigation Trigger (Bottom Bar) -->
  <div
    v-if="showTrigger && position === 'bottom'"
    class="mobile-navigation-trigger fixed bottom-0 left-0 right-0 z-40 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 shadow-lg"
  >
    <div class="trigger-content">
      <!-- Navigation Items in Bottom Bar -->
      <nav class="trigger-navigation" aria-label="Bottom navigation">
        <ul class="trigger-list flex justify-around">
          <li
            v-for="item in triggerItems"
            :key="item.id"
            class="trigger-item"
          >
            <button
              type="button"
              class="trigger-button flex flex-col items-center justify-center p-3 w-full rounded-lg transition-colors"
              :class="getTriggerButtonClasses(item)"
              :aria-label="item.label"
              @click="(e) => handleTriggerClick(item, e)"
            >
              <!-- Icon -->
              <span class="trigger-icon" aria-hidden="true">
                <svg
                  class="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </span>

              <!-- Label (wenn aktiv) -->
              <span
                v-if="isItemActive(item)"
                class="trigger-label text-xs mt-1 font-medium"
              >
                {{ item.label }}
              </span>
            </button>
          </li>

          <!-- Menu Trigger -->
          <li class="trigger-item">
            <button
              type="button"
              class="trigger-button flex flex-col items-center justify-center p-3 w-full rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400 transition-colors"
              :aria-label="visible ? t('mobileNav.closeMenu') : t('mobileNav.openMenu')"
              :aria-expanded="visible"
              @click="toggleNavigation"
            >
              <span class="trigger-icon" aria-hidden="true">
                <svg
                  class="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    v-if="!visible"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                  <path
                    v-else
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </span>
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { MobileNavigationProps, NavigationItem as NavigationItemType } from '~/types/layout-types'
import { DEFAULT_NAVIGATION_ITEMS } from '~/types/layout-types'
import { useLayoutNavigation } from '~/composables/useLayoutNavigation'

import Logo from '~/components/atoms/Logo.vue'
import NavigationItemComponent from '~/components/molecules/NavigationItem.vue'
import ThemeToggle from '~/components/molecules/ThemeToggle.vue'

interface Props extends MobileNavigationProps {
  /** Zeige Trigger (Bottom/Top Bar) */
  showTrigger?: boolean
  /** Trigger Items für Bottom Bar */
  triggerItems?: NavigationItemType[]
  /** Navigation Item Größe */
  navigationItemSize?: 'sm' | 'md' | 'lg'
  /** Navigation Item Variante */
  navigationItemVariant?: 'default' | 'primary' | 'secondary' | 'ghost'
  /** Navigation Item Padding */
  navigationItemPadding?: 'none' | 'sm' | 'md' | 'lg'
  /** Animation */
  animation?: 'slide' | 'fade' | 'scale'
  /** Zeige Theme Toggle */
  showThemeToggle?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  navigationItems: () => DEFAULT_NAVIGATION_ITEMS,
  currentRoute: '/',
  visible: false,
  position: 'bottom',
  showTrigger: true,
  triggerItems: () => [
    { id: 'home', label: 'Home', to: '/', icon: 'home' },
    { id: 'hackathons', label: 'Hackathons', to: '/hackathons', icon: 'trophy' },
    { id: 'projects', label: 'Projects', to: '/projects', icon: 'code' },
    { id: 'notifications', label: 'Notifications', to: '/notifications', icon: 'bell' },
  ],
  navigationItemSize: 'md',
  navigationItemVariant: 'default',
  navigationItemPadding: 'md',
  animation: 'slide',
  showThemeToggle: true,
})

const emit = defineEmits<{
  'toggle': [visible: boolean]
  'close': []
  'open': []
  'item-click': [item: NavigationItemType, event: MouseEvent]
  'trigger-click': [item: NavigationItemType, event: MouseEvent]
  'theme-change': [theme: string]
  'logo-click': [event: MouseEvent]
}>()

const { t } = useI18n()

// Navigation Composable
const navigation = useLayoutNavigation(props.navigationItems, {
  initialRoute: props.currentRoute,
})

// Gefilterte Navigationselemente
const filteredNavigationItems = computed(() => {
  return props.navigationItems
})

// Panel Klassen
const panelClasses = computed(() => {
  const classes: string[] = []
  
  if (props.animation === 'slide') {
    if (props.position === 'bottom') {
      classes.push(props.visible ? 'translate-y-0' : 'translate-y-full')
    } else {
      classes.push(props.visible ? 'translate-x-0' : '-translate-x-full')
    }
  } else if (props.animation === 'scale') {
    classes.push(props.visible ? 'scale-100 opacity-100' : 'scale-95 opacity-0')
  } else {
    classes.push(props.visible ? 'opacity-100' : 'opacity-0')
  }
  
  if (props.position === 'bottom') {
    classes.push('bottom-0 left-0 right-0 max-h-[85vh] rounded-t-2xl')
  } else {
    classes.push('top-0 left-0 right-0 max-w-sm')
  }
  
  return classes.join(' ')
})

// Trigger Button Klassen
const getTriggerButtonClasses = (item: NavigationItemType) => {
  const baseClasses = 'flex flex-col items-center justify-center p-3 w-full rounded-lg transition-colors'
  const isActive = isItemActive(item)
  
  if (isActive) {
    return `${baseClasses} bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400`
  }
  
  return `${baseClasses} hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400`
}

// Methoden
const toggleNavigation = () => {
  const newVisible = !props.visible
  emit('toggle', newVisible)
  
  if (newVisible) {
    emit('open')
  } else {
    emit('close')
  }
}

const closeNavigation = () => {
  if (props.visible) {
    emit('toggle', false)
    emit('close')
  }
}

const handleLogoClick = (event: MouseEvent) => {
  emit('logo-click', event)
  closeNavigation()
}

const handleItemClick = (item: NavigationItemType, event: MouseEvent) => {
  emit('item-click', item, event)
  closeNavigation()
}

const handleTriggerClick = (item: NavigationItemType, event: MouseEvent) => {
  emit('trigger-click', item, event)
}

const handleThemeChange = (theme: string) => {
  emit('theme-change', theme)
}

const isItemActive = (item: NavigationItemType): boolean => {
  return navigation.isRouteActive(item.to)
}
</script>

<style scoped>
.mobile-navigation-overlay {
  backdrop-filter: blur(4px);
}

.mobile-navigation-panel {
  box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.1), 0 -2px 4px -1px rgba(0, 0, 0, 0.06);
}

@media (prefers-color-scheme: dark) {
  .mobile-navigation-panel {
    box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.3), 0 -2px 4px -1px rgba(0, 0, 0, 0.2);
  }
}
</style>
