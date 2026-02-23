# Backend Refactoring Migration Plan

## Overview
This document outlines the plan to refactor the monolithic backend files into the new modular architecture. The goal is to migrate all remaining files from the old structure (`backend/*.py`) into the new modular structure (`backend/app/`).

## File Categorization

### 1. Authentication Files
**Files to migrate:**
- `backend/auth.py` → `backend/app/core/auth.py` (JWT utilities, token creation/verification)
- `backend/email_auth.py` → `backend/app/services/email_auth_service.py` (Email authentication logic)
- `backend/google_oauth.py` → `backend/app/services/google_oauth_service.py` (Google OAuth integration)
- `backend/github_oauth.py` → `backend/app/services/github_oauth_service.py` (GitHub OAuth integration)

**Dependencies:**
- Uses `crud.py`, `schemas.py`, `database.py`
- Needs to be updated to use new repositories and services

### 2. Database Files
**Files to migrate:**
- `backend/database.py` → `backend/app/core/database.py` (Already exists, needs updating)
- `backend/models.py` → Already migrated to `backend/app/domain/models/`

**Changes needed:**
- Update `database.py` to use SQLAlchemy 2.0 style
- Ensure compatibility with new model imports

### 3. Email Files
**Files to migrate:**
- `backend/email_service.py` → `backend/app/services/email_service.py`
- `backend/email_verification.py` → `backend/app/services/email_verification_service.py`

**Dependencies:**
- Uses `template_engine.py`, `crud.py`
- Needs to be updated to use new repositories

### 4. Notification Files
**Files to migrate:**
- `backend/notification_service.py` → `backend/app/services/notification_service.py`
- `backend/notification_preference_service.py` → `backend/app/services/notification_preference_service.py`
- `backend/push_notification_service.py` → `backend/app/services/push_notification_service.py`

**Dependencies:**
- Uses `email_service.py`, `template_engine.py`, `crud.py`
- Needs to be updated to use new repositories

### 5. Template Engine
**Files to migrate:**
- `backend/template_engine.py` → `backend/app/utils/template_engine.py`

**Dependencies:**
- Uses `i18n/translations.py`
- Should remain as a utility

### 6. CRUD Operations
**Files to migrate:**
- `backend/crud.py` → Split into repository files in `backend/app/repositories/`

**Strategy:**
- Create separate repository files for each entity:
  - `user_repository.py` (already exists)
  - `project_repository.py`
  - `hackathon_repository.py`
  - `team_repository.py`
  - `notification_repository.py`
  - `shared_repository.py` (for File, NewsletterSubscription, etc.)

### 7. Schemas
**Files to migrate:**
- `backend/schemas.py` → Already migrated to `backend/app/domain/schemas/`

**Status:**
- Most schemas already created
- Need to verify all schemas from old file are present

### 8. Utility Files
**Files to migrate:**
- `backend/file_upload.py` → Already migrated to `backend/app/utils/file_upload.py`
- `backend/geocoding.py` → Already migrated to `backend/app/utils/geocoding.py`

### 9. Test Files
**Files to keep in root:**
- `backend/test_*.py` files should remain in root for pytest compatibility
- These are test files, not part of the application

### 10. Migration Scripts
**Files to keep in root:**
- `backend/migrate_image_data.py`
- `backend/fix_*.py` scripts
- `backend/run_notification_migration.py`

## Migration Strategy

### Phase 1: Authentication & Database (Highest Priority)
1. Update `backend/app/core/database.py` with enhanced functionality from old `database.py`
2. Create `backend/app/core/auth.py` with JWT utilities
3. Create OAuth service files in `backend/app/services/`

### Phase 2: Email & Template Engine
1. Migrate `email_service.py` to `backend/app/services/`
2. Migrate `template_engine.py` to `backend/app/utils/`
3. Update imports to use new modular structure

### Phase 3: Notification System
1. Migrate notification services to `backend/app/services/`
2. Update dependencies to use new email service and repositories

### Phase 4: CRUD Operations Split
1. Analyze `crud.py` functions by entity
2. Create dedicated repository files
3. Update all service files to use new repositories

### Phase 5: Integration & Testing
1. Update `backend/app/main.py` to use all refactored components
2. Update `backend/main.py` (old entry point) to import from new structure
3. Run comprehensive tests

## Dependencies Resolution

### Circular Import Prevention
The new modular structure should follow this dependency flow:
```
API Routes → Services → Repositories → Models
                    ↓
              Utilities (auth, email, etc.)
```

### Import Updates Required
All migrated files need to update their imports:
- `import crud` → `from app.repositories import user_repository, project_repository, ...`
- `import models` → `from app.domain.models import User, Project, ...`
- `import schemas` → `from app.domain.schemas import UserCreate, UserUpdate, ...`
- `from database import get_db` → `from app.core.database import get_db`

## Testing Strategy

### Unit Tests
- Keep existing test files in root
- Update test imports to use new modular structure
- Ensure all tests pass after migration

### Integration Tests
- Test API endpoints with refactored services
- Verify authentication flow works
- Test notification delivery

## Risk Mitigation

### Backup Strategy
1. Create backup of current working state
2. Use Git branches for incremental migration
3. Test each phase independently before proceeding

### Rollback Plan
If issues arise:
1. Revert to previous Git commit
2. Restore from backup
3. Fix issues in isolation before reattempting

## Timeline & Milestones

### Milestone 1: Authentication Working
- JWT authentication functional
- OAuth login working
- Database connections established

### Milestone 2: Core Services Operational
- Email service sending emails
- Template engine rendering correctly
- Basic CRUD operations via repositories

### Milestone 3: Full Feature Parity
- All notification channels working
- File upload functional
- Geocoding service operational

### Milestone 4: Performance & Cleanup
- Optimize imports and dependencies
- Remove old files from root (or keep as compatibility layer)
- Update documentation

## Success Criteria
1. All API endpoints function as before
2. No breaking changes to frontend
3. All existing tests pass
4. Improved code organization and maintainability
5. Clear separation of concerns in modular architecture