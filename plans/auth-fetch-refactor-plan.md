# Authentication Fetch Refactoring Plan

## Current State Analysis

### Dual Authentication Mechanisms
1. **`auth-fetch.ts` Plugin** (Global override)
   - Automatically intercepts ALL `fetch()` calls
   - Adds auth headers for backend API calls
   - Handles token refresh on 401 responses
   - Sets Content-Type: application/json for non-FormData requests
   - Only active on client-side

2. **`fetchWithAuth` Store Method** (Explicit wrapper)
   - Must be explicitly called
   - Adds auth headers if token exists
   - Handles token refresh on 401
   - Used in 67 locations already
   - Missing some features from plugin

### Direct `fetch()` Calls (36 instances)
**Public API endpoints** (can use `fetchWithAuth` safely):
- Hackathons list (`/api/hackathons`)
- Projects list (`/api/projects`)
- Users list (`/api/users`)
- Vote statistics (`/api/projects/{id}/vote-stats`)
- Newsletter subscription (`/api/newsletter/subscribe`)

**Auth-related endpoints** (need special handling):
- Login (`/api/auth/login`)
- Register (`/api/auth/register`)
- Password reset/forgot (`/api/auth/reset-password`, `/api/auth/forgot-password`)
- Email verification (`/api/auth/verify-email`)
- Token refresh (`/api/auth/refresh`)

**Service Worker calls** (special case):
- Push notifications (`/api/push/vapid-public-key`)
- Offline notifications (`/api/notifications/offline`)

## Migration Strategy

### Phase 1: Enhance `fetchWithAuth` Method
**Location**: `frontend3/app/stores/auth.ts`

**Required Improvements**:
1. **Content-Type handling**: Automatically set `application/json` for POST/PUT/PATCH requests unless body is FormData
2. **FormData detection**: Skip Content-Type header for FormData requests
3. **Better error handling**: Improve logging and error recovery
4. **URL normalization**: Handle both relative and absolute URLs consistently
5. **API detection**: Optional - check if URL is backend API to avoid adding auth headers to external services

**Implementation Approach**:
```typescript
async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
  const config = useRuntimeConfig()
  const backendUrl = config.public.apiUrl || 'http://localhost:8000'
  const fullUrl = url.startsWith('http') ? url : `${backendUrl}${url}`

  // Prepare headers
  const headers = new Headers(options.headers || {})
  
  // Add auth header if token exists
  if (token.value) {
    headers.set('Authorization', `Bearer ${token.value}`)
  }
  
  // Add Content-Type for JSON requests (POST/PUT/PATCH) if not FormData
  if (!headers.has('Content-Type') && options.method && ['POST', 'PUT', 'PATCH'].includes(options.method)) {
    const isFormData = options.body instanceof FormData
    if (!isFormData) {
      headers.set('Content-Type', 'application/json')
    }
  }
  
  let response = await fetch(fullUrl, { ...options, headers })
  
  // Handle token expiration
  if (response.status === 401 && token.value) {
    const refreshed = await refreshAccessToken()
    if (refreshed) {
      // Update auth header with new token
      headers.set('Authorization', `Bearer ${token.value}`)
      response = await fetch(fullUrl, { ...options, headers })
    }
  }
  
  return response
}
```

### Phase 2: Remove `auth-fetch.ts` Plugin
**Steps**:
1. Delete `frontend3/app/plugins/auth-fetch.ts`
2. Verify no other files import or depend on the plugin
3. Nuxt will automatically stop loading the plugin (no config changes needed)

### Phase 3: Convert All `fetch()` Calls to `fetchWithAuth`

#### Category A: Public API Calls
**Files to update**:
- `frontend3/app/pages/hackathons/index.vue` (line 328)
- `frontend3/app/pages/projects/index.vue` (lines 320, 442)
- `frontend3/app/pages/hackathons/[id]/projects.vue` (lines 197, 201, 390)
- `frontend3/app/pages/hackathons/[id]/index.vue` (lines 502, 623)
- `frontend3/app/pages/projects/[id]/edit.vue` (lines 462, 522)
- `frontend3/app/pages/users/index.vue` (lines 198, 250, 273, 325)
- `frontend3/app/stores/voting.ts` (line 132)
- `frontend3/app/components/AppFooter.vue` (line 275)

**Pattern**: Replace `fetch(`${apiUrl}/api/...`)` with `authStore.fetchWithAuth(`/api/...`)`

#### Category B: Auth-Related Calls
**Special Considerations**:
- Login/register calls should NOT have auth headers (token doesn't exist yet)
- Token refresh needs careful handling to avoid infinite loops
- Password reset/forgot are public endpoints

**Approach**:
1. Keep using `fetch()` for `/api/auth/refresh` to avoid circular dependency
2. Use `fetchWithAuth` for other auth endpoints - it won't add headers if no token exists
3. Update auth store methods to use `fetchWithAuth` where appropriate

**Files to update**:
- `frontend3/app/stores/auth.ts` (lines 163, 204, 266, 324, 487, 524)
- `frontend3/app/pages/forgot-password.vue` (line 78)
- `frontend3/app/pages/reset-password.vue` (line 145)
- `frontend3/app/pages/verify-email.vue` (line 124)

#### Category C: Service Worker Calls
**Special Case**: Service worker (`frontend3/public/sw.js`) runs outside Vue context
- Cannot access auth store
- Cannot use `fetchWithAuth`
- Should keep using plain `fetch()`

**Files to update**: None (keep as-is)

### Phase 4: Testing Strategy
1. **Authentication flow**: Login, register, logout
2. **Token refresh**: Wait for token expiration or simulate 401
3. **Public endpoints**: Verify they work without authentication
4. **Protected endpoints**: Verify they require authentication
5. **FormData requests**: Test file uploads and multipart forms
6. **Error handling**: Test network errors, server errors

### Phase 5: Cleanup and Documentation
1. Remove any unused imports
2. Update comments referencing the old plugin
3. Document the new authentication approach
4. Create guidelines for future API calls

## Risk Assessment

### High Risk Areas
1. **Token refresh infinite loop**: If `fetchWithAuth` calls `/api/auth/refresh` and gets 401, it could try to refresh again
2. **Service worker authentication**: Push notifications may fail if they require auth
3. **FormData handling**: Incorrect Content-Type could break file uploads

### Mitigation Strategies
1. Add exclusion for `/api/auth/refresh` endpoint in `fetchWithAuth`
2. Keep service worker calls as plain `fetch()` - they don't need auth
3. Test FormData uploads thoroughly

## Success Criteria
1. All API calls work correctly with authentication
2. Token refresh handles 401 responses properly
3. No infinite loops or recursion
4. Public endpoints remain accessible without authentication
5. FormData requests work correctly
6. Service worker functions normally

## Rollback Plan
If issues arise:
1. Restore `auth-fetch.ts` plugin
2. Revert changes to `fetchWithAuth` method
3. Revert converted `fetch()` calls
4. All changes are in version control

## Timeline
This refactoring can be completed in a single focused session (2-3 hours of implementation plus testing).