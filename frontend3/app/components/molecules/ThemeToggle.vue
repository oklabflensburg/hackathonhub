<template>
  <div class="theme-toggle">
    <!-- Simple Toggle Button -->
    <button
      v-if="variant === 'simple'"
      type="button"
      class="theme-toggle-simple"
      :class="simpleButtonClasses"
      :title="toggleTitle"
      :aria-label="toggleAriaLabel"
      @click="toggleTheme"
    >
      <span class="sr-only">{{ toggleAriaLabel }}</span>
      
      <!-- Light Icon -->
      <svg
        v-if="currentTheme === 'light'"
        class="theme-icon"
        :class="iconClasses"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
      
      <!-- Dark Icon -->
      <svg
        v-else
        class="theme-icon"
        :class="iconClasses"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
      </svg>
    </button>

    <!-- Select Dropdown -->
    <div v-else class="theme-toggle-select relative">
      <button
        type="button"
        class="theme-toggle-select-button"
        :class="selectButtonClasses"
        :aria-expanded="dropdownOpen"
        :aria-label="selectAriaLabel"
        @click="toggleDropdown"
        @keydown.escape="closeDropdown"
      >
        <!-- Current Theme Icon -->
        <span class="flex items-center">
          <svg
            class="theme-icon mr-2"
            :class="iconClasses"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              v-if="currentTheme === 'light'"
              stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
            />
            <path
              v-else-if="currentTheme === 'dark'"
              stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
            />
            <path
              v-else
              stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9.663 17h4.673M12 3v1m8 8h-1M4 12H3m15.364-6.364l-.707.707M6.343 6.343l-.707.707m12.728 12.728l-.707-.707M6.343 17.657l-.707-.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
            />
          </svg>
          
          <span v-if="showLabel" class="truncate">
            {{ currentThemeLabel }}
          </span>
          
          <!-- Chevron -->
          <svg
            class="ml-2 w-4 h-4 transition-transform duration-200"
            :class="{ 'rotate-180': dropdownOpen }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </span>
      </button>

      <!-- Dropdown Menu -->
      <div
        v-if="dropdownOpen"
        v-click-outside="closeDropdown"
        class="theme-toggle-dropdown absolute z-10 mt-2 w-48 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 dark:ring-gray-700"
        :class="dropdownPlacementClasses"
        role="menu"
        aria-orientation="vertical"
      >
        <div class="py-1" role="none">
          <!-- Light Theme Option -->
          <button
            type="button"
            class="theme-option"
            :class="optionClasses('light')"
            role="menuitem"
            @click="setTheme('light')"
          >
            <svg class="mr-3 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <span class="flex-1 text-left">{{ t('theme.light') }}</span>
            <svg v-if="themeState.current === 'light'" class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
          </button>

          <!-- Dark Theme Option -->
          <button
            type="button"
            class="theme-option"
            :class="optionClasses('dark')"
            role="menuitem"
            @click="setTheme('dark')"
          >
            <svg class="mr-3 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
            <span class="flex-1 text-left">{{ t('theme.dark') }}</span>
            <svg v-if="themeState.current === 'dark'" class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
          </button>

          <!-- System Theme Option -->
          <button
            type="button"
            class="theme-option"
            :class="optionClasses('system')"
            role="menuitem"
            @click="setTheme('system')"
          >
            <svg class="mr-3 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m8 8h-1M4 12H3m15.364-6.364l-.707.707M6.343 6.343l-.707.707m12.728 12.728l-.707-.707M6.343 17.657l-.707-.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <span class="flex-1 text-left">{{ t('theme.system') }}</span>
            <svg v-if="themeState.current === 'system'" class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ThemeToggleProps } from '~/types/layout-types'
import { useTheme, type Theme } from '~/composables/useTheme'

interface Props extends ThemeToggleProps {
  /** Variante (simple oder select) */
  variant?: 'simple' | 'select'
  /** Dropdown Platzierung */
  placement?: 'bottom-start' | 'bottom-end' | 'top-start' | 'top-end'
}

const props = withDefaults(defineProps<Props>(), {
  initialTheme: undefined,
  showLabel: true,
  size: 'md',
  variant: 'simple',
  placement: 'bottom-end',
})

const emit = defineEmits<{
  'theme-change': [theme: Theme]
}>()

// Composables
const { t } = useI18n()
const theme = useTheme()
const dropdownOpen = ref(false)

// Theme State
const themeState = theme.state
const currentTheme = theme.currentTheme

// Initial Theme setzen falls angegeben
if (props.initialTheme) {
  theme.setTheme(props.initialTheme)
}

// Labels
const toggleTitle = computed(() => {
  return currentTheme.value === 'light'
    ? t('theme.switchToDark')
    : t('theme.switchToLight')
})

const toggleAriaLabel = computed(() => {
  return currentTheme.value === 'light'
    ? t('theme.switchToDark')
    : t('theme.switchToLight')
})

const selectAriaLabel = computed(() => {
  return t('theme.selectTheme')
})

const currentThemeLabel = computed(() => {
  switch (themeState.value.current) {
    case 'light':
      return t('theme.light')
    case 'dark':
      return t('theme.dark')
    case 'system':
      return t('theme.system')
    default:
      return t('theme.system')
  }
})

// Klassen
const simpleButtonClasses = computed(() => {
  const base = 'inline-flex items-center justify-center rounded-full focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 transition-colors'
  
  const sizeMap = {
    sm: 'p-1.5',
    md: 'p-2',
    lg: 'p-3',
  }
  
  const colorClasses = currentTheme.value === 'light'
    ? 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
    : 'bg-gray-800 dark:bg-gray-200 text-gray-100 dark:text-gray-800 hover:bg-gray-700 dark:hover:bg-gray-300'
  
  return `${base} ${sizeMap[props.size] || sizeMap.md} ${colorClasses}`
})

const selectButtonClasses = computed(() => {
  const base = 'inline-flex items-center justify-between w-full rounded-md border border-gray-300 dark:border-gray-600 shadow-sm px-4 py-2 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 transition-colors'
  
  const sizeMap = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
  }
  
  return `${base} ${sizeMap[props.size] || sizeMap.md}`
})

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

const dropdownPlacementClasses = computed(() => {
  switch (props.placement) {
    case 'bottom-start':
      return 'left-0 origin-top-left'
    case 'bottom-end':
      return 'right-0 origin-top-right'
    case 'top-start':
      return 'left-0 bottom-full mb-2 origin-bottom-left'
    case 'top-end':
      return 'right-0 bottom-full mb-2 origin-bottom-right'
    default:
      return 'right-0 origin-top-right'
  }
})

// Option Klassen
function optionClasses(themeOption: Theme) {
  const base = 'flex items-center w-full px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700 transition-colors'
  
  const active = themeState.value.current === themeOption
    ? 'bg-gray-50 dark:bg-gray-800'
    : ''
  
  return `${base} ${active}`
}

// Methods
function toggleTheme() {
  theme.toggleTheme()
  emit('theme-change', currentTheme.value === 'light' ? 'dark' : 'light')
}

function setTheme(newTheme: Theme) {
  theme.setTheme(newTheme)
  emit('theme-change', newTheme)
  closeDropdown()
}

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value
}

function closeDropdown() {
  dropdownOpen.value = false
}
</script>

<style scoped>
.theme-toggle-simple {
  transition: all 0.2s ease;
}

.theme-toggle-simple:hover {
  transform: scale(1.05);
}

.theme-toggle-simple:active {
  transform: scale(0.95);
}

.theme-toggle-dropdown {
  animation: fadeInScale 0.15s ease-out;
}

.theme-option {
  transition: all 0.15s ease;
}

.theme-option:hover {
  transform: translateX(2px);
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>