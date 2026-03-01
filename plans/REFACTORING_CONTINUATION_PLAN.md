# Atomic Design Refactoring - Fortsetzungsplan

## 📋 Aktueller Status (Stand: 1. März 2026)

### ✅ Abgeschlossene Phasen
1. **Phase 1: Atoms** - Vollständig abgeschlossen
   - Alle 6 Atom-Komponenten erstellt: Button, Input, LoadingSpinner, Avatar, Card, Tag
   - TypeScript-Typisierung, Dark Mode, Accessibility implementiert

2. **Phase 2: Molecules** - Vollständig abgeschlossen  
   - 4 Kern-Molecules erstellt: FormField, SearchBar, Pagination, Alert
   - Viele zusätzliche Molecules existieren bereits

3. **Phase 3: Organisms** - Teilweise abgeschlossen
   - CommentSection Organism komplett (CommentItem, CommentForm, ReplyThread)
   - ProfileHeader und UserSettingsForm Organisms
   - ProjectDetailMainContent und ProjectDetailSidebar
   - ProjectListOrganism und TeamDetailHeader

### 🔄 In Bearbeitung
- **Profilseite** (`profile.vue`) - Wird aktuell refaktorisiert
- **Projekt-Detailseite** (`projects/[id]/index.vue`) - Bereits teilweise refaktorisiert

## 🎯 Nächste Prioritäten (basierend auf Master-Plan)

### 1. Hochprioritäre Seiten (Woche 5-6)
**create.vue (36.080 Zeichen)** - Erstellungsseite für Projekte/Hackathons
- **Status**: Noch nicht refaktorisiert
- **Komplexität**: Sehr hoch (größte Seite nach Profilseite)
- **Geplante Organisms**: 
  - `ProjectForm.vue` (für Projekt-Erstellung)
  - `HackathonForm.vue` (für Hackathon-Erstellung)
  - `FormWizard.vue` (Tabs-Navigation)

### 2. Kritische Seiten (Woche 6-7)
**notifications.vue (23.719 Zeichen)** - Benachrichtigungsseite
- **Status**: Noch nicht refaktorisiert
- **Geplante Organisms**:
  - `NotificationPreferences.vue`
  - `NotificationList.vue`

**my-projects.vue (18.236 Zeichen)** und **my-votes.vue (19.963 Zeichen)**
- **Status**: Noch nicht refaktorisiert
- **Geplante Komponenten**: Gemeinsame `UserContentList.vue`

### 3. Domänen-Seiten (Woche 7-8)
**Hackathon-Seiten**:
- `hackathons/[id]/index.vue` (25.544 Zeichen) - Teilweise refaktorisiert
- `hackathons/index.vue` (13.296 Zeichen) - Liste

**Team-Seiten**:
- `teams/[id]/index.vue` (32.288 Zeichen) - Detailseite
- `teams/index.vue` (12.044 Zeichen) - Liste

**Listen-Seiten**:
- `projects/index.vue` (13.698 Zeichen) - Projekt-Liste
- `users/index.vue` (10.426 Zeichen) - Benutzer-Liste

## 🏗️ Detaillierter Aktionsplan

### Phase A: Fertigstellung laufender Arbeiten (1-2 Tage)
1. **Profilseite komplettieren** (`profile.vue`)
   - UserSettingsForm Organism finalisieren
   - ProfileHeader Organism integrieren
   - FormField Molecules für alle Eingabefelder verwenden
   - Testing und Validierung

2. **Projekt-Detailseite optimieren** (`projects/[id]/index.vue`)
   - Fehlende Atomic Design-Komponenten identifizieren
   - Konsistente Props- und Event-Schnittstellen
   - Performance-Optimierung

### Phase B: create.vue Refactoring (3-4 Tage)
1. **Analyse der aktuellen create.vue Struktur**
   - Identifizieren von wiederverwendbaren Teilen
   - Aufteilung in logische Abschnitte

2. **Form-Organisms erstellen**
   - `organisms/forms/ProjectForm.vue`
   - `organisms/forms/HackathonForm.vue`
   - `organisms/forms/FormWizard.vue`

3. **Integration in create.vue**
   - Schrittweise Migration
   - Formular-Validierung beibehalten
   - API-Integration testen

### Phase C: Notifications und User Content (2-3 Tage)
1. **notifications.vue refaktorieren**
   - `NotificationPreferences.vue` Organism
   - `NotificationList.vue` Organism
   - Filter- und Sortier-Funktionalität

2. **my-projects.vue und my-votes.vue vereinheitlichen**
   - Gemeinsame `UserContentList.vue` Komponente
   - Konsistente Filter- und Sortier-Optionen
   - Responsive Design optimieren

### Phase D: Domänen-Seiten (3-4 Tage)
1. **Hackathon-Seiten komplettieren**
   - `HackathonDescription.vue` Molecule verbessern
   - `ParticipantList.vue` Organism optimieren
   - `HackathonActions.vue` mit Atomic Design-Komponenten

2. **Team-Seiten refaktorieren**
   - `TeamHeader.vue` Organism finalisieren
   - `TeamMembers.vue` Organism (Mitglieder-Verwaltung)
   - `TeamProjects.vue` Molecule

3. **Listen-Seiten vereinheitlichen**
   - Gemeinsame `ListLayout` Template
   - Konsistente Filter-Komponenten
   - Pagination-Integration

## 🔧 Fehlende Komponenten (zu erstellen)

### Organisms
1. **Modal.vue** - Modal-Dialog mit Overlay und Fokus-Management
2. **CardGrid.vue** - Raster von Karten für Projekt-Listen
3. **Sidebar.vue** - Seitenleiste mit Navigation und Filter-Optionen
4. **AuthForm.vue** - Für login.vue und register.vue
5. **PasswordResetFlow.vue** - Für forgot-password.vue und reset-password.vue

### Molecules
1. **FilterGroup.vue** - Erweiterte Filter-UI (laut Master-Plan)
2. **SocialLoginButtons.vue** - Für Authentifizierungsseiten
3. **UserCard.vue** - Verbesserte Version für Benutzer-Listen

## 📊 Erfolgskriterien für jede Phase

### Für jede refaktorisierte Seite:
- [ ] TypeScript-Typisierung komplett
- [ ] Atomic Design-Komponenten verwendet
- [ ] Keine Konsolen-Fehler
- [ ] Responsive Design getestet
- [ ] Dark Mode unterstützt
- [ ] Accessibility (ARIA) implementiert
- [ ] Performance gleich oder besser
- [ ] Bundle-Größe nicht signifikant erhöht

### Für das Gesamtsystem:
- [ ] Konsistente UI über alle Seiten
- [ ] Wiederverwendbare Komponenten-Bibliothek
- [ ] Gute Developer Experience (Importe, Dokumentation)
- [ ] Test Coverage > 80% für neue Komponenten

## 🚀 Empfohlene Vorgehensweise

### Iterativer Ansatz
1. **Feature-Branch erstellen**: `feat/atomic-design-phase3`
2. **Seite für Seite refaktorieren**: Nicht alle Seiten gleichzeitig
3. **Testing nach jeder Seite**: Unit-Tests und Integrationstests
4. **Code-Review einholen**: Vor dem Merge in den Hauptbranch

### Technische Entscheidungen
1. **Composition API**: Weiterhin `<script setup>` verwenden
2. **TypeScript**: Strikte Typisierung beibehalten
3. **Tailwind CSS**: Utility-First Ansatz fortsetzen
4. **Auto-Imports**: Nuxt 3 Auto-Imports nutzen

## 📈 Risikomanagement

| Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|--------|-------------------|------------|------------|
| Zeitüberschreitung | Mittel | Hoch | Priorisierung, iterative Lieferung |
| Inkompatible Props | Niedrig | Mittel | TypeScript-Typen, Integrationstests |
| Design-Inkonsistenzen | Niedrig | Niedrig | Design-Tokens, Tailwind-Konfiguration |
| Performance-Regression | Niedrig | Mittel | Bundle-Analyse, Lazy-Loading |

## 🎉 Erwartete Vorteile

1. **Reduzierte Komplexität**: Kleinere, fokussierte Komponenten
2. **Bessere Wartbarkeit**: Einfacher zu verstehen und zu ändern
3. **Konsistente UI**: Einheitliches Design über alle Seiten
4. **Wiederverwendbarkeit**: Komponenten können in anderen Projekten verwendet werden
5. **Bessere Testbarkeit**: Isolierte Komponenten sind einfacher zu testen

## 🔄 Nächste Schritte

1. **Benutzer-Feedback** zu diesem Plan einholen
2. **Prioritäten bestätigen** (create.vue zuerst?)
3. **In Code-Mode wechseln** für die Implementierung
4. **Iterativ vorgehen**: Eine Seite nach der anderen

---
**Erstellt am**: 1. März 2026  
**Basierend auf**: Atomic Design Refactoring Master Plan  
**Aktueller Branch**: Unbekannt (Feature-Branch empfohlen)  
**Geplante Dauer**: 2-3 Wochen für alle verbleibenden Seiten