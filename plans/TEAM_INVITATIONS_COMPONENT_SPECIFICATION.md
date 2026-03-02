# Team Invitations - Komponenten-Spezifikation

## Übersicht

Dieses Dokument enthält detaillierte Spezifikationen für alle neuen Komponenten, die für das Atomic Design Refactoring der Team-Einladungen benötigt werden.

## Composables

### 1. useTeamInvitations.ts

**Zweck**: Logik für das Abrufen und Verwalten von Team-Einladungen.

**Typen**:
```typescript
export interface TeamInvitation {
  id: number
  team_id: number
  invited_user_id: number
  inviter_id: number
  status: 'pending' | 'accepted' | 'declined' | 'cancelled'
  created_at: string
  updated_at: string
  invited_user?: {
    id: number
    username: string
    name?: string
    avatar_url?: string
  }
  inviter?: {
    id: number
    username: string
    avatar_url?: string
  }
  team?: {
    id: number
    name: string
    hackathon?: {
      id: number
      name: string
    }
  }
}

export interface UseTeamInvitationsOptions {
  teamId: Ref<number> | number
  autoFetch?: boolean
  pollInterval?: number // für real-time updates
}
```

**API**:
```typescript
export function useTeamInvitations(options: UseTeamInvitationsOptions) {
  // State
  const invitations: Ref<TeamInvitation[]> = ref([])
  const loading: Ref<boolean> = ref(false)
  const error: Ref<string | null> = ref(null)
  
  // Methods
  async function fetchInvitations(): Promise<void>
  async function cancelInvitation(invitationId: number): Promise<boolean>
  async function sendInvitation(userId: number): Promise<boolean>
  async function refresh(): Promise<void>
  
  // Computed
  const pendingInvitations = computed(() => ...)
  const acceptedInvitations = computed(() => ...)
  const invitationCount = computed(() => ...)
  
  return {
    // State
    invitations,
    loading,
    error,
    
    // Computed
    pendingInvitations,
    acceptedInvitations,
    invitationCount,
    
    // Methods
    fetchInvitations,
    cancelInvitation,
    sendInvitation,
    refresh,
  }
}
```

### 2. useUserSearch.ts

**Zweck**: Logik für die Benutzersuche mit Autocomplete und Debouncing.

**Typen**:
```typescript
export interface UserSearchResult {
  id: number
  username: string
  name?: string
  avatar_url?: string
  email?: string
  is_member?: boolean // bereits Teammitglied
}

export interface UseUserSearchOptions {
  debounceMs?: number
  minQueryLength?: number
  excludeUserIds?: number[]
}
```

**API**:
```typescript
export function useUserSearch(options: UseUserSearchOptions = {}) {
  // State
  const query: Ref<string> = ref('')
  const results: Ref<UserSearchResult[]> = ref([])
  const loading: Ref<boolean> = ref(false)
  const error: Ref<string | null> = ref(null)
  
  // Methods
  async function search(searchQuery: string): Promise<void>
  function clear(): void
  function selectUser(user: UserSearchResult): void
  
  // Computed
  const hasResults = computed(() => ...)
  const isEmpty = computed(() => ...)
  
  return {
    // State
    query,
    results,
    loading,
    error,
    
    // Computed
    hasResults,
    isEmpty,
    
    // Methods
    search,
    clear,
    selectUser,
  }
}
```

## Molecules

### 1. InvitationItem.vue

**Verwendungszweck**: Einzelnes Einladungselement in der Liste.

**Props**:
```typescript
interface InvitationItemProps {
  invitation: TeamInvitation
  showCancelButton?: boolean
  showInviter?: boolean
  showTeamInfo?: boolean
  showStatus?: boolean
  formatDate?: (dateString: string) => string
  labels?: {
    pending?: string
    invited?: string
    by?: string
    cancel?: string
    unknownUser?: string
  }
}
```

**Events**:
- `cancel: (invitationId: number) => void`
- `click: (invitation: TeamInvitation) => void`

**Slots**:
- `avatar`: Custom Avatar (erhält `{ user }`)
- `content`: Custom Hauptinhalt (erhält `{ invitation }`)
- `actions`: Custom Actions (erhält `{ invitation, cancel }`)
- `status`: Custom Status-Badge

**Design-Anforderungen**:
- Responsive Layout
- Dark Mode Support
- Accessibility: Keyboard navigation, ARIA labels
- Hover-Effekte für Interaktivität

### 2. InviteUserForm.vue

**Verwendungszweck**: Formular zum Einladen eines Benutzers.

**Props**:
```typescript
interface InviteUserFormProps {
  teamId: number
  maxMembers?: number
  currentMemberCount?: number
  disabled?: boolean
  placeholder?: string
  buttonLabel?: string
  helpText?: string
}
```

**Events**:
- `invite-sent: { userId: number, username: string }`
- `error: { message: string, code?: string }`
- `search: { query: string }`

**Slots**:
- `before-input`: Content vor dem Input
- `after-input`: Content nach dem Input
- `help-text`: Custom Hilfetext
- `button`: Custom Button

**State** (intern):
- `username: Ref<string>`
- `searching: Ref<boolean>`
- `inviting: Ref<boolean>`
- `selectedUser: Ref<UserSearchResult | null>`

### 3. UserSearchInput.vue

**Verwendungszweck**: Input mit Autocomplete für Benutzersuche.

**Props**:
```typescript
interface UserSearchInputProps {
  modelValue: string
  suggestions: UserSearchResult[]
  loading?: boolean
  placeholder?: string
  minChars?: number
  maxSuggestions?: number
  disabled?: boolean
  excludeUserIds?: number[]
}
```

**Events**:
- `update:modelValue: (value: string) => void`
- `select: (user: UserSearchResult) => void`
- `search: (query: string) => void`
- `clear: () => void`

**Slots**:
- `suggestion-item`: Custom Suggestion Item (erhält `{ user, index }`)
- `empty-state`: Custom Empty State (erhält `{ query }`)
- `loading-state`: Custom Loading State

**Design-Anforderungen**:
- Dropdown mit max. 5 Vorschlägen
- Keyboard navigation (Arrow keys, Enter, Escape)
- Virtuelles Scrolling für viele Ergebnisse
- Highlighting des Suchbegriffs in den Ergebnissen

## Organisms

### 1. TeamInvitations.vue

**Verwendungszweck**: Liste der ausstehenden Team-Einladungen.

**Props**:
```typescript
interface TeamInvitationsProps {
  teamId: number
  isTeamOwner: boolean
  showHeader?: boolean
  showEmptyState?: boolean
  showLoadingState?: boolean
  showErrorState?: boolean
  autoLoad?: boolean
  pollInterval?: number
  maxVisible?: number
  labels?: {
    title?: string
    emptyTitle?: string
    emptyDescription?: string
    loading?: string
    error?: string
    retry?: string
  }
}
```

**Events**:
- `invitation-cancelled: { invitationId: number, invitation: TeamInvitation }`
- `loaded: { invitations: TeamInvitation[], count: number }`
- `error: { message: string, code?: string }`
- `retry: () => void`

**Slots**:
- `header`: Custom Header (erhält `{ count, isTeamOwner }`)
- `empty-state`: Custom Empty State (erhält `{ isTeamOwner }`)
- `loading-state`: Custom Loading State
- `error-state`: Custom Error State (erhält `{ error, retry }`)
- `invitation-item`: Custom Invitation Item (erhält `{ invitation, cancel }`)
- `footer`: Content nach der Liste

**Design-Anforderungen**:
- Responsive Grid/List Layout
- Smooth Loading Transitions
- Empty State mit Illustration
- Error State mit Retry-Button

### 2. TeamInviteSection.vue

**Verwendungszweck**: Sektion zum Einladen neuer Teammitglieder.

**Props**:
```typescript
interface TeamInviteSectionProps {
  teamId: number
  isTeamOwner: boolean
  isTeamFull: boolean
  currentMemberCount?: number
  maxMembers?: number
  showHelpText?: boolean
  showMemberCount?: boolean
  disabled?: boolean
  labels?: {
    title?: string
    placeholder?: string
    button?: string
    helpText?: string
    memberCount?: string
    teamFull?: string
  }
}
```

**Events**:
- `invite-sent: { userId: number, username: string }`
- `error: { message: string, code?: string }`
- `search: { query: string }`

**Slots**:
- `before-form`: Content vor dem Formular
- `after-form`: Content nach dem Formular
- `help-text`: Custom Hilfetext (erhält `{ currentMemberCount, maxMembers }`)
- `team-full-message`: Custom Message wenn Team voll

**Design-Anforderungen**:
- Conditional Rendering (nur anzeigen wenn `isTeamOwner && !isTeamFull`)
- Visuelles Feedback bei Erfolg/Fehler
- Progress Bar für Mitgliederanzahl (optional)

## Integration mit bestehenden Komponenten

### Wiederverwendung vorhandener Komponenten

- **EmptyState**: Verwende `molecules/EmptyState.vue`
- **LoadingState**: Verwende `molecules/LoadingState.vue`
- **ErrorState**: Verwende `molecules/ErrorState.vue`
- **Avatar**: Verwende `atoms/Avatar.vue`
- **Button**: Verwende `atoms/Button.vue`
- **Input**: Verwende `atoms/Input.vue`
- **Tag**: Verwende `atoms/Tag.vue` für Status-Badges

### Abhängigkeiten

- `useTeamStore` für Team-Daten
- `useAuthStore` für aktuellen Benutzer
- `useUIStore` für Notifications
- `useI18n` für Internationalisierung

## Testing Strategy

### Unit Tests
- Jedes Composable: Testen aller Funktionen und States
- Jede Molecule: Testen von Props, Events und Slots
- Jeder Organism: Testen der Integration

### Integration Tests
- TeamInvitations + useTeamInvitations
- TeamInviteSection + useUserSearch
- Vollständiger Workflow: Suche → Einladung → Anzeige

### E2E Tests
- Team-Owner lädt Benutzer ein
- Teammitglied sieht ausstehende Einladungen
- Team-Owner storniert Einladung

## Accessibility Requirements

### WCAG 2.1 AA Compliance
- **Keyboard Navigation**: Alle interaktiven Elemente erreichbar
- **Screen Reader**: Sinnvolle ARIA-Labels und Live Regions
- **Color Contrast**: Mindestens 4.5:1 für Text
- **Focus Management**: Logischer Focus Order
- **Error Handling**: Accessible Error Messages

### Spezifische Anforderungen
- UserSearchInput: `aria-autocomplete="list"`, `aria-expanded`, `aria-activedescendant`
- InvitationItem: `role="listitem"`, `aria-label` mit Benutzerinfo
- Loading States: `aria-live="polite"` für Statusänderungen

## Performance Considerations

### Optimierungen
- **Debouncing**: User-Suche nach 300ms
- **Pagination**: Bei >10 Einladungen lazy loading
- **Caching**: Einladungen für 30 Sekunden cachen
- **Virtual Scrolling**: Für lange Listen (>50 Einträge)
- **Lazy Loading**: Komponenten nur bei Bedarf laden

### Bundle Size
- Tree-shaking sicherstellen
- Dynamische Imports für nicht-kritische Komponenten
- Shared Dependencies minimieren

## Internationalisierung

### Übersetzungsschlüssel
```json
{
  "teams": {
    "invitations": {
      "title": "Team Invitations",
      "pending": "Pending",
      "invited": "Invited",
      "by": "by",
      "cancel": "Cancel",
      "unknownUser": "Unknown User",
      "emptyTitle": "No pending invitations",
      "emptyDescription": "There are no pending invitations for this team.",
      "loading": "Loading invitations...",
      "error": "Failed to load invitations"
    },
    "invite": {
      "title": "Invite Members",
      "placeholder": "Enter username",
      "button": "Invite",
      "helpText": "Enter a username to invite them to your team",
      "memberCount": "{current}/{max} members",
      "teamFull": "Team is full"
    }
  }
}
```

## Migration Checklist

### Vor der Migration
- [ ] Backup des aktuellen Codes
- [ ] Feature-Flag Konfiguration
- [ ] Testing Environment setup

### Während der Migration
- [ ] Composables implementieren und testen
- [ ] Molecules implementieren und testen
- [ ] Organisms implementieren und testen
- [ ] Integration mit Feature-Flag
- [ ] Manuelles Testing aller Szenarien

### Nach der Migration
- [ ] Feature-Flag entfernen
- [ ] Alten Code löschen
- [ ] Performance-Metriken vergleichen
- [ ] Dokumentation aktualisieren
- [ ] Team informieren

---
**Status**: Spezifikationen erstellt  
**Nächste Schritte**: Implementierungsplan erstellen  
**Priorität**: Hoch (Teil von Phase 3 Refactoring)