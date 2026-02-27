<template>
  <div class="py-8">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-16">
      <svg class="w-24 h-24 text-red-400 mx-auto mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">{{ t('projects.details.notFoundTitle') }}
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
      <NuxtLink to="/projects"
        class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        {{ t('projects.details.backToProjects') }}
      </NuxtLink>
    </div>

    <!-- Project Details -->
    <div v-else-if="project" class="max-w-6xl mx-auto px-0 sm:px-2 md:px-4 lg:px-6">
      <ProjectHeader
        :project="project"
        :show-voting="authStore.isAuthenticated"
        :format-date="formatDate"
      />

      <!-- Project Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Project Image -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden aspect-ratio-16-9">
            <img :src="projectImage" :alt="project.title" class="img-cover" />
          </div>

          <!-- Description -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">{{ t('projects.detail.description') }}</h2>
            <div class="prose dark:prose-invert max-w-none">
              <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line">{{ project.description }}</p>
            </div>
          </div>
          <TechnologyTags
            :technologies="projectTechnologies"
            :title="t('projects.detail.technologies')"
          />
          <ProjectLinks
            :title="t('projects.detail.links')"
            :repository-label="t('projects.details.githubRepository')"
            :live-label="t('projects.details.liveDemo')"
            :empty-label="'No links provided for this project'"
            :repository-url="project.repository_url"
            :live-url="project.live_url"
          />

          <!-- Comments Section -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ t('projects.detail.comments') }}</h2>
              <span
                class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-sm">
                {{ project.comment_count || 0 }} comments
              </span>
            </div>

            <!-- Add Comment Form (for authenticated users) -->
            <div v-if="authStore.isAuthenticated" class="mb-8">
              <textarea v-model="newComment" :placeholder="$t('projects.comments.addCommentPlaceholder')" rows="3"
                class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                :disabled="commentLoading"></textarea>
              <div class="flex justify-end mt-3">
                <button @click="submitComment" :disabled="commentLoading || !newComment.trim()"
                  class="btn btn-primary px-6 disabled:opacity-50 disabled:cursor-not-allowed">
                  <svg v-if="commentLoading" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                    <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  <span v-else>{{ t('projects.comments.postComment') }}</span>
                </button>
              </div>
            </div>
            <div v-else class="mb-8 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg text-center">
              <p class="text-gray-600 dark:text-gray-400">
                {{ t('projects.comments.signInToComment') }}
              </p>
            </div>

            <!-- Comments List -->
            <div v-if="commentsLoading" class="text-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
              <p class="mt-2 text-gray-600 dark:text-gray-400">Loading comments...</p>
            </div>
            <div v-else-if="comments.length === 0" class="text-center py-8">
              <svg class="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor"
                viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <p class="text-gray-500 dark:text-gray-400">{{ t('projects.comments.noCommentsYet') }}</p>
            </div>
            <div v-else class="space-y-6">
              <div v-for="comment in comments" :key="comment.id"
                class="border-b border-gray-200 dark:border-gray-700 pb-6 last:border-0">
                <div class="flex items-start space-x-3">
                  <!-- User Avatar -->
                  <NuxtLink :to="'/profile'"
                    class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center flex-shrink-0 overflow-hidden hover:opacity-90 transition-opacity">
                    <img v-if="comment.user?.avatar_url" :src="comment.user.avatar_url" :alt="comment.user.name"
                      class="w-full h-full object-cover" />
                    <span v-else class="text-sm font-medium text-gray-700 dark:text-gray-300">
                      {{ comment.user?.name?.charAt(0)?.toUpperCase() || 'U' }}
                    </span>
                  </NuxtLink>

                  <!-- Comment Content -->
                  <div class="flex-1">
                    <div v-if="editingCommentId !== comment.id">
                      <div class="flex items-center justify-between mb-2">
                        <div>
                          <span class="font-medium text-gray-900 dark:text-white">{{ comment.user?.name || 'Anonymous'
                            }}</span>
                          <span class="text-sm text-gray-500 dark:text-gray-400 ml-3">{{ formatDate(comment.created_at)
                            }}</span>
                        </div>
                        <div v-if="authStore.user?.id === comment.user_id" class="flex items-center space-x-2">
                          <button @click="editComment(comment)"
                            class="text-sm text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400">
                            Edit
                          </button>
                          <button @click="deleteComment(comment.id)"
                            class="text-sm text-red-500 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300">
                            Delete
                          </button>
                        </div>
                      </div>
                      <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line">{{ comment.content }}</p>

                      <!-- Comment Actions -->
                      <div class="flex items-center space-x-4 mt-3">
                        <button @click="voteComment(comment.id, 'upvote')"
                          class="flex items-center space-x-1 text-sm text-gray-500 dark:text-gray-400 hover:text-green-600 dark:hover:text-green-400">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                          </svg>
                          <span>{{ comment.upvote_count || 0 }}</span>
                        </button>
                        <button @click="voteComment(comment.id, 'downvote')"
                          class="flex items-center space-x-1 text-sm text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                          </svg>
                          <span>{{ comment.downvote_count || 0 }}</span>
                        </button>
                        <button @click="startReply(comment.id)"
                          class="text-sm text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400">
                          Reply
                        </button>
                      </div>

                      <!-- Reply Form -->
                      <div v-if="replyingToCommentId === comment.id"
                        class="mt-4 ml-6 border-l-2 border-gray-200 dark:border-gray-700 pl-4">
                        <textarea v-model="replyContent" rows="2"
                          :placeholder="$t('projects.comments.writeReplyPlaceholder')"
                          class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                          :disabled="replyLoading"></textarea>
                        <div class="flex justify-end space-x-2 mt-2">
                          <button @click="cancelReply"
                            class="px-4 py-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-300"
                            :disabled="replyLoading">
                            Cancel
                          </button>
                          <button @click="submitReply(comment.id)"
                            class="px-4 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
                            :disabled="replyLoading || !replyContent.trim()">
                            <span v-if="replyLoading">{{ t('projects.comments.posting') }}</span>
                            <span v-else>{{ t('projects.comments.postReply') }}</span>
                          </button>
                        </div>
                      </div>
                    </div>

                    <!-- Edit Form (shown when editingCommentId === comment.id) -->
                    <div v-else>
                      <div class="flex items-center justify-between mb-2">
                        <div>
                          <NuxtLink :to="'/profile'"
                            class="font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                            {{ comment.user?.name || 'Anonymous' }}
                          </NuxtLink>
                          <span class="text-sm text-gray-500 dark:text-gray-400 ml-3">{{ formatDate(comment.created_at)
                            }}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                          <button @click="saveComment(comment.id)"
                            class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300">
                            Save
                          </button>
                          <button @click="cancelEdit"
                            class="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300">
                            Cancel
                          </button>
                        </div>
                      </div>
                      <textarea v-model="editingContent" rows="3"
                        class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"></textarea>
                    </div>

                    <!-- Replies Section (only shown when not editing) -->
                    <div v-if="editingCommentId !== comment.id && comment.replies && comment.replies.length > 0"
                      class="mt-4 ml-6 space-y-4 border-l-2 border-gray-200 dark:border-gray-700 pl-4">
                      <div v-for="reply in comment.replies" :key="reply.id" class="pt-4 first:pt-0">
                        <div class="flex items-start space-x-3">
                          <!-- User Avatar -->
                          <NuxtLink :to="'/profile'"
                            class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center flex-shrink-0 overflow-hidden hover:opacity-90 transition-opacity">
                            <img v-if="reply.user?.avatar_url" :src="reply.user.avatar_url" :alt="reply.user.name"
                              class="w-full h-full object-cover" />
                            <span v-else class="text-xs font-medium text-gray-700 dark:text-gray-300">
                              {{ reply.user?.name?.charAt(0)?.toUpperCase() || 'U' }}
                            </span>
                          </NuxtLink>

                          <!-- Reply Content -->
                          <div class="flex-1">
                            <div class="flex items-center justify-between mb-1">
                              <div>
                                <NuxtLink :to="'/profile'"
                                  class="text-sm font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                                  {{ reply.user?.name || 'Anonymous' }}
                                </NuxtLink>
                                <span class="text-xs text-gray-500 dark:text-gray-400 ml-2">{{
                                  formatDate(reply.created_at) }}</span>
                              </div>
                              <div v-if="authStore.user?.id === reply.user_id" class="flex items-center space-x-2">
                                <button @click="editComment(reply)"
                                  class="text-xs text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400">
                                  Edit
                                </button>
                                <button @click="deleteComment(reply.id)"
                                  class="text-xs text-red-500 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300">
                                  Delete
                                </button>
                              </div>
                            </div>
                            <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-line">{{ reply.content }}
                            </p>

                            <!-- Reply Actions -->
                            <div class="flex items-center space-x-3 mt-2">
                              <button @click="voteComment(reply.id, 'upvote')"
                                class="flex items-center space-x-1 text-xs text-gray-500 dark:text-gray-400 hover:text-green-600 dark:hover:text-green-400">
                                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M5 15l7-7 7 7" />
                                </svg>
                                <span>{{ reply.upvote_count || 0 }}</span>
                              </button>
                              <button @click="voteComment(reply.id, 'downvote')"
                                class="flex items-center space-x-1 text-xs text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400">
                                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 9l-7 7-7-7" />
                                </svg>
                                <span>{{ reply.downvote_count || 0 }}</span>
                              </button>
                              <button @click="startReply(reply.id)"
                                class="text-xs text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400">
                                Reply
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
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

          <CreatorInfo
            :project="project"
            :title="t('projects.detail.creator')"
            subtitle="Project Creator"
          />

          <ProjectActions
            :project="project"
            :can-edit="canEditProject"
            :title="t('projects.detail.actions')"
            :edit-label="t('projects.detail.editProject')"
            :delete-label="t('projects.detail.deleteProject')"
            :view-hackathon-label="t('projects.detail.viewHackathon')"
            :view-team-label="t('projects.detail.viewTeam')"
            :back-label="t('projects.detail.backToProjects')"
            @delete="deleteProject"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { format } from 'date-fns'
import { useRoute, useRouter } from '#imports'
import { useAuthStore } from '~/stores/auth'
import { useVotingStore } from '~/stores/voting'
import { useUIStore } from '~/stores/ui'
import { useI18n } from 'vue-i18n'
import { generateProjectPlaceholder } from '~/utils/placeholderImages'
import { resolveImageUrl } from '~/utils/imageUrl'
import ProjectHeader from '~/components/projects/ProjectHeader.vue'
import TechnologyTags from '~/components/projects/TechnologyTags.vue'
import ProjectLinks from '~/components/projects/ProjectLinks.vue'
import ProjectStats from '~/components/projects/ProjectStats.vue'
import CreatorInfo from '~/components/projects/CreatorInfo.vue'
import ProjectActions from '~/components/projects/ProjectActions.vue'

interface CommentUser {
  name: string
  avatar_url: string | null
}

interface Comment {
  id: number
  content: string
  created_at: string
  user_name?: string
  user_id?: number
  upvote_count?: number
  downvote_count?: number
  replies?: Comment[]
  user?: CommentUser
}

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const votingStore = useVotingStore()
const uiStore = useUIStore()
const { t } = useI18n()

const loading = ref(true)
const error = ref<string | null>(null)
const project = ref<any>(null)

// Comments state
const comments = ref<Comment[]>([])
const commentsLoading = ref(false)
const newComment = ref('')
const commentLoading = ref(false)
const editingCommentId = ref<number | null>(null)
const editingContent = ref('')
const replyingToCommentId = ref<number | null>(null)
const replyContent = ref('')
const replyLoading = ref(false)

const projectTechnologies = computed(() => {
  if (!project.value?.technologies) return []
  return project.value.technologies.split(',').map((tech: string) => tech.trim()).filter(Boolean)
})

const projectImage = computed(() => {
  if (!project.value?.image_path) {
    // Generate a placeholder image based on project ID and title
    return generateProjectPlaceholder({
      id: project.value?.id || 0,
      title: project.value?.title || 'Project'
    })
  }
  return resolveImageUrl(project.value.image_path, useRuntimeConfig().public.apiUrl || 'http://localhost:8000')
})

const canEditProject = computed(() => {
  if (!authStore.isAuthenticated || !project.value) {
    return false
  }

  // Check if user is the project owner
  // Convert both to numbers for comparison
  const userId = Number(authStore.user?.id)
  const ownerId = Number(project.value.owner_id)
  const isOwner = userId === ownerId

  if (isOwner) return true

  // TODO: Check if user is a team member
  // For now, only owner can edit
  return false
})

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  try {
    return format(new Date(dateString), 'MMM dd, yyyy')
  } catch {
    return dateString
  }
}

const fetchProject = async () => {
  try {
    loading.value = true
    error.value = null

    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // First, increment the view count
    try {
      await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId}/view`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })
    } catch (viewErr) {
      console.warn('Failed to increment view count:', viewErr)
      // Continue loading project even if view increment fails
    }

    // Then fetch the project details
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId}`)

    if (!response.ok) {
      if (response.status === 404) {
        error.value = 'Project not found'
        uiStore.showError('Project not found', 'The project you are looking for does not exist or has been removed.')
      } else {
        error.value = `Failed to load project: ${response.status}`
        uiStore.showError('Failed to load project', `Unable to load project details. Please try again later. (Error: ${response.status})`)
      }
      return
    }

    project.value = await response.json()

    // Also fetch vote stats for this project
    await votingStore.getProjectVoteStats(projectId)
  } catch (err) {
    console.error('Error fetching project:', err)
    error.value = 'Failed to load project details'
    uiStore.showError('Failed to load project', 'An unexpected error occurred while loading the project. Please try again later.')
  } finally {
    loading.value = false
  }
}

// Comments methods
const fetchComments = async () => {
  try {
    commentsLoading.value = true
    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId}/comments`)

    if (response.ok) {
      const data = await response.json()
      // Transform comments to match frontend expectations
      comments.value = (data.comments || []).map((comment: Comment) => ({
        ...comment,
        user: {
          name: comment.user_name || 'Anonymous',
          avatar_url: null // Backend doesn't provide avatar_url for comments
        }
      }))
    }
  } catch (err) {
    console.error('Error fetching comments:', err)
    uiStore.showError('Failed to load comments', 'Unable to load comments. Please try again later.')
  } finally {
    commentsLoading.value = false
  }
}

const submitComment = async () => {
  if (!newComment.value.trim() || commentLoading.value) return

  try {
    commentLoading.value = true
    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      console.error('No authentication token')
      uiStore.showError('Authentication required', 'Please log in to post a comment.')
      commentLoading.value = false
      return
    }

    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: newComment.value.trim()
      })
    })

    if (response.ok) {
      newComment.value = ''
      await fetchComments()
      // Update comment count in project
      if (project.value) {
        project.value.comment_count = (project.value.comment_count || 0) + 1
      }
    } else {
      console.error('Failed to submit comment:', response.status)
      uiStore.showError('Failed to submit comment', `Unable to submit your comment. Please try again. (Error: ${response.status})`)
    }
  } catch (err) {
    console.error('Error submitting comment:', err)
    uiStore.showError('Failed to submit comment', 'An unexpected error occurred while submitting your comment. Please try again.')
  } finally {
    commentLoading.value = false
  }
}

const editComment = (comment: Comment) => {
  editingCommentId.value = comment.id
  editingContent.value = comment.content
}

const saveComment = async (commentId: number) => {
  if (!editingContent.value.trim()) return

  try {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      console.error('No authentication token')
      uiStore.showError('Authentication required', 'Please log in to edit a comment.')
      return
    }

    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/comments/${commentId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: editingContent.value.trim()
      })
    })

    if (response.ok) {
      editingCommentId.value = null
      editingContent.value = ''
      await fetchComments()
    } else {
      console.error('Failed to update comment:', response.status)
      uiStore.showError('Failed to update comment', `Unable to update your comment. Please try again. (Error: ${response.status})`)
    }
  } catch (err) {
    console.error('Error updating comment:', err)
    uiStore.showError('Failed to update comment', 'An unexpected error occurred while updating your comment. Please try again.')
  }
}

const cancelEdit = () => {
  editingCommentId.value = null
  editingContent.value = ''
}

const deleteComment = async (commentId: number) => {
  if (!confirm('Are you sure you want to delete this comment?')) return

  try {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      console.error('No authentication token')
      uiStore.showError('Authentication required', 'Please log in to edit a comment.')
      return
    }

    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/comments/${commentId}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      await fetchComments()
      // Update comment count in project
      if (project.value) {
        project.value.comment_count = Math.max(0, (project.value.comment_count || 1) - 1)
      }
    } else {
      console.error('Failed to delete comment:', response.status)
      uiStore.showError('Failed to delete comment', `Unable to delete your comment. Please try again. (Error: ${response.status})`)
    }
  } catch (err) {
    console.error('Error deleting comment:', err)
    uiStore.showError('Failed to delete comment', 'An unexpected error occurred while deleting your comment. Please try again.')
  }
}

const voteComment = async (commentId: number, voteType: 'upvote' | 'downvote') => {
  try {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      console.error('No authentication token')
      uiStore.showError('Authentication required', 'Please log in to vote on a comment.')
      return
    }

    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/comments/${commentId}/vote`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ vote_type: voteType })
    })

    if (response.ok) {
      // Refresh comments to get updated vote counts
      await fetchComments()
    } else {
      console.error('Failed to vote on comment:', response.status)
      uiStore.showError('Failed to vote on comment', `Unable to vote on the comment. Please try again. (Error: ${response.status})`)
    }
  } catch (err) {
    console.error('Error voting on comment:', err)
    uiStore.showError('Failed to vote on comment', 'An unexpected error occurred while voting on the comment. Please try again.')
  }
}

// Reply functions
const startReply = (commentId: number) => {
  replyingToCommentId.value = commentId
  replyContent.value = ''
}

const cancelReply = () => {
  replyingToCommentId.value = null
  replyContent.value = ''
}

const submitReply = async (commentId: number) => {
  if (!replyContent.value.trim() || replyLoading.value) return

  try {
    replyLoading.value = true
    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      console.error('No authentication token')
      uiStore.showError('Authentication required', 'Please log in to post a reply.')
      replyLoading.value = false
      return
    }

    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: replyContent.value.trim(),
        parent_comment_id: commentId
      })
    })

    if (response.ok) {
      replyContent.value = ''
      replyingToCommentId.value = null
      await fetchComments()
      // Update comment count in project
      if (project.value) {
        project.value.comment_count = (project.value.comment_count || 0) + 1
      }
    } else {
      console.error('Failed to submit reply:', response.status)
      uiStore.showError('Failed to submit reply', `Unable to submit your reply. Please try again. (Error: ${response.status})`)
    }
  } catch (err) {
    console.error('Error submitting reply:', err)
    uiStore.showError('Failed to submit reply', 'An unexpected error occurred while submitting your reply. Please try again.')
  } finally {
    replyLoading.value = false
  }
}

const deleteProject = async () => {
  if (!confirm(t('projects.delete.confirm', { title: project.value?.title || 'this project' }))) {
    return
  }

  try {
    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'

    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      uiStore.showWarning(t('projects.delete.authRequired'), t('common.authenticationRequired'))
      return
    }

    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      uiStore.showSuccess(t('projects.delete.success'), t('common.success'))
      router.push('/projects')
    } else {
      if (response.status === 401) {
        uiStore.showError(t('projects.delete.sessionExpired'), t('common.authenticationError'))
      } else if (response.status === 403) {
        uiStore.showError(t('projects.delete.notAuthorized'), t('common.authorizationError'))
      } else {
        uiStore.showError(t('projects.delete.failed'), t('common.error'))
      }
    }
  } catch (err) {
    console.error('Error deleting project:', err)
    uiStore.showError(t('projects.delete.error'), t('common.error'))
  }
}

onMounted(() => {
  fetchProject()
  fetchComments()
})
</script>
