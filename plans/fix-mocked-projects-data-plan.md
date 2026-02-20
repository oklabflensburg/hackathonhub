# Fix Mocked Projects Data Plan

## Problem Statement
Under `https://hackathonhub.oklabflensburg.de/hackathons/8/projects`, the projects view shows mocked/random data instead of real API data. Issues include:
- Placeholder gradient images instead of real project images
- Random vote, comment, and view counts that change on refresh
- Single owner shown instead of actual team members
- Default tech stack (`['Python', 'JavaScript', 'React', 'Node.js']`) instead of actual technologies

## Root Causes Identified

### 1. Missing API Endpoint
**File**: `frontend3/app/pages/hackathons/[id]/projects.vue` (lines 195-209)
**Issue**: Frontend calls `/api/projects?hackathon_id=${id}` but this endpoint doesn't exist in `backend/main.py`
**Current Behavior**: 
- API returns 404 or error
- Frontend falls back to fetching all projects and filtering locally
- If that fails, uses empty array

### 2. Data Transformation Issues
**File**: `frontend3/app/pages/hackathons/[id]/projects.vue` (lines 227-328)
**Issues**:
- Lines 323-325: Uses `Math.random()` for votes, comments, and views
- Lines 237-239: Team data only shows owner, not actual team members
- Lines 242-244: Default tech stack when technologies not provided
- Lines 247-304: Generates SVG placeholder images instead of using real images

### 3. Backend API Limitations
**File**: `backend/main.py` (lines 98-107)
**Issue**: `/api/projects` endpoint doesn't accept `hackathon_id` query parameter
**Note**: `crud.get_projects_by_hackathon()` function exists but isn't exposed as API endpoint

## Solution Plan

### Phase 1: Backend API Enhancement
1. **Add hackathon_id parameter to /api/projects endpoint**
   - Modify `get_projects()` function in `backend/main.py`
   - Add optional `hackathon_id: Optional[int] = Query(None)` parameter
   - Use `crud.get_projects_by_hackathon()` when hackathon_id is provided
   - Update OpenAPI documentation

2. **Ensure proper data serialization**
   - Check that all necessary fields are included in `schemas.Project`
   - Verify team member data is available through relationships

### Phase 2: Frontend Data Transformation Fix
1. **Remove random data generation**
   - Replace `Math.random()` calls with actual API data
   - Use `apiProject.upvote_count`, `apiProject.comment_count`, `apiProject.view_count`

2. **Fix team data display**
   - Query team members from API if available
   - Fall back to owner-only display if team data not available

3. **Fix tech stack parsing**
   - Properly parse `technologies` field (comma-separated string)
   - Handle empty/null cases gracefully

4. **Fix image handling**
   - Use `image_path` from API when available
   - Generate proper image URLs using `config.public.apiUrl`
   - Only use placeholders when no image exists

### Phase 3: Additional Improvements
1. **Add loading states and error handling**
2. **Implement proper caching for project data**
3. **Add pagination support for large hackathons**
4. **Update documentation for the changes**

## Implementation Details

### Backend Changes (`backend/main.py`)

```python
@app.get("/api/projects", response_model=List[schemas.Project])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    search: str = Query(None, description="Search query for full-text search"),
    hackathon_id: Optional[int] = Query(None, description="Filter by hackathon ID"),
    db: Session = Depends(get_db)
):
    """Get all hackathon projects with optional filters"""
    if hackathon_id:
        projects = crud.get_projects_by_hackathon(db, hackathon_id=hackathon_id, skip=skip, limit=limit)
    else:
        projects = crud.get_projects(db, skip=skip, limit=limit, search=search)
    return projects
```

### Frontend Changes (`frontend3/app/pages/hackathons/[id]/projects.vue`)

1. **Update fetchProjects function** (lines 187-224):
   - Remove fallback to fetching all projects
   - Handle 404 gracefully (empty results)

2. **Rewrite transformProject function** (lines 227-328):
   ```javascript
   const transformProject = (apiProject: any) => {
     // Use real API data
     const votes = apiProject.upvote_count || apiProject.vote_score || 0
     const comments = apiProject.comment_count || 0
     const views = apiProject.view_count || 0
     
     // Parse technologies
     const techStack = apiProject.technologies ?
       apiProject.technologies.split(',').map((t: string) => t.trim()).filter(Boolean) :
       []
     
     // Generate proper image URL
     const backendUrl = config.public.apiUrl || 'http://localhost:8000'
     const image = apiProject.image_path ?
       `${backendUrl}${apiProject.image_path.startsWith('/') ? '' : '/'}${apiProject.image_path}` :
       generatePlaceholderImage(apiProject.id || 0, apiProject.title || 'Untitled')
     
     return {
       id: apiProject.id,
       name: apiProject.title || 'Untitled Project',
       description: apiProject.description || 'No description available.',
       image: image,
       status: determineStatus(apiProject.status),
       team: getTeamMembers(apiProject),
       techStack: techStack,
       votes: votes,
       comments: comments,
       views: views,
       hasVoted: false // Would come from user's vote status
     }
   }
   ```

## Testing Strategy

1. **Test with hackathon ID 8**
   - Verify API endpoint returns correct projects
   - Check that data transformation works correctly
   - Ensure no random data appears

2. **Test edge cases**
   - Hackathon with no projects
   - Projects without images
   - Projects without technologies
   - Large number of projects (pagination)

3. **Browser testing**
   - Check console for API errors
   - Verify images load correctly
   - Test search functionality

## Success Criteria

1. ✅ Projects show real data from database
2. ✅ No random numbers on page refresh
3. ✅ Real project images (or appropriate placeholders)
4. ✅ Actual team members displayed when available
5. ✅ Correct tech stacks from project data
6. ✅ Proper error handling for missing data

## Files to Modify

### Backend:
- `backend/main.py` - Add hackathon_id parameter to get_projects endpoint
- `backend/crud.py` - Ensure get_projects_by_hackathon works correctly

### Frontend:
- `frontend3/app/pages/hackathons/[id]/projects.vue` - Fix data transformation
- Potentially `frontend3/app/stores/projects.ts` if project store exists

## Timeline
This fix should be implemented as a high priority since it affects the core functionality of viewing hackathon projects.