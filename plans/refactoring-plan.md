# Refactoring-Plan: Thematische Komponenten für Frontend

## Ziel
Das Frontend in kleinere, thematisch fokussierte Komponenten aufteilen, um Wartbarkeit, Wiederverwendbarkeit und Lesbarkeit zu verbessern.

## Strategie
**Inkrementelles Refactoring** – Schrittweise Extraktion von Komponenten ohne bestehende Funktionalität zu brechen. Jede Phase wird mit Tests überprüft.

## Phasen

### Phase 0: Vorbereitung
1. **Backup** – Sicherstellen, dass aktueller Code committet ist
2. **Test-Setup** – Sicherstellen, dass bestehende Tests laufen
3. **Komponenten-Verzeichnisstruktur** erstellen:
   ```
   app/components/
   ├── atoms/           # Grundlegende UI-Elemente
   ├── molecules/       # Kombinationen von Atoms
   ├── organisms/       # Komplexe Komponenten
   ├── projects/        # Projekt-spezifische Komponenten
   ├── hackathons/      # Hackathon-spezifische Komponenten
   ├── teams/           # Team-spezifische Komponenten
   ├── comments/        # Kommentar-Komponenten
   └── layout/          # Layout-Komponenten (bereits vorhanden)
   ```

### Phase 1: Foundation – UI Atoms & Molecules
**Ziel:** Grundlegende UI-Komponenten erstellen, die in vielen Bereichen verwendet werden können.

#### 1.1 Card-Komponente (`atoms/Card.vue`)
- Props: `padding`, `rounded`, `shadow`, `background`, `border`
- Slots: `default`, `header`, `footer`
- Verwendung: Ersetzt viele divs mit Tailwind-Klassen

#### 1.2 Button-Varianten (`atoms/Button.vue`)
- Props: `variant` (primary, secondary, danger, ghost), `size`, `loading`, `disabled`
- Slots: `default`, `icon`
- Verwendung: Standardisiert Buttons im gesamten Projekt

#### 1.3 Avatar-Komponente (`atoms/Avatar.vue`)
- Props: `src`, `alt`, `size`, `fallbackText`
- Fallback: Initialen oder generisches Icon
- Verwendung: Überall wo Benutzeravatare angezeigt werden

#### 1.4 Tag-Komponente (`atoms/Tag.vue`)
- Props: `text`, `color`, `size`, `removable`
- Events: `remove`
- Verwendung: Technologie-Tags, Status-Tags, Kategorien

#### 1.5 LoadingSpinner (`atoms/LoadingSpinner.vue`)
- Props: `size`, `color`
- Verwendung: Einheitliche Ladeanimation

### Phase 2: Kommentar-System (Organism)
**Ziel:** Das komplexe Kommentar-System aus der Projekt-Detailseite extrahieren.

#### 2.1 CommentItem (`comments/CommentItem.vue`)
- Props: `comment` (Object), `editable`, `deletable`
- Events: `edit`, `delete`, `reply`, `vote`
- Enthält: Avatar, Benutzername, Datum, Inhalt, Voting-Buttons, Aktionen

#### 2.2 CommentForm (`comments/CommentForm.vue`)
- Props: `placeholder`, `loading`, `autoFocus`
- Events: `submit`
- Slots: `actions`
- Enthält: Textarea, Submit-Button, Cancel-Button

#### 2.3 ReplyThread (`comments/ReplyThread.vue`)
- Props: `replies` (Array), `parentId`
- Events: `addReply`, `editReply`, `deleteReply`
- Enthält: Liste von CommentItem für Antworten

#### 2.4 CommentSection (`organisms/CommentSection.vue`)
- Props: `comments` (Array), `projectId`, `loading`
- Events: `commentAdded`, `commentUpdated`, `commentDeleted`
- Enthält: CommentForm, Liste von CommentItem, ReplyThread
- Logik: Fetch, Post, Edit, Delete von Kommentaren (kann in Composable ausgelagert werden)

#### 2.5 Composable: `useComments`
- Funktionen: `fetchComments`, `postComment`, `editComment`, `deleteComment`, `voteComment`
- Zustand: `comments`, `loading`, `error`
- Wiederverwendbar für Hackathons, Teams, etc.

### Phase 3: Projekt-Domain-Komponenten
**Ziel:** Projekt-spezifische Blöcke extrahieren.

#### 3.1 ProjectHeader (`projects/ProjectHeader.vue`)
- Props: `project` (Object)
- Enthält: Titel, Besitzer-Avatar, Datum, Status-Tag, Hackathon-Link

#### 3.2 ProjectImage (`projects/ProjectImage.vue`)
- Props: `src`, `alt`, `title`, `fallbackType`
- Logik: Platzhalter-Generierung bei fehlendem Bild

#### 3.3 TechnologyTags (`projects/TechnologyTags.vue`)
- Props: `technologies` (Array oder String)
- Logik: Parsen von komma-separierten Strings, Rendern von Tag-Komponenten

#### 3.4 ProjectLinks (`projects/ProjectLinks.vue`)
- Props: `repositoryUrl`, `liveUrl`
- Enthält: GitHub- und Live-Demo-Links mit Icons

#### 3.5 ProjectStats (`projects/ProjectStats.vue`)
- Props: `upvotes`, `downvotes`, `score`, `comments`, `views`
- Verwendet: Card-Komponente, verbesserte Darstellung

#### 3.6 CreatorInfo (`projects/CreatorInfo.vue`)
- Props: `creator` (Object), `team` (Object optional)
- Enthält: Avatar, Name, Rolle, Team-Info

#### 3.7 ProjectActions (`projects/ProjectActions.vue`)
- Props: `project` (Object), `canEdit`, `canDelete`
- Events: `edit`, `delete`, `viewHackathon`, `viewTeam`
- Enthält: Buttons für Aktionen

### Phase 4: Integration in Projekt-Detailseite
**Ziel:** Die extrahierten Komponenten in `app/pages/projects/[id]/index.vue` integrieren.

#### 4.1 Schrittweise Ersetzung
1. Ersetze Projekt-Header durch `ProjectHeader`
2. Ersetze Bild-Bereich durch `ProjectImage`
3. Ersetze Technologie-Tags durch `TechnologyTags`
4. Ersetze Links-Bereich durch `ProjectLinks`
5. Ersetze Statistiken durch `ProjectStats`
6. Ersetze Ersteller-Info durch `CreatorInfo`
7. Ersetze Aktionen durch `ProjectActions`
8. Ersetze Kommentar-Bereich durch `CommentSection`

#### 4.2 State Management anpassen
- Props an neue Komponenten übergeben
- Events von Komponenten behandeln
- Logik in Composable Functions verschieben

### Phase 5: Hackathon- und Team-Domain
**Ziel:** Ähnliches Refactoring für Hackathon- und Team-Seiten.

#### 5.1 Hackathon-Komponenten (`hackathons/`)
- `HackathonHeader`, `HackathonDescription`, `PrizeList`, `RulesSection`, etc.

#### 5.2 Team-Komponenten (`teams/`)
- `TeamCard`, `TeamMemberList`, `TeamInvitation`, etc.

### Phase 6: Testing & Optimierung
**Ziel:** Sicherstellen, dass alles funktioniert und optimieren.

#### 6.1 Komponententests
- Vitest + Vue Test Utils für jede neue Komponente
- Testen von Props, Events, Slots

#### 6.2 Integrationstests
- Testen der Projekt-Detailseite mit neuen Komponenten
- E2E-Tests mit Playwright (falls vorhanden)

#### 6.3 Performance-Optimierung
- Lazy-Loading von Komponenten wo möglich
- Memoization von teuren Berechnungen

## Zeitplan (relativ)

- **Phase 0:** 0.5 Tage
- **Phase 1:** 1-2 Tage
- **Phase 2:** 2-3 Tage
- **Phase 3:** 1-2 Tage
- **Phase 4:** 1-2 Tage
- **Phase 5:** 2-3 Tage (optional, je nach Priorität)
- **Phase 6:** 1-2 Tage

**Gesamt:** ~8-14 Tage für vollständiges Refactoring

## Erfolgskriterien

1. **Reduzierte Zeilenanzahl** in Seitenkomponenten (mindestens 50% Reduktion)
2. **Erhöhte Wiederverwendbarkeit** (Komponenten werden in mehr als einem Kontext verwendet)
3. **Verbesserte Testbarkeit** (jede Komponente kann isoliert getestet werden)
4. **Konsistente UI** (durch standardisierte Atoms/Molecules)
5. **Keine Regressionen** (alle bestehenden Funktionen bleiben erhalten)

## Risiken & Mitigation

| Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|--------|-------------------|------------|------------|
| Brechen bestehender Funktionalität | Mittel | Hoch | Schrittweises Vorgehen, Tests nach jedem Schritt, Feature-Branches |
| Performance-Einbußen durch viele Komponenten | Niedrig | Niedrig | Performance-Monitoring, Lazy-Loading, Memoization |
| Inkonsistente Props/Events-Schnittstellen | Mittel | Mittel | Dokumentation, TypeScript-Typen, Review-Prozess |
| Zeitüberschreitung | Hoch | Mittel | Priorisierung auf kritische Bereiche, iterative Lieferung |

## Nächste Schritte

1. **Todo-Liste für Implementierung** erstellen
2. **Benutzer-Feedback** zum Plan einholen
3. **Mit der Implementierung von Phase 1 beginnen**