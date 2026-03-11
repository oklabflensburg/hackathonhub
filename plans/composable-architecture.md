# Architektur für Vue Composables

## Grundprinzipien

### 1. Single Responsibility
Jedes Composable ist für einen spezifischen Domänenbereich oder API-Endpunkt verantwortlich.

### 2. Reaktiver State
- Verwende `ref` für primitive Werte und Objektreferenzen
- Verwende `reactive` für komplexe Objektzustände
- Verwende `computed` für abgeleitete Werte

### 3. Error-Handling
- Konsistente Error-Objekte
- User-friendly Error-Messages
- Automatisches Logging

### 4. Loading States
- Loading-Indikatoren für alle asynchronen Operationen
- Verhindern von doppelten Requests

### 5. Type Safety
- Vollständige TypeScript-Typen
- Generics für flexible Rückgabetypen

## Composable-Template

```typescript
import { ref, computed, reactive } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'

interface UseResourceOptions {
  // Optionale Konfiguration
}

interface Resource {
  // Typdefinitionen
}

export function useResource(options: UseResourceOptions = {}) {
  // Stores
  const authStore = useAuthStore()
  const uiStore = useUIStore()

  // State
  const data = ref<Resource[]>([])
  const current = ref<Resource | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const isEmpty = computed(() => data.value.length === 0)
  const hasError = computed(() => error.value !== null)

  // Methods
  const fetchAll = async (params?: Record<string, any>) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await authStore.fetchWithAuth('/api/resource', {
        params
      })
      
      if (!response.ok) {
        throw new Error(`Failed to fetch: ${response.statusText}`)
      }
      
      data.value = await response.json()
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error'
      uiStore.showError('Failed to load resource')
      console.error('Error fetching resource:', err)
    } finally {
      loading.value = false
    }
  }

  const create = async (resourceData: Partial<Resource>) => {
    // Ähnliche Implementierung
  }

  const update = async (id: string, updates: Partial<Resource>) => {
    // Ähnliche Implementierung
  }

  const remove = async (id: string) => {
    // Ähnliche Implementierung
  }

  // Return public API
  return {
    // State
    data,
    current,
    loading,
    error,
    
    // Computed
    isEmpty,
    hasError,
    
    // Methods
    fetchAll,
    create,
    update,
    remove,
    
    // Utilities
    reset: () => {
      data.value = []
      current.value = null
      error.value = null
    }
  }
}
```

## API-Client Abstraktion

Um Code-Duplikation zu vermeiden, erstellen wir einen zentralen API-Client:

```typescript
// app/utils/api-client.ts
import { useAuthStore } from '~/stores/auth'

export class ApiClient {
  private authStore = useAuthStore()

  async get<T>(url: string, options?: RequestInit): Promise<T> {
    return this.request<T>('GET', url, options)
  }

  async post<T>(url: string, body?: any, options?: RequestInit): Promise<T> {
    return this.request<T>('POST', url, { ...options, body: JSON.stringify(body) })
  }

  async put<T>(url: string, body?: any, options?: RequestInit): Promise<T> {
    return this.request<T>('PUT', url, { ...options, body: JSON.stringify(body) })
  }

  async delete<T>(url: string, options?: RequestInit): Promise<T> {
    return this.request<T>('DELETE', url, options)
  }

  private async request<T>(method: string, url: string, options?: RequestInit): Promise<T> {
    const response = await this.authStore.fetchWithAuth(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`)
    }

    return response.json()
  }
}

// Verwendung in Composables
const api = new ApiClient()
const data = await api.get<User[]>('/api/users')
```

## Composable-Kategorien

### 1. Authentication (`useAuth.ts`)
```typescript
interface UseAuth {
  // State
  user: Ref<User | null>
  isLoading: Ref<boolean>
  error: Ref<string | null>
  
  // Methods
  login: (credentials: LoginCredentials) => Promise<void>
  register: (credentials: RegisterCredentials) => Promise<void>
  logout: () => Promise<void>
  forgotPassword: (email: string) => Promise<void>
  resetPassword: (token: string, newPassword: string) => Promise<void>
  verifyEmail: (token: string) => Promise<void>
  refreshToken: () => Promise<void>
  
  // OAuth
  loginWithGoogle: (redirectUrl?: string) => Promise<void>
  loginWithGitHub: (redirectUrl?: string) => Promise<void>
  
  // 2FA
  verify2FA: (tempToken: string, code: string) => Promise<void>
  verify2FABackup: (tempToken: string, backupCode: string) => Promise<void>
}
```

### 2. User Management (`useUserProfile.ts`, `useUserStats.ts`)
```typescript
interface UseUserProfile {
  // State
  profile: Ref<UserProfile | null>
  stats: Ref<UserStats | null>
  
  // Methods
  fetchProfile: (userId?: string) => Promise<void>
  updateProfile: (updates: Partial<UserProfile>) => Promise<void>
  fetchStats: (userId?: string) => Promise<void>
  fetchUserTeams: (userId?: string) => Promise<Team[]>
}
```

### 3. File Upload (`useFileUpload.ts`)
```typescript
interface UseFileUpload {
  // State
  progress: Ref<number>
  isUploading: Ref<boolean>
  uploadedFile: Ref<File | null>
  
  // Methods
  upload: (file: File, options?: UploadOptions) => Promise<UploadResult>
  cancel: () => void
}
```

### 4. Newsletter (`useNewsletter.ts`)
```typescript
interface UseNewsletter {
  // State
  isSubscribed: Ref<boolean>
  isLoading: Ref<boolean>
  
  // Methods
  subscribe: (email: string) => Promise<void>
  unsubscribe: (email: string) => Promise<void>
  checkSubscription: (email: string) => Promise<boolean>
}
```

### 5. Push Notifications (`usePushNotifications.ts`)
```typescript
interface UsePushNotifications {
  // State
  isSupported: Ref<boolean>
  isSubscribed: Ref<boolean>
  vapidPublicKey: Ref<string | null>
  
  // Methods
  getVapidKey: () => Promise<string>
  subscribe: () => Promise<PushSubscription>
  unsubscribe: () => Promise<void>
  getSubscriptions: () => Promise<PushSubscription[]>
}
```

## Migrationsstrategie

### Schritt 1: Neue Composables erstellen
- Implementieren der fehlenden Composables
- Unit-Tests schreiben
- Dokumentation erstellen

### Schritt 2: Komponenten migrieren
- Identifizieren aller Komponenten mit direkten API-Aufrufen
- Schrittweise Migration zu Composables
- Jede Komponente einzeln testen

### Schritt 3: Store-Refactoring
- Auth-Store-Logik in `useAuth` auslagern
- Andere Stores überprüfen und ggf. migrieren

### Schritt 4: Konsolidierung
- Code-Review durchführen
- Performance optimieren
- Dokumentation aktualisieren

## Qualitätskriterien

### Code Coverage
- Mindestens 80% Testabdeckung für jedes Composable
- Unit-Tests für alle öffentlichen Methoden
- Integrationstests für API-Interaktionen

### Performance
- Keine unnötigen Re-Renderings
- Effiziente Caching-Strategien
- Debouncing bei häufigen Updates

### Wartbarkeit
- Klare Dokumentation
- Konsistente Namenskonventionen
- Regelmäßige Code-Reviews

## Erfolgsmetriken

1. **Keine direkten `fetch`-Aufrufe** in Vue-Komponenten
2. **Alle API-Endpunkte** durch Composables abgedeckt
3. **Konsistente Error-Handling** über alle Composables
4. **Verbesserte Developer Experience** durch wiederverwendbare Composables
5. **Reduzierte Code-Duplikation** um mindestens 40%