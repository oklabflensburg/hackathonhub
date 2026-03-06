# Phase 3: Team Components - Atomic Design Implementation Plan

## Übersicht
Phase 3 implementiert Team-Komponenten nach dem Atomic Design-Prinzip, basierend auf dem erfolgreichen Muster von Phase 2 (Project Components).

## Ziele
1. **TypeScript-Typen** für Team-Komponenten erstellen
2. **Feature-Flags** für Atomic Team Components erweitern
3. **20 Atomic Design Komponenten** implementieren (Atoms, Molecules, Organisms, Templates)
4. **3 Composables** für Team-Logik erstellen
5. **Bestehende Team-Seiten** mit Atomic Design Komponenten integrieren

## Tasks (24)

### 1. TypeScript-Typen für Team-Komponenten
- **Datei**: `frontend3/app/types/team-types.ts`
- **Inhalt**:
  - `Team` Interface mit allen Team-Eigenschaften
  - `TeamMember` Interface für Team-Mitglieder
  - `TeamInvitation` Interface für Einladungen
  - `TeamRole` Enum für Rollen (Owner, Admin, Member)
  - `TeamStatus` Enum für Team-Status (Active, Inactive, Archived)
  - `TeamVisibility` Enum für Sichtbarkeit (Public, Private)
  - `TeamStats` Interface für Team-Statistiken

### 2. Feature-Flags für Atomic Team Components erweitern
- **Datei**: `frontend3/app/config/feature-flags.ts`
- **Änderung**: `atomicTeamComponents: true` hinzufügen
- **Zweck**: Graduelle Einführung ohne Breaking Changes

### Atoms (7)

#### 3. TeamBadge.vue Atom implementieren
- **Pfad**: `frontend3/app/components/atoms/teams/TeamBadge.vue`
- **Props**: `status`, `size`, `showLabel`
- **Funktionalität**: Visuelle Darstellung des Team-Status

#### 4. TeamMemberAvatar.vue Atom implementieren
- **Pfad**: `frontend3/app/components/atoms/teams/TeamMemberAvatar.vue`
- **Props**: `member`, `size`, `showName`, `showRole`
- **Funktionalität**: Avatar für Team-Mitglieder

#### 5. TeamJoinButton.vue Atom implementieren
- **Pfad**: `frontend3/app/components/atoms/teams/TeamJoinButton.vue`
- **Props**: `team`, `userId`, `isMember`, `loading`
- **Funktionalität**: Button zum Beitreten/Verlassen eines Teams

#### 6. TeamInviteButton.vue Atom implementieren
- **Pfad**: `frontend3/app/components/atoms/teams/TeamInviteButton.vue`
- **Props**: `team`, `disabled`, `loading`
- **Funktionalität**: Button zum Einladen von Mitgliedern

#### 7. TeamSettingsButton.vue Atom implementieren
- **Pfad**: `frontend3/app/components/atoms/teams/TeamSettingsButton.vue`
- **Props**: `team`, `disabled`, `loading`
- **Funktionalität**: Button für Team-Einstellungen

#### 8. TeamVisibilityBadge.vue Atom implementieren
- **Pfad**: `frontend3/app/components/atoms/teams/TeamVisibilityBadge.vue`
- **Props**: `visibility`, `size`
- **Funktionalität**: Badge für Team-Sichtbarkeit (Public/Private)

#### 9. TeamRoleBadge.vue Atom implementieren
- **Pfad**: `frontend3/app/components/atoms/teams/TeamRoleBadge.vue`
- **Props**: `role`, `size`
- **Funktionalität**: Badge für Team-Rollen (Owner, Admin, Member)

### Molecules (5)

#### 10. TeamCardHeader.vue Molekül implementieren
- **Pfad**: `frontend3/app/components/molecules/teams/TeamCardHeader.vue`
- **Props**: `team`, `showActions`, `compact`
- **Funktionalität**: Header für Team-Karten mit Titel und Status

#### 11. TeamCardContent.vue Molekül implementieren
- **Pfad**: `frontend3/app/components/molecules/teams/TeamCardContent.vue`
- **Props**: `team`, `showDescription`, `showStats`, `maxDescriptionLength`
- **Funktionalität**: Content-Bereich für Team-Karten

#### 12. TeamCardFooter.vue Molekül implementieren
- **Pfad**: `frontend3/app/components/molecules/teams/TeamCardFooter.vue`
- **Props**: `team`, `userId`, `showMemberCount`, `showJoinButton`
- **Funktionalität**: Footer für Team-Karten mit Aktionen

#### 13. TeamMemberItem.vue Molekül implementieren
- **Pfad**: `frontend3/app/components/molecules/teams/TeamMemberItem.vue`
- **Props**: `member`, `team`, `currentUserId`, `showActions`
- **Funktionalität**: Einzelnes Team-Mitglied mit Aktionen

#### 14. TeamInvitationItem.vue Molekül implementieren
- **Pfad**: `frontend3/app/components/molecules/teams/TeamInvitationItem.vue`
- **Props**: `invitation`, `team`, `currentUserId`, `showActions`
- **Funktionalität**: Einzelne Team-Einladung mit Aktionen

### Organisms (5)

#### 15. TeamCard.vue Organism implementieren
- **Pfad**: `frontend3/app/components/organisms/teams/TeamCard.vue`
- **Props**: `team`, `userId`, `compact`, `showActions`
- **Funktionalität**: Komplette Team-Karte mit allen Unterkomponenten

#### 16. TeamList.vue Organism implementieren
- **Pfad**: `frontend3/app/components/organisms/teams/TeamList.vue`
- **Props**: `teams`, `userId`, `loading`, `error`, `emptyMessage`
- **Funktionalität**: Liste von Team-Karten mit Grid-Layout

#### 17. TeamDetailsHeader.vue Organism implementieren
- **Pfad**: `frontend3/app/components/organisms/teams/TeamDetailsHeader.vue`
- **Props**: `team`, `userId`, `loading`, `showActions`
- **Funktionalität**: Header für Team-Detail-Seiten

#### 18. TeamDetailsSidebar.vue Organism implementieren
- **Pfad**: `frontend3/app/components/organisms/teams/TeamDetailsSidebar.vue`
- **Props**: `team`, `members`, `invitations`, `userId`, `loading`
- **Funktionalität**: Sidebar für Team-Detail-Seiten

#### 19. TeamMembersList.vue Organism implementieren
- **Pfad**: `frontend3/app/components/organisms/teams/TeamMembersList.vue`
- **Props**: `team`, `members`, `userId`, `loading`, `error`, `showInviteButton`
- **Funktionalität**: Liste von Team-Mitgliedern mit Verwaltungsfunktionen

### Templates (2)

#### 20. TeamsPageTemplate.vue Template implementieren
- **Pfad**: `frontend3/app/components/templates/teams/TeamsPageTemplate.vue`
- **Props**: `teams`, `userId`, `loading`, `error`, `totalCount`, `page`, `pageSize`, `searchQuery`, `selectedFilters`
- **Events**: `search`, `filter-change`, `sort-change`, `page-change`, `create-team`
- **Funktionalität**: Template für Team-Listen-Seiten

#### 21. TeamDetailsTemplate.vue Template implementieren
- **Pfad**: `frontend3/app/components/templates/teams/TeamDetailsTemplate.vue`
- **Props**: `team`, `members`, `invitations`, `userId`, `loading`, `error`
- **Events**: `update-team`, `delete-team`, `invite-member`, `remove-member`, `update-member-role`
- **Funktionalität**: Template für Team-Detail-Seiten

### Composables (3)

#### 22. useTeams.ts Composable implementieren
- **Pfad**: `frontend3/app/composables/useTeams.ts`
- **Funktionalität**: Umfassende Team-Datenverwaltung (Fetching, Filtering, Sorting)
- **Features**: Pagination, Search, Filter, Sort, Create, Update, Delete

#### 23. useTeamMembers.ts Composable implementieren
- **Pfad**: `frontend3/app/composables/useTeamMembers.ts`
- **Funktionalität**: Team-Mitglieder-Verwaltung
- **Features**: Get Members, Add Member, Remove Member, Update Role

#### 24. useTeamInvitations.ts Composable implementieren
- **Pfad**: `frontend3/app/composables/useTeamInvitations.ts`
- **Funktionalität**: Team-Einladungs-Verwaltung
- **Features**: Get Invitations, Send Invitation, Accept Invitation, Reject Invitation

### Wrapper Components (2)

#### 25. TeamListAtomicWrapper.vue erstellen
- **Pfad**: `frontend3/app/components/teams/TeamListAtomicWrapper.vue`
- **Funktionalität**: Wrapper für Team-Listen-Seiten mit Feature-Flag-Switching
- **Props**: Alle Props von `TeamsPageTemplate`
- **Slots**: `default` für Legacy-Implementierung

#### 26. TeamDetailAtomicWrapper.vue erstellen
- **Pfad**: `frontend3/app/components/teams/TeamDetailAtomicWrapper.vue`
- **Funktionalität**: Wrapper für Team-Detail-Seiten mit Feature-Flag-Switching
- **Props**: Alle Props von `TeamDetailsTemplate`
- **Slots**: `default` für Legacy-Implementierung

### Integration (3)

#### 27. Team-Listen-Seite integrieren (`/teams`)
- **Datei**: `frontend3/app/pages/teams/index.vue`
- **Wrapper**: `TeamListAtomicWrapper`
- **Zweck**: Integration der Atomic Design Team-Komponenten

#### 28. Team-Detail-Seite integrieren (`/teams/[id]`)
- **Datei**: `frontend3/app/pages/teams/[id]/index.vue`
- **Wrapper**: `TeamDetailAtomicWrapper`
- **Zweck**: Integration der Atomic Design Team-Komponenten

#### 29. Hackathon-Team-Liste integrieren (`/hackathons/[id]/teams`)
- **Datei**: `frontend3/app/pages/hackathons/[id]/teams.vue`
- **Wrapper**: `TeamListAtomicWrapper`
- **Zweck**: Integration der Atomic Design Team-Komponenten

### Dokumentation & Testing (3)

#### 30. TypeScript-Typen dokumentieren
- **Datei**: `frontend3/docs/TEAM_TYPES_DOCUMENTATION.md`
- **Inhalt**: Dokumentation aller Team-Typen und Enums

#### 31. Integration Guide erstellen
- **Datei**: `frontend3/docs/ATOMIC_TEAM_COMPONENTS_INTEGRATION_GUIDE.md`
- **Inhalt**: Schritt-für-Schritt Anleitung zur Integration

#### 32. Testing & Build-Verifikation
- **Aktionen**:
  1. TypeScript-Fehler beheben
  2. Build testen (`npm run build`)
  3. Linting testen (`npm run lint`)
  4. Integration testen (Feature-Flag Switching)

## Zeitplan

### Woche 1: Foundation & Atoms
- **Tag 1**: TypeScript-Typen und Feature-Flags (Tasks 1-2)
- **Tag 2**: Atoms implementieren (Tasks 3-9)
- **Tag 3**: Molecules implementieren (Tasks 10-14)

### Woche 2: Organisms & Templates
- **Tag 4**: Organisms implementieren (Tasks 15-19)
- **Tag 5**: Templates implementieren (Tasks 20-21)
- **Tag 6**: Composables implementieren (Tasks 22-24)

### Woche 3: Integration & Testing
- **Tag 7**: Wrapper Components erstellen (Tasks 25-26)
- **Tag 8**: Seiten integrieren (Tasks 27-29)
- **Tag 9**: Dokumentation und Testing (Tasks 30-32)

## Erfolgskriterien

### Technische Kriterien
1. ✅ **Build erfolgreich**: Keine TypeScript-Fehler
2. ✅ **Linting bestanden**: Keine ESLint-Fehler
3. ✅ **Feature-Flags funktionieren**: Einfaches Switching zwischen Legacy und Atomic
4. ✅ **Responsive Design**: Mobile-first Ansatz
5. ✅ **Accessibility**: ARIA-Labels und Keyboard-Navigation

### Funktionale Kriterien
1. ✅ **Alle Team-Komponenten implementiert**: 20 Atomic Design Komponenten
2. ✅ **Alle Team-Seiten integriert**: 3 Seiten mit Atomic Design
3. ✅ **Vollständige TypeScript-Typisierung**: Keine `any`-Typen
4. ✅ **Umfassende Dokumentation**: 3 Dokumentationsdateien
5. ✅ **Testing abgeschlossen**: Build und Linting erfolgreich

## Risiken und Mitigation

### Risiko 1: Inkompatibilität mit bestehenden Datenstrukturen
- **Mitigation**: TypeScript-Typen basierend auf bestehenden Backend-Strukturen
- **Fallback**: Feature-Flag für einfache Deaktivierung

### Risiko 2: Performance-Probleme
- **Mitigation**: Lazy Loading von Komponenten
- **Optimierung**: Effiziente Reaktivität mit Vue 3 Composition API

### Risiko 3: UI-Inkonsistenzen
- **Mitigation**: Wiederverwendung von Design-System aus Phase 1 und 2
- **Konsistenz**: Gleiche CSS-Variablen und Utility-Klassen

## Fazit
Phase 3 baut auf den erfolgreichen Mustern von Phase 2 auf und implementiert ein vollständiges Atomic Design-System für Team-Komponenten. Der schrittweise Ansatz mit Feature-Flags ermöglicht eine risikoarme Einführung ohne Breaking Changes.