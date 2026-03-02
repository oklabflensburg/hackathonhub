# Phase 3 Refactoring Plan - Organisms und Seiten-Refactoring

## Übersicht

Phase 3 des Atomic Design Refactorings konzentriert sich auf die Refaktorierung der verbleibenden großen Seiten durch Extraktion von Organism-Komponenten und Integration der bereits erstellten Atoms und Molecules.

## Aktueller Status

### ✅ Abgeschlossen
- **Phase 1 (Atoms)**: Button, Input, LoadingSpinner, Avatar, Card, Tag
- **Phase 2 (Molecules)**: FormField, SearchBar, Pagination, Alert, und 20+ weitere Molecules
- **Teilweise Phase 3**: CommentSection, ProjectForm, HackathonForm, ProfileHeader, etc.

### ⚠️ In Arbeit / Geplant
- Refaktorierung der größten Seiten (32k+ Zeichen)
- Erstellung fehlender Organism-Komponenten
- Integration und Migration bestehender Komponenten

## Priorisierte Seiten für Refactoring

### 1. Team-Detailseite (`teams/[id]/index.vue`) - 32.288 Zeichen
**Aktueller Zustand**: Verwendet `TeamDetailHeader`, aber viel Inline-Code für Mitgliederliste und Projekte

**Zu erstellende Organisms**:
- `TeamMembers.vue` - Mitgliederliste mit Rollenverwaltung
- `TeamProjects.vue` - Projekte des Teams
- `TeamDescription.vue` - Beschreibung mit Bearbeitungsfunktion
- `TeamInvitations.vue` - Einladungsverwaltung (falls vorhanden)

**Refactoring-Strategie**:
1. `TeamMembers` Organism extrahieren (Zeilen 50-150+)
2. `TeamProjects` Organism extrahieren (falls vorhanden)
3. `TeamDescription` als Molecule extrahieren
4. Seite auf ~8.000 Zeichen reduzieren

### 2. Profilseite (`profile.vue`) - 26.970 Zeichen
**Aktueller Zustand**: Verwendet `ProfileHeader` und `UserSettingsForm`, aber viel Inline-Code

**Zu erstellende Organisms**:
- `ProfileOverview.vue` - Benutzerübersicht mit Statistiken
- `UserProjects.vue` - Projekte des Benutzers
- `UserTeams.vue` - Teams des Benutzers
- `ProfileSettings.vue` - Einstellungen (evtl. erweitern)

**Refactoring-Strategie**:
1. Tab-basierte Navigation extrahieren
2. Jeden Tab-Inhalt als separate Organism-Komponente
3. Gemeinsame Logik in Composable `useProfile` extrahieren
4. Seite auf ~10.000 Zeichen reduzieren

### 3. Hackathon-Detailseite (`hackathons/[id]/index.vue`) - 25.544 Zeichen
**Aktueller Zustand**: Verwendet mehrere Komponenten, aber könnte weiter strukturiert werden

**Zu erstellende Organisms**:
- `HackathonInfo.vue` - Grundinformationen und Beschreibung
- `HackathonProjects.vue` - Projekte im Hackathon
- `HackathonParticipants.vue` - Teilnehmerliste (evtl. erweitern)
- `HackathonSidebar.vue` - Sidebar mit Aktionen und Statistiken

**Refactoring-Strategie**:
1. Bestehende Komponenten besser organisieren
2. Tab-Navigation für Projekte/Teilnehmer/Regeln
3. Gemeinsame Logik in Composable `useHackathon` extrahieren
4. Seite auf ~12.000 Zeichen reduzieren

### 4. Notifications-Seite (`notifications.vue`) - 23.719 Zeichen
**Aktueller Zustand**: Verwendet `NotificationSettings` und `NotificationContainer`

**Zu erstellende Organisms**:
- `NotificationList.vue` - Liste der Benachrichtigungen mit Filter
- `NotificationFilters.vue` - Filter- und Sortieroptionen
- `NotificationPreferences.vue` - Einstellungen (evtl. erweitern)

**Refactoring-Strategie**:
1. Filterlogik in Composable `useNotifications` extrahieren
2. Listendarstellung als Organism
3. Einstellungen als separate Komponente
4. Seite auf ~8.000 Zeichen reduzieren

### 5. Projekt-Bearbeitungsseite (`projects/[id]/edit.vue`) - 23.661 Zeichen
**Aktueller Zustand**: Wahrscheinlich viel Formular-Code

**Zu erstellende Organisms**:
- `EditProjectForm.vue` - Formular für Projektbearbeitung
- `ImageUploadSection.vue` - Bild-Upload mit Vorschau
- `TechnologyManagement.vue` - Technologie-Verwaltung

**Refactoring-Strategie**:
1. Wiederverwendung von `ProjectForm` Organism
2. Anpassung für Edit-Modus
3. Extraktion von Bild-Upload-Logik
4. Seite auf ~6.000 Zeichen reduzieren

## Fehlende Komponenten (Identifikation)

Basierend auf der Analyse der größten Seiten identifiziere ich folgende fehlende Komponenten:

### Organisms benötigt:
1. `TeamMembers.vue` - Für Team-Detailseite
2. `TeamProjects.vue` - Für Team-Detailseite  
3. `ProfileOverview.vue` - Für Profilseite
4. `UserProjects.vue` - Für Profilseite
5. `UserTeams.vue` - Für Profilseite
6. `HackathonInfo.vue` - Für Hackathon-Detailseite
7. `HackathonProjects.vue` - Für Hackathon-Detailseite
8. `NotificationList.vue` - Für Notifications-Seite
9. `NotificationFilters.vue` - Für Notifications-Seite
10. `EditProjectForm.vue` - Für Projekt-Bearbeitungsseite

### Molecules benötigt (optional):
1. `MemberCard.vue` - Für TeamMembers Organism
2. `NotificationItem.vue` - Für NotificationList Organism
3. `ProjectCardCompact.vue` - Für Listen in Profil/Team
4. `TeamCardCompact.vue` - Für Listen in Profil

### Composables benötigt:
1. `useTeamMembers.ts` - Für Team-Mitglieder-Verwaltung
2. `useUserProfile.ts` - Für Profil-Daten
3. `useNotifications.ts` - Für Benachrichtigungs-Logik
4. `useHackathonData.ts` - Für Hackathon-Daten

## Zeitplan und Meilensteine

### Woche 1: Team-Detailseite Refactoring
- **Tag 1-2**: `TeamMembers` Organism erstellen und testen
- **Tag 3**: `TeamProjects` Organism erstellen (falls benötigt)
- **Tag 4**: Integration in Team-Detailseite
- **Tag 5**: Testing und Optimierung

### Woche 2: Profilseite Refactoring
- **Tag 1**: `ProfileOverview` Organism erstellen
- **Tag 2**: `UserProjects` und `UserTeams` Organisms erstellen
- **Tag 3**: Tab-Navigation implementieren
- **Tag 4**: Integration in Profilseite
- **Tag 5**: Testing und Optimierung

### Woche 3: Hackathon-Detailseite Refactoring
- **Tag 1**: `HackathonInfo` Organism erstellen
- **Tag 2**: `HackathonProjects` Organism erstellen
- **Tag 3**: Tab-Navigation implementieren
- **Tag 4**: Integration in Hackathon-Detailseite
- **Tag 5**: Testing und Optimierung

### Woche 4: Notifications und Projekt-Edit Refactoring
- **Tag 1-2**: `NotificationList` und `NotificationFilters` Organisms
- **Tag 3**: `EditProjectForm` Organism (basierend auf ProjectForm)
- **Tag 4**: Integration in entsprechende Seiten
- **Tag 5**: Testing, Bug-Fixing, Optimierung

## Erfolgskriterien

### Quantitative KPIs:
1. **Seitengröße reduzieren**: Jede Seite um mindestens 60% reduzieren
   - Team-Detail: 32k → 12k Zeichen
   - Profil: 27k → 10k Zeichen  
   - Hackathon-Detail: 25k → 12k Zeichen
   - Notifications: 24k → 8k Zeichen
   - Projekt-Edit: 24k → 6k Zeichen

2. **Wiederverwendbarkeit**: 80% der neuen Organisms in ≥2 Kontexten verwendbar
3. **Test Coverage**: > 80% für alle neuen Komponenten
4. **Performance**: Keine signifikante Verschlechterung der Ladezeiten

### Qualitative KPIs:
1. **Verbesserte Wartbarkeit**: Klare Trennung der Verantwortlichkeiten
2. **Bessere Developer Experience**: Einfacheres Onboarding, bessere Autocomplete
3. **Konsistente UI**: Einheitliches Design über alle Seiten
4. **Barrierefreiheit**: Accessibility-Standards für alle neuen Komponenten

## Risiken und Mitigation

### Technische Risiken:
| Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|--------|-------------------|------------|------------|
| Breaking Changes | Mittel | Hoch | Schrittweises Vorgehen, Feature-Flags, umfassende Tests |
| Performance-Einbußen | Niedrig | Mittel | Regelmäßige Performance-Messungen, Lazy-Loading |
| Design-Inkonsistenzen | Niedrig | Niedrig | Design-Tokens, Tailwind-Konfiguration konsistent halten |
| TypeScript-Fehler | Mittel | Mittel | Strikte Typisierung, regelmäßige Type-Checks |

### Organisatorische Risiken:
| Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|--------|-------------------|------------|------------|
| Zeitüberschreitung | Mittel | Hoch | Realistische Schätzungen, Priorisierung, iterative Lieferung |
| Scope Creep | Mittel | Mittel | Klare Requirements, Change-Control-Prozess |
| Unvorhergesehene Komplexität | Hoch | Hoch | Prototyping, technische Spikes vor Implementierung |

## Nächste Schritte

1. **Genehmigung dieses Plans** durch den Benutzer
2. **Erstellung detaillierter Komponenten-Spezifikationen** für jede Organism-Komponente
3. **Start mit Team-Detailseite Refactoring** als höchste Priorität
4. **Regelmäßige Reviews und Anpassungen** basierend auf Feedback

## Empfehlungen

1. **Iterativer Ansatz**: Eine Seite nach der anderen refaktorieren, nicht parallel
2. **Testing-First**: Unit-Tests vor Implementierung schreiben
3. **Dokumentation**: Komponenten-APIs dokumentieren während der Entwicklung
4. **Code-Reviews**: Regelmäßige Reviews zur Qualitätssicherung

---
**Status**: Phase 3 Plan erstellt  
**Empfohlener Start**: Mit Team-Detailseite Refactoring  
**Erwarteter Abschluss**: 4 Wochen bei Vollzeit-Entwicklung