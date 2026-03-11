# Umfassende Migrationsstrategie für Vue 3 Composables

## 1. Analyse des aktuellen Zustands

### Identifizierte direkte API-Aufrufe:

#### **Stores mit direkten `fetch`-Aufrufen:**
1. **`frontend3/app/stores/auth.ts`** - 13 direkte `fetch`-Aufrufe:
   - `loginWithGitHub()` (Zeile 111)
   - `loginWithGoogle()` (Zeile 149)
   - `verifyTwoFactor()` (Zeile 796)
   - `verifyTwoFactorBackup()` (Zeile 839)
   - `loginWithEmail2FA()` (Zeile 883)
   - `fetchWithAuth()` (Zeilen 362, 412, 461, 691, 716)

2. **`frontend3/app/stores/notification.ts`** - 1 direkter `fetch`-Aufruf:
   - `getVapidPublicKey()` (Zeile 261)

#### **Seiten, die Stores verwenden (indirekte API-Aufrufe):**
- Alle 29 Seiten in `/frontend3/app/pages/` verwenden Stores für API-Operationen
- Keine direkten `fetch`-Aufrufe in Seiten gefunden

#### **Bereits erstellte Composables:**
- ✅ `useAuth.ts` - Authentication (468 Zeilen)
- ✅ `useFileUpload.ts` - File Upload (210 Zeilen)
- ✅ `useNewsletter.ts` - Newsletter (210 Zeilen)
- ✅ `useProjects.ts` - Projects (514 Zeilen)
- ✅ `useTeams.ts` - Teams (~650 Zeilen)
- ✅ `useHackathons.ts` - Hackathons (~500 Zeilen)
- ✅ `useComments.ts` - Comments (~500 Zeilen)

#### **Bereits migrierte Komponenten:**
- ✅ `forgot-password.vue` - Ersetzt direkten `fetch` durch `useAuth().forgotPassword()`
- ✅ `reset-password.vue` - Ersetzt direkten `fetch` durch `useAuth().resetPassword()`
- ✅ `verify-email.vue` - Ersetzt direkten `fetch` durch `useAuth().verifyEmail()`
- ✅ `AppFooterContent.vue` - Ersetzt direkten `fetch` durch `useNewsletter().subscribe()`

## 2. Migrationsstrategie

### **Phase 1: Store-Refactoring (Priorität: Hoch)**
**Ziel:** Ersetzen aller direkten `fetch`-Aufrufe in Stores durch Composables

#### **Auth Store Migration:**
1. **Erstellen einer refactored Version** (`auth-refactored.ts`) mit Composable-Integration
2. **Schrittweise Migration** der Store-Funktionen:
   - `loginWithGitHub()` → `useAuth().loginWithGitHub()`
   - `loginWithGoogle()` → `useAuth().loginWithGoogle()`
   - `verifyTwoFactor()` → `useAuth().verifyTwoFactor()`
   - `verifyTwoFactorBackup()` → `useAuth().verifyTwoFactorBackup()`
   - `loginWithEmail2FA()` → `useAuth().loginWithEmail2FA()`
   - `fetchWithAuth()` → `apiClient` mit automatischem Token-Refresh

3. **Beibehaltung der Store-Schnittstelle** für Kompatibilität:
   - Store-Methoden werden zu Wrappern um Composables
   - Store-State bleibt erhalten für globale Auth-Informationen

#### **Notification Store Migration:**
1. **Erstellen von `useNotifications` Composable** (falls nicht existiert)
2. **Migration von `getVapidPublicKey()`** → `useNotifications().getVapidPublicKey()`

### **Phase 2: Seiten-Migration (Priorität: Mittel)**
**Ziel:** Ersetzen von Store-Aufrufen in Seiten durch direkte Composable-Nutzung

#### **Priorisierungsmatrix:**
| Priorität | Seiten | Begründung |
|-----------|--------|------------|
| **Hoch** | `login.vue`, `register.vue`, `verify-2fa.vue` | Direkte Auth-Interaktion, kritischer Pfad |
| **Mittel** | `teams/[id]/index.vue`, `teams/[id]/edit.vue` | Team-Management, wichtige Funktionen |
| **Niedrig** | `index.vue`, `about.vue` | Statische Seiten, weniger API-Aufrufe |

#### **Migrationsmuster für Seiten:**
```typescript
// Vorher (Store-basiert)
const authStore = useAuthStore()
await authStore.loginWithEmail(credentials)

// Nachher (Composable-basiert)
const { loginWithEmail, isLoading, error } = useAuth()
await loginWithEmail(credentials)
```

### **Phase 3: Komponenten-Migration (Priorität: Niedrig)**
**Ziel:** Ersetzen von Store-Aufrufen in Komponenten durch Composables

#### **Betroffene Komponenten:**
- `organisms/auth/*.vue` - Auth-Formulare
- `organisms/teams/*.vue` - Team-Komponenten
- `organisms/projects/*.vue` - Projekt-Komponenten
- `organisms/hackathons/*.vue` - Hackathon-Komponenten

## 3. Technische Implementierungsdetails

### **Auth Store Refactoring-Ansatz:**

#### **Option A: Hybrid-Ansatz (Empfohlen)**
- Store bleibt als State-Container erhalten
- Store-Methoden delegieren an Composables
- Keine Breaking Changes für bestehende Komponenten

```typescript
// auth-refactored.ts
export const useAuthStore = defineStore('auth', () => {
  // State bleibt gleich
  const token = ref<string | null>(null)
  const user = ref<User | null>(null)
  
  // Composable-Instanz
  const authComposable = useAuth()
  
  // Store-Methoden als Wrapper
  async function loginWithEmail(credentials: LoginCredentials) {
    const result = await authComposable.loginWithEmail(credentials)
    if (result.success) {
      token.value = result.access_token
      user.value = result.user
    }
    return result
  }
  
  return { token, user, loginWithEmail, ...authComposable }
})
```

#### **Option B: Vollständige Migration**
- Store wird durch Composables ersetzt
- Erfordert Änderungen in allen Komponenten
- Bessere Langzeit-Architektur

### **API-Client Integration:**
- **Bestehender `apiClient`** wird von Composables verwendet
- **Token-Refresh-Logik** wird in `apiClient` integriert
- **Error-Handling** wird zentralisiert

## 4. Migrationsplan (Zeitliche Abfolge)

### **Woche 1: Foundation & Auth Store**
1. **Tag 1-2:** Auth Store Refactoring (Hybrid-Ansatz)
   - Erstellen von `auth-refactored.ts`
   - Migration der kritischen Auth-Methoden
   - Testing der Auth-Funktionalität

2. **Tag 3-4:** Notification Store Migration
   - Erstellen von `useNotifications` Composable
   - Migration des Notification Stores
   - Testing der Push-Notifications

### **Woche 2: Seiten-Migration (High-Priority)**
3. **Tag 5-7:** Auth-bezogene Seiten
   - `login.vue`, `register.vue`, `verify-2fa.vue`
   - Testing aller Auth-Flows

4. **Tag 8-10:** Team-bezogene Seiten
   - `teams/[id]/index.vue`, `teams/[id]/edit.vue`
   - Testing der Team-Funktionalität

### **Woche 3: Seiten-Migration (Medium-Priority)**
5. **Tag 11-13:** Projekt-bezogene Seiten
   - `projects/[id]/index.vue`, `projects/create.vue`
   - Testing der Projekt-Funktionalität

6. **Tag 14-15:** Hackathon-bezogene Seiten
   - `hackathons/[id]/index.vue`, `hackathons/create.vue`
   - Testing der Hackathon-Funktionalität

### **Woche 4: Komponenten & Abschluss**
7. **Tag 16-18:** Komponenten-Migration
   - High-Usage-Komponenten zuerst
   - Testing nach jeder Migration

8. **Tag 19-20:** Testing & Validierung
   - End-to-End-Tests aller Flows
   - Performance-Testing
   - Bug-Fixing

9. **Tag 21:** Dokumentation & Code-Review
   - Vollständige Dokumentation
   - Code-Review vor Merge

## 5. Testing-Strategie

### **Unit Tests:**
- Jedes Composable hat eigene Tests
- Store-Wrapper werden getestet
- API-Client-Tests für Error-Handling

### **Integration Tests:**
- Seiten-Komponenten mit Composables
- Auth-Flows (Login, Register, 2FA)
- CRUD-Operationen (Teams, Projekte, Hackathons)

### **End-to-End Tests:**
- Cypress für kritische User-Journeys
- Testing aller migrierten Seiten
- Cross-Browser Testing

### **Performance Tests:**
- Bundle-Size-Analyse vor/nach Migration
- Ladezeiten-Vergleich
- Memory-Usage-Monitoring

## 6. Risikoanalyse und Fallback-Strategie

### **Identifizierte Risiken:**
1. **Breaking Changes:** Komponenten, die direkt auf Store-Interna zugreifen
2. **TypeScript-Kompatibilität:** Unterschiedliche Rückgabetypen zwischen Store und Composable
3. **Race Conditions:** Parallele API-Aufrufe mit unterschiedlichen Implementierungen
4. **Token-Refresh-Logik:** Komplexe Auth-Logik könnte unterbrochen werden

### **Fallback-Strategien:**
1. **Feature Flags:** Möglichkeit zur Rückkehr zur alten Implementierung
2. **Parallel-Betrieb:** Beide Implementierungen verfügbar während Migration
3. **Rollback-Plan:** Schnelle Rückkehr zum vorherigen Zustand bei kritischen Fehlern
4. **Staged Rollout:** Migration in kleinen, testbaren Schritten

### **Monitoring:**
- **Error-Logging:** Erweiterte Error-Tracking für migrierte Komponenten
- **Performance-Monitoring:** Ladezeiten und API-Latenz
- **User-Feedback:** Frühes Feedback von Test-Usern

## 7. Erfolgskriterien

### **Technische Kriterien:**
- ✅ Keine direkten `fetch`-Aufrufe in Stores
- ✅ Alle Seiten verwenden Composables für API-Interaktionen
- ✅ TypeScript-Fehlerfreiheit
- ✅ Bundle-Size nicht signifikant erhöht
- ✅ Performance gleich oder besser als vorher

### **Funktionale Kriterien:**
- ✅ Alle bestehenden Features funktionieren
- ✅ Auth-Flows (Login, Register, 2FA) funktionieren
- ✅ CRUD-Operationen (Teams, Projekte, Hackathons) funktionieren
- ✅ Error-Handling konsistent und benutzerfreundlich

### **Qualitätskriterien:**
- ✅ Vollständige Testabdeckung für migrierte Komponenten
- ✅ Dokumentation aller Änderungen
- ✅ Code-Review abgeschlossen
- ✅ Keine Regressionen in bestehenden Tests

## 8. Nächste Schritte

### **Unmittelbare Aktionen:**
1. **Auth Store Refactoring beginnen** - Erstellen der hybriden Store-Version
2. **Testing-Infrastruktur vorbereiten** - Unit Tests für Composables
3. **Migrations-Tracking implementieren** - Dokumentation des Fortschritts

### **Langfristige Planung:**
1. **Composable-Erweiterungen** - Weitere Composables für spezielle Use Cases
2. **TypeScript-Verbesserungen** - Striktere Typen und bessere IntelliSense
3. **Performance-Optimierungen** - Caching-Strategien für Composables
4. **Developer Experience** - Better Tooling und Dokumentation für Composables

---

**Letzte Aktualisierung:** 2026-03-10  
**Status:** Strategie erstellt, Implementierung beginnt mit Auth Store Refactoring  
**Verantwortlich:** Entwicklungsteam  
**Nächster Meilenstein:** Auth Store Migration abgeschlossen (geplant: 2026-03-12)