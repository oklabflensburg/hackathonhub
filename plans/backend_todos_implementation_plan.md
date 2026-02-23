# Backend TODOs Implementation Plan

## Overview
This document outlines a comprehensive plan to implement all TODOs found in the backend folder, following existing architectural plans and priorities. The implementation will complete the backend refactoring and make all API endpoints functional.

## TODOs Categorization

### 1. Authentication TODOs (2 items)
**Location**: `backend/app/core/auth.py`
- **TODO 1**: Implement refresh token revocation and creation (lines 158-160)
- **TODO 2**: Store new refresh token in database (lines 165-171)

**Implementation Plan**:
1. Create `RefreshToken` model in domain models
2. Implement `RefreshTokenRepository` with CRUD operations
3. Update `refresh_tokens()` function to:
   - Revoke old refresh token using repository
   - Store new refresh token in database
   - Validate token existence during verification

### 2. Notification Service TODOs (10 items)
**Location**: `backend/app/api/v1/notifications/routes.py`
All endpoints need service implementation:
- GET `/notifications/` - Get user notifications
- GET `/notifications/{notification_id}` - Get specific notification
- POST `/notifications/` - Create notification
- POST `/notifications/{notification_id}/read` - Mark as read
- POST `/notifications/read-all` - Mark all as read
- GET `/notifications/preferences` - Get preferences
- PUT `/notifications/preferences/{preference_id}` - Update preference
- GET `/notifications/push-subscriptions` - Get push subscriptions
- POST `/notifications/push-subscriptions` - Create push subscription
- DELETE `/notifications/push-subscriptions/{subscription_id}` - Delete subscription

**Implementation Plan**:
1. Create `NotificationService` with business logic
2. Create `NotificationRepository` for data access
3. Create `NotificationPreferenceService` and `NotificationPreferenceRepository`
4. Create `PushSubscriptionService` and `PushSubscriptionRepository`
5. Implement all API endpoints using these services
6. Integrate with existing notification system components

### 3. Hackathon Service TODOs (8 items)
**Location**: `backend/app/api/v1/hackathons/routes.py`
All endpoints need service implementation:
- GET `/hackathons/` - Get all hackathons
- GET `/hackathons/{hackathon_id}` - Get specific hackathon
- POST `/hackathons/` - Create hackathon
- PUT `/hackathons/{hackathon_id}` - Update hackathon
- DELETE `/hackathons/{hackathon_id}` - Delete hackathon
- POST `/hackathons/{hackathon_id}/register` - Register for hackathon
- GET `/hackathons/{hackathon_id}/projects` - Get hackathon projects
- GET `/hackathons/{hackathon_id}/teams` - Get hackathon teams

**Implementation Plan**:
1. Create `HackathonService` with business logic
2. Create `HackathonRepository` for data access
3. Create `HackathonRegistrationService` and `HackathonRegistrationRepository`
4. Implement all API endpoints using these services
5. Integrate with existing geocoding and file upload services

### 4. Project Service TODOs (7 items)
**Location**: `backend/app/api/v1/projects/routes.py`
All endpoints need service implementation:
- GET `/projects/` - Get all projects
- GET `/projects/{project_id}` - Get specific project
- POST `/projects/` - Create project
- PUT `/projects/{project_id}` - Update project
- DELETE `/projects/{project_id}` - Delete project
- POST `/projects/{project_id}/vote` - Vote for project
- GET `/projects/{project_id}/comments` - Get project comments

**Implementation Plan**:
1. Create `ProjectService` with business logic
2. Create `ProjectRepository` for data access
3. Create `VoteService` and `VoteRepository` for voting logic
4. Create `CommentService` and `CommentRepository` for comments
5. Implement all API endpoints using these services
6. Integrate with existing file upload and notification systems

### 5. Team Service TODOs (11 items)
**Location**: `backend/app/api/v1/teams/routes.py`
All endpoints need service implementation:
- GET `/teams/` - Get all teams
- GET `/teams/{team_id}` - Get specific team
- POST `/teams/` - Create team
- PUT `/teams/{team_id}` - Update team
- DELETE `/teams/{team_id}` - Delete team
- GET `/teams/{team_id}/members` - Get team members
- POST `/teams/{team_id}/members` - Add team member
- DELETE `/teams/{team_id}/members/{member_id}` - Remove member
- GET `/teams/{team_id}/invitations` - Get invitations
- POST `/teams/{team_id}/invitations` - Create invitation
- POST `/teams/invitations/{invitation_id}/accept` - Accept invitation
- POST `/teams/invitations/{invitation_id}/decline` - Decline invitation

**Implementation Plan**:
1. Create `TeamService` with business logic
2. Create `TeamRepository` for data access
3. Create `TeamMemberService` and `TeamMemberRepository`
4. Create `TeamInvitationService` and `TeamInvitationRepository`
5. Implement all API endpoints using these services
6. Integrate with notification system for invitation emails

### 6. User Profile TODOs (1 item)
**Location**: `backend/app/api/v1/users/routes.py`
- **TODO**: Add profile information like projects, teams, etc. (line 76)

**Implementation Plan**:
1. Enhance `UserService` to include profile aggregation
2. Update GET `/users/me` endpoint to include:
   - User's projects
   - User's teams
   - User's hackathon registrations
   - User's notification preferences
3. Create comprehensive user profile DTO

### 7. Backend Refactoring Migration
**Based on**: `plans/backend_refactoring_migration_plan.md`

**Implementation Plan**:
1. **Phase 1**: Complete domain models migration
   - Migrate remaining models from `backend/models.py` to `backend/app/domain/models/`
   - Ensure all relationships are properly configured
2. **Phase 2**: Complete repository layer
   - Create remaining repository files for all entities
   - Migrate CRUD functions from `backend/crud.py`
3. **Phase 3**: Complete service layer
   - Create remaining service files
   - Migrate business logic from monolithic files
4. **Phase 4**: Update API routes
   - Ensure all routes use new services and repositories
   - Update imports throughout codebase
5. **Phase 5**: Integration and testing
   - Update `backend/app/main.py` to use all refactored components
   - Run comprehensive tests
   - Fix any integration issues

## Implementation Priority Order

### High Priority (Core Functionality)
1. **Authentication TODOs** - Security critical
2. **Backend Refactoring Completion** - Foundation for everything else
3. **User Profile TODOs** - Basic user experience

### Medium Priority (Core Features)
4. **Project Service TODOs** - Core application feature
5. **Hackathon Service TODOs** - Core application feature
6. **Team Service TODOs** - Core application feature

### Lower Priority (Advanced Features)
7. **Notification Service TODOs** - Advanced feature with existing partial implementation

## Dependencies and Integration Points

### Existing Services to Integrate With:
1. **Email Service**: `backend/app/services/email_service.py`
2. **Template Engine**: `backend/app/utils/template_engine.py`
3. **File Upload**: `backend/app/utils/file_upload.py`
4. **Geocoding**: `backend/app/utils/geocoding.py`
5. **i18n**: `backend/i18n/` for translations

### Database Considerations:
1. Ensure all migrations are applied
2. Check for existing data that needs migration
3. Test with both SQLite and PostgreSQL

## Testing Strategy

### Unit Tests:
- Test each service independently
- Test repository layer with in-memory database
- Test API endpoints with mocked services

### Integration Tests:
- Test full request/response cycles
- Test database interactions
- Test external service integrations (email, geocoding)

### End-to-End Tests:
- Test complete user workflows
- Test authentication flows
- Test notification delivery

## Success Criteria

1. All 42 TODO comments are implemented and removed
2. All API endpoints return appropriate responses (not 501 or 404 for unimplemented features)
3. Backend refactoring is complete with no remaining monolithic dependencies
4. All existing functionality is preserved
5. Code follows the established modular architecture
6. Comprehensive test coverage for new implementations
7. Documentation is updated to reflect changes

## Timeline and Phasing

### Phase 1: Foundation (Week 1)
- Implement authentication TODOs
- Complete backend refactoring migration
- Implement user profile TODOs

### Phase 2: Core Features (Week 2)
- Implement project service TODOs
- Implement hackathon service TODOs
- Implement team service TODOs

### Phase 3: Advanced Features (Week 3)
- Implement notification service TODOs
- Integration testing
- Performance optimization

### Phase 4: Polish (Week 4)
- Documentation updates
- Final testing
- Deployment preparation

## Risk Mitigation

### Technical Risks:
1. **Database schema changes**: Use Alembic migrations for all changes
2. **Breaking existing functionality**: Maintain backward compatibility during migration
3. **Performance issues**: Profile and optimize critical paths

### Process Risks:
1. **Scope creep**: Stick to implementing TODOs only, avoid feature creep
2. **Testing gaps**: Implement comprehensive test suite early
3. **Integration issues**: Test integration points thoroughly

## Next Steps

1. Review this plan with stakeholders
2. Begin implementation with Phase 1
3. Regular progress updates and adjustments as needed
4. Final review and sign-off before deployment

## Appendix: Detailed TODO List

### Authentication (2)
- [ ] `backend/app/core/auth.py:158` - Implement refresh token revocation and creation
- [ ] `backend/app/core/auth.py:165` - Store new refresh token in database

### Notifications (10)
- [ ] `backend/app/api/v1/notifications/routes.py:26` - Implement notification service (GET /)
- [ ] `backend/app/api/v1/notifications/routes.py:36` - Implement notification service (GET /{id})
- [ ] `backend/app/api/v1/notifications/routes.py:46` - Implement notification service (POST /)
- [ ] `backend/app/api/v1/notifications/routes.py:56` - Implement notification marking (POST /{id}/read)
- [ ] `backend/app/api/v1/notifications/routes.py:65` - Implement bulk notification marking (POST /read-all)
- [ ] `backend/app/api/v1/notifications/routes.py:74` - Implement preference retrieval (GET /preferences)
- [ ] `backend/app/api/v1/notifications/routes.py:85` - Implement preference update (PUT /preferences/{id})
- [ ] `backend/app/api/v1/notifications/routes.py:94` - Implement subscription retrieval (GET /push-subscriptions)
- [ ] `backend/app/api/v1/notifications/routes.py:104` - Implement subscription creation (POST /push-subscriptions)
- [ ] `backend/app/api/v1/notifications/routes.py:114` - Implement subscription deletion (DELETE /push-subscriptions/{id})

### Hackathons (8)
- [ ] `backend/app/api/v1/hackathons/routes.py:21` - Implement hackathon service (GET /)
- [ ] `backend/app/api/v1/hackathons/routes.py:31` - Implement hackathon service (GET /{id})
- [ ] `backend/app/api/v1/hackathons/routes.py:41` - Implement hackathon service (POST /)
- [ ] `backend/app/api/v1/hackathons/routes.py:52` - Implement hackathon service (PUT /{id})
- [ ] `backend/app/api/v1/hackathons/routes.py:62` - Implement hackathon service (DELETE /{id})
- [ ] `backend/app/api/v1/hackathons/routes.py:72` - Implement registration logic (POST /{id}/register)
- [ ] `backend/app/api/v1/hackathons/routes.py:85` - Implement project retrieval (GET /{id}/projects)
- [ ] `backend/app/api/v1/hackathons/routes.py:95` - Implement team retrieval (GET /{id}/teams)

### Projects (7)
- [ ] `backend/app/api/v1/projects/routes.py:21` - Implement project service (GET /)
- [ ] `backend/app/api/v1/projects/routes.py:31` - Implement project service (GET /{id})
- [ ] `backend/app/api/v1/projects/routes.py:41` - Implement project service (POST /)
- [ ] `backend/app/api/v1/projects/routes.py:52` - Implement project service (PUT /{id})
- [ ] `backend/app/api/v1/projects/routes.py:62` - Implement project service (DELETE /{id})
- [ ] `backend/app/api/v1/projects/routes.py:73` - Implement voting logic (POST /{id}/vote)
- [ ] `backend/app/api/v1/projects/routes.py:83` - Implement comment retrieval (GET /{id}/comments)

### Teams (11)
- [ ] `backend/app/api/v1/teams/routes.py:25` - Implement team service (GET /)
- [ ] `backend/app/api/v1/teams/routes.py:35` - Implement team service (GET /{id})
- [ ] `backend/app/api/v1/teams/routes.py:45` - Implement team service (POST /)
- [ ] `backend/app/api/v1/teams/routes.py:56` - Implement team service (PUT /{id})
- [ ] `backend/app/api/v1/teams/routes.py:66` - Implement team service (DELETE /{id})
- [ ] `backend/app/api/v1/teams/routes.py:76` - Implement team member retrieval (GET /{id}/members)
- [ ] `backend/app/api/v1/teams/routes.py:87` - Implement team member addition (POST /{id}/members)
- [ ] `backend/app/api/v1/teams/routes.py:98` - Implement team member removal (DELETE /{id}/members/{member_id})
- [ ] `backend/app/api/v1/teams/routes.py:108` - Implement invitation retrieval (GET /{id}/invitations)
- [ ] `backend/app/api/v1/teams/routes.py:119` - Implement invitation creation (POST /{id}/invitations)
- [ ] `backend/app/api/v1/teams/routes.py:129` - Implement invitation acceptance (POST /invitations/{id}/accept)
- [ ] `backend/app/api/v1/teams/routes.py:139` - Implement invitation decline (POST /invitations/{id}/decline)

### Users (1)
- [ ] `backend/app/api/v1/users/routes.py:76` - Add profile information like projects, teams, etc.

### Backend Refactoring
- [ ] Complete migration from monolithic to modular architecture per `plans/backend_refactoring_migration_plan.md`