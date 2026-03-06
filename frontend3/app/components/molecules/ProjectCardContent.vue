<template>
  <div class="project-card-content" :class="contentClasses">
    <!-- Featured Image (optional) -->
    <div
      v-if="showFeaturedImage && project.featuredImage"
      class="featured-image-container mb-4"
      :class="imageContainerClasses"
    >
      <img
        :src="project.featuredImage"
        :alt="`Featured image for ${project.title}`"
        class="featured-image w-full h-full object-cover rounded-lg"
        :class="imageClasses"
        loading="lazy"
        @error="handleImageError"
      />
      
      <!-- Image Overlay (optional) -->
      <div
        v-if="showImageOverlay"
        class="image-overlay absolute inset-0 bg-gradient-to-t from-black/60 to-transparent rounded-lg flex items-end p-4"
      >
        <div class="overlay-content text-white">
          <slot name="image-overlay">
            <!-- Default overlay content -->
            <div class="flex items-center justify-between w-full">
              <span class="text-sm font-medium">
                {{ project.technologies?.length || 0 }} technologies
              </span>
              <span class="text-sm">
                {{ formatDate(project.createdAt) }}
              </span>
            </div>
          </slot>
        </div>
      </div>
    </div>
    
    <!-- Projekt-Beschreibung -->
    <div v-if="showDescription" class="project-description mb-4">
      <p class="description-text" :class="descriptionClasses">
        {{ displayDescription }}
      </p>
      
      <!-- Read More Link (wenn Text abgeschnitten) -->
      <button
        v-if="showReadMore && isTruncated && interactive"
        type="button"
        class="read-more-link mt-2 text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline focus:outline-none"
        @click="toggleReadMore"
      >
        {{ showFullDescription ? 'Show less' : 'Read more' }}
      </button>
    </div>
    
    <!-- Kurzbeschreibung (alternative) -->
    <div
      v-else-if="showShortDescription && project.shortDescription"
      class="project-short-description mb-4"
    >
      <p class="short-description-text text-gray-600 dark:text-gray-400" :class="shortDescriptionClasses">
        {{ project.shortDescription }}
      </p>
    </div>
    
    <!-- Tags (optional) -->
    <div
      v-if="showTags && project.tags?.length > 0"
      class="project-tags mb-4"
      :class="tagsClasses"
    >
      <div class="tags-header flex items-center justify-between mb-2">
        <span class="tags-label text-xs font-medium text-gray-500 dark:text-gray-400">
          Tags:
        </span>
        <button
          v-if="showAllTagsButton && project.tags.length > maxVisibleTags"
          type="button"
          class="show-all-tags text-xs text-blue-600 dark:text-blue-400 hover:underline focus:outline-none"
          @click="handleShowAllTags"
        >
          Show all ({{ project.tags.length }})
        </button>
      </div>
      
      <div class="tags-list flex flex-wrap gap-1">
        <ProjectTag
          v-for="tag in visibleTags"
          :key="tag.id"
          :tag="tag"
          size="sm"
          :clickable="interactive"
          @click="handleTagClick"
        />
      </div>
    </div>
    
    <!-- Technologies (optional) -->
    <div
      v-if="showTechnologies && project.technologies?.length > 0"
      class="project-technologies mb-4"
      :class="technologiesClasses"
    >
      <div class="technologies-header flex items-center justify-between mb-2">
        <span class="technologies-label text-xs font-medium text-gray-500 dark:text-gray-400">
          Technologies:
        </span>
        <button
          v-if="showAllTechnologiesButton && project.technologies.length > maxVisibleTechnologies"
          type="button"
          class="show-all-technologies text-xs text-blue-600 dark:text-blue-400 hover:underline focus:outline-none"
          @click="handleShowAllTechnologies"
        >
          Show all ({{ project.technologies.length }})
        </button>
      </div>
      
      <div class="technologies-list flex flex-wrap gap-1">
        <span
          v-for="tech in visibleTechnologies"
          :key="tech.id"
          class="technology-badge inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
          :class="technologyBadgeClasses(tech)"
          :style="{ backgroundColor: `${tech.color}15`, color: tech.color }"
          @click="handleTechnologyClick(tech)"
        >
          <span
            v-if="tech.icon"
            class="technology-icon mr-1"
            aria-hidden="true"
          >
            {{ tech.icon }}
          </span>
          {{ tech.name }}
        </span>
      </div>
    </div>
    
    <!-- Team Members (optional) -->
    <div
      v-if="showTeam && project.team?.length > 0"
      class="project-team mb-4"
      :class="teamClasses"
    >
      <div class="team-header flex items-center justify-between mb-2">
        <span class="team-label text-xs font-medium text-gray-500 dark:text-gray-400">
          Team ({{ project.team.length }}):
        </span>
        <button
          v-if="showAllTeamButton && project.team.length > maxVisibleTeamMembers"
          type="button"
          class="show-all-team text-xs text-blue-600 dark:text-blue-400 hover:underline focus:outline-none"
          @click="handleShowAllTeam"
        >
          Show all
        </button>
      </div>
      
      <div class="team-members flex flex-wrap gap-2">
        <div
          v-for="member in visibleTeamMembers"
          :key="member.user.id"
          class="team-member flex items-center gap-1.5"
          :class="teamMemberClasses"
          @click="handleTeamMemberClick(member)"
        >
          <!-- Avatar -->
          <div
            v-if="member.user.avatarUrl"
            class="member-avatar w-6 h-6 rounded-full overflow-hidden"
          >
            <img
              :src="member.user.avatarUrl"
              :alt="`Avatar of ${member.user.username}`"
              class="w-full h-full object-cover"
            />
          </div>
          <div
            v-else
            class="member-avatar-placeholder w-6 h-6 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-xs"
          >
            {{ member.user.username?.charAt(0).toUpperCase() || '?' }}
          </div>
          
          <!-- Name (nur in expanded view) -->
          <span
            v-if="showTeamMemberNames"
            class="member-name text-xs text-gray-700 dark:text-gray-300 truncate max-w-[80px]"
          >
            {{ member.user.username }}
          </span>
          
          <!-- Role Badge (optional) -->
          <span
            v-if="showTeamMemberRoles && member.role !== 'member'"
            class="member-role text-[10px] px-1 py-0.5 rounded bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400"
          >
            {{ member.role }}
          </span>
        </div>
        
        <!-- More Members Indicator -->
        <div
          v-if="hasMoreTeamMembers"
          class="more-members text-xs text-gray-500 dark:text-gray-400 flex items-center"
        >
          +{{ project.team.length - maxVisibleTeamMembers }}
        </div>
      </div>
    </div>
    
    <!-- Deadline (optional) -->
    <div
      v-if="showDeadline && project.deadline"
      class="project-deadline mb-4"
      :class="deadlineClasses"
    >
      <div class="deadline-header flex items-center gap-2 mb-1">
        <span class="deadline-icon" aria-hidden="true">
          <svg
            class="w-4 h-4 text-gray-400 dark:text-gray-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
        </span>
        <span class="deadline-label text-xs font-medium text-gray-500 dark:text-gray-400">
          Deadline:
        </span>
      </div>
      <time
        :datetime="project.deadline"
        class="deadline-date text-sm font-medium text-gray-700 dark:text-gray-300"
        :class="{ 'text-red-600 dark:text-red-400': isDeadlinePassed }"
      >
        {{ formatDate(project.deadline) }}
        <span
          v-if="isDeadlinePassed"
          class="deadline-passed ml-2 text-xs font-normal text-red-500 dark:text-red-400"
        >
          (Passed)
        </span>
        <span
          v-else-if="daysUntilDeadline >= 0"
          class="deadline-countdown ml-2 text-xs font-normal text-gray-500 dark:text-gray-400"
        >
          (in {{ daysUntilDeadline }} day{{ daysUntilDeadline !== 1 ? 's' : '' }})
        </span>
      </time>
    </div>
    
    <!-- Custom Content Slot -->
    <div v-if="$slots.default" class="custom-content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Project, ProjectTechnology, ProjectTeamMember } from '~/types/project-types'
import ProjectTag from '~/components/atoms/ProjectTag.vue'
import { ref, computed } from 'vue'

interface Props {
  /** Projekt-Daten */
  project: Project
  /** Interaktive Elemente */
  interactive?: boolean
  /** Featured Image anzeigen */
  showFeaturedImage?: boolean
  /** Image Overlay anzeigen */
  showImageOverlay?: boolean
  /** Beschreibung anzeigen */
  showDescription?: boolean
  /** Kurzbeschreibung anzeigen */
  showShortDescription?: boolean
  /** Maximale Beschreibungslänge */
  maxDescriptionLength?: number
  /** Tags anzeigen */
  showTags?: boolean
  /** Technologies anzeigen */
  showTechnologies?: boolean
  /** Team anzeigen */
  showTeam?: boolean
  /** Deadline anzeigen */
  showDeadline?: boolean
  /** Maximale sichtbare Tags */
  maxVisibleTags?: number
  /** Maximale sichtbare Technologies */
  maxVisibleTechnologies?: number
  /** Maximale sichtbare Team-Mitglieder */
  maxVisibleTeamMembers?: number
  /** Team-Mitglieder-Namen anzeigen */
  showTeamMemberNames?: boolean
  /** Team-Mitglieder-Rollen anzeigen */
  showTeamMemberRoles?: boolean
  /** "Show All" Buttons anzeigen */
  showAllTagsButton?: boolean
  showAllTechnologiesButton?: boolean
  showAllTeamButton?: boolean
  /** Read More Link anzeigen */
  showReadMore?: boolean
  /** Kompakte Variante */
  compact?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  interactive: true,
  showFeaturedImage: true,
  showImageOverlay: false,
  showDescription: true,
  showShortDescription: false,
  maxDescriptionLength: 150,
  showTags: true,
  showTechnologies: true,
  showTeam: false,
  showDeadline: false,
  maxVisibleTags: 4,
  maxVisibleTechnologies: 4,
  maxVisibleTeamMembers: 4,
  showTeamMemberNames: false,
  showTeamMemberRoles: false,
  showAllTagsButton: true,
  showAllTechnologiesButton: true,
  showAllTeamButton: true,
  showReadMore: true,
  compact: false,
})

const emit = defineEmits<{
  'tag-click': [tag: any]
  'technology-click': [technology: ProjectTechnology]
  'team-member-click': [member: ProjectTeamMember]
  'show-all-tags': []
  'show-all-technologies': []
  'show-all-team': []
  'image-error': [error: Event]
}>()

// Local State
const showFullDescription = ref(false)
const imageError = ref(false)

// Computed Properties
const contentClasses = computed(() => {
  return props.compact ? 'compact' : ''
})

const imageContainerClasses = computed(() => {
  const base = 'relative overflow-hidden rounded-lg'
  const aspect = props.compact ? 'aspect-video' : 'aspect-[16/9]'
  return `${base} ${aspect}`
})

const imageClasses = computed(() => {
  return 'transition-transform duration-300 hover:scale-105'
})

const descriptionClasses = computed(() => {
  const base = 'text-gray-700 dark:text-gray-300'
  const size = props.compact ? 'text-sm' : 'text-base'
  return `${base} ${size}`
})

const shortDescriptionClasses = computed(() => {
  return props.compact ? 'text-sm' : 'text-base'
})

const tagsClasses = computed(() => {
  return props.compact ? 'text-xs' : ''
})

const technologiesClasses = computed(() => {
  return props.compact ? 'text-xs' : ''
})

const teamClasses = computed(() => {
  return props.compact ? 'text-xs' : ''
})

const teamMemberClasses = computed(() => {
  const base = 'cursor-pointer hover:opacity-80 transition-opacity'
  return props.interactive ? base : ''
})

const deadlineClasses = computed(() => {
  return props.compact ? 'text-xs' : 'text-sm'
})

const displayDescription = computed(() => {
  if (!props.project.description) return ''
  
  if (showFullDescription.value) {
    return props.project.description
  }
  
  if (props.project.description.length <= props.maxDescriptionLength) {
    return props.project.description
  }
  
  return props.project.description.substring(0, props.maxDescriptionLength) + '...'
})

const isTruncated = computed(() => {
  if (!props.project.description) return false
  return props.project.description.length > props.maxDescriptionLength
})

const visibleTags = computed(() => {
  if (!props.project.tags) return []
  return props.project.tags.slice(0, props.maxVisibleTags)
})

const visibleTechnologies = computed(() => {
  if (!props.project.technologies) return []
  return props.project.technologies.slice(0, props.maxVisibleTechnologies)
})

const visibleTeamMembers = computed(() => {
  if (!props.project.team) return []
  
  // Sort by role (owner first, then by joined date)
  const sortedTeam = [...props.project.team].sort((a, b) => {
    if (a.role === 'owner' && b.role !== 'owner') return -1
    if (a.role !== 'owner' && b.role === 'owner') return 1
    return new Date(a.joinedAt).getTime() - new Date(b.joinedAt).getTime()
  })
  
  return sortedTeam.slice(0, props.maxVisibleTeamMembers)
})

const hasMoreTeamMembers = computed(() => {
  if (!props.project.team) return false
  return props.project.team.length > props.maxVisibleTeamMembers
})

const isDeadlinePassed = computed(() => {
  if (!props.project.deadline) return false
  const deadline = new Date(props.project.deadline)
  const now = new Date()
  return deadline < now
})

const daysUntilDeadline = computed(() => {
  if (!props.project.deadline) return -1
  const deadline = new Date(props.project.deadline)
  const now = new Date()
  const diffTime = deadline.getTime() - now.getTime()
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
})

// Helper Functions
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('de-DE', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

const technologyBadgeClasses = (tech: ProjectTechnology) => {
  const base = 'cursor-pointer hover:opacity-80 transition-opacity border'
  return props.interactive ? base : 'border'
}

// Event Handlers
const toggleReadMore = () => {
  showFullDescription.value = !showFullDescription.value
}

const handleTagClick = (tag: any) => {
  if (props.interactive) {
    emit('tag-click', tag)
  }
}

const handleTechnologyClick = (tech: ProjectTechnology) => {
  if (props.interactive) {
    emit('technology-click', tech)
  }
}

const handleTeamMemberClick = (member: ProjectTeamMember) => {
  if (props.interactive) {
    emit('team-member-click', member)
  }
}

const handleShowAllTags = () => {
  emit('show-all-tags')
}

const handleShowAllTechnologies = () => {
  emit('show-all-technologies')
}

const handleShowAllTeam = () => {
  emit('show-all-team')
}

const handleImageError = (error: Event) => {
  imageError.value = true
  emit('image-error', error)
}
</script>

<style scoped>
.project-card-content {
  transition: all 0.2s ease;
}

/* Compact Variante */
.project-card-content.compact .featured-image-container {
  margin-bottom: 0.75rem;
}
</style>
