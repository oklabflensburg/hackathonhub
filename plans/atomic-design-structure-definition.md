# Atomic Design Struktur-Definition

## Überblick

Atomic Design ist eine Methodik zur Erstellung von Design-Systemen, die aus fünf verschiedenen Ebenen besteht:

1. **Atoms**: Grundlegende UI-Elemente (Buttons, Inputs, Labels, etc.)
2. **Molecules**: Kombinationen von Atoms, die zusammen eine einfache Funktion erfüllen
3. **Organisms**: Komplexe Komponenten aus Molecules und/oder Atoms
4. **Templates**: Seiten-Layouts ohne konkreten Inhalt
5. **Pages**: Konkrete Instanzen von Templates mit echten Inhalten

## Verzeichnisstruktur

```
frontend3/app/components/
├── atoms/                    # Grundlegende UI-Elemente
│   ├── Avatar.vue              (existiert)
│   ├── Button.vue              (zu erstellen)
│   ├── Card.vue                (existiert)
│   ├── Tag.vue                 (existiert)
│   ├── Input.vue               (zu erstellen)
│   ├── Textarea.vue            (zu erstellen)
│   ├── Select.vue              (zu erstellen)
│   ├── Checkbox.vue            (zu erstellen)
│   ├── Radio.vue               (zu erstellen)
│   ├── LoadingSpinner.vue      (zu erstellen)
│   ├── Icon.vue                (zu erstellen)
│   └── Badge.vue               (zu erstellen)
├── molecules/                # Einfache Kombinationen
│   ├── FormField.vue           (zu erstellen)
│   ├── FormSection.vue         (zu erstellen)
│   ├── SearchBar.vue           (zu erstellen)
│   ├── FilterGroup.vue         (zu erstellen)
│   ├── Pagination.vue          (zu erstellen)
│   ├── SocialLoginButtons.vue  (zu erstellen)
│   ├── FileUpload.vue          (zu erstellen)
│   ├── DateRangePicker.vue     (zu erstellen)
│   └── ToggleSwitch.vue        (zu erstellen)
├── organisms/                # Komplexe Komponenten
│   ├── CommentSection.vue      (zu erstellen)
│   ├── ProjectHeader.vue       (existiert in projects/)
│   ├── ProfileHeader.vue       (zu erstellen)
│   ├── NotificationPreferences.vue (zu erstellen)
│   ├── TeamManagement.vue      (zu erstellen)
│   ├── ProjectForm.vue         (zu erstellen)
│   ├── HackathonForm.vue       (zu erstellen)
│   └── UserSettingsForm.vue    (zu erstellen)
├── templates/                # Seiten-Layouts (optional)
│   ├── AuthLayout.vue          (zu erstellen)
│   ├── DashboardLayout.vue     (zu erstellen)
│   ├── FormLayout.vue          (zu erstellen)
│   └── DetailLayout.vue        (zu erstellen)
└── [domains]/               # Domänenspezifische Komponenten (können Organisms sein)
    ├── projects/               (existiert)
    ├── hackathons/             (existiert)
    ├── teams/                  (existiert)
    ├── users/                  (existiert)
    ├── invitations/            (existiert)
    └── home/                   (existiert)
```

## Komponenten-Spezifikationen

### Atoms (Grundlegende UI-Elemente)

#### 1. Button.vue
```typescript
Props:
- variant: 'primary' | 'secondary' | 'danger' | 'ghost' | 'link'
- size: 'sm' | 'md' | 'lg'
- loading: boolean
- disabled: boolean
- fullWidth: boolean
- type: 'button' | 'submit' | 'reset'

Slots:
- default: Button text
- icon: Icon vor/nach Text
```

#### 2. Input.vue
```typescript
Props:
- type: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url'
- modelValue: string | number
- placeholder: string
- disabled: boolean
- readonly: boolean
- error: string | boolean
- success: string | boolean

Events:
- update:modelValue
- focus, blur, input, change
```

#### 3. LoadingSpinner.vue
```typescript
Props:
- size: 'sm' | 'md' | 'lg' | 'xl' | number
- color: string (CSS color)
- thickness: number (px)
```

### Molecules (Einfache Kombinationen)

#### 1. FormField.vue
```typescript
Props:
- label: string
- required: boolean
- error: string
- help: string
- id: string

Slots:
- default: Input/Select/Textarea etc.
- label: Custom label
- help: Custom help text
```

#### 2. SearchBar.vue
```typescript
Props:
- placeholder: string
- debounce: number (ms)
- modelValue: string

Events:
- update:modelValue
- search: (query: string) => void

Composition:
- Input Atom
- Icon Atom (Search)
- Button Atom (Clear)
```

#### 3. Pagination.vue
```typescript
Props:
- total: number
- perPage: number
- currentPage: number
- showNumbers: boolean
- showPrevNext: boolean

Events:
- page-change: (page: number) => void
```

### Organisms (Komplexe Komponenten)

#### 1. CommentSection.vue
```typescript
Props:
- comments: Comment[]
- loading: boolean
- error: string
- projectId: number | string
- currentUserId: number | string

Events:
- comment-added: (comment: Comment) => void
- comment-updated: (comment: Comment) => void
- comment-deleted: (commentId: number) => void

Composition:
- CommentItem (Molecule)
- CommentForm (Molecule)
- ReplyThread (Organism)
- useComments Composable
```

#### 2. ProjectForm.vue
```typescript
Props:
- project: Project (für Bearbeitung)
- loading: boolean

Events:
- submit: (projectData: ProjectFormData) => void
- cancel: () => void

Composition:
- FormField Molecules
- Input/Textarea/Select Atoms
- FileUpload Molecule
- TechnologyTags Component
```

### Domänenspezifische Komponenten

Existierende Komponenten werden in die Atomic Design-Hierarchie eingeordnet:

#### Atoms (in domains/)
- `projects/TechnologyTags.vue` → Eigentlich ein Molecule (Tag-Liste)
- `projects/ProjectLinks.vue` → Molecule (Link-Liste)

#### Molecules (in domains/)
- `projects/ProjectStats.vue` → Molecule (Statistik-Karten)
- `projects/CreatorInfo.vue` → Molecule (Avatar + Info)
- `projects/ProjectActions.vue` → Molecule (Button-Gruppe)

#### Organisms (in domains/)
- `projects/ProjectHeader.vue` → Organism (komplexe Header-Komponente)
- `hackathons/HackathonHero.vue` → Organism (Hero-Bereich)
- `teams/TeamDetailHeader.vue` → Organism

## Implementierungsrichtlinien

### 1. Props-Konventionen
- Verwende `kebab-case` für Prop-Namen im Template
- Verwende `camelCase` für Prop-Namen in TypeScript
- Definiere explizite Typen für alle Props
- Setze sinnvolle Default-Werte

### 2. Events-Konventionen
- Verwende `kebab-case` für Event-Namen
- Präfixe: `update:` für Two-Way Binding, `@` für Aktionen
- Beispiele: `@submit`, `@cancel`, `update:modelValue`

### 3. Slots
- Verwende benannte Slots für komplexe Strukturen
- `default` Slot für Hauptinhalt
- Benannte Slots für spezifische Bereiche: `header`, `footer`, `actions`

### 4. Styling
- Tailwind CSS für Utility-Klassen
- Scoped Styles für komponentenspezifisches Styling
- CSS Custom Properties für thematische Werte
- Dark Mode unterstützung via `dark:` Präfix

### 5. TypeScript
- Definiere Interfaces für Props und Events
- Verwende `defineProps` und `defineEmits` mit TypeScript
- Exportiere Typen für Wiederverwendung

### 6. Komposition
- Extrahiere Logik in Composable Functions
- Verwende `provide/inject` für tief verschachtelte Komponenten
- Vermeide prop drilling über mehr als 2 Ebenen

## Migrationsstrategie

### Phase 1: Foundation
1. Erstelle fehlende Atoms (`Button`, `Input`, `LoadingSpinner`)
2. Erstelle `molecules/` und `organisms/` Verzeichnisse
3. Migriere existierende Komponenten in die richtige Hierarchie

### Phase 2: Kritische Organisms
1. Erstelle `CommentSection` Organism
2. Erstelle `ProjectForm` Organism
3. Erstelle `ProfileHeader` Organism

### Phase 3: Seiten-Refactoring
1. Refaktoriere Projekt-Detailseite mit neuen Komponenten
2. Refaktoriere Profilseite
3. Refaktoriere Erstellungsseiten

### Phase 4: Vereinheitlichung
1. Standardisiere alle Formulare mit `FormField` Molecules
2. Vereinheitliche Listen-Komponenten
3. Implementiere konsistente Error-Handling

## Qualitätskriterien

### Für jede neue Komponente:
- [ ] TypeScript-Typen definiert
- [ ] Props und Events dokumentiert
- [ ] Unit-Test vorhanden
- [ ] Responsive Design getestet
- [ ] Dark Mode unterstützt
- [ ] Accessibility (ARIA) implementiert
- [ ] Internationalisierung (i18n) berücksichtigt

### Für Refactored Seiten:
- [ ] Reduzierung der Zeilenanzahl um mindestens 50%
- [ ] Keine Regressionen in Funktionalität
- [ ] Verbesserte Performance (Bundle Size, Ladezeit)
- [ ] Bessere Testbarkeit

## Nächste Schritte

1. Erstelle die fehlenden Basis-Atoms (`Button`, `Input`, `LoadingSpinner`)
2. Beginne mit dem `CommentSection` Organism für die Projekt-Detailseite
3. Refaktoriere schrittweise die Projekt-Detailseite
4. Überprüfe nach jedem Schritt die Funktionalität