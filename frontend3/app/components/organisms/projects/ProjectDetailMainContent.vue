<template>
  <ProjectImage :src="projectImage" :alt="project.title" :title="project.title" />

  <ProjectDescription :title="t('projects.detail.description')" :description="project.description" />

  <TechnologyTags :technologies="projectTechnologies" :title="t('projects.detail.technologies')" />

  <ProjectLinks
    :title="t('projects.detail.links')"
    :repository-label="t('projects.details.githubRepository')"
    :live-label="t('projects.details.liveDemo')"
    :empty-label="t('projects.detail.noLinksProvided')"
    :repository-url="project.repository_url"
    :live-url="project.live_url"
  />

  <CommentSection
    :title="t('projects.detail.comments')"
    :comments="comments"
    :loading="commentsLoading"
    :submitting="submittingComment"
    :error="commentsError"
    :comment-count="projectCommentCount"
    :current-user-id="currentUserId"
    :is-authenticated="isAuthenticated"
    :format-date="formatDate"
    :add-comment-placeholder="t('projects.comments.addCommentPlaceholder')"
    :post-comment-label="t('projects.comments.postComment')"
    :post-reply-label="t('projects.comments.postReply')"
    :sign-in-to-comment-label="t('projects.comments.signInToComment')"
    :empty-comments-label="t('projects.comments.noCommentsYet')"
    :loading-comments-label="t('projects.comments.loadingComments')"
    :error-comments-label="t('projects.comments.failedLoad')"
    :retry-label="t('projects.comments.retry')"
    :save-label="t('common.save')"
    :comments-count-label="t('projects.comments.countLabel')"
    :delete-confirm-label="t('projects.comments.deleteConfirm')"
    @add="$emit('add-comment', $event)"
    @update="onUpdateComment"
    @remove="onDeleteComment"
    @vote="onVoteComment"
    @reply="onReplyComment"
    @retry="$emit('retry-comments')"
  />
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import type { ProjectComment } from '~/composables/useComments'
import ProjectImage from '~/components/molecules/ProjectImage.vue'
import ProjectDescription from '~/components/molecules/ProjectDescription.vue'
import TechnologyTags from '~/components/projects/TechnologyTags.vue'
import ProjectLinks from '~/components/projects/ProjectLinks.vue'
import CommentSection from '~/components/organisms/comments/CommentSection.vue'

interface ProjectLike {
  title: string
  description: string
  repository_url?: string | null
  live_url?: string | null
}

interface Props {
  project: ProjectLike
  projectImage: string
  projectTechnologies: string[]
  comments: ProjectComment[]
  commentsLoading: boolean
  submittingComment: boolean
  commentsError: string | null
  projectCommentCount: number
  currentUserId?: number
  isAuthenticated: boolean
  formatDate: (value: string) => string
}

defineProps<Props>()

const emit = defineEmits<{
  'add-comment': [content: string]
  'update-comment': [id: number, content: string]
  'delete-comment': [id: number]
  'vote-comment': [id: number, voteType: 'upvote' | 'downvote']
  'reply-comment': [parentId: number, content: string]
  'retry-comments': []
}>()

const { t } = useI18n()

const onUpdateComment = (id: number, content: string) => emit('update-comment', id, content)
const onDeleteComment = (id: number) => emit('delete-comment', id)
const onVoteComment = (id: number, voteType: 'upvote' | 'downvote') => emit('vote-comment', id, voteType)
const onReplyComment = (parentId: number, content: string) => emit('reply-comment', parentId, content)
</script>
