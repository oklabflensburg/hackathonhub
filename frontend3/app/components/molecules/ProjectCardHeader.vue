<template>
  <div class="project-card-header" :class="headerClasses">
    <!-- Link Wrapper (wenn clickable) -->
    <component
      :is="clickable ? 'a' : 'div'"
      v-if="clickable"
      :href="projectLink"
      class="header-link"
      :aria-label="`View project: ${project.title}`"
      @click="handleClick"
    >
      <slot name="before-title" />
      
      <!-- Projekt-Titel -->
      <h3 class="project-title" :class="titleClasses">
        <span class="title-text">
          {{ project.title }}
        </span>
        
        <!-- Status Badge (optional) -->
        <ProjectStatusBadge
          v-if="showStatus"
          :status="project.status"
          :size="statusSize"
          :variant="statusVariant"
          :show-label="showStatusLabel"
          :show-icon="showStatusIcon"
          class="ml-2"
        />
      </h3>
      
      <slot name="after-title" />
    </component>
    
    <!-- Non-clickable Version -->
    <template v-else>
      <slot name="before-title" />
      
      <!-- Projekt-Titel -->
      <h3 class="project-title" :class="titleClasses">
        <span class="title-text">
          {{ project.title }}
        </span>
        
        <!-- Status Badge (optional) -->
        <ProjectStatusBadge
          v-if="showStatus"
          :status="project.status"
          :size="statusSize"
          :variant="statusVariant"
          :show-label="showStatusLabel"
          :show-icon="showStatusIcon"
          class="ml-2"
        />
      </h3>
      
      <slot name="after-title" />
    </template>
    
    <!-- Projekt-Metadaten -->
    <div v-if="showMetadata" class="project-metadata" :class="metadataClasses">
      <!-- Autor/Avatar (erstes Team-Mitglied als Owner) -->
      <div v-if="showAuthor && project.team?.length > 0" class="author-info">
        <slot name="author">
          <div class="flex items-center gap-2">
            <!-- Avatar -->
            <div
              v-if="getOwnerAvatarUrl"
              class="author-avatar"
              :class="avatarClasses"
            >
              <img
                :src="getOwnerAvatarUrl"
                :alt="`Avatar of ${getOwner()?.user?.username}`"
                class="w-full h-full rounded-full object-cover"
              />
            </div>
            <div
              v-else
              class="author-avatar-placeholder"
              :class="avatarPlaceholderClasses"
            >
              <span class="placeholder-text">
                {{ getOwner()?.user?.username?.charAt(0).toUpperCase() || '?' }}
              </span>
            </div>
            
            <!-- Autor-Name -->
            <span class="author-name" :class="authorNameClasses">
              {{ getOwner()?.user?.username || 'Unknown' }}
            </span>
          </div>
        </slot>
      </div>
      
      <!-- Erstellungsdatum -->
      <div v-if="showDate && project.createdAt" class="creation-date">
        <time :datetime="project.createdAt" :class="dateClasses">
          {{ formatDate(project.createdAt) }}
        </time>
      </div>
      
      <!-- Team Info (optional) -->
      <div v-if="showTeam && project.team?.length > 0" class="team-info">
        <span class="team-label" :class="teamLabelClasses">
          Team:
        </span>
        <span class="team-name" :class="teamNameClasses">
          {{ project.team.length }} member{{ project.team.length !== 1 ? 's' : '' }}
        </span>
      </div>
      
      <!-- Hackathon Info (optional) -->
      <div v-if="showHackathon && project.hackathonName" class="hackathon-info">
        <span class="hackathon-label" :class="hackathonLabelClasses">
          Hackathon:
        </span>
        <span class="hackathon-name" :class="hackathonNameClasses">
          {{ project.hackathonName }}
        </span>
      </div>
    </div>
    
    <!-- Aktionen (optional) -->
    <div v-if="showActions" class="header-actions" :class="actionsClasses">
      <slot name="actions">
        <!-- Platzhalter für benutzerdefinierte Aktionen -->
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Project } from '~/types/project-types'
import ProjectStatusBadge from '~/components/atoms/ProjectStatusBadge.vue'

interface Props {
  /** Projekt-Daten */
  project: Project
  /** Klickbarer Header */
  clickable?: boolean
  /** Projekt-Link (wenn clickable) */
  projectLink?: string
  /** Status anzeigen */
  showStatus?: boolean
  /** Status-Badge Größe */
  statusSize?: 'sm' | 'md' | 'lg'
  /** Status-Badge Variante */
  statusVariant?: 'solid' | 'outline' | 'soft'
  /** Status-Label anzeigen */
  showStatusLabel?: boolean
  /** Status-Icon anzeigen */
  showStatusIcon?: boolean
  /** Metadaten anzeigen */
  showMetadata?: boolean
  /** Autor anzeigen */
  showAuthor?: boolean
  /** Erstellungsdatum anzeigen */
  showDate?: boolean
  /** Team anzeigen */
  showTeam?: boolean
  /** Hackathon anzeigen */
  showHackathon?: boolean
  /** Aktionen anzeigen */
  showActions?: boolean
  /** Kompakte Variante */
  compact?: boolean
  /** Ausrichtung */
  align?: 'left' | 'center' | 'right'
}

const props = withDefaults(defineProps<Props>(), {
  clickable: false,
  showStatus: true,
  statusSize: 'sm',
  statusVariant: 'soft',
  showStatusLabel: false,
  showStatusIcon: true,
  showMetadata: true,
  showAuthor: true,
  showDate: true,
  showTeam: false,
  showHackathon: false,
  showActions: false,
  compact: false,
  align: 'left',
})

const emit = defineEmits<{
  'click': [project: Project]
}>()

const getOwnerAvatarUrl = computed(() => getOwner()?.user?.avatarUrl || getOwner()?.user?.avatar_url)

// Computed Properties
const headerClasses = computed(() => {
  const classes: string[] = []
  
  if (props.compact) {
    classes.push('compact')
  }
  
  switch (props.align) {
    case 'center':
      classes.push('text-center')
      break
    case 'right':
      classes.push('text-right')
      break
    case 'left':
    default:
      classes.push('text-left')
  }
  
  return classes.join(' ')
})

const titleClasses = computed(() => {
  const classes: string[] = [
    'font-semibold leading-tight',
    props.compact ? 'text-lg' : 'text-xl',
  ]
  
  if (props.clickable) {
    classes.push('hover:text-blue-600 dark:hover:text-blue-400 transition-colors')
  }
  
  return classes.join(' ')
})

const metadataClasses = computed(() => {
  const classes: string[] = [
    'flex flex-wrap items-center gap-3 mt-2',
    props.compact ? 'text-xs' : 'text-sm',
  ]
  
  return classes.join(' ')
})

const avatarClasses = computed(() => {
  return props.compact ? 'w-6 h-6' : 'w-8 h-8'
})

const avatarPlaceholderClasses = computed(() => {
  const base = 'rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center'
  const size = props.compact ? 'w-6 h-6 text-xs' : 'w-8 h-8 text-sm'
  return `${base} ${size}`
})

const authorNameClasses = computed(() => {
  return 'text-gray-700 dark:text-gray-300 font-medium'
})

const dateClasses = computed(() => {
  return 'text-gray-500 dark:text-gray-400'
})

const teamLabelClasses = computed(() => {
  return 'text-gray-500 dark:text-gray-400'
})

const teamNameClasses = computed(() => {
  return 'text-gray-700 dark:text-gray-300 font-medium'
})

const hackathonLabelClasses = computed(() => {
  return 'text-gray-500 dark:text-gray-400'
})

const hackathonNameClasses = computed(() => {
  return 'text-gray-700 dark:text-gray-300 font-medium'
})

const actionsClasses = computed(() => {
  return 'mt-3 flex items-center justify-end gap-2'
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

const getOwner = () => {
  if (!props.project.team || props.project.team.length === 0) {
    return null
  }
  
  // Find owner (role === 'owner') or first team member
  const owner = props.project.team.find(member => member.role === 'owner')
  return owner || props.project.team[0]
}

const handleClick = (event: Event) => {
  if (props.clickable) {
    emit('click', props.project)
  }
}
</script>

<style scoped>
.project-card-header {
  transition: all 0.2s ease;
}

.header-link {
  display: block;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}

.header-link:hover .project-title {
  text-decoration: underline;
  text-decoration-thickness: 2px;
  text-underline-offset: 2px;
}

/* Compact Variante */
.project-card-header.compact .project-title {
  font-size: 1.125rem;
  line-height: 1.4;
}

.project-card-header.compact .project-metadata {
  font-size: 0.75rem;
  margin-top: 0.5rem;
}

/* Responsive Anpassungen */
@media (max-width: 640px) {
  .project-card-header:not(.compact) .project-title {
    font-size: 1.25rem;
  }
  
  .project-metadata {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .header-actions {
    flex-wrap: wrap;
    justify-content: flex-start;
  }
}

/* Dark Mode Optimierungen */
@media (prefers-color-scheme: dark) {
  .header-link:hover .project-title {
    color: #60a5fa;
  }
  
  .author-avatar-placeholder {
    background-color: #374151;
  }
}

/* Accessibility */
.header-link:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 2px;
  border-radius: 0.25rem;
}

/* Loading State (für zukünftige Erweiterungen) */
.project-card-header.loading .project-title,
.project-card-header.loading .project-metadata > * {
  position: relative;
  overflow: hidden;
}

.project-card-header.loading .project-title::after,
.project-card-header.loading .project-metadata > *::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style>
