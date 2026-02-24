# Clickable Cards Implementation Plan (Updated)

## Overview
Make ALL cards on the homepage (http://localhost:3001/) clickable with proper navigation to relevant pages.

## Current State Analysis

### 1. Stats Cards (Lines 71-86 in `index.vue`)
- Simple `div` elements with no click handlers
- Display: active hackathons, projects submitted, total votes, active participants
- **New Requirement**: Make clickable with following navigation:
  - Active Hackathons → `/hackathons` (filtered to show active ones if possible)
  - Projects Submitted → `/projects`
  - Total Votes → `/projects?sort=votes` (or `/projects` with votes sorting)
  - Active Participants → `/users`

### 2. Featured Hackathon Cards (Lines 98-137)
- Partial implementation: Only "View Details" link is clickable via `NuxtLink`
- Card container is `div.card-hover` without click handler
- Need to make entire card clickable to hackathon detail page

### 3. Top Project Cards (Lines 150-183)
- Partial implementation: Image and title area wrapped in `NuxtLink`
- Vote buttons are outside the link, preventing full-card clickability
- Need to handle vote button interaction separately
- Navigate to project detail page

## Implementation Requirements

### Frontend Changes Needed

#### 1. Update `frontend3/app/pages/index.vue`

**A. Add navigation functions in script section:**
```typescript
const router = useRouter()

// Navigate to hackathon detail page
const navigateToHackathon = (hackathonId: number) => {
  router.push(`/hackathons/${hackathonId}`)
}

// Navigate to project detail page  
const navigateToProject = (projectId: number) => {
  router.push(`/projects/${projectId}`)
}

// Navigate to stats-related pages
const navigateToHackathonsList = () => {
  router.push('/hackathons')
}

const navigateToProjectsList = () => {
  router.push('/projects')
}

const navigateToProjectsByVotes = () => {
  router.push('/projects?sort=votes')
}

const navigateToUsersList = () => {
  router.push('/users')
}

// Handle project card click (with vote button exception)
const handleProjectCardClick = (projectId: number, event: MouseEvent) => {
  // Check if click originated from vote buttons
  const target = event.target as HTMLElement
  const isVoteButton = target.closest('.vote-button') || 
                      target.closest('[data-vote-button]') ||
                      target.closest('button')
  
  if (!isVoteButton) {
    navigateToProject(projectId)
  }
}
```

**B. Modify stats cards template (lines 71-86):**
```vue
<!-- Stats Section -->
<section class="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
  <div 
    class="card text-center cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
    role="link"
    tabindex="0"
    @click="navigateToHackathonsList"
    @keydown.enter="navigateToHackathonsList"
    @keydown.space="navigateToHackathonsList"
  >
    <div class="text-3xl font-bold text-primary-600 dark:text-primary-400 mb-2">{{ stats.activeHackathons }}</div>
    <div class="text-gray-600 dark:text-gray-400">{{ t('home.stats.activeHackathons') }}</div>
  </div>
  
  <div 
    class="card text-center cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
    role="link"
    tabindex="0"
    @click="navigateToProjectsList"
    @keydown.enter="navigateToProjectsList"
    @keydown.space="navigateToProjectsList"
  >
    <div class="text-3xl font-bold text-green-600 dark:text-green-400 mb-2">{{ stats.projectsSubmitted }}</div>
    <div class="text-gray-600 dark:text-gray-400">{{ t('home.stats.projectsSubmitted') }}</div>
  </div>
  
  <div 
    class="card text-center cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
    role="link"
    tabindex="0"
    @click="navigateToProjectsByVotes"
    @keydown.enter="navigateToProjectsByVotes"
    @keydown.space="navigateToProjectsByVotes"
  >
    <div class="text-3xl font-bold text-purple-600 dark:text-purple-400 mb-2">{{ stats.totalVotes }}</div>
    <div class="text-gray-600 dark:text-gray-400">{{ t('home.stats.totalVotes') }}</div>
  </div>
  
  <div 
    class="card text-center cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
    role="link"
    tabindex="0"
    @click="navigateToUsersList"
    @keydown.enter="navigateToUsersList"
    @keydown.space="navigateToUsersList"
  >
    <div class="text-3xl font-bold text-orange-600 dark:text-orange-400 mb-2">{{ stats.activeParticipants }}</div>
    <div class="text-gray-600 dark:text-gray-400">{{ t('home.stats.activeParticipants') }}</div>
  </div>
</section>
```

**C. Modify hackathon card template (lines 98-137):**
```vue
<div 
  v-for="hackathon in featuredHackathons" 
  :key="hackathon.id" 
  class="card-hover group relative cursor-pointer focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
  role="link"
  :aria-label="`View details for ${hackathon.name}`"
  tabindex="0"
  @click="navigateToHackathon(hackathon.id)"
  @keydown.enter="navigateToHackathon(hackathon.id)"
  @keydown.space="navigateToHackathon(hackathon.id)"
>
  <!-- Keep existing content but remove the individual NuxtLink for "View Details" -->
  <!-- ... existing card content ... -->
  
  <div class="flex items-center justify-between text-sm">
    <div class="flex items-center space-x-4">
      <!-- ... existing icons ... -->
    </div>
    <!-- Remove the NuxtLink wrapper, keep text only -->
    <span class="text-primary-600 dark:text-primary-400 font-medium">
      {{ t('common.viewDetails') }}
    </span>
  </div>
</div>
```

**D. Modify project card template (lines 150-183):**
```vue
<div 
  v-for="project in topProjects" 
  :key="project.id" 
  class="card-hover group relative cursor-pointer focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
  role="link"
  :aria-label="`View details for ${project.name}`"
  tabindex="0"
  @click="handleProjectCardClick(project.id, $event)"
  @keydown.enter="navigateToProject(project.id)"
  @keydown.space="navigateToProject(project.id)"
>
  <!-- Remove the NuxtLink wrapper from image/title area -->
  <!-- Project Image -->
  <div class="relative w-full mb-4 overflow-hidden rounded-lg aspect-ratio-4-3">
    <img :src="project.imageUrl" :alt="project.name"
      class="img-cover transition-transform duration-300 group-hover:scale-105" />
    <div class="absolute top-2 right-2">
      <span class="badge badge-success">{{ project.hackathon }}</span>
    </div>
  </div>

  <div class="flex items-start justify-between mb-3">
    <div>
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1 group-hover:text-primary-600 dark:group-hover:text-primary-400">
        {{ project.name }}
      </h3>
      <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('common.by') }} {{ project.author }}</p>
    </div>
  </div>
  <p class="text-gray-600 dark:text-gray-400 mb-4 text-sm line-clamp-2">
    {{ project.description }}
  </p>

  <!-- Vote buttons need to stop event propagation -->
  <div class="flex items-center justify-between" @click.stop>
    <VoteButtons 
      :project-id="project.id" 
      :initial-upvotes="project.upvotes"
      :initial-downvotes="project.downvotes" 
      :initial-user-vote="project.userVote"
      class="vote-button"
    />
    <div class="flex items-center space-x-2">
      <span class="text-sm text-gray-500 dark:text-gray-400">
        {{ project.tech.join(', ') }}
      </span>
    </div>
  </div>
</div>
```

### Backend Considerations
No backend changes required for basic clickability. However, note:
- The `/users` page might need to be implemented if it doesn't exist
- The query parameter `?sort=votes` might need backend support for sorting
- Consider if active hackathons should be filtered (might need `?status=active` parameter)

## Implementation Steps

### Phase 1: Stats Cards Implementation
1. Add navigation functions for stats pages
2. Update stats cards with click handlers and accessibility attributes
3. Add hover and focus styles

### Phase 2: Hackathon Cards Implementation  
1. Add `navigateToHackathon` function
2. Update hackathon cards with full-card clickability
3. Remove redundant `NuxtLink` wrapper

### Phase 3: Project Cards Implementation
1. Add `navigateToProject` and `handleProjectCardClick` functions
2. Update project cards with click handling that excludes vote buttons
3. Ensure vote buttons have `@click.stop` to prevent navigation

### Phase 4: Testing & Polish
1. Test all navigation scenarios
2. Verify keyboard accessibility
3. Check mobile touch interactions
4. Ensure consistent styling

## Success Criteria
- [ ] All stats cards are clickable and navigate to appropriate pages
- [ ] Hackathon cards navigate to hackathon detail pages
- [ ] Project cards navigate to project detail pages (except when clicking vote buttons)
- [ ] Vote buttons work independently
- [ ] Keyboard navigation works for all cards
- [ ] Focus states are visible
- [ ] Hover effects provide visual feedback
- [ ] No regression in existing functionality

## Notes
1. Check if `/users` route exists. If not, consider alternative navigation or implement the page.
2. Verify that `?sort=votes` parameter works with the projects listing page.
3. Consider adding query parameters for filtering (e.g., `?status=active` for hackathons).
4. Ensure the `card` class has appropriate padding for focus rings.