# Plan: Refactoring von Vue-Komponenten zur Verwendung von Composables

## Aktueller Stand

### Vorhandene Composables
1. `useComments.ts` - Kommentar-Operationen
2. `useFeatureFlags.ts` - Feature-Flags
3. `useHackathonData.ts` - Hackathon-Daten
4. `useHackathonsList.ts` - Hackathon-Listen
5. `useLayoutNavigation.ts` - Layout-Navigation
6. `useNotifications.ts` - Benachrichtigungen
7. `usePrivacySettings.ts` - Datenschutzeinstellungen
8. `useProjectComments.ts` - Projektkommentare
9. `useProjectFilters.ts` - Projektfilter
10. `useProjects.ts` - Projekt-Operationen
11. `useProjectVoting.ts` - Projekt-Voting
12. `useSettings.ts` - Einstellungen
13. `useTeamInvitations.ts` - Team-Einladungen
14. `useTeamMembers.ts` - Team-Mitglieder
15. `useTeams.ts` - Team-Operationen
16. `useTheme.ts` - Theme-Management
17. `useUserProfile.ts` - Benutzerprofil
18. `useUserSearch.ts` - Benutzersuche

### API-Endpunkte (Backend)
Basierend auf der Analyse der `routes.py`-Dateien:

#### Authentication (`/api/auth`)
- `POST /login` - Login
- `POST /login/json` - Login (JSON)
- `POST /refresh` - Token-Refresh
- `POST /logout` - Logout
- `GET /google` - Google OAuth
- `GET /google/callback` - Google Callback
- `POST /register` - Registrierung
- `POST /forgot-password` - Passwort vergessen
- `POST /reset-password` - Passwort zurücksetzen
- `GET /github` - GitHub OAuth
- `GET /github/callback` - GitHub Callback
- `POST /verify-email` - E-Mail-Verifizierung
- `POST /resend-verification` - Verifizierung erneut senden
- `POST /verify-2fa` - 2FA-Verifizierung
- `POST /verify-2fa-backup` - 2FA-Backup-Verifizierung

#### Users (`/api/users`)
- `GET /me` - Aktueller Benutzer
- `PATCH /me` - Benutzer aktualisieren
- `GET /me/stats` - Benutzerstatistiken
- `GET /me/projects` - Benutzerprojekte
- `GET /me/votes` - Benutzer-Votes
- `GET /me/teams/{hackathon_id}` - Benutzerteams für Hackathon
- `GET /{user_id}/teams` - Benutzerteams
- `GET /{user_id}` - Benutzer abrufen
- `PUT /{user_id}` - Benutzer aktualisieren
- `DELETE /{user_id}` - Benutzer löschen
- `GET /{user_id}/profile` - Benutzerprofil

#### Projects (`/api/projects`)
- `GET /{project_id}` - Projekt abrufen
- `PUT /{project_id}` - Projekt aktualisieren
- `DELETE /{project_id}` - Projekt löschen
- `POST /{project_id}/vote` - Für Projekt voten
- `GET /{project_id}/vote-stats` - Vote-Statistiken
- `POST /{project_id}/view` - View-Inkrement
- `DELETE /{project_id}/vote` - Vote entfernen
- `GET /{project_id}/comments` - Projektkommentare
- `POST /{project_id}/comments` - Kommentar erstellen

#### Teams (`/api/teams`)
- `GET /{team_id}` - Team abrufen
- `PUT /{team_id}` - Team aktualisieren
- `DELETE /{team_id}` - Team löschen
- `GET /{team_id}/members` - Team-Mitglieder
- `GET /{team_id}/projects` - Team-Projekte
- `POST /{team_id}/members` - Mitglied hinzufügen
- `DELETE /{team_id}/members/{user_id}` - Mitglied entfernen
- `GET /{team_id}/invitations` - Team-Einladungen
- `POST /{team_id}/invitations` - Einladung erstellen
- `POST /invitations/{invitation_id}/accept` - Einladung annehmen
- `POST /invitations/{invitation_id}/decline` - Einladung ablehnen
- `DELETE /invitations/{invitation_id}` - Einladung löschen

#### Hackathons (`/api/hackathons`)
- `GET /{hackathon_id}` - Hackathon abrufen
- `PUT /{hackathon_id}` - Hackathon aktualisieren
- `DELETE /{hackathon_id}` - Hackathon löschen
- `POST /{hackathon_id}/register` - Für Hackathon registrieren
- `GET /{hackathon_id}/projects` - Hackathon-Projekte
- `GET /{hackathon_id}/teams` - Hackathon-Teams

#### Notifications (`/api/notifications`)
- `POST /read-all` - Alle als gelesen markieren
- `GET /preferences` - Benachrichtigungseinstellungen
- `POST /preferences/{notification_type}/{channel}` - Einstellung aktualisieren
- `GET /push-subscriptions` - Push-Abonnements
- `POST /push-subscriptions` - Push-Abonnement erstellen
- `GET /unread-count` - Ungelesene Anzahl
- `GET /{notification_id}` - Benachrichtigung abrufen
- `POST /{notification_id}/read` - Als gelesen markieren
- `DELETE /push-subscriptions/{subscription_id}` - Abonnement löschen

#### Comments (`/api/comments`)
- `PUT /{comment_id}` - Kommentar aktualisieren
- `DELETE /{comment_id}` - Kommentar löschen
- `POST /{comment_id}/vote` - Für Kommentar voten
- `DELETE /{comment_id}/vote` - Kommentar-Vote entfernen

#### Settings (`/api/settings`)
- `GET /security` - Sicherheitseinstellungen
- `POST /security/2fa/enable` - 2FA aktivieren
- `POST /security/2fa/verify` - 2FA verifizieren
- `POST /security/2fa/disable` - 2FA deaktivieren
- `GET /` - Einstellungen abrufen
- `PUT /` - Einstellungen aktualisieren

#### Newsletter (`/api/newsletter`)
- `POST /subscribe` - Newsletter abonnieren
- `POST /unsubscribe` - Newsletter abbestellen

#### Uploads (`/api/uploads`)
- `POST /upload` - Datei hochladen

#### Push (`/api/push`)
- `GET /vapid-public-key` - VAPID Public Key

#### Compatibility (`/api/compatibility`)
- `GET /push-subscriptions` - Push-Abonnements (Kompatibilität)

#### Me (`/api/me`)
- `GET /me` - Aktueller Benutzer (Details)
- `GET /me/votes` - Benutzer-Votes
- `GET /me/registrations` - Hackathon-Registrierungen
- `GET /me/invitations` - Team-Einladungen

## Identifizierte Lücken

### Fehlende Composables
1. **Authentication** - Kein dediziertes Composable für Auth-Operationen
   - Login, Register, Logout, Token-Refresh
   - Passwort zurücksetzen, E-Mail-Verifizierung
   - OAuth-Flows (Google, GitHub)

2. **User Management** - `useUserProfile.ts` existiert, deckt aber nicht alle Endpunkte ab
   - Benutzerstatistiken, Benutzerprofil, Benutzerteams

3. **File Uploads** - Kein Composable für Datei-Uploads
   - `POST /api/uploads/upload`

4. **Newsletter** - Kein Composable für Newsletter-Operationen
   - Abonnieren/Abbestellen

5. **Push Notifications** - Kein Composable für Push-Operationen
   - VAPID Key, Abonnement-Management

6. **Hackathon Registration** - Teilweise abgedeckt durch `useHackathonData.ts`
   - Registrierung für Hackathons fehlt

7. **Comment Voting** - Teilweise abgedekct durch `useComments.ts` und `useProjectComments.ts`
   - Kommentar-Voting könnte eigenes Composable benötigen

8. **Team Invitations** - `useTeamInvitations.ts` existiert, aber nicht vollständig
   - Annehmen/Ablehnen von Einladungen

### Direkte API-Aufrufe in Komponenten
Basierend auf der Suche:

1. `forgot-password.vue` - `POST /api/auth/forgot-password`
2. `reset-password.vue` - `POST /api/auth/reset-password`
3. `verify-email.vue` - `POST /api/auth/verify-email`
4. `AppFooterContent.vue` - `POST /api/newsletter/subscribe`
5. Auth-Store enthält viele direkte `fetch`-Aufrufe

## Architekturvorschlag

### Composable-Struktur
Jedes Composable sollte folgende Eigenschaften haben:
- Klare Zuständigkeit für einen bestimmten Domänenbereich
- Reaktive State-Variablen (`ref`, `reactive`)
- Computed Properties für abgeleitete Daten
- Methoden für API-Operationen
- Error-Handling und Loading-States
- Optionale Konfiguration über Parameter

### Namenskonventionen
- `use{Resource}{Operation}` oder `use{Resource}`
- Beispiele: `useAuth`, `useUserStats`, `useFileUpload`, `useNewsletter`

### Gemeinsame Basis
Ein Basis-Composable oder Utility-Funktionen für:
- API-Client mit Authentication
- Standardisierte Error-Handling
- Loading-State-Management

## Zu erstellende Composables

### Phase 1: Kritische Lücken
1. `useAuth.ts` - Authentication-Operationen
2. `useFileUpload.ts` - Datei-Uploads
3. `useNewsletter.ts` - Newsletter-Abonnements
4. `usePushNotifications.ts` - Push-Benachrichtigungen

### Phase 2: Erweiterung bestehender Composables
5. `useUserStats.ts` - Benutzerstatistiken
6. `useHackathonRegistration.ts` - Hackathon-Registrierung
7. `useCommentVoting.ts` - Kommentar-Voting
8. `useTeamInvitationActions.ts` - Team-Einladungsaktionen

### Phase 3: Refactoring bestehender Logik
9. Migration von Auth-Store-Logik zu `useAuth`
10. Migration von direkten `fetch`-Aufrufen in Komponenten
11. Aktualisierung aller Komponenten zur Verwendung der Composables

## Priorisierung

1. **Höchste Priorität**: Authentication-Composable, da es in vielen Komponenten verwendet wird
2. **Hohe Priorität**: Newsletter und File Upload, da sie direkte Aufrufe haben
3. **Mittlere Priorität**: Erweiterung bestehender Composables
4. **Niedrige Priorität**: Optimierung und Konsolidierung

## Nächste Schritte

1. Detaillierte Spezifikation für jedes Composable erstellen
2. Implementierungsplan mit konkreten Aufgaben
3. Teststrategie definieren
4. Migration planen (schrittweise oder Big Bang)
5. Dokumentation der neuen Composables