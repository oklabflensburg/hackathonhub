# Implementation Checklist: FastAPI Status Codes & i18n Integration

## Phase 1: Foundation Setup

### 1.1 Create i18n Helper Module
- [ ] Create `backend/app/i18n/helpers.py` with helper functions
- [ ] Implement `raise_i18n_http_exception()` function
- [ ] Add common shortcuts: `raise_not_found()`, `raise_forbidden()`, etc.
- [ ] Add locale extraction helper: `get_locale_from_request()`

### 1.2 Create Locale Dependency
- [ ] Create `backend/app/i18n/dependencies.py`
- [ ] Implement `get_locale()` dependency function
- [ ] Test dependency injection pattern

### 1.3 Update Translations Dictionary
- [ ] Add missing error message translations to `backend/app/i18n/translations.py`
- [ ] Ensure all existing error messages have translation keys
- [ ] Add parameterized translations for dynamic content

### 1.4 Configure i18n Middleware
- [ ] Check if `backend/app/main.py` includes i18n middleware
- [ ] Add middleware if missing: `app.add_middleware(create_i18n_middleware())`
- [ ] Verify middleware works with Accept-Language header

## Phase 2: Update Route Files (High Priority)

### 2.1 Update `backend/app/api/v1/projects/routes.py`
- [ ] Add import: `from fastapi import status`
- [ ] Add import: `from app.i18n.dependencies import get_locale`
- [ ] Add import: `from app.i18n.helpers import raise_not_found, raise_forbidden`
- [ ] Update all HTTPException calls to use status constants
- [ ] Add `locale: str = Depends(get_locale)` to route functions
- [ ] Replace hardcoded error messages with i18n helpers
- [ ] Test all project endpoints

**Specific updates needed:**
- Line 45: `status_code=404` → `status_code=status.HTTP_404_NOT_FOUND`
- Line 83: `status_code=403` → `status_code=status.HTTP_403_FORBIDDEN`
- Line 92: `status_code=404` → `status_code=status.HTTP_404_NOT_FOUND`
- Line 113: `status_code=403` → `status_code=status.HTTP_403_FORBIDDEN`
- Line 120: `status_code=500` → `status_code=status.HTTP_500_INTERNAL_SERVER_ERROR`
- Line 147: `status_code=400` → `status_code=status.HTTP_400_BAD_REQUEST`
- Line 154: `status_code=404` → `status_code=status.HTTP_404_NOT_FOUND`
- Line 199: `status_code=404` → `status_code=status.HTTP_404_NOT_FOUND`
- Line 228: `status_code=404` → `status_code=status.HTTP_404_NOT_FOUND`
- Line 251: `status_code=404` → `status_code=status.HTTP_404_NOT_FOUND`
- Line 259: `status_code=404` → `status_code=status.HTTP_404_NOT_FOUND`
- Line 293: `status_code=404` → `status_code=status.HTTP_404_NOT_FOUND`
- Line 333: `status_code=404` → `status_code=status.HTTP_404_NOT_FOUND`

### 2.2 Update `backend/app/api/v1/teams/routes.py`
- [ ] Add import: `from fastapi import status`
- [ ] Add import: `from app.i18n.dependencies import get_locale`
- [ ] Add import: `from app.i18n.helpers import raise_not_found, raise_forbidden`
- [ ] Update all HTTPException calls to use status constants
- [ ] Add locale dependency to route functions
- [ ] Replace hardcoded error messages with i18n helpers
- [ ] Test all team endpoints

### 2.3 Update `backend/app/api/v1/users/routes.py`
- [ ] Add import: `from fastapi import status`
- [ ] Add import: `from app.i18n.dependencies import get_locale`
- [ ] Add import: `from app.i18n.helpers import raise_not_found, raise_forbidden`
- [ ] Update all HTTPException calls to use status constants
- [ ] Add locale dependency to route functions
- [ ] Replace hardcoded error messages with i18n helpers
- [ ] Test all user endpoints

### 2.4 Update `backend/app/api/v1/hackathons/routes.py`
- [ ] Add import: `from fastapi import status`
- [ ] Add import: `from app.i18n.dependencies import get_locale`
- [ ] Add import: `from app.i18n.helpers import raise_not_found, raise_forbidden`
- [ ] Update all HTTPException calls to use status constants
- [ ] Add locale dependency to route functions
- [ ] Replace hardcoded error messages with i18n helpers
- [ ] Test all hackathon endpoints

## Phase 3: Update Route Files (Medium Priority)

### 3.1 Update `backend/app/api/v1/comments/routes.py`
- [ ] Add import: `from fastapi import status`
- [ ] Add import: `from app.i18n.dependencies import get_locale`
- [ ] Add import: `from app.i18n.helpers import raise_not_found, raise_forbidden`
- [ ] Update all HTTPException calls to use status constants
- [ ] Add locale dependency to route functions
- [ ] Replace hardcoded error messages with i18n helpers
- [ ] Test all comment endpoints

### 3.2 Update `backend/app/api/v1/notifications/routes.py`
- [ ] Add import: `from fastapi import status`
- [ ] Add import: `from app.i18n.dependencies import get_locale`
- [ ] Add import: `from app.i18n.helpers import raise_not_found, raise_forbidden`
- [ ] Update all HTTPException calls to use status constants
- [ ] Add locale dependency to route functions
- [ ] Replace hardcoded error messages with i18n helpers
- [ ] Test all notification endpoints

### 3.3 Update `backend/app/api/v1/auth/routes.py`
- [ ] Already uses status constants, needs i18n integration
- [ ] Add import: `from app.i18n.dependencies import get_locale`
- [ ] Add import: `from app.i18n.helpers import raise_i18n_http_exception`
- [ ] Add locale dependency to route functions
- [ ] Replace hardcoded error messages with i18n helpers
- [ ] Test all auth endpoints with different languages

## Phase 4: Update Service Layer

### 4.1 Update `backend/app/services/file_service.py`
- [ ] Add import: `from fastapi import status`
- [ ] Update HTTPException calls to use status constants
- [ ] Add locale parameter to functions that raise exceptions
- [ ] Use i18n helpers for error messages
- [ ] Test file upload functionality

### 4.2 Update `backend/app/utils/file_upload.py`
- [ ] Add import: `from fastapi import status`
- [ ] Update HTTPException calls to use status constants
- [ ] Add locale parameter to methods
- [ ] Use i18n helpers for error messages
- [ ] Test file validation

### 4.3 Update `backend/app/core/auth.py`
- [ ] Already has some status constants, standardize all
- [ ] Update remaining numeric codes to status constants
- [ ] Add i18n support for auth error messages
- [ ] Test authentication flows

## Phase 5: Update Remaining Files

### 5.1 Update `backend/app/api/v1/me/routes.py`
- [ ] Add import: `from fastapi import status`
- [ ] Update HTTPException calls to use status constants
- [ ] Add i18n support

### 5.2 Update `backend/app/api/v1/compatibility/routes.py`
- [ ] Add import: `from fastapi import status`
- [ ] Update HTTPException calls to use status constants
- [ ] Add i18n support

### 5.3 Update `backend/app/api/v1/push/routes.py`
- [ ] Add import: `from fastapi import status`
- [ ] Update HTTPException calls to use status constants
- [ ] Add i18n support

## Phase 6: Testing and Validation

### 6.1 Unit Testing
- [ ] Test each updated route with English locale
- [ ] Test each updated route with German locale
- [ ] Test each updated route with unsupported locale (should fallback to English)
- [ ] Test parameterized translations with different values
- [ ] Test error response formats

### 6.2 Integration Testing
- [ ] Test complete authentication flow with i18n
- [ ] Test file upload with error messages in different languages
- [ ] Test permission errors with localized messages
- [ ] Test validation errors with localized messages

### 6.3 Regression Testing
- [ ] Verify all existing functionality still works
- [ ] Test backward compatibility of error response formats
- [ ] Ensure no breaking changes for frontend consumers

## Phase 7: Documentation and Cleanup

### 7.1 Update Documentation
- [ ] Update API documentation with i18n support notes
- [ ] Document new i18n helper functions
- [ ] Add examples of using i18n in route functions
- [ ] Update README with i18n configuration instructions

### 7.2 Code Quality
- [ ] Run linter on all updated files
- [ ] Fix any formatting issues
- [ ] Ensure consistent import ordering
- [ ] Remove any unused imports

### 7.3 Final Verification
- [ ] Verify all HTTPException calls use FastAPI status constants
- [ ] Verify all error messages are translatable via i18n
- [ ] Verify i18n middleware is properly configured
- [ ] Verify translations exist for all error messages
- [ ] Perform final end-to-end testing

## Success Metrics

1. **100% of HTTPException calls** use FastAPI status constants (not numeric codes)
2. **100% of error messages** are translatable via i18n system
3. **i18n middleware** is active and working in main application
4. **Translations exist** for all error messages in both English and German
5. **All existing tests pass** with updated code
6. **API responses maintain backward compatibility** where possible

## Rollback Plan

If issues arise during implementation:
1. Revert changes to one file at a time
2. Keep i18n helper module as standalone (can be disabled)
3. Maintain numeric status codes as fallback during transition
4. Use feature flags if needed for gradual rollout