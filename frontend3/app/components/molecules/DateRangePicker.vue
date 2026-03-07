<template>
  <div class="date-range-picker" ref="containerRef">
    <!-- Trigger button/input -->
    <div class="trigger-container" @click="togglePicker">
      <slot name="trigger" :start-date="modelValue?.start" :end-date="modelValue?.end">
        <div class="default-trigger flex items-center gap-2 px-3 py-2 border rounded-md bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer">
          <Icon
            name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' /></svg>"
            :size="16"
            is-svg
            class="text-gray-500"
          />
          <span class="text-sm">
            {{ displayText }}
          </span>
          <Icon
            name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7' /></svg>"
            :size="16"
            is-svg
            class="text-gray-500 ml-auto"
          />
        </div>
      </slot>
    </div>

    <!-- Picker dropdown -->
    <Teleport v-if="isMounted" to="body">
      <div
        v-if="isOpen"
        ref="pickerRef"
        :class="pickerClasses"
        :style="pickerStyles"
        @click.stop
      >
        <!-- Header with month/year navigation -->
        <div class="picker-header">
          <div class="flex items-center justify-between mb-4">
            <button
              type="button"
              class="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
              @click="previousMonth"
              aria-label="Previous month"
            >
              <Icon
                name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15 19l-7-7 7-7' /></svg>"
                :size="20"
                is-svg
              />
            </button>
            
            <div class="flex items-center gap-2">
              <select
                v-model="currentMonth"
                class="bg-transparent border-none focus:outline-none text-sm font-medium"
                @change="handleMonthChange"
              >
                <option v-for="month in months" :key="month.value" :value="month.value">
                  {{ month.label }}
                </option>
              </select>
              
              <select
                v-model="currentYear"
                class="bg-transparent border-none focus:outline-none text-sm font-medium"
                @change="handleYearChange"
              >
                <option v-for="year in years" :key="year" :value="year">
                  {{ year }}
                </option>
              </select>
            </div>
            
            <button
              type="button"
              class="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
              @click="nextMonth"
              aria-label="Next month"
            >
              <Icon
                name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 5l7 7-7 7' /></svg>"
                :size="20"
                is-svg
              />
            </button>
          </div>
          
          <!-- Weekday headers -->
          <div class="grid grid-cols-7 gap-1 mb-2">
            <div
              v-for="day in weekdays"
              :key="day"
              class="text-center text-xs font-medium text-gray-500 dark:text-gray-400 py-1"
            >
              {{ day }}
            </div>
          </div>
        </div>

        <!-- Calendar grid -->
        <div class="calendar-grid">
          <div
            v-for="(day, index) in calendarDays"
            :key="index"
            :class="dayClasses(day)"
            @click="selectDate(day)"
            @mouseenter="hoverDate(day)"
            @mouseleave="hoverDate(null)"
          >
            <span class="day-number">
              {{ day ? day.getDate() : '' }}
            </span>
          </div>
        </div>

        <!-- Quick selection buttons -->
        <div v-if="presets.length > 0" class="presets mt-4 pt-4 border-t dark:border-gray-700">
          <div class="grid grid-cols-2 gap-2">
            <button
              v-for="preset in presets"
              :key="preset.label"
              type="button"
              class="text-xs px-3 py-1.5 rounded border hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              @click="applyPreset(preset)"
            >
              {{ preset.label }}
            </button>
          </div>
        </div>

        <!-- Action buttons -->
        <div class="actions mt-4 pt-4 border-t dark:border-gray-700 flex justify-between">
          <button
            type="button"
            class="text-sm px-3 py-1.5 rounded border hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            @click="clearSelection"
          >
            Clear
          </button>
          
          <div class="flex gap-2">
            <button
              type="button"
              class="text-sm px-3 py-1.5 rounded border hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              @click="closePicker"
            >
              Cancel
            </button>
            
            <button
              type="button"
              class="text-sm px-3 py-1.5 rounded bg-primary-600 text-white hover:bg-primary-700 transition-colors"
              @click="applySelection"
            >
              Apply
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import Icon from '../atoms/Icon.vue'

export interface DateRange {
  start: Date | null
  end: Date | null
}

export interface DateRangePickerProps {
  /** Current date range value */
  modelValue?: DateRange
  /** Minimum selectable date */
  minDate?: Date
  /** Maximum selectable date */
  maxDate?: Date
  /** Whether the picker is disabled */
  disabled?: boolean
  /** Placeholder text when no date is selected */
  placeholder?: string
  /** Format for displaying selected dates */
  displayFormat?: string
  /** Preset date ranges */
  presets?: Array<{
    label: string
    start: Date
    end: Date
  }>
  /** Position of the picker dropdown */
  position?: 'bottom' | 'top' | 'left' | 'right'
}

const props = withDefaults(defineProps<DateRangePickerProps>(), {
  placeholder: 'Select date range',
  displayFormat: 'MMM d, yyyy',
  presets: () => [
    { label: 'Today', start: new Date(), end: new Date() },
    { label: 'Yesterday', start: new Date(Date.now() - 86400000), end: new Date(Date.now() - 86400000) },
    { label: 'Last 7 days', start: new Date(Date.now() - 6 * 86400000), end: new Date() },
    { label: 'Last 30 days', start: new Date(Date.now() - 29 * 86400000), end: new Date() },
    { label: 'This month', start: new Date(new Date().getFullYear(), new Date().getMonth(), 1), end: new Date() },
    { label: 'Last month', start: new Date(new Date().getFullYear(), new Date().getMonth() - 1, 1), end: new Date(new Date().getFullYear(), new Date().getMonth(), 0) },
  ],
  position: 'bottom',
})

const emit = defineEmits<{
  /** Emitted when date range changes */
  'update:modelValue': [value: DateRange]
  /** Emitted when selection is applied */
  apply: [value: DateRange]
  /** Emitted when picker is opened */
  open: []
  /** Emitted when picker is closed */
  close: []
}>()

// Refs
const containerRef = ref<HTMLElement>()
const pickerRef = ref<HTMLElement>()
const isOpen = ref(false)
const isMounted = ref(false)
const currentMonth = ref(new Date().getMonth())
const currentYear = ref(new Date().getFullYear())
const hoveredDate = ref<Date | null>(null)
const tempSelection = ref<DateRange>({ start: null, end: null })

// Current value
const value = computed({
  get: () => props.modelValue || { start: null, end: null },
  set: (val) => emit('update:modelValue', val),
})

// Initialize temp selection with current value
watch(value, (newVal) => {
  tempSelection.value = { ...newVal }
}, { immediate: true })

// Months for dropdown
const months = computed(() => {
  return Array.from({ length: 12 }, (_, i) => ({
    value: i,
    label: new Date(2000, i, 1).toLocaleDateString('en-US', { month: 'long' }),
  }))
})

// Years for dropdown (10 years back and forward)
const years = computed(() => {
  const currentYear = new Date().getFullYear()
  return Array.from({ length: 21 }, (_, i) => currentYear - 10 + i)
})

// Weekday labels
const weekdays = computed(() => {
  return ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
})

// Calendar days for current month
const calendarDays = computed(() => {
  const firstDayOfMonth = new Date(currentYear.value, currentMonth.value, 1)
  const lastDayOfMonth = new Date(currentYear.value, currentMonth.value + 1, 0)
  const firstDayOfWeek = firstDayOfMonth.getDay()
  const daysInMonth = lastDayOfMonth.getDate()
  
  const days: (Date | null)[] = []
  
  // Add empty cells for days before the first day of the month
  for (let i = 0; i < firstDayOfWeek; i++) {
    days.push(null)
  }
  
  // Add days of the month
  for (let i = 1; i <= daysInMonth; i++) {
    days.push(new Date(currentYear.value, currentMonth.value, i))
  }
  
  return days
})

// Display text for trigger
const displayText = computed(() => {
  const { start, end } = value.value
  
  if (!start && !end) {
    return props.placeholder
  }
  
  if (start && end) {
    const format = (date: Date) => date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
    return `${format(start)} - ${format(end)}`
  }
  
  if (start) {
    return `From ${start.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`
  }
  
  return props.placeholder
})

// Picker classes
const pickerClasses = computed(() => {
  const base = [
    'date-picker-dropdown',
    'absolute',
    'z-50',
    'bg-white',
    'dark:bg-gray-800',
    'border',
    'rounded-lg',
    'shadow-lg',
    'p-4',
    'min-w-64',
  ]
  
  // Position classes
  if (props.position === 'bottom') {
    base.push('top-full mt-1')
  } else if (props.position === 'top') {
    base.push('bottom-full mb-1')
  }
  
  return base.join(' ')
})

// Picker styles
const pickerStyles = computed(() => {
  if (!containerRef.value || !isOpen.value) {
    return {}
  }
  
  const rect = containerRef.value.getBoundingClientRect()
  
  return {
    left: `${rect.left}px`,
    top: props.position === 'bottom' ? `${rect.bottom}px` : 'auto',
    bottom: props.position === 'top' ? `${window.innerHeight - rect.top}px` : 'auto',
  }
})

// Day classes
const dayClasses = (day: Date | null) => {
  if (!day) return 'day-cell empty'
  
  const classes = ['day-cell', 'text-center', 'py-2', 'rounded', 'cursor-pointer', 'transition-colors']
  
  // Check if day is today
  const today = new Date()
  if (day.getDate() === today.getDate() &&
      day.getMonth() === today.getMonth() &&
      day.getFullYear() === today.getFullYear()) {
    classes.push('today')
  }
  
  // Check if day is in current month
  if (day.getMonth() !== currentMonth.value) {
    classes.push('other-month', 'text-gray-400', 'dark:text-gray-500')
  }
  
  // Check if day is selected
  const { start, end } = tempSelection.value
  if (start && day.getTime() === start.getTime()) {
    classes.push('selected-start', 'bg-primary-600', 'text-white')
  } else if (end && day.getTime() === end.getTime()) {
    classes.push('selected-end', 'bg-primary-600', 'text-white')
  } else if (start && end && day > start && day < end) {
    classes.push('in-range', 'bg-primary-100', 'dark:bg-primary-900')
  }
  
  // Check if day is hovered (for range selection)
  if (hoveredDate.value && start && !end) {
    const hover = hoveredDate.value
    if ((day > start && day < hover) || (day < start && day > hover)) {
      classes.push('hover-range', 'bg-primary-50', 'dark:bg-primary-800')
    }
  }
  
  // Check if day is disabled
  if (props.minDate && day < props.minDate) {
    classes.push('disabled', 'opacity-50', 'cursor-not-allowed')
  } else if (props.maxDate && day > props.maxDate) {
    classes.push('disabled', 'opacity-50', 'cursor-not-allowed')
  }
  
  return classes.join(' ')
}

// Methods
const togglePicker = () => {
  if (props.disabled) return
  
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    emit('open')
    document.addEventListener('click', handleClickOutside)
  } else {
    emit('close')
    document.removeEventListener('click', handleClickOutside)
  }
}

const closePicker = () => {
  isOpen.value = false
  emit('close')
  document.removeEventListener('click', handleClickOutside)
}

const handleClickOutside = (event: MouseEvent) => {
  if (pickerRef.value && !pickerRef.value.contains(event.target as Node) &&
      containerRef.value && !containerRef.value.contains(event.target as Node)) {
    closePicker()
  }
}

const selectDate = (day: Date | null) => {
  if (!day || props.disabled) return
  
  // Check if date is within min/max bounds
  if (props.minDate && day < props.minDate) return
  if (props.maxDate && day > props.maxDate) return
  
  const { start, end } = tempSelection.value
  
  if (!start || (start && end)) {
    // Start new selection
    tempSelection.value = { start: day, end: null }
  } else if (start && !end) {
    // Complete selection
    if (day > start) {
      tempSelection.value = { start, end: day }
    } else {
      tempSelection.value = { start: day, end: start }
    }
  }
}

const hoverDate = (day: Date | null) => {
  hoveredDate.value = day
}

const previousMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

const handleMonthChange = () => {
  // Month already updated via v-model
}

const handleYearChange = () => {
  // Year already updated via v-model
}

const applyPreset = (preset: { start: Date; end: Date }) => {
  tempSelection.value = { start: preset.start, end: preset.end }
  applySelection()
}

const clearSelection = () => {
  tempSelection.value = { start: null, end: null }
}

const applySelection = () => {
  value.value = { ...tempSelection.value }
  emit('apply', value.value)
  closePicker()
}

// Lifecycle
onMounted(() => {
  isMounted.value = true
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.date-range-picker {
  position: relative;
  display: inline-block;
}

.default-trigger {
  transition: all 0.2s ease;
}

.default-trigger:hover {
  border-color: var(--primary-500);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
}

.day-cell {
  min-width: 32px;
  min-height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
}

.day-cell:hover:not(.disabled):not(.selected-start):not(.selected-end) {
  background-color: var(--gray-100);
  color: var(--gray-900);
}

.day-cell.today {
  font-weight: 600;
  color: var(--primary-600);
}

.day-cell.selected-start,
.day-cell.selected-end {
  font-weight: 600;
}

.day-cell.in-range {
  color: var(--primary-700);
}

.day-cell.disabled {
  pointer-events: none;
  color: var(--gray-400);
}

.day-cell.other-month {
  color: var(--gray-400);
}

.date-picker-dropdown {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.presets button {
  transition: all 0.2s ease;
}

.presets button:hover {
  background-color: var(--primary-50);
  border-color: var(--primary-300);
  color: var(--primary-700);
}

.actions button {
  transition: all 0.2s ease;
}
</style>