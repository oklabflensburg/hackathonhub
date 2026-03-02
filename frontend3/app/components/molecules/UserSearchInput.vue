<template>
  <div class="user-search-input relative">
    <!-- Input field -->
    <div class="relative">
      <input
        ref="inputRef"
        v-model="localValue"
        type="text"
        :placeholder="placeholder"
        :disabled="disabled"
        class="w-full input"
        :class="{ 'pr-10': loading }"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
        @keydown.down="handleKeyDown"
        @keydown.up="handleKeyUp"
        @keydown.enter="handleEnter"
        @keydown.escape="handleEscape"
      />
      
      <!-- Loading indicator -->
      <div v-if="loading" class="absolute right-3 top-1/2 transform -translate-y-1/2">
        <svg class="animate-spin h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      </div>
    </div>

    <!-- Suggestions dropdown -->
    <div
      v-if="showDropdown"
      ref="dropdownRef"
      class="absolute z-50 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg max-h-60 overflow-y-auto"
      style="top: 100%;"
    >
      <!-- Loading state -->
      <div v-if="loading" class="px-4 py-3 text-center text-gray-500 dark:text-gray-400 text-sm">
        Searching...
      </div>

      <!-- Empty state -->
      <div v-else-if="suggestions.length === 0 && localValue.length >= minChars" class="px-4 py-3 text-gray-500 dark:text-gray-400 text-sm">
        <slot name="empty-state" :query="localValue">
          No matching users found
        </slot>
      </div>

      <!-- Suggestions list -->
      <div v-else>
        <div
          v-for="(user, index) in visibleSuggestions"
          :key="user.id"
          class="px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer flex items-center"
          :class="{ 'bg-gray-50 dark:bg-gray-700': index === activeIndex }"
          @mousedown="handleSuggestionClick(user)"
          @mouseenter="activeIndex = index"
        >
          <!-- Custom suggestion slot -->
          <slot name="suggestion-item" :user="user" :index="index">
            <!-- Default suggestion item -->
            <div class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center mr-3 overflow-hidden">
              <img
                v-if="user.avatar_url"
                :src="user.avatar_url"
                :alt="user.username"
                class="w-full h-full object-cover"
              />
              <span v-else class="text-xs font-medium text-primary-600 dark:text-primary-400">
                {{ user.username.charAt(0).toUpperCase() }}
              </span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="font-medium text-gray-900 dark:text-white truncate">
                {{ user.username }}
              </div>
              <div v-if="user.name" class="text-sm text-gray-500 dark:text-gray-400 truncate">
                {{ user.name }}
              </div>
              <div v-if="user.is_member" class="text-xs text-gray-400 dark:text-gray-500 mt-1">
                Already a team member
              </div>
            </div>
          </slot>
        </div>

        <!-- Show more indicator -->
        <div v-if="hasMoreSuggestions" class="px-4 py-2 text-center text-sm text-gray-500 dark:text-gray-400 border-t border-gray-100 dark:border-gray-700">
          {{ moreSuggestionsText }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, type PropType } from 'vue'
import type { UserSearchInputProps, UserSearchResult } from '~/types/team-invitations'

const props = withDefaults(defineProps<UserSearchInputProps>(), {
  modelValue: '',
  suggestions: () => [],
  loading: false,
  placeholder: 'Search users...',
  minChars: 2,
  maxSuggestions: 5,
  disabled: false,
  excludeUserIds: () => []
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'select': [user: UserSearchResult]
  'search': [query: string]
  'clear': []
}>()

// Refs
const inputRef = ref<HTMLInputElement | null>(null)
const dropdownRef = ref<HTMLDivElement | null>(null)
const localValue = ref(props.modelValue)
const showDropdown = ref(false)
const activeIndex = ref(-1)
const isMouseOverDropdown = ref(false)

// Computed
const visibleSuggestions = computed(() => {
  // Filter out excluded users
  let filtered = props.suggestions.filter(user => 
    !props.excludeUserIds.includes(user.id)
  )
  
  // Limit to max suggestions
  if (props.maxSuggestions && filtered.length > props.maxSuggestions) {
    filtered = filtered.slice(0, props.maxSuggestions)
  }
  
  return filtered
})

const hasMoreSuggestions = computed(() => {
  const filtered = props.suggestions.filter(user => 
    !props.excludeUserIds.includes(user.id)
  )
  return props.maxSuggestions && filtered.length > props.maxSuggestions
})

const moreSuggestionsText = computed(() => {
  const total = props.suggestions.filter(user => 
    !props.excludeUserIds.includes(user.id)
  ).length
  return `+${total - visibleSuggestions.value.length} more`
})

// Methods
function handleInput(event: Event) {
  const value = (event.target as HTMLInputElement).value
  localValue.value = value
  emit('update:modelValue', value)
  
  if (value.length >= props.minChars) {
    showDropdown.value = true
    emit('search', value)
  } else {
    showDropdown.value = false
  }
  
  activeIndex.value = -1
}

function handleFocus() {
  if (localValue.value.length >= props.minChars && visibleSuggestions.value.length > 0) {
    showDropdown.value = true
  }
}

function handleBlur() {
  // Delay hiding dropdown to allow click on suggestion
  setTimeout(() => {
    if (!isMouseOverDropdown.value) {
      showDropdown.value = false
    }
  }, 200)
}

function handleSuggestionClick(user: UserSearchResult) {
  selectUser(user)
}

function selectUser(user: UserSearchResult) {
  localValue.value = user.username
  emit('update:modelValue', user.username)
  emit('select', user)
  showDropdown.value = false
  activeIndex.value = -1
  
  // Focus back on input
  nextTick(() => {
    inputRef.value?.focus()
  })
}

function handleKeyDown(event: KeyboardEvent) {
  event.preventDefault()
  if (visibleSuggestions.value.length === 0) return
  
  activeIndex.value = Math.min(activeIndex.value + 1, visibleSuggestions.value.length - 1)
  scrollToActiveItem()
}

function handleKeyUp(event: KeyboardEvent) {
  event.preventDefault()
  if (visibleSuggestions.value.length === 0) return
  
  activeIndex.value = Math.max(activeIndex.value - 1, 0)
  scrollToActiveItem()
}

function handleEnter(event: KeyboardEvent) {
  if (activeIndex.value >= 0 && activeIndex.value < visibleSuggestions.value.length) {
    const user = visibleSuggestions.value[activeIndex.value]
    if (user) {
      event.preventDefault()
      selectUser(user)
    }
  }
}

function handleEscape() {
  showDropdown.value = false
  activeIndex.value = -1
}

function scrollToActiveItem() {
  nextTick(() => {
    const activeElement = dropdownRef.value?.querySelector(`[data-index="${activeIndex.value}"]`)
    if (activeElement) {
      activeElement.scrollIntoView({ block: 'nearest' })
    }
  })
}

function clear() {
  localValue.value = ''
  emit('update:modelValue', '')
  emit('clear')
  showDropdown.value = false
  activeIndex.value = -1
}

// Watch for modelValue changes from parent
watch(() => props.modelValue, (newValue) => {
  if (newValue !== localValue.value) {
    localValue.value = newValue
  }
})

// Watch for suggestions changes
watch(() => props.suggestions, (newSuggestions) => {
  if (newSuggestions.length > 0 && localValue.value.length >= props.minChars) {
    showDropdown.value = true
  } else if (newSuggestions.length === 0) {
    // Close dropdown when suggestions become empty
    showDropdown.value = false
  }
})

// Mouse events for dropdown
function onDropdownMouseEnter() {
  isMouseOverDropdown.value = true
}

function onDropdownMouseLeave() {
  isMouseOverDropdown.value = false
}

// Expose methods
defineExpose({
  clear,
  focus: () => inputRef.value?.focus(),
  blur: () => inputRef.value?.blur()
})
</script>

<style scoped>
.user-search-input input:disabled {
  @apply cursor-not-allowed bg-gray-50 dark:bg-gray-800;
}

/* Custom scrollbar for dropdown */
.user-search-input .overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: #9ca3af #f3f4f6;
}

.user-search-input .overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.user-search-input .overflow-y-auto::-webkit-scrollbar-track {
  background: #f3f4f6;
  border-radius: 3px;
}

.user-search-input .overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: #9ca3af;
  border-radius: 3px;
}

.dark .user-search-input .overflow-y-auto {
  scrollbar-color: #4b5563 #1f2937;
}

.dark .user-search-input .overflow-y-auto::-webkit-scrollbar-track {
  background: #1f2937;
}

.dark .user-search-input .overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: #4b5563;
}
</style>