# Bewertung bestehender Komponenten

## Komponenten im `app/components/` Verzeichnis

| Komponente | Größe (Zeichen) | Beschreibung | Wiederverwendbarkeit | Verbesserungspotenzial |
|------------|-----------------|--------------|----------------------|------------------------|
| `AppHeader.vue` | 20.436 | Hauptnavigation mit Logo, Menü, Theme-Toggle, Sprache, Benutzermenü | Hoch (wird auf allen Seiten verwendet) | Gering, bereits gut modularisiert |
| `AppFooter.vue` | 15.316 | Footer mit Links, Copyright | Hoch (wird auf allen Seiten verwendet) | Gering |
| `AppSidebar.vue` | 9.509 | Sidebar-Navigation für mobile/desktop | Hoch | Gering |
| `HackathonEditForm.vue` | 17.242 | Formular zum Bearbeiten/Erstellen von Hackathons | Mittel (nur auf Hackathon-Edit-Seite) | Könnte in kleinere Formularkomponenten aufgeteilt werden |
| `ImprovedStatsCard.vue` | 3.991 | Generische Statistik-Karte mit Icon, Wert, Label, Link | Hoch (kann überall verwendet werden) | Wird aktuell nicht genutzt; könnte in Projekt-Detailseite integriert werden |
| `LanguageSwitcher.vue` | 3.996 | Sprachumschalter mit Flaggen | Hoch | Gering |
| `MobileBottomNav.vue` | 8.973 | Mobile Bottom Navigation | Hoch | Gering |
| `NotificationContainer.vue` | 6.027 | Container für Benachrichtigungen | Hoch | Gering |
| `NotificationSettings.vue` | 20.210 | Einstellungen für Benachrichtigungen | Mittel (nur auf Profilseite) | Könnte in kleinere Einstellungskomponenten aufgeteilt werden |
| `TeamSelection.vue` | 8.090 | Team-Auswahl-Dropdown | Mittel (wird in Formularen verwendet) | Gering |
| `VoteButtons.vue` | 6.484 | Upvote/Downvote-Buttons mit Zählern | Hoch (wird in Projekten und Kommentaren verwendet) | Gering |

## Fehlende Komponenten (identifiziert aus großen Seiten)

### Projekt-Domain
1. **ProjectHeader** – Titel, Besitzer, Datum, Status, Hackathon-Link
2. **ProjectImage** – Bild mit Platzhalter-Fallback
3. **ProjectDescription** – Beschreibungstext mit Formatierung
4. **TechnologyTags** – Liste von Technologie-Tags mit Links
5. **ProjectLinks** – Externe Links (GitHub, Live-Demo)
6. **CommentSection** – Kommentare mit Antworten, Bearbeitung, Löschung, Voting
7. **ProjectStats** – Statistik-Karten (Upvotes, Downvotes, Score, Kommentare, Views)
8. **CreatorInfo** – Erstellerinformationen mit Avatar
9. **ProjectActions** – Aktionen (Bearbeiten, Löschen, Hackathon anzeigen, Team-Info)
10. **TeamInfo** – Team-Informationen (falls Team-Projekt)

### Hackathon-Domain
1. **HackathonHeader** – Name, Datum, Ort, Bild/Gradient
2. **HackathonDescription** – Beschreibung
3. **PrizeList** – Liste von Preisen
4. **RulesSection** – Regeln und Richtlinien
5. **ParticipantList** – Teilnehmerliste
6. **ProjectGallery** – Galerie der Projekte im Hackathon

### Gemeinsame UI-Elemente
1. **Card** – Generische Karte mit Padding, Hintergrund, Shadow
2. **Tag** – Tag/Komponente für Technologien, Status etc.
3. **Avatar** – Benutzeravatar mit Fallback
4. **Button** – Konsistente Button-Varianten (primary, secondary, danger)
5. **LoadingSpinner** – Ladeanimation
6. **EmptyState** – Leerzustand mit Icon und Text

## Bewertung der Code-Qualität

### Stärken
- TypeScript wird verwendet (gute Typisierung)
- Composition API (`<script setup>`) wird konsistent eingesetzt
- Tailwind CSS für Styling (konsistentes Design)
- Internationalisierung (i18n) integriert
- Stores für State-Management (Pinia)

### Schwächen
- Große Seitenkomponenten mit gemischten Verantwortlichkeiten
- Begrenzte Wiederverwendung von UI-Logik (z.B. Kommentar-Logik ist in Seite eingebettet)
- Keine klare Komponenten-Hierarchie (Atomic Design o.ä.)
- Einige Komponenten könnten besser getestet sein

## Empfehlungen

1. **Priorisiere die Extraktion der Kommentar-Sektion** – Diese ist komplex und wird wahrscheinlich auch in anderen Kontexten wiederverwendet (z.B. Hackathon-Diskussionen).
2. **Erstelle eine `Card`-Komponente** – Viele Bereiche verwenden ähnliche Karten-Stile (weißer Hintergrund, Rundung, Shadow).
3. **Extrahiere Projekt-spezifische Komponenten** in `app/components/projects/` Verzeichnis.
4. **Erstelle Composable Functions** für gemeinsame Logik (z.B. `useComments`, `useVoting`, `useProject`).
5. **Aktualisiere die Projekt-Detailseite** schrittweise, um neue Komponenten zu integrieren.

## Nächste Schritte

1. Thematische Bereiche identifizieren und priorisieren
2. Detaillierten Refactoring-Plan erstellen
3. Todo-Liste für Implementierung vorbereiten