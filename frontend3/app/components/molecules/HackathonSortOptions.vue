<template>
  <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3">
    <!-- Label -->
    <div class="flex items-center gap-2">
      <Icon name="sort" class="w-4 h-4 text-gray-500" />
      <span class="text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap">
        Sortieren nach:
      </span>
    </div>

    <!-- Sort Options -->
    <div class="flex flex-wrap gap-2">
      <button
        v-for="option in sortOptions"
        :key="option.value"
        type="button"
        class="inline-flex items-center gap-2 px-3 py-2 rounded-lg border transition-colors"
        :class="[
          selectedSort === option.value
            ? 'bg-blue-50 dark:bg-blue-900/30 border-blue-200 dark:border-blue-700 text-blue-700 dark:text-blue-300'
            : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
        ]"
        @click="selectSort(option.value)"
      >
        <Icon :name="option.icon" class="w-4 h-4" />
        <span class="text-sm font-medium">{{ option.label }}</span>
        <Icon
          v-if="selectedSort === option.value && sortDirection === 'asc'"
          name="chevron-up"
          class="w-4 h-4"
        />
        <Icon
          v-if="selectedSort === option.value && sortDirection === 'desc'"
          name="chevron-down"
          class="w-4 h-4"
        />
      </button>
    </div>

    <!-- Direction Toggle -->
    <button
      v-if="selectedSort"
      type="button"
      class="inline-flex items-center gap-2 px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
      @click="toggleDirection"
      :title="sortDirection === 'asc' ? 'Aufsteigend' : 'Absteigend'"
    >
      <Icon
        :name="sortDirection === 'asc' ? 'arrow-up' : 'arrow-down'"
        class="w-4 h-4"
      />
      <span class="text-sm font-medium">
        {{ sortDirection === 'asc' ? 'Aufsteigend' : 'Absteigend' }}
      </span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Icon from '~/components/atoms/Icon.vue'

interface SortOption {
  value: string
  label: string
  icon: string
  defaultDirection?: 'asc' | 'desc'
}

interface Props {
  modelValue?: string
  direction?: 'asc' | 'desc'
  options?: SortOption[]
}

interface Emits {
  (e: 'update:modelValue', value: string): void
  (e: 'update:direction', direction: 'asc' | 'desc'): void
  (e: 'change', payload: { sort: string; direction: 'asc' | 'desc' }): void
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: 'newest',
  direction: 'desc',
  options: () => [
    { value: 'newest', label: 'Neueste', icon: 'calendar', defaultDirection: 'desc' },
    { value: 'oldest', label: 'Älteste', icon: 'calendar', defaultDirection: 'asc' },
    { value: 'participants', label: 'Teilnehmer', icon: 'users', defaultDirection: 'desc' },
    { value: 'prize', label: 'Preisgeld', icon: 'award', defaultDirection: 'desc' },
    { value: 'deadline', label: 'Deadline', icon: 'clock', defaultDirection: 'asc' },
    { value: 'name', label: 'Name', icon: 'type', defaultDirection: 'asc' },
    { value: 'popularity', label: 'Beliebtheit', icon: 'trending-up', defaultDirection: 'desc' }
  ]
})

const emit = defineEmits<Emits>()

const selectedSort = ref(props.modelValue)
const sortDirection = ref(props.direction)

const sortOptions = computed(() => props.options)

function selectSort(sort: string) {
  const option = sortOptions.value.find(opt => opt.value === sort)
  
  if (option) {
    // If clicking the same sort option, toggle direction
    if (selectedSort.value === sort) {
      toggleDirection()
    } else {
      // Select new sort option with its default direction
      selectedSort.value = sort
      sortDirection.value = option.defaultDirection || 'desc'
      
      emit('update:modelValue', sort)
      emit('update:direction', sortDirection.value)
      emitChange()
    }
  }
}

function toggleDirection() {
  sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  emit('update:direction', sortDirection.value)
  emitChange()
}

function emitChange() {
  emit('change', {
    sort: selectedSort.value,
    direction: sortDirection.value
  })
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  selectedSort.value = newValue
})

watch(() => props.direction, (newValue) => {
  sortDirection.value = newValue
})
</script>

<style scoped>
/* Additional styling if needed */
</style>