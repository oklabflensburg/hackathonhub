<template>
  <div class="flex items-center justify-between">
    <div class="text-sm text-gray-600 dark:text-gray-300">
      <slot name="info" :start="startItem" :end="endItem" :total="effectiveTotalItems">
         Showing {{ startItem }}-{{ endItem }} of {{ effectiveTotalItems }} items
      </slot>
    </div>
    
    <div class="flex items-center gap-1">
      <Button
        :disabled="currentPage === 1"
        variant="ghost"
        size="sm"
        @click="$emit('page-change', currentPage - 1)"
      >
        <template #icon>
          <Icon name="chevron-left" size="sm" />
        </template>
        Previous
      </Button>
      
      <div class="flex items-center gap-1">
        <template v-for="page in visiblePages" :key="page">
          <Button
            v-if="page === '...'"
            variant="ghost"
            size="sm"
            disabled
            class="cursor-default"
          >
            ...
          </Button>
          <Button
            v-else
            :variant="page === currentPage ? 'primary' : 'ghost'"
            size="sm"
            @click="$emit('page-change', page as number)"
          >
            {{ page }}
          </Button>
        </template>
      </div>
      
      <Button
        :disabled="currentPage === totalPages"
        variant="ghost"
        size="sm"
        @click="$emit('page-change', currentPage + 1)"
      >
        Next
        <template #icon>
          <Icon name="chevron-right" size="sm" />
        </template>
      </Button>
    </div>
    
    <div class="flex items-center gap-2">
      <span class="text-sm text-gray-600 dark:text-gray-300">Items per page:</span>
      <select
        :value="itemsPerPage"
        class="px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        @change="$emit('per-page-change', parseInt(($event.target as HTMLSelectElement).value))"
      >
        <option v-for="option in perPageOptions" :key="option" :value="option">
          {{ option }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Button from '~/components/atoms/Button.vue'
import Icon from '~/components/atoms/Icon.vue'

interface Props {
  currentPage: number
  itemsPerPage?: number
  perPage?: number // Alias for itemsPerPage for backward compatibility
  totalItems?: number
  total?: number // Alias for totalItems for backward compatibility
  perPageOptions?: number[]
  maxVisiblePages?: number
}

const props = withDefaults(defineProps<Props>(), {
  perPageOptions: () => [10, 25, 50, 100],
  maxVisiblePages: 5
})

// Use totalItems or total (alias)
const effectiveTotalItems = computed(() => {
  return props.totalItems ?? props.total ?? 0
})

// Use itemsPerPage or perPage (alias)
const effectiveItemsPerPage = computed(() => {
  return props.itemsPerPage ?? props.perPage ?? 10
})

defineEmits<{
  'page-change': [page: number]
  'per-page-change': [perPage: number]
}>()

const totalPages = computed(() => Math.ceil(effectiveTotalItems.value / effectiveItemsPerPage.value))
const startItem = computed(() => (props.currentPage - 1) * effectiveItemsPerPage.value + 1)
const endItem = computed(() => Math.min(props.currentPage * effectiveItemsPerPage.value, effectiveTotalItems.value))

const visiblePages = computed(() => {
  const pages: (number | string)[] = []
  const halfVisible = Math.floor(props.maxVisiblePages / 2)
  
  let startPage = Math.max(1, props.currentPage - halfVisible)
  let endPage = Math.min(totalPages.value, startPage + props.maxVisiblePages - 1)
  
  // Adjust start page if we're near the end
  if (endPage - startPage + 1 < props.maxVisiblePages) {
    startPage = Math.max(1, endPage - props.maxVisiblePages + 1)
  }
  
  // Add first page and ellipsis if needed
  if (startPage > 1) {
    pages.push(1)
    if (startPage > 2) {
      pages.push('...')
    }
  }
  
  // Add visible pages
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i)
  }
  
  // Add last page and ellipsis if needed
  if (endPage < totalPages.value) {
    if (endPage < totalPages.value - 1) {
      pages.push('...')
    }
    pages.push(totalPages.value)
  }
  
  return pages
})
</script>

<style scoped>
/* Add any custom styles if needed */
</style>
