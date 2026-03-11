# Konkreter Migrationsplan für Composables

## Überblick
Dieser Plan beschreibt die konkreten Schritte zur Migration aller Composables auf das neue Schema mit zentralen Typ-Definitionen, basierend auf der Analyse in `composable-migration-review.md`.

## Phase 0: Vorbereitung und Entscheidungen

### 0.1 Architektur-Entscheidungen
Bevor mit der Migration begonnen wird, müssen folgende Entscheidungen getroffen werden:

1. **Case Convention**: 
   - **Empfehlung**: camelCase für Frontend-Typen (konsistent mit TypeScript/JavaScript Konventionen)
   - **Begründung**: Bessere Integration mit Vue/TypeScript Ecosystem, konsistent mit bestehenden `team-types.ts`

2. **ID-Typen**:
   - **Empfehlung**: `string` für alle IDs (UUIDs)
   - **Begründung**: Zukunftssicherheit, konsistent mit modernen APIs, einfachere Serialisierung

3. **API Response Mapping**:
   - **Empfehlung**: Dedizierte Mapper-Funktionen für snake_case API → camelCase Frontend
   - **Begründung**: Trennung von Concerns, einfachere Wartung

### 0.2 Tooling Setup
1. **TypeScript Konfiguration**: Sicherstellen, dass `strict: true` aktiviert ist
2. **ESLint Regeln**: Regeln für konsistente Importe und Typ-Verwendung
3. **Test Setup**: Unit-Test Framework für Composable-Tests
4. **CI/CD Pipeline**: Automatische TypeScript- und Test-Validierung

## Phase 1: Typ-Definition Konsolidierung

### 1.1 Aktualisierung bestehender Typ-Dateien

#### `team-types.ts` Aktualisierung
```typescript
// Vorher: id: string, camelCase
// Nachher: id: number (vorübergehend für API-Kompatibilität), snake_case für API-Felder

export interface Team {
  id: number  // Temporär für API-Kompatibilität
  name: string
  description: string | null
  hackathon_id: number
  max_members: number
  is_open: boolean
  created_by: number
  created_at: string
  // ... weitere Felder
}

// Zusätzlich: Frontend-spezifische Typen mit camelCase
export interface TeamFrontend {
  id: string
  name: string
  description: string | null
  hackathonId: number
  maxMembers: number
  isOpen: boolean
  createdBy: number
  createdAt: string
  // Transformierte Felder
}
```

#### `project-types.ts` Aktualisierung
```typescript
// Integration mit API-Struktur
export interface Project {
  id: number
  title: string
  description?: string
  repository_url?: string
  live_url?: string
  technologies?: string
  status?: string
  is_public?: boolean
  hackathon_id?: number
  team_id?: number
  image_path?: string
  owner_id?: number
  created_at: string
  updated_at?: string
  upvote_count: number
  downvote_count: number
  vote_score: number
  comment_count: number
  view_count: number
}

// API-spezifische Typen
export interface ProjectCreateData {
  title: string
  description?: string
  repository_url?: string
  // ... etc
}
```

#### `hackathon-types.ts` Aktualisierung
```typescript
// Erweiterung um fehlende Felder
export interface Hackathon {
  id: number
  name: string
  description: string
  start_date: string
  end_date: string
  location: string
  latitude?: number      // Neu
  longitude?: number     // Neu
  website?: string       // Neu
  image_url?: string
  banner_path?: string   // Neu
  // ... bestehende Felder
}
```

### 1.2 Erstellung fehlender Typ-Dateien

#### `comment-types.ts` (Neu)
```typescript
export interface Comment {
  id: number
  content: string
  user_id: number
  project_id: number
  parent_id?: number
  upvote_count: number
  downvote_count: number
  vote_score: number
  created_at: string
  updated_at?: string
  user?: any
  project?: any
  replies?: Comment[]
}

export interface CommentCreateData {
  content: string
  parent_id?: number
}

export interface CommentUpdateData {
  content: string
}

export interface CommentVoteData {
  vote_type: 'upvote' | 'downvote'
}

export interface CommentVoteStats {
  upvotes: number
  downvotes: number
  total_score: number
  user_vote?: 'upvote' | 'downvote'
}
```

#### `file-upload-types.ts` (Neu)
```typescript
export interface FileUploadOptions {
  onProgress?: (percent: number) => void
  maxFileSize?: number
  allowedTypes?: string[]
}

export interface UploadResult {
  id: number
  filename: string
  path: string
  url: string
  size: number
  mime_type: string
  uploaded_at: string
}
```

#### `newsletter-types.ts` (Neu)
```typescript
export interface NewsletterSubscription {
  email: string
  source: 'website_footer' | 'registration' | 'manual'
  subscribed_at: string
  unsubscribed_at?: string
}

export interface NewsletterSubscribeData {
  email: string
  source?: string
}
```

## Phase 2: Composable-Migration

### 2.1 `useTeams.ts` Migration

#### Schritt 1: Typ-Importe aktualisieren
```typescript
// Vorher:
interface Team { /* lokale Definition */ }

// Nachher:
import type {
  Team,
  TeamMember,
  TeamInvitation,
  TeamCreateData,
  TeamUpdateData,
  TeamMemberCreateData,
  TeamMemberUpdateData,
  TeamInvitationCreateData,
  UseTeamsOptions
} from '~/types/team-types'

// Re-export für Abwärtskompatibilität
export type {
  Team,
  TeamMember,
  TeamInvitation,
  TeamCreateData,
  TeamUpdateData,
  TeamMemberCreateData,
  TeamMemberUpdateData,
  TeamInvitationCreateData,
  UseTeamsOptions
}
```

#### Schritt 2: State-Typen aktualisieren
```typescript
// Vorher:
const teams = ref<Team[]>([])
const currentTeam = ref<Team | null>(null)

// Nachher: (keine Änderung nötig, da Typen kompatibel)
```

#### Schritt 3: Methoden-Signaturen validieren
- Sicherstellen, dass alle Methoden-Parameter mit importierten Typen übereinstimmen
- API-Response Typen anpassen falls nötig

#### Schritt 4: Enum-Verwendung einführen
```typescript
// Vorher:
status: string

// Nachher:
import { TeamInvitationStatus } from '~/types/team-types'
status: TeamInvitationStatus
```

#### Schritt 5: Testing
- Unit-Tests für migrierte Methoden
- TypeScript-Kompilierung validieren
- Integration mit bestehenden Komponenten testen

### 2.2 `useProjects.ts` Migration

#### Schritt 1: Typ-Importe aktualisieren
```typescript
import type {
  Project,
  ProjectCreateData,
  ProjectUpdateData,
  VoteData,
  VoteStats,
  UseProjectsOptions
} from '~/types/project-types'

// Re-export
export type {
  Project,
  ProjectCreateData,
  ProjectUpdateData,
  VoteData,
  VoteStats,
  UseProjectsOptions
}
```

#### Schritt 2: Entfernung doppelter Typen
- Lokale `Project`, `ProjectCreateData`, etc. Interfaces entfernen
- Sicherstellen, dass alle Referenzen aktualisiert sind

#### Schritt 3: Enum-Integration
```typescript
// Vorher:
status?: string
is_public?: boolean

// Nachher:
import { ProjectStatus, ProjectVisibility } from '~/types/project-types'
status?: ProjectStatus
visibility?: ProjectVisibility
```

#### Schritt 4: API-Response Mapping
```typescript
// Optional: Mapper-Funktion für komplexe Transformationen
function mapApiProject(apiProject: any): Project {
  return {
    id: apiProject.id,
    title: apiProject.title,
    // ... mapping
  }
}
```

### 2.3 `useHackathons.ts` Migration

#### Schritt 1: Typ-Importe aktualisieren
```typescript
import type {
  Hackathon,
  HackathonCreateData,
  HackathonUpdateData,
  HackathonRegistration,
  HackathonRegistrationStatus
} from '~/types/hackathon-types'

// Re-export
export type {
  Hackathon,
  HackathonCreateData,
  HackathonUpdateData,
  HackathonRegistration,
  HackathonRegistrationStatus
}
```

#### Schritt 2: Feld-Konsistenz
- Sicherstellen, dass alle Felder in `hackathon-types.ts` vorhanden sind
- Fehlende Felder (`latitude`, `longitude`, `website`, `banner_path`) hinzufügen

#### Schritt 3: Strukturierte Daten
```typescript
// Vorher:
prizes?: string
organizers?: string

// Nachher (wenn API unterstützt):
prizes?: Prize[]
organizers?: Organizer[]
```

### 2.4 `useComments.ts` Migration

#### Schritt 1: Neue Typ-Datei erstellen
- `comment-types.ts` wie oben definiert erstellen

#### Schritt 2: Typ-Importe aktualisieren
```typescript
import type {
  Comment,
  CommentCreateData,
  CommentUpdateData,
  CommentVoteData,
  CommentVoteStats,
  UseCommentsOptions
} from '~/types/comment-types'

// Re-export
export type {
  Comment,
  CommentCreateData,
  CommentUpdateData,
  CommentVoteData,
  CommentVoteStats,
  UseCommentsOptions
}
```

#### Schritt 3: Lokale Typen entfernen
- Alle lokalen Interface-Definitionen entfernen

### 2.5 Weitere Composables

#### `useNotifications.ts`
```typescript
import type {
  Notification,
  NotificationPreferences,
  // ... etc
} from '~/types/notification-types'
```

#### `useSettings.ts`
```typescript
import type {
  UserSettings,
  NotificationSettings,
  PrivacySettings,
  // ... etc
} from '~/types/settings-types'
```

#### `useFileUpload.ts`
```typescript
import type {
  FileUploadOptions,
  UploadResult
} from '~/types/file-upload-types'
```

#### `useNewsletter.ts`
```typescript
import type {
  NewsletterSubscription,
  NewsletterSubscribeData
} from '~/types/newsletter-types'
```

## Phase 3: Mapper-Funktionen und Utilities

### 3.1 API Response Mapper
```typescript
// utils/api-mappers.ts
export function mapApiTeam(apiTeam: any): Team {
  return {
    id: apiTeam.id,
    name: apiTeam.name,
    description: apiTeam.description,
    hackathon_id: apiTeam.hackathon_id,
    max_members: apiTeam.max_members,
    is_open: apiTeam.is_open,
    created_by: apiTeam.created_by,
    created_at: apiTeam.created_at,
    // ... weitere Felder
  }
}

export function mapApiProject(apiProject: any): Project {
  return {
    id: apiProject.id,
    title: apiProject.title,
    description: apiProject.description,
    repository_url: apiProject.repository_url,
    // ... etc
  }
}
```

### 3.2 Transformations-Utilities
```typescript
// utils/type-transformers.ts
export function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase())
}

export function camelToSnake(str: string): string {
  return str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`)
}

export function transformKeys(
  obj: Record<string, any>,
  transformer: (key: string) => string
): Record<string, any> {
  return Object.keys(obj).reduce((acc, key) => {
    acc[transformer(key)] = obj[key]
    return acc
  }, {} as Record<string, any>)
}
```

## Phase 4: Testing und Validierung

### 4.1 Unit-Tests für jedes Composable
```typescript
// tests/composables/useTeams.test.ts
import { describe, it, expect } from 'vitest'
import { useTeams } from '~/composables/useTeams'

describe('useTeams', () => {
  it('should fetch teams', async () => {
    const { fetchTeams, teams } = useTeams()
    await fetchTeams()
    expect(teams.value).toBeInstanceOf(Array)
  })
  
  it('should handle errors', async () => {
    // Test Error-Handling
  })
})
```

### 4.2 TypeScript Validierung
```bash
# TypeScript Kompilierung prüfen
npx tsc --noEmit --project frontend3

# Typ-Inkonsistenzen finden
npx tsc --noEmit --strict --project frontend3
```

### 4.3 Integrationstests
- Testen mit bestehenden Komponenten
- E2E-Tests für kritische User Flows
- Performance-Tests für Composables

## Phase 5: Dokumentation und Schulung

### 5.1 Composable-README aktualisieren
```markdown
# Aktualisierte Composable-Architektur

## Typ-Import Pattern
```typescript
// Korrekt:
import type { Project, ProjectCreateData } from '~/types/project-types'

// Falsch:
interface Project { /* lokale Definition */ }
```

## 5.2 Typ-Dokumentation
- JSDoc Kommentare für alle Typen
- Beispiele für Typ-Verwendung
- Migration-Guide für bestehenden Code

## 5.3 Code-Review Checkliste
- [ ] Importiert zentrale Typen statt lokale Definitionen?
- [ ] Verwendet Enums statt String-Literale?
- [ ] Konsistente Feldnamen (snake_case für API)?
- [ ] TypeScript-Fehlerfrei?
- [ ] Unit-Tests vorhanden?

## Zeitplan und Aufwandsschätzung

### Woche 1: Vorbereitung und Typ-Konsolidierung
- Tag 1-2: Architektur-Entscheidungen und Tooling
- Tag 3-4: Typ-Dateien aktualisieren/erstellen
- Tag 5: Review und Validierung

### Woche 2-3: Composable-Migration
- Tag 1-2: `useTeams.ts` Migration
- Tag 3-4: `useProjects.ts` Migration  
- Tag 5-6: `useHackathons.ts` Migration
- Tag 7-8: `useComments.ts` und andere Composables
- Tag 9-10: Mapper-Funktionen und Utilities

### Woche 4: Testing und Dokumentation
- Tag 1-3: Unit-Tests schreiben
- Tag 4-5: Integrationstests und Validierung
- Tag 6-7: Dokumentation aktualisieren
- Tag 8-10: Bug-Fixing und Finalisierung

## Risiken und Mitigation

### Risiko 1: Breaking Changes
**Mitigation**: 
- Hybride Ansätze (beide Typen unterstützen)
- Deprecation-Warnings für alte Typen
- Schrittweise Migration mit Feature-Flags

### Risiko 2: Performance-Impact
**Mitigation**:
- Performance-Monitoring während Migration
- Benchmark-Tests für kritische Composables
- Lazy-Loading für große Typ-Definitionen

### Risiko 3: Team-Resistance
**Mitigation**:
- Frühzeitige Einbindung des Teams
- Klare Dokumentation und Schulung
- Positive Beispiele (`useAuth.ts` als Vorbild)

## Erfolgsmetriken

### Quantitative Metriken
- ✅ 100% der Composables verwenden zentrale Typen
- ✅ 0 TypeScript-Fehler nach Migration
- ✅ 100% Test-Abdeckung für kritische Composables
- ✅ < 5% Performance-Degradation

### Qualitative Metriken
- ✅ Verbesserte Developer Experience
- ✅ Einfachere Code-Wartung
- ✅ Bessere Type-Safety
- ✅ Konsistente Architektur

## Fazit

Die Migration zu zentralen Typ-Definitionen ist ein kritischer Schritt zur Verbesserung der Code-Qualität und Wartbarkeit des Projekts. Durch die strukturierte, phasenweise Herangehensweise können Risiken minimiert und ein reibungsloser Übergang gewährleistet werden.

Der positive Effekt wird sich in reduzierten Bugs, verbesserter Developer Productivity und einer konsistenteren Architektur manifestieren, die das Wachstum des Projekts langfristig unterstützt.