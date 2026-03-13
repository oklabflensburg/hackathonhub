<template>
  <div :class="containerClasses" :title="tooltipText" aria-label="Team member avatar">
    <!-- Avatar image -->
    <img
      v-if="avatarUrl"
      :src="avatarUrl"
      :alt="displayName || 'Team member'"
      :class="avatarClasses"
      @error="handleImageError"
    />
    
    <!-- Fallback avatar with initials -->
    <div
      v-else
      :class="fallbackClasses"
      :style="fallbackStyle"
    >
      {{ initials }}
    </div>
    
    <!-- Member name (if shown) -->
    <div v-if="showName" :class="nameClasses">
      {{ displayName || username }}
      <span v-if="showRole && memberRole" :class="roleClasses">
        {{ roleLabel }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { TeamMemberAvatarProps } from '~/types/team-types'
import { TeamRole, getTeamRoleColor } from '~/types/team-types'

const props = withDefaults(defineProps<TeamMemberAvatarProps>(), {
  size: 'md',
  showName: false,
  showRole: false
})

// Reactive state for image loading errors
const imageError = ref(false)

// Extract member information
const memberInfo = computed(() => {
  if ('userId' in props.member) {
    // TeamMember type
    return {
      id: props.member.userId,
      username: props.member.user?.username || 'user',
      displayName: props.member.user?.displayName || props.member.user?.display_name || props.member.user?.username || 'User',
      avatarUrl: props.member.user?.avatarUrl || props.member.user?.avatar_url || null,
      role: props.member.role
    }
  } else {
    // TeamMemberUser type
    return {
      id: String(props.member.id),
      username: props.member.username || 'user',
      displayName: props.member.displayName || props.member.display_name || props.member.username || 'User',
      avatarUrl: props.member.avatarUrl || props.member.avatar_url || null,
      role: TeamRole.MEMBER
    }
  }
})

// Size classes mapping
const sizeClasses = {
  xs: {
    container: 'flex items-center space-x-1',
    avatar: 'w-6 h-6',
    fallback: 'w-6 h-6 text-xs',
    name: 'text-xs'
  },
  sm: {
    container: 'flex items-center space-x-2',
    avatar: 'w-8 h-8',
    fallback: 'w-8 h-8 text-sm',
    name: 'text-sm'
  },
  md: {
    container: 'flex items-center space-x-3',
    avatar: 'w-10 h-10',
    fallback: 'w-10 h-10 text-base',
    name: 'text-base'
  },
  lg: {
    container: 'flex items-center space-x-4',
    avatar: 'w-12 h-12',
    fallback: 'w-12 h-12 text-lg',
    name: 'text-lg'
  },
  xl: {
    container: 'flex items-center space-x-4',
    avatar: 'w-16 h-16',
    fallback: 'w-16 h-16 text-xl',
    name: 'text-xl'
  }
} as const

// Role label mapping
const roleLabels = {
  [TeamRole.OWNER]: 'Owner',
  [TeamRole.ADMIN]: 'Admin',
  [TeamRole.MEMBER]: 'Member',
  [TeamRole.PENDING]: 'Pending'
} as const

// Role color classes
const roleColorClasses = {
  red: 'text-red-600 dark:text-red-400',
  orange: 'text-orange-600 dark:text-orange-400',
  green: 'text-green-600 dark:text-green-400',
  gray: 'text-gray-500 dark:text-gray-400'
} as const

// Computed properties
const avatarUrl = computed(() => imageError.value ? null : memberInfo.value.avatarUrl)
const displayName = computed(() => memberInfo.value.displayName)
const username = computed(() => memberInfo.value.username)
const memberRole = computed(() => memberInfo.value.role)
const roleLabel = computed(() => roleLabels[memberRole.value] || 'Member')
const roleColor = computed(() => getTeamRoleColor(memberRole.value))

// Generate initials from display name
const initials = computed(() => {
  const name = displayName.value || username.value
  return name
    .split(' ')
    .map(part => part.charAt(0).toUpperCase())
    .slice(0, 2)
    .join('')
})

// Generate fallback background color based on user ID
const fallbackColor = computed(() => {
  const colors = [
    'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200',
    'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200',
    'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  ]
  
  // Simple hash based on user ID for consistent color
  const id = memberInfo.value.id
  let hash = 0
  for (let i = 0; i < id.length; i++) {
    hash = id.charCodeAt(i) + ((hash << 5) - hash)
  }
  
  const index = Math.abs(hash) % colors.length
  return colors[index]
})

const tooltipText = computed(() => {
  const base = `${displayName.value} (${username.value})`
  return props.showRole ? `${base} - ${roleLabel.value}` : base
})

// CSS classes
const containerClasses = computed(() => [
  sizeClasses[props.size].container,
  'transition-opacity duration-200 hover:opacity-90'
])

const avatarClasses = computed(() => [
  sizeClasses[props.size].avatar,
  'rounded-full object-cover border-2 border-white dark:border-gray-800 shadow-sm'
])

const fallbackClasses = computed(() => [
  sizeClasses[props.size].fallback,
  fallbackColor.value,
  'rounded-full flex items-center justify-center font-medium border-2 border-white dark:border-gray-800 shadow-sm'
])

const fallbackStyle = computed(() => ({
  lineHeight: '1'
}))

const nameClasses = computed(() => [
  sizeClasses[props.size].name,
  'font-medium text-gray-900 dark:text-gray-100'
])

const roleClasses = computed(() => [
  'ml-2 text-xs font-normal',
  roleColorClasses[roleColor.value]
])

// Event handlers
const handleImageError = () => {
  imageError.value = true
}
</script>

<style scoped>
/* Additional styles if needed */
</style>
