# FastAPI Status Codes and i18n Standardization Plan

## Current State Analysis

### 1. Status Code Usage Patterns
- **Files using FastAPI status constants** (correct pattern):
  - `backend/app/api/v1/auth/routes.py` - Uses `status.HTTP_401_UNAUTHORIZED`, `status.HTTP_403_FORBIDDEN`, etc.
  - `backend/app/core/auth.py` - Uses `status.HTTP_401_UNAUTHORIZED`

- **Files using numeric status codes** (needs updating):
  - `backend/app/api/v1/projects/routes.py` - Uses `status_code=404`, `status_code=403`, etc.
  - `backend/app/api/v1/teams/routes.py` - Uses `status_code=404`, `status_code=403`, etc.
  - `backend/app/api/v1/users/routes.py` - Uses `status_code=404`, `status_code=403`, etc.
  - `backend/app/api/v1/hackathons/routes.py` - Uses `status_code=404`, `status_code=403`, etc.
  - `backend/app/api/v1/comments/routes.py` - Uses `status_code=404`, `status_code=403`, etc.
  - `backend/app/api/v1/notifications/routes.py` - Uses `status_code=404`, `status_code=500`, etc.
  - `backend/app/services/file_service.py` - Uses `status_code=404`, `status_code=403`, etc.
  - `backend/app/utils/file_upload.py` - Uses `status_code=400`, `status_code=500`, etc.
  - `backend/app/core/auth.py` (mixed - some numeric, some constants)

### 2. i18n Translation System
- **Existing translations**: Located in `backend/app/i18n/translations.py`
- **Available error keys** (in `errors` category):
  - `project_not_found`, `hackathon_not_found`, `comment_not_found`, `vote_not_found`
  - `user_not_found`, `unauthorized`, `forbidden`, `invalid_token`
  - `token_expired`, `invalid_vote_type`, `missing_auth_header`
  - `token_refresh_failed`, `only_owner_can_update`, `only_owner_can_delete`
  - `only_owner_or_team_can_update`, `only_comment_author_can_update`
  - `only_comment_author_can_delete`, `only_hackathon_owner_can_update`
  - `already_registered`, `email_already_subscribed`, `email_not_found`
  - `failed_to_subscribe`, `validation_error`, `server_error`
  - `geocoding_failed`, `github_auth_failed`, `oauth_failed`

- **Missing translations**: Many error messages in the codebase don't have corresponding translation keys.

### 3. i18n Middleware Configuration
- **Configured in**: `backend/main.py` (legacy file) via `app.add_middleware(LocaleMiddleware)`
- **Not configured in**: `backend/app/main.py` (modular structure)
- **Middleware function**: `get_locale_from_request(request)` available to get locale from request state

## Standardization Plan

### Phase 1: Update Import Statements
All files using HTTPException need to import `status` from FastAPI:
```python
from fastapi import APIRouter, Depends, HTTPException, status
```

### Phase 2: Map Numeric Codes to FastAPI Constants
Common conversions needed:
- `404` → `status.HTTP_404_NOT_FOUND`
- `403` → `status.HTTP_403_FORBIDDEN`
- `401` → `status.HTTP_401_UNAUTHORIZED`
- `400` → `status.HTTP_400_BAD_REQUEST`
- `500` → `status.HTTP_500_INTERNAL_SERVER_ERROR`
- `501` → `status.HTTP_501_NOT_IMPLEMENTED`

### Phase 3: i18n Integration Strategy
Two approaches for error messages:

**Option A: Direct translation in HTTPException**
```python
from app.i18n.translations import get_translation
from app.i18n.middleware import get_locale_from_request

locale = get_locale_from_request(request)
detail = get_translation("errors.project_not_found", locale)
raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
```

**Option B: Helper function for common patterns**
```python
def raise_not_found(request: Request, entity: str):
    locale = get_locale_from_request(request)
    detail = get_translation(f"errors.{entity}_not_found", locale)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
```

### Phase 4: Add Missing Translation Keys
Based on code analysis, we need to add translations for:
- "Not authorized to update this project"
- "Not authorized to delete this project"
- "Failed to delete project"
- "Vote type must be 'upvote' or 'downvote'"
- "Cannot upload avatar for another user"
- "File too large. Max size is {max_size}MB"
- "File type not allowed. Allowed types: {types}"
- And many more...

### Phase 5: Ensure i18n Middleware is Active
Update `backend/app/main.py` to include i18n middleware:
```python
from app.i18n.middleware import create_i18n_middleware
app.add_middleware(create_i18n_middleware())
```

## Implementation Priority

### High Priority (Core Routes)
1. `backend/app/api/v1/projects/routes.py` - 15+ HTTPException calls
2. `backend/app/api/v1/teams/routes.py` - 20+ HTTPException calls
3. `backend/app/api/v1/users/routes.py` - 10+ HTTPException calls
4. `backend/app/api/v1/hackathons/routes.py` - 10+ HTTPException calls

### Medium Priority (Other Routes)
5. `backend/app/api/v1/comments/routes.py`
6. `backend/app/api/v1/notifications/routes.py`
7. `backend/app/api/v1/auth/routes.py` (already has status constants, needs i18n)

### Low Priority (Services & Utilities)
8. `backend/app/services/file_service.py`
9. `backend/app/utils/file_upload.py`
10. `backend/app/core/auth.py` (partial update)

## Success Criteria
1. All HTTPException calls use FastAPI status constants
2. All error messages are translatable via i18n system
3. i18n middleware is properly configured in main app
4. Translations exist for all error messages in both English and German
5. Code maintains backward compatibility

## Risks and Considerations
1. **Breaking changes**: Changing error message formats could affect frontend
2. **Performance**: i18n lookups add minimal overhead
3. **Testing**: Need to verify translations work correctly
4. **Fallback**: Ensure English fallback when translations missing