<template>
  <div class="relative">
    <div class="relative">
      <Icon
        name="search"
        class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
        size="sm"
      />
      <input
        :value="modelValue"
        type="search"
        :placeholder="placeholder"
        class="w-full pl-10 pr-10 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        @keyup.enter="$emit('search', modelValue)"
      />
      <button
        v-if="modelValue"
        @click="$emit('update:modelValue', ''); $emit('search', '')"
        class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
      >
        <Icon name="x" size="sm" />
      </button>
    </div>
    
    <div v-if="showFilters" class="mt-2 flex flex-wrap gap-2">
      <select
        v-model="selectedFilter"
        class="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        @change="$emit('filter-change', selectedFilter)"
      >
        <option value="">All Categories</option>
        <option v-for="filter in filters" :key="filter.value" :value="filter.value">
          {{ filter.label }}
        </option>
      </select>
      
      <select
        v-model="selectedSort"
        class="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        @change="$emit('sort-change', selectedSort)"
      >
        <option value="relevance">Relevance</option>
        <option value="newest">Newest</option>
        <option value="popular">Most Popular</option>
        <option value="votes">Most Votes</option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Icon from '~/components/atoms/Icon.vue'

interface FilterOption {
  value: string
  label: string
}

interface Props {
  modelValue: string
  placeholder?: string
  showFilters?: boolean
  filters?: FilterOption[]
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Search...',
  showFilters: false,
  filters: () => []
})

defineEmits<{
  'update:modelValue': [value: string]
  'search': [value: string]
  'filter-change': [value: string]
  'sort-change': [value: string]
}>()

const selectedFilter = ref('')
const selectedSort = ref('relevance')
</script>

<style scoped>
/* Add any custom styles if needed */
</style>
