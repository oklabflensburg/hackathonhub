# Atomic Design Komponentenhierarchie für /settings Seite

## Übersicht
Basierend auf der bestehenden Atomic Design Struktur des Projekts, hier ist die vorgeschlagene Komponentenhierarchie für die /settings Seite.

## Atoms (Grundlegende UI-Elemente)

### Bestehende Atoms (Wiederverwendung)
- `Button` - Für Aktionen (Speichern, Abbrechen, Löschen)
- `Input` - Für Texteingaben
- `Checkbox` - Für Boolesche Einstellungen
- `Radio` - Für Einzelauswahl
- `Select` - Für Dropdown-Auswahl
- `Textarea` - Für längere Texteingaben
- `Avatar` - Für Profilbild
- `Badge` - Für Statusanzeigen
- `Card` - Für Container
- `Divider` - Für visuelle Trennung
- `Tooltip` - Für Erklärungen

### Neue Atoms (Erforderlich)
- `ToggleSwitch` - Für Ein/Aus-Einstellungen (kann aus bestehenden Checkboxen erweitert werden)
- `TabItem` - Für Tab-Navigation
- `SectionHeader` - Für Abschnittsüberschriften mit optionaler Beschreibung
- `PrivacyBadge` - Für Datenschutz-Level-Anzeige

## Molecules (Kombination von Atoms)

### Bestehende Molecules (Wiederverwendung)
- `FormField` - Label + Input/Select/Textarea + Error Message
- `EmptyState` - Für leere Einstellungsbereiche
- `LoadingState` - Für Ladezustände

### Neue Molecules (Erforderlich)
- `SettingsToggle` - Label + Beschreibung + ToggleSwitch
- `SettingsSelect` - Label + Beschreibung + Select
- `SettingsInput` - Label + Beschreibung + Input + Validierung
- `OAuthConnection` - Avatar + Name + Status + Connect/Disconnect Button
- `PrivacySetting` - Label + Beschreibung + PrivacyBadge + Options
- `NotificationChannel` - Channel Name + Icon + ToggleSwitch + Settings Link

## Organisms (Komplexe Komponenten)

### Bestehende Organisms (Wiederverwendung)
- `UserSettingsForm` - Für Profilinformationen (bereits vorhanden)
- `NotificationSettingsPanel` - Für Benachrichtigungseinstellungen (bereits vorhanden)
- `ConfirmDialog` - Für Bestätigungsdialoge

### Neue Organisms (Erforderlich)
- `ProfileSettingsOrganism` - Konsolidierte Profil-Einstellungen (Avatar, Name, Bio, etc.)
- `AccountSecurityOrganism` - Passwortänderung, 2FA, Sitzungsverwaltung
- `OAuthConnectionsOrganism` - GitHub, Google OAuth Verbindungen
- `PrivacySettingsOrganism` - Datenschutzeinstellungen, Sichtbarkeit
- `PlatformPreferencesOrganism` - Theme, Sprache, Standardeinstellungen
- `NotificationPreferencesOrganism` - Erweiterte Benachrichtigungseinstellungen
- `DataManagementOrganism` - Datenexport, Account-Löschung
- `APIAccessOrganism` - API-Schlüssel, Zugriffsrechte

## Templates (Seitenlayouts)

### Bestehende Templates (Anpassung)
- `SettingsPageTemplate` - Hauptlayout für Einstellungsseite
  - Header mit Titel und Beschreibung
  - Linke Navigation (Tabs oder vertikale Menü)
  - Hauptinhaltbereich
  - Aktionen-Bereich (Speichern/Abbrechen)

### Seitenstruktur
```
SettingsPageTemplate
├── SettingsNavigation (Organism)
│   ├── TabItem (Atom) × N
├── SettingsContentArea
│   ├── ProfileSettingsOrganism
│   ├── AccountSecurityOrganism  
│   ├── NotificationPreferencesOrganism
│   ├── PrivacySettingsOrganism
│   ├── PlatformPreferencesOrganism
│   ├── OAuthConnectionsOrganism
│   └── DataManagementOrganism
└── SettingsActions (Organism)
    ├── Button (Save)
    └── Button (Cancel)
```

## Pages (Vollständige Seiten)

### Neue Page
- `/pages/settings.vue` - Haupt-Einstellungsseite
  - Verwendet SettingsPageTemplate
  - Lädt Benutzerdaten
  - Handles Formular-Submission
  - Verwaltet Tab-Navigation

### Unter-Seiten (Optional)
- `/pages/settings/profile.vue` - Nur Profil-Einstellungen
- `/pages/settings/security.vue` - Nur Sicherheitseinstellungen
- `/pages/settings/notifications.vue` - Nur Benachrichtigungseinstellungen

## Composables (Logik-Wiederverwendung)

### Bestehende Composables (Wiederverwendung)
- `useUserProfile` - Für Benutzerdaten
- `useNotifications` - Für Benachrichtigungseinstellungen
- `useTheme` - Für Theme-Einstellungen

### Neue Composables (Erforderlich)
- `useSettings` - Zentrale Settings-Logik
  - Datenladen
  - Validierung
  - Speichern
  - Fehlerbehandlung
- `usePrivacySettings` - Spezifisch für Datenschutz
- `usePlatformPreferences` - Für Platform-Einstellungen
- `useOAuthConnections` - Für OAuth-Verwaltung

## Stores (State Management)

### Bestehende Stores (Erweiterung)
- `auth` store - Für Benutzerdaten
- `preferences` store - Für Benutzereinstellungen

### Neue Stores (Optional)
- `settings` store - Für Einstellungszustand
  - Aktive Tab
  - Ungespeicherte Änderungen
  - Validierungsfehler

## Typen (TypeScript)

### Bestehende Typen (Erweiterung)
- `user-types.ts` - User und Settings-Typen erweitern

### Neue Typen (Erforderlich)
- `settings-types.ts` - Alle Settings-spezifischen Typen
  ```typescript
  interface UserSettings {
    profile: ProfileSettings;
    security: SecuritySettings;
    notifications: NotificationSettings;
    privacy: PrivacySettings;
    platform: PlatformPreferences;
    connections: OAuthConnections;
  }
  
  interface ProfileSettings {
    username: string;
    email: string;
    name?: string;
    avatar_url?: string;
    bio?: string;
    location?: string;
    company?: string;
  }
  
  interface SecuritySettings {
    password?: string;
    two_factor_enabled: boolean;
    active_sessions: Session[];
  }
  
  // Weitere Interfaces...
  ```

## Implementierungsstrategie

### Phase 1: Foundation
1. Typen und Interfaces definieren
2. Basis-Komponenten (Atoms/Molecules) erstellen
3. SettingsPageTemplate implementieren

### Phase 2: Core Features
1. ProfileSettingsOrganism (basiert auf bestehendem UserSettingsForm)
2. NotificationPreferencesOrganism (basiert auf bestehendem NotificationSettingsPanel)
3. Grundlegende Navigation

### Phase 3: Advanced Features
1. AccountSecurityOrganism
2. PrivacySettingsOrganism
3. PlatformPreferencesOrganism

### Phase 4: Polish
1. Validierung und Fehlerbehandlung
2. Loading States
3. Success/Error Feedback
4. Responsive Design

## Wiederverwendung bestehender Komponenten

Das Projekt hat bereits eine solide Atomic Design Basis. Wir sollten:
1. Bestehende Atoms/Molecules maximal wiederverwenden
2. Bestehende Organisms erweitern statt neu zu erstellen
3. Konsistente Props-Interfaces beibehalten
4. Bestehende Design-Tokens und CSS-Klassen verwenden

## Next Steps
1. Backend-API-Erweiterungen definieren
2. Datenmodelle finalisieren
3. UI/UX-Design detaillieren
4. Implementierungsplan erstellen