# Clickable Cards Implementation Plan

## Overview
Make cards on the homepage (http://localhost:3001/) clickable with proper navigation to detail pages. Based on user requirements, only hackathon and project cards need to be clickable (stats cards remain non-clickable).

## Current State Analysis

### 1. Stats Cards (Lines 71-86 in `index.vue`)
- Simple `div` elements with no click handlers
- Display: active hackathons, projects submitted, total votes, active participants
- **Decision**: Keep non-clickable per user requirement

### 2. Featured Hackathon Cards (Lines 98-137)
- Partial implementation: Only "View Details" link is clickable via `NuxtLink`
- Card container is `div.card-hover` without click handler
- Need to make entire card clickable

### 3. Top Project Cards (Lines 150-183)
- Partial implementation: Image and title area wrapped in `NuxtLink`
- Vote buttons are outside the link, preventing full-card clickability
- Need to handle vote button interaction separately

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

**B. Modify hackathon card template (lines 98-137):**
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

**C. Modify project card template (lines 150-183):**
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

#### 2. Update VoteButtons Component
If the `VoteButtons` component doesn't already have proper event handling, we may need to:
- Add `@click.stop` to vote buttons to prevent card navigation
- Ensure buttons have `data-vote-button` attribute for detection

#### 3. CSS/UX Enhancements
- Ensure `card-hover` class provides appropriate hover states
- Add `transition-colors duration-200` for smooth hover effects
- Consider adding a subtle scale transform on hover: `group-hover:scale-[1.02]`

### Backend Considerations
No backend changes required for basic clickability. Existing endpoints:
- `GET /api/hackathons` - provides hackathon data
- `GET /api/projects` - provides project data
- Detail pages already exist: `/hackathons/{id}`, `/projects/{id}`

## Implementation Steps

### Phase 1: Frontend Modifications
1. **Update script section** of `index.vue` with navigation functions
2. **Modify hackathon cards** to be fully clickable
3. **Modify project cards** with click handling that excludes vote buttons
4. **Test navigation** for both card types
5. **Verify accessibility** (keyboard navigation, focus states)

### Phase 2: UX Polish
1. **Add hover effects** to match other pages in the application
2. **Ensure consistent styling** with `hackathons/index.vue` and `projects/index.vue`
3. **Test on mobile** for touch interactions
4. **Verify vote buttons** still work correctly

### Phase 3: Testing
1. **Manual testing** of all click scenarios
2. **Keyboard navigation** testing (Tab, Enter, Space)
3. **Screen reader** compatibility check
4. **Cross-browser testing** (Chrome, Firefox, Safari)

## Files to Modify
1. `frontend3/app/pages/index.vue` - Primary changes
2. (Optional) `frontend3/app/components/VoteButtons.vue` - If event propagation fixes needed

## Success Criteria
- [ ] Clicking anywhere on a hackathon card navigates to that hackathon's detail page
- [ ] Clicking anywhere on a project card (except vote buttons) navigates to that project's detail page
- [ ] Vote buttons on project cards work independently without triggering navigation
- [ ] Keyboard navigation works (Tab to card, Enter/Space to navigate)
- [ ] Focus states are visible for accessibility
- [ ] Hover effects provide visual feedback
- [ ] Mobile touch interactions work correctly
- [ ] No regression in existing functionality

## Notes
1. The `card-hover` class already provides some hover styling. Check if it needs enhancement.
2. Consider adding `cursor-pointer` to stats cards for visual consistency (even though they're not clickable).
3. Ensure the "View Details" text in hackathon cards remains visually distinct but doesn't break the card layout.
4. Test with real data to ensure IDs are correctly passed to navigation functions.