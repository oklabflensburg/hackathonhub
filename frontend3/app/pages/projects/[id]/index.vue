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
          <ProjectDetailMainContent
            :project="project"
            :project-image="projectImage"
            :project-technologies="projectTechnologies"
            :comments="comments"
            :comments-loading="commentsLoading"
            :submitting-comment="submittingComment"
            :comments-error="commentsError"
            :project-comment-count="projectCommentCount"
            :current-user-id="Number(authStore.user?.id)"
            :is-authenticated="authStore.isAuthenticated"
            :format-date="formatDate"
            @add-comment="handleAddComment"
            @update-comment="handleUpdateComment"
            @delete-comment="handleDeleteComment"
            @vote-comment="handleVoteComment"
            @reply-comment="handleReplyComment"
            @retry-comments="fetchComments"
          />
        </template>

        <template #sidebar>
          <ProjectDetailSidebar
            :project="project"
            :can-edit-project="canEditProject"
            @delete-project="deleteProject"
          />
        </template>
      </DetailLayout>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { format } from 'date-fns'
import { useRoute, useRouter } from '#imports'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '~/stores/auth'
import { useVotingStore } from '~/stores/voting'
import { generateProjectPlaceholder } from '~/utils/placeholderImages'
import { resolveImageUrl } from '~/utils/imageUrl'
import { useComments } from '~/composables/useComments'
import ProjectHeader from '~/components/projects/ProjectHeader.vue'
import DetailLayout from '~/components/templates/DetailLayout.vue'
import ProjectDetailMainContent from '~/components/organisms/projects/ProjectDetailMainContent.vue'
import ProjectDetailSidebar from '~/components/organisms/projects/ProjectDetailSidebar.vue'
import LoadingSpinner from '~/components/atoms/LoadingSpinner.vue'

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

const canEditProject = computed(() => Number(authStore.user?.id) === Number(project.value?.user_id))

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
