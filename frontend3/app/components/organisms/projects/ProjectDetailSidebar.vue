<template>
  <ProjectStats
    :title="t('projects.detail.projectStats')"
    :stats="stats"
  />

  <CreatorInfo :project="project" :title="t('projects.detail.creator')" :subtitle="t('projects.detail.projectCreator')" />

  <div class="space-y-3">
    <button class="w-full btn btn-outline" @click="$emit('report-project')">Report Project</button>
    <NuxtLink v-if="canViewReports" :to="`/projects/${project.id}/reports`" class="w-full btn btn-outline text-center">Project Reports</NuxtLink>
  </div>

  <ProjectActions
    :project="project"
    :can-edit="canEditProject"
    :title="t('projects.detail.actions')"
    :edit-label="t('projects.detail.editProject')"
    :delete-label="t('projects.detail.deleteProject')"
    :view-hackathon-label="t('projects.detail.viewHackathon')"
    :view-team-label="t('projects.detail.viewTeam')"
    :back-label="t('projects.detail.backToProjects')"
    @delete="$emit('delete-project')"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { ProjectStats } from '~/components/molecules'
import CreatorInfo from '~/components/organisms/pages/projects/CreatorInfo.vue'
import ProjectActions from '~/components/organisms/pages/projects/ProjectActions.vue'

interface Props {
  project: any
  canEditProject: boolean
  canViewReports?: boolean
}

const props = defineProps<Props>()
defineEmits<{ 'delete-project': []; 'report-project': [] }>()

const { t } = useI18n()

const stats = computed(() => ({
  votes: props.project.total_votes ?? ((props.project.upvote_count || 0) + (props.project.downvote_count || 0)),
  voteChange: 0, // Not available from API
  comments: props.project.total_comments ?? (props.project.comment_count || 0),
  views: props.project.view_count || 0,
  shares: 0, // Not available
  engagementRate: props.project.engagement_rate ?? 0,
  lastActivityAt: props.project.last_activity_at,
  createdAt: props.project.created_at || props.project.createdAt || new Date().toISOString(),
  updatedAt: props.project.updated_at || props.project.updatedAt,
  status: 'published' as const // Match the expected type
}))
</script>
