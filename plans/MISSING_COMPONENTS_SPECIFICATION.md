# Fehlende Komponenten - Spezifikationen

## Übersicht

Dieses Dokument listet alle fehlenden Komponenten auf, die für das Phase 3 Refactoring benötigt werden. Jede Komponente enthält eine detaillierte Spezifikation mit Props, Events, Slots und Verwendungszweck.

## Organisms benötigt für Team-Detailseite

### 1. TeamMembers.vue
**Verwendungszweck**: Anzeige und Verwaltung von Team-Mitgliedern

**Props**:
```typescript
interface TeamMembersProps {
  members: Array<{
    id: number
    user_id: number
    user?: {
      id: number
      name: string
      username: string
      avatar_url?: string
    }
    role: 'owner' | 'member'
    joined_at: string
  }>
  currentUserId?: number | null
  isTeamOwner: boolean
  maxMembers: number
  labels?: {
    teamMembers: string
    members: string
    noMembersYet: string
    owner: string
    member: string
    joined: string
    makeOwner: string
    makeMember: string
    remove: string
    confirmRemoveMember: string
  }
}
```

**Events**:
- `make-owner: (userId: number) => void`
- `make-member: (userId: number) => void`
- `remove-member: (userId: number) => void`

**Slots**:
- `empty-state` - Custom Empty State
- `member-actions` - Custom Actions für Mitglieder

**Verwendungsort**: `teams/[id]/index.vue`

### 2. TeamProjects.vue
**Verwendungszweck**: Anzeige der Projekte des Teams

**Props**:
```typescript
interface TeamProjectsProps {
  projects: Array<{
    id: number
    title: string
    description: string
    image_path?: string
    technologies: string
    upvote_count: number
    comment_count: number
    created_at: string
  }>
  loading?: boolean
  emptyMessage?: string
}
```

**Events**:
- `project-click: (projectId: number) => void`

**Slots**:
- `project-card` - Custom Projekt-Karte
- `empty-state` - Custom Empty State

**Verwendungsort**: `teams/[id]/index.vue`

## Organisms benötigt für Profilseite

### 3. ProfileOverview.vue
**Verwendungszweck**: Übersicht der Benutzerstatistiken und Informationen

**Props**:
```typescript
interface ProfileOverviewProps {
  user: {
    id: number
    name: string
    username: string
    email?: string
    avatar_url?: string
    bio?: string
    location?: string
    website?: string
    github_username?: string
    twitter_username?: string
  }
  stats?: {
    projectCount: number
    teamCount: number
    hackathonCount: number
    voteCount: number
  }
  isCurrentUser: boolean
}
```

**Events**:
- `edit-profile: () => void`

**Slots**:
- `stats` - Custom Statistiken
- `bio` - Custom Bio-Bereich
- `social-links` - Custom Social Links

**Verwendungsort**: `profile.vue`

### 4. UserProjects.vue
**Verwendungszweck**: Liste der Projekte des Benutzers

**Props**:
```typescript
interface UserProjectsProps {
  projects: Array<Project>
  loading?: boolean
  emptyMessage?: string
  showFilters?: boolean
}
```

**Events**:
- `project-click: (projectId: number) => void`
- `filter-change: (filters: ProjectFilters) => void`

**Slots**:
- `project-card` - Custom Projekt-Karte
- `empty-state` - Custom Empty State

**Verwendungsort**: `profile.vue`, `my-projects.vue`

### 5. UserTeams.vue
**Verwendungszweck**: Liste der Teams des Benutzers

**Props**:
```typescript
interface UserTeamsProps {
  teams: Array<Team>
  loading?: boolean
  emptyMessage?: string
  showRole?: boolean
}
```

**Events**:
- `team-click: (teamId: number) => void`

**Slots**:
- `team-card` - Custom Team-Karte
- `empty-state` - Custom Empty State

**Verwendungsort**: `profile.vue`

## Organisms benötigt für Hackathon-Detailseite

### 6. HackathonInfo.vue
**Verwendungszweck**: Detaillierte Informationen über einen Hackathon

**Props**:
```typescript
interface HackathonInfoProps {
  hackathon: {
    id: number
    title: string
    description: string
    start_date: string
    end_date: string
    location?: string
    online: boolean
    max_participants?: number
    prize_pool?: string
    rules?: string
    technologies?: string
  }
  formattedDates?: {
    start: string
    end: string
    duration: string
  }
}
```

**Events**: Keine

**Slots**:
- `description` - Custom Beschreibung
- `rules` - Custom Regeln
- `technologies` - Custom Technologien

**Verwendungsort**: `hackathons/[id]/index.vue`

### 7. HackathonProjects.vue
**Verwendungszweck**: Projekte im Hackathon (könnte wiederverwendet werden)

**Props**:
```typescript
interface HackathonProjectsProps {
  projects: Array<Project>
  hackathonId: number
  loading?: boolean
  emptyMessage?: string
  showFilters?: boolean
}
```

**Events**:
- `project-click: (projectId: number) => void`
- `filter-change: (filters: ProjectFilters) => void`

**Slots**:
- `project-card` - Custom Projekt-Karte
- `empty-state` - Custom Empty State

**Verwendungsort**: `hackathons/[id]/index.vue`, `hackathons/[id]/projects.vue`

## Organisms benötigt für Notifications-Seite

### 8. NotificationList.vue
**Verwendungszweck**: Liste von Benachrichtigungen mit Filter- und Sortieroptionen

**Props**:
```typescript
interface NotificationListProps {
  notifications: Array<{
    id: number
    type: string
    title: string
    message: string
    read: boolean
    created_at: string
    data?: any
  }>
  loading?: boolean
  emptyMessage?: string
  showFilters?: boolean
  showMarkAllRead?: boolean
}
```

**Events**:
- `notification-click: (notificationId: number) => void`
- `mark-read: (notificationId: number) => void`
- `mark-all-read: () => void`
- `delete: (notificationId: number) => void`
- `filter-change: (filters: NotificationFilters) => void`

**Slots**:
- `notification-item` - Custom Benachrichtigungs-Item
- `empty-state` - Custom Empty State

**Verwendungsort**: `notifications.vue`

### 9. NotificationFilters.vue
**Verwendungszweck**: Filter- und Sortieroptionen für Benachrichtigungen

**Props**:
```typescript
interface NotificationFiltersProps {
  filters: {
    readStatus: 'all' | 'read' | 'unread'
    type: string
    dateRange: {
      start?: string
      end?: string
    }
  }
  availableTypes: string[]
}
```

**Events**:
- `update-filters: (filters: NotificationFilters) => void`
- `reset: () => void`

**Slots**: Keine

**Verwendungsort**: `notifications.vue` (als Teil von NotificationList)

## Organisms benötigt für Projekt-Bearbeitungsseite

### 10. EditProjectForm.vue
**Verwendungszweck**: Formular zur Bearbeitung eines bestehenden Projekts

**Props**:
```typescript
interface EditProjectFormProps {
  project: {
    id: number
    title: string
    description: string
    technologies: string
    repository_url?: string
    live_url?: string
    image_path?: string
    hackathon_id?: number
  }
  hackathons?: Array<{
    id: number
    title: string
  }>
  loading?: boolean
}
```

**Events**:
- `submit: (projectData: ProjectUpdate) => void`
- `cancel: () => void`
- `delete: () => void`

**Slots**:
- `before-form` - Content vor dem Formular
- `after-form` - Content nach dem Formular
- `actions` - Custom Formular-Actions

**Verwendungsort**: `projects/[id]/edit.vue`

## Molecules benötigt (optional)

### 1. MemberCard.vue
**Verwendungszweck**: Karte für ein einzelnes Teammitglied

**Props**:
```typescript
interface MemberCardProps {
  member: TeamMember
  showRole?: boolean
  showActions?: boolean
  isCurrentUser?: boolean
  isTeamOwner?: boolean
}
```

**Events**:
- `make-owner: () => void`
- `make-member: () => void`
- `remove: () => void`

**Slots**:
- `avatar` - Custom Avatar
- `actions` - Custom Actions

**Verwendungsort**: `TeamMembers.vue`

### 2. NotificationItem.vue
**Verwendungszweck**: Einzelne Benachrichtigung

**Props**:
```typescript
interface NotificationItemProps {
  notification: Notification
  showType?: boolean
  showTime?: boolean
}
```

**Events**:
- `click: () => void`
- `mark-read: () => void`
- `delete: () => void`

**Slots**:
- `icon` - Custom Icon
- `actions` - Custom Actions

**Verwendungsort**: `NotificationList.vue`

## Composables benötigt

### 1. useTeamMembers.ts
**Zweck**: Logik für Team-Mitglieder-Verwaltung

**Funktionen**:
- `fetchMembers(teamId)`
- `addMember(teamId, userId)`
- `removeMember(teamId, userId)`
- `changeRole(teamId, userId, role)`

**State**:
- `members: Ref<TeamMember[]>`
- `loading: Ref<boolean>`
- `error: Ref<string | null>`

### 2. useUserProfile.ts
**Zweck**: Logik für Benutzerprofil-Daten

**Funktionen**:
- `fetchUserProfile(userId)`
- `updateProfile(userId, data)`
- `fetchUserProjects(userId)`
- `fetchUserTeams(userId)`

**State**:
- `profile: Ref<UserProfile | null>`
- `projects: Ref<Project[]>`
- `teams: Ref<Team[]>`
- `loading: Ref<boolean>`

### 3. useNotifications.ts
**Zweck**: Logik für Benachrichtigungen

**Funktionen**:
- `fetchNotifications(filters)`
- `markAsRead(notificationId)`
- `markAllAsRead()`
- `deleteNotification(notificationId)`
- `getUnreadCount()`

**State**:
- `notifications: Ref<Notification[]>`
- `unreadCount: Ref<number>`
- `loading: Ref<boolean>`
- `filters: Ref<NotificationFilters>`

### 4. useHackathonData.ts
**Zweck**: Logik für Hackathon-Daten

**Funktionen**:
- `fetchHackathonDetails(hackathonId)`
- `fetchHackathonProjects(hackathonId, filters)`
- `fetchHackathonParticipants(hackathonId)`
- `joinHackathon(hackathonId)`
- `leaveHackathon(hackathonId)`

**State**:
- `hackathon: Ref<Hackathon | null>`
- `projects: Ref<Project[]>`
- `participants: Ref<Participant[]>`
- `loading: Ref<boolean>`

## Implementierungsreihenfolge

### Priorität 1 (Team-Detailseite):
1. `useTeamMembers.ts` Composable
2. `MemberCard.vue` Molecule (optional)
3. `TeamMembers.vue` Organism
4. `TeamProjects.vue` Organism

### Priorität 2 (Profilseite):
1. `useUserProfile.ts` Composable
2. `ProfileOverview.vue` Organism
3. `UserProjects.vue` Organism
4. `UserTeams.vue` Organism

### Priorität 3 (Hackathon-Detailseite):
1. `useHackathonData.ts` Composable
2. `HackathonInfo.vue` Organism
3. `HackathonProjects.vue` Organism

### Priorität 4 (Notifications):
1. `useNotifications.ts` Composable
2. `NotificationItem.vue` Molecule
3. `NotificationList.vue` Organism
4. `NotificationFilters.vue` Organism

### Priorität 5 (Projekt-Edit):
1. `EditProjectForm.vue` Organism (basierend auf ProjectForm)

## Nächste Schritte

1. **Genehmigung der Spezifikationen** durch den Benutzer
2. **Erstellung der Composables** zuerst (da sie von mehreren Komponenten verwendet werden)
3. **Implementierung der Molecules** (falls benötigt)
4. **Implementierung der Organisms**
5. **Integration in die Seiten**

---
**Status**: Spezifikationen erstellt  
**Empfohlener Start**: Mit `useTeamMembers.ts` Composable  
**Zeitaufwand**: 2-3 Tage pro Organism (inklusive Testing)