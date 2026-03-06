# Hackathon Pages Atomic Design Refactoring Plan

## Analyseergebnisse

### Aktuelle Komponentenstruktur

**Pages:**
1. `hackathons/index.vue` - Hackathon-Liste
2. `hackathons/[id]/index.vue` - Hackathon-Detail
3. `hackathons/[id]/projects.vue` - Hackathon-Projekte
4. `create/hackathon.vue` - Hackathon erstellen

**Verwendete Komponenten:**

| Komponente | Typ (aktuell) | Soll-Typ | Verzeichnis (aktuell) | Soll-Verzeichnis |
|------------|---------------|----------|----------------------|------------------|
| PageHeader | Molecule | Molecule | molecules/ | ✓ |
| FilterTabs | Molecule | Molecule | molecules/ | ✓ |
| LoadingState | Molecule | Molecule | molecules/ | ✓ |
| ErrorState | Molecule | Molecule | molecules/ | ✓ |
| EmptyState | Molecule | Molecule | molecules/ | ✓ |
| Pagination | Molecule | Molecule | molecules/ | ✓ |
| HackathonListCard | Organism | Organism | organisms/hackathons/ | ✓ |
| HackathonHero | Organism | Organism | hackathons/ | organisms/hackathons/ |
| HackathonDescription | Organism | Organism | hackathons/ | organisms/hackathons/ |
| PrizeList | Organism | Organism | hackathons/ | organisms/hackathons/ |
| RulesSection | Organism | Organism | hackathons/ | organisms/hackathons/ |
| HackathonStats | Organism | Organism | hackathons/ | organisms/hackathons/ |
| HackathonActions | Organism | Organism | hackathons/ | organisms/hackathons/ |
| ParticipantList | Organism | Organism | hackathons/ | organisms/hackathons/ |
| HackathonProjectCard | Organism | Organism | hackathons/ | organisms/hackathons/ |
| ProjectListOrganism | Organism | Organism | organisms/projects/ | ✓ |
| HackathonForm | Organism | Organism | organisms/forms/ | ✓ |
| Card | Atom | Atom | atoms/ | ✓ |
| HackathonEditForm | Organism | Organism | components/ | organisms/hackathons/ |

### Identifizierte Probleme

1. **Inkonsistente Verzeichnisstruktur**: Hackathon-Komponenten sind auf zwei Orte verteilt (`components/hackathons/` und `components/organisms/hackathons/`).

2. **Fehlende Atomic Design Klassifizierung**: Komponenten in `components/hackathons/` sind de facto Organismen, sollten aber im `organisms/hackathons/` Verzeichnis sein.

3. **Redundante Komponente**: `components/hackathons/HackathonListCard.vue` existiert doppelt (eine in `hackathons/`, eine in `organisms/hackathons/`). Nur die in `organisms/hackathons/` wird verwendet.

4. **Fehlende Wiederverwendung von Atoms/Molecules**: Viele Hackathon-Komponenten verwenden direkte HTML statt vorhandener Atoms/Molecules (Button, Badge, StatItem).

5. **Fehlende Komponenten**: Keine Hackathon-spezifischen Templates, keine erweiterten Filterkomponenten.

6. **Konsistenz mit anderen Bereichen**: Teams und Projects haben klare Atomic Design Struktur; Hackathons sollten folgen.

## Implementierungsplan

### Phase 1: Verzeichnisstruktur bereinigen

1. **Duplikate entfernen**: Löschen von `components/hackathons/HackathonListCard.vue` (wenn nicht verwendet).
2. **Organismen verschieben**: Alle Komponenten aus `components/hackathons/` nach `components/organisms/hackathons/` verschieben:
   - `HackathonHero.vue`
   - `HackathonDescription.vue`
   - `PrizeList.vue`
   - `RulesSection.vue`
   - `HackathonStats.vue`
   - `HackathonActions.vue`
   - `ParticipantList.vue`
   - `HackathonProjectCard.vue`
3. **HackathonEditForm verschieben**: `components/HackathonEditForm.vue` nach `components/organisms/hackathons/HackathonEditForm.vue`.
4. **Import-Pfade aktualisieren**: In allen Pages und Komponenten die Import-Pfade anpassen.

### Phase 2: Atomic Design Verbesserungen

1. **HackathonStats refactoren**: Verwenden von Atom-Komponenten:
   - `Badge` für Status
   - `StatItem` (neu erstellen) für Statistikzeilen
2. **ParticipantList refactoren**: Verwenden von `TeamCard` oder `TeamMemberItem` Molekül.
3. **HackathonActions refactoren**: Verwenden von `Button` Atom.
4. **Neue Atom/Molecule Komponenten erstellen** (falls benötigt):
   - `StatItem` Molekül für Statistikzeilen
   - `HackathonStatusBadge` Atom (kann aus `Badge` erweitert werden)
5. **Konsistente Props-Schnittstellen**: TypeScript Interfaces für Hackathon-Daten definieren.

### Phase 3: Templates und erweiterte Funktionalität

1. **HackathonPageTemplate erstellen**: Template für Hackathon-Detailseiten (optional).
2. **HackathonFilter Organism erstellen**: Erweiterte Filterkomponente für Hackathon-Liste.
3. **HackathonCard Molekül erstellen**: Kleine Karte für kompakte Darstellungen (optional).

### Phase 4: Konsistenzprüfung und Testing

1. **Alle Pages auf Konsistenz prüfen**: Sicherstellen, dass alle Importe korrekt sind.
2. **TypeScript-Fehler beheben**: Nach dem Refactoring mögliche TypeScript-Fehler korrigieren.
3. **Build testen**: `npm run build` ausführen, um sicherzustellen, dass keine Breaking Changes entstanden sind.
4. **Visuelle Regression testen**: Manuell prüfen, ob UI unverändert bleibt.

## Detaillierte Aufgabenliste

### Aufgabe 1: Duplikate entfernen
- [ ] Prüfen, ob `components/hackathons/HackathonListCard.vue` verwendet wird
- [ ] Wenn nicht verwendet, Datei löschen
- [ ] Wenn verwendet, Importe auf `organisms/hackathons/HackathonListCard.vue` umstellen

### Aufgabe 2: Organismen verschieben
- [ ] Neue Verzeichnisstruktur erstellen: `components/organisms/hackathons/`
- [ ] Dateien von `components/hackathons/` nach `components/organisms/hackathons/` verschieben:
  - [ ] `HackathonHero.vue`
  - [ ] `HackathonDescription.vue`
  - [ ] `PrizeList.vue`
  - [ ] `RulesSection.vue`
  - [ ] `HackathonStats.vue`
  - [ ] `HackathonActions.vue`
  - [ ] `ParticipantList.vue`
  - [ ] `HackathonProjectCard.vue`
- [ ] `HackathonEditForm.vue` von `components/` nach `components/organisms/hackathons/` verschieben

### Aufgabe 3: Import-Pfade aktualisieren
- [ ] In `hackathons/index.vue`: Import von `HackathonListCard` prüfen (bereits korrekt)
- [ ] In `hackathons/[id]/index.vue`: Alle Importe von `~/components/hackathons/` auf `~/components/organisms/hackathons/` aktualisieren
- [ ] In `hackathons/[id]/projects.vue`: Import von `HackathonProjectCard` aktualisieren
- [ ] In `create/hackathon.vue`: Import von `HackathonForm` bleibt gleich
- [ ] In `hackathons/[id]/index.vue`: Import von `HackathonEditForm` aktualisieren

### Aufgabe 4: HackathonStats mit Atoms/Molecules refactoren
- [ ] `StatItem` Molekül erstellen (wiederverwendbar für Statistikzeilen)
- [ ] `Badge` Atom für Status verwenden
- [ ] `HackathonStats.vue` umschreiben, um diese Komponenten zu nutzen

### Aufgabe 5: ParticipantList mit Team-Komponenten refactoren
- [ ] Prüfen, ob `TeamCard` oder `TeamMemberItem` Molekül verwendet werden kann
- [ ] `ParticipantList.vue` anpassen, um Team-Komponenten zu nutzen
- [ ] Falls nicht passend, eigene `TeamCard` Variante für Hackathons erstellen

### Aufgabe 6: HackathonActions mit Button Atom refactoren
- [ ] `Button` Atom importieren und verwenden
- [ ] Konsistente Styling mit anderen Buttons im Projekt

### Aufgabe 7: TypeScript Interfaces definieren
- [ ] `types/hackathon.ts` erstellen mit Interfaces für:
  - `Hackathon`
  - `HackathonPrize`
  - `HackathonTeam`
  - `HackathonStats`
- [ ] Alle Komponenten auf TypeScript Interfaces umstellen

### Aufgabe 8: Build und Testing
- [ ] `npm run build` ausführen
- [ ] TypeScript-Fehler beheben
- [ ] Manuell Pages testen:
  - [ ] `http://localhost:3001/hackathons`
  - [ ] `http://localhost:3001/hackathons/1`
  - [ ] `http://localhost:3001/hackathons/1/projects`
  - [ ] `http://localhost:3001/create/hackathon`

## Risiken und Abhängigkeiten

1. **Breaking Changes**: Änderungen an Import-Pfaden können zu Runtime-Fehlern führen, wenn nicht alle Dateien aktualisiert werden.
2. **Visuelle Änderungen**: Refactoring könnte unbeabsichtigte Styling-Änderungen verursachen.
3. **TypeScript-Kompatibilität**: Neue Interfaces müssen mit bestehenden Datenstrukturen kompatibel sein.
4. **Backend-API**: Komponenten hängen von Backend-API-Datenstrukturen ab; Änderungen dort könnten Props beeinflussen.

## Erfolgskriterien

1. **Alle Hackathon-Pages funktionieren** ohne Fehler im Browser.
2. **Build erfolgreich** ohne TypeScript- oder Compiler-Fehler.
3. **Konsistente Verzeichnisstruktur**: Alle Hackathon-Organismen unter `organisms/hackathons/`.
4. **Wiederverwendung von Atoms/Molecules**: Mindestens 3 Komponenten verwenden vorhandene Atoms/Molecules.
5. **TypeScript-Sicherheit**: Alle Props sind korrekt typisiert.

## Zeitplan (relativ)

- Phase 1: 1-2 Stunden
- Phase 2: 2-3 Stunden
- Phase 3: 1-2 Stunden (optional)
- Phase 4: 1-2 Stunden

**Gesamt: 5-9 Stunden Arbeit**

## Nächste Schritte

1. Benutzer um Genehmigung des Plans bitten.
2. Bei Genehmigung in Code-Mode wechseln und Implementierung starten.
3. Schrittweise gemäß Aufgabenliste vorgehen.
4. Nach jedem größeren Schritt Build testen.