# Backend Modular Architecture Design

## Current Issues
1. **Monolithic files**: `main.py` (82K chars), `crud.py` (50K chars), `models.py` (19K chars)
2. **Mixed concerns**: Business logic, data access, and API routes are intertwined
3. **Poor separation**: CRUD operations, business logic, and API endpoints in single files
4. **Maintainability challenges**: Large files are difficult to navigate and modify

## Current Implementation Status (as of 2026-02-22)

### ✅ **Completed**
- New directory structure created at `backend/app/`
- Repository pattern implemented with 15+ repository classes
- Domain models and schemas migrated to new structure
- API routes organized by domain in modular structure
- Core services migrated (notification, email, auth services)
- New application entry point at `app/main.py`

### ⚠️ **Partially Implemented / In Progress**
- Service layer created but not fully integrated with API routes
- Legacy code (`crud.py`, old service files) still exists and is used
- Duplication between old and new service implementations
- API routes call repositories directly instead of services
- Two `main.py` files (new and legacy) coexist

### 📋 **Remaining Work to Complete the Plan**
1. Update API routes to use service layer instead of repositories
2. Create `auth_service.py` facade for consolidated authentication
3. Update all imports to use new modular structure
4. Remove legacy `crud.py` and old service files
5. Make `app/main.py` the primary entry point
6. Update tests to use new structure

## Proposed Architecture

### Layer Separation
```
┌─────────────────────────────────────────┐
│            API Layer (Routes)           │
│  - FastAPI route definitions           │
│  - Request/response handling           │
│  - Dependency injection                │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         Service Layer (Business Logic)  │
│  - Business rules and workflows        │
│  - Transaction management              │
│  - Orchestration of repositories       │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│    Repository Layer (Data Access)       │
│  - Database operations                 │
│  - CRUD operations                     │
│  - Query building                      │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         Domain Layer (Models/Schemas)   │
│  - SQLAlchemy models                   │
│  - Pydantic schemas                    │
│  - Domain entities and relationships   │
└─────────────────────────────────────────┘
```

### Directory Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app initialization
│   ├── core/                        # Core application components
│   │   ├── __init__.py
│   │   ├── config.py               # Configuration
│   │   ├── database.py             # Database setup
│   │   ├── dependencies.py         # FastAPI dependencies
│   │   └── exceptions.py           # Custom exceptions
│   │
│   ├── api/                        # API routes (controllers)
│   │   ├── __init__.py
│   │   ├── v1/                     # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── router.py          # Main router combining all routes
│   │   │   ├── auth/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── routes.py      # Authentication endpoints
│   │   │   │   └── dependencies.py
│   │   │   ├── users/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py      # User endpoints
│   │   │   ├── projects/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py      # Project endpoints
│   │   │   ├── hackathons/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py      # Hackathon endpoints
│   │   │   ├── teams/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py      # Team endpoints
│   │   │   └── notifications/
│   │   │       ├── __init__.py
│   │   │       └── routes.py      # Notification endpoints
│   │   │
│   ├── domain/                      # Domain models and schemas
│   │   ├── __init__.py
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Base model and custom types
│   │   │   ├── user.py             # User model
│   │   │   ├── project.py          # Project model
│   │   │   ├── hackathon.py        # Hackathon model
│   │   │   ├── team.py             # Team model
│   │   │   ├── notification.py     # Notification models
│   │   │   └── shared.py           # Shared models (vote, comment, etc.)
│   │   │
│   │   └── schemas/                 # Pydantic schemas
│   │       ├── __init__.py
│   │       ├── user.py
│   │       ├── project.py
│   │       ├── hackathon.py
│   │       ├── team.py
│   │       └── notification.py
│   │
│   ├── repositories/                # Data access layer
│   │   ├── __init__.py
│   │   ├── base.py                 # Base repository class
│   │   ├── user_repository.py
│   │   ├── project_repository.py
│   │   ├── hackathon_repository.py
│   │   ├── team_repository.py
│   │   └── notification_repository.py
│   │
│   ├── services/                    # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── project_service.py
│   │   ├── hackathon_service.py
│   │   ├── team_service.py
│   │   ├── notification_service.py
│   │   ├── auth_service.py
│   │   └── file_service.py
│   │
│   └── utils/                       # Utilities and helpers
│       ├── __init__.py
│       ├── file_upload.py
│       ├── email_service.py
│       ├── template_engine.py
│       └── geocoding.py
│
├── migrations/                      # Alembic migrations (unchanged)
├── templates/                       # Email templates (unchanged)
├── i18n/                           # Internationalization (unchanged)
└── uploads/                        # Uploaded files (unchanged)
```

### Domain Boundaries

#### 1. User/Auth Domain
- **Models**: User, RefreshToken, PasswordResetToken, EmailVerificationToken
- **Schemas**: User schemas, authentication schemas
- **Services**: Authentication, password management, email verification
- **Repositories**: User repository, token repositories
- **Routes**: `/api/auth/*`, `/api/users/*`

#### 2. Project Domain
- **Models**: Project, Vote, Comment, CommentVote
- **Schemas**: Project, Vote, Comment schemas
- **Services**: Project management, voting, commenting
- **Repositories**: Project, Vote, Comment repositories
- **Routes**: `/api/projects/*`, `/api/votes/*`, `/api/comments/*`

#### 3. Hackathon Domain
- **Models**: Hackathon, HackathonRegistration
- **Schemas**: Hackathon, registration schemas
- **Services**: Hackathon management, registration
- **Repositories**: Hackathon, registration repositories
- **Routes**: `/api/hackathons/*`, `/api/registrations/*`

#### 4. Team Domain
- **Models**: Team, TeamMember, TeamInvitation
- **Schemas**: Team, member, invitation schemas
- **Services**: Team management, invitations, membership
- **Repositories**: Team, member, invitation repositories
- **Routes**: `/api/teams/*`, `/api/invitations/*`

#### 5. Notification Domain
- **Models**: NotificationType, UserNotification, UserNotificationPreference, PushSubscription
- **Schemas**: Notification schemas
- **Services**: Notification sending, preference management
- **Repositories**: Notification repositories
- **Routes**: `/api/notifications/*`, `/api/preferences/*`

#### 6. Shared/Cross-cutting Concerns
- **File Management**: File upload service
- **Email**: Email service, template engine
- **Geocoding**: Location services
- **Internationalization**: i18n middleware and translations

### Migration Strategy

#### Phase 1: Create New Structure
1. Create new directory structure alongside existing files
2. Implement base repository pattern
3. Create domain models and schemas in new structure

#### Phase 2: Incremental Migration
1. Start with one domain (e.g., User/Auth)
2. Move models, schemas, repositories, services, and routes
3. Update imports and test functionality
4. Repeat for each domain

#### Phase 3: Integration and Cleanup
1. Update main.py to use new routers
2. Remove old monolithic files
3. Update all imports across the codebase
4. Run comprehensive tests

### Benefits
1. **Improved Maintainability**: Smaller, focused files
2. **Better Separation of Concerns**: Clear boundaries between layers
3. **Enhanced Testability**: Isolated components are easier to test
4. **Scalability**: New features can be added in isolated modules
5. **Team Collaboration**: Multiple developers can work on different domains simultaneously
6. **Code Reusability**: Shared components can be reused across domains

### Considerations
1. **Backward Compatibility**: Ensure existing API endpoints remain unchanged
2. **Database Migrations**: No changes to database schema required
3. **Testing**: Comprehensive test suite needed to validate refactoring
4. **Documentation**: Update API documentation and internal docs