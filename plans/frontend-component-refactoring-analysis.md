# Analyse: Frontend-Komponenten-Refactoring

## Aktuelle Situation

Das Frontend (Nuxt 3 + Vue 3) hat bereits einige wiederverwendbare Komponenten im Verzeichnis `app/components/`:

- `AppHeader.vue`, `AppFooter.vue`, `AppSidebar.vue` (Layout)
- `LanguageSwitcher.vue`, `VoteButtons.vue`, `NotificationContainer.vue` (Funktional)
- `ImprovedStatsCard.vue`, `TeamSelection.vue`, `HackathonEditForm.vue` (Spezifisch)

Allerdings enthalten viele Seitenkomponenten (z.B. `app/pages/projects/[id]/index.vue`, `app/pages/hackathons/[id]/index.vue`) sehr viel Code (bis zu 1000 Zeilen) und mischen verschiedene Themenbereiche:

### Beispiel Projekt-Detailseite (974 Zeilen)
1. **Project Header** – Titel, Besitzer, Datum, Status, Hackathon-Link
2. **Project Image** – Bildanzeige
3. **Description** – Beschreibungstext
4. **Technologies** – Technologie-Tags
5. **Links** – Repository- und Live-Demo-Links
6. **Comments Section** – Kommentare mit Antworten, Bearbeitung, Löschung, Voting
7. **Stats Card** – Statistiken (Upvotes, Downvotes, Score, Kommentare, Views)
8. **Creator Info** – Erstellerinformationen
9. **Actions Card** – Aktionen (Bearbeiten, Löschen, Hackathon anzeigen, Team-Info)
10. **Team Section** – Team-Informationen

## Interpretierte Anforderung

"ensure the frontend has single components of thematical code" könnte bedeuten:

1. **Aufteilung großer Komponenten** in kleinere, thematisch fokussierte Komponenten
2. **Wiederverwendbarkeit** erhöhen durch Extraktion gemeinsamer UI-Elemente
3. **Thematische Organisation** nach Domänen (Projects, Hackathons, Teams, Comments)
4. **Architektur-Pattern** wie Atomic Design (Atoms, Molecules, Organisms) einführen

## Mögliche Ansätze

### Option A: Seitenspezifische Komponenten
- Erstelle `ProjectHeader.vue`, `ProjectStats.vue`, `ProjectComments.vue` etc. im Verzeichnis `app/components/projects/`
- Extrahiere Logik aus der Seite in separate Komponenten
- Behalte bestehende Struktur bei, aber verbessere Modularität

### Option B: Domänenübergreifende Komponenten
- Erstelle generische Komponenten wie `Card.vue`, `TagList.vue`, `CommentThread.vue`
- Verwende diese in mehreren Seiten (Projects, Hackathons, Teams)
- Höhere Wiederverwendbarkeit, aber möglicherweise komplexer

### Option C: Atomic Design-Implementierung
- Organisiere Komponenten in `atoms/`, `molecules/`, `organisms/`, `templates/`
- Refactoring des gesamten Frontends für konsistente Struktur
- Größerer Aufwand, aber langfristig skalierbar

## Fragen zur Klärung

1. **Welcher Ansatz ist bevorzugt?** (A, B, C oder eine andere Variante?)
2. **Sollen nur die größten Seiten refaktorisiert werden** oder das gesamte Frontend?
3. **Gibt es spezifische Themenbereiche**, die priorisiert werden sollen? (z.B. Kommentar-System, Statistiken, Formulare)
4. **Sollen bestehende Komponenten erhalten bleiben** oder teilweise neu geschrieben werden?
5. **Welche Namenskonventionen** sollen verwendet werden? (PascalCase, kebab-case, etc.)
6. **Soll TypeScript-Striktheit** erhöht werden (striktere Interfaces, Typen)?

## Vorschlag für nächste Schritte

Basierend auf der Analyse schlage ich folgenden Plan vor:

1. **Identifiziere thematische Blöcke** in den größten Seitenkomponenten
2. **Erstelle Komponenten für jeden Block** mit klaren Props und Events
3. **Extrahiere Geschäftslogik** in Composable Functions (z.B. `useComments`, `useProjectStats`)
4. **Aktualisiere die Seiten** zur Verwendung der neuen Komponenten
5. **Teste die Funktionalität** nach jedem Refactoring-Schritt

## Beispiel-Komponenten, die erstellt werden könnten

- `ProjectHeader.vue` (Titel, Besitzer, Status)
- `ProjectImage.vue` (Bild mit Platzhalter-Fallback)
- `TechnologyTags.vue` (Liste von Technologie-Tags)
- `ProjectLinks.vue` (GitHub, Live-Demo Links)
- `CommentSection.vue` (Kommentare mit Antworten)
- `ProjectStats.vue` (Statistik-Karten)
- `CreatorInfo.vue` (Erstellerinformationen)
- `ProjectActions.vue` (Bearbeiten, Löschen, Navigation)

Bitte geben Sie Feedback zu diesem Vorschlag und klären Sie die gewünschte Richtung.