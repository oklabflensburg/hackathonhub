# Atomic Design Refactoring: Team Invitations

## Übersicht

Dieses Dokument beschreibt die Migration der Team-Einladungsfunktionalität von einer inline-Implementierung zu einer Atomic Design-basierten Architektur.

## Ziele

1. **Wiederverwendbarkeit**: Komponenten können in anderen Kontexten verwendet werden (Admin-Bereich, Benachrichtigungen)
2. **Wartbarkeit**: Klare Trennung der Zuständigkeiten durch Atomic Design Ebenen
3. **Testbarkeit**: Einfacheres Unit-Testing durch isolierte Komponenten
4. **Konsistenz**: Einheitliches Design und Verhalten über die gesamte Anwendung
5. **Migration Safety**: Feature Flags ermöglichen schrittweise Migration

## Atomic Design Ebenen

### 1. Atome (Atoms)
- **`LoadingSpinner.vue`** (bereits existierend)
- **`Avatar.vue`** (bereits existierend)
- **`Button.vue`** (bereits existierend)
- **`Input.vue`** (bereits existierend)

### 2. Moleküle (Molecules)
- **`InvitationItem.vue`** - Einzelnes Einladungselement mit Avatar, Name, Status und Aktionen
- **`InviteUserForm.vue`** - Formular zum Einladen von Benutzern mit Autocomplete
- **`UserSearchInput.vue`** - Eingabefeld mit Debouncing und Vorschlägen

### 3. Organismen (Organisms)
- **`TeamInvitations.vue`** - Liste aller ausstehenden Einladungen mit Header und Empty States
- **`TeamInviteSection.vue`** - Kombiniertes Einladungsformular mit Team-Status-Informationen

### 4. Templates (Templates)
- **Team Detail Page Template** - Verwendet die Organismen in der richtigen Layout-Struktur

### 5. Seiten (Pages)
- **`teams/[id]/index.vue`** - Migrierte Team-Detailseite mit Atomic Design Komponenten

## Composables

### `useTeamInvitations.ts`
Verwaltet den Zustand und die Logik für Team-Einladungen:
- Abrufen von Einladungen
- Senden von Einladungen
- Stornieren von Einladungen
- Real-time Updates (Polling)

### `useUserSearch.ts`
Verwaltet die Benutzersuche mit Debouncing:
- API-Aufrufe mit Debouncing
- Filterung von bereits vorhandenen Teammitgliedern
- Loading- und Error-States

## TypeScript Typen

### `team-invitations.ts`
Definiert alle Schnittstellen für Team-Einladungen:
- `TeamInvitation` - Vollständige Einladungsdaten
- `UserSearchResult` - Benutzersuchergebnis
- Props-Schnittstellen für alle Komponenten
- Hilfsfunktionen für Formatierung

## Feature Flags

### `feature-flags.ts`
Ermöglicht schrittweise Migration:
- `atomicTeamInvitations`: Aktiviert Atomic Design Komponenten
- `improvedUserSearch`: Aktiviert verbesserte Benutzersuche
- `realTimeInvitations`: Aktiviert Polling für Echtzeit-Updates
- `newTeamManagementUI`: Aktiviert neue UI (zukünftig)

## Migration

### Vorher (Inline-Implementierung)
- Einladungsformular und Liste inline in `teams/[id]/index.vue`
- Duplizierte Logik über mehrere Seiten
- Schwierige Wartung und Testing

### Nachher (Atomic Design)
- **Einladungsformular**: `TeamInviteSection` Organism
- **Einladungsliste**: `TeamInvitations` Organism
- **Wiederverwendbare Logik**: `useTeamInvitations` und `useUserSearch` Composables
- **Konsistente Typen**: `team-invitations.ts`

## Vorteile

### 1. Code-Qualität
- **Type Safety**: Vollständige TypeScript-Unterstützung
- **Separation of Concerns**: Klare Trennung von UI, Logik und Daten
- **Reusability**: Komponenten können in anderen Kontexten verwendet werden

### 2. Developer Experience
- **Autocomplete**: Bessere IDE-Unterstützung durch TypeScript
- **Documentation**: Selbst-dokumentierende Komponenten mit Props-Schnittstellen
- **Debugging**: Isolierte Komponenten sind einfacher zu debuggen

### 3. Performance
- **Debouncing**: Verbesserte Benutzersuche mit Debouncing
- **Lazy Loading**: Komponenten können lazy geladen werden
- **Optimistic Updates**: Sofortiges UI-Feedback bei Aktionen

### 4. Wartbarkeit
- **Centralized Types**: Einheitliche Typdefinitionen
- **Consistent Patterns**: Atomic Design sorgt für konsistente Patterns
- **Easy Updates**: Änderungen nur an einer Stelle notwendig

## Testing Strategie

### Unit Tests
- **Molecules**: Testen der einzelnen UI-Komponenten
- **Composables**: Testen der Geschäftslogik
- **Types**: TypeScript-Compiler als erster Test

### Integration Tests
- **Organisms**: Testen der Komponenten-Interaktion
- **Pages**: Testen der vollständigen Seiten

### E2E Tests
- **User Flows**: Testen des gesamten Einladungs-Workflows
- **Edge Cases**: Testen von Grenzfällen (Team voll, Berechtigungen)

## Backend API Änderungen

### Benutzersuche API
Die Atomic Design Implementierung erfordert eine verbesserte Benutzersuche-API:

#### Vorher (Problem)
- `/api/users` gab alle Benutzer zurück, unabhängig vom Suchbegriff
- Keine Filterung nach Benutzernamen möglich
- Frontend musste alle Benutzer laden und client-seitig filtern

#### Nachher (Lösung)
- **API-Endpoint**: `/api/users?username={query}&limit={limit}`
- **Filterung**: Case-insensitive partial matching auf Benutzernamen
- **Implementierung**: `search_users` Methode im `UserService`
- **Repository**: `search_by_username` im `UserRepository`

#### Code-Änderungen
1. **`backend/app/api/v1/users/routes.py`**:
   ```python
   @router.get("", response_model=list[User])
   async def get_users(
       username: str = None,
       skip: int = 0,
       limit: int = 100,
       db: Session = Depends(get_db)
   ):
       if username:
           return user_service.search_users(db, username, limit)
       else:
           return user_service.get_users(db, skip=skip, limit=limit)
   ```

2. **`backend/app/services/user_service.py`**:
   ```python
   def search_users(
       self, db: Session, username_query: str, limit: int = 10
   ) -> List[UserSchema]:
       users = self.user_repo.search_by_username(db, username_query, limit)
       return [UserSchema.model_validate(user) for user in users]
   ```

3. **`backend/app/repositories/user_repository.py`**:
   ```python
   def search_by_username(self, db: Session, username_query: str, limit: int = 10):
       return db.query(User).filter(
           User.username.ilike(f"%{username_query}%")
       ).limit(limit).all()
   ```

#### Vorteile
- **Performance**: Weniger Datenübertragung
- **Skalierbarkeit**: Server-seitige Filterung bei vielen Benutzern
- **Konsistenz**: Gleiche Logik wie andere Such-APIs im System

## Nächste Schritte

### Kurzfristig (Phase 6)
1. **Testing**: Unit-Tests für die neuen Komponenten
2. **Documentation**: API-Dokumentation für die Composables
3. **Performance**: Optimierung der Debouncing-Logik

### Mittelfristig
1. **Admin Area**: Verwenden der Komponenten im Admin-Bereich
2. **Notifications**: Integration mit dem Benachrichtigungssystem
3. **Real-time**: WebSocket-Integration für Echtzeit-Updates

### Langfristig
1. **Design System**: Integration in das globale Design System
2. **Accessibility**: Verbesserung der Barrierefreiheit
3. **Internationalization**: Vollständige i18n-Unterstützung

## Rollback Plan

Bei Problemen kann schnell auf die alte Implementierung zurückgesetzt werden:

1. **Feature Flag**: `atomicTeamInvitations` auf `false` setzen
2. **Backup**: Original-Code in `index.vue.backup` gespeichert
3. **Gradual Rollout**: Kann schrittweise für bestimmte Teams aktiviert werden

## Erfolgskriterien

- [x] Build ohne Fehler
- [x] TypeScript-Typen korrekt definiert
- [x] Komponenten wiederverwendbar
- [x] Feature Flags funktionieren
- [ ] Unit Tests vorhanden
- [ ] Performance verbessert
- [ ] Developer Feedback positiv

## Benachrichtigungssystem Integration

### Übersicht
Die Atomic Design Implementierung der Team-Einladungen ist jetzt vollständig mit dem Benachrichtigungssystem integriert. Bei wichtigen Ereignissen im Einladungs-Workflow werden automatisch Benachrichtigungen gesendet.

### Unterstützte Benachrichtigungen

#### 1. Team-Einladung gesendet
**Trigger**: Wenn ein Team-Besitzer einen Benutzer zu seinem Team einlädt
**Empfänger**: Eingeladener Benutzer
**Implementierung**:
- `NotificationService.send_team_invitation_notification()`
- Wird in `TeamService.create_team_invitation()` aufgerufen
- Sendet E-Mail, Push und In-App-Benachrichtigungen

#### 2. Team-Einladung angenommen
**Trigger**: Wenn ein eingeladener Benutzer die Einladung annimmt
**Empfänger**: Team-Besitzer
**Implementierung**:
- `NotificationService.send_team_member_added_notification()`
- Wird in `TeamService.accept_team_invitation()` aufgerufen
- Informiert den Team-Besitzer über das neue Teammitglied

#### 3. Team-Einladung abgelehnt
**Trigger**: Wenn ein eingeladener Benutzer die Einladung ablehnt
**Empfänger**: Team-Besitzer
**Implementierung**:
- `NotificationService.send_team_invitation_declined_notification()`
- Wird in `TeamService.decline_team_invitation()` aufgerufen
- Informiert den Team-Besitzer über die abgelehnte Einladung

### Backend-Implementierung

#### Code-Änderungen in `backend/app/services/team_service.py`:

1. **Import des NotificationService**:
   ```python
   from app.services.notification_service import NotificationService
   ```

2. **Initialisierung im Konstruktor**:
   ```python
   def __init__(self):
       # ... existing repositories
       self.notification_service = NotificationService()
   ```

3. **Benachrichtigung bei Einladungserstellung**:
   ```python
   def create_team_invitation(self, ...):
       # ... existing logic
       
       # Send notification to invited user
       try:
           self.notification_service.send_team_invitation_notification(
               db=db,
               team_id=team_id,
               invited_user_id=invitation_create.invitee_id,
               inviter_id=inviter_id,
               language="en"
           )
       except Exception as e:
           # Log error but don't fail the invitation creation
           logging.error(f"Failed to send team invitation notification: {e}")
   ```

4. **Benachrichtigung bei Einladungsannahme**:
   ```python
   def accept_team_invitation(self, ...):
       # ... existing logic
       
       # Send notification to team owner about accepted invitation
       try:
           self.notification_service.send_team_member_added_notification(
               db=db,
               team_id=invitation.team_id,
               user_id=user_id,
               added_by_id=user_id,
               language="en"
           )
       except Exception as e:
           logging.error(f"Failed to send team member added notification: {e}")
   ```

5. **Benachrichtigung bei Einladungsablehnung**:
   ```python
   def decline_team_invitation(self, ...):
       # ... existing logic
       
       # Send notification to team owner about declined invitation
       try:
           self.notification_service.\
               send_team_invitation_declined_notification(
                   db=db,
                   team_id=invitation.team_id,
                   invited_user_id=user_id,
                   inviter_id=invitation.inviter_id,
                   language="en"
               )
       except Exception as e:
           logging.error(
               f"Failed to send team invitation declined notification: {e}"
           )
   ```

### Fehlerbehandlung
- Benachrichtigungsfehler werden geloggt, aber beeinträchtigen nicht den Haupt-Workflow
- Graceful degradation: Einladungen funktionieren auch ohne Benachrichtigungen
- Alle Exceptions werden abgefangen und geloggt

### Vorteile der Integration
1. **Automatische Benachrichtigungen**: Keine manuellen Aufrufe notwendig
2. **Konsistenter Workflow**: Benutzer werden über wichtige Ereignisse informiert
3. **Mehrkanal-Support**: E-Mail, Push und In-App-Benachrichtigungen
4. **Internationalisierung**: Unterstützung für multiple Sprachen
5. **Robuste Fehlerbehandlung**: Hauptfunktionalität bleibt intakt

## Bekannte Probleme und Lösungen

### Problem: Doppelte API-Aufrufe
**Symptom**: Der API-Endpoint `/api/teams/{id}/invitations` wird mehrfach aufgerufen.

**Ursache**:
1. `TeamInvitations` Komponente hat `poll-interval="30000"` (30 Sekunden Polling) für Auto-Refresh
2. `TeamInviteSection` Komponente wird ebenfalls gerendert (für Team-Besitzer)
3. `InviteUserForm` innerhalb von `TeamInviteSection` instanziiert sein eigenes `useTeamInvitations` Composable
4. Beide Composable-Instanzen können API-Aufrufe tätigen

**Lösung**:
1. Polling-Interval bleibt aktiv (30000ms) für Auto-Refresh der Einladungsliste
2. `InviteUserForm` verwendet jetzt direkt den Team-Store anstatt das Composable
3. Dadurch wird nur eine Composable-Instanz für das Abrufen von Einladungen verwendet

**Code-Änderungen**:
1. **`frontend3/app/components/molecules/InviteUserForm.vue`**:
   - Importiert `useTeamStore` anstatt `useTeamInvitations`
   - Verwendet `teamStore.inviteToTeam()` direkt
   - Kein separates Composable-Instance mehr

2. **Polling bleibt aktiv**:
   ```vue
   <TeamInvitations
     :poll-interval="30000"  <!-- Auto-Polling bleibt aktiv -->
   />
   ```

**Vorteile**:
- Auto-Polling bleibt für Real-time Updates aktiv
- Keine doppelten API-Aufrufe mehr
- Bessere Trennung der Zuständigkeiten
- `InviteUserForm` ist jetzt unabhängig vom Einladungs-Status

## Changelog

### 2026-03-02: Bugfix - Doppelte API-Aufrufe
- Polling-Interval in Team-Detailseite auf 0 gesetzt
- Composable-Logik verbessert: Polling nur bei `autoFetch: true`
- Build erfolgreich ohne Fehler

### 2026-03-02: Initiale Implementierung
- Alle Atomic Design Komponenten erstellt
- TypeScript Typen definiert
- Composables implementiert
- Team-Detailseite migriert
- Feature Flags hinzugefügt
- Dokumentation erstellt

## Verantwortlichkeiten

- **Frontend Team**: Wartung und Erweiterung der Komponenten
- **Design Team**: Konsistenz mit Design System
- **QA Team**: Testing und Qualitätssicherung
- **Product Team**: Feature Requests und Priorisierung