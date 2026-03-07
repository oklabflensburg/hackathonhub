<template>
  <div class="relative w-full">
    <!-- Search Icon -->
    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
      <Icon name="search" class="h-5 w-5 text-gray-400" />
    </div>

    <!-- Input Field -->
    <Input
      ref="inputRef"
      v-model="searchValue"
      :placeholder="placeholder"
      :disabled="disabled"
      class="pl-10 pr-10 w-full"
      @input="handleInput"
      @focus="handleFocus"
      @blur="handleBlur"
      @keydown.enter="handleSubmit"
      @keydown.esc="handleClear"
    />

    <!-- Clear Button -->
    <button
      v-if="showClearButton"
      type="button"
      class="absolute inset-y-0 right-0 pr-3 flex items-center"
      @click="handleClear"
      @mousedown.prevent
    >
      <Icon name="x" class="h-5 w-5 text-gray-400 hover:text-gray-600" />
    </button>

    <!-- Loading Indicator -->
    <div
      v-if="loading"
      class="absolute inset-y-0 right-0 pr-3 flex items-center"
    >
      <Icon name="loader" class="h-5 w-5 text-gray-400 animate-spin" />
    </div>

    <!-- Search Suggestions Dropdown -->
    <div
      v-if="showSuggestions && suggestions.length > 0"
      class="absolute z-10 mt-1 w-full bg-white dark:bg-gray-800 shadow-lg rounded-md border border-gray-200 dark:border-gray-700 max-h-60 overflow-auto"
    >
      <div
        v-for="(suggestion, index) in suggestions"
        :key="index"
        class="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer flex items-center justify-between"
        @click="selectSuggestion(suggestion)"
        @mouseenter="hoveredIndex = index"
        @mouseleave="hoveredIndex = -1"
        :class="{
          'bg-gray-100 dark:bg-gray-700': hoveredIndex === index
        }"
      >
        <div class="flex items-center">
          <Icon name="search" class="h-4 w-4 text-gray-400 mr-2" />
          <span class="text-gray-700 dark:text-gray-300">{{ suggestion.text }}</span>
        </div>
          <Badge v-if="suggestion.count" size="sm" variant="gray">
          {{ suggestion.count }}
        </Badge>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import Icon from '~/components/atoms/Icon.vue'
import Input from '~/components/atoms/Input.vue'
import Badge from '~/components/atoms/Badge.vue'

interface Suggestion {
  text: string
  value: string
  count?: number
}

interface Props {
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  loading?: boolean
  debounce?: number
  showSuggestions?: boolean
  suggestions?: Suggestion[]
  autoFocus?: boolean
}

interface Emits {
  (e: 'update:modelValue', value: string): void
  (e: 'search', value: string): void
  (e: 'clear'): void
  (e: 'focus'): void
  (e: 'blur'): void
  (e: 'select-suggestion', suggestion: Suggestion): void
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: 'Hackathons suchen...',
  disabled: false,
  loading: false,
  debounce: 300,
  showSuggestions: false,
  suggestions: () => [],
  autoFocus: false
})

const emit = defineEmits<Emits>()

const inputRef = ref<HTMLInputElement>()
const searchValue = ref(props.modelValue)
const isFocused = ref(false)
const hoveredIndex = ref(-1)
let debounceTimer: NodeJS.Timeout | null = null

const showClearButton = computed(() => {
  return searchValue.value.length > 0 && !props.loading
})

function handleInput() {
  emit('update:modelValue', searchValue.value)
  
  // Debounce the search event
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  debounceTimer = setTimeout(() => {
    emit('search', searchValue.value)
  }, props.debounce)
}

function handleSubmit() {
  emit('search', searchValue.value)
}

function handleClear() {
  searchValue.value = ''
  emit('update:modelValue', '')
  emit('clear')
  emit('search', '')
  
  // Focus the input after clearing
  nextTick(() => {
    inputRef.value?.focus()
  })
}

function handleFocus() {
  isFocused.value = true
  emit('focus')
}

function handleBlur() {
  // Small delay to allow click events on suggestions
  setTimeout(() => {
    isFocused.value = false
    emit('blur')
  }, 200)
}

function selectSuggestion(suggestion: Suggestion) {
  searchValue.value = suggestion.text
  emit('update:modelValue', suggestion.text)
  emit('select-suggestion', suggestion)
  emit('search', suggestion.text)
  
  // Focus back on input
  nextTick(() => {
    inputRef.value?.focus()
  })
}

// Auto-focus if requested
if (props.autoFocus) {
  nextTick(() => {
    inputRef.value?.focus()
  })
}
</script>

<style scoped>
/* Additional styling if needed */
</style>