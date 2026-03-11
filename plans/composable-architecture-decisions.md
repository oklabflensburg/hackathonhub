# Architektur-Entscheidungen für Composable-Migration

## Entscheidungen getroffen am 2026-03-10

### 1. Case Convention
**Entscheidung**: camelCase für alle Frontend-Typen und -Properties

**Begründung**:
- Konsistenz mit bestehenden TypeScript-Konventionen im Projekt
- Bessere Integration mit Vue/JavaScript Ökosystem
- API-Responses werden mit snake_case geliefert, benötigen Mapping
- Bestehende `team-types.ts` und `project-types.ts` verwenden bereits camelCase

**Implementierung**:
- Alle neuen Typ-Definitionen verwenden camelCase
- API-Response Mapper transformieren snake_case → camelCase
- Bestehende camelCase Typen bleiben unverändert

### 2. ID-Typen
**Entscheidung**: `string` für alle ID-Felder

**Begründung**:
- UUIDs werden als Strings gespeichert und übertragen
- Konsistenz mit bestehenden `team-types.ts` (`id: string`)
- Vermeidung von Typ-Konflikten zwischen `number` und `string`
- Bessere Kompatibilität mit zukünftigen Änderungen

**Implementierung**:
- Aktualisierung von `hackathon-types.ts` von `id: number` zu `id: string`
- Aktualisierung aller Composables zu `string` IDs
- API-Responses können Zahlen enthalten, benötigen String-Konvertierung

### 3. Enum vs String Literal
**Entscheidung**: TypeScript Enums für feste Wertemengen

**Begründung**:
- Bessere Type-Safety und Autovervollständigung
- Bestehende Enums in `team-types.ts` und `project-types.ts`
- Konsistente Dokumentation der möglichen Werte

**Implementierung**:
- Neue Enums für fehlende Wertemengen (z.B. CommentStatus, NotificationType)
- Verwendung bestehender Enums wo möglich

### 4. API Response Mapping
**Entscheidung**: Zentrale Mapper-Funktionen für API-Response Transformation

**Begründung**:
- Trennung von API-Format und Frontend-Format
- Einfacheres Handling von Feldnamen-Unterschieden
- Zentrale Stelle für Format-Konvertierungen

**Implementierung**:
- `utils/api-mappers.ts` mit Mapper-Funktionen für alle Entitäten
- Automatische snake_case → camelCase Konvertierung
- Typ-Konvertierung (number → string für IDs)

### 5. Composable Return Types
**Entscheidung**: Zentrale Return-Type Interfaces in Typ-Dateien

**Begründung**:
- Konsistente Signatur für alle Composables
- Wiederverwendbarkeit in Tests und Dokumentation
- Bessere Type-Safety für Composables

**Implementierung**:
- `UseTeamsReturn`, `UseProjectsReturn` etc. in entsprechenden Typ-Dateien
- Composables importieren und implementieren diese Interfaces

### 6. Abwärtskompatibilität
**Entscheidung**: Hybrid-Ansatz mit Re-export Pattern

**Begründung**:
- Vermeidung von Breaking Changes für bestehende Komponenten
- Schrittweise Migration möglich
- Alte und neue Typen koexistieren während der Migration

**Implementierung**:
- Alte Typen bleiben als Aliase verfügbar
- Neue Typen werden parallel eingeführt
- Migration Guide für Komponenten-Entwickler

### 7. Dateiformat für Zeitstempel
**Entscheidung**: ISO 8601 Strings (`string`)

**Begründung**:
- Konsistenz mit bestehenden Typen (`createdAt: string`)
- Einfache Serialisierung/Deserialisierung
- Kompatibilität mit JavaScript Date-Objekten

### 8. Nullable vs Optional Fields
**Entscheidung**: Explizite Nullability mit `| null` für nullable Felder

**Begründung**:
- Klare Unterscheidung zwischen "nicht vorhanden" und "explizit null"
- Konsistenz mit bestehenden Typen
- Bessere Type-Safety

## Migration Prioritäten

### Phase 1: Typ-Definition Konsolidierung
1. `hackathon-types.ts` aktualisieren (ID: string, camelCase)
2. `comment-types.ts` erstellen (neu)
3. `notification-types.ts` erstellen (neu)
4. `file-upload-types.ts` erstellen (neu)

### Phase 2: Composable-Migration
1. `useTeams.ts` - Hochpriorität (größte Inkonsistenzen)
2. `useProjects.ts` - Hochpriorität (wichtige Business-Logik)
3. `useHackathons.ts` - Hochpriorität (ID-Typ Konflikt)
4. `useComments.ts` - Mittelpriorität (neue Typ-Datei)
5. Weitere Composables - Niedrigpriorität

### Phase 3: Mapper-Implementierung
1. `utils/api-mappers.ts` mit Basis-Mappern
2. Entity-spezifische Mapper-Funktionen
3. Test-Suite für Mapper

## Erfolgskriterien
- Keine TypeScript-Kompilierungsfehler nach Migration
- Alle bestehenden Tests bestehen
- Keine Breaking Changes für öffentliche APIs
- Konsistente Feldnamen über alle Typen hinweg
- Vollständige Dokumentation der Änderungen