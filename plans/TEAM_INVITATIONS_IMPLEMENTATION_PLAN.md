# Team Invitations - Implementierungsplan

## Übersicht

Dieser Plan beschreibt die konkreten Implementierungsschritte für das Atomic Design Refactoring der Team-Einladungen. Der Plan ist in aufeinanderfolgende Phasen unterteilt, die von einem Entwickler im Code Mode ausgeführt werden können.

## Phase 1: Vorbereitung und Setup

### Schritt 1.1: TypeScript Typen definieren
**Datei**: `frontend3/app/types/team-invitations.ts`
```typescript
export interface TeamInvitation {
  id: number
  team_id: number
  invited_user_id: number
  inviter_id: number
  status: 'pending' | 'accepted' | 'declined' | 'cancelled'
  created_at: string
  updated_at: string
  invited_user?: {
    id: number
    username: string
    name?: string
    avatar_url?: string
  }
  inviter?: {
    id: number
    username: string
    avatar_url?: string
  }
  team?: {
    id: number
    name: string
    hackathon?: {
      id: number
      name: string
    }
  }
}

export interface UserSearchResult {
  id: number
  username: string
  name?: string
  avatar_url?: string
  email?: string
  is_member?: boolean
}
```

### Schritt 1.2: Feature-Flag konfigurieren
**Datei**: `frontend3/app/config/feature-flags.ts`
```typescript
export const featureFlags = {
  useNewTeamInvitations: process.env.NUXT_PUBLIC_USE_NEW_TEAM_INVITATIONS === 'true' || false,
}
```

## Phase 2: Composables implementieren

### Schritt 2.1: `useTeamInvitations.ts` erstellen
**Datei**: `frontend3/app/composables/useTeamInvitations.ts`
- Implementiere alle Funktionen aus der Spezifikation
- Integriere mit bestehendem `teamStore`
- Füge Error Handling hinzu
- Schreibe Unit Tests in `frontend3/test/composables/useTeamInvitations.test.ts`

### Schritt 2.2: `useUserSearch.ts` erstellen
**Datei**: `frontend3/app/composables/useUserSearch.ts`
- Implementiere Debouncing mit `useDebounceFn` von VueUse
- Integriere mit User-API Endpoint
- Füge Filterung für bereits vorhandene Teammitglieder hinzu
- Schreibe Unit Tests

## Phase 3: Molecules implementieren

### Schritt 3.1: `InvitationItem.vue` erstellen
**Datei**: `frontend3/app/components/molecules/InvitationItem.vue`
- Kopiere das Design aus dem bestehenden Inline-Code (Zeilen 120-173 in `index.vue`)
- Extrahiere in wiederverwendbare Komponente
- Füge Props, Events und Slots hinzu
- Stelle Dark Mode Support sicher
- Schreibe Component Tests

### Schritt 3.2: `InviteUserForm.vue` erstellen
**Datei**: `frontend3/app/components/molecules/InviteUserForm.vue`
- Kombiniere Input und Button mit Logik
- Integriere `useUserSearch` Composable
- Füge Loading States hinzu
- Implementiere Erfolgs-/Fehler-Feedback
- Schreibe Component Tests

### Schritt 3.3: `UserSearchInput.vue` erstellen
**Datei**: `frontend3/app/components/molecules/UserSearchInput.vue`
- Erstelle dedizierte Search-Input-Komponente
- Implementiere Dropdown mit Vorschlägen
- Füge Keyboard Navigation hinzu
- Optimiere für Accessibility
- Schreibe Component Tests

## Phase 4: Organisms implementieren

### Schritt 4.1: `TeamInvitations.vue` erstellen
**Datei**: `frontend3/app/components/organisms/teams/TeamInvitations.vue`
- Kombiniere `InvitationItem` mit Loading, Empty, Error States
- Integriere `useTeamInvitations` Composable
- Füge Header mit Anzahl der ausstehenden Einladungen hinzu
- Implementiere Cancel-Funktionalität für Team-Owner
- Schreibe Integrationstests

### Schritt 4.2: `TeamInviteSection.vue` erstellen
**Datei**: `frontend3/app/components/organisms/teams/TeamInviteSection.vue`
- Kombiniere `InviteUserForm` mit Hilfetext und Member Count
- Füge Conditional Rendering basierend auf `isTeamOwner` und `isTeamFull` hinzu
- Integriere mit Team-Store für Member Count
- Schreibe Integrationstests

## Phase 5: Migration der Team-Detailseite

### Schritt 5.1: Feature-Flag Integration
**Datei**: `frontend3/app/pages/teams/[id]/index.vue`
```vue
<!-- Vorübergehend: Beide Versionen -->
<template>
  <!-- ... bestehender Code ... -->
  
  <!-- Team Invitations Section -->
  <div v-if="featureFlags.useNewTeamInvitations">
    <TeamInvitations
      :team-id="teamId"
      :is-team-owner="isTeamOwner"
      :show-header="true"
      @invitation-cancelled="handleInvitationCancelled"
    />
  </div>
  <div v-else>
    <!-- Existierender Inline-Code (Zeilen 95-175) -->
  </div>
  
  <!-- Invite Section (for owners) -->
  <div v-if="featureFlags.useNewTeamInvitations && isTeamOwner && !isTeamFull">
    <TeamInviteSection
      :team-id="teamId"
      :is-team-owner="isTeamOwner"
      :is-team-full="isTeamFull"
      :current-member-count="members.length"
      :max-members="team.max_members"
      @invite-sent="handleInviteSent"
    />
  </div>
  <div v-else-if="isTeamOwner && !isTeamFull">
    <!-- Existierender Inline-Code (Zeilen 43-92) -->
  </div>
</template>

<script setup>
import { featureFlags } from '~/config/feature-flags'
import TeamInvitations from '~/components/organisms/teams/TeamInvitations.vue'
import TeamInviteSection from '~/components/organisms/teams/TeamInviteSection.vue'
</script>
```

### Schritt 5.2: Event Handler anpassen
- Passe `handleInvitationCancelled` an, um mit der neuen Komponente zu arbeiten
- Passe `handleInviteSent` an, um die Einladungsliste zu aktualisieren
- Stelle sicher, dass alle bestehenden Funktionen (`cancelInvitation`, `sendInvitation`) weiterhin funktionieren

### Schritt 5.3: Testing der Migration
1. **Manuelles Testing**:
   - Team-Owner kann Benutzer einladen
   - Einladungen erscheinen in der Liste
   - Team-Owner kann Einladungen stornieren
   - Teammitglieder sehen Einladungen (keine Cancel-Buttons)
   - Responsive Design auf verschiedenen Bildschirmgrößen
   - Dark Mode funktioniert

2. **Automated Testing**:
   - E2E Tests für den kompletten Einladungs-Workflow
   - Integrationstests für die Seite
   - Regressionstests für bestehende Funktionalität

## Phase 6: Optimierung und Feinschliff

### Schritt 6.1: Performance Optimierungen
- Lazy Loading der Invitations-Komponenten
- Implementiere Virtual Scrolling für lange Listen
- Cache Einladungsdaten im Store
- Optimiere Bundle Size durch dynamische Imports

### Schritt 6.2: Accessibility Verbesserungen
- Füge ARIA-Labels zu allen interaktiven Elementen hinzu
- Stelle Keyboard Navigation sicher
- Teste mit Screen Readern
- Füge Focus Management hinzu

### Schritt 6.3: Internationalisierung
- Erstelle/aktualisiere Übersetzungsschlüssel in `frontend3/app/i18n/`
- Stelle sicher, dass alle Labels übersetzbar sind
- Teste mit verschiedenen Sprachen

## Phase 7: Finale Migration und Cleanup

### Schritt 7.1: Feature-Flag entfernen
1. Setze `NUXT_PUBLIC_USE_NEW_TEAM_INVITATIONS=true` in Production
2. Überwache Fehler und Performance für 24 Stunden
3. Wenn stabil: Entferne Feature-Flag und alten Code

### Schritt 7.2: Alten Code entfernen
**Datei**: `frontend3/app/pages/teams/[id]/index.vue`
- Entferne den `v-else` Zweig und den alten Inline-Code
- Entferne nicht mehr benötigte Funktionen (`cancelInvitation`, `sendInvitation`, `searchUsers`, etc.)
- Bereinige Importe

### Schritt 7.3: Dokumentation aktualisieren
1. **Komponenten-Dokumentation**: Füge JSDoc Kommentare zu allen neuen Komponenten hinzu
2. **Storybook**: Erstelle Stories für die neuen Komponenten (falls Storybook verwendet wird)
3. **Developer Guide**: Dokumentiere die neue API im `README.md` oder Developer Guide

## Rollback Plan

### Bei kritischen Problemen:
1. Setze `NUXT_PUBLIC_USE_NEW_TEAM_INVITATIONS=false`
2. Der alte Code wird wieder aktiviert
3. Analysiere das Problem und fixe es
4. Erneut deployen

### Notfall-Maßnahmen:
- Database Backup vor Migration
- Monitoring von Error Rates und Performance Metrics
- Schnelle Rollback-Fähigkeit durch Feature-Flags

## Erfolgsmetriken

### Quantitative Metriken:
- [ ] Seitenladezeit nicht erhöht
- [ ] Bundle Size erhöht sich um < 10KB
- [ ] 0 neue Console Errors in Production
- [ ] Test Coverage > 80% für neue Komponenten

### Qualitative Metriken:
- [ ] Developer Feedback positiv
- [ ] Code Review ohne major issues
- [ ] Accessibility Audit bestanden
- [ ] UI/UX identisch oder verbessert

## Zeitplan und Aufwandsschätzung

### Geschätzter Aufwand (in Personentagen):
- Phase 1: 0.5 Tage
- Phase 2: 1.5 Tage
- Phase 3: 2 Tage
- Phase 4: 1.5 Tage
- Phase 5: 1.5 Tage
- Phase 6: 1 Tag
- Phase 7: 0.5 Tage

**Gesamt**: 8.5 Tage (ca. 2 Wochen bei Teilzeit)

### Empfohlener Zeitplan:
- **Woche 1**: Phase 1-3 (Composables und Molecules)
- **Woche 2**: Phase 4-5 (Organisms und Migration)
- **Woche 3**: Phase 6-7 (Optimierung und Cleanup)

## Nächste Schritte

1. **Genehmigung dieses Plans** durch den Benutzer
2. **Wechsel in Code Mode** für die Implementierung
3. **Iterative Entwicklung** mit regelmäßigen Reviews
4. **Testing und Qualitätssicherung** in jeder Phase
5. **Production Deployment** nach erfolgreichem Testing

---
**Status**: Implementierungsplan erstellt  
**Empfohlener Start**: Mit Phase 1 (TypeScript Typen)  
**Risikobewertung**: Niedrig (dank Feature-Flags und schrittweisem Vorgehen)