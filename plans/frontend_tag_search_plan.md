# Frontend-Änderungen für Tag-Suche

## 1. Projekt-Detailseite (`/projects/[id]/index.vue`)

### Aktuelle Situation:
- Technologien werden als nicht-klickbare `<span>`-Elemente angezeigt (Zeilen 122-129)
- `projectTechnologies` ist ein computed property, das `project.technologies` in ein Array aufteilt

### Änderungen:
1. **Tags klickbar machen**:
   - `<span>` durch `<NuxtLink>` ersetzen
   - Link-Ziel: `/projects?technology=${encodeURIComponent(tech)}`
   - Styling beibehalten, aber mit Hover-Effekt für Interaktivität

2. **Code-Änderung**:
```vue
<!-- Vorher: -->
<span 
  v-for="tech in projectTechnologies" 
  :key="tech"
  class="px-4 py-2 bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-300 rounded-lg text-sm font-medium"
>
  {{ tech }}
</span>

<!-- Nachher: -->
<NuxtLink
  v-for="tech in projectTechnologies" 
  :key="tech"
  :to="`/projects?technology=${encodeURIComponent(tech)}`"
  class="px-4 py-2 bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-300 rounded-lg text-sm font-medium hover:bg-primary-200 dark:hover:bg-primary-800 transition-colors"
>
  {{ tech }}
</NuxtLink>
```

3. **Eventuell Tooltip hinzufügen**: "Click to search for projects with this technology"

## 2. Projekte-Listenseite (`/projects/index.vue`)

### Aktuelle Situation:
- Clientseitige Filterung mit `selectedTags`
- URL-Parameter werden nicht verwendet
- Suchlogik in `filteredProjects` computed property

### Änderungen:
1. **URL-Parameter unterstützen**:
   - `technology`-Query-Parameter aus der URL lesen
   - Bei Vorhandensein automatisch zu `selectedTags` hinzufügen
   - URL bei Änderung von `selectedTags` aktualisieren

2. **Composition API Updates**:
```typescript
const route = useRoute()
const router = useRouter()

// Initialisiere selectedTags aus URL-Parametern
const selectedTags = ref<string[]>([])
if (route.query.technology) {
  const tech = Array.isArray(route.query.technology) 
    ? route.query.technology[0] 
    : route.query.technology
  selectedTags.value = [tech]
}

// Watch selectedTags und update URL
watch(selectedTags, (newTags) => {
  const query: any = { ...route.query }
  if (newTags.length > 0) {
    query.technology = newTags[0] // Einzelner Tag für jetzt
  } else {
    delete query.technology
  }
  router.replace({ query })
})

// Watch route changes um selectedTags zu synchronisieren
watch(() => route.query.technology, (tech) => {
  if (tech && !selectedTags.value.includes(tech as string)) {
    selectedTags.value = [tech as string]
  } else if (!tech && selectedTags.value.length > 0) {
    selectedTags.value = []
  }
})
```

3. **Backend-Integration**:
   - Aktuelle clientseitige Filterung durch Backend-API-Aufruf ersetzen
   - Bei `selectedTags`-Änderung API mit `technology`-Parameter aufrufen
   - Loading-State und Error-Handling hinzufügen

4. **API-Aufruf**:
```typescript
const { data: projects, pending, refresh } = await useFetch('/api/v1/projects', {
  query: {
    technology: selectedTags.value.length > 0 ? selectedTags.value[0] : undefined,
    limit: 50
  },
  baseURL: 'http://localhost:8000' // Backend-URL
})
```

## 3. Komponenten-Refactoring

### `TagBadge`-Komponente erstellen:
Wiederverwendbare Komponente für klickbare Tags in gesamter App.

```vue
<!-- components/TagBadge.vue -->
<template>
  <NuxtLink
    :to="`/projects?technology=${encodeURIComponent(tag)}`"
    class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium transition-colors"
    :class="[
      variant === 'primary' 
        ? 'bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-300 hover:bg-primary-200 dark:hover:bg-primary-800'
        : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
    ]"
  >
    <slot>{{ tag }}</slot>
  </NuxtLink>
</template>

<script setup lang="ts">
defineProps<{
  tag: string
  variant?: 'primary' | 'secondary'
}>()
</script>
```

## 4. Internationalisierung (i18n)

Neue Übersetzungen hinzufügen:
- `projects.detail.technologyClickHint`: "Click to search for projects with this technology"
- `projects.filter.activeTechnologyFilter`: "Filtering by technology: {technology}"

## 5. UX-Verbesserungen

1. **Breadcrumb/Navigation**: Bei aktivem Filter anzeigen
2. **Clear Filter Button**: Deutlicher Button zum Entfernen des Filters
3. **Empty State**: Angepasste Meldung bei keinen Ergebnissen
4. **Loading Indicators**: Bei Backend-Suche Loading-Spinner anzeigen

## 6. Testfälle

1. Klick auf Tag in Projekt-Detailseite navigiert zur Listenseite mit Filter
2. URL-Parameter werden korrekt gesetzt
3. Filter kann über URL geteilt werden
4. Clear Filter funktioniert
5. Mehrere Tags kombinieren (spätere Iteration)

## 7. Abhängigkeiten

- `vue-router` und `nuxt` bereits vorhanden
- Keine neuen Pakete erforderlich
- Backend-API muss verfügbar sein