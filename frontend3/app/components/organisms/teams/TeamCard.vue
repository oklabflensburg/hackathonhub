<template>
  <div
    class="team-card bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 border border-gray-200 dark:border-gray-700 overflow-hidden"
    :class="{
      'cursor-pointer': clickable,
      'opacity-75': team.status === 'inactive' || team.status === 'archived'
    }"
    @click="handleClick"
  >
    <!-- Team Banner -->
    <div
      v-if="team.bannerUrl"
      class="team-banner h-32 bg-gradient-to-r from-blue-500 to-purple-600 relative"
    >
      <img
        :src="team.bannerUrl"
        :alt="`${team.name} banner`"
        class="w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-black bg-opacity-20"></div>
    </div>
    <div
      v-else
      class="team-banner h-32 bg-gradient-to-r from-blue-500 to-purple-600"
    ></div>

    <!-- Team Content -->
    <!-- Team Header using TeamCardHeader molecule -->
    <TeamCardHeader
      :team="team"
      :current-user-id="currentUserId"
      :is-member="isCurrentUserMember"
      :is-pending="isCurrentUserPending"
      :show-join-button="showJoinButton"
      :show-more-actions="showMoreActions"
      @join="handleJoin"
      @leave="handleLeave"
      @cancel="handleCancel"
      @more-actions="handleMoreActions"
    />

    <!-- Team Content using TeamCardContent molecule -->
    <TeamCardContent
      :team="team"
      :team-members="teamMembers"
      :show-members-preview="showMembersPreview"
      class="mb-6"
    />

    <div class="p-6">
      <!-- Team Footer using TeamCardFooter molecule -->
      <TeamCardFooter
        :team="team"
        :show-view-count="true"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { Team, TeamMember } from '~/types/team-types'
import TeamCardHeader from '~/components/molecules/teams/TeamCardHeader.vue'
import TeamCardContent from '~/components/molecules/teams/TeamCardContent.vue'
import TeamCardFooter from '~/components/molecules/teams/TeamCardFooter.vue'

interface Props {
  team: Team
  currentUserId?: string | null
  teamMembers?: TeamMember[]
  showJoinButton?: boolean
  showMembersPreview?: boolean
  showMoreActions?: boolean
  clickable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  currentUserId: null,
  teamMembers: () => [],
  showJoinButton: true,
  showMembersPreview: true,
  showMoreActions: true,
  clickable: true
})

interface Emits {
  (e: 'click', team: Team): void
  (e: 'join', team: Team): void
  (e: 'leave', team: Team): void
  (e: 'cancel', team: Team): void
  (e: 'more-actions', team: Team): void
  (e: 'view-team', team: Team): void
}

const emit = defineEmits<Emits>()

const { t } = useI18n()

// Computed properties
const isCurrentUserMember = computed(() => {
  if (!props.currentUserId || !props.teamMembers) return false
  return props.teamMembers.some(member => member.userId === props.currentUserId)
})

const isCurrentUserPending = computed(() => {
  // In a real implementation, we would check pending invitations
  return false
})

const handleClick = () => {
  if (props.clickable) {
    emit('click', props.team)
    emit('view-team', props.team)
  }
}

const handleJoin = () => {
  emit('join', props.team)
}

const handleLeave = () => {
  emit('leave', props.team)
}

const handleCancel = () => {
  emit('cancel', props.team)
}

const handleMoreActions = (event: Event) => {
  event.stopPropagation()
  emit('more-actions', props.team)
}
</script>

<style scoped>
.team-card {
  transition: all 0.3s ease;
}

.team-card:hover {
  transform: translateY(-2px);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>