# Phase 1: Layout-Komponenten - Detaillierte Todo-Liste

## Übersicht
Migration der globalen Layout-Komponenten zu Atomic Design. Diese Komponenten werden auf fast jeder Seite verwendet und haben hohe Wiederverwendbarkeit.

## Aktuelle Komponenten (zu migrieren)
1. `AppHeader.vue` → Wird bereits als `AppHeaderBar.vue` in `organisms/layout/` verwendet
2. `AppFooter.vue` → Wird bereits als `AppFooterContent.vue` in `organisms/layout/` verwendet
3. `AppSidebar.vue` → Muss migriert werden
4. `MobileBottomNav.vue` → Muss migriert werden

## Neue Atomic Design-Struktur

### Atome (neu zu erstellen)
1. **`Logo.vue`**
   - Props: `size` (sm, md, lg), `darkMode` (boolean)
   - Events: `click`
   - Slots: default für Text-Logo

2. **`NavigationLink.vue`**
   - Props: `to` (Route), `active` (boolean), `icon` (string)
   - Events: `click`
   - Slots: default für Link-Text

### Moleküle (neu zu erstellen)
1. **`NavigationItem.vue`**
   - Kombiniert: `NavigationLink` + optionales Icon
   - Props: `to`, `active`, `icon`, `badgeCount` (number)
   - Events: `click`

2. **`ThemeToggle.vue`**
   - Kombiniert: Button + Icon + Zustandsmanagement
   - Props: `initialTheme` ('light' | 'dark')
   - Events: `theme-change`

3. **`UserMenu.vue`**
   - Kombiniert: Avatar + Dropdown-Menü
   - Props: `user` (User object), `avatarUrl` (string)
   - Events: `logout`, `profile-click`, `settings-click`

### Organismen (zu migrieren/erstellen)
1. **`AppSidebar.vue`** (neu in `organisms/layout/`)
   - Kombiniert: `Logo` + `NavigationItem`-Liste + `ThemeToggle`
   - Props: `navigationItems` (Array), `currentRoute` (string), `user` (object)
   - Events: `navigate`, `toggle-theme`

2. **`MobileNavigation.vue`** (neu in `organisms/layout/`)
   - Kombiniert: `NavigationItem`-Liste für mobile Ansicht
   - Props: `navigationItems` (Array), `currentRoute` (string)
   - Events: `navigate`

3. **`AppHeaderBar.vue`** (bereits existiert - zu überprüfen/verbessern)
4. **`AppFooterContent.vue`** (bereits existiert - zu überprüfen/verbessern)

### Composables (neu zu erstellen)
1. **`useLayoutNavigation.ts`**
   - Verwaltet Navigationszustand
   - Logik für aktive Routes
   - Responsive Navigation (mobile/desktop)

2. **`useTheme.ts`**
   - Theme-Management (light/dark)
   - Persistenz in localStorage
   - System-Preference Detection

## Schritt-für-Schritt Implementierung

### Schritt 1: TypeScript-Typen erstellen
```typescript
// frontend3/app/types/layout-types.ts
export interface NavigationItem {
  id: string
  label: string
  to: string
  icon?: string
  badgeCount?: number
  requiresAuth?: boolean
}

export interface UserMenuOption {
  id: string
  label: string
  icon: string
  action: () => void
}

export interface ThemeState {
  current: 'light' | 'dark'
  systemPreference: 'light' | 'dark'
  persisted: boolean
}
```

### Schritt 2: Feature-Flags erweitern
```typescript
// frontend3/app/config/feature-flags.ts
export interface FeatureFlags {
  atomicTeamInvitations: boolean      // Bereits existiert
  atomicLayoutComponents: boolean     // Neu für Phase 1
  // ... andere Flags
}

const featureFlags: FeatureFlags = {
  atomicTeamInvitations: true,
  atomicLayoutComponents: process.env.NUXT_PUBLIC_FEATURE_ATOMIC_LAYOUT === 'true' || false,
  // ...
}
```

### Schritt 3: Atome implementieren
1. `Logo.vue` erstellen
2. `NavigationLink.vue` erstellen
3. Tests schreiben
4. In `atoms/index.ts` exportieren

### Schritt 4: Moleküle implementieren
1. `NavigationItem.vue` erstellen
2. `ThemeToggle.vue` erstellen
3. `UserMenu.vue` erstellen
4. Tests schreiben
5. In `molecules/index.ts` exportieren

### Schritt 5: Composables implementieren
1. `useLayoutNavigation.ts` erstellen
2. `useTheme.ts` erstellen
3. Tests schreiben

### Schritt 6: Organismen implementieren/migrieren
1. `AppSidebar.vue` in `organisms/layout/` erstellen
2. `MobileNavigation.vue` in `organisms/layout/` erstellen
3. Bestehende `AppHeaderBar.vue` und `AppFooterContent.vue` überprüfen/verbessern
4. Tests schreiben

### Schritt 7: Seiten anpassen
1. `app.vue` anpassen, um Atomic Design Layout-Komponenten zu verwenden
2. Feature-Flag-Logik implementieren
3. Fallback zu alten Komponenten bei deaktiviertem Flag

### Schritt 8: Testing
1. Unit-Tests für alle neuen Komponenten
2. Integrationstests für Layout-Organismen
3. E2E-Tests für Navigation und Theme-Toggle

### Schritt 9: Rollout
1. Feature-Flag für Entwickler aktivieren
2. Testing in Entwicklungsumgebung
3. Feature-Flag für Staging aktivieren
4. User Acceptance Testing
5. Feature-Flag für Produktion aktivieren (graduell)

## Spezifische Todo-Liste

### Woche 1: Grundlagen
- [ ] `layout-types.ts` erstellen
- [ ] Feature-Flags erweitern
- [ ] `Logo.vue` Atom implementieren
- [ ] `NavigationLink.vue` Atom implementieren
- [ ] `NavigationItem.vue` Molekül implementieren

### Woche 2: Theme und User-Menü
- [ ] `ThemeToggle.vue` Molekül implementieren
- [ ] `UserMenu.vue` Molekül implementieren
- [ ] `useTheme.ts` Composable implementieren
- [ ] `useLayoutNavigation.ts` Composable implementieren

### Woche 3: Organismen
- [ ] `AppSidebar.vue` Organism implementieren
- [ ] `MobileNavigation.vue` Organism implementieren
- [ ] Bestehende Header/Footer Komponenten überprüfen
- [ ] Responsive Design implementieren

### Woche 4: Integration und Testing
- [ ] `app.vue` anpassen für Feature-Flag
- [ ] Unit-Tests für alle neuen Komponenten
- [ ] Integrationstests für Layout
- [ ] E2E-Tests für Navigation

### Woche 5: Rollout
- [ ] Feature-Flag in Entwicklung aktivieren
- [ ] Testing in Dev-Umgebung
- [ ] Feature-Flag in Staging aktivieren
- [ ] UAT durchführen
- [ ] Rollout-Plan für Produktion erstellen

## Erfolgskriterien für Phase 1

### Technische Kriterien
- [ ] Alle neuen Komponenten folgen Atomic Design-Prinzipien
- [ ] TypeScript-Typen vollständig und korrekt
- [ ] Feature-Flags funktionieren korrekt
- [ ] Keine Regressionen in bestehender Navigation
- [ ] Responsive Design funktioniert auf allen Geräten
- [ ] Theme-Switching funktioniert und persistiert

### Performance Kriterien
- [ ] Bundle-Größe nicht signifikant erhöht
- [ ] Ladezeit für Layout-Komponenten gleich oder besser
- [ ] Keine Memory-Leaks in Composables

### UX Kriterien
- [ ] Navigation funktioniert wie erwartet
- [ ] Theme-Toggle sofort sichtbar
- [ ] Mobile Navigation intuitiv
- [ ] Accessibility-Anforderungen erfüllt

## Risiken und Mitigation

### Risiko 1: Breaking Changes in Navigation
- **Mitigation**: Feature-Flag mit Fallback zu alten Komponenten
- **Testing**: Umfassende Navigationstests

### Risiko 2: Performance-Einbußen
- **Mitigation**: Code-Splitting für Layout-Komponenten
- **Monitoring**: Performance-Metriken vor/nach Vergleich

### Risiko 3: Theme-Konsistenz
- **Mitigation**: System-weite Theme-Klasse verwenden
- **Testing**: Theme-Testing auf allen Seiten

### Risiko 4: Mobile UX
- **Mitigation**: Usability-Testing auf mobilen Geräten
- **Feedback**: Frühes Feedback von mobilen Nutzern

## Abhängigkeiten

### Backend
- Keine direkten Backend-Änderungen benötigt
- User-Daten für UserMenu aus bestehenden APIs

### Frontend
- Bestehende Auth-Store für User-Daten
- Bestehende Routing-Logik
- Bestehende i18n für Übersetzungen

### Design System
- Konsistenz mit bestehenden Design-Tokens
- Tailwind CSS Klassen wiederverwenden

## Dokumentation

### Zu erstellende Dokumentation
1. **Komponenten-Dokumentation**: Props, Events, Slots für jede neue Komponente
2. **Composable-Dokumentation**: API für `useLayoutNavigation` und `useTheme`
3. **Migrations-Guide**: Wie von alten zu neuen Komponenten wechseln
4. **Testing-Guide**: Wie die neuen Komponenten getestet werden

### Zu aktualisierende Dokumentation
1. **Atomic Design Plan**: Phase 1 als abgeschlossen markieren
2. **Feature-Flag Dokumentation**: Neue Flags dokumentieren
3. **Architektur-Dokumentation**: Layout-Architektur aktualisieren

## Nächste Schritte nach Phase 1

1. **Review**: Code-Review aller neuen Komponenten
2. **Performance Audit**: Bundle-Analyse durchführen
3. **User Feedback**: Feedback von Beta-Nutzern sammeln
4. **Phase 2 vorbereiten**: Projekt-Komponenten analysieren

## Verantwortlichkeiten

### Frontend Developer
- Implementierung der Komponenten
- Testing der Komponenten
- Dokumentation der APIs

### Designer
- Design-Review der neuen Komponenten
- Accessibility-Review
- UX-Feedback

### QA Engineer
- Testing der Layout-Komponenten
- Cross-Browser Testing
- Mobile Device Testing

### Product Owner
- Priorisierung der Features
- User Acceptance Testing
- Rollout-Entscheidungen