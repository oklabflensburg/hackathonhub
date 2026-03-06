# Atomic Design Refactoring Plan - Frontend

## Übersicht

Dieses Dokument beschreibt den umfassenden Plan zur Migration des Hackathon-Dashboard-Frontends zu einer Atomic Design-basierten Architektur. Basierend auf der erfolgreichen Implementierung für Team-Einladungen werden nun alle weiteren Komponenten nach demselben Muster refactored.

## Aktueller Stand

### Bereits implementiert ✅
- **Team-Einladungen**: Vollständige Atomic Design-Implementierung
  - Atome: `Button`, `Input`, `Avatar`, `LoadingSpinner`
  - Moleküle: `InvitationItem`, `InviteUserForm`, `UserSearchInput`
  - Organismen: `TeamInvitations`, `TeamInviteSection`
  - Composables: `useTeamInvitations`, `useUserSearch`
  - TypeScript-Typen: `team-invitations.ts`
  - Feature-Flags: `atomicTeamInvitations`, `improvedUserSearch`

### Atomic Design Verzeichnisstruktur
```
app/components/
├── atoms/           # Grundlegende UI-Elemente
├── molecules/       # Kombinationen von Atomen
├── organisms/       # Komplexe Komponenten aus Molekülen
├── templates/       # Seitenlayouts
└── [feature]/      # Feature-spezifische Komponenten (zu migrieren)
```

## Zu migrierende Bereiche (Prioritäten)

### Phase 1: Layout-Komponenten (Hohe Priorität)
**Ziel**: Migration der globalen Layout-Komponenten, die auf allen Seiten verwendet werden.

#### Komponenten:
1. `AppHeader.vue` → `organisms/layout/AppHeaderBar.vue` (bereits existiert)
2. `AppFooter.vue` → `organisms/layout/AppFooterContent.vue` (bereits existiert)
3. `AppSidebar.vue` → `organisms/layout/AppSidebar.vue` (neu)
4. `MobileBottomNav.vue` → `organisms/layout/MobileNavigation.vue` (neu)

#### Neue Atome/Moleküle:
- `NavigationItem.vue` (Molecule)
- `Logo.vue` (Atom)
- `ThemeToggle.vue` (Molecule)

### Phase 2: Projekt-Komponenten (Hohe Priorität)
**Ziel**: Migration der Projekt-bezogenen Komponenten.

#### Komponenten:
1. `CreatorInfo.vue` → `molecules/ProjectCreatorInfo.vue`
2. `ProjectActions.vue` → `molecules/ProjectActions.vue`
3. `ProjectDescription.vue` → `molecules/ProjectDescription.vue` (bereits existiert)
4. `ProjectImage.vue` → `molecules/ProjectImage.vue` (bereits existiert)
5. `ProjectHeader.vue` → `molecules/ProjectHeader.vue` (bereits existiert)

#### Neue Organismen:
- `ProjectDetailOrganism.vue` - Kombiniert alle Projekt-Komponenten
- `ProjectListOrganism.vue` - Bereits existiert

#### Composables:
- `useProjects.ts` - Projekt-Logik und Zustandsmanagement
- `useProjectVoting.ts` - Voting-Logik

### Phase 3: Hackathon-Komponenten (Hohe Priorität)
**Ziel**: Migration der Hackathon-bezogenen Komponenten.

#### Komponenten:
1. `HackathonEditForm.vue` → `organisms/forms/HackathonForm.vue` (bereits existiert)
2. `HackathonActions.vue` → `molecules/HackathonActions.vue`
3. `HackathonDescription.vue` → `molecules/HackathonDescription.vue`
4. `HackathonHero.vue` → `organisms/hackathons/HackathonHero.vue`
5. `HackathonStats.vue` → `molecules/HackathonStats.vue`

#### Neue Organismen:
- `HackathonDetailOrganism.vue` - Kombiniert alle Hackathon-Komponenten

#### Composables:
- `useHackathons.ts` - Hackathon-Logik und Zustandsmanagement

### Phase 4: Benutzer-Komponenten (Mittlere Priorität)
**Ziel**: Migration der Benutzer-bezogenen Komponenten.

#### Komponenten:
1. `UserCard.vue` → `molecules/UserCard.vue`
2. `UserProfileOverview.vue` → `organisms/profile/UserProfileOverview.vue`
3. `UserProfileSidebar.vue` → `organisms/profile/UserProfileSidebar.vue`
4. `UsersPageHeader.vue` → `molecules/UsersPageHeader.vue`

#### Composables:
- `useUserProfile.ts` - Benutzerprofil-Logik

### Phase 5: Notification-Komponenten (Mittlere Priorität)
**Ziel**: Migration der Benachrichtigungs-Komponenten.

#### Komponenten:
1. `NotificationContainer.vue` → `organisms/notifications/NotificationContainer.vue`
2. `NotificationSettings.vue` → `organisms/notifications/NotificationSettings.vue`

#### Composables:
- `useNotifications.ts` - Benachrichtigungs-Logik

### Phase 6: Utility-Komponenten (Niedrige Priorität)
**Ziel**: Migration der verbleibenden Utility-Komponenten.

#### Komponenten:
1. `ImprovedStatsCard.vue` → `molecules/StatsCard.vue`
2. `LanguageSwitcher.vue` → `molecules/LanguageSwitcher.vue`
3. `TeamSelection.vue` → `molecules/TeamSelection.vue`

## Technische Implementierung

### 1. Feature-Flags
Erweiterung der bestehenden Feature-Flag-Implementierung:
```typescript
// feature-flags.ts
export interface FeatureFlags {
  atomicTeamInvitations: boolean      // Bereits existiert
  atomicLayoutComponents: boolean     // Neu
  atomicProjectComponents: boolean    // Neu
  atomicHackathonComponents: boolean  // Neu
  atomicUserComponents: boolean       // Neu
  atomicNotificationComponents: boolean // Neu
}
```

### 2. TypeScript-Typen
Erstellung zentraler TypeScript-Typen für jede Domäne:
- `project-types.ts` - Projekt-bezogene Typen
- `hackathon-types.ts` - Hackathon-bezogene Typen
- `user-types.ts` - Benutzer-bezogene Typen
- `notification-types.ts` - Benachrichtigungs-bezogene Typen

### 3. Composables
Implementierung von wiederverwendbaren Composables für jede Domäne:
- Zustandsmanagement
- API-Integration
- Geschäftslogik
- Error-Handling

### 4. Testing-Strategie
- **Unit Tests**: Für Atome, Moleküle und Composables
- **Integration Tests**: Für Organismen
- **E2E Tests**: Für vollständige Seiten und Workflows

## Migrations-Ansatz

### Schrittweise Migration
1. **Analyse**: Bestehende Komponenten analysieren
2. **Atomic Design-Klassifizierung**: Komponenten in Atome, Moleküle, Organismen einteilen
3. **Refactoring**: Komponenten in Atomic Design-Struktur migrieren
4. **Feature-Flag**: Neue Komponenten hinter Feature-Flag aktivieren
5. **Testing**: Umfassende Tests durchführen
6. **Rollout**: Feature-Flag für bestimmte Benutzer aktivieren
7. **Monitoring**: Performance und Fehler überwachen
8. **Vollständige Aktivierung**: Feature-Flag für alle Benutzer aktivieren

### Rollback-Plan
Bei Problemen kann schnell auf die alte Implementierung zurückgesetzt werden:
1. Feature-Flag auf `false` setzen
2. Backup-Code in `*.vue.backup` Dateien verfügbar
3. Gradueller Rollout ermöglicht schrittweise Korrekturen

## Erfolgskriterien

### Technische Kriterien
- [ ] Build ohne Fehler
- [ ] TypeScript-Typen korrekt definiert
- [ ] Keine Regressionen in bestehenden Funktionen
- [ ] Performance verbessert oder gleichbleibend
- [ ] Test-Abdeckung mindestens 80%

### Business Kriterien
- [ ] Benutzer können alle Funktionen wie gewohnt nutzen
- [ ] Keine negativen Auswirkungen auf UX
- [ ] Entwickler-Produktivität verbessert
- [ ] Wartbarkeit des Codes verbessert

## Zeitplan (Phasen)

### Phase 1: Layout-Komponenten
- **Dauer**: 3-5 Tage
- **Lieferumfang**: Alle Layout-Komponenten migriert
- **Risiken**: Gering (ähnlich wie Team-Einladungen)

### Phase 2: Projekt-Komponenten
- **Dauer**: 5-7 Tage
- **Lieferumfang**: Projekt-bezogene Komponenten migriert
- **Risiken**: Mittel (komplexe Geschäftslogik)

### Phase 3: Hackathon-Komponenten
- **Dauer**: 4-6 Tage
- **Lieferumfang**: Hackathon-bezogene Komponenten migriert
- **Risiken**: Mittel (ähnlich wie Projekte)

### Phase 4-6: Restliche Komponenten
- **Dauer**: 7-10 Tage
- **Lieferumfang**: Alle verbleibenden Komponenten migriert
- **Risiken**: Niedrig (einfachere Komponenten)

## Verantwortlichkeiten

### Frontend Team
- Implementierung der Atomic Design-Komponenten
- Erstellung der TypeScript-Typen
- Implementierung der Composables
- Unit-Testing

### Design Team
- Konsistenz mit Design System
- Design-Review der neuen Komponenten
- Accessibility-Review

### QA Team
- Testing der migrierten Komponenten
- Regressionstesting
- Performance-Testing

### Product Team
- Priorisierung der Migrations-Reihenfolge
- User Acceptance Testing
- Feedback-Sammlung

## Nächste Schritte

1. **Genehmigung**: Diesen Plan mit Stakeholdern besprechen und genehmigen
2. **Phase 1 starten**: Layout-Komponenten migrieren
3. **Testing**: Umfassende Tests durchführen
4. **Rollout**: Schrittweise Aktivierung über Feature-Flags
5. **Monitoring**: Performance und Fehler überwachen
6. **Iteration**: Basierend auf Feedback anpassen

## Anhang

### Atomic Design Prinzipien
1. **Atome**: Grundlegende UI-Elemente (Button, Input, etc.)
2. **Moleküle**: Kombinationen von Atomen (FormField, SearchBar, etc.)
3. **Organismen**: Komplexe Komponenten aus Molekülen (CommentSection, etc.)
4. **Templates**: Seitenlayouts
5. **Seiten**: Konkrete Instanzen von Templates mit echten Daten

### Vorteile von Atomic Design
- **Wiederverwendbarkeit**: Komponenten können in verschiedenen Kontexten verwendet werden
- **Konsistenz**: Einheitliches Design über die gesamte Anwendung
- **Wartbarkeit**: Klare Trennung der Zuständigkeiten
- **Testbarkeit**: Einfacheres Unit-Testing durch isolierte Komponenten
- **Skalierbarkeit**: Einfache Erweiterung des Design Systems