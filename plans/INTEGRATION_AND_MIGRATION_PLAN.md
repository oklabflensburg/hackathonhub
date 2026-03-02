# Integration und Migration Plan

## Übersicht

Dieser Plan beschreibt die schrittweise Integration der neuen Organism-Komponenten in die bestehenden Seiten und die Migration von Inline-Code zu den neuen Komponenten.

## Grundprinzipien

1. **Schrittweises Vorgehen**: Eine Komponente nach der anderen integrieren
2. **Feature-Flags**: Optionale Nutzung neuer Komponenten während der Migration
3. **Testing-First**: Jede Integration mit Tests absichern
4. **Rollback-Fähigkeit**: Jeder Schritt sollte reversibel sein

## Migrationsstrategie für jede Seite

### 1. Team-Detailseite (`teams/[id]/index.vue`)

**Aktueller Zustand**:
- Verwendet `TeamDetailHeader` Komponente
- Inline-Code für Mitgliederliste (~100 Zeilen)
- Inline-Code für Projekte (falls vorhanden)
- Inline-Code für Beschreibung

**Migrationsschritte**:

#### Schritt 1: `TeamMembers` Organism integrieren
1. `TeamMembers.vue` Komponente erstellen (basierend auf Spezifikation)
2. Inline-Code für Mitgliederliste (Zeilen 50-150+) identifizieren
3. Temporäre Komponente mit Feature-Flag einfügen:
   ```vue
   <!-- Vorübergehend: Beide Versionen anzeigen -->
   <div v-if="useNewTeamMembers">
     <TeamMembers
       :members="members"
       :current-user-id="authStore.user?.id"
       :is-team-owner="isTeamOwner"
       :max-members="team.max_members"
       @make-owner="makeOwner"
       @make-member="makeMember"
       @remove-member="removeMember"
     />
   </div>
   <div v-else>
     <!-- Existierender Inline-Code -->
   </div>
   ```

4. Event-Handler anpassen:
   - `makeOwner`, `makeMember`, `removeMember` Funktionen müssen mit der neuen Komponente kompatibel sein

5. Testing:
   - Unit-Tests für `TeamMembers` Komponente
   - Integrationstests für die Seite
   - Manuelles Testing aller Mitglieder-Aktionen

6. Feature-Flag entfernen:
   - Nach erfolgreichem Testing Inline-Code entfernen
   - Nur neue Komponente verwenden

#### Schritt 2: `TeamProjects` Organism integrieren (falls benötigt)
1. Prüfen, ob Projekte in der Team-Detailseite angezeigt werden
2. Falls ja: `TeamProjects.vue` erstellen und integrieren
3. Ähnlicher Prozess wie bei `TeamMembers`

#### Schritt 3: `TeamDescription` als Molecule extrahieren
1. Beschreibungsbereich (Zeilen 43-48) in Molecule extrahieren
2. Mit Bearbeitungsfunktion erweitern (falls benötigt)

**Erwartetes Ergebnis**:
- Reduzierung von ~100 Zeilen Inline-Code auf ~20 Zeilen Komponenten-Usage
- Bessere Wartbarkeit und Testbarkeit
- Wiederverwendbare Komponente für andere Kontexte

### 2. Profilseite (`profile.vue`)

**Aktueller Zustand**:
- Verwendet `ProfileHeader` und `UserSettingsForm`
- Komplexe Tab-Navigation mit Inline-Inhalten
- Viel Inline-Code für Projekte, Teams, Einstellungen

**Migrationsschritte**:

#### Schritt 1: Tab-Struktur refaktorieren
1. Aktuelle Tab-Logik analysieren
2. Gemeinsame Tab-Komponente erstellen oder vorhandene verwenden
3. Tab-Inhalte als separate Organisms strukturieren

#### Schritt 2: `ProfileOverview` integrieren
1. Für "Übersicht"-Tab: `ProfileOverview` Organism erstellen
2. Benutzerstatistiken und Informationen extrahieren
3. Integration mit Feature-Flag

#### Schritt 3: `UserProjects` integrieren
1. Für "Projekte"-Tab: `UserProjects` Organism erstellen
2. Projektliste und Filterlogik extrahieren
3. Wiederverwendung für `my-projects.vue` ermöglichen

#### Schritt 4: `UserTeams` integrieren
1. Für "Teams"-Tab: `UserTeams` Organism erstellen
2. Teamliste extrahieren

#### Schritt 5: `UserSettingsForm` optimieren
1. Bereits vorhandene Komponente überprüfen
2. Eventuell in kleinere Komponenten aufteilen

**Erwartetes Ergebnis**:
- Klare Trennung der Tab-Inhalte
- Wiederverwendbare Organisms für Profile und Listen
- Reduzierung der Seitenkomplexität

### 3. Hackathon-Detailseite (`hackathons/[id]/index.vue`)

**Aktueller Zustand**:
- Verwendet mehrere Komponenten (`HackathonDescription`, `ParticipantList`, etc.)
- Könnte weiter strukturiert werden

**Migrationsschritte**:

#### Schritt 1: Tab-Navigation implementieren
1. Aktuelle Struktur analysieren (Projekte vs. Teilnehmer vs. Informationen)
2. Tab-Komponente für bessere Navigation erstellen

#### Schritt 2: `HackathonInfo` integrieren
1. Grundinformationen und Beschreibung in Organism extrahieren
2. Regeln und Technologien integrieren

#### Schritt 3: `HackathonProjects` integrieren
1. Projektliste für Hackathon optimieren
2. Filter und Sortierung hinzufügen

#### Schritt 4: `ParticipantList` optimieren
1. Bereits vorhandene Komponente überprüfen
2. Eventuell erweitern oder in Organism umwandeln

**Erwartetes Ergebnis**:
- Bessere Benutzerführung durch Tabs
- Konsistente Struktur mit anderen Detailseiten
- Wiederverwendbare Komponenten

### 4. Notifications-Seite (`notifications.vue`)

**Aktueller Zustand**:
- Verwendet `NotificationSettings` und `NotificationContainer`
- Komplexe Filter- und Einstellungslogik

**Migrationsschritte**:

#### Schritt 1: `NotificationList` integrieren
1. Benachrichtigungsliste mit Filterlogik extrahieren
2. Mark-as-Read und Delete-Funktionalität integrieren

#### Schritt 2: `NotificationFilters` integrieren
1. Filterkomponente als separate Molecule oder Teil von `NotificationList`
2. TypeScript-Typen für Filter definieren

#### Schritt 3: `NotificationSettings` optimieren
1. Bereits vorhandene Komponente überprüfen
2. Eventuell in Organism umwandeln

**Erwartetes Ergebnis**:
- Trennung von Liste, Filtern und Einstellungen
- Bessere Performance durch optimierte Filterlogik
- Wiederverwendbare Komponenten

### 5. Projekt-Bearbeitungsseite (`projects/[id]/edit.vue`)

**Migrationsschritte**:

#### Schritt 1: `EditProjectForm` erstellen
1. Basierend auf vorhandenem `ProjectForm` Organism
2. Anpassungen für Edit-Modus:
   - Pre-filled Form Fields
   - Delete-Button
   - Image Update Logic

#### Schritt 2: Bild-Upload optimieren
1. Separate `ImageUploadSection` Komponente erstellen
2. Vorschau, Crop-Funktionalität, Validierung

#### Schritt 3: Technologie-Management
1. `TechnologyManagement` Komponente erstellen
2. Tag-Input mit Autocomplete

**Erwartetes Ergebnis**:
- Wiederverwendung von `ProjectForm` Logik
- Spezifische Edit-Funktionalität
- Bessere Benutzererfahrung für Bild-Upload

## Technische Implementierungsdetails

### Feature-Flags Implementierung
```typescript
// In Composition API
const useNewComponents = ref(false)

// Oder in Config
const config = useRuntimeConfig()
const useNewTeamMembers = config.public.featureFlags?.newTeamMembers || false
```

### State Management Migration
- Existierender State in Composables extrahieren
- Kompatibilität mit beiden Versionen während der Migration
- Schrittweise Migration der Event-Handler

### Testing Strategy
1. **Unit Tests**: Für jede neue Komponente
2. **Integration Tests**: Für die Integration in Seiten
3. **E2E Tests**: Für kritische User Journeys
4. **Regression Tests**: Für bestehende Funktionalität

### Performance Considerations
- Lazy-Loading für nicht-kritische Komponenten
- Memoization für teure Berechnungen
- Bundle Size Monitoring

## Rollback Plan

### Für jede Migration:
1. **Vor der Migration**: Commit mit sauberem Zustand
2. **Während der Migration**: Feature-Flags für einfaches Umschalten
3. **Bei Problemen**: 
   - Feature-Flag auf "false" setzen
   - Zur vorherigen Version zurückkehren
   - Problem analysieren und fixen

### Monitoring:
- Console Errors überwachen
- User Feedback sammeln
- Performance-Metriken tracken

## Zeitplan für Integration

### Woche 1: Team-Detailseite
- Tag 1: `TeamMembers` Komponente erstellen und testen
- Tag 2: Integration mit Feature-Flag
- Tag 3: Testing und Bug-Fixing
- Tag 4: Feature-Flag entfernen, Inline-Code löschen
- Tag 5: `TeamProjects` Integration (falls benötigt)

### Woche 2: Profilseite
- Tag 1: Tab-Struktur refaktorieren
- Tag 2: `ProfileOverview` integrieren
- Tag 3: `UserProjects` integrieren
- Tag 4: `UserTeams` integrieren
- Tag 5: Testing und Optimierung

### Woche 3: Hackathon-Detailseite
- Tag 1: Tab-Navigation implementieren
- Tag 2: `HackathonInfo` integrieren
- Tag 3: `HackathonProjects` integrieren
- Tag 4: Testing und Optimierung
- Tag 5: Feinabstimmung

### Woche 4: Notifications und Projekt-Edit
- Tag 1-2: `NotificationList` und `NotificationFilters`
- Tag 3: `EditProjectForm`
- Tag 4: Integration und Testing
- Tag 5: Finale Optimierungen und Bug-Fixing

## Erfolgsmetriken für Integration

### Für jede Seite:
- [ ] Keine Regressionen in bestehender Funktionalität
- [ ] Reduzierung der Seiten-Größe um ≥ 60%
- [ ] Alle Unit- und Integrationstests bestehen
- [ ] Keine neuen Console Errors
- [ ] Performance gleich oder besser

### Für das Gesamtsystem:
- [ ] Bundle Size nicht signifikant erhöht
- [ ] Ladezeiten gleich oder besser
- [ ] Developer Experience verbessert
- [ ] Code Coverage erhöht

## Nächste Schritte nach Abschluss

1. **Code Review**: Alle neuen Komponenten und Integrationen
2. **Performance Audit**: Bundle Size und Ladezeiten analysieren
3. **Documentation**: Komponenten-Dokumentation aktualisieren
4. **Knowledge Transfer**: Team über neue Struktur informieren
5. **Phase 4 Planung**: Nächste Refactoring-Schritte planen

---
**Status**: Integrationsplan erstellt  
**Empfohlener Start**: Mit Team-Detailseite Migration  
**Risikobewertung**: Mittel (wegen Feature-Flags und schrittweisem Vorgehen)