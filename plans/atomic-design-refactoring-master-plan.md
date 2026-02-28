# Atomic Design Refactoring - Master Plan

## Übersicht

Dieser Master-Plan beschreibt das vollständige Refactoring aller Frontend-Seiten gemäß Atomic Design-Prinzipien. Basierend auf der Analyse von 19 Seiten und 40+ Komponenten wird ein schrittweiser, inkrementeller Ansatz verfolgt.

## Ziele

1. **Alle Seiten** in kleinere, thematisch fokussierte Komponenten aufteilen
2. **Atomic Design-Struktur** implementieren (Atoms, Molecules, Organisms, Templates)
3. **Wiederverwendbarkeit** maximieren durch extrahierte Komponenten
4. **Wartbarkeit** verbessern durch reduzierte Komplexität pro Datei
5. **Konsistente UI** durch standardisierte Design-Komponenten

## Aktueller Status

### Seiten-Analyse (19 Seiten)
- **Sehr große Seiten** (> 30k Zeichen): 3 Seiten (create.vue, profile.vue, notifications.vue)
- **Große Seiten** (15-30k Zeichen): 4 Seiten (Projekt-, Hackathon-, Team-Detail, my-votes)
- **Mittlere Seiten** (5-15k Zeichen): 7 Seiten
- **Kleine Seiten** (< 5k Zeichen): 5 Seiten

### Komponenten-Analyse (40+ Komponenten)
- **Atoms existieren**: Avatar, Card, Tag
- **Molecules fehlen**: FormField, SearchBar, Pagination, etc.
- **Organisms fehlen**: CommentSection, ProfileHeader, etc.
- **Domänenkomponenten existieren**: projects/, hackathons/, teams/, users/, invitations/, home/

## Phasen-Plan

### Phase 0: Vorbereitung (Woche 0)
- [ ] Git Branch erstellen: `feat/atomic-design-refactoring`
- [ ] Aktuellen Code committen
- [ ] Test-Suite ausführen (Baseline)
- [ ] Performance-Baseline messen (Bundle Size, Ladezeiten)

### Phase 1: Foundation (Woche 1-2)
**Ziel**: Atomic Design-Struktur aufbauen und Basis-Komponenten erstellen

#### Woche 1: Atoms
- [ ] `Button.vue` Atom erstellen (Grundlage für alle Interaktionen)
- [ ] `Input.vue` Atom erstellen (Formulare)
- [ ] `LoadingSpinner.vue` Atom erstellen (Ladezustände)
- [ ] `Icon.vue` Atom erstellen (optional, für Konsistenz)
- [ ] Unit-Tests für alle Atoms
- [ ] Dokumentation (Props, Events, Usage)

#### Woche 2: Molecules Verzeichnis
- [ ] `molecules/` Verzeichnis erstellen
- [ ] `FormField.vue` Molecule (Label + Input + Error)
- [ ] `SearchBar.vue` Molecule (Input + Icon + Clear)
- [ ] `Pagination.vue` Molecule (Seitennavigation)
- [ ] `FilterGroup.vue` Molecule (Filter-UI)
- [ ] Barrel-Exports (`index.ts`)

### Phase 2: Kritische Seiten Refactoring (Woche 3-5)
**Ziel**: Die komplexesten Seiten zuerst refaktorieren

#### Woche 3: Projekt-Detailseite (`projects/[id]/index.vue`)
- [ ] `organisms/comments/` Verzeichnis erstellen
- [ ] `CommentItem.vue`, `CommentForm.vue`, `CommentSection.vue`
- [ ] `useComments` Composable
- [ ] `ProjectImage.vue` und `ProjectDescription.vue` Molecules
- [ ] Integration in Projekt-Detailseite
- [ ] Testing (Unit + Integration)

#### Woche 4: Profilseite (`profile.vue`) - 37.995 Zeichen
- [ ] `organisms/ProfileHeader.vue` erstellen
- [ ] `organisms/UserSettingsForm.vue` erstellen  
- [ ] `molecules/ProfileSection.vue` erstellen
- [ ] Aufteilung in: Übersicht, Einstellungen, Projekte, Teams
- [ ] Integration und Testing

#### Woche 5: Erstellungsseite (`create.vue`) - 36.080 Zeichen
- [ ] `organisms/ProjectForm.vue` erstellen
- [ ] `organisms/HackathonForm.vue` erstellen
- [ ] `molecules/FormWizard.vue` erstellen (Tabs: Project/Hackathon)
- [ ] Formular-Validierung und Submission
- [ ] Integration und Testing

### Phase 3: Domänen-Seiten Refactoring (Woche 6-8)
**Ziel**: Alle domänenspezifischen Seiten vereinheitlichen

#### Woche 6: Hackathon-Seiten
- [ ] `hackathons/[id]/index.vue` vervollständigen
  - `HackathonDescription.vue` Molecule
  - `ParticipantList.vue` Organism
  - `HackathonActions.vue` verbessern
- [ ] `hackathons/index.vue` (Liste) refaktorieren
  - `HackathonListCard.vue` verwenden
  - Filter- und Sortier-Komponenten

#### Woche 7: Team-Seiten
- [ ] `teams/[id]/index.vue` refaktorieren
  - `TeamHeader.vue` Organism
  - `TeamMembers.vue` Organism (Mitglieder-Verwaltung)
  - `TeamProjects.vue` Molecule
- [ ] `teams/index.vue` (Liste) refaktorieren
  - `TeamListCard.vue` verwenden

#### Woche 8: Listen-Seiten vereinheitlichen
- [ ] `projects/index.vue` refaktorieren
  - Einheitliche Projekt-Karten
  - Gemeinsame Filter-Komponenten
- [ ] `users/index.vue` refaktorieren
  - `UserCard.vue` verwenden
- [ ] Gemeinsame `ListLayout` Template erstellen

### Phase 4: Authentifizierung & Einstellungen (Woche 9-10)
**Ziel**: Restliche Seiten refaktorieren

#### Woche 9: Authentifizierungsseiten
- [ ] `login.vue` und `register.vue` refaktorieren
  - `AuthForm.vue` Organism
  - `SocialLoginButtons.vue` Molecule
- [ ] `forgot-password.vue` und `reset-password.vue`
  - `PasswordResetFlow.vue` Organism
- [ ] `verify-email.vue` vereinfachen

#### Woche 10: Einstellungs- und Verwaltungsseiten
- [ ] `notifications.vue` refaktorieren
  - `NotificationPreferences.vue` Organism
  - `NotificationList.vue` Organism
- [ ] `my-projects.vue` und `my-votes.vue`
  - Gemeinsame `UserContentList.vue` Komponente
- [ ] `about.vue` (bereits einfach, optional)

### Phase 5: Testing & Optimierung (Woche 11-12)
**Ziel**: Qualität sicherstellen und optimieren

#### Woche 11: Testing
- [ ] Unit-Tests für alle neuen Komponenten
- [ ] Integrationstests für kritische Seiten
- [ ] E2E-Tests für Haupt-Workflows
- [ ] Test Coverage auf > 80% bringen

#### Woche 12: Optimierung & Abschluss
- [ ] Performance-Analyse (Bundle Size, Ladezeiten)
- [ ] Lazy-Loading für nicht-kritische Komponenten
- [ ] Code-Splitting optimieren
- [ ] Dokumentation vervollständigen
- [ ] Code-Review und Merge-Vorbereitung

## Komponenten-Hierarchie (Final)

### Atoms (Grundlegende UI-Elemente)
```
atoms/
├── Avatar.vue      (existiert)
├── Button.vue      (neu)
├── Card.vue        (existiert)
├── Tag.vue         (existiert)
├── Input.vue       (neu)
├── Textarea.vue    (neu)
├── Select.vue      (neu)
├── Checkbox.vue    (neu)
├── Radio.vue       (neu)
├── LoadingSpinner.vue (neu)
└── Icon.vue        (neu, optional)
```

### Molecules (Einfache Kombinationen)
```
molecules/
├── FormField.vue           (Label + Input + Error)
├── FormSection.vue         (Gruppe von FormFields)
├── SearchBar.vue           (Input + Search Icon + Clear)
├── FilterGroup.vue         (Checkbox/Radio-Gruppe)
├── Pagination.vue          (Seitennavigation)
├── SocialLoginButtons.vue  (Google/GitHub Buttons)
├── FileUpload.vue          (Drag & Drop)
├── DateRangePicker.vue     (Datumswahl)
└── ToggleSwitch.vue        (Ein/Aus-Schalter)
```

### Organisms (Komplexe Komponenten)
```
organisms/
├── comments/
│   ├── CommentItem.vue
│   ├── CommentForm.vue
│   ├── ReplyThread.vue
│   └── CommentSection.vue
├── forms/
│   ├── ProjectForm.vue
│   ├── HackathonForm.vue
│   └── UserSettingsForm.vue
├── ProfileHeader.vue
├── NotificationPreferences.vue
├── TeamManagement.vue
└── AuthForm.vue
```

### Domänenspezifische Komponenten (bleiben erhalten)
```
[domains]/
├── projects/       (existiert, wird als Molecules/Organisms klassifiziert)
├── hackathons/     (existiert, wird als Molecules/Organisms klassifiziert)
├── teams/          (existiert, wird als Molecules/Organisms klassifiziert)
├── users/          (existiert, wird als Molecules/Organisms klassifiziert)
├── invitations/    (existiert)
└── home/           (existiert)
```

## Erfolgskriterien (KPIs)

### Quantitative KPIs
1. **Reduzierung der Seiten-Größe**: Durchschnittlich 60% Reduktion pro Seite
   - Aktuell: 19 Seiten, durchschnittlich 12.500 Zeichen
   - Ziel: Durchschnittlich 5.000 Zeichen pro Seite

2. **Wiederverwendbarkeit**: 80% der neuen Komponenten in ≥2 Kontexten verwendet
   - Aktuell: Begrenzte Wiederverwendung
   - Ziel: Hohe Wiederverwendung durch Atomic Design

3. **Test Coverage**: > 80% für neue Komponenten
   - Aktuell: Unbekannt
   - Ziel: Umfassende Testabdeckung

4. **Performance**: Keine signifikante Verschlechterung
   - Bundle Size: ≤ 10% Erhöhung
   - Ladezeiten: ≤ 5% Erhöhung

### Qualitative KPIs
1. **Wartbarkeit**: Einfacher zu verstehen und zu ändern
2. **Konsistenz**: Einheitliche UI über alle Seiten
3. **Developer Experience**: Bessere Autocomplete und Type-Safety
4. **Onboarding**: Neue Entwickler können schneller beitragen

## Risikomanagement

### Technische Risiken
| Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|--------|-------------------|------------|------------|
| Breaking Changes | Mittel | Hoch | Schrittweises Vorgehen, Feature-Flags, Tests |
| Performance-Einbußen | Niedrig | Mittel | Regelmäßige Performance-Messungen, Optimierung |
| Design-Inkonsistenzen | Niedrig | Niedrig | Design-Tokens, Tailwind-Konfiguration |
| TypeScript-Fehler | Mittel | Mittel | Strikte Typisierung, `strict: true` |

### Organisatorische Risiken
| Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|--------|-------------------|------------|------------|
| Zeitüberschreitung | Hoch | Hoch | Priorisierung, iterative Lieferung, MVP-Ansatz |
| Scope Creep | Mittel | Hoch | Klare Requirements, Change-Control |
| Team-Kapazität | Mittel | Hoch | Realistische Planung, externe Unterstützung |

## Kommunikationsplan

### Interne Kommunikation
- **Wöchentliche Updates**: Fortschritt, Blockaden, nächste Schritte
- **Code-Reviews**: Alle größeren Änderungen
- **Demo-Sessions**: Nach jeder Phase

### Dokumentation
- **Komponenten-Dokumentation**: Props, Events, Usage-Beispiele
- **Architektur-Dokumentation**: Atomic Design-Struktur
- **Migrations-Guide**: Für bestehende Entwickler

## Rollout-Strategie

### Staged Rollout
1. **Phase 1-2** (Foundation + Kritische Seiten): Feature-Branch, intensive Testing
2. **Phase 3** (Domänen-Seiten): Stückweise Integration
3. **Phase 4-5** (Rest + Optimierung): Finale Integration

### Deployment-Strategie
- **Feature-Flags**: Für kritische Änderungen
- **A/B Testing**: Optional für UX-Verbesserungen
- **Rollback-Plan**: Bei kritischen Issues

## Ressourcen-Bedarf

### Entwicklung
- **Frontend-Entwickler**: 1-2 Personen (12 Wochen)
- **QA/Testing**: 0.5 Personen (part-time)
- **Design-Review**: 0.25 Personen (as needed)

### Tooling
- **Testing**: Vitest, Vue Test Utils, Playwright (falls vorhanden)
- **Documentation**: Storybook (optional), MDX
- **CI/CD**: Bestehende Pipeline

## Nächste Schritte

### Unmittelbar (vor Beginn)
1. [ ] Benutzer-Feedback zu diesem Master-Plan einholen
2. [ ] Git Branch erstellen: `feat/atomic-design-refactoring`
3. [ ] Entwicklungsumgebung vorbereiten
4. [ ] Team-Briefing durchführen

### Woche 1 Start
1. [ ] Mit `Button.vue` Atom beginnen
2. [ ] Erste Komponenten in isoliertem Kontext testen
3. [ ] In einfacher Seite integrieren (z.B. About-Seite)

## Anhang

### Referenz-Dokumente
1. `plans/atomic-design-refactoring-prioritization.md` - Priorisierungsliste
2. `plans/atomic-design-structure-definition.md` - Struktur-Definition
3. `plans/component-creation-todo.md` - Komponenten-Erstellung
4. `plans/project-detail-refactoring-plan.md` - Projekt-Detailseite Plan

### Externe Referenzen
- Atomic Design by Brad Frost
- Vue 3 Composition API Best Practices
- Tailwind CSS Design Systems