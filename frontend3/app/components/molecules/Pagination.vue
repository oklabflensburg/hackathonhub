<template>
  <div class="flex items-center justify-between gap-2">
    <Button variant="secondary" size="sm" :disabled="currentPage <= 1" @click="changePage(currentPage - 1)">Prev</Button>
    <div class="hidden sm:flex items-center gap-2">
      <button
        v-for="page in pages"
        :key="page"
        class="px-3 py-1 rounded-md text-sm"
        :class="page === currentPage ? 'bg-primary-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200'"
        @click="changePage(page)"
      >
        {{ page }}
      </button>
    </div>
    <Button variant="secondary" size="sm" :disabled="currentPage >= totalPages" @click="changePage(currentPage + 1)">Next</Button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Button from '~/components/atoms/Button.vue'

interface Props {
  total: number
  perPage?: number
  currentPage?: number
}

const props = withDefaults(defineProps<Props>(), {
  perPage: 10,
  currentPage: 1,
})

const emit = defineEmits<{ 'page-change': [page: number] }>()

const totalPages = computed(() => Math.max(1, Math.ceil(props.total / props.perPage)))
const pages = computed(() => Array.from({ length: totalPages.value }, (_, i) => i + 1))

const changePage = (page: number) => {
  if (page < 1 || page > totalPages.value || page === props.currentPage) {
    return
  }

  emit('page-change', page)
}
</script>
