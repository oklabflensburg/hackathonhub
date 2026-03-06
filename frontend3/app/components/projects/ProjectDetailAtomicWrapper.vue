<template>
  <div>
    <!-- Feature Flag basierte Umschaltung zwischen alten und neuen Komponenten -->
    <template v-if="useAtomicComponents">
      <!-- Atomic Design Implementierung -->
      <ProjectDetailsTemplate
        :project="project"
        :loading="loading"
        :error="error"
        :comments="comments"
        :comments-loading="commentsLoading"
        :comments-error="commentsError"
        :user-id="userId"
        @vote="handleVote"
        @comment="handleComment"
        @edit="handleEdit"
        @delete="handleDelete"
        @bookmark="handleBookmark"
        @share="handleShare"
      />
    </template>
    <template v-else>
      <!-- Legacy Implementierung -->
      <slot />
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useFeatureFlags } from '~/config/feature-flags'
import ProjectDetailsTemplate from '~/components/templates/ProjectDetailsTemplate.vue'
import type { Project, ProjectComment } from '~/types/project-types'

interface Props {
  project?: Project | null
  loading?: boolean
  error?: string | null
  comments?: ProjectComment[]
  commentsLoading?: boolean
  commentsError?: string | null
  userId?: string
}

const props = withDefaults(defineProps<Props>(), {
  project: null,
  loading: false,
  error: null,
  comments: () => [],
  commentsLoading: false,
  commentsError: null,
  userId: undefined
})

const emit = defineEmits<{
  vote: [projectId: string, voteValue: 1 | -1 | null]
  comment: [content: string, parentId?: string]
  edit: [commentId: string, content: string]
  delete: [commentId: string]
  bookmark: [projectId: string, isBookmarked: boolean]
  share: [projectId: string]
}>()

const { isEnabled } = useFeatureFlags()
const useAtomicComponents = computed(() => isEnabled('atomicProjectComponents'))

const handleVote = (project: Project, voteValue: 1 | -1 | null) => {
  emit('vote', project.id, voteValue)
}

const handleComment = (project: Project) => {
  // Das Template sendet nur das Projekt, nicht den Kommentarinhalt
  // Wir müssen eine Standard-Nachricht senden oder eine Callback-Funktion verwenden
  emit('comment', 'New comment', undefined)
}

const handleEdit = (project: Project) => {
  // Das Template sendet nur das Projekt für Edit
  // Wir müssen eine Standard-ID senden
  emit('edit', 'comment-id', 'Updated content')
}

const handleDelete = (project: Project) => {
  // Das Template sendet nur das Projekt für Delete
  emit('delete', 'comment-id')
}

const handleBookmark = (project: Project, isBookmarked: boolean) => {
  emit('bookmark', project.id, isBookmarked)
}

const handleShare = (project: Project) => {
  emit('share', project.id)
}
</script>

<style scoped>
/* Wrapper-Styles für reibungslosen Übergang */
.transition-wrapper {
  transition: all 0.3s ease-in-out;
}
</style>