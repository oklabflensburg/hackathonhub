# Team Membership Implementation Plan

## Current State Analysis

### Backend
- **Models**: `Team`, `TeamMember`, `TeamInvitation` models exist in `models.py`
- **CRUD Operations**: Team-related CRUD functions exist in `crud.py`:
  - `get_team()`, `get_team_with_details()`, `get_teams_by_hackathon()`, `get_user_teams()`
  - `create_team()`, `update_team()`, `delete_team()`
  - `get_team_member()`, `add_team_member()`, `remove_team_member()`
  - `get_team_invitation()`, `get_user_invitations()`, `create_team_invitation()`, `accept_team_invitation()`, `decline_team_invitation()`
- **Schemas**: Team schemas exist in `schemas.py`:
  - `Team`, `TeamCreate`, `TeamWithMembers`
  - `TeamMember`, `TeamMemberCreate`
  - `TeamInvitation`, `TeamInvitationCreate`
- **Missing**: API endpoints for team management are not implemented in `main.py`

### Frontend
- **UI Components**: Team display exists in project cards and project pages
- **Forms**: Team member input fields in project creation/editing forms
- **Data**: Currently using mock data for team members
- **Missing**: Actual team management UI, connection to backend APIs

## Backend API Endpoint Design

### 1. Team Management Endpoints

#### GET `/api/teams`
- List teams with optional filters
- Query params: `hackathon_id`, `skip`, `limit`, `is_open`
- Response: `List[TeamWithMembers]`

#### GET `/api/teams/{team_id}`
- Get team details with members
- Response: `TeamWithMembers`

#### POST `/api/teams`
- Create a new team
- Request: `TeamCreate`
- Response: `TeamWithMembers`
- Automatically adds creator as team owner

#### PUT `/api/teams/{team_id}`
- Update team details (name, description, max_members, is_open)
- Request: `TeamCreate`
- Response: `TeamWithMembers`
- Only team owners can update

#### DELETE `/api/teams/{team_id}`
- Delete a team
- Only team owners can delete
- Response: `{"message": "Team deleted successfully"}`

#### GET `/api/hackathons/{hackathon_id}/teams`
- List teams for a specific hackathon
- Response: `List[TeamWithMembers]`

### 2. Team Member Management Endpoints

#### GET `/api/teams/{team_id}/members`
- List team members
- Response: `List[TeamMember]`

#### POST `/api/teams/{team_id}/members`
- Add a team member (for team owners)
- Request: `TeamMemberCreate`
- Response: `TeamMember`

#### DELETE `/api/teams/{team_id}/members/{user_id}`
- Remove a team member
- Team owners can remove any member
- Members can remove themselves
- Response: `{"message": "Member removed successfully"}`

#### GET `/api/users/{user_id}/teams`
- Get all teams a user belongs to
- Response: `List[TeamWithMembers]`

### 3. Team Invitation Endpoints

#### GET `/api/teams/{team_id}/invitations`
- List pending invitations for a team
- Only team owners can view
- Response: `List[TeamInvitation]`

#### POST `/api/teams/{team_id}/invitations`
- Invite a user to join a team
- Request: `TeamInvitationCreate`
- Response: `TeamInvitation`
- Only team owners can invite

#### GET `/api/me/invitations`
- Get current user's pending invitations
- Response: `List[TeamInvitation]`

#### POST `/api/invitations/{invitation_id}/accept`
- Accept a team invitation
- Response: `TeamMember` (new team member record)

#### POST `/api/invitations/{invitation_id}/decline`
- Decline a team invitation
- Response: `{"message": "Invitation declined"}`

#### DELETE `/api/invitations/{invitation_id}`
- Cancel a pending invitation
- Only inviter or team owner can cancel
- Response: `{"message": "Invitation cancelled"}`

### 4. Updated `/api/me` Endpoint

#### GET `/api/me` (Enhanced)
- Return `UserWithDetails` instead of basic `User`
- Include: `teams: List[TeamMember]`, `projects`, `votes`, etc.
- This provides complete user context including team memberships

## Frontend Implementation Design

### 1. New Pages

#### `/teams` - Team Discovery
- Browse teams by hackathon
- Search and filter teams
- Join open teams (if applicable)

#### `/teams/create` - Create Team
- Form to create new team
- Select hackathon, set team name/description
- Set team size limits and openness

#### `/teams/{id}` - Team Details
- View team information
- List team members
- Manage team (for owners)
- Invite new members

#### `/teams/{id}/edit` - Edit Team
- Edit team details
- Manage team members

#### `/invitations` - My Invitations
- View pending team invitations
- Accept/decline invitations

### 2. Updated Existing Pages

#### Project Creation/Editing
- Replace mock team member fields with actual team selection
- Allow selecting from user's teams
- Or create new team during project creation

#### Project Display
- Show actual team members instead of mock data
- Link to team page

#### Hackathon Pages
- Show teams participating in hackathon
- Team registration/creation flow

### 3. UI Components

#### `TeamCard.vue`
- Display team summary
- Member avatars
- Join/leave buttons

#### `TeamMemberList.vue`
- List team members with roles
- Remove member functionality (for owners)

#### `TeamInvitationForm.vue`
- Form to invite users to team
- Search for users by username/email

#### `InvitationList.vue`
- Display pending invitations
- Accept/decline actions

## Data Flow

1. User creates/joins team via frontend
2. Frontend calls backend team APIs
3. Backend updates database and returns team data
4. Frontend updates UI and local state
5. `/api/me` returns updated team memberships
6. Project creation uses actual team IDs

## Integration Points

### Project-Team Relationship
Currently projects have `owner_id` but no `team_id`. Options:
1. Add `team_id` field to `Project` model
2. Use existing `hackathon_id` + team membership for permissions
3. Create `ProjectTeam` junction table

Recommended: Add `team_id` to `Project` model as optional foreign key to `Team`.

### Permission System Update
- Project editing: Allow team members (not just owner)
- Team-based permissions for hackathon projects

## Migration Requirements

1. Add `team_id` column to `projects` table
2. Update existing projects to maintain owner-only permissions
3. Create migration for new schema

## Testing Strategy

1. Backend API tests for all endpoints
2. Frontend component tests
3. Integration tests for team creation → project assignment
4. Permission tests for team-based access control

## Timeline & Priority

### Phase 1: Backend Foundation
1. Implement team API endpoints
2. Update `/api/me` endpoint
3. Add `team_id` to Project model

### Phase 2: Frontend Core
1. Team creation/management pages
2. Invitation system
3. Update project forms to use teams

### Phase 3: Integration & Polish
1. Update existing pages to use real team data
2. Permission system updates
3. Testing and bug fixes

## Success Metrics
- Users can create and manage teams
- Team invitations work end-to-end
- Projects can be associated with teams
- Team members have appropriate permissions
- All existing functionality continues to work