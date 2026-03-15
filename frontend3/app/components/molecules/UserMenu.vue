<template>
  <div class="user-menu relative">
    <!-- Trigger Button -->
    <button
      type="button"
      class="user-menu-trigger"
      :class="triggerClasses"
      :aria-expanded="dropdownOpen"
      :aria-label="triggerAriaLabel"
      @click="toggleDropdown"
      @keydown.escape="closeDropdown"
    >
      <!-- Avatar -->
      <div class="flex items-center">
        <!-- Avatar Image -->
        <div
          v-if="resolvedAvatarUrl"
          class="flex-shrink-0 rounded-full overflow-hidden"
          :class="avatarSizeClasses"
        >
          <img
            :src="resolvedAvatarUrl"
            :alt="avatarAlt"
            class="w-full h-full object-cover"
            @error="handleImageError"
          />
        </div>

        <!-- Avatar Fallback -->
        <div
          v-else
          class="flex-shrink-0 rounded-full flex items-center justify-center"
          :class="[avatarSizeClasses, avatarFallbackClasses]"
        >
          <span :class="avatarInitialClasses">
            {{ userInitials }}
          </span>
        </div>

        <!-- User Info (wenn erweitert) -->
        <div v-if="showUserInfo" class="ml-3 text-left">
          <p class="text-sm font-medium text-gray-700 dark:text-gray-300 truncate">
            {{ user?.username || 'User' }}
          </p>
          <p v-if="showEmail && user?.email" class="text-xs text-gray-500 dark:text-gray-400 truncate">
            {{ user.email }}
          </p>
        </div>

        <!-- Chevron -->
        <svg
          v-if="showChevron"
          class="ml-2 w-4 h-4 transition-transform duration-200"
          :class="{ 'rotate-180': dropdownOpen }"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </button>

    <!-- Dropdown Menu -->
    <div
      v-if="dropdownOpen"
      v-click-outside="closeDropdown"
      class="user-menu-dropdown absolute z-50 mt-2 w-56 rounded-xl border border-gray-200 bg-white py-2 shadow-elevated dark:border-gray-700 dark:bg-gray-800 divide-y divide-gray-100 dark:divide-gray-700 glass-effect"
      :class="dropdownPlacementClasses"
      role="menu"
      aria-orientation="vertical"
    >
      <!-- User Info Section -->
      <div v-if="showUserInfoInDropdown" class="px-3 sm:px-4 py-2 sm:py-3" role="none">
        <p class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
          {{ user?.username || 'User' }}
        </p>
        <p v-if="showEmail && user?.email" class="text-xs text-gray-500 dark:text-gray-400 truncate mt-1">
          {{ user.email }}
        </p>
        <p v-if="user?.role" class="text-xs text-gray-500 dark:text-gray-400 mt-1">
          <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200">
            {{ user.role }}
          </span>
        </p>
      </div>

      <!-- Menu Options -->
      <div class="py-1" role="none">
        <template v-for="option in effectiveMenuOptions" :key="option.id">
          <!-- Separator -->
          <div
            v-if="option.separatorBefore"
            class="border-t border-gray-100 dark:border-gray-700 my-1"
            role="separator"
          />

          <!-- Menu Option -->
          <button
            type="button"
            class="user-menu-option"
            :class="optionClasses(option)"
            role="menuitem"
            @click="handleOptionClick(option)"
          >
            <span class="flex items-center">
              <!-- Icon -->
              <span class="mr-3" :class="optionIconClasses(option)" aria-hidden="true">
                <slot :name="`icon-${option.id}`">
                  <svg
                    v-if="!option.icon.includes('.')"
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <!-- Placeholder Icon - in einer echten Implementierung würden wir Icon-Komponenten verwenden -->
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <span v-else :class="option.icon" />
                </slot>
              </span>

              <!-- Label -->
              <span class="flex-1 text-left">
                {{ option.label }}
              </span>
            </span>
          </button>
        </template>
      </div>

      <!-- Theme Toggle in Dropdown (optional) -->
      <div v-if="showThemeToggleInDropdown" class="py-1 px-4" role="none">
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-700 dark:text-gray-300">
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
</template>

<script setup lang="ts">
import type { UserMenuProps, UserMenuOption } from '~/types/layout-types'
import { DEFAULT_USER_MENU_OPTIONS } from '~/types/layout-types'
import ThemeToggle from './ThemeToggle.vue'

interface Props extends UserMenuProps {
  /** Zeige User Info neben Avatar */
  showUserInfo?: boolean
  /** Zeige User Info im Dropdown */
  showUserInfoInDropdown?: boolean
  /** Zeige Chevron */
  showChevron?: boolean
  /** Avatar Größe */
  avatarSize?: 'sm' | 'md' | 'lg' | 'xl'
  /** Trigger Variante */
  variant?: 'avatar-only' | 'with-info' | 'minimal'
  /** Zeige Theme Toggle im Dropdown */
  showThemeToggleInDropdown?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  user: undefined,
  avatarUrl: undefined,
  menuOptions: undefined,
  showEmail: true,
  placement: 'bottom-end',
  showUserInfo: false,
  showUserInfoInDropdown: true,
  showChevron: true,
  avatarSize: 'md',
  variant: 'avatar-only',
  showThemeToggleInDropdown: false,
})

const emit = defineEmits<{
  'option-click': [option: UserMenuOption]
  'avatar-click': [event: MouseEvent]
  'theme-change': [theme: string]
}>()

const { t } = useI18n()
const dropdownOpen = ref(false)
const resolvedAvatarUrl = computed(() => props.avatarUrl || props.user?.avatarUrl || props.user?.avatar_url)

// Effektive Menu-Optionen (Standard oder benutzerdefiniert)
const effectiveMenuOptions = computed(() => {
  return props.menuOptions || DEFAULT_USER_MENU_OPTIONS
})

// User Initialen
const userInitials = computed(() => {
  if (!props.user?.username) return 'U'
  
  const name = props.user.username
  return name
    .split(' ')
    .map((part: string) => part.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2)
})

// Avatar Alt Text
const avatarAlt = computed(() => {
  return props.user?.username
    ? `${props.user.username}'s avatar`
    : 'User avatar'
})

// Trigger Aria Label
const triggerAriaLabel = computed(() => {
  return props.user?.username
    ? t('userMenu.openMenuFor', { username: props.user.username })
    : t('userMenu.openMenu')
})

// Klassen
const triggerClasses = computed(() => {
  const base = 'flex items-center focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 transition-colors duration-200'
  
  const variantClasses = {
    'avatar-only': 'space-x-1 sm:space-x-2 p-1.5 sm:p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800',
    'with-info': 'space-x-1 sm:space-x-2 p-1.5 sm:p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800',
    'minimal': 'p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800',
  }
  
  return `${base} ${variantClasses[props.variant] || variantClasses['avatar-only']}`
})

const avatarSizeClasses = computed(() => {
  switch (props.avatarSize) {
    case 'sm':
      return 'w-8 h-8'
    case 'md':
      return 'w-10 h-10'
    case 'lg':
      return 'w-12 h-12'
    case 'xl':
      return 'w-16 h-16'
    default:
      return 'w-10 h-10'
  }
})

const avatarFallbackClasses = computed(() => {
  return 'bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200'
})

const avatarInitialClasses = computed(() => {
  switch (props.avatarSize) {
    case 'sm':
      return 'text-xs font-semibold'
    case 'md':
      return 'text-sm font-semibold'
    case 'lg':
      return 'text-base font-semibold'
    case 'xl':
      return 'text-lg font-semibold'
    default:
      return 'text-sm font-semibold'
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
function optionClasses(option: UserMenuOption) {
  const base = 'flex items-center w-full px-3 sm:px-4 py-2 sm:py-3 text-sm transition-colors'
  
  if (option.dangerous) {
    return `${base} text-red-700 dark:text-red-300 hover:bg-red-50 dark:hover:bg-red-900/20 focus:bg-red-50 dark:focus:bg-red-900/20`
  }
  
  return `${base} text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:bg-gray-100 dark:focus:bg-gray-700`
}

function optionIconClasses(option: UserMenuOption) {
  if (option.dangerous) {
    return 'text-red-500 dark:text-red-400'
  }
  return 'text-gray-400 dark:text-gray-500'
}

// Methods
function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value
  if (dropdownOpen.value) {
    emit('avatar-click', new MouseEvent('click'))
  }
}

function closeDropdown() {
  dropdownOpen.value = false
}

function handleOptionClick(option: UserMenuOption) {
  option.action()
  emit('option-click', option)
  closeDropdown()
}

function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  // Fallback wird durch das v-else im Template angezeigt
}

function handleThemeChange(theme: string) {
  emit('theme-change', theme)
}
</script>

<style scoped>
.user-menu-trigger {
  transition: background-color 0.2s ease, color 0.2s ease;
}

.user-menu-dropdown {
  animation: fadeInScale 0.15s ease-out;
}

.user-menu-option {
  transition: background-color 0.15s ease, color 0.15s ease;
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
