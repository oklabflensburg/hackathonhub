# Missing Endpoints Implementation Plan

## Overview
During the refactoring from monolithic `backend/main.py` to modular architecture, several API endpoints were not migrated to the new structure. This document outlines the missing endpoints and provides an implementation plan.

## Missing Endpoints Identified

### 1. Project Domain
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/projects/{project_id}/vote-stats` | GET | Get vote statistics for a project | **MISSING** |
| `/api/projects/{project_id}/vote` | DELETE | Remove user's vote from a project | **MISSING** |
| `/api/projects/{project_id}/view` | POST | Increment project view count | **MISSING** |
| `/api/projects/{project_id}/comments` | POST | Create a comment on a project | **MISSING** |
| `/api/comments/{comment_id}` | PUT | Update a comment | **MISSING** |
| `/api/comments/{comment_id}` | DELETE | Delete a comment | **MISSING** |
| `/api/comments/{comment_id}/vote` | POST | Vote on a comment | **MISSING** |
| `/api/comments/{comment_id}/vote` | DELETE | Remove vote from a comment | **MISSING** |

### 2. User Domain
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/users/me/votes` | GET | Get current user's votes | **MISSING** |
| `/api/users/me/projects` | GET | Get current user's projects | **MISSING** |
| `/api/users/me/stats` | GET | Get current user's statistics | **MISSING** |
| `/api/users/me/teams/{hackathon_id}` | GET | Get user's teams for specific hackathon | **MISSING** |
| `/api/users/{user_id}/teams` | GET | Get a user's teams | **MISSING** |

### 3. Authentication Domain
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/auth/register` | POST | Register new user | **MISSING** |
| `/api/auth/forgot-password` | POST | Request password reset | **MISSING** |
| `/api/auth/reset-password` | POST | Reset password with token | **MISSING** |
| `/api/auth/verify-email` | POST | Verify email address | **MISSING** |
| `/api/auth/resend-verification` | POST | Resend verification email | **MISSING** |
| `/api/auth/github` | GET | GitHub OAuth initiation | **MISSING** |
| `/api/auth/github/callback` | GET | GitHub OAuth callback | **MISSING** |

### 4. Other Endpoints
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/upload` | POST | File upload endpoint | **MISSING** |
| `/api/newsletter/subscribe` | POST | Subscribe to newsletter | **IMPLEMENTED** (Fixed 422 error - now accepts JSON body) |
| `/api/newsletter/unsubscribe` | POST | Unsubscribe from newsletter | **IMPLEMENTED** (Fixed 422 error - now accepts JSON body) |

## Priority Classification

### High Priority (Blocking Frontend Functionality)
1. `GET /api/projects/{project_id}/vote-stats` - Frontend is getting 404 errors
2. `DELETE /api/projects/{project_id}/vote` - Frontend voting functionality incomplete
3. `GET /api/users/me/votes` - Needed for user vote state

### Medium Priority (Core Features)
4. `POST /api/projects/{project_id}/comments` - Commenting functionality
5. `PUT /api/comments/{comment_id}` - Comment editing
6. `DELETE /api/comments/{comment_id}` - Comment deletion
7. `POST /api/auth/register` - User registration
8. `POST /api/auth/forgot-password` - Password recovery
9. `POST /api/auth/reset-password` - Password reset

### Low Priority (Enhancements)
10. Remaining endpoints for completeness

## Implementation Strategy

### Phase 1: High Priority Endpoints
Implement the most critical missing endpoints that are causing frontend issues.

**Files to modify:**
1. `backend/app/api/v1/projects/routes.py` - Add vote-stats and DELETE vote endpoints
2. `backend/app/api/v1/users/routes.py` - Add /me/votes endpoint
3. Update corresponding services if needed

### Phase 2: Comment Endpoints
Implement comment-related endpoints in a new or existing module.

**Options:**
- Add to `backend/app/api/v1/projects/routes.py` (nested under projects)
- Create separate `comments` module
- Follow existing pattern in legacy code

### Phase 3: Authentication Endpoints
Implement missing auth endpoints in the auth module.

**Files to modify:**
1. `backend/app/api/v1/auth/routes.py` - Add register, password reset, etc.
2. Ensure corresponding services exist

### Phase 4: Remaining Endpoints
Complete implementation of all other missing endpoints.

## Technical Details

### 1. Vote-Stats Endpoint Implementation
```python
@router.get("/{project_id}/vote-stats")
async def get_project_vote_stats(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get vote statistics for a project."""
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "project_id": project_id,
        "upvotes": project.upvote_count or 0,
        "downvotes": project.downvote_count or 0,
        "total_score": project.vote_score or 0,
        "user_vote": None  # Public endpoint doesn't include user vote
    }
```

### 2. DELETE Vote Endpoint Implementation
```python
@router.delete("/{project_id}/vote")
async def remove_vote(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Remove user's vote from a project."""
    # Check if project exists
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Remove vote using service
    success = project_service.remove_vote(db, project_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Vote not found")
    
    # Get updated project
    project = project_service.get_project(db, project_id)
    
    return {
        "message": "Vote removed successfully",
        "project_stats": {
            "project_id": project_id,
            "upvotes": project.upvote_count or 0,
            "downvotes": project.downvote_count or 0,
            "total_score": project.vote_score or 0,
            "user_vote": None
        }
    }
```

### 3. User Votes Endpoint Implementation
```python
@router.get("/me/votes")
async def get_user_votes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get current user's votes."""
    # Implementation depends on vote repository/service
    votes = vote_repository.get_by_user(db, current_user.id)
    return votes
```

## Dependencies and Services Needed

1. **Vote Service Methods:**
   - `get_vote_stats(project_id)` - Already exists in project_service?
   - `remove_vote(project_id, user_id)` - Needs implementation

2. **Comment Service:**
   - May need new `comment_service.py` or extend `project_service.py`

3. **Auth Service:**
   - Registration, password reset, email verification methods

## Testing Strategy

1. **Unit Tests:** Test each endpoint individually
2. **Integration Tests:** Test full flow (vote → get stats → remove vote)
3. **Frontend Integration:** Verify frontend works with new endpoints

## Migration Considerations

1. **Backward Compatibility:** Ensure response structures match legacy endpoints
2. **Database Schema:** No changes needed
3. **Error Handling:** Consistent with existing patterns

## Next Steps

1. Review this plan with stakeholders
2. Prioritize implementation based on business needs
3. Begin implementation in Code mode
4. Test thoroughly before deployment

## References

- Legacy implementation: `backend/main.py`
- Current modular structure: `backend/app/api/v1/`
- Frontend expectations: `frontend3/app/stores/voting.ts`