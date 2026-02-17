<template>
  <!-- Mobile Bottom Navigation -->
  <nav class="fixed bottom-0 left-0 right-0 z-40 lg:hidden 
              bg-white/95 dark:bg-gray-900/95 backdrop-blur-lg
              border-t border-gray-200 dark:border-gray-800
              shadow-elevated-dark">
    <div class="flex items-center justify-around px-2 py-3">
      <!-- Home -->
      <NuxtLink
        to="/"
        class="flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-200"
        :class="$route.path === '/' 
          ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/30' 
          : 'text-gray-600 dark:text-gray-400 hover:text-primary-500 dark:hover:text-primary-300 hover:bg-gray-50 dark:hover:bg-gray-800'"
      >
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
        <span class="text-xs font-medium">Home</span>
      </NuxtLink>

      <!-- Hackathons -->
      <NuxtLink
        to="/hackathons"
        class="flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-200"
        :class="$route.path.startsWith('/hackathons') 
          ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/30' 
          : 'text-gray-600 dark:text-gray-400 hover:text-primary-500 dark:hover:text-primary-300 hover:bg-gray-50 dark:hover:bg-gray-800'"
      >
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <span class="text-xs font-medium">Hackathons</span>
      </NuxtLink>

      <!-- Projects -->
      <NuxtLink
        to="/projects"
        class="flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-200"
        :class="$route.path.startsWith('/projects') 
          ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/30' 
          : 'text-gray-600 dark:text-gray-400 hover:text-primary-500 dark:hover:text-primary-300 hover:bg-gray-50 dark:hover:bg-gray-800'"
      >
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="text-xs font-medium">Projects</span>
      </NuxtLink>

      <!-- Create (Center with accent) -->
      <NuxtLink
        to="/create"
        class="flex flex-col items-center justify-center p-3 -mt-6 rounded-full 
               bg-gradient-to-br from-primary-500 to-purple-600 
               text-white shadow-lg hover:shadow-xl 
               transition-all duration-200 hover:-translate-y-1"
      >
        <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        <span class="text-xs font-medium mt-1">Create</span>
      </NuxtLink>

      <!-- Profile -->
      <NuxtLink
        to="/profile"
        class="flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-200"
        :class="$route.path.startsWith('/profile') || $route.path.startsWith('/my-') 
          ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/30' 
          : 'text-gray-600 dark:text-gray-400 hover:text-primary-500 dark:hover:text-primary-300 hover:bg-gray-50 dark:hover:bg-gray-800'"
      >
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        <span class="text-xs font-medium">Profile</span>
      </NuxtLink>

      <!-- Search -->
      <button
        @click="toggleSearch"
        class="flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-200 text-gray-600 dark:text-gray-400 hover:text-primary-500 dark:hover:text-primary-300 hover:bg-gray-50 dark:hover:bg-gray-800"
      >
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <span class="text-xs font-medium">Search</span>
      </button>
    </div>
  </nav>

  <!-- Search Modal -->
  <div v-if="showSearch" class="fixed inset-0 z-50 lg:hidden" @click="closeSearch">
    <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeSearch"></div>
    <div class="absolute bottom-20 left-4 right-4 bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-4" @click.stop>
      <div class="flex items-center mb-4">
        <svg class="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          ref="searchInput"
          v-model="searchQuery"
          type="text"
          placeholder="Search hackathons, projects, users..."
          class="flex-1 bg-transparent border-none outline-none text-gray-900 dark:text-white placeholder-gray-500"
          @keyup.enter="performSearch"
        />
        <button @click="closeSearch" class="ml-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="text-sm text-gray-500 dark:text-gray-400 text-center">
        Type and press Enter to search across projects
      </div>
      <div class="mt-3 flex flex-wrap gap-2">
        <button
          @click="searchProjects"
          class="text-xs px-3 py-1.5 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 hover:bg-primary-200 dark:hover:bg-primary-800/50 transition-colors"
        >
          Search Projects
        </button>
        <button
          @click="searchHackathons"
          class="text-xs px-3 py-1.5 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 hover:bg-purple-200 dark:hover:bg-purple-800/50 transition-colors"
        >
          Search Hackathons
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from '#imports'

const router = useRouter()
const showSearch = ref(false)
const searchQuery = ref('')
const searchInput = ref<HTMLInputElement | null>(null)

const toggleSearch = () => {
  showSearch.value = !showSearch.value
  if (showSearch.value) {
    setTimeout(() => {
      searchInput.value?.focus()
    }, 100)
  }
}

const closeSearch = () => {
  showSearch.value = false
  searchQuery.value = ''
}

const performSearch = () => {
  if (searchQuery.value.trim()) {
    // Default to searching projects
    searchProjects()
  }
}

const searchProjects = () => {
  if (searchQuery.value.trim()) {
    router.push(`/projects?q=${encodeURIComponent(searchQuery.value.trim())}`)
    closeSearch()
  }
}

const searchHackathons = () => {
  if (searchQuery.value.trim()) {
    router.push(`/hackathons?q=${encodeURIComponent(searchQuery.value.trim())}`)
    closeSearch()
  }
}

// Close search on escape key
const handleEscape = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && showSearch.value) {
    closeSearch()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleEscape)
})
</script>

<style scoped>
/* Add bottom padding to pages to account for fixed nav */
:global(body) {
  padding-bottom: 5rem !important;
}

@media (min-width: 1024px) {
  :global(body) {
    padding-bottom: 0 !important;
  }
}
</style>