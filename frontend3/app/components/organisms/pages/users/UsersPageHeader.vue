<template>
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
    <div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ title }}</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">{{ subtitle }}</p>
    </div>
    <div class="flex items-center space-x-4">
      <div class="relative">
        <input :value="searchQuery" @input="onSearchInput" type="text" :placeholder="searchPlaceholder" class="input pl-10" />
      </div>
      <select :value="sortBy" @change="onSortChange" class="input">
        <option value="newest">{{ newestLabel }}</option>
        <option value="name">{{ nameLabel }}</option>
        <option value="activity">{{ activityLabel }}</option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  subtitle: string
  searchQuery: string
  sortBy: string
  searchPlaceholder: string
  newestLabel: string
  nameLabel: string
  activityLabel: string
}>()

const emit = defineEmits<{ (e:'update:searchQuery', value:string):void; (e:'update:sortBy', value:string):void }>()

const onSearchInput = (event: Event) => {
  emit('update:searchQuery', (event.target as HTMLInputElement).value)
}

const onSortChange = (event: Event) => {
  emit('update:sortBy', (event.target as HTMLSelectElement).value)
}
</script>
