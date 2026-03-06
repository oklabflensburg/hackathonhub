<template>
  <div class="team-members-panel">
    <div class="panel-header mb-6">
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">
            Team Members
          </h2>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Manage team members and their roles
          </p>
        </div>
        <div class="flex space-x-3">
          <!-- Search Input -->
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-100"
              placeholder="Search members..."
            />
            <div class="absolute left-3 top-1/2 transform -translate-y-1/2">
              <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
          
          <!-- Filter Dropdown -->
          <div class="relative">
            <button
              type="button"
              class="inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
              @click="showFilterDropdown = !showFilterDropdown"
            >
              <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              Filter
            </button>
            
            <!-- Filter Dropdown Menu -->
            <div
              v-if="showFilterDropdown"
              class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg border border-gray-200 dark:border-gray-700 z-10"
            >
              <div class="p-3">
                <div class="space-y-2">
                  <div class="flex items-center">
                    <input
                      id="filter-all"
                      v-model="filterRole"
                      type="radio"
                      value="all"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600"
                    />
                    <label for="filter-all" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
                      All Roles
                    </label>
                  </div>
                  <div class="flex items-center">
                    <input
                      id="filter-owner"
                      v-model="filterRole"
                      type="radio"
                      value="owner"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600"
                    />
                    <label for="filter-owner" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
                      Owners
                    </label>
                  </div>
                  <div class="flex items-center">
                    <input
                      id="filter-admin"
                      v-model="filterRole"
                      type="radio"
                      value="admin"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600"
                    />
                    <label for="filter-admin" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
                      Admins
                    </label>
                  </div>
                  <div class="flex items-center">
                    <input
                      id="filter-member"
                      v-model="filterRole"
                      type="radio"
                      value="member"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600"
                    />
                    <label for="filter-member" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
                      Members
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-state text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">Loading team members...</p>
    </div>
    
    <!-- Content -->
    <div v-else class="panel-content">
      <!-- Stats -->
      <div class="stats-grid grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="stat-item bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
          <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
            {{ stats.total }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Total Members
          </div>
        </div>
        <div class="stat-item bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
          <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
            {{ stats.owners }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Owners
          </div>
        </div>
        <div class="stat-item bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
          <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
            {{ stats.admins }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Admins
          </div>
        </div>
        <div class="stat-item bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
          <div class="stat-value text-2xl font-bold text-gray-900 dark:text-gray-100">
            {{ stats.members }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Members
          </div>
        </div>
      </div>
      
      <!-- Members List -->
      <div class="members-list">
        <div v-if="filteredMembers.length > 0" class="space-y-3">
          <TeamMemberItem
            v-for="member in filteredMembers"
            :key="member.id"
            :member="member"
            :team="team"
            :canManageTeam="canManageTeam"
            @remove="onRemoveMember"
            @promote="onPromoteMember"
            @demote="onDemoteMember"
          />
        </div>
        <div v-else class="empty-state text-center py-12">
          <svg class="h-16 w-16 mx-auto text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="mt-4 text-lg font-medium text-gray-900 dark:text-gray-100">
            No members found
          </h3>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            {{ searchQuery ? 'Try a different search term' : 'Invite members to join your team' }}
          </p>
        </div>
      </div>
      
      <!-- Pagination -->
      <div v-if="filteredMembers.length > 0 && totalPages > 1" class="pagination mt-6 flex justify-between items-center">
        <div class="text-sm text-gray-700 dark:text-gray-300">
          Showing {{ startIndex + 1 }}-{{ Math.min(endIndex, filteredMembers.length) }} of {{ filteredMembers.length }} members
        </div>
        <div class="flex space-x-2">
          <button
            type="button"
            class="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="currentPage === 1"
            @click="prevPage"
          >
            Previous
          </button>
          <div class="flex items-center space-x-1">
            <span
              v-for="page in visiblePages"
              :key="page"
              class="px-3 py-1 rounded-md text-sm font-medium cursor-pointer"
              :class="{
                'bg-primary-600 text-white': page === currentPage,
                'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700': page !== currentPage
              }"
              @click="goToPage(page)"
            >
              {{ page }}
            </span>
            <span v-if="hasMorePages" class="px-2 text-gray-500">...</span>
          </div>
          <button
            type="button"
            class="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="currentPage === totalPages"
            @click="nextPage"
          >
            Next
          </button>
        </div>
      </div>
    </div>
    
    <!-- Remove Member Modal -->
    <div v-if="showRemoveModal" class="fixed inset-0 bg-gray-500 dark:bg-gray-900 bg-opacity-75 dark:bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg max-w-md w-full p-6">
        <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4">
          Remove Member
        </h3>
        <p class="text-gray-700 dark:text-gray-300 mb-6">
          Are you sure you want to remove <strong>{{ selectedMember?.user?.displayName || selectedMember?.user?.username || 'this member' }}</strong> from the team?
        </p>
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
            @click="showRemoveModal = false"
          >
            Cancel
          </button>
          <button
            type="button"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            @click="confirmRemoveMember"
          >
            Remove Member
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import type { Team, TeamMember } from '~/types/team-types'
import TeamMemberItem from '~/components/molecules/teams/TeamMemberItem.vue'

const props = withDefaults(defineProps<{
  team: Team
  members: TeamMember[]
  loading?: boolean
  canManageTeam?: boolean
  itemsPerPage?: number
}>(), {
  members: () => [],
  loading: false,
  canManageTeam: false,
  itemsPerPage: 10,
})

const emit = defineEmits<{
  'remove-member': [memberId: string]
  'promote-member': [memberId: string]
  'demote-member': [memberId: string]
}>()

// UI state
const searchQuery = ref('')
const filterRole = ref('all')
const showFilterDropdown = ref(false)
const showRemoveModal = ref(false)
const currentPage = ref(1)
const selectedMember = ref<TeamMember | null>(null)

// Computed properties
const stats = computed(() => {
  const total = props.members.length
  const owners = props.members.filter(m => m.role === 'owner').length
  const admins = props.members.filter(m => m.role === 'admin').length
  const members = props.members.filter(m => m.role === 'member').length
  const pending = props.members.filter(m => m.role === 'pending').length
  
  return { total, owners, admins, members, pending }
})

const filteredMembers = computed(() => {
  let filtered = [...props.members]
  
  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter(member => {
      const displayName = member.user?.displayName?.toLowerCase() || ''
      const username = member.user?.username?.toLowerCase() || ''
      const email = member.user?.email?.toLowerCase() || ''
      
      return displayName.includes(query) ||
             username.includes(query) ||
             email.includes(query)
    })
  }
  
  // Filter by role
  if (filterRole.value !== 'all') {
    filtered = filtered.filter(member => member.role === filterRole.value)
  }
  
  // Sort: owners first, then admins, then members, then pending
  filtered.sort((a, b) => {
    const roleOrder = { owner: 0, admin: 1, member: 2, pending: 3 }
    return roleOrder[a.role] - roleOrder[b.role]
  })
  
  return filtered
})

const totalPages = computed(() => {
  return Math.ceil(filteredMembers.value.length / props.itemsPerPage)
})

const paginatedMembers = computed(() => {
  const start = (currentPage.value - 1) * props.itemsPerPage
  const end = start + props.itemsPerPage
  return filteredMembers.value.slice(start, end)
})

const startIndex = computed(() => {
  return (currentPage.value - 1) * props.itemsPerPage
})

const endIndex = computed(() => {
  return Math.min(startIndex.value + props.itemsPerPage, filteredMembers.value.length)
})

const visiblePages = computed(() => {
  const pages: number[] = []
  const maxVisible = 5
  
  if (totalPages.value <= maxVisible) {
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i)
    }
  } else {
    let start = Math.max(1, currentPage.value - 2)
    let end = Math.min(totalPages.value, start + maxVisible - 1)
    
    if (end - start + 1 < maxVisible) {
      start = Math.max(1, end - maxVisible + 1)
    }
    
    for (let i = start; i <= end; i++) {
      pages.push(i)
    }
  }
  
  return pages
})

const hasMorePages = computed(() => {
  const lastVisiblePage = visiblePages.value[visiblePages.value.length - 1]
  return lastVisiblePage ? lastVisiblePage < totalPages.value : false
})

// Methods
const onRemoveMember = (memberId: string) => {
  const member = props.members.find(m => m.id === memberId)
  if (member) {
    selectedMember.value = member
    showRemoveModal.value = true
  }
}

const confirmRemoveMember = () => {
  if (selectedMember.value) {
    emit('remove-member', selectedMember.value.id)
    showRemoveModal.value = false
    selectedMember.value = null
  }
}

const onPromoteMember = (memberId: string) => {
  emit('promote-member', memberId)
}

const onDemoteMember = (memberId: string) => {
  emit('demote-member', memberId)
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const goToPage = (page: number) => {
  currentPage.value = page
}

// Reset pagination when filters change
watch([searchQuery, filterRole], () => {
  currentPage.value = 1
})
</script>

<style scoped>
.stats-grid {
  display: grid;
}

.members-list {
  min-height: 300px;
}

.empty-state {
  border: 2px dashed #e5e7eb;
  border-radius: 0.5rem;
}

.dark .empty-state {
  border-color: #4b5563;
}

.pagination span {
  transition: all 0.2s ease;
  cursor: pointer;
}

.pagination span:hover:not(.bg-primary-600) {
  background-color: #f3f4f6;
}

.dark .pagination span:hover:not(.bg-primary-600) {
  background-color: #374151;
}
</style>
