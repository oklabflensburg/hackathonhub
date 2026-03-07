# Atomic Design Migration Plan - Hackathon Dashboard

## Zielstellung
Vollständige Migration aller Frontend-Komponenten auf Atomic Design, Eliminierung von Legacy-Komponenten und Duplikaten, Konsistenz über alle Seiten.

## Aktueller Status
- ✅ **Phase 1-3 abgeschlossen**: Layout, Projekt- und Team-Komponenten migriert
- ⚠️ **Gemischte Nutzung**: Einige Seiten verwenden Atomic Design, andere nicht
- ❌ **Legacy-Bereiche**: Auth-Flows, Homepage, Notifications
- 🔄 **Duplikate**: Parallele Komponenten-Strukturen

## Phasenplan

### Phase 4: Auth-Komponenten Migration (Priorität 1)
**Ziel**: Alle Authentifizierungs-Seiten auf Atomic Design umstellen

#### Schritt 4.1: Auth-Atoms erstellen/verwenden
- [ ] Prüfen, ob existierende Atoms (`Button`, `Input`, `Card`, `Alert`) für Auth ausreichen
- [ ] Gegebenenfalls spezifische Auth-Atoms erstellen:
  - `AuthCard.vue` (Atom) - Spezielles Card-Design für Auth
  - `OAuthButton.vue` (Atom) - Button für OAuth-Provider

#### Schritt 4.2: Auth-Molecules erstellen
- [ ] `FormField.vue` (existiert) - Für Eingabefelder mit Label und Validation
- [ ] `AuthForm.vue` (Molecule) - Basis-Formular für Auth
- [ ] `OAuthButtons.vue` (Molecule) - Gruppe von OAuth-Buttons

#### Schritt 4.3: Auth-Organisms erstellen
- [ ] `LoginForm.vue` (Organism) - Komplette Login-Form
- [ ] `RegisterForm.vue` (Organism) - Komplette Registrierungs-Form
- [ ] `PasswordResetForm.vue` (Organism) - Passwort-Reset-Form
- [ ] `EmailVerificationForm.vue` (Organism) - Email-Verifikation

#### Schritt 4.4: Auth-Templates erstellen
- [ ] `AuthLayout.vue` (Template) - Layout für Auth-Seiten (existiert möglicherweise)

#### Schritt 4.5: Seiten migrieren
- [ ] `login.vue` → Verwendet `LoginForm` (Organism)
- [ ] `register.vue` → Verwendet `RegisterForm` (Organism)
- [ ] `forgot-password.vue` → Verwendet `PasswordResetForm` (Organism)
- [ ] `reset-password.vue` → Verwendet `PasswordResetForm` (Organism)
- [ ] `verify-email.vue` → Verwendet `EmailVerificationForm` (Organism)

### Phase 5: Homepage Migration (Priorität 1)
**Ziel**: Homepage auf Atomic Design umstellen

#### Schritt 5.1: Home-Organisms migrieren
- [ ] `HomeHero.vue` (Legacy) → `organisms/pages/home/HomeHero.vue` (bereits existiert)
- [ ] `HomeStatsSection.vue` (Legacy) → `organisms/pages/home/HomeStatsSection.vue` (bereits existiert)
- [ ] `HomeHackathonCard.vue` (Legacy) → `organisms/pages/home/HomeHackathonCard.vue` (bereits existiert)
- [ ] `HomeProjectCard.vue` (Legacy) → `organisms/pages/home/HomeProjectCard.vue` (bereits existiert)
- [ ] `HomeCtaSection.vue` (Legacy) → `organisms/pages/home/HomeCtaSection.vue` (bereits existiert)

#### Schritt 5.2: Homepage-Template erstellen
- [ ] `HomePageTemplate.vue` (Template) - Layout für Homepage

#### Schritt 5.3: Seite migrieren
- [ ] `index.vue` → Verwendet Home-Organisms und HomePageTemplate

### Phase 6: Notifications Migration (Priorität 2)
**Ziel**: Notification-System auf Atomic Design umstellen

#### Schritt 6.1: Notification-Komponenten analysieren
- [ ] Bestehende `NotificationContainer.vue`, `NotificationSettings.vue` analysieren
- [ ] Atomic Design-Äquivalente identifizieren/erstellen

#### Schritt 6.2: Notification-Atoms/Molecules erstellen
- [ ] `NotificationItem.vue` (Molecule) - Einzelne Notification (existiert)
- [ ] `NotificationBadge.vue` (Atom) - Badge für unread counts (existiert)
- [ ] `NotificationIcon.vue` (Atom) - Icon für Notifications (existiert)

#### Schritt 6.3: Notification-Organisms erstellen
- [ ] `NotificationCenter.vue` (Organism) - Notification-Übersicht (existiert)
- [ ] `NotificationSettingsPanel.vue` (Organism) - Einstellungen

#### Schritt 6.4: Seite migrieren
- [ ] `notifications.vue` → Verwendet Notification-Organisms

### Phase 7: Duplikate konsolidieren (Priorität 1)
**Ziel**: Parallele Komponenten-Strukturen bereinigen

#### Schritt 7.1: Projekt-Komponenten konsolidieren
- [ ] Entscheidung: `projects/` (Legacy) vs `organisms/pages/projects/` (Atomic Design)
- [ ] Atomic Design-Versionen als Standard etablieren
- [ ] Legacy-Komponenten entfernen oder als Deprecated markieren
- [ ] Alle Referenzen auf Legacy-Komponenten aktualisieren

#### Schritt 7.2: Home-Komponenten konsolidieren
- [ ] `home/` (Legacy) → `organisms/pages/home/` migrieren
- [ ] Legacy-Verzeichnis entfernen

#### Schritt 7.3: User-Komponenten konsolidieren
- [ ] `users/` (Legacy) → `organisms/pages/users/` migrieren
- [ ] Legacy-Verzeichnis entfernen

### Phase 8: Feature-Flags und Dokumentation (Priorität 2)
**Ziel**: Feature-Flags aktualisieren und Dokumentation synchronisieren

#### Schritt 8.1: Feature-Flags aktualisieren
- [ ] `feature-flags.ts` mit tatsächlichem Stand synchronisieren
- [ ] Flags für neue Migrationsphasen hinzufügen:
  - `atomicAuthComponents: boolean`
  - `atomicHomeComponents: boolean`
  - `atomicNotificationComponents: boolean`

#### Schritt 8.2: Dokumentation aktualisieren
- [ ] `ATOMIC_DESIGN_REFACTORING_COMPLETION.md` aktualisieren
- [ ] Neue Phasen dokumentieren
- [ ] README aktualisieren

### Phase 9: Konsistenz und Qualität (Priorität 3)
**Ziel**: Einheitliche Struktur und Qualität sicherstellen

#### Schritt 9.1: Import-Konsistenz
- [ ] Einheitliche Import-Struktur etablieren (immer über Index-Dateien)
- [ ] Auto-Import Konfiguration prüfen

#### Schritt 9.2: TypeScript-Typisierung
- [ ] Fehlende Typen für Auth, Home, Notifications ergänzen
- [ ] TypeScript-Konfiguration optimieren

#### Schritt 9.3: Testing
- [ ] Unit-Tests für neue Atomic Design-Komponenten
- [ ] Integrationstests für migrierte Seiten

## Zeitplan (Schätzungen)

### Woche 1-2: Phase 4 (Auth)
- Auth-Atoms/Molecules/Organisms erstellen
- Auth-Seiten migrieren
- Testing durchführen

### Woche 3: Phase 5 (Homepage)
- Home-Organisms verwenden
- Homepage migrieren
- Testing durchführen

### Woche 4: Phase 6 (Notifications)
- Notification-Komponenten analysieren und migrieren
- Notifications-Seite migrieren

### Woche 5: Phase 7 (Duplikate)
- Projekt-, Home-, User-Komponenten konsolidieren
- Legacy-Komponenten entfernen

### Woche 6: Phase 8-9 (Dokumentation & Qualität)
- Feature-Flags aktualisieren
- Dokumentation vervollständigen
- Import-Konsistenz herstellen

## Erfolgskriterien

### Quantitative
- ✅ 100% der Seiten verwenden Atomic Design-Komponenten
- ✅ 0 Legacy-Komponenten außerhalb der Atomic Design-Struktur
- ✅ 0 Duplikate (parallele Implementierungen)
- ✅ 100% TypeScript-Abdeckung für öffentliche APIs

### Qualitative
- ✅ Konsistente Benutzererfahrung über alle Seiten
- ✅ Einheitliche Code-Struktur
- ✅ Gute Wartbarkeit und Erweiterbarkeit
- ✅ Vollständige Dokumentation

## Risiken und Mitigation

### Risiko 1: Breaking Changes
- **Mitigation**: Feature-Flags für schrittweise Migration
- **Mitigation**: Paralleler Betrieb während Migration
- **Mitigation**: Umfassendes Testing

### Risiko 2: Performance-Einbußen
- **Mitigation**: Bundle-Analyse durchführen
- **Mitigation**: Code-Splitting optimieren
- **Mitigation**: Lazy-Loading für nicht-kritische Komponenten

### Risiko 3: Entwickler-Akzeptanz
- **Mitigation**: Klare Dokumentation und Beispiele
- **Mitigation**: Schulung/Onboarding für Team
- **Mitigation**: Konsistente Developer Experience

## Ressourcen

### Benötigte Komponenten
1. **Auth-Atoms**: 2-3 neue Atoms
2. **Auth-Molecules**: 3-4 neue Molecules
3. **Auth-Organisms**: 4-5 neue Organisms
4. **Templates**: 1-2 neue Templates

### Technische Voraussetzungen
- Vue 3 / Nuxt 3 Kenntnisse
- TypeScript-Erfahrung
- Atomic Design-Verständnis
- Testing-Kenntnisse (Vitest/Vue Test Utils)

## Verantwortlichkeiten

- **Frontend Lead**: Gesamtverantwortung, Architektur-Entscheidungen
- **Frontend Developer 1**: Auth-Migration (Phase 4)
- **Frontend Developer 2**: Homepage-Migration (Phase 5)
- **Frontend Developer 3**: Notifications & Duplikate (Phase 6-7)
- **Tech Writer**: Dokumentation (Phase 8)

## Nächste Schritte

1. **Sofort**: Detaillierte Spezifikation für Auth-Komponenten erstellen
2. **Tag 1**: Mit Phase 4.1 (Auth-Atoms) beginnen
3. **Woche 1**: Erste migrierte Auth-Seite in Testumgebung deployen
4. **Wöchentlich**: Fortschrittsreview mit Team

---
**Plan erstellt am**: 07.03.2026  
**Plan Version**: 1.0  
**Verantwortlich**: Kilo Code  
**Projekt**: Hackathon Dashboard Frontend