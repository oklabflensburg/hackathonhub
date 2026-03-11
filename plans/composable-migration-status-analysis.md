# Vue Composables Migration Status Analyse

## Übersicht
Systematische Analyse aller 22 Vue-Composables im Projekt zur Bewertung des Migrationsstatus bezüglich:
1. Verwendung zentraler Typ-Dateien (`~/types/*`)
2. Verwendung des zentralen `ApiClient` (`~/utils/api-client`)
3. Konsistenz mit Architekturrichtlinien

## Composables Liste und Status

### ✅ **Vollständig migriert** (verwenden zentrale Typen + ApiClient)

| Composable | Zentrale Typen | ApiClient | Bemerkungen |
|------------|----------------|-----------|-------------|
| `useAuth.ts` | ✅ `auth-types.ts` | ✅ | Vollständig migriert, verwendet zentrale Typen |
| `useTeams.ts` | ✅ `team-types.ts` | ✅ | Vollständig migriert mit API-Mappern |
| `useProjects.ts` | ✅ `project-types.ts` | ✅ | Vollständig migriert mit API-spezifischen Typen |
| `useComments.ts` | ✅ `comment-types.ts` | ✅ | Verwendet zentrale Typen und ApiClient |
| `useNotifications.ts` | ✅ `notification-types.ts` | ✅ | Verwendet zentrale Typen |
| `useSettings.ts` | ✅ `settings-types.ts` | ⚠️ | Verwendet zentrale Typen, aber API-Aufrufe sind TODO |
| `usePrivacySettings.ts` | ✅ `settings-types.ts` | ❌ | UI-only, keine API-Aufrufe |
| `useLayoutNavigation.ts` | ✅ `layout-types.ts` | ❌ | UI-only, keine API-Aufrufe |
| `useTheme.ts` | ✅ `layout-types.ts` | ❌ | UI-only, keine API-Aufrufe |
| `useFeatureFlags.ts` | ❌ (eigene Interface) | ❌ | Wrapper um bestehende Implementierung |

### ⚠️ **Teilweise migriert** (verwenden zentrale Typen, aber nicht ApiClient)

| Composable | Zentrale Typen | ApiClient | Bemerkungen |
|------------|----------------|-----------|-------------|
| `useHackathonData.ts` | ✅ `hackathon-types.ts` | ❌ | Verwendet zentrale Typen, aber keine API-Aufrufe |
| `useHackathonsList.ts` | ✅ `hackathon-types.ts` | ❌ | Verwendet zentrale Typen, aber keine API-Aufrufe |
| `useUserProfile.ts` | ✅ `user-types.ts` | ❌ | Verwendet zentrale Typen, aber keine API-Aufrufe |
| `useProjectFilters.ts` | ✅ `project-types.ts` | ❌ | UI-only, keine API-Aufrufe |
| `useProjectComments.ts` | ✅ `project-types.ts` | ❌ | Verwendet zentrale Typen, aber keine API-Aufrufe |
| `useProjectVoting.ts` | ✅ `project-types.ts` | ❌ | Verwendet zentrale Typen, aber keine API-Aufrufe |
| `useTeamInvitations.ts` | ✅ `team-invitations.ts` | ❌ | Verwendet zentrale Typen, aber keine API-Aufrufe |
| `useUserSearch.ts` | ✅ `team-invitations.ts` | ❌ | Verwendet zentrale Typen, aber keine API-Aufrufe |
| `useTeamMembers.ts` | ❌ (lokale Typen) | ❌ | Verwendet lokale Typen, keine API-Aufrufe |

### ❌ **Nicht migriert** (verwenden weder zentrale Typen noch ApiClient)

| Composable | Zentrale Typen | ApiClient | Bemerkungen |
|------------|----------------|-----------|-------------|
| `useHackathons.ts` | ⚠️ (gemischt) | ✅ | Verwendet teilweise zentrale Typen, aber nicht vollständig migriert |
| `useNewsletter.ts` | ❌ (lokale Typen) | ✅ | Verwendet ApiClient, aber keine zentralen Typen |
| `useFileUpload.ts` | ❌ (lokale Typen) | ❌ | Verwendet weder zentrale Typen noch ApiClient |

## Detaillierte Analyse

### 1. **`useHackathons.ts`** - ⚠️ Teilweise migriert
- **Importe**: `import type { Hackathon, HackathonRegistration, HackathonRegistrationStatus } from '~/types/hackathon-types'`
- **ApiClient**: ✅ Verwendet
- **Problem**: Verwendet teilweise zentrale Typen, aber nicht vollständig migriert (fehlende API-spezifische Typen, keine Mapper)

### 2. **`useNewsletter.ts`** - ❌ Nicht migriert  
- **Importe**: Keine zentralen Typen
- **ApiClient**: ✅ Verwendet
- **Problem**: Verwendet lokale Typen statt `newsletter-types.ts`

### 3. **`useFileUpload.ts`** - ❌ Nicht migriert
- **Importe**: Keine zentralen Typen
- **ApiClient**: ❌ Nicht verwendet (vermutlich direkte fetch/axios)
- **Problem**: Muss zu `file-upload-types.ts` migriert werden

### 4. **`useSettings.ts`** - ⚠️ Teilweise migriert
- **Importe**: ✅ Vollständige `settings-types.ts` Importe
- **ApiClient**: ⚠️ TODO-Kommentare für API-Aufrufe
- **Problem**: API-Implementierung fehlt

### 5. **UI-only Composables** - ✅ Migriert (soweit relevant)
- `usePrivacySettings.ts`, `useLayoutNavigation.ts`, `useTheme.ts`, `useFeatureFlags.ts`
- Diese benötigen keine API-Aufrufe, daher ist die Migration auf zentrale Typen ausreichend

## Identifizierte Probleme

### 1. **Fehlende zentrale Typ-Dateien**
- `team-invitations.ts` existiert bereits und wird verwendet
- `file-upload-types.ts` wurde erstellt, aber nicht von `useFileUpload.ts` verwendet
- `newsletter-types.ts` wurde erstellt, aber nicht von `useNewsletter.ts` verwendet

### 2. **Inkonsistente ApiClient-Nutzung**
- Einige Composables verwenden `useApiClient()`, andere nicht
- `useSettings.ts` hat TODO-Kommentare für API-Implementierung
- `useFileUpload.ts` verwendet wahrscheinlich direkte fetch/axios-Aufrufe

### 3. **Fehlende API-Mapper**
- `useHackathons.ts` verwendet keine Mapper für API-Response Transformation
- `useNewsletter.ts` verwendet keine Mapper
- `useFileUpload.ts` verwendet keine Mapper

## Migrationsprioritäten

### **Priorität 1: Kritische Composables mit API-Aufrufen**
1. **`useHackathons.ts`** - Hochpriorität (wird häufig verwendet, hat API-Aufrufe)
2. **`useNewsletter.ts`** - Mittelpriorität (verwendet ApiClient, aber keine zentralen Typen)
3. **`useFileUpload.ts`** - Hochpriorität (vermutlich direkte fetch-Aufrufe)

### **Priorität 2: Composables mit fehlender API-Implementierung**
4. **`useSettings.ts`** - Mittelpriorität (TODO-Kommentare für API-Aufrufe)

### **Priorität 3: UI-only Composables (niedrige Priorität)**
5. **`useHackathonData.ts`** - Kann später migriert werden
6. **`useHackathonsList.ts`** - Kann später migriert werden
7. **`useUserProfile.ts`** - Kann später migriert werden

## Migrationsplan

### Phase 1: `useHackathons.ts` Migration
1. Zentrale Typen in `hackathon-types.ts` vervollständigen
2. API-spezifische Typen (`ApiHackathon`, `ApiHackathonCreateData`, etc.) hinzufügen
3. Mapper-Funktionen in `api-mappers.ts` ergänzen
4. Composable auf string IDs und camelCase umstellen
5. API-Response Mapping implementieren

### Phase 2: `useNewsletter.ts` Migration
1. Zentrale Typen in `newsletter-types.ts` überprüfen/ergänzen
2. Composable auf zentrale Typen umstellen
3. API-Response Mapping implementieren

### Phase 3: `useFileUpload.ts` Migration
1. Zentrale Typen in `file-upload-types.ts` überprüfen/ergänzen
2. Composable auf ApiClient umstellen
3. API-Response Mapping implementieren

### Phase 4: `useSettings.ts` Fertigstellung
1. API-Aufrufe implementieren
2. Error-Handling hinzufügen
3. Loading-States implementieren

## Empfehlungen

### 1. **Konsistente Import-Struktur**
```typescript
// Gutes Beispiel (useAuth.ts)
import { useApiClient } from '~/utils/api-client'
import type { LoginCredentials, RegisterCredentials } from '~/types/auth-types'
```

### 2. **API-Response Mapping**
```typescript
// Gutes Beispiel (useTeams.ts)
const response = await apiClient.get<ApiTeam[]>(url)
const teams = response.map(mapApiTeamToTeam)
```

### 3. **String IDs und camelCase**
```typescript
// Frontend: string IDs, camelCase
const teamId = "123" // string
const teamName = "teamName" // camelCase

// API: number IDs, snake_case
const numericId = idToNumber(teamId) // 123
const apiPayload = { team_name: teamName } // snake_case
```

### 4. **Error-Handling**
```typescript
try {
  const response = await apiClient.get<ApiEntity>(url)
  return mapApiEntityToEntity(response)
} catch (error) {
  error.value = error instanceof Error ? error.message : 'Unknown error'
  throw error
}
```

## Nächste Schritte

1. **Priorität 1 Composables migrieren** (`useHackathons.ts`, `useNewsletter.ts`, `useFileUpload.ts`)
2. **TypeScript-Validierung** für alle migrierten Composables
3. **Testing** der migrierten Composables
4. **Dokumentation** der Migration abschließen

Die Analyse zeigt, dass der Großteil der Composables bereits zentrale Typen verwendet, aber einige kritische Composables noch nicht vollständig migriert sind. Die Migration kann schrittweise nach dem etablierten Muster durchgeführt werden.