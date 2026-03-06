<template>
  <div class="team-card-header" :class="headerClasses">
    <!-- Link Wrapper (if clickable) -->
    <component
      :is="clickable ? 'a' : 'div'"
      v-if="clickable"
      :href="teamLink"
      class="header-link"
      :aria-label="`View team: ${team.name}`"
      @click="handleClick"
    >
      <slot name="before-title" />
      
      <!-- Team Title -->
      <h3 class="team-title" :class="titleClasses">
        <span class="title-text">
          {{ team.name }}
        </span>
        
        <!-- Status Badge -->
        <TeamBadge
          v-if="showStatus"
          :status="team.status"
          :size="statusSize"
          :show-label="showStatusLabel"
          class="ml-2"
        />
        
        <!-- Visibility Badge -->
        <TeamVisibilityBadge
          v-if="showVisibility"
          :visibility="team.visibility"
          :size="visibilitySize"
          :show-label="showVisibilityLabel"
          class="ml-2"
        />
      </h3>
      
      <slot name="after-title" />
    </component>
    
    <!-- Non-clickable Version -->
    <template v-else>
      <slot name="before-title" />
      
      <!-- Team Title -->
      <h3 class="team-title" :class="titleClasses">
        <span class="title-text">
          {{ team.name }}
        </span>
        
        <!-- Status Badge -->
        <TeamBadge
          v-if="showStatus"
          :status="team.status"
          :size="statusSize"
          :show-label="showStatusLabel"
          class="ml-2"
        />
        
        <!-- Visibility Badge -->
        <TeamVisibilityBadge
          v-if="showVisibility"
          :visibility="team.visibility"
          :size="visibilitySize"
          :show-label="showVisibilityLabel"
          class="ml-2"
        />
      </h3>
      
      <slot name="after-title" />
    </template>
    
    <!-- Actions (if showActions is true) -->
    <div v-if="showActions && !compact" class="team-actions">
      <slot name="actions">
        <!-- Default actions slot -->
        <TeamInviteButton
          v-if="showInviteButton"
          :team="team"
          :size="actionButtonSize"
          variant="outline"
          class="mr-2"
          @invite="handleInvite"
        />
        
        <TeamSettingsButton
          v-if="showSettingsButton"
          :team="team"
          :size="actionButtonSize"
          variant="ghost"
          @settings="handleSettings"
        />
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { TeamCardHeaderProps } from '~/types/team-types'
import TeamBadge from '~/components/atoms/teams/TeamBadge.vue'
import TeamVisibilityBadge from '~/components/atoms/teams/TeamVisibilityBadge.vue'
import TeamInviteButton from '~/components/atoms/teams/TeamInviteButton.vue'
import TeamSettingsButton from '~/components/atoms/teams/TeamSettingsButton.vue'

const props = withDefaults(defineProps<TeamCardHeaderProps & {
  clickable?: boolean
  showStatus?: boolean
  showVisibility?: boolean
  showStatusLabel?: boolean
  showVisibilityLabel?: boolean
  showInviteButton?: boolean
  showSettingsButton?: boolean
  statusSize?: 'sm' | 'md' | 'lg'
  visibilitySize?: 'sm' | 'md' | 'lg'
  actionButtonSize?: 'sm' | 'md' | 'lg' | 'xl'
}>(), {
  showActions: true,
  compact: false,
  clickable: true,
  showStatus: true,
  showVisibility: true,
  showStatusLabel: true,
  showVisibilityLabel: true,
  showInviteButton: true,
  showSettingsButton: true,
  statusSize: 'sm',
  visibilitySize: 'sm',
  actionButtonSize: 'sm'
})

const emit = defineEmits<{
  click: [event: MouseEvent]
  invite: [teamId: string]
  settings: [teamId: string]
}>()

// Computed properties
const teamLink = computed(() => `/teams/${props.team.id}`)

const headerClasses = computed(() => [
  'flex items-start justify-between',
  props.compact ? 'p-3' : 'p-4',
  props.clickable ? 'cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200' : ''
])

const titleClasses = computed(() => [
  'text-lg font-semibold text-gray-900 dark:text-white flex items-center',
  props.compact ? 'text-base' : 'text-lg'
])

// Event handlers
const handleClick = (event: MouseEvent) => {
  if (!props.clickable) return
  emit('click', event)
}

const handleInvite = (teamId: string) => {
  emit('invite', teamId)
}

const handleSettings = (teamId: string) => {
  emit('settings', teamId)
}
</script>

<style scoped>
.team-card-header {
  border-bottom: 1px solid #e5e7eb;
}

.dark .team-card-header {
  border-bottom-color: #374151;
}

.header-link {
  display: block;
  text-decoration: none;
  color: inherit;
  flex-grow: 1;
}

.team-title {
  margin: 0;
  line-height: 1.4;
}

.title-text {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.team-actions {
  display: flex;
  align-items: center;
  margin-left: auto;
  padding-left: 1rem;
}
</style>