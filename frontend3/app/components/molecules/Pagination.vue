<template>
  <div class="flex items-center justify-between gap-4">
    <!-- Showing info (optional) -->
    <div v-if="showInfo" class="text-sm text-gray-600 dark:text-gray-400">
      <slot name="info" :start="startItem" :end="endItem" :total="total">
        {{ $t('pagination.showing') }} {{ startItem }}-{{ endItem }} {{ $t('pagination.of') }} {{ total }}
      </slot>
    </div>

    <!-- Pagination controls -->
    <div class="flex items-center space-x-2">
      <!-- Previous button -->
      <button
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage <= 1"
        class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
        :aria-label="$t('pagination.previous')"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      <!-- Page numbers with ellipsis -->
      <template v-for="page in pageNumbers" :key="page">
        <button
          v-if="page === '...'"
          disabled
          class="px-3 py-1 rounded-lg text-gray-400"
        >
          ...
        </button>
        <button
          v-else
          @click="goToPage(page as number)"
          :class="[
            'px-3 py-1 rounded-lg',
            currentPage === page
              ? 'bg-primary-600 text-white'
              : 'hover:bg-gray-100 dark:hover:bg-gray-800'
          ]"
        >
          {{ page }}
        </button>
      </template>

      <!-- Next button -->
      <button
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage >= totalPages"
        class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
        :aria-label="$t('pagination.next')"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  total: number
  perPage?: number
  currentPage?: number
  showInfo?: boolean
  maxVisiblePages?: number
}

const props = withDefaults(defineProps<Props>(), {
  perPage: 10,
  currentPage: 1,
  showInfo: false,
  maxVisiblePages: 5
})

const emit = defineEmits<{ 'page-change': [page: number] }>()

const totalPages = computed(() => Math.max(1, Math.ceil(props.total / props.perPage)))

const startItem = computed(() => ((props.currentPage - 1) * props.perPage) + 1)
const endItem = computed(() => Math.min(props.currentPage * props.perPage, props.total))

// Generate page numbers with ellipsis logic
const pageNumbers = computed(() => {
  const current = props.currentPage
  const total = totalPages.value
  const maxVisible = props.maxVisiblePages
  const pages: (number | string)[] = []

  if (total <= maxVisible) {
    // Show all pages
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    // Always include first page
    pages.push(1)

    // Calculate start and end of visible range
    let start = Math.max(2, current - Math.floor(maxVisible / 2))
    let end = Math.min(total - 1, start + maxVisible - 3)

    // Adjust if we're near the end
    if (end === total - 1) {
      start = total - maxVisible + 2
    }

    // Add ellipsis after first page if needed
    if (start > 2) pages.push('...')

    // Add visible pages
    for (let i = start; i <= end; i++) pages.push(i)

    // Add ellipsis before last page if needed
    if (end < total - 1) pages.push('...')

    // Always include last page
    if (total > 1) pages.push(total)
  }

  return pages
})

const goToPage = (page: number) => {
  if (page < 1 || page > totalPages.value || page === props.currentPage) return
  emit('page-change', page)
}
</script>
