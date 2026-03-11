# Vue Composables - API-Abstraktion

## Übersicht

Diese Composables ersetzen direkte API-Aufrufe in Vue-Komponenten durch dedizierte, wiederverwendbare Funktionen. Jedes Composable kapselt die Datenabfragelogik, reaktiven State und Error-Handling für einen bestimmten API-Endpunkt oder eine Datenoperation.

## Implementierte Composables

### 1. `useAuth` - Authentifizierung
**Verantwortung**: Alle Authentifizierungsoperationen (Login, Registrierung, 2FA, Token-Management)

**Features**:
- Login mit Email/Passwort (mit 2FA-Unterstützung)
- Registrierung
- Passwort zurücksetzen
- E-Mail-Verifizierung
- OAuth-Login (GitHub, Google)
- Token-Refresh
- Automatisches Error-Handling

**Verwendung**:
```typescript
const { loginWithEmail, isLoading, error } = useAuth()

await loginWithEmail({ email, password })
```

### 2. `useFileUpload` - Datei-Uploads
**Verantwortung**: Datei-Uploads mit Progress-Tracking

**Features**:
- Einzel- und Mehrfach-Uploads
- Progress-Tracking
- Cancel-Funktionalität
- Automatisches Error-Handling
- TypeScript-Unterstützung für Dateitypen

**Verwendung**:
```typescript
const { uploadSingle, isUploading, progress } = useFileUpload()

const result = await uploadSingle(file, {
  onProgress: (percent) => console.log(percent)
})
```

### 3. `useNewsletter` - Newsletter-Abonnements
**Verantwortung**: Newsletter-An- und Abmeldungen

**Features**:
- Idempotency-Key-Unterstützung (verhindert doppelte Abonnements)
- E-Mail-Validierung
- Lokaler State-Cache
- Automatisches Error-Handling

**Verwendung**:
```typescript
const { subscribe, isLoading } = useNewsletter()

await subscribe(email, 'website_footer')
```

### 4. `useProjects` - Projekt-Management
**Verantwortung**: Alle Projekt-bezogenen Operationen

**Features**:
- Projekte auflisten und filtern
- Einzelne Projekte abrufen
- Projekte erstellen, aktualisieren und löschen
- Für Projekte voten (Upvote/Downvote)
- Projekt-Kommentare verwalten
- View-Count-Tracking
- Automatisches Error-Handling

**Verwendung**:
```typescript
const { fetchProjects, createProject, voteForProject } = useProjects()

const projects = await fetchProjects({ hackathon_id: 1 })
await createProject({ title: 'Mein Projekt', description: '...' })
await voteForProject(projectId, 'upvote')
```

### 5. `useTeams` - Team-Management
**Verantwortung**: Alle Team-bezogenen Operationen

**Features**:
- Teams auflisten und filtern
- Einzelne Teams abrufen
- Teams erstellen, aktualisieren und löschen
- Team-Mitglieder verwalten
- Team-Einladungen senden und verwalten
- Team beitreten/verlassen
- Team-Projekte abrufen
- Automatisches Error-Handling

**Verwendung**:
```typescript
const { fetchTeams, createTeam, addTeamMember } = useTeams()

const teams = await fetchTeams({ hackathon_id: 1 })
await createTeam({ name: 'Mein Team', hackathon_id: 1 })
await addTeamMember(teamId, { user_id: 123 })
```

### 6. `useHackathons` - Hackathon-Management
**Verantwortung**: Alle Hackathon-bezogenen Operationen

**Features**:
- Hackathons auflisten und filtern (aktiv, kommend, laufend)
- Einzelne Hackathons abrufen
- Hackathons erstellen, aktualisieren und löschen
- Für Hackathons registrieren/abmelden
- Registrierungsstatus prüfen
- Hackathon-Teams und -Projekte abrufen
- Automatisches Error-Handling

**Verwendung**:
```typescript
const { fetchHackathons, registerForHackathon } = useHackathons()

const hackathons = await fetchHackathons({ active_only: true })
await registerForHackathon(hackathonId)
```

### 7. `useComments` - Kommentar-System
**Verantwortung**: Alle Kommentar-bezogenen Operationen

**Features**:
- Projekt-Kommentare abrufen
- Kommentare erstellen, aktualisieren und löschen
- Für Kommentare voten (Upvote/Downvote)
- Antworten auf Kommentare erstellen
- Kommentar-Bäume erstellen (verschachtelte Darstellung)
- Kommentare nach Score oder Datum sortieren
- Automatisches Error-Handling

**Verwendung**:
```typescript
const { fetchProjectComments, createProjectComment, voteForComment } = useComments()

const comments = await fetchProjectComments(projectId)
await createProjectComment(projectId, { content: 'Toller Beitrag!' })
await voteForComment(commentId, 'upvote')
```

## API-Client Abstraktion

### `utils/api-client.ts`
Zentrale Klasse für alle HTTP-Requests mit folgenden Features:

1. **Automatisches Error-Handling**: Konsistente Error-Response-Formatierung
2. **Token-Refresh**: Automatisches Aktualisieren abgelaufener Tokens
3. **TypeScript-Support**: Strikte Typisierung für Request/Response
4. **SSR-Kompatibilität**: Server-Side Rendering Unterstützung
5. **Request-Interceptors**: Möglichkeit für globale Request-Modifikationen

**Verwendung**:
```typescript
import { useApiClient } from '~/utils/api-client'

const apiClient = useApiClient()
const data = await apiClient.get<User>('/api/me')
```

## Migrierte Komponenten

1. **`forgot-password.vue`** - Ersetzt durch `useAuth().forgotPassword()`
2. **`reset-password.vue`** - Ersetzt durch `useAuth().resetPassword()`
3. **`verify-email.vue`** - Ersetzt durch `useAuth().verifyEmail()`
4. **`AppFooterContent.vue`** - Ersetzt durch `useNewsletter().subscribe()`

## Refactored Auth-Store

Der Auth-Store wurde teilweise refactored, um direkte `fetch`-Aufrufe durch `apiClient` zu ersetzen:

- `resendVerificationEmail()` - ✅ Migriert
- `refreshAccessToken()` - ✅ Migriert  
- `logout()` - ✅ Migriert
- `fetchUserWithToken()` - ✅ Migriert
- `refreshUser()` - ✅ Migriert
- `loginWithEmail()` - ✅ Migriert
- `registerWithEmail()` - ✅ Migriert

## Architektur-Vorteile

1. **Entkopplung**: Komponenten sind von API-Implementierungsdetails isoliert
2. **Wiederverwendbarkeit**: Composables können überall in der Anwendung verwendet werden
3. **Konsistenz**: Einheitliches Error-Handling und Loading-States
4. **Testbarkeit**: Composables sind einfacher zu mocken und zu testen
5. **TypeScript-Sicherheit**: Strikte Typisierung für alle API-Antworten

## Nächste Schritte

1. **✅ Weitere Composables erstellen** - Alle geplanten Composables implementiert:
   - `useProjects` - ✅ Implementiert
   - `useTeams` - ✅ Implementiert
   - `useHackathons` - ✅ Implementiert
   - `useComments` - ✅ Implementiert

2. **Bestehende Stores migrieren**:
   - Team-Store - ⏳ In Planung
   - Project-Store - ⏳ In Planung
   - Voting-Store - ⏳ In Planung
   - Notification-Store - ⏳ In Planung

3. **Testing-Infrastruktur** für Composables implementieren:
   - Unit-Tests für jedes Composable
   - Integration-Tests mit Mock-API
   - E2E-Tests für kritische Workflows

4. **Weitere Komponenten migrieren**:
   - Projekt-Erstellungs-Formulare
   - Team-Management-Komponenten
   - Hackathon-Registrierungsseiten
   - Kommentar-Komponenten

5. **Performance-Optimierungen**:
   - Request-Caching implementieren
   - Debouncing für Such-Operationen
   - Optimistic Updates für schnelle UI-Updates

6. **Dokumentation vervollständigen** mit Beispielen und Best Practices