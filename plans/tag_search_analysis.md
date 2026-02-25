# Analyse der Tag-Suche-Anforderung

## Aktueller Stand

### Backend
- Projektmodell hat Feld `technologies` (String, kommagetrennte Liste)
- Keine dedizierte Tag-Tabelle
- API-Route `GET /projects` unterstützt nur `user`-Filter, keine Technologie-/Tag-Filterung
- Service- und Repository-Schicht haben keine Methoden für Technologie-Filterung

### Frontend
- Projekt-Detailseite (`/projects/[id]`) zeigt Technologien als nicht-klickbare Tags an (Abschnitt "Technologies")
- Projekte-Listenseite (`/projects`) hat clientseitige Tag-Filterung (`selectedTags`), die auf dem Feld `tech` basiert (wahrscheinlich `technologies`)
- Tag-Filterung ist rein clientseitig, keine URL-Parameter

## Anforderung laut Benutzer
"Implement a search for tag under http://localhost:3001/projects/1 but in backend and frontend; the tags should be clickable and trigger a backend search for projects with same tag and show result in frontend change url"

Interpretation:
1. Auf der Projekt-Detailseite (`/projects/1`) sollen Tags (Technologien) klickbar sein
2. Beim Klick soll eine Backend-Suche nach Projekten mit demselben Tag ausgelöst werden
3. Die Ergebnisse sollen im Frontend angezeigt werden (wahrscheinlich auf der Projekte-Listenseite)
4. Die URL soll sich ändern (z.B. `/projects?technology=python`)

## Offene Fragen zur Klärung

1. **Tag vs. Technology**: Sollen wir die bestehenden "Technologies" als Tags verwenden oder ein separates Tag-System einführen?
2. **Suchlogik**: Soll die Suche exakte Übereinstimmung oder Teilübereinstimmung sein? (Technologies sind kommagetrennt, z.B. "python,javascript,react")
3. **Ergebnisanzeige**: Sollen die Ergebnisse auf einer separaten Seite oder auf derselben Projekt-Detailseite angezeigt werden?
4. **URL-Struktur**: Welche URL-Parameter sollen verwendet werden? (`/projects?tag=python`, `/projects?technology=python`, `/search?q=python`)
5. **Filterkombination**: Sollen mehrere Tags kombiniert werden können (AND/OR)?
6. **Backend-API**: Soll die bestehende `GET /projects`-Route erweitert werden oder eine neue Route erstellt werden?

## Vorschläge

1. **Backend-Erweiterung**:
   - Parameter `technology` oder `tag` zu `GET /projects` hinzufügen
   - Repository-Methode `get_by_technology` erstellen, die `LIKE '%technology%'` verwendet
   - Service-Methode entsprechend erweitern

2. **Frontend-Änderungen**:
   - Projekt-Detailseite: Technologie-Tags in `<NuxtLink>` umwandeln, die zu `/projects?technology=${tech}` navigieren
   - Projekte-Listenseite: URL-Parameter `technology` auslesen und automatisch Filter anwenden
   - URL-Synchronisation: Bei Klick auf Tag soll URL aktualisiert werden

3. **Optional**: Tag-Cloud oder Suchseite erstellen

Bitte bestätigen Sie diese Interpretation oder geben Sie präzisere Anforderungen.