# Todo-Liste: Implementierung thematischer Komponenten

## Phase 0: Vorbereitung
- [ ] Sicherstellen, dass alle Änderungen committet sind
- [ ] Verzeichnisstruktur erstellen:
  - `app/components/atoms/`
  - `app/components/molecules/`
  - `app/components/organisms/`
  - `app/components/projects/`
  - `app/components/hackathons/`
  - `app/components/teams/`
  - `app/components/comments/`
  - `app/components/layout/` (existiert bereits)

## Phase 1: Foundation – UI Atoms & Molecules

### 1.1 Card-Komponente (`atoms/Card.vue`)
- [ ] Datei erstellen mit Template, Script, Style
- [ ] Props definieren: `padding`, `rounded`, `shadow`, `background`, `border`
- [ ] Slots implementieren: `default`, `header`, `footer`
- [ ] Tailwind-Klassen dynamisch generieren
- [ ] Testkomponente erstellen
- [ ] In Projekt-Detailseite testweise verwenden

### 1.2 Button-Varianten (`atoms/Button.vue`)
- [ ] Datei erstellen
- [ ] Props: `variant`, `size`, `loading`, `disabled`
- [ ] Slots: `default`, `icon`
- [ ] CSS-Klassen für jede Variante
- [ ] Loading-State mit Spinner
- [ ] Testkomponente
- [ ] Einige Buttons in Projekt-Detailseite ersetzen

### 1.3 Avatar-Komponente (`atoms/Avatar.vue`)
- [ ] Datei erstellen
- [ ] Props: `src`, `alt`, `size`, `fallbackText`
- [ ] Fallback-Logik (Initialen oder generisches Icon)
- [ ] Responsive Größen
- [ ] Testkomponente
- [ ] In Projekt-Detailseite für Besitzer-Avatar verwenden

### 1.4 Tag-Komponente (`atoms/Tag.vue`)
- [ ] Datei erstellen
- [ ] Props: `text`, `color`, `size`, `removable`
- [ ] Events: `remove`
- [ ] Farbvarianten (primary, success, warning, danger, neutral)
- [ ] Testkomponente
- [ ] In Technologie-Tags testweise verwenden

### 1.5 LoadingSpinner (`atoms/LoadingSpinner.vue`)
- [ ] Datei erstellen
- [ ] Props: `size`, `color`
- [ ] SVG-basierter Spinner
- [ ] Testkomponente
- [ ] In Projekt-Detailseite für Loading-State verwenden

## Phase 2: Kommentar-System

### 2.1 Composable: `useComments`
- [ ] Datei `composables/useComments.ts` erstellen
- [ ] Funktionen: `fetchComments`, `postComment`, `editComment`, `deleteComment`, `voteComment`
- [ ] Zustand: `comments`, `loading`, `error`
- [ ] TypeScript-Interfaces für Comment
- [ ] Integration mit bestehendem Auth-Store
- [ ] Test mit Mock-Daten

### 2.2 CommentItem (`comments/CommentItem.vue`)
- [ ] Datei erstellen
- [ ] Props: `comment`, `editable`, `deletable`
- [ ] Events: `edit`, `delete`, `reply`, `vote`
- [ ] Template mit Avatar, Benutzername, Datum, Inhalt
- [ ] Voting-Buttons (Upvote/Downvote)
- [ ] Bearbeiten/Löschen-Buttons (conditional)
- [ ] Testkomponente

### 2.3 CommentForm (`comments/CommentForm.vue`)
- [ ] Datei erstellen
- [ ] Props: `placeholder`, `loading`, `autoFocus`
- [ ] Events: `submit`
- [ ] Slots: `actions`
- [ ] Textarea mit Auto-Resize
- [ ] Submit- und Cancel-Buttons
- [ ] Validierung (nicht leer)
- [ ] Testkomponente

### 2.4 ReplyThread (`comments/ReplyThread.vue`)
- [ ] Datei erstellen
- [ ] Props: `replies`, `parentId`
- [ ] Events: `addReply`, `editReply`, `deleteReply`
- [ ] Liste von CommentItem für Antworten
- [ ] Einrückung/Visualisierung als Thread
- [ ] Testkomponente

### 2.5 CommentSection (`organisms/CommentSection.vue`)
- [ ] Datei erstellen
- [ ] Props: `comments`, `projectId`, `loading`
- [ ] Events: `commentAdded`, `commentUpdated`, `commentDeleted`
- [ ] Verwendet: CommentForm, CommentItem, ReplyThread
- [ ] Integriert `useComments` Composable
- [ ] Loading- und Error-States
- [ ] Testkomponente

## Phase 3: Projekt-Domain-Komponenten

### 3.1 ProjectHeader (`projects/ProjectHeader.vue`)
- [ ] Datei erstellen
- [ ] Props: `project` (Object)
- [ ] Enthält: Titel, Besitzer-Avatar (Avatar-Komponente), Datum, Status-Tag (Tag-Komponente), Hackathon-Link
- [ ] Responsive Layout
- [ ] Testkomponente

### 3.2 ProjectImage (`projects/ProjectImage.vue`)
- [ ] Datei erstellen
- [ ] Props: `src`, `alt`, `title`, `fallbackType`
- [ ] Logik: Platzhalter-Generierung (nutzt `generateProjectPlaceholder` aus utils)
- [ ] Lazy-Loading mit Intersection Observer
- [ ] Testkomponente

### 3.3 TechnologyTags (`projects/TechnologyTags.vue`)
- [ ] Datei erstellen
- [ ] Props: `technologies` (Array oder String)
- [ ] Logik: Parsen von komma-separierten Strings
- [ ] Rendert Liste von Tag-Komponenten
- [ ] Links zu Filter-Seite
- [ ] Testkomponente

### 3.4 ProjectLinks (`projects/ProjectLinks.vue`)
- [ ] Datei erstellen
- [ ] Props: `repositoryUrl`, `liveUrl`
- [ ] Icons für GitHub und Live-Demo
- [ ] Externe Links mit Target `_blank`
- [ ] Fallback: "No links provided"
- [ ] Testkomponente

### 3.5 ProjectStats (`projects/ProjectStats.vue`)
- [ ] Datei erstellen
- [ ] Props: `upvotes`, `downvotes`, `score`, `comments`, `views`
- [ ] Verwendet Card-Komponente
- [ ] Grid-Layout für Statistik-Karten
- [ ] Tooltips oder Erklärungen
- [ ] Testkomponente

### 3.6 CreatorInfo (`projects/CreatorInfo.vue`)
- [ ] Datei erstellen
- [ ] Props: `creator`, `team` (optional)
- [ ] Avatar-Komponente für Creator
- [ ] Name und Rolle anzeigen
- [ ] Team-Info falls vorhanden
- [ ] Link zum Profil
- [ ] Testkomponente

### 3.7 ProjectActions (`projects/ProjectActions.vue`)
- [ ] Datei erstellen
- [ ] Props: `project`, `canEdit`, `canDelete`
- [ ] Events: `edit`, `delete`, `viewHackathon`, `viewTeam`
- [ ] Button-Komponenten für Aktionen
- [ ] Conditional Rendering basierend auf Berechtigungen
- [ ] Bestätigungs-Dialog für Löschen
- [ ] Testkomponente

## Phase 4: Integration in Projekt-Detailseite

### 4.1 Vorbereitung
- [ ] Backup der aktuellen `app/pages/projects/[id]/index.vue`
- [ ] Neue Komponenten importieren

### 4.2 Schrittweise Ersetzung
- [ ] Projekt-Header ersetzen (Zeilen 28-86)
- [ ] Bild-Bereich ersetzen (Zeilen 92-95)
- [ ] Technologie-Tags ersetzen (Zeilen 105-116)
- [ ] Links-Bereich ersetzen (Zeilen 118-159)
- [ ] Statistiken ersetzen (Zeilen 393-418)
- [ ] Ersteller-Info ersetzen (Zeilen 420-446)
- [ ] Aktionen ersetzen (Zeilen 448-526)
- [ ] Kommentar-Bereich ersetzen (Zeilen 161-387)

### 4.3 State Management anpassen
- [ ] Props aus `project`-Object extrahieren
- [ ] Event-Handler für Komponenten-Events implementieren
- [ ] Logik in Composable Functions verschieben
- [ ] TypeScript-Typen aktualisieren

### 4.4 Testing nach jedem Schritt
- [ ] Manuell testen: Seite laden, Daten anzeigen
- [ ] Interaktionen testen: Kommentar posten, Voting, Bearbeiten
- [ ] Responsive Design prüfen
- [ ] Browser-Konsolen auf Fehler prüfen

## Phase 5: Hackathon- und Team-Domain (optional)

### 5.1 Hackathon-Komponenten
- [ ] `HackathonHeader` erstellen
- [ ] `HackathonDescription` erstellen
- [ ] `PrizeList` erstellen
- [ ] `RulesSection` erstellen
- [ ] In Hackathon-Detailseite integrieren

### 5.2 Team-Komponenten
- [ ] `TeamCard` erstellen
- [ ] `TeamMemberList` erstellen
- [ ] `TeamInvitation` erstellen
- [ ] In Team-Seiten integrieren

## Phase 6: Testing & Optimierung

### 6.1 Komponententests
- [ ] Vitest-Setup überprüfen
- [ ] Für jede neue Komponente Unit-Tests schreiben
- [ ] Test Coverage messen

### 6.2 Integrationstests
- [ ] Projekt-Detailseite Integrationstest
- [ ] Kommentar-Funktionalität testen
- [ ] Voting-Funktionalität testen

### 6.3 Performance-Optimierung
- [ ] Bundle-Größe analysieren
- [ ] Lazy-Loading für nicht-kritische Komponenten
- [ ] Memoization von teuren Berechnungen (computed)

## Abschluss

- [ ] Dokumentation aktualisieren (README, Komponenten-Docs)
- [ ] Code-Review durchführen (falls im Team)
- [ ] Pull Request erstellen und mergen
- [ ] Deployment testen

## Priorisierung

**High Priority (muss zuerst):**
1. Card-Komponente (Grundlage für viele andere)
2. CommentSection (komplexester Block)
3. ProjectHeader (sichtbarster Teil)

**Medium Priority:**
4. Button, Avatar, Tag (UI-Konsistenz)
5. ProjectStats, TechnologyTags, ProjectLinks
6. CreatorInfo, ProjectActions

**Low Priority (optional):**
7. Hackathon- und Team-Komponenten
8. Erweiterte Optimierungen

## Hinweise

- Jede Komponente sollte eigene TypeScript-Interfaces haben
- Internationalisierung (i18n) berücksichtigen
- Dark Mode unterstützen (Tailwind Dark-Klassen)
- Accessibility (ARIA-Attribute) implementieren
- Responsive Design testen (Mobile, Tablet, Desktop)