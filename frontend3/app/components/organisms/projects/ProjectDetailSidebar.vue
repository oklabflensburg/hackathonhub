<template>
  <ProjectStats
    :title="t('projects.detail.projectStats')"
    :upvotes="project.upvote_count || 0"
    :downvotes="project.downvote_count || 0"
    :score="project.vote_score || 0"
    :comments="project.comment_count || 0"
    :views="project.view_count || 0"
    :labels="{
      upvotes: t('projects.detail.upvotes'),
      downvotes: t('projects.detail.downvotes'),
      score: t('projects.detail.totalScore'),
      comments: t('projects.detail.comments'),
      views: t('projects.detail.views')
    }"
  />

  <CreatorInfo :project="project" :title="t('projects.detail.creator')" :subtitle="t('projects.detail.projectCreator')" />

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
import { useI18n } from 'vue-i18n'
import { ProjectStats } from '~/components/molecules'
import CreatorInfo from '~/components/projects/CreatorInfo.vue'
import ProjectActions from '~/components/projects/ProjectActions.vue'

interface Props {
  project: any
  canEditProject: boolean
}

defineProps<Props>()
defineEmits<{ 'delete-project': [] }>()

const { t } = useI18n()
</script>
