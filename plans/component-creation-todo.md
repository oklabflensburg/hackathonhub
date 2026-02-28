# Todo: Erstellung fehlender Basis-Komponenten

## Phase 1: Atoms erstellen (Grundlegende UI-Elemente)

### 1.1 Button.vue
- [ ] Verzeichnis `frontend3/app/components/atoms/` überprüfen
- [ ] Datei `Button.vue` erstellen
- [ ] Props definieren: `variant`, `size`, `loading`, `disabled`, `fullWidth`, `type`
- [ ] Slots implementieren: `default`, `icon`
- [ ] Tailwind-Klassen für Varianten definieren
- [ ] Loading-State mit Spinner
- [ ] Accessibility (ARIA) implementieren
- [ ] Unit-Test erstellen
- [ ] In bestehender Seite testen (z.B. Projekt-Detailseite)

### 1.2 Input.vue
- [ ] Datei `Input.vue` erstellen
- [ ] Props definieren: `type`, `modelValue`, `placeholder`, `disabled`, `readonly`, `error`, `success`
- [ ] Events: `update:modelValue`, `focus`, `blur`, `input`, `change`
- [ ] Error/Success-States mit Icons
- [ ] Clear-Button für Suchfelder
- [ ] Unit-Test erstellen

### 1.3 LoadingSpinner.vue
- [ ] Datei `LoadingSpinner.vue` erstellen
- [ ] Props: `size`, `color`, `thickness`
- [ ] SVG-basierter Spinner
- [ ] CSS-Animationen
- [ ] Unit-Test erstellen

### 1.4 Icon.vue (optional)
- [ ] Datei `Icon.vue` erstellen
- [ ] Props: `name`, `size`, `color`
- [ ] SVG-Icons aus Icon-Set laden
- [ ] Fallback für fehlende Icons

## Phase 2: Molecules Verzeichnis und erste Molecules

### 2.1 Verzeichnisstruktur erstellen
- [ ] `frontend3/app/components/molecules/` Verzeichnis erstellen
- [ ] `index.ts` für Barrel-Exports erstellen

### 2.2 FormField.vue
- [ ] Datei `FormField.vue` erstellen
- [ ] Props: `label`, `required`, `error`, `help`, `id`
- [ ] Slots: `default`, `label`, `help`
- [ ] Error-Anzeige mit roter Umrandung und Text
- [ ] Required-Marker (*)
- [ ] Help-Text unter dem Feld
- [ ] Unit-Test erstellen

### 2.3 SearchBar.vue
- [ ] Datei `SearchBar.vue` erstellen
- [ ] Props: `placeholder`, `debounce`, `modelValue`
- [ ] Events: `update:modelValue`, `search`
- [ ] Composition: Input Atom + Search Icon + Clear Button
- [ ] Debounce-Funktionalität
- [ ] Unit-Test erstellen

### 2.4 Pagination.vue
- [ ] Datei `Pagination.vue` erstellen
- [ ] Props: `total`, `perPage`, `currentPage`, `showNumbers`, `showPrevNext`
- [ ] Events: `page-change`
- [ ] Berechnung der Seitenzahlen
- [ ] Responsive Design (mobile: nur Prev/Next)
- [ ] Unit-Test erstellen

## Phase 3: Organisms Verzeichnis und kritische Organisms

### 3.1 Verzeichnisstruktur erstellen
- [ ] `frontend3/app/components/organisms/` Verzeichnis erstellen
- [ ] `index.ts` für Barrel-Exports erstellen

### 3.2 CommentSection Organism (höchste Priorität)
- [ ] Unterverzeichnis `comments/` in `organisms/` erstellen
- [ ] `CommentItem.vue` (Molecule) erstellen
  - Props: `comment`, `editable`, `deletable`, `currentUserId`
  - Events: `edit`, `delete`, `reply`, `vote`
  - Template mit Avatar, Benutzername, Datum, Inhalt
  - Voting-Buttons (Upvote/Downvote)
  - Bearbeiten/Löschen-Buttons (conditional)
- [ ] `CommentForm.vue` (Molecule) erstellen
  - Props: `placeholder`, `loading`, `autoFocus`, `replyTo`
  - Events: `submit`, `cancel`
  - Textarea mit Auto-Resize
  - Submit- und Cancel-Buttons
  - Validierung (nicht leer)
- [ ] `ReplyThread.vue` (Organism) erstellen
  - Props: `replies`, `parentId`, `depth`
  - Events: `addReply`, `editReply`, `deleteReply`
  - Liste von CommentItem für Antworten
  - Einrückung/Visualisierung als Thread
- [ ] `CommentSection.vue` (Organism) erstellen
  - Props: `comments`, `projectId`, `loading`, `currentUserId`
  - Events: `commentAdded`, `commentUpdated`, `commentDeleted`
  - Composition: CommentForm + Liste von CommentItem + ReplyThread
  - Loading- und Error-States
- [ ] Composable `useComments.ts` erstellen
  - Funktionen: `fetchComments`, `postComment`, `editComment`, `deleteComment`, `voteComment`
  - Zustand: `comments`, `loading`, `error`
  - TypeScript-Interfaces für Comment

### 3.3 ProjectForm Organism (für create.vue und edit.vue)
- [ ] Unterverzeichnis `forms/` in `organisms/` erstellen
- [ ] `ProjectForm.vue` erstellen
  - Props: `project` (für Bearbeitung), `loading`, `hackathons` (Liste)
  - Events: `submit`, `cancel`
  - Formular-Felder: Titel, Beschreibung, Technologien, Links, Bild
  - Validierung
  - Integration mit bestehender API

## Phase 4: Integration und Migration

### 4.1 Bestehende Komponenten migrieren
- [ ] `projects/TechnologyTags.vue` als Molecule klassifizieren
- [ ] `projects/ProjectLinks.vue` als Molecule klassifizieren  
- [ ] `projects/ProjectStats.vue` als Molecule klassifizieren
- [ ] `projects/CreatorInfo.vue` als Molecule klassifizieren
- [ ] `projects/ProjectActions.vue` als Molecule klassifizieren
- [ ] `projects/ProjectHeader.vue` als Organism bestätigen

### 4.2 Barrel-Exports aktualisieren
- [ ] `frontend3/app/components/atoms/index.ts` aktualisieren
- [ ] `frontend3/app/components/molecules/index.ts` aktualisieren
- [ ] `frontend3/app/components/organisms/index.ts` aktualisieren
- [ ] Haupt-`index.ts` für einfache Imports aktualisieren

## Phase 5: Testing und Dokumentation

### 5.1 Unit-Tests
- [ ] Test-Setup überprüfen (Vitest + Vue Test Utils)
- [ ] Für jede neue Komponente Unit-Tests schreiben
- [ ] Test Coverage messen und verbessern

### 5.2 Dokumentation
- [ ] Komponenten-Dokumentation in README oder Storybook
- [ ] Props und Events dokumentieren
- [ ] Usage-Beispiele erstellen

### 5.3 Integration
- [ ] Neue Komponenten in bestehenden Seiten testen
- [ ] Performance-Impact messen
- [ ] Browser-Kompatibilität testen

## Zeitplan (geschätzt)

### Woche 1: Atoms und Molecules
- Tag 1-2: Button, Input, LoadingSpinner
- Tag 3-4: FormField, SearchBar, Pagination
- Tag 5: Testing und Integration

### Woche 2: CommentSection Organism
- Tag 1: CommentItem und CommentForm
- Tag 2: ReplyThread und CommentSection
- Tag 3: useComments Composable
- Tag 4: Integration in Projekt-Detailseite
- Tag 5: Testing und Bug-Fixing

### Woche 3: Weitere Organisms und Migration
- Tag 1-2: ProjectForm Organism
- Tag 3: Migration bestehender Komponenten
- Tag 4-5: Testing und Optimierung

## Erfolgskriterien

### Für jede Komponente:
- [ ] TypeScript-Typen korrekt definiert
- [ ] Props und Events funktionieren wie spezifiziert
- [ ] Unit-Tests bestehen
- [ ] Responsive Design getestet (Mobile, Tablet, Desktop)
- [ ] Dark Mode unterstützt
- [ ] Accessibility (Screen Reader) getestet
- [ ] Keine Konsolen-Fehler

### Für das Gesamtsystem:
- [ ] Bundle-Größe nicht signifikant erhöht
- [ ] Ladezeiten gleich oder besser
- [ ] Keine Regressionen in bestehender Funktionalität
- [ ] Konsistente UI über alle Seiten

## Nächste Schritte nach Abschluss

1. **Refactoring der Projekt-Detailseite** mit neuen Komponenten
2. **Refactoring der Profilseite** mit ProfileHeader Organism
3. **Refactoring der Erstellungsseiten** mit ProjectForm Organism
4. **Vereinheitlichung aller Formulare** mit FormField Molecules

## Risiken und Mitigation

| Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|--------|-------------------|------------|------------|
| Inkompatible Props/Events | Mittel | Mittel | TypeScript-Typen, Integrationstests |
| Performance-Einbußen | Niedrig | Niedrig | Bundle-Analyse, Lazy-Loading |
| Design-Inkonsistenzen | Niedrig | Niedrig | Design-Tokens, Tailwind-Konfiguration |
| Zeitüberschreitung | Mittel | Hoch | Priorisierung, iterative Lieferung |

## Start der Implementierung

Die Implementierung kann beginnen, sobald:
1. Dieser Plan vom Benutzer genehmigt wurde
2. Der aktuelle Code committet ist
3. Ein Feature-Branch erstellt wurde

Empfohlener Start: Mit `Button.vue` Atom, da es die Grundlage für viele andere Komponenten ist.