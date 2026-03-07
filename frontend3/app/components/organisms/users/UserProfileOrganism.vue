<template>
  <div class="user-profile" :class="profileClasses">
    <!-- Profile header -->
    <div class="profile-header" :class="headerClasses">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between">
        <div class="flex items-center">
          <!-- Avatar -->
          <div class="relative">
            <div class="profile-avatar" :class="avatarClasses">
              <img
                v-if="avatarUrl"
                :src="avatarUrl"
                :alt="name || 'User avatar'"
                class="w-full h-full object-cover rounded-full"
              />
              <div
                v-else
                class="w-full h-full flex items-center justify-center rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 text-white font-semibold"
              >
                {{ avatarInitials }}
              </div>
              
              <!-- Online status indicator -->
              <div
                v-if="showOnlineStatus"
                class="absolute bottom-0 right-0 w-4 h-4 rounded-full border-2 border-white dark:border-gray-800"
                :class="onlineStatusClasses"
              />
            </div>
            
            <!-- Verification badge -->
            <div
              v-if="verified"
              class="absolute -top-1 -right-1 w-6 h-6 rounded-full bg-blue-500 text-white flex items-center justify-center"
              title="Verified"
            >
              <Icon
                name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' /></svg>"
                :size="12"
                is-svg
              />
            </div>
          </div>
          
          <!-- User info -->
          <div class="ml-4">
            <h2 class="profile-name" :class="nameClasses">
              {{ name }}
              <span v-if="username" class="text-gray-500 dark:text-gray-400 font-normal">
                @{{ username }}
              </span>
            </h2>
            
            <div class="flex items-center mt-1 space-x-4">
              <!-- Role badge -->
              <Badge
                v-if="role"
                :variant="roleVariant"
                size="sm"
              >
                {{ role }}
              </Badge>
              
              <!-- Location -->
              <div v-if="location" class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                <Icon
                  name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z' /><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15 11a3 3 0 11-6 0 3 3 0 016 0z' /></svg>"
                  :size="14"
                  is-svg
                  class="mr-1"
                />
                {{ location }}
              </div>
              
              <!-- Member since -->
              <div v-if="memberSince" class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                <Icon
                  name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' /></svg>"
                  :size="14"
                  is-svg
                  class="mr-1"
                />
                Member since {{ memberSince }}
              </div>
            </div>
            
            <!-- Bio -->
            <p v-if="bio" class="profile-bio mt-3 text-gray-700 dark:text-gray-300">
              {{ bio }}
            </p>
          </div>
        </div>
        
        <!-- Actions -->
        <div class="mt-4 md:mt-0 flex space-x-2">
          <slot name="actions">
            <button
              v-if="showFollowButton"
              type="button"
              class="px-4 py-2 rounded-md font-medium"
              :class="followButtonClasses"
              @click="$emit('follow')"
            >
              {{ isFollowing ? 'Following' : 'Follow' }}
            </button>
            
            <button
              v-if="showMessageButton"
              type="button"
              class="px-4 py-2 rounded-md font-medium border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
              @click="$emit('message')"
            >
              Message
            </button>
            
            <button
              v-if="showMoreButton"
              type="button"
              class="p-2 rounded-md border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
              @click="$emit('more')"
              aria-label="More options"
            >
              <Icon
                name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z' /></svg>"
                :size="16"
                is-svg
              />
            </button>
          </slot>
        </div>
      </div>
    </div>

    <!-- Profile stats -->
    <div v-if="showStats" class="profile-stats" :class="statsClasses">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <!-- Projects stat -->
        <div class="stat-item text-center">
          <div class="stat-value" :class="statValueClasses">
            {{ stats.projects || 0 }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Projects
          </div>
        </div>
        
        <!-- Hackathons stat -->
        <div class="stat-item text-center">
          <div class="stat-value" :class="statValueClasses">
            {{ stats.hackathons || 0 }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Hackathons
          </div>
        </div>
        
        <!-- Followers stat -->
        <div class="stat-item text-center">
          <div class="stat-value" :class="statValueClasses">
            {{ stats.followers || 0 }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Followers
          </div>
        </div>
        
        <!-- Following stat -->
        <div class="stat-item text-center">
          <div class="stat-value" :class="statValueClasses">
            {{ stats.following || 0 }}
          </div>
          <div class="stat-label text-sm text-gray-600 dark:text-gray-400">
            Following
          </div>
        </div>
      </div>
    </div>

    <!-- Profile tabs -->
    <div v-if="showTabs" class="profile-tabs" :class="tabsClasses">
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="-mb-px flex space-x-8">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            class="py-3 px-1 border-b-2 font-medium text-sm"
            :class="getTabClasses(tab)"
            @click="selectTab(tab)"
          >
            {{ tab.label }}
            <span
              v-if="tab.count !== undefined"
              class="ml-2 py-0.5 px-2 text-xs rounded-full"
              :class="tabCountClasses"
            >
              {{ tab.count }}
            </span>
          </button>
        </nav>
      </div>
    </div>

    <!-- Profile content -->
    <div class="profile-content" :class="contentClasses">
      <slot>
        <!-- Default content slot -->
        <div class="p-6 text-center text-gray-500 dark:text-gray-400">
          Profile content goes here
        </div>
      </slot>
      
      <!-- Selected tab content -->
      <div v-if="selectedTab && selectedTab.component" class="mt-6">
        <component :is="selectedTab.component" />
      </div>
    </div>

    <!-- Profile footer -->
    <div v-if="showFooter" class="profile-footer" :class="footerClasses">
      <slot name="footer">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-500 dark:text-gray-400">
            <slot name="footer-left">
              Last updated: {{ lastUpdated }}
            </slot>
          </div>
          
          <div class="flex items-center space-x-2">
            <slot name="footer-right">
              <button
                v-if="showEditProfile"
                type="button"
                class="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
                @click="$emit('edit-profile')"
              >
                Edit Profile
              </button>
            </slot>
          </div>
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import Icon from '../../atoms/Icon.vue'
import Badge from '../../atoms/Badge.vue'

export interface UserProfileTab {
  id: string
  label: string
  count?: number
  component?: any
}

export interface UserProfileStats {
  projects?: number
  hackathons?: number
  followers?: number
  following?: number
  wins?: number
  contributions?: number
}

export interface UserProfileProps {
  /** User's name */
  name: string
  /** User's username/handle */
  username?: string
  /** User's bio/description */
  bio?: string
  /** URL to user's avatar */
  avatarUrl?: string
  /** User's role (e.g., Developer, Designer, Organizer) */
  role?: string
  /** Role variant for badge styling */
  roleVariant?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info' | 'gray'
  /** User's location */
  location?: string
  /** Member since date */
  memberSince?: string
  /** Whether user is verified */
  verified?: boolean
  /** Whether user is online */
  online?: boolean
  /** Whether to show online status indicator */
  showOnlineStatus?: boolean
  /** Whether user is being followed */
  isFollowing?: boolean
  /** User profile stats */
  stats?: UserProfileStats
  /** Profile tabs */
  tabs?: UserProfileTab[]
  /** Whether to show stats section */
  showStats?: boolean
  /** Whether to show tabs section */
  showTabs?: boolean
  /** Whether to show footer */
  showFooter?: boolean
  /** Whether to show follow button */
  showFollowButton?: boolean
  /** Whether to show message button */
  showMessageButton?: boolean
  /** Whether to show more button */
  showMoreButton?: boolean
  /** Whether to show edit profile button */
  showEditProfile?: boolean
  /** Last updated text */
  lastUpdated?: string
  /** Profile variant */
  variant?: 'default' | 'compact' | 'detailed'
  /** Whether profile is loading */
  loading?: boolean
}

const props = withDefaults(defineProps<UserProfileProps>(), {
  roleVariant: 'primary',
  verified: false,
  online: false,
  showOnlineStatus: true,
  isFollowing: false,
  stats: () => ({}),
  tabs: () => [
    { id: 'projects', label: 'Projects', count: 0 },
    { id: 'hackathons', label: 'Hackathons', count: 0 },
    { id: 'teams', label: 'Teams', count: 0 },
    { id: 'activity', label: 'Activity', count: 0 },
  ],
  showStats: true,
  showTabs: true,
  showFooter: false,
  showFollowButton: true,
  showMessageButton: true,
  showMoreButton: true,
  showEditProfile: false,
  lastUpdated: 'Just now',
  variant: 'default',
  loading: false,
})

const emit = defineEmits<{
  /** Emitted when follow button is clicked */
  follow: []
  /** Emitted when message button is clicked */
  message: []
  /** Emitted when more button is clicked */
  more: []
  /** Emitted when edit profile button is clicked */
  'edit-profile': []
  /** Emitted when a tab is selected */
  'tab-selected': [tab: UserProfileTab]
}>()

// Reactive state
const selectedTab = ref<UserProfileTab | null>(props.tabs[0] || null)

// Computed properties
const profileClasses = computed(() => {
  const classes = ['rounded-lg', 'overflow-hidden']
  
  // Variant classes
  const variantClasses = {
    default: 'bg-white dark:bg-gray-800 shadow-sm',
    compact: 'bg-transparent',
    detailed: 'bg-white dark:bg-gray-800 shadow-lg',
  }
  classes.push(variantClasses[props.variant])
  
  return classes
})

const headerClasses = computed(() => {
  const classes = ['p-6']
  
  if (props.variant === 'detailed') {
    classes.push('border-b border-gray-200 dark:border-gray-700')
  }
  
  return classes
})

const avatarClasses = computed(() => {
  const classes = ['relative']
  
  // Size based on variant
  const sizeClasses = {
    default: 'w-20 h-20',
    compact: 'w-16 h-16',
    detailed: 'w-24 h-24',
  }
  classes.push(sizeClasses[props.variant])
  
  return classes
})

const avatarInitials = computed(() => {
  if (!props.name) return '?'
  return props.name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

const onlineStatusClasses = computed(() => {
  return props.online 
    ? 'bg-green-500' 
    : 'bg-gray-400 dark:bg-gray-600'
})

const nameClasses = computed(() => {
  const classes = ['text-xl font-bold']
  
  // Variant classes for name
  const variantClasses = {
    default: 'text-gray-900 dark:text-white',
    compact: 'text-gray-900 dark:text-white',
    detailed: 'text-2xl text-gray-900 dark:text-white',
  }
  classes.push(variantClasses[props.variant])
  
  return classes
})

const followButtonClasses = computed(() => {
  return props.isFollowing
    ? 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600'
    : 'bg-primary-600 text-white hover:bg-primary-700'
})

const statsClasses = computed(() => {
  const classes = ['px-6', 'py-4']
  
  if (props.variant === 'detailed') {
    classes.push('border-b border-gray-200 dark:border-gray-700')
  }
  
  return classes
})

const statValueClasses = computed(() => {
  const classes = ['text-2xl font-bold']
  
  // Variant classes for stat value
  const variantClasses = {
    default: 'text-gray-900 dark:text-white',
    compact: 'text-gray-900 dark:text-white',
    detailed: 'text-3xl text-gray-900 dark:text-white',
  }
  classes.push(variantClasses[props.variant])
  
  return classes
})

const tabsClasses = computed(() => {
  const classes = ['px-6', 'pt-4']
  
  if (props.variant === 'detailed') {
    classes.push('border-b border-gray-200 dark:border-gray-700')
  }
  
  return classes
})

const tabCountClasses = computed(() => {
  return 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
})

const contentClasses = computed(() => {
  return 'p-6'
})

const footerClasses = computed(() => {
  const classes = ['px-6', 'py-4', 'border-t']
  
  // Variant classes for footer
  const variantClasses = {
    default: 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50',
    compact: 'border-gray-200 dark:border-gray-700',
    detailed: 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50',
  }
  classes.push(variantClasses[props.variant])
  
  return classes
})

// Methods
const selectTab = (tab: UserProfileTab) => {
  selectedTab.value = tab
  emit('tab-selected', tab)
}

const getTabClasses = (tab: UserProfileTab) => {
  const isActive = selectedTab.value?.id === tab.id
  return {
    'border-primary-500 text-primary-600 dark:text-primary-400': isActive,
    'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300': !isActive,
  }
}
</script>

<style scoped>
.user-profile {
  transition: all 0.2s ease-in-out;
}

.profile-avatar {
  transition: transform 0.2s ease;
}

.profile-avatar:hover {
  transform: scale(1.05);
}

.profile-name {
  line-height: 1.2;
}

.profile-bio {
  line-height: 1.6;
}

.stat-item {
  transition: all 0.2s ease;
}

.stat-item:hover .stat-value {
  color: var(--primary-600);
}

.stat-value {
  transition: color 0.2s ease;
}

.stat-label {
  transition: color 0.2s ease;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .profile-header {
    padding: 1rem;
  }
  
  .profile-stats {
    padding: 1rem;
  }
  
  .profile-tabs {
    padding: 0 1rem;
  }
  
  .profile-content {
    padding: 1rem;
  }
  
  .profile-footer {
    padding: 1rem;
  }
}

@media (max-width: 640px) {
  .profile-header .flex {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .profile-header .flex > div:first-child {
    width: 100%;
  }
  
  .profile-header .mt-4 {
    margin-top: 1rem;
    width: 100%;
  }
  
  .profile-stats .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
