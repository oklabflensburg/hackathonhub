<template>
  <div class="flex flex-col md:flex-row gap-4 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
    <!-- Search Input -->
    <div class="flex-1">
      <div class="relative">
        <Icon name="search" class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
        <Input
          v-model="searchQuery"
          placeholder="Hackathons suchen..."
          class="pl-10 w-full"
          @input="onSearch"
        />
      </div>
    </div>

    <!-- Status Filter -->
    <div class="flex items-center gap-2">
      <label class="text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap">
        Status:
      </label>
      <Select v-model="selectedStatus" @change="onStatusChange" class="min-w-[120px]">
        <option value="all">Alle</option>
        <option value="upcoming">Bevorstehend</option>
        <option value="active">Aktiv</option>
        <option value="past">Vergangen</option>
      </Select>
    </div>

    <!-- Location Filter -->
    <div class="flex items-center gap-2">
      <label class="text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap">
        Ort:
      </label>
      <Select v-model="selectedLocation" @change="onLocationChange" class="min-w-[140px]">
        <option value="all">Alle</option>
        <option value="virtual">Virtual</option>
        <option value="physical">Vor Ort</option>
        <option value="hybrid">Hybrid</option>
      </Select>
    </div>

    <!-- Sort Options -->
    <div class="flex items-center gap-2">
      <label class="text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap">
        Sortieren:
      </label>
      <Select v-model="selectedSort" @change="onSortChange" class="min-w-[140px]">
        <option value="newest">Neueste zuerst</option>
        <option value="oldest">Älteste zuerst</option>
        <option value="participants">Meiste Teilnehmer</option>
        <option value="prize">Höchster Preis</option>
        <option value="deadline">Nächste Deadline</option>
      </Select>
    </div>

    <!-- Clear Filters Button -->
    <Button
      v-if="hasActiveFilters"
      variant="outline"
      size="sm"
      @click="clearFilters"
      class="whitespace-nowrap"
    >
      <Icon name="x" class="w-4 h-4 mr-1" />
      Filter löschen
    </Button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Icon from '~/components/atoms/Icon.vue'
import Input from '~/components/atoms/Input.vue'
import Select from '~/components/atoms/Select.vue'
import Button from '~/components/atoms/Button.vue'

interface Props {
  initialSearch?: string
  initialStatus?: string
  initialLocation?: string
  initialSort?: string
}

interface Emits {
  (e: 'search', value: string): void
  (e: 'status-change', value: string): void
  (e: 'location-change', value: string): void
  (e: 'sort-change', value: string): void
  (e: 'clear-filters'): void
}

const props = withDefaults(defineProps<Props>(), {
  initialSearch: '',
  initialStatus: 'all',
  initialLocation: 'all',
  initialSort: 'newest'
})

const emit = defineEmits<Emits>()

const searchQuery = ref(props.initialSearch)
const selectedStatus = ref(props.initialStatus)
const selectedLocation = ref(props.initialLocation)
const selectedSort = ref(props.initialSort)

const hasActiveFilters = computed(() => {
  return (
    searchQuery.value !== '' ||
    selectedStatus.value !== 'all' ||
    selectedLocation.value !== 'all' ||
    selectedSort.value !== 'newest'
  )
})

function onSearch() {
  emit('search', searchQuery.value)
}

function onStatusChange() {
  emit('status-change', selectedStatus.value)
}

function onLocationChange() {
  emit('location-change', selectedLocation.value)
}

function onSortChange() {
  emit('sort-change', selectedSort.value)
}

function clearFilters() {
  searchQuery.value = ''
  selectedStatus.value = 'all'
  selectedLocation.value = 'all'
  selectedSort.value = 'newest'
  
  emit('search', '')
  emit('status-change', 'all')
  emit('location-change', 'all')
  emit('sort-change', 'newest')
  emit('clear-filters')
}
</script>

<style scoped>
/* Additional styling if needed */
</style>