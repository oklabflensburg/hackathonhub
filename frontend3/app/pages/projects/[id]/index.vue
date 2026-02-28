<template>
  <div class="py-8">
    <div v-if="loading" class="flex justify-center py-12">
      <LoadingSpinner size="lg" />
    </div>

    <div v-else-if="error" class="text-center py-16">
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">{{ t('projects.details.notFoundTitle') }}</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
      <NuxtLink to="/projects" class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
        {{ t('projects.details.backToProjects') }}
      </NuxtLink>
    </div>

    <div v-else-if="project" class="max-w-6xl mx-auto px-0 sm:px-2 md:px-4 lg:px-6">
      <ProjectHeader :project="project" :show-voting="authStore.isAuthenticated" :format-date="formatDate" />

      <DetailLayout>
        <template #main>
          <div class="space-y-8">
            <ProjectImage
              :src="projectImage"
              :alt="project.title"
              :title="project.title"
            />

            <ProjectDescription
              :title="t('projects.detail.description')"
              :description="project.description"
            />

            <TechnologyTags :technologies="projectTechnologies" :title="t('projects.detail.technologies')" />

            <ProjectLinks
              :title="t('projects.detail.links')"
              :repository-label="t('projects.details.githubRepository')"
              :live-label="t('projects.details.liveDemo')"
              :empty-label="'No links provided for this project'"
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
              :current-user-id="Number(authStore.user?.id)"
              :is-authenticated="authStore.isAuthenticated"
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
              @add="handleAddComment"
              @update="handleUpdateComment"
              @remove="handleDeleteComment"
              @vote="handleVoteComment"
              @reply="handleReplyComment"
              @retry="fetchComments"
            />
          </div>
        </template>

        <template #sidebar>
          <div class="space-y-6">
            <ProjectDetailSidebar
              :project="project"
              :can-edit-project="canEditProject"
              @delete-project="deleteProject"
            />
          </div>
        </template>
      </DetailLayout>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { format } from 'date-fns'
import { useRoute, useRouter } from '#imports'
import { useAuthStore } from '~/stores/auth'
import { useVotingStore } from '~/stores/voting'
import { generateProjectPlaceholder } from '~/utils/placeholderImages'
import { resolveImageUrl } from '~/utils/imageUrl'
import { useComments } from '~/composables/useComments'
import { ProjectHeader, TechnologyTags, ProjectLinks, ProjectImage, ProjectDescription } from '~/components/molecules'
import CommentSection from '~/components/organisms/comments/CommentSection.vue'
import LoadingSpinner from '~/components/atoms/LoadingSpinner.vue'
import DetailLayout from '~/components/templates/DetailLayout.vue'
import ProjectDetailSidebar from '~/components/organisms/projects/ProjectDetailSidebar.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const votingStore = useVotingStore()
const { t } = useI18n()

const loading = ref(true)
const error = ref<string | null>(null)
const project = ref<any>(null)

const projectId = computed(() => Number(route.params.id))
const projectCommentCount = ref(0)

const {
  comments,
  loading: commentsLoading,
  submitting: submittingComment,
  error: commentsError,
  fetchComments,
  postComment,
  updateComment,
  deleteComment,
  voteComment,
} = useComments(projectId, projectCommentCount)

const projectTechnologies = computed(() => (project.value?.technologies || '').split(',').map((tech: string) => tech.trim()).filter(Boolean))

const projectImage = computed(() => {
  if (!project.value?.image_path) {
    return generateProjectPlaceholder({
      id: project.value?.id || 0,
      title: project.value?.title || 'Project',
    })
  }

  return resolveImageUrl(project.value.image_path, useRuntimeConfig().public.apiUrl || 'http://localhost:8000')
})

const canEditProject = computed(() => Number(authStore.user?.id) === Number(project.value?.owner_id))

const formatDate = (value: string) => {
  try {
    return format(new Date(value), 'MMM d, yyyy')
  } catch {
    return value
  }
}

const fetchProject = async () => {
  try {
    loading.value = true
    const backendUrl = useRuntimeConfig().public.apiUrl || 'http://localhost:8000'

    await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId.value}/view`, { method: 'POST' })

    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId.value}`)

    if (!response.ok) {
      error.value = response.status === 404 ? 'Project not found' : `Failed to load project: ${response.status}`
      return
    }

    project.value = await response.json()
    projectCommentCount.value = project.value?.comment_count || 0
    await votingStore.getProjectVoteStats(projectId.value)
  } catch (err) {
    console.error('Error fetching project:', err)
    error.value = 'Failed to load project details'
  } finally {
    loading.value = false
  }
}

const handleAddComment = async (content: string) => {
  await postComment(content)
}

const handleReplyComment = async (parentId: number, content: string) => {
  await postComment(content, parentId)
}

const handleUpdateComment = async (commentId: number, content: string) => {
  await updateComment(commentId, content)
}

const handleDeleteComment = async (commentId: number) => {
  await deleteComment(commentId)
}

const handleVoteComment = async (commentId: number, voteType: 'upvote' | 'downvote') => {
  await voteComment(commentId, voteType)
}

const deleteProject = async () => {
  if (!confirm(t('projects.delete.confirm', { title: project.value?.title || 'this project' }))) return

  try {
    const backendUrl = useRuntimeConfig().public.apiUrl || 'http://localhost:8000'
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId.value}`, {
      method: 'DELETE',
    })

    if (response.ok) {
      router.push('/projects')
    }
  } catch (err) {
    console.error('Error deleting project:', err)
  }
}

onMounted(async () => {
  await fetchProject()
  await fetchComments()
})
</script>
