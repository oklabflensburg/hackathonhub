<template>
  <div class="space-y-8">
    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Hackathons</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">
          Discover and join hackathons from around the world
        </p>
      </div>
      <div class="flex items-center space-x-4">
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search hackathons..."
            class="input pl-10"
          />
          <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <NuxtLink to="/create?tab=hackathon" class="btn btn-primary">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Create Hackathon
        </NuxtLink>
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="flex flex-wrap gap-2 border-b border-gray-200 dark:border-gray-700 pb-4">
      <button
        v-for="filter in filters"
        :key="filter.value"
        @click="activeFilter = filter.value"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors',
          activeFilter === filter.value
            ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400'
            : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
        ]"
      >
        {{ filter.label }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">Loading hackathons...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-6 text-red-400">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.342 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
      </div>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        Failed to load hackathons
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
      <button @click="() => { fetchHackathons(1) }" class="btn btn-primary">
        Try Again
      </button>
    </div>

    <!-- Hackathons Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="hackathon in filteredHackathons"
        :key="hackathon.id"
        class="card-hover group"
      >
        <!-- Hackathon Image -->
        <div class="relative h-48 mb-4 rounded-xl overflow-hidden">
          <img
            :src="hackathon.image"
            :alt="hackathon.name"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <div class="absolute top-4 right-4">
            <span :class="[
              'badge',
              hackathon.status === 'Active' ? 'badge-success' :
              hackathon.status === 'Upcoming' ? 'badge-warning' :
              hackathon.status === 'Completed' ? 'badge-info' : 'badge-primary'
            ]">
              {{ hackathon.status }}
            </span>
          </div>
          <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
            <h3 class="text-xl font-bold text-white">{{ hackathon.name }}</h3>
          </div>
        </div>

        <!-- Hackathon Details -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <div class="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                <span class="text-sm font-medium text-gray-600 dark:text-gray-400">
                  {{ hackathon.organization.charAt(0) }}
                </span>
              </div>
              <span class="text-gray-600 dark:text-gray-400">{{ hackathon.organization }}</span>
            </div>
            <div v-if="hackathon.prize" class="text-right">
              <div class="text-lg font-bold text-gray-900 dark:text-white">{{ hackathon.prize }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Prize Pool</div>
            </div>
          </div>

          <p class="text-gray-600 dark:text-gray-400 text-sm">
            {{ hackathon.description }}
          </p>

          <!-- Stats -->
          <div class="grid grid-cols-3 gap-4 py-4 border-t border-gray-100 dark:border-gray-800">
            <div class="text-center">
              <div class="text-xl font-bold text-gray-900 dark:text-white">{{ hackathon.participants }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">Participants</div>
            </div>
            <div class="text-center">
              <div class="text-xl font-bold text-gray-900 dark:text-white">{{ hackathon.projects }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">Projects</div>
            </div>
            <div class="text-center">
              <div class="text-xl font-bold text-gray-900 dark:text-white">{{ hackathon.duration }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">Duration</div>
            </div>
          </div>

          <!-- Dates -->
          <div class="flex items-center justify-between text-sm">
            <div class="flex items-center text-gray-500 dark:text-gray-400">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {{ hackathon.startDate }} - {{ hackathon.endDate }}
            </div>
            <div class="flex items-center space-x-2">
              <span class="text-gray-500 dark:text-gray-400">
                {{ hackathon.location }}
              </span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-800">
            <div class="flex items-center space-x-2">
              <span v-for="tag in hackathon.tags.slice(0, 2)" :key="tag" class="badge badge-primary text-xs">
                {{ tag }}
              </span>
              <span v-if="hackathon.tags.length > 2" class="text-xs text-gray-500 dark:text-gray-400">
                +{{ hackathon.tags.length - 2 }}
              </span>
            </div>
            <NuxtLink
              :to="`/hackathons/${hackathon.id}`"
              class="btn btn-primary px-4 py-2 text-sm"
            >
              View Details
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!isLoading && !error && filteredHackathons.length === 0" class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-6 text-gray-300 dark:text-gray-600">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      </div>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        No hackathons found
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        Try adjusting your search or filter to find what you're looking for.
      </p>
      <button @click="resetFilters" class="btn btn-primary">
        Reset Filters
      </button>
    </div>

    <!-- Pagination -->
    <div v-if="!isLoading && !error && filteredHackathons.length > 0" class="flex items-center justify-between pt-8 border-t border-gray-200 dark:border-gray-700">
       <div class="text-sm text-gray-600 dark:text-gray-400">
         <template v-if="searchQuery || activeFilter !== 'all'">
           Showing {{ filteredHackathons.length }} of {{ hackathons.length }} loaded hackathons
         </template>
         <template v-else>
           Showing {{ ((currentPage - 1) * pageSize) + 1 }}-{{ Math.min(currentPage * pageSize, totalHackathons) }} of {{ totalHackathons }} hackathons
         </template>
       </div>
       <div class="flex items-center space-x-2">
         <button 
           @click="goToPage(currentPage - 1)"
           :disabled="currentPage === 1"
           class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
         >
           <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
           </svg>
         </button>
         
         <!-- Show page numbers -->
         <template v-for="page in getPageNumbers()" :key="page">
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
         
         <button 
           @click="goToPage(currentPage + 1)"
           :disabled="!hasMore"
           class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
         >
           <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
           </svg>
         </button>
       </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const searchQuery = ref('')
const activeFilter = ref('all')
const hackathons = ref<any[]>([])
const isLoading = ref(true)
const error = ref<string | null>(null)

// Pagination state
const currentPage = ref(1)
const pageSize = ref(9) // Show 9 hackathons per page (3x3 grid)
const totalHackathons = ref(0)
const hasMore = ref(true)

const filters = [
  { label: 'All Hackathons', value: 'all' },
  { label: 'Active', value: 'active' },
  { label: 'Upcoming', value: 'upcoming' },
  { label: 'Completed', value: 'completed' },
  { label: 'Online', value: 'online' },
  { label: 'In-person', value: 'in-person' }
]

// Fetch hackathons from backend API with pagination
const fetchHackathons = async (page: number = 1) => {
  isLoading.value = true
  error.value = null
  try {
    const skip = (page - 1) * pageSize.value
    const limit = pageSize.value
    
    const response = await fetch(`http://localhost:8000/api/hackathons?skip=${skip}&limit=${limit}`)
    if (!response.ok) {
      throw new Error(`Failed to fetch hackathons: ${response.status}`)
    }
    const data = await response.json()
    
    // Check if we got fewer hackathons than requested (end of data)
    if (data.length < pageSize.value) {
      hasMore.value = false
    } else {
      hasMore.value = true
    }
    
    // Transform API data to match frontend format
    const transformedData = data.map((h: any) => {
      const startDate = new Date(h.start_date)
      const endDate = new Date(h.end_date)
      const now = new Date()
      
      // Determine status based on dates and is_active
      let status = 'Upcoming'
      if (h.is_active === false) {
        status = 'Completed'
      } else if (startDate <= now && endDate >= now) {
        status = 'Active'
      } else if (endDate < now) {
        status = 'Completed'
      }
      
      // Format dates for display
      const formatDate = (date: Date) => {
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
      }
      
      // Calculate duration in hours
      const durationMs = endDate.getTime() - startDate.getTime()
      const durationHours = Math.round(durationMs / (1000 * 60 * 60))
      const duration = `${durationHours}h`
      
      // Use organization from API or extract from location
      const organization = h.organization || (h.location.includes('Flensburg') ? 'OK Lab Flensburg' : 'Hackathon Organizer')
      
      // Generate tags based on description
      const tags: string[] = []
      const desc = h.description.toLowerCase()
      if (desc.includes('data') || desc.includes('ai')) tags.push('Data Science')
      if (desc.includes('web') || desc.includes('app')) tags.push('Web Development')
      if (desc.includes('mobile')) tags.push('Mobile')
      if (desc.includes('iot')) tags.push('IoT')
      if (desc.includes('sustainability') || desc.includes('climate')) tags.push('Sustainability')
      if (tags.length === 0) tags.push('General', 'Technology')
      
      return {
        id: h.id,
        name: h.name,
        organization,
        status,
        description: h.description || 'No description available',
        image: h.image_url || 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80',
        prize: h.prize_pool || null, // Use real prize pool from API, null if empty
        participants: h.participant_count ? `${h.participant_count}+` : '0+',
        projects: h.project_count || Math.floor((h.participant_count || 0) / 3) || 0, // Use real project count or estimate
        duration,
        startDate: formatDate(startDate),
        endDate: formatDate(endDate),
        location: h.location,
        tags
      }
    })
    
    // Update hackathons based on page
    if (page === 1) {
      hackathons.value = transformedData
    } else {
      hackathons.value = [...hackathons.value, ...transformedData]
    }
    
    // Update current page
    currentPage.value = page
    
    // Update total count (estimate based on fetched data)
    if (transformedData.length > 0) {
      totalHackathons.value = (page - 1) * pageSize.value + transformedData.length
      if (hasMore.value) {
        totalHackathons.value += pageSize.value // Estimate there are more
      }
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to load hackathons'
    console.error('Error fetching hackathons:', err)
  } finally {
    isLoading.value = false
  }
}

// Function to change pages
const goToPage = (page: number) => {
  if (page < 1) return
  fetchHackathons(page)
}

// Calculate which page numbers to show in pagination
const getPageNumbers = () => {
  const totalPages = Math.ceil(totalHackathons.value / pageSize.value)
  const current = currentPage.value
  const delta = 2 // Number of pages to show on each side of current page
  const range: (number | string)[] = []
  
  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || (i >= current - delta && i <= current + delta)) {
      range.push(i)
    } else if (range[range.length - 1] !== '...') {
      range.push('...')
    }
  }
  
  return range
}

const filteredHackathons = computed(() => {
  let filtered = hackathons.value

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(h =>
      h.name.toLowerCase().includes(query) ||
      h.organization.toLowerCase().includes(query) ||
      h.description.toLowerCase().includes(query) ||
      h.tags.some((tag: string) => tag.toLowerCase().includes(query))
    )
  }

  // Apply status filter
  if (activeFilter.value !== 'all') {
    if (activeFilter.value === 'active') {
      filtered = filtered.filter(h => h.status === 'Active')
    } else if (activeFilter.value === 'upcoming') {
      filtered = filtered.filter(h => h.status === 'Upcoming')
    } else if (activeFilter.value === 'completed') {
      filtered = filtered.filter(h => h.status === 'Completed')
    } else if (activeFilter.value === 'online') {
      filtered = filtered.filter(h => h.location.toLowerCase().includes('online') || h.location.toLowerCase().includes('virtual'))
    } else if (activeFilter.value === 'in-person') {
      filtered = filtered.filter(h => !h.location.toLowerCase().includes('online') && !h.location.toLowerCase().includes('virtual'))
    }
  }

  return filtered
})

const resetFilters = () => {
  searchQuery.value = ''
  activeFilter.value = 'all'
}

// Fetch hackathons on component mount
onMounted(() => {
  fetchHackathons(1)
})
</script>