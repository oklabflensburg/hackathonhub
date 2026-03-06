<template>
  <div class="project-filter-item" :class="filterItemClasses">
    <!-- Filter Label -->
    <label
      v-if="showLabel"
      :for="filterId"
      class="filter-label block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
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
    
    <!-- Filter Input Container -->
    <div class="filter-input-container relative">
      <!-- Text Input -->
      <input
        v-if="type === 'text' || type === 'search'"
        :id="filterId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :aria-label="ariaLabel"
        class="filter-input w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-offset-1 transition-colors"
        :class="inputClasses"
        @input="handleInput"
        @keydown.enter="handleEnter"
        @blur="handleBlur"
      />
      
      <!-- Select Input -->
      <select
        v-else-if="type === 'select'"
        :id="filterId"
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        :aria-label="ariaLabel"
        class="filter-select w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-offset-1 transition-colors appearance-none"
        :class="selectClasses"
        @change="handleSelectChange"
      >
        <option
          v-if="showDefaultOption"
          value=""
          :disabled="required"
        >
          {{ defaultOptionText || 'Select an option' }}
        </option>
        <option
          v-for="option in options"
          :key="option.value"
          :value="option.value"
          :disabled="option.disabled"
        >
          {{ option.label }}
        </option>
      </select>
      
      <!-- Checkbox Group -->
      <div
        v-else-if="type === 'checkbox'"
        class="checkbox-group space-y-2"
      >
        <label
          v-for="option in options"
          :key="option.value"
          class="checkbox-item flex items-center gap-2 cursor-pointer"
        >
          <input
            type="checkbox"
            :value="option.value"
            :checked="isChecked(option.value)"
            :disabled="disabled || option.disabled"
            class="checkbox-input h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded"
            @change="handleCheckboxChange(option.value, $event)"
          />
          <span class="checkbox-label text-sm text-gray-700 dark:text-gray-300">
            {{ option.label }}
          </span>
          <span
            v-if="option.count !== undefined"
            class="checkbox-count text-xs text-gray-500 dark:text-gray-400 ml-auto"
          >
            ({{ option.count }})
          </span>
        </label>
      </div>
      
      <!-- Radio Group -->
      <div
        v-else-if="type === 'radio'"
        class="radio-group space-y-2"
      >
        <label
          v-for="option in options"
          :key="option.value"
          class="radio-item flex items-center gap-2 cursor-pointer"
        >
          <input
            type="radio"
            :value="option.value"
            :checked="modelValue === option.value"
            :disabled="disabled || option.disabled"
            class="radio-input h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600"
            @change="handleRadioChange(option.value)"
          />
          <span class="radio-label text-sm text-gray-700 dark:text-gray-300">
            {{ option.label }}
          </span>
          <span
            v-if="option.count !== undefined"
            class="radio-count text-xs text-gray-500 dark:text-gray-400 ml-auto"
          >
            ({{ option.count }})
          </span>
        </label>
      </div>
      
      <!-- Date Input -->
      <input
        v-else-if="type === 'date'"
        :id="filterId"
        type="date"
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        :aria-label="ariaLabel"
        class="filter-date w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-offset-1 transition-colors"
        :class="inputClasses"
        @change="handleDateChange"
      />
      
      <!-- Range Slider -->
      <div
        v-else-if="type === 'range'"
        class="range-slider-container"
      >
        <div class="range-values flex justify-between text-xs text-gray-500 dark:text-gray-400 mb-1">
          <span>{{ minLabel || min }}</span>
          <span>{{ maxLabel || max }}</span>
        </div>
        <input
          :id="filterId"
          type="range"
          :value="modelValue"
          :min="min"
          :max="max"
          :step="step"
          :disabled="disabled"
          :aria-label="ariaLabel"
          class="filter-range w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer"
          :class="rangeClasses"
          @input="handleRangeInput"
          @change="handleRangeChange"
        />
        <div class="range-current-value text-center text-sm font-medium text-gray-700 dark:text-gray-300 mt-1">
          {{ currentRangeValue }}
        </div>
      </div>
      
      <!-- Search Icon (for search type) -->
      <div
        v-if="type === 'search' && showSearchIcon"
        class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
        aria-hidden="true"
      >
        <svg
          class="h-4 w-4 text-gray-400 dark:text-gray-500"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>
      
      <!-- Clear Button (when value exists) -->
      <button
        v-if="showClearButton && modelValue && !disabled"
        type="button"
        class="absolute inset-y-0 right-0 pr-3 flex items-center"
        :class="clearButtonClasses"
        :aria-label="`Clear ${label}`"
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
    
    <!-- Helper Text -->
    <p
      v-if="helperText"
      class="helper-text mt-1 text-xs"
      :class="helperTextClasses"
      :id="`${filterId}-helper`"
    >
      {{ helperText }}
    </p>
    
    <!-- Error Message -->
    <p
      v-if="error"
      class="error-message mt-1 text-xs"
      :class="errorClasses"
      :id="`${filterId}-error`"
    >
      {{ error }}
    </p>
    
    <!-- Selected Values (for multi-select) -->
    <div
      v-if="showSelectedValues && selectedValues.length > 0"
      class="selected-values mt-2"
    >
      <div class="selected-label text-xs text-gray-500 dark:text-gray-400 mb-1">
        Selected:
      </div>
      <div class="selected-tags flex flex-wrap gap-1">
        <span
          v-for="value in selectedValues"
          :key="value"
          class="selected-tag inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300"
        >
          {{ getOptionLabel(value) }}
          <button
            v-if="!disabled"
            type="button"
            class="ml-1 text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-200 focus:outline-none"
            :aria-label="`Remove ${getOptionLabel(value)}`"
            @click="handleRemoveSelected(value)"
          >
            <svg
              class="h-3 w-3"
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
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

interface FilterOption {
  value: string | number
  label: string
  disabled?: boolean
  count?: number
}

interface Props {
  /** Filter-Typ */
  type?: 'text' | 'search' | 'select' | 'checkbox' | 'radio' | 'date' | 'range'
  /** v-model Wert */
  modelValue?: string | number | string[] | number[] | null
  /** Filter-Label */
  label?: string
  /** Platzhalter-Text */
  placeholder?: string
  /** Optionen für select/checkbox/radio */
  options?: FilterOption[]
  /** Minimum (für range) */
  min?: number
  /** Maximum (für range) */
  max?: number
  /** Step (für range) */
  step?: number
  /** Minimum Label (für range) */
  minLabel?: string
  /** Maximum Label (für range) */
  maxLabel?: string
  /** Deaktiviert */
  disabled?: boolean
  /** Erforderlich */
  required?: boolean
  /** Label anzeigen */
  showLabel?: boolean
  /** Default Option für Select anzeigen */
  showDefaultOption?: boolean
  /** Default Option Text */
  defaultOptionText?: string
  /** Search Icon anzeigen */
  showSearchIcon?: boolean
  /** Clear Button anzeigen */
  showClearButton?: boolean
  /** Selected Values anzeigen */
  showSelectedValues?: boolean
  /** Helper Text */
  helperText?: string
  /** Error Message */
  error?: string
  /** Größe */
  size?: 'sm' | 'md' | 'lg'
  /** Variante */
  variant?: 'default' | 'outline' | 'filled'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  label: '',
  placeholder: '',
  options: () => [],
  min: 0,
  max: 100,
  step: 1,
  disabled: false,
  required: false,
  showLabel: true,
  showDefaultOption: true,
  showSearchIcon: true,
  showClearButton: true,
  showSelectedValues: true,
  size: 'md',
  variant: 'default',
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number | string[] | number[] | (string | number)[] | null): void
  (e: 'change', value: string | number | string[] | number[] | (string | number)[] | null): void
  (e: 'input', value: string): void
  (e: 'clear'): void
  (e: 'enter', value: string): void
  (e: 'blur'): void
}>()

// Computed Properties
const filterId = computed(() => {
  return `filter-${Math.random().toString(36).substr(2, 9)}`
})

const ariaLabel = computed(() => {
  return props.label || props.placeholder || 'Filter input'
})

const filterItemClasses = computed(() => {
  return props.disabled ? 'opacity-60 cursor-not-allowed' : ''
})

const inputClasses = computed(() => {
  const classes: string[] = []
  
  // Size
  switch (props.size) {
    case 'sm':
      classes.push('py-1.5 text-xs')
      break
    case 'lg':
      classes.push('py-2.5 text-base')
      break
    case 'md':
    default:
      classes.push('py-2 text-sm')
  }
  
  // Variant
  switch (props.variant) {
    case 'outline':
      classes.push('border-gray-300 dark:border-gray-600 bg-transparent focus:border-blue-500 dark:focus:border-blue-400 focus:ring-blue-500 dark:focus:ring-blue-400')
      break
    case 'filled':
      classes.push('border-transparent bg-gray-100 dark:bg-gray-800 focus:bg-white dark:focus:bg-gray-900 focus:ring-blue-500 dark:focus:ring-blue-400')
      break
    case 'default':
    default:
      classes.push('border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 focus:border-blue-500 dark:focus:border-blue-400 focus:ring-blue-500 dark:focus:ring-blue-400')
  }
  
  // Error State
  if (props.error) {
    classes.push('border-red-300 dark:border-red-700 focus:border-red-500 dark:focus:border-red-400 focus:ring-red-500 dark:focus:ring-red-400')
  }
  
  // Disabled State
  if (props.disabled) {
    classes.push('bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 cursor-not-allowed')
  }
  
  return classes.join(' ')
})

const selectClasses = computed(() => {
  const base = inputClasses.value
  return `${base} pr-8`
})

const rangeClasses = computed(() => {
  const classes: string[] = []
  
  if (props.disabled) {
    classes.push('opacity-50 cursor-not-allowed')
  }
  
  return classes.join(' ')
})

const clearButtonClasses = computed(() => {
  return 'text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 focus:outline-none focus:text-gray-600 dark:focus:text-gray-300'
})

const helperTextClasses = computed(() => {
  return props.error ? 'text-red-600 dark:text-red-400' : 'text-gray-500 dark:text-gray-400'
})

const errorClasses = computed(() => {
  return 'text-red-600 dark:text-red-400'
})

const currentRangeValue = computed(() => {
  if (props.type !== 'range' || !props.modelValue) return ''
  
  if (props.options && props.options.length > 0) {
    const option = props.options.find(opt => opt.value === props.modelValue)
    return option ? option.label : props.modelValue
  }
  
  return props.modelValue
})

const selectedValues = computed(() => {
  if (!props.modelValue) return []
  
  if (Array.isArray(props.modelValue)) {
    return props.modelValue
  }
  
  return [props.modelValue]
})

// Helper Functions
const isChecked = (value: string | number) => {
  if (!props.modelValue || !Array.isArray(props.modelValue)) return false
  return props.modelValue.includes(value as never)
}

const getOptionLabel = (value: string | number) => {
  const option = props.options.find(opt => opt.value === value)
  return option ? option.label : String(value)
}

// Event Handlers
const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('input', target.value)
  emit('update:modelValue', target.value)
}

const handleEnter = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('enter', target.value)
}

const handleBlur = () => {
  emit('blur')
}

const handleSelectChange = (event: Event) => {
  const target = event.target as HTMLSelectElement
  emit('update:modelValue', target.value)
  emit('change', target.value)
}

const handleCheckboxChange = (value: string | number, event: Event) => {
  const target = event.target as HTMLInputElement
  const currentValue = props.modelValue as (string | number)[] || []
  
  let newValue: (string | number)[]
  if (target.checked) {
    newValue = [...currentValue, value]
  } else {
    newValue = currentValue.filter(v => v !== value)
  }
  
  emit('update:modelValue', newValue)
  emit('change', newValue)
}

const handleRadioChange = (value: string | number) => {
  emit('update:modelValue', value)
  emit('change', value)
}

const handleDateChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
  emit('change', target.value)
}

const handleRangeInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  // Only update model on change, not on every input
}

const handleRangeChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const value = props.options && props.options.length > 0
    ? props.options[target.valueAsNumber]?.value || target.value
    : target.value
  
  emit('update:modelValue', value)
  emit('change', value)
}

const handleClear = () => {
  if (props.type === 'checkbox') {
    emit('update:modelValue', [] as (string | number)[])
    emit('change', [] as (string | number)[])
  } else {
    emit('update:modelValue', null)
    emit('change', null)
  }
  emit('clear')
}

const handleRemoveSelected = (value: string | number) => {
  if (props.type === 'checkbox') {
    const currentValue = props.modelValue as (string | number)[] || []
    const newValue = currentValue.filter(v => v !== value)
    emit('update:modelValue', newValue)
    emit('change', newValue)
  } else {
    emit('update:modelValue', null)
    emit('change', null)
  }
}
</script>
