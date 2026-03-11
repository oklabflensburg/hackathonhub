# Migrationsplan für verbleibende Vue-Composables

## Übersicht
Dieser Plan beschreibt die schrittweise Migration der verbleibenden 3 kritischen Composables, die noch nicht vollständig auf die zentrale Architektur migriert wurden.

## Kritische Composables für Migration

### 1. **`useHackathons.ts`** (Priorität: Hoch)
- **Status**: Teilweise migriert (verwendet zentrale Typen und ApiClient, aber nicht vollständig)
- **Probleme**:
  - Verwendet teilweise zentrale Typen, aber nicht alle benötigten Typen
  - Keine API-Response Mapper
  - Keine konsistente ID-Typ Konvertierung (string ↔ number)
  - Keine camelCase/snake_case Transformation

### 2. **`useNewsletter.ts`** (Priorität: Mittel)
- **Status**: Nicht migriert (verwendet ApiClient, aber keine zentralen Typen)
- **Probleme**:
  - Verwendet lokale Typen statt `newsletter-types.ts`
  - Keine API-Response Mapper
  - Keine konsistente Error-Handling

### 3. **`useFileUpload.ts`** (Priorität: Hoch)
- **Status**: Nicht migriert (verwendet weder zentrale Typen noch ApiClient)
- **Probleme**:
  - Verwendet wahrscheinlich direkte fetch/axios-Aufrufe
  - Keine zentralen Typen
  - Kein ApiClient

## Detaillierter Migrationsplan

### Phase 1: `useHackathons.ts` Migration

#### Schritt 1: Zentrale Typen vervollständigen
- **Datei**: `frontend3/app/types/hackathon-types.ts`
- **Erforderliche Ergänzungen**:
  - API-spezifische Typen: `ApiHackathon`, `ApiHackathonCreateData`, `ApiHackathonUpdateData`
  - API-Response Typen: `ApiHackathonRegistration`, `ApiHackathonRegistrationStatus`
  - Frontend-spezifische Typen: `Hackathon`, `HackathonRegistration`, `HackathonRegistrationStatus`
  - Mapper-Typen: `HackathonCreateUpdateData`

#### Schritt 2: Mapper-Funktionen ergänzen
- **Datei**: `frontend3/app/utils/api-mappers.ts`
- **Erforderliche Funktionen**:
  ```typescript
  export function mapApiHackathonToHackathon(apiHackathon: ApiHackathon): Hackathon
  export function mapHackathonCreateUpdateDataToApi(data: HackathonCreateUpdateData): ApiHackathonCreateData | ApiHackathonUpdateData
  export function mapApiHackathonRegistrationToHackathonRegistration(apiRegistration: ApiHackathonRegistration): HackathonRegistration
  ```

#### Schritt 3: Composable migrieren
- **Datei**: `frontend3/app/composables/useHackathons.ts`
- **Änderungen**:
  1. Vollständige Importe von zentralen Typen
  2. String IDs statt number IDs
  3. API-Response Mapping in allen Methoden
  4. camelCase/snake_case Transformation
  5. Konsistentes Error-Handling

#### Schritt 4: Testing und Validierung
- TypeScript-Kompilierung testen
- Laufzeit-Verhalten validieren
- Abwärtskompatibilität sicherstellen

### Phase 2: `useNewsletter.ts` Migration

#### Schritt 1: Zentrale Typen überprüfen/ergänzen
- **Datei**: `frontend3/app/types/newsletter-types.ts`
- **Erforderliche Typen**:
  - `NewsletterSubscription`
  - `NewsletterPreferences`
  - `ApiNewsletterSubscription`
  - `ApiNewsletterPreferences`

#### Schritt 2: Mapper-Funktionen ergänzen
- **Datei**: `frontend3/app/utils/api-mappers.ts`
- **Erforderliche Funktionen**:
  ```typescript
  export function mapApiNewsletterSubscriptionToNewsletterSubscription(apiSubscription: ApiNewsletterSubscription): NewsletterSubscription
  ```

#### Schritt 3: Composable migrieren
- **Datei**: `frontend3/app/composables/useNewsletter.ts`
- **Änderungen**:
  1. Importe von zentralen Typen hinzufügen
  2. Lokale Typen durch zentrale Typen ersetzen
  3. API-Response Mapping implementieren
  4. Konsistentes Error-Handling

### Phase 3: `useFileUpload.ts` Migration

#### Schritt 1: Zentrale Typen überprüfen/ergänzen
- **Datei**: `frontend3/app/types/file-upload-types.ts`
- **Erforderliche Typen**:
  - `FileUploadOptions`
  - `FileUploadProgress`
  - `UploadedFile`
  - `ApiUploadedFile`

#### Schritt 2: Composable auf ApiClient umstellen
- **Datei**: `frontend3/app/composables/useFileUpload.ts`
- **Änderungen**:
  1. `useApiClient` importieren und verwenden
  2. Direkte fetch/axios-Aufrufe durch ApiClient ersetzen
  3. Zentrale Typen importieren und verwenden
  4. Progress-Handling implementieren
  5. Error-Handling konsolidieren

#### Schritt 3: Mapper-Funktionen ergänzen
- **Datei**: `frontend3/app/utils/api-mappers.ts`
- **Erforderliche Funktionen**:
  ```typescript
  export function mapApiUploadedFileToUploadedFile(apiFile: ApiUploadedFile): UploadedFile
  ```

### Phase 4: `useSettings.ts` Fertigstellung

#### Schritt 1: API-Aufrufe implementieren
- **Datei**: `frontend3/app/composables/useSettings.ts`
- **Änderungen**:
  1. `useApiClient` importieren und verwenden
  2. TODO-Kommentare durch echte API-Aufrufe ersetzen
  3. Loading-States implementieren
  4. Error-Handling hinzufügen

#### Schritt 2: Validation und Error-Handling
- Validierungslogik konsolidieren
- User-freundliche Error-Messages
- Auto-Save-Funktionalität testen

## Technische Implementierungsdetails

### 1. API-Response Mapping Pattern
```typescript
// Vorher (ohne Mapping)
const response = await apiClient.get<any>(`/api/hackathons/${hackathonId}`)
currentHackathon.value = response

// Nachher (mit Mapping)
const numericId = idToNumber(hackathonId)
const response = await apiClient.get<ApiHackathon>(`/api/hackathons/${numericId}`)
currentHackathon.value = mapApiHackathonToHackathon(response)
```

### 2. ID-Typ Konvertierung
```typescript
// Frontend: string IDs
const hackathonId = "123"

// API: number IDs  
const numericId = idToNumber(hackathonId) // 123

// Response: zurück zu string
const hackathon = mapApiHackathonToHackathon(response) // id: "123"
```

### 3. Case Convention Transformation
```typescript
// Frontend: camelCase
const hackathonData = {
  hackathonName: "My Hackathon",
  startDate: "2024-01-01"
}

// API: snake_case
const apiPayload = camelToSnake(hackathonData) // {
  // hackathon_name: "My Hackathon",
  // start_date: "2024-01-01"
// }
```

### 4. Error-Handling Konsistenz
```typescript
async function fetchHackathon(hackathonId: string): Promise<Hackathon> {
  try {
    isLoading.value = true
    error.value = null
    
    const numericId = idToNumber(hackathonId)
    const response = await apiClient.get<ApiHackathon>(`/api/hackathons/${numericId}`)
    
    return mapApiHackathonToHackathon(response)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to fetch hackathon'
    throw err
  } finally {
    isLoading.value = false
  }
}
```

## Prioritäten und Zeitplan

### Woche 1: `useHackathons.ts` Migration
- **Montag**: Zentrale Typen und Mapper ergänzen
- **Dienstag**: Composable migrieren
- **Mittwoch**: Testing und Validierung
- **Donnerstag**: Bugfixes und Optimierungen

### Woche 2: `useFileUpload.ts` und `useNewsletter.ts` Migration
- **Montag**: `useFileUpload.ts` auf ApiClient umstellen
- **Dienstag**: `useNewsletter.ts` migrieren
- **Mittwoch**: Testing beider Composables
- **Donnerstag**: Dokumentation und Code-Review

### Woche 3: `useSettings.ts` Fertigstellung und Abschluss
- **Montag**: API-Aufrufe in `useSettings.ts` implementieren
- **Dienstag**: Validation und Error-Handling
- **Mittwoch**: Gesamttesting aller migrierten Composables
- **Donnerstag**: Dokumentation abschließen

## Erfolgskriterien

### 1. **Technische Kriterien**
- ✅ Alle Composables verwenden zentrale Typ-Dateien
- ✅ Alle Composables verwenden den zentralen ApiClient
- ✅ Konsistente ID-Typ Konvertierung (string ↔ number)
- ✅ Konsistente Case Convention (camelCase ↔ snake_case)
- ✅ Einheitliches Error-Handling Pattern
- ✅ TypeScript-Kompilierung ohne Fehler

### 2. **Qualitätskriterien**
- ✅ Keine Breaking Changes für bestehende Komponenten
- ✅ Vollständige Abwärtskompatibilität
- ✅ Konsistente Developer Experience
- ✅ Gute Dokumentation und Code-Kommentare
- ✅ Einheitliche Testing-Coverage

### 3. **Performance-Kriterien**
- ✅ Keine Performance-Regression
- ✅ Effiziente Mapper-Funktionen
- ✅ Minimale Bundle-Size-Erhöhung
- ✅ Gute Caching-Strategien

## Risiken und Mitigation

### 1. **Breaking Changes**
- **Risiko**: Migration könnte bestehende Komponenten brechen
- **Mitigation**: Abwärtskompatible APIs beibehalten, schrittweise Migration

### 2. **Performance-Impact**
- **Risiko**: Mapper-Funktionen könnten Performance beeinträchtigen
- **Mitigation**: Effiziente Implementierung, Caching, Lazy-Loading

### 3. **Testing-Aufwand**
- **Risiko**: Umfangreiche Tests erforderlich
- **Mitigation**: Automatisierte Tests, schrittweise Validierung

### 4. **Developer Adoption**
- **Risiko**: Entwickler müssen neue Patterns lernen
- **Mitigation**: Gute Dokumentation, Code-Beispiele, Schulungen

## Nächste Schritte

1. **Phase 1 starten**: `useHackathons.ts` Migration
2. **Code-Review** nach jeder Phase
3. **Testing** automatisieren
4. **Dokumentation** aktualisieren
5. **Developer Onboarding** vorbereiten

Die Migration der verbleibenden Composables kann nach diesem Plan schrittweise und kontrolliert durchgeführt werden, wobei die etablierten Architekturmuster und Best Practices konsequent angewendet werden.