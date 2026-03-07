# Atomic Design Best Practices Guide

## Einführung

Dieser Leitfaden beschreibt die Best Practices für die Entwicklung und Wartung des Atomic Design Systems im Hackathon Dashboard. Die Einhaltung dieser Richtlinien gewährleistet Konsistenz, Wartbarkeit und Skalierbarkeit der Komponentenbibliothek.

## 1. Komponenten-Architektur

### 1.1 Atomic Design Ebenen

**Atoms** (Grundbausteine):
- Sollten keine Abhängigkeiten zu anderen Komponenten haben
- Maximale Wiederverwendbarkeit anstreben
- Keine Geschäftslogik enthalten

**Molecules** (Moleküle):
- Kombinieren 2-5 Atoms zu einer funktionalen Einheit
- Enthalten einfache Interaktionslogik
- Sollten kontextunabhängig sein

**Organisms** (Organismen):
- Kombinieren Molecules und/oder Atoms zu komplexen UI-Bereichen
- Dürfen Geschäftslogik enthalten
- Können kontextabhängig sein

**Templates** (Vorlagen):
- Definieren Seitenlayouts
- Platzieren Organisms in einem Raster/Layout
- Enthalten keine echten Daten

**Pages** (Seiten):
- Instanziieren Templates mit echten Daten
- Enthalten Seiten-spezifische Logik
- Sind routenabhängig

### 1.2 Dateistruktur

```
components/
├── atoms/
│   ├── Button.vue
│   ├── Icon.vue
│   └── Badge.vue
├── molecules/
│   ├── DateRangePicker.vue
│   └── FileUpload.vue
├── organisms/
│   ├── hackathons/
│   │   ├── ParticipantList.vue
│   │   └── PrizeList.vue
│   └── users/
│       └── UserProfile.vue
├── templates/
│   ├── HackathonDetailTemplate.vue
│   └── DashboardTemplate.vue
└── pages/
    ├── dashboard/
    │   └── index.vue
    └── hackathons/
        └── [id]/
            └── index.vue
```

## 2. Entwicklungspraktiken

### 2.1 TypeScript Integration

**Props Definition:**
```typescript
// ❌ Schlecht - Keine Typisierung
defineProps(['title', 'items', 'loading'])

// ✅ Gut - Mit TypeScript Interface
interface Props {
  title: string
  items: any[]
  loading: boolean
  variant?: 'primary' | 'secondary'
}

defineProps<Props>()
```

**Events Definition:**
```typescript
// ❌ Schlecht - Unklare Events
const emit = defineEmits(['click', 'update'])

// ✅ Gut - Typisierte Events
defineEmits<{
  (e: 'click', payload: MouseEvent): void
  (e: 'update:value', value: string): void
  (e: 'submit', data: FormData): void
}>()
```

### 2.2 Styling mit Tailwind CSS

**Konsistente Klassen:**
```vue
<template>
  <!-- ❌ Schlecht - Inkonsistente Klassen -->
  <button class="px-3 py-1.5 bg-blue-600 hover:bg-blue-700">
  
  <!-- ✅ Gut - Konsistente Klassen -->
  <button class="px-4 py-2 bg-primary-600 hover:bg-primary-700">
</template>
```

**Responsive Design:**
```vue
<template>
  <!-- ❌ Schlecht - Kein responsives Design -->
  <div class="w-64">
  
  <!-- ✅ Gut - Responsive Klassen -->
  <div class="w-full md:w-64 lg:w-80">
</template>
```

### 2.3 Slot Patterns

**Named Slots:**
```vue
<!-- Komponente -->
<template>
  <div class="card">
    <header v-if="$slots.header" class="card-header">
      <slot name="header" />
    </header>
    <div class="card-body">
      <slot />
    </div>
    <footer v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </footer>
  </div>
</template>

<!-- Verwendung -->
<Card>
  <template #header>
    <h2>Titel</h2>
  </template>
  <p>Inhalt</p>
  <template #footer>
    <Button>Action</Button>
  </template>
</Card>
```

**Scoped Slots:**
```vue
<!-- Komponente -->
<template>
  <ul>
    <li v-for="item in items" :key="item.id">
      <slot :item="item" :index="index" />
    </li>
  </ul>
</template>

<!-- Verwendung -->
<List :items="users">
  <template #default="{ item, index }">
    <UserCard :user="item" :index="index" />
  </template>
</List>
```

## 3. Performance Optimierung

### 3.1 Lazy Loading

```vue
<script setup>
// ❌ Schlecht - Alle Komponenten werden sofort geladen
import HeavyComponent from './HeavyComponent.vue'

// ✅ Gut - Lazy Loading für große Komponenten
const HeavyComponent = defineAsyncComponent(() =>
  import('./HeavyComponent.vue')
)
</script>
```

### 3.2 Memoization

```vue
<script setup>
import { computed } from 'vue'

const props = defineProps<{
  items: any[]
  filter: string
}>()

// ❌ Schlecht - Neuberechnung bei jedem Render
const filteredItems = () => {
  return props.items.filter(item => 
    item.name.includes(props.filter)
  )
}

// ✅ Gut - Computed Property mit Caching
const filteredItems = computed(() => {
  return props.items.filter(item => 
    item.name.includes(props.filter)
  )
})
</script>
```

### 3.3 Event Debouncing

```vue
<script setup>
import { ref, watch } from 'vue'
import { debounce } from 'lodash-es'

const searchQuery = ref('')
const results = ref([])

// ✅ Gut - Debouncing für Suchanfragen
const debouncedSearch = debounce(async (query) => {
  if (!query) {
    results.value = []
    return
  }
  
  results.value = await searchApi(query)
}, 300)

watch(searchQuery, debouncedSearch)
</script>
```

## 4. Testing Strategien

### 4.1 Test-Pyramide

```
        E2E Tests (10%)
           /      \
          /        \
 Integration Tests (20%)
        /            \
       /              \
   Unit Tests (70%)
```

### 4.2 Unit Tests für Atoms

```typescript
// Button.test.ts
import { mount } from '@vue/test-utils'
import Button from './Button.vue'

describe('Button', () => {
  it('renders with default variant', () => {
    const wrapper = mount(Button, {
      slots: { default: 'Click me' }
    })
    
    expect(wrapper.text()).toBe('Click me')
    expect(wrapper.classes()).toContain('btn-primary')
  })
  
  it('emits click event', async () => {
    const wrapper = mount(Button)
    
    await wrapper.trigger('click')
    
    expect(wrapper.emitted('click')).toHaveLength(1)
  })
})
```

### 4.3 Integration Tests für Organisms

```typescript
// ParticipantList.test.ts
import { mount } from '@vue/test-utils'
import ParticipantList from './ParticipantList.vue'

describe('ParticipantList', () => {
  it('displays loading state', () => {
    const wrapper = mount(ParticipantList, {
      props: {
        title: 'Participants',
        items: [],
        loading: true,
        loadingLabel: 'Loading...'
      }
    })
    
    expect(wrapper.text()).toContain('Loading...')
  })
  
  it('displays participants when loaded', async () => {
    const mockParticipants = [
      { id: 1, name: 'Team Alpha', open: true },
      { id: 2, name: 'Team Beta', open: false }
    ]
    
    const wrapper = mount(ParticipantList, {
      props: {
        title: 'Participants',
        items: mockParticipants,
        loading: false
      }
    })
    
    expect(wrapper.text()).toContain('Team Alpha')
    expect(wrapper.text()).toContain('Team Beta')
  })
})
```

## 5. Accessibility (A11y)

### 5.1 ARIA Labels

```vue
<template>
  <!-- ❌ Schlecht - Keine ARIA Labels -->
  <button @click="toggleMenu">
    <Icon name="menu" />
  </button>
  
  <!-- ✅ Gut - Mit ARIA Labels -->
  <button 
    @click="toggleMenu"
    aria-label="Toggle navigation menu"
    aria-expanded="isMenuOpen"
  >
    <Icon name="menu" />
  </button>
</template>
```

### 5.2 Keyboard Navigation

```vue
<script setup>
import { onMounted, ref } from 'vue'

const menuItems = ref([])
const focusedIndex = ref(-1)

// ✅ Gut - Keyboard Navigation implementieren
function handleKeydown(event) {
  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      focusedIndex.value = Math.min(
        focusedIndex.value + 1, 
        menuItems.value.length - 1
      )
      break
    case 'ArrowUp':
      event.preventDefault()
      focusedIndex.value = Math.max(focusedIndex.value - 1, 0)
      break
    case 'Enter':
    case ' ':
      if (focusedIndex.value >= 0) {
        selectItem(menuItems.value[focusedIndex.value])
      }
      break
  }
}
</script>
```

### 5.3 Focus Management

```vue
<template>
  <div 
    ref="container"
    tabindex="-1"
    @keydown="handleKeydown"
  >
    <!-- Focus-trapped content -->
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const container = ref()

// ✅ Gut - Focus innerhalb der Komponente halten
function trapFocus() {
  const focusableElements = container.value.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  )
  
  if (focusableElements.length > 0) {
    focusableElements[0].focus()
  }
}
</script>
```

## 6. Dokumentation

### 6.1 Komponenten-Dokumentation

```vue
<!--
/**
 * @name Button
 * @description A reusable button component with multiple variants and sizes.
 * 
 * @prop {string} variant - The button variant (primary, secondary, outline, ghost, danger)
 * @prop {string} size - The button size (xs, sm, md, lg)
 * @prop {boolean} disabled - Whether the button is disabled
 * @prop {boolean} loading - Shows a loading spinner
 * 
 * @event click - Emitted when the button is clicked
 * 
 * @slot default - The button content
 * 
 * @example
 * <Button variant="primary" size="md" @click="handleClick">
 *   Click me
 * </Button>
 */
-->
```

### 6.2 Storybook Stories

```typescript
// Button.stories.ts
import type { Meta, StoryObj } from '@storybook/vue3'
import Button from './Button.vue'

const meta: Meta<typeof Button> = {
  title: 'Atoms/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost', 'danger']
    },
    size: {
      control: 'select',
      options: ['xs', 'sm', 'md', 'lg']
    }
  }
}

export default meta

type Story = StoryObj<typeof Button>

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button'
  }
}

export const Loading: Story = {
  args: {
    variant: 'primary',
    loading: true,
    children: 'Loading...'
  }
}
```

## 7. Code Review Checkliste

### Vor dem Einreichen:
- [ ] TypeScript-Typen korrekt definiert
- [ ] Alle Props dokumentiert
- [ ] Events korrekt definiert
- [ ] Tailwind-Klassen konsistent
- [ ] Responsive Design implementiert
- [ ] Accessibility (ARIA) berücksichtigt
- [ ] Unit Tests geschrieben/aktualisiert
- [ ] Keine Console.logs im Produktionscode
- [ ] Keine unnötigen Abhängigkeiten
- [ ] Bundle Size überprüft

### Während des Reviews:
- [ ] Atomic Design Ebene eingehalten
- [ ] Wiederverwendbarkeit gewährleistet
- [ ] Performance optimiert
- [ ] Security Aspekte berücksichtigt
- [ ] Internationalisierung (i18n) unterstützt
- [ ] Dark Mode kompatibel
- [ ] Browser-Kompatibilität getestet

## 8. Troubleshooting

### Häufige Probleme:

**Problem:** Komponente wird nicht gerendert
**Lösung:** 
1. Prüfe TypeScript-Fehler in der Konsole
2. Überprüfe Prop-Typen
3. Stelle sicher, dass die Komponente registriert ist

**Problem:** Styling wird nicht angewendet
**Lösung:**
1. Prüfe Tailwind-Klassen auf Tippfehler
2. Stelle sicher, dass Tailwind korrekt konfiguriert ist
3. Überprüfe CSS-Spezifität

**Problem:** Events werden nicht ausgelöst
**Lösung:**
1. Prüfe Event-Definition mit `defineEmits`
2. Überprüfe Event-Handler in der Parent-Komponente
3. Stelle sicher, dass die Komponente nicht disabled ist

## 9. Weiterführende Ressourcen

### Dokumentation:
- [Vue 3 Documentation](https://vuejs.org/guide/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Atomic Design by Brad Frost](http://atomicdesign.bradfrost.com/)

### Tools:
- [Vue DevTools](https://devtools.vuejs.org/)
- [Storybook](https://storybook.js.org/)
- [Vitest](https://vitest.dev/)
- [Playwright](https://playwright.dev/)

### Community:
- [Vue.js Forum](https://forum.vuejs.org/)
- [Vue Discord](https://vue.land/discord)
- [Tailwind CSS Discord](https://tailwindcss.com/discord)

---

*Letzte Aktualisierung: März 2026*  
*Version: 1.0.0*  
*Autor: Hackathon Dashboard Development Team*