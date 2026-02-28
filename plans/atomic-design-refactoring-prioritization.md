# Atomic Design Refactoring - Priorisierungsliste

## Bewertung des aktuellen Zustands

### Atomic Design Struktur (aktuell)
- ✅ **Atoms**: `Avatar.vue`, `Card.vue`, `Tag.vue` (existieren)
- ❌ **Molecules**: Kein dediziertes Verzeichnis
- ❌ **Organisms**: Kein dediziertes Verzeichnis  
- ✅ **Templates**: Seiten als Templates
- ✅ **Domänenkomponenten**: `projects/`, `hackathons/`, `teams/`, `users/`, `invitations/`, `home/`

### Seiten-Bewertung (nach Größe und Komplexität)

#### 1. Sehr große Seiten (> 30.000 Zeichen) - HOHE PRIORITÄT
| Seite | Größe | Refactoring-Status | Notwendige Aktionen |
|-------|-------|-------------------|---------------------|
| `create.vue` | 36.080 Zeichen | ❌ Kaum refaktoriert | - Aufteilung in Projekt/Hackathon-Erstellungs-Komponenten<br>- Extraktion von Formular-Komponenten<br>- Erstellung von `FormField`, `FormSection` Molecules |
| `profile.vue` | 37.995 Zeichen | ❌ Teilweise refaktoriert | - Extraktion von Profil-Sektionen (Übersicht, Einstellungen, Projekte)<br>- Erstellung von `ProfileHeader`, `ProfileSection` Organisms |
| `notifications.vue` | 23.719 Zeichen | ❌ Teilweise refaktoriert | - Extraktion von `NotificationList`, `NotificationItem`<br>- Erstellung von `NotificationPreferences` Organism |

#### 2. Große Seiten (15.000-30.000 Zeichen) - MITTLERE PRIORITÄT
| Seite | Größe | Refactoring-Status | Notwendige Aktionen |
|-------|-------|-------------------|---------------------|
| `projects/[id]/index.vue` | 34.216 Zeichen | ✅ Teilweise refaktoriert | - Kommentar-Sektion extrahieren (`CommentSection`)<br>- Projekt-Bild-Komponente erstellen<br>- Restliche Inline-Logik in Composable auslagern |
| `hackathons/[id]/index.vue` | 31.624 Zeichen | ✅ Gut refaktoriert | - Fehlende Komponenten: `HackathonDescription`, `ParticipantList`<br>- Bearbeitungs-Logik extrahieren |
| `teams/[id]/index.vue` | 32.288 Zeichen | ❌ Teilweise refaktoriert | - Team-Header extrahieren (`TeamHeader`)<br>- Mitglieder-Verwaltung extrahieren (`TeamMembers`)<br>- Projekt-Liste extrahieren (`TeamProjects`) |
| `my-votes.vue` | 19.963 Zeichen | ❌ Kaum refaktoriert | - Vote-Liste-Komponente erstellen<br>- Filter- und Suchkomponenten extrahieren |

#### 3. Mittlere Seiten (10.000-15.000 Zeichen) - NIEDRIGE PRIORITÄT
| Seite | Größe | Refactoring-Status | Notwendige Aktionen |
|-------|-------|-------------------|---------------------|
| `projects/index.vue` | 23.749 Zeichen | ❌ Teilweise refaktoriert | - Projekt-Karten-Komponente verbessern<br>- Filter-Komponenten extrahieren<br>- Pagination-Komponente erstellen |
| `hackathons/index.vue` | 14.991 Zeichen | ❌ Teilweise refaktoriert | - Hackathon-Karten-Komponente verwenden (`HackathonListCard`)<br>- Filter- und Sortier-Komponenten |
| `my-projects.vue` | 18.236 Zeichen | ❌ Kaum refaktoriert | - Projekt-Liste-Komponente wiederverwenden<br>- Bearbeitungs-Aktionen extrahieren |
| `about.vue` | 8.881 Zeichen | ✅ Einfach, kein Refactoring nötig | - Keine Aktionen notwendig |

#### 4. Authentifizierungsseiten - NIEDRIGE PRIORITÄT
| Seite | Größe | Refactoring-Status | Notwendige Aktionen |
|-------|-------|-------------------|---------------------|
| `login.vue` | 11.001 Zeichen | ❌ Kaum refaktoriert | - Formular-Komponenten extrahieren<br>- Social Login-Komponenten |
| `register.vue` | 11.845 Zeichen | ❌ Kaum refaktoriert | - Formular-Komponenten extrahieren<br>- Validierungs-Logik in Composable |
| `forgot-password.vue` | 4.245 Zeichen | ❌ Kaum refaktoriert | - Einfache Formular-Komponente |
| `reset-password.vue` | 7.353 Zeichen | ❌ Kaum refaktoriert | - Einfache Formular-Komponente |
| `verify-email.vue` | 6.596 Zeichen | ❌ Kaum refaktoriert | - Status-Anzeige-Komponente |

## Priorisierungsliste (Reihenfolge der Implementierung)

### Phase 1: Foundation & Hochprioritäre Seiten (Woche 1)
1. **Atomic Design Struktur vervollständigen**
   - `molecules/` Verzeichnis erstellen
   - `organisms/` Verzeichnis erstellen
   - Basis-Komponenten definieren

2. **Projekt-Detailseite vervollständigen** (`projects/[id]/index.vue`)
   - Kommentar-System extrahieren (`organisms/CommentSection`)
   - Projekt-Bild-Komponente (`projects/ProjectImage`)
   - Composable `useComments` erstellen

3. **Hackathon-Detailseite vervollständigen** (`hackathons/[id]/index.vue`)
   - Fehlende Komponenten: `HackathonDescription`, `ParticipantList`
   - Bearbeitungs-Logik in Composable auslagern

### Phase 2: Große komplexe Seiten (Woche 2)
4. **Profilseite refaktorieren** (`profile.vue`)
   - `ProfileHeader` Organism
   - `ProfileSection` Molecules für verschiedene Bereiche
   - `UserProjectsList`, `UserSettingsForm`

5. **Erstellungsseite refaktorieren** (`create.vue`)
   - Aufteilung in `ProjectCreateForm` und `HackathonCreateForm`
   - Formular-Komponenten (`FormField`, `FormSection`, `FormWizard`)
   - Shared Form-Logik in Composable

### Phase 3: Team- und Listen-Seiten (Woche 3)
6. **Team-Detailseite refaktorieren** (`teams/[id]/index.vue`)
   - `TeamHeader` Organism
   - `TeamMembers` Management-Komponente
   - `TeamProjects` Liste

7. **Listen-Seiten vereinheitlichen**
   - `projects/index.vue` mit wiederverwendbaren Filter-Komponenten
   - `hackathons/index.vue` mit `HackathonListCard`
   - `teams/index.vue` mit `TeamListCard`
   - `users/index.vue` mit `UserCard`

### Phase 4: Authentifizierung und Rest (Woche 4)
8. **Authentifizierungsseiten**
   - `AuthForm` Molecule für Login/Register
   - `SocialLoginButtons` Molecule
   - `PasswordResetFlow` Organism

9. **Einstellungs- und Verwaltungsseiten**
   - `notifications.vue` mit `NotificationPreferences`
   - `my-projects.vue` und `my-votes.vue` vereinheitlichen

### Phase 5: Testing & Optimierung (Woche 5)
10. **Integrationstests und Qualitätssicherung**
    - Komponententests für alle neuen Komponenten
    - Integrationstests für kritische Seiten
    - Performance-Optimierung (Lazy-Loading, Memoization)

## Atomic Design Struktur-Vorschlag

```
app/components/
├── atoms/           # Grundlegende UI-Elemente
│   ├── Avatar.vue      (existiert)
│   ├── Button.vue      (fehlt)
│   ├── Card.vue        (existiert)
│   ├── Tag.vue         (existiert)
│   ├── Input.vue       (fehlt)
│   ├── Textarea.vue    (fehlt)
│   └── LoadingSpinner.vue (fehlt)
├── molecules/       # Kombinationen von Atoms
│   ├── FormField.vue
│   ├── FormSection.vue
│   ├── SearchBar.vue
│   ├── FilterGroup.vue
│   ├── Pagination.vue
│   └── SocialLoginButtons.vue
├── organisms/       # Komplexe Komponenten
│   ├── CommentSection.vue
│   ├── ProjectHeader.vue      (existiert in projects/)
│   ├── ProfileHeader.vue
│   ├── NotificationPreferences.vue
│   └── TeamManagement.vue
├── templates/       # Seiten-Layouts (optional)
│   ├── AuthLayout.vue
│   ├── DashboardLayout.vue
│   └── FormLayout.vue
└── [domains]/      # Domänenspezifische Komponenten
    ├── projects/       (existiert)
    ├── hackathons/     (existiert)
    ├── teams/          (existiert)
    ├── users/          (existiert)
    ├── invitations/    (existiert)
    └── home/           (existiert)
```

## Erfolgskriterien

1. **Reduzierung der Seiten-Größe**: Jede Seite sollte unter 5.000 Zeichen liegen (aktuell bis zu 37.995)
2. **Wiederverwendbarkeit**: Komponenten sollten in mindestens 2 Kontexten verwendet werden
3. **Testabdeckung**: Alle neuen Komponenten sollten Unit-Tests haben
4. **Konsistente API**: Props und Events folgen einheitlichen Konventionen
5. **Performance**: Keine signifikante Verschlechterung der Ladezeiten

## Nächste Schritte

1. Benutzer-Feedback zu dieser Priorisierungsliste einholen
2. Mit Phase 1 beginnen (Atomic Design Struktur + Projekt-Detailseite)
3. Iteratives Vorgehen mit regelmäßiger Überprüfung