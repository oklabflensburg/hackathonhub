# Atomic Design System - Hackathon Dashboard

## Übersicht

Dieses Dokument beschreibt das Atomic Design System, das für das Hackathon Dashboard implementiert wurde. Das System folgt der Atomic Design Methodologie von Brad Frost, die Komponenten in fünf Ebenen unterteilt: **Atoms**, **Molecules**, **Organisms**, **Templates** und **Pages**.

## Struktur

```
frontend3/app/components/
├── atoms/              # Grundlegende UI-Elemente
├── molecules/          # Kombinationen von Atoms
├── organisms/          # Komplexe Komponenten aus Molecules/Atoms
├── templates/          # Seitenlayouts
└── pages/              # Vollständige Seiten
```

## Atoms (Grundbausteine)

Atoms sind die kleinsten, nicht weiter teilbaren UI-Elemente.

### Implementierte Atoms

1. **Icon** (`atoms/Icon.vue`)
   - SVG-Icons mit verschiedenen Größen und Farben
   - Unterstützt Lucide Icons (falls installiert) oder Fallback-SVG

2. **Skeleton** (`atoms/Skeleton.vue`)
   - Ladeanimationen für verschiedene Inhalte
   - Varianten: Text, Circle, Rectangle

3. **Alert** (`atoms/Alert.vue`)
   - Benachrichtigungen mit verschiedenen Varianten
   - Varianten: success, error, warning, info, neutral

4. **Tooltip** (`atoms/Tooltip.vue`)
   - Kontextuelle Hilfetexte
   - Positionierung: top, bottom, left, right

5. **ProgressBar** (`atoms/ProgressBar.vue`)
   - Fortschrittsanzeige mit Prozentangabe
   - Varianten: primary, success, warning, error

6. **Badge** (`atoms/Badge.vue`)
   - Status- und Kategorie-Badges
   - Varianten: primary, success, warning, error, neutral, outline

7. **Avatar** (`atoms/Avatar.vue`)
   - Benutzer- und Team-Avatare
   - Größen: xs, sm, md, lg, xl

8. **Button** (`atoms/Button.vue`)
   - Interaktive Schaltflächen
   - Varianten: primary, secondary, outline, ghost, danger
   - Größen: xs, sm, md, lg

9. **Card** (`atoms/Card.vue`)
   - Container für zusammengehörige Inhalte
   - Unterstützt Header, Body und Footer

10. **LoadingSpinner** (`atoms/LoadingSpinner.vue`)
    - Lade-Indikatoren
    - Größen: sm, md, lg

11. **HackathonDateDisplay** (`atoms/HackathonDateDisplay.vue`)
    - Spezialisiertes Atom für Hackathon-Datumsanzeige
    - Formatiert Start- und Enddaten

## Molecules (Moleküle)

Molecules sind Kombinationen von Atoms, die zusammen eine einfache Funktionalität bilden.

### Implementierte Molecules

1. **DateRangePicker** (`molecules/DateRangePicker.vue`)
   - Datumsbereichsauswahl für Hackathons
   - Validierung und Fehlerbehandlung

2. **FileUpload** (`molecules/FileUpload.vue`)
   - Datei-Upload mit Drag & Drop
   - Validierung von Dateitypen und -größen

3. **HackathonFilterBar** (`molecules/HackathonFilterBar.vue`)
   - Filterung von Hackathons nach Status
   - Kombination aus Button-Gruppe

4. **HackathonSearchInput** (`molecules/HackathonSearchInput.vue`)
   - Suchfunktion für Hackathons
   - Debouncing und Autocomplete

5. **HackathonSortOptions** (`molecules/HackathonSortOptions.vue`)
   - Sortieroptionen für Hackathon-Listen
   - Dropdown mit verschiedenen Kriterien

## Organisms (Organismen)

Organisms sind komplexe UI-Komponenten, die aus mehreren Molecules und/oder Atoms bestehen.

### Implementierte Organisms

1. **DashboardWidget** (`organisms/DashboardWidget.vue`)
   - Dashboard-Widget mit Titel, Inhalt und Aktionen
   - Unterstützt verschiedene Layouts

2. **UserProfileOrganism** (`organisms/UserProfileOrganism.vue`)
   - Komplette Benutzerprofilansicht
   - Kombiniert Avatar, Badges, Buttons und Statistiken

3. **NotificationCenter** (`organisms/NotificationCenter.vue`)
   - Benachrichtigungszentrale mit Filterung
   - Kombiniert Alert, Badge und Button-Komponenten

4. **ParticipantList** (`organisms/hackathons/ParticipantList.vue`)
   - Teilnehmerliste für Hackathons
   - Verwendet Card, Badge, Avatar, Button, Icon

5. **PrizeList** (`organisms/hackathons/PrizeList.vue`)
   - Preisliste für Hackathons
   - Verwendet Card, Badge, Icon, Button

6. **RulesSection** (`organisms/hackathons/RulesSection.vue`)
   - Regelsektion für Hackathons
   - Verwendet Card, Badge, Icon, Button mit Parser-Funktionalität

## Templates (Vorlagen)

Templates definieren das Seitenlayout und die Platzierung von Organisms.

### Implementierte Templates

1. **HackathonDetailTemplate** (`templates/HackathonDetailTemplate.vue`)
   - Layout für Hackathon-Detailseiten
   - Platzierung von Hero, Beschreibung, Preisen, Regeln

2. **HackathonListTemplate** (`templates/HackathonListTemplate.vue`)
   - Layout für Hackathon-Listen
   - Integration von Filter, Suche und Sortierung

3. **HackathonFormTemplate** (`templates/HackathonFormTemplate.vue`)
   - Layout für Hackathon-Formulare
   - Formularvalidierung und Datei-Upload

## Pages (Seiten)

Pages sind vollständige Seiten, die Templates mit echten Daten füllen.

### Beispielseite

1. **Dashboard** (`pages/dashboard/index.vue`)
   - Demonstrationsseite für Atomic Design Hierarchie
   - Verwendet alle Ebenen des Systems

## Best Practices

### 1. Komponenten-Wiederverwendung
- **Atoms** sollten maximal wiederverwendbar sein
- **Molecules** sollten eine spezifische, abgeschlossene Funktionalität bieten
- **Organisms** sollten kontextabhängig sein und Geschäftslogik enthalten

### 2. Props und Events
- Verwende TypeScript Interfaces für Props
- Definiere klare Events mit `defineEmits`
- Dokumentiere alle Props und Events im Komponenten-Kommentar

### 3. Styling
- Verwende Tailwind CSS für Styling
- Halte Komponenten stylistisch unabhängig
- Verwende CSS-Variablen für thematische Anpassungen

### 4. Testing
- Unit-Tests für Atoms und Molecules
- Integrationstests für Organisms
- E2E-Tests für Templates und Pages

### 5. Dokumentation
- Jede Komponente sollte einen JSDoc-Kommentar haben
- Beispiele für die Verwendung bereitstellen
- Props und Events dokumentieren

## Implementierungsbeispiel

### Atom (Button)
```vue
<template>
  <button
    :class="buttonClasses"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
defineProps<{
  variant: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size: 'xs' | 'sm' | 'md' | 'lg'
  disabled?: boolean
}>()

defineEmits<{
  (e: 'click'): void
}>()
</script>
```

### Molecule (DateRangePicker)
```vue
<template>
  <div class="date-range-picker">
    <Icon name="calendar" />
    <input :value="startDate" @input="updateStart" />
    <span>bis</span>
    <input :value="endDate" @input="updateEnd" />
    <Alert v-if="error" :variant="'error'" :message="error" />
  </div>
</template>
```

### Organism (ParticipantList)
```vue
<template>
  <section>
    <div class="header">
      <Icon name="users" />
      <h2>{{ title }}</h2>
      <Badge>{{ items.length }}</Badge>
    </div>
    
    <div v-for="team in items" :key="team.id">
      <Card>
        <Avatar :src="team.avatar" />
        <h3>{{ team.name }}</h3>
        <Badge :variant="team.open ? 'success' : 'neutral'">
          {{ team.open ? 'Open' : 'Closed' }}
        </Badge>
        <Button @click="viewTeam(team.id)">View</Button>
      </Card>
    </div>
  </section>
</template>
```

## Migration von Legacy-Komponenten

### Schritt 1: Identifizieren
- Analysiere bestehende Komponenten auf ihre Atomic Design Ebene
- Identifiziere Duplikate und Inkonsistenzen

### Schritt 2: Refactoring
1. Extrahiere Atoms aus komplexen Komponenten
2. Kombiniere Atoms zu Molecules
3. Baue Organisms aus bestehenden Molecules
4. Erstelle Templates für Seitenlayouts

### Schritt 3: Testing
- Teste jede neue Komponente isoliert
- Stelle sicher, dass bestehende Funktionen erhalten bleiben
- Führe Integrationstests durch

## Vorteile des Atomic Design Systems

1. **Konsistenz**: Einheitliches Erscheinungsbild über die gesamte Anwendung
2. **Wiederverwendbarkeit**: Komponenten können in verschiedenen Kontexten verwendet werden
3. **Wartbarkeit**: Einfacheres Debugging und Updates
4. **Skalierbarkeit**: Einfache Erweiterung des Systems
5. **Teamarbeit**: Klare Aufgabenteilung zwischen Designern und Entwicklern

## Nächste Schritte

1. **Komponenten-Bibliothek erweitern**
   - Weitere Atoms für spezielle Anwendungsfälle
   - Molecules für Formulare und Datenvisualisierung
   - Organisms für komplexe Geschäftslogik

2. **Design Tokens implementieren**
   - Zentrale Farbpalette
   - Typografie-System
   - Spacing-Skala

3. **Storybook Integration**
   - Visuelle Komponentendokumentation
   - Interaktive Beispiele
   - Automatisierte Tests

4. **Performance Optimierung**
   - Lazy Loading von Komponenten
   - Tree Shaking für ungenutzte Komponenten
   - Bundle Size Optimierung

## Kontakt und Support

Bei Fragen oder Problemen mit dem Atomic Design System:
- Dokumentation konsultieren
- Komponenten-Beispiele studieren
- Bei technischen Fragen das Entwicklungsteam kontaktieren

---

*Letzte Aktualisierung: März 2026*  
*Version: 1.0.0*  
*Autor: Hackathon Dashboard Development Team*