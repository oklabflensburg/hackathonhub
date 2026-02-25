# Vote Functionality Fix Implementation Plan

## Problem Statement
Users can vote multiple times on the same project due to race conditions and insufficient frontend debouncing. The vote function should properly handle concurrent requests and prevent multiple votes.

## Identified Issues

### Backend Issues (`backend/app/api/v1/projects/routes.py`):
1. **Race Condition**: The `vote_for_project` endpoint uses a read-modify-write pattern vulnerable to concurrent requests
2. **Error Handling**: Database integrity errors (unique constraint violations) are not handled gracefully
3. **Transaction Isolation**: No explicit transaction management for atomic operations

### Frontend Issues:
1. **Inconsistent Loading State**: `VoteButtons.vue` uses local `isVotingInProgress` instead of store's `isLoading` map
2. **No Debouncing**: Rapid clicks can queue multiple vote requests
3. **State Synchronization**: UI doesn't immediately reflect vote state changes

## Solution Design

### Backend Fixes:

#### 1. Atomic Vote Operation
Replace the current read-modify-write logic with an atomic database operation using PostgreSQL's `ON CONFLICT` clause or SQLAlchemy's `merge` operation.

**Current flow:**
1. Check if vote exists
2. If exists: update or delete
3. If not exists: create

**Proposed flow:**
1. Use `db.merge()` or upsert operation
2. Handle conflicts with proper error catching
3. Use database transaction for atomicity

#### 2. Error Handling
- Catch `IntegrityError` for unique constraint violations
- Return appropriate error messages
- Implement retry logic or conflict resolution

#### 3. Transaction Management
- Use explicit transaction blocks
- Ensure proper rollback on errors

### Frontend Fixes:

#### 1. Loading State Synchronization
- Use `votingStore.isVotingInProgress(projectId)` instead of local state
- Ensure store properly tracks loading state per project

#### 2. Debouncing
- Add debounce to `handleVote` function (e.g., 500ms)
- Prevent multiple rapid clicks

#### 3. Optimistic UI Updates
- Immediately update UI when vote is clicked
- Roll back if API call fails

## Implementation Steps

### Phase 1: Backend Fixes
1. Modify `vote_for_project` endpoint in `routes.py`:
   - Add transaction handling
   - Implement proper error handling for integrity errors
   - Use atomic operations where possible

2. Update `VoteRepository` methods if needed

### Phase 2: Frontend Fixes  
1. Update `VoteButtons.vue`:
   - Use store loading state
   - Add debouncing
   - Implement optimistic updates

2. Update `voting.ts` store:
   - Ensure `isLoading` map is properly maintained
   - Add methods for optimistic state updates

### Phase 3: Testing
1. Test concurrent voting scenarios
2. Test rapid clicking behavior
3. Verify UI state consistency
4. Test error scenarios

## Code Changes Overview

### Backend Changes (`backend/app/api/v1/projects/routes.py`):
```python
@router.post("/{project_id}/vote")
async def vote_for_project(
    project_id: int,
    request: Request,
    vote_type: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Vote for a project with proper concurrency handling."""
    try:
        # Normalize vote type
        vote_type = vote_type.lower().strip()
        
        # Map 'up'/'down' to 'upvote'/'downvote'
        if vote_type == 'up':
            vote_type = 'upvote'
        elif vote_type == 'down':
            vote_type = 'downvote'
            
        # Validate vote type
        if vote_type not in ["upvote", "downvote"]:
            raise_bad_request(
                locale,
                validation_key="vote_type_must_be",
                option1="upvote",
                option2="downvote"
            )
            
        # Check if project exists
        project = project_repository.get(db, project_id)
        if not project:
            raise_not_found(locale, "project")
            
        # Use transaction for atomic operation
        try:
            # Check existing vote and perform atomic update
            existing_vote = vote_repository.get_user_vote_for_project(
                db, current_user.id, project_id
            )
            
            if existing_vote:
                if existing_vote.vote_type == vote_type:
                    # Same vote type - remove the vote
                    vote_repository.delete(db, id=existing_vote.id)
                    message = f"Removed {vote_type}"
                else:
                    # Change vote type
                    existing_vote.vote_type = vote_type
                    db.commit()
                    message = f"Changed vote to {vote_type}"
            else:
                # Create new vote with conflict handling
                try:
                    vote_repository.create(db, obj_in={
                        "user_id": current_user.id,
                        "project_id": project_id,
                        "vote_type": vote_type
                    })
                    message = f"Added {vote_type}"
                except IntegrityError:
                    # Race condition: vote was created by another request
                    db.rollback()
                    # Retry or return current state
                    existing_vote = vote_repository.get_user_vote_for_project(
                        db, current_user.id, project_id
                    )
                    if existing_vote:
                        message = f"Already voted {existing_vote.vote_type}"
                    else:
                        # Should not happen, but retry once
                        vote_repository.create(db, obj_in={
                            "user_id": current_user.id,
                            "project_id": project_id,
                            "vote_type": vote_type
                        })
                        message = f"Added {vote_type}"
                        
        except IntegrityError as e:
            db.rollback()
            raise_bad_request(locale, "vote_conflict")
            
        # Update vote counts
        vote_repository.update_vote_counts(db, project_id)
        
        # Get updated vote stats
        project = project_repository.get(db, project_id)
        db.refresh(project)
        
        return {
            "message": message,
            "project_id": project_id,
            "vote_type": vote_type,
            "project_stats": {
                "upvotes": getattr(project, 'upvote_count', 0),
                "downvotes": getattr(project, 'downvote_count', 0),
                "total_score": getattr(project, 'vote_score', 0)
            }
        }
        
    except Exception as e:
        # Handle other errors
        raise_internal_server_error(locale, "vote", entity="project")
```

### Frontend Changes (`frontend3/app/components/VoteButtons.vue`):
```typescript
// Add debouncing
import { debounce } from 'lodash-es'

const handleVote = debounce(async (voteType: 'up' | 'down') => {
  if (!authStore.isAuthenticated) {
    uiStore.showError(t('votes.pleaseLogin'))
    return
  }

  // Use store loading state
  if (votingStore.isVotingInProgress(props.projectId)) return

  try {
    // Optimistically update UI
    const currentUserVote = userVote.value
    const currentUpvotes = upvotes.value
    const currentDownvotes = downvotes.value
    
    // If user is clicking the same vote type again, remove the vote
    if (currentUserVote === voteType) {
      // Optimistically update
      // ... update local state
      await votingStore.removeVote(props.projectId)
      uiStore.showSuccess(t('votes.voteRemoved'))
    } else {
      // Optimistically update  
      // ... update local state
      await votingStore.voteForProject(props.projectId, voteType)
      uiStore.showSuccess(voteType === 'up' ? t('votes.upvotedSuccessfully') : t('votes.downvotedSuccessfully'))
    }
  } catch (error) {
    // Revert optimistic update on error
    uiStore.showError(error instanceof Error ? error.message : t('votes.failedToVote'))
  }
}, 500, { leading: true, trailing: false })
```

## Success Criteria
1. Users cannot vote multiple times on the same project concurrently
2. Rapid clicking doesn't cause multiple vote requests
3. UI properly reflects voting state at all times
4. Error cases are handled gracefully with appropriate user feedback

## Rollback Plan
If issues arise:
1. Revert backend changes to original implementation
2. Revert frontend changes
3. Keep database schema unchanged (unique constraint remains)