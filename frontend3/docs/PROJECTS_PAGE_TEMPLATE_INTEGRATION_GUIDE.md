# ProjectsPageTemplate Integration Guide

## Übersicht

Die `ProjectsPageTemplate`-Integration ermöglicht die Verwendung von Atomic Design Komponenten für Projekt-Listen-Seiten. Diese Anleitung dokumentiert die Integration der `ProjectsPageTemplate` in die bestehende Hackathon-Projektliste.

## Implementierte Komponenten

### 1. ProjectListAtomicWrapper.vue

**Pfad:** `frontend3/app/components/projects/ProjectListAtomicWrapper.vue`

**Zweck:** Wrapper-Komponente, die zwischen Legacy- und Atomic-Design-Version umschaltet basierend auf Feature-Flags.

**Funktionen:**
- Automatische Umschaltung basierend auf `atomicProjectComponents` Feature-Flag
- Datenkonvertierung zwischen Legacy- und Atomic-Design-Formaten
- Event-Handler-Propagation zwischen beiden Systemen
- Slots für benutzerdefinierte Inhalte

**Props-Schnittstelle:**
```typescript
interface Props {
  // Page Configuration
  pageTitle?: string
  pageDescription?: string
  
  // Data
  projects: any[] // Legacy project format
  loading?: boolean
  error?: string | null
  totalItems?: number
  itemsPerPage?: number
  
  // Configuration Flags
  showHeader?: boolean
  showHeaderActions?: boolean
  showSearch?: boolean
  showCreateButton?: boolean
  showViewControls?: boolean
  showViewToggle?: boolean
  showSort?: boolean
  showFilters?: boolean
  showProjectFilters?: boolean
  showAdditionalFilters?: boolean
  showPagination?: boolean
  showFooter?: boolean
  
  // User Permissions
  canCreate?: boolean
  
  // View Configuration
  defaultViewMode?: 'grid' | 'list'
  gridColumns?: number
  
  // Empty State
  emptyMessage?: string
  
  // Layout Variant
  variant?: 'default' | 'sidebar-left' | 'sidebar-right' | 'full-width'
  
  // Feature Flag Override
  forceAtomic?: boolean
  forceLegacy?: boolean
}
```

### 2. Hackathon-Projektliste Integration

**Pfad:** `frontend3/app/pages/hackathons/[id]/projects.vue`

**Änderungen:**
1. **Wrapper-Integration:** Ersetzung des direkten `ProjectListOrganism` durch `ProjectListAtomicWrapper`
2. **Datenfluss:** Beibehaltung der bestehenden Datenfetching- und Transformationslogik
3. **Event-Handler:** Mapping von Atomic-Design-Events zu bestehenden Funktionen
4. **Fallback:** Legacy-Version bleibt im Default-Slot für Feature-Flag-Deaktivierung

**Wichtige Integrationspunkte:**
- Projektdaten werden automatisch von Legacy- zu Atomic-Format konvertiert
- Event-Handler (`handleSearch`, `handleSubmitProject`, etc.) werden propagiert
- Feature-Flag-Steuerung über `useFeatureFlags().isEnabled('atomicProjectComponents')`

## Datenkonvertierung

### Legacy zu Atomic Format
```typescript
// Legacy Projekt-Format (bestehendes System)
{
  id: number,
  name: string,
  title: string,
  description: string,
  image: string,
  status: string,
  team: any[],
  techStack: string[],
  votes: number,
  comments: number,
  views: number,
  hasVoted: boolean,
  owner_id: number,
  hackathon_id: number
}

// Atomic Design Projekt-Format (neues System)
{
  id: string,
  title: string,
  slug: string,
  description: string,
  status: ProjectStatus,
  visibility: ProjectVisibility,
  featuredImage: string,
  team: ProjectTeamMember[],
  technologies: ProjectTechnology[],
  tags: ProjectTag[],
  stats: ProjectStats,
  userVote: 1 | -1 | null,
  isBookmarked: boolean,
  // ... weitere Felder
}
```

### Konvertierungsfunktionen
- `convertLegacyProjectToAtomic()`: Wandelt Legacy-Projekte in Atomic-Design-Format um
- `convertAtomicProjectToLegacy()`: Wandelt Atomic-Projekte zurück in Legacy-Format
- `mapLegacyStatusToProjectStatus()`: Mappt Legacy-Status zu ProjectStatus Enum
- `mapLegacyTechStackToTechnologies()`: Konvertiert Tech-Stack-Arrays zu ProjectTechnology-Objekten

## Feature-Flag-Steuerung

### Aktivierung/Deaktivierung
```typescript
// Feature-Flag prüfen
const { isEnabled } = useFeatureFlags()
const useAtomicComponents = isEnabled('atomicProjectComponents')

// Manuelle Überschreibung (für Testing)
<ProjectListAtomicWrapper :force-atomic="true" ... />
<ProjectListAtomicWrapper :force-legacy="true" ... />
```

### Feature-Flag-Konfiguration
```typescript
// frontend3/app/config/feature-flags.ts
export const featureFlags = {
  atomicProjectComponents: true, // Aktiviert für sofortige Nutzung
  // ... andere Flags
}
```

## Event-Handler-Mapping

| Atomic-Design Event | Legacy Handler | Zweck |
|---------------------|----------------|-------|
| `@search` | `handleSearch` | Suchanfrage verarbeiten |
| `@create` | `handleSubmitProject` | Projekt erstellen |
| `@sort-change` | `handleSortChange` | Sortierung ändern |
| `@project-click` | `viewProject` | Projekt anzeigen |
| `@project-vote` | `handleProjectVote` | Projekt bewerten |
| `@project-comment` | `handleProjectComment` | Kommentar hinzufügen |
| `@project-share` | `handleProjectShare` | Projekt teilen |
| `@retry` | `fetchProjects` | Daten neu laden |

## Responsive Design

Die `ProjectsPageTemplate` unterstützt verschiedene Layout-Varianten:

### Verfügbare Varianten
- **`default`**: Standard-Layout mit Sidebar-Filtern
- **`sidebar-left`**: Filter-Sidebar links
- **`sidebar-right`**: Filter-Sidebar rechts  
- **`full-width`**: Volle Breite ohne Sidebar (für Hackathon-Projektliste verwendet)

### Responsive Features
- Mobile-first Design
- Adaptive Grid/List-Ansicht
- Responsive Filter-Sidebar
- Touch-optimierte Interaktionen

## Testing

### Manuelles Testing
1. **Feature-Flag aktiviert:** `atomicProjectComponents: true`
   - Atomic-Design-Version sollte angezeigt werden
   - Alle Funktionen sollten arbeiten (Suche, Sortierung, etc.)
   - Responsive Design sollte korrekt funktionieren

2. **Feature-Flag deaktiviert:** `atomicProjectComponents: false`
   - Legacy-Version sollte angezeigt werden
   - Bestehende Funktionalität sollte unverändert bleiben

### Automatisches Testing (TODO)
- Unit Tests für Datenkonvertierung
- Integration Tests für Event-Handler
- E2E Tests für Benutzerinteraktionen

## Performance Considerations

### Vorteile
1. **Lazy Loading:** Atomic-Komponenten können dynamisch importiert werden
2. **Tree Shaking:** Unbenutzte Komponenten werden aus dem Bundle entfernt
3. **Caching:** Atomic-Komponenten können besser gecached werden
4. **Wiederverwendbarkeit:** Komponenten können in anderen Kontexten genutzt werden

### Optimierungen
- Code-Splitting für große Komponenten
- Memoization für teure Berechnungen
- Debouncing für Such- und Filter-Events

## Migration Path

### Phase 1: Integration (Abgeschlossen)
- ✅ `ProjectListAtomicWrapper` erstellt
- ✅ Hackathon-Projektliste integriert
- ✅ Datenkonvertierung implementiert
- ✅ Feature-Flag-Steuerung eingerichtet

### Phase 2: Testing (In Progress)
- [ ] Manuelle Testing der Integration
- [ ] Performance-Messungen
- [ ] Benutzer-Feedback sammeln

### Phase 3: Rollout
- [ ] Feature-Flag für alle Benutzer aktivieren
- [ ] Monitoring von Fehlern und Performance
- [ ] Legacy-Code entfernen (optional)

### Phase 4: Erweiterung
- [ ] Weitere Projekt-Listen-Seiten migrieren
- [ ] Atomic-Komponenten optimieren
- [ ] Neue Features hinzufügen

## Troubleshooting

### Häufige Probleme

1. **TypeScript-Fehler bei Props**
   ```bash
   # Fehler: Type 'boolean' is not assignable to type 'any[]'
   # Lösung: v-bind Syntax verwenden statt einzelner Props
   <ProjectListAtomicWrapper v-bind="{ showFilters: false, ... }" />
   ```

2. **Datenkonvertierungsfehler**
   ```typescript
   // Prüfen Sie die Datenstruktur
   console.log('Legacy project:', legacyProject)
   console.log('Atomic project:', convertLegacyProjectToAtomic(legacyProject))
   ```

3. **Feature-Flag funktioniert nicht**
   ```typescript
   // Feature-Flag prüfen
   console.log('atomicProjectComponents enabled:', 
     useFeatureFlags().isEnabled('atomicProjectComponents'))
   
   // Config prüfen
   import { featureFlags } from '~/config/feature-flags'
   console.log('Feature flags:', featureFlags)
   ```

### Debugging
```typescript
// Debug-Logging aktivieren
const debug = ref(false)

// In Wrapper-Komponente
watch(useAtomicComponents, (newVal) => {
  console.log('Atomic components enabled:', newVal)
  console.log('Projects count:', props.projects.length)
  console.log('Atomic projects:', atomicProjects.value.length)
})
```

## Nächste Schritte

### Kurzfristig
1. Weitere Projekt-Listen-Seiten identifizieren
2. Testing-Suite erweitern
3. Performance-Optimierungen implementieren

### Langfristig
1. Vollständige Migration aller Projekt-Komponenten
2. Atomic Design auf andere Bereiche ausweiten
3. Design System dokumentieren und standardisieren

## Referenzen

- [Atomic Design Methodology](https://atomicdesign.bradfrost.com/)
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [TypeScript with Vue](https://vuejs.org/guide/typescript/overview.html)
- [Feature Flag Best Practices](https://featureflags.io/feature-flag-best-practices/)

---

**Letzte Aktualisierung:** 2026-03-03  
**Status:** Phase 2 (Testing)  
**Verantwortlich:** Frontend Refactoring Team