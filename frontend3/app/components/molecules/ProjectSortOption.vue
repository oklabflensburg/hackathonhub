<template>
  <div class="project-sort-option" :class="sortOptionClasses">
    <!-- Sort Label -->
    <label
      v-if="showLabel"
      :for="sortId"
      class="sort-label block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
    >
      {{ label }}
      <span
        v-if="required"
        class="text-red-500 dark:text-red-400 ml-1"
        aria-hidden="true"
      >
        *
      </span>
    </label>
    
    <!-- Sort Container -->
    <div class="sort-container flex flex-wrap gap-2">
      <!-- Sort Option Buttons -->
      <button
        v-for="option in sortOptions"
        :key="option.value"
        type="button"
        class="sort-button inline-flex items-center px-3 py-2 border rounded-lg text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1"
        :class="getButtonClasses(option)"
        :disabled="disabled || option.disabled"
        :aria-label="`Sort by ${option.label}`"
        :aria-pressed="isSelected(option.value)"
        @click="handleSortClick(option.value)"
      >
        <!-- Option Icon -->
        <svg
          v-if="option.icon"
          class="h-4 w-4 mr-2"
          :class="getIconClasses(option)"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            v-if="option.icon === 'trending-up'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
          />
          <path
            v-else-if="option.icon === 'trending-down'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"
          />
          <path
            v-else-if="option.icon === 'calendar'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
          <path
            v-else-if="option.icon === 'star'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
          />
          <path
            v-else-if="option.icon === 'eye'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
          <path
            v-else-if="option.icon === 'chat'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
          />
          <path
            v-else-if="option.icon === 'bookmark'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
          />
          <path
            v-else-if="option.icon === 'clock'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
          />
          <path
            v-else-if="option.icon === 'users'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0c-.966 0-1.75.79-1.75 1.764s.784 1.764 1.75 1.764 1.75-.79 1.75-1.764-.783-1.764-1.75-1.764z"
          />
          <path
            v-else-if="option.icon === 'fire'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"
          />
          <path
            v-else-if="option.icon === 'new'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 6v6m0 0v6m0-6h6m-6 0H6"
          />
        </svg>
        
        <!-- Option Label -->
        <span class="sort-button-label">
          {{ option.label }}
        </span>
        
        <!-- Sort Direction Indicator -->
        <svg
          v-if="showDirectionIndicator && isSelected(option.value) && sortDirection"
          class="h-4 w-4 ml-2"
          :class="directionIndicatorClasses"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            v-if="sortDirection === 'asc'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 15l7-7 7 7"
          />
          <path
            v-else-if="sortDirection === 'desc'"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
        
        <!-- Option Count -->
        <span
          v-if="option.count !== undefined"
          class="sort-count ml-2 px-1.5 py-0.5 text-xs rounded-full"
          :class="getCountClasses(option)"
        >
          {{ option.count }}
        </span>
      </button>
    </div>
    
    <!-- Sort Direction Toggle -->
    <div
      v-if="showDirectionToggle && modelValue"
      class="direction-toggle mt-3"
    >
      <div class="toggle-label text-xs text-gray-500 dark:text-gray-400 mb-1">
        Sort direction:
      </div>
      <div class="toggle-buttons flex gap-2">
        <button
          type="button"
          class="direction-button inline-flex items-center px-3 py-1.5 border rounded-lg text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1"
          :class="getDirectionButtonClasses('asc')"
          :disabled="disabled"
          :aria-label="'Sort ascending'"
          :aria-pressed="sortDirection === 'asc'"
          @click="handleDirectionClick('asc')"
        >
          <svg
            class="h-3 w-3 mr-1"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 15l7-7 7 7"
            />
          </svg>
          Ascending
        </button>
        <button
          type="button"
          class="direction-button inline-flex items-center px-3 py-1.5 border rounded-lg text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1"
          :class="getDirectionButtonClasses('desc')"
          :disabled="disabled"
          :aria-label="'Sort descending'"
          :aria-pressed="sortDirection === 'desc'"
          @click="handleDirectionClick('desc')"
        >
          <svg
            class="h-3 w-3 mr-1"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 9l-7 7-7-7"
            />
          </svg>
          Descending
        </button>
      </div>
    </div>
    
    <!-- Selected Option Display -->
    <div
      v-if="showSelectedDisplay && modelValue"
      class="selected-display mt-3"
    >
      <div class="selected-label text-xs text-gray-500 dark:text-gray-400 mb-1">
        Currently sorted by:
      </div>
      <div class="selected-value inline-flex items-center px-3 py-1.5 border rounded-lg text-sm">
        <span class="selected-text font-medium">
          {{ selectedOption?.label }}
        </span>
        <span
          v-if="sortDirection"
          class="selected-direction ml-2 text-xs text-gray-500 dark:text-gray-400"
        >
          ({{ sortDirection === 'asc' ? 'Ascending' : 'Descending' }})
        </span>
        <button
          v-if="showClearButton"
          type="button"
          class="clear-button ml-2 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 focus:outline-none"
          :aria-label="'Clear sort'"
          @click="handleClear"
        >
          <svg
            class="h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
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
    </div>
    
    <!-- Helper Text -->
    <p
      v-if="helperText"
      class="helper-text mt-2 text-xs text-gray-500 dark:text-gray-400"
    >
      {{ helperText }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ProjectSortOption } from '../../types/project-types'

interface SortOption {
  value: ProjectSortOption
  label: string
  icon?: string
  disabled?: boolean
  count?: number
}

interface Props {
  /** v-model Wert */
  modelValue?: ProjectSortOption | null
  /** Sort-Richtung */
  sortDirection?: 'asc' | 'desc'
  /** Sort-Optionen */
  sortOptions?: SortOption[]
  /** Label */
  label?: string
  /** Deaktiviert */
  disabled?: boolean
  /** Erforderlich */
  required?: boolean
  /** Label anzeigen */
  showLabel?: boolean
  /** Direction Indicator anzeigen */
  showDirectionIndicator?: boolean
  /** Direction Toggle anzeigen */
  showDirectionToggle?: boolean
  /** Selected Display anzeigen */
  showSelectedDisplay?: boolean
  /** Clear Button anzeigen */
  showClearButton?: boolean
  /** Helper Text */
  helperText?: string
  /** Größe */
  size?: 'sm' | 'md' | 'lg'
  /** Variante */
  variant?: 'default' | 'outline' | 'filled'
}

const props = withDefaults(defineProps<Props>(), {
  label: 'Sort by',
  sortOptions: () => [
    { value: ProjectSortOption.NEWEST, label: 'Newest', icon: 'new' },
    { value: ProjectSortOption.OLDEST, label: 'Oldest', icon: 'clock' },
    { value: ProjectSortOption.MOST_VIEWED, label: 'Most Views', icon: 'eye' },
    { value: ProjectSortOption.MOST_VOTED, label: 'Most Votes', icon: 'star' },
    { value: ProjectSortOption.MOST_COMMENTED, label: 'Most Comments', icon: 'chat' },
    { value: ProjectSortOption.TRENDING, label: 'Trending', icon: 'trending-up' },
    { value: ProjectSortOption.DEADLINE, label: 'Deadline', icon: 'clock' },
    { value: ProjectSortOption.ALPHABETICAL, label: 'Alphabetical', icon: 'sort-alpha' },
  ],
  showLabel: true,
  showDirectionIndicator: true,
  showDirectionToggle: true,
  showSelectedDisplay: true,
  showClearButton: true,
  size: 'md',
  variant: 'default',
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: ProjectSortOption | null): void
  (e: 'update:sortDirection', value: 'asc' | 'desc'): void
  (e: 'change', value: { sortBy: ProjectSortOption | null, direction: 'asc' | 'desc' }): void
  (e: 'clear'): void
}>()

// Computed Properties
const sortId = computed(() => {
  return `sort-${Math.random().toString(36).substr(2, 9)}`
})

const sortOptionClasses = computed(() => {
  return props.disabled ? 'opacity-60 cursor-not-allowed' : ''
})

const directionIndicatorClasses = computed(() => {
  return 'text-blue-600 dark:text-blue-400'
})

const selectedOption = computed(() => {
  if (!props.modelValue) return null
  return props.sortOptions.find(option => option.value === props.modelValue)
})

// Helper Functions
const isSelected = (value: ProjectSortOption) => {
  return props.modelValue === value
}

const getButtonClasses = (option: SortOption) => {
  const classes: string[] = []
  
  // Size
  switch (props.size) {
    case 'sm':
      classes.push('px-2 py-1 text-xs')
      break
    case 'lg':
      classes.push('px-4 py-2.5 text-base')
      break
    case 'md':
    default:
      classes.push('px-3 py-2 text-sm')
  }
  
  // Variant and State
  if (isSelected(option.value)) {
    // Selected state
    switch (props.variant) {
      case 'outline':
        classes.push('border-blue-500 dark:border-blue-400 text-blue-700 dark:text-blue-300 bg-blue-50 dark:bg-blue-900/20 focus:ring-blue-500 dark:focus:ring-blue-400')
        break
      case 'filled':
        classes.push('border-transparent bg-blue-600 dark:bg-blue-500 text-white focus:ring-blue-500 dark:focus:ring-blue-400')
        break
      case 'default':
      default:
        classes.push('border-blue-500 dark:border-blue-400 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 focus:ring-blue-500 dark:focus:ring-blue-400')
    }
  } else {
    // Unselected state
    switch (props.variant) {
      case 'outline':
        classes.push('border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:border-gray-400 dark:hover:border-gray-500 hover:text-gray-900 dark:hover:text-gray-100 focus:ring-gray-500 dark:focus:ring-gray-400')
        break
      case 'filled':
        classes.push('border-transparent bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 focus:ring-gray-500 dark:focus:ring-gray-400')
        break
      case 'default':
      default:
        classes.push('border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 hover:border-gray-400 dark:hover:border-gray-500 hover:text-gray-900 dark:hover:text-gray-100 focus:ring-gray-500 dark:focus:ring-gray-400')
    }
  }
  
  // Disabled state
  if (props.disabled || option.disabled) {
    classes.push('opacity-50 cursor-not-allowed')
  }
  
  return classes.join(' ')
}

const getIconClasses = (option: SortOption) => {
  if (isSelected(option.value)) {
    return 'text-blue-600 dark:text-blue-400'
  }
  return 'text-gray-400 dark:text-gray-500'
}

const getCountClasses = (option: SortOption) => {
  if (isSelected(option.value)) {
    return 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300'
  }
  return 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'
}

const getDirectionButtonClasses = (direction: 'asc' | 'desc') => {
  const classes: string[] = []
  
  if (props.sortDirection === direction) {
    classes.push('border-blue-500 dark:border-blue-400 text-blue-700 dark:text-blue-300 bg-blue-50 dark:bg-blue-900/20')
  } else {
    classes.push('border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:border-gray-400 dark:hover:border-gray-500')
  }
  
  if (props.disabled) {
    classes.push('opacity-50 cursor-not-allowed')
  }
  
  return classes.join(' ')
}

// Event Handlers
const handleSortClick = (value: ProjectSortOption) => {
  if (props.disabled) return
  
  // Toggle if already selected
  const newValue = props.modelValue === value ? null : value
  emit('update:modelValue', newValue)
  emit('change', { sortBy: newValue, direction: props.sortDirection || 'desc' })
}

const handleDirectionClick = (direction: 'asc' | 'desc') => {
  if (props.disabled || !props.modelValue) return
  
  emit('update:sortDirection', direction)
  emit('change', { sortBy: props.modelValue, direction })
}

const handleClear = () => {
  if (props.disabled) return
  
  emit('update:modelValue', null)
  emit('update:sortDirection', 'desc')
  emit('change', { sortBy: null, direction: 'desc' })
  emit('clear')
}
</script>