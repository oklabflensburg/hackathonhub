# Frontend Team Management UI Design

## Overview
Design for team management UI components and pages to integrate with the backend team API endpoints.

## Component Architecture

### 1. Team Store (`stores/team.ts`)
New Pinia store for managing team state and API calls.

```typescript
// stores/team.ts
interface Team {
  id: number
  name: string
  description: string
  hackathon_id: number
  max_members: number
  is_open: boolean
  created_by: number
  created_at: string
  member_count: number
  members: TeamMember[]
  creator: User
}

interface TeamMember {
  id: number
  team_id: number
  user_id: number
  role: 'owner' | 'member'
  joined_at: string
  user: User
}

interface TeamInvitation {
  id: number
  team_id: number
  invited_user_id: number
  invited_by: number
  status: 'pending' | 'accepted' | 'declined'
  created_at: string
  expires_at: string | null
  invited_user: User
  inviter: User
  team: Team
}

// Store functions:
- fetchTeams(hackathonId?: number)
- fetchTeam(teamId: number)
- createTeam(teamData)
- updateTeam(teamId, teamData)
- deleteTeam(teamId)
- fetchTeamMembers(teamId)
- addTeamMember(teamId, userId, role)
- removeTeamMember(teamId, userId)
- fetchMyInvitations()
- acceptInvitation(invitationId)
- declineInvitation(invitationId)
- inviteToTeam(teamId, userId)
```

### 2. UI Components

#### `TeamCard.vue`
Display team summary in lists.

**Props:**
- `team: Team` - Team data
- `showActions: boolean` - Whether to show action buttons
- `compact: boolean` - Compact mode for dense layouts

**Slots:**
- `actions` - Custom action buttons

**Features:**
- Team name and description
- Member count avatars
- Hackathon badge
- Join/Leave buttons (context-aware)
- View details link

#### `TeamMemberList.vue`
List team members with management options.

**Props:**
- `teamId: number` - Team ID
- `editable: boolean` - Whether current user can edit
- `members: TeamMember[]` - List of members (optional, will fetch if not provided)

**Features:**
- Member avatars and names
- Role badges (owner/member)
- Remove button (for owners)
- Leave team button (for members)
- Empty state

#### `TeamInvitationForm.vue`
Form to invite users to a team.

**Props:**
- `teamId: number` - Team ID
- `teamName: string` - Team name (for display)

**Features:**
- User search by username/email
- Invitation message
- Role selection (member by default)
- Validation (team size limits, existing members)

#### `InvitationList.vue`
Display pending invitations with actions.

**Props:**
- `invitations: TeamInvitation[]` - List of invitations

**Features:**
- Invitation cards with team details
- Accept/Decline buttons
- Expiration status
- Empty state

#### `TeamForm.vue`
Form for creating/editing teams.

**Props:**
- `team: Team | null` - Existing team data for editing
- `hackathonId: number | null` - Pre-selected hackathon

**Features:**
- Team name and description
- Hackathon selection (if not pre-selected)
- Max members slider (1-10)
- Open/closed team toggle
- Validation

### 3. Pages

#### `/teams` - Team Discovery
Route: `app/pages/teams/index.vue`

**Features:**
- Browse teams by hackathon
- Search and filter (open teams, hackathon, size)
- Create new team button
- Grid/List view toggle
- Pagination

**Layout:**
```
[Header: "Teams" + Create Button]
[Filters: Hackathon dropdown, Open teams toggle, Search]
[Team Cards Grid]
[Pagination]
```

#### `/teams/create` - Create Team
Route: `app/pages/teams/create.vue`

**Features:**
- TeamForm component
- Success redirect to team page
- Error handling

#### `/teams/[id]` - Team Details
Route: `app/pages/teams/[id]/index.vue`

**Features:**
- Team header with name, description, stats
- TeamMemberList component
- Action buttons (Edit, Invite, Leave) based on user role
- Team projects list (if projects are team-based)
- Invitation management section (for owners)

#### `/teams/[id]/edit` - Edit Team
Route: `app/pages/teams/[id]/edit.vue`

**Features:**
- TeamForm component with existing data
- Delete team button (for owners)
- Member management section

#### `/invitations` - My Invitations
Route: `app/pages/invitations/index.vue`

**Features:**
- InvitationList component
- Tabs: Pending / Accepted / Declined
- Empty states
- Notification badges

### 4. Integration with Existing Pages

#### Project Creation/Editing
Update `app/pages/create.vue` and `app/pages/projects/[id]/edit.vue`:

**Changes:**
- Replace mock team member fields with team selection
- Add "Select Team" dropdown showing user's teams
- "Create New Team" button that opens modal
- Team-based permission checks

#### Project Display
Update `app/pages/projects/[id]/index.vue` and project cards:

**Changes:**
- Show actual team members instead of mock data
- Link to team page
- Team badge on project cards

#### Hackathon Pages
Update `app/pages/hackathons/[id]/index.vue`:

**Changes:**
- Add "Teams" tab to hackathon details
- Show teams participating in hackathon
- "Join Team" or "Create Team" CTAs

### 5. Navigation Updates

#### AppHeader
Add "Teams" to main navigation:
- Teams (dropdown: Browse, My Teams, Invitations)
- Or separate: Teams, Invitations (badge for pending)

#### User Profile
Add "My Teams" section to profile page.

### 6. State Management

#### Auth Store Updates
Update `stores/auth.ts` User interface to include teams:

```typescript
interface User {
  id: number
  // ... existing fields
  teams?: TeamMember[] // Add teams from /api/me response
}
```

#### Team Store Integration
- Initialize team store with user's teams from auth store
- Sync team state across components
- Handle team updates in real-time (optional: WebSocket for invites)

### 7. API Integration Layer

#### `utils/teamApi.ts`
API client functions for team endpoints:

```typescript
export const teamApi = {
  getTeams: (params) => fetchWithAuth('/api/teams', { params }),
  getTeam: (id) => fetchWithAuth(`/api/teams/${id}`),
  createTeam: (data) => fetchWithAuth('/api/teams', { method: 'POST', body: data }),
  updateTeam: (id, data) => fetchWithAuth(`/api/teams/${id}`, { method: 'PUT', body: data }),
  deleteTeam: (id) => fetchWithAuth(`/api/teams/${id}`, { method: 'DELETE' }),
  getTeamMembers: (teamId) => fetchWithAuth(`/api/teams/${teamId}/members`),
  addTeamMember: (teamId, userId, role) => fetchWithAuth(`/api/teams/${teamId}/members`, { 
    method: 'POST', 
    body: { user_id: userId, role } 
  }),
  removeTeamMember: (teamId, userId) => fetchWithAuth(`/api/teams/${teamId}/members/${userId}`, { 
    method: 'DELETE' 
  }),
  getMyInvitations: () => fetchWithAuth('/api/me/invitations'),
  acceptInvitation: (invitationId) => fetchWithAuth(`/api/invitations/${invitationId}/accept`, { 
    method: 'POST' 
  }),
  declineInvitation: (invitationId) => fetchWithAuth(`/api/invitations/${invitationId}/decline`, { 
    method: 'POST' 
  }),
  inviteToTeam: (teamId, userId) => fetchWithAuth(`/api/teams/${teamId}/invitations`, { 
    method: 'POST', 
    body: { invited_user_id: userId } 
  }),
}
```

### 8. Internationalization

Add translations for team-related text in `i18n/locales/`:

```json
{
  "teams": {
    "title": "Teams",
    "createTeam": "Create Team",
    "myTeams": "My Teams",
    "teamName": "Team Name",
    "teamDescription": "Team Description",
    "maxMembers": "Maximum Members",
    "openTeam": "Open Team",
    "closedTeam": "Closed Team",
    "members": "Members",
    "invitations": "Invitations",
    "pending": "Pending",
    "accepted": "Accepted",
    "declined": "Declined",
    "joinTeam": "Join Team",
    "leaveTeam": "Leave Team",
    "inviteMembers": "Invite Members",
    "noTeams": "No teams found",
    "createFirstTeam": "Create your first team"
  }
}
```

### 9. Responsive Design

**Mobile:**
- Single column layout for team cards
- Bottom sheet for team actions
- Simplified forms

**Tablet:**
- 2-column grid for team cards
- Sidebar navigation for team management

**Desktop:**
- 3-4 column grid for team cards
- Multi-panel layouts for team details

### 10. Accessibility

- ARIA labels for team actions
- Keyboard navigation for team lists
- Screen reader support for team status
- Color contrast for team badges

### 11. Performance Considerations

- Lazy load team lists with pagination
- Virtual scrolling for large team member lists
- Cache team data in Pinia store
- Optimistic updates for team actions

### 12. Error Handling

- Network error states
- Permission error messages
- Team size limit warnings
- Invitation expiration handling

### 13. Testing Strategy

**Component Tests:**
- TeamCard rendering and interactions
- TeamForm validation
- InvitationList acceptance flow

**Integration Tests:**
- Team creation flow
- Invitation acceptance flow
- Team member management

**E2E Tests:**
- Complete team lifecycle (create → invite → accept → manage → delete)
- Cross-user team interactions