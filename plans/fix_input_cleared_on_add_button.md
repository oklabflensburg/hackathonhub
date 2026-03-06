# Plan: Fix Input Cleared When User Presses "Add" Button

## Problembeschreibung
Auf der Seite `http://localhost:3001/create/hackathon` werden Eingabefelder geleert, wenn der Benutzer auf den "Add"-Button für Tags klickt. Das Problem tritt wahrscheinlich im Hackathon-Erstellungsformular auf.

## Analyse

### Betroffene Komponenten
1. `frontend3/app/pages/create/hackathon.vue` - Hauptseite
2. `frontend3/app/components/organisms/forms/HackathonForm.vue` - Formularkomponente
3. `frontend3/app/components/atoms/Input.vue` - Input-Komponente

### Aktueller Codefluss
1. Benutzer gibt einen Tag-Namen in das Input-Feld ein
2. Benutzer klickt auf "Add"-Button
3. `addTag()`-Funktion wird aufgerufen:
   - Validiert den Tag
   - Fügt Tag zu `formData.value.tags` hinzu
   - Setzt `newTag.value = ''` (leert das Input-Feld)
4. `formData`-Änderung löst Watch aus:
   - `watch(formData)` emittiert `update:modelValue`
   - Parent-Komponente aktualisiert `hackathonForm.value`
   - `watch(props.modelValue)` in HackathonForm setzt `formData.value` neu

### Mögliche Root Causes
1. **Event Propagation**: Button könnte Formular-Submit auslösen
2. **Reactivity Loop**: Watch-Zyklen führen zu unerwartetem Reset
3. **Formular-Reset**: `resetHackathonForm()` könnte fälschlicherweise aufgerufen werden
4. **Vue Re-rendering**: Komponente wird neu gerendert und verliert Fokus/Daten

## Lösungsstrategien

### Strategie 1: Event Propagation verhindern
- `@click.prevent` zum Button hinzufügen
- `event.preventDefault()` in `addTag()` aufrufen
- Button `type="button"` explizit setzen (bereits vorhanden)

### Strategie 2: Reactivity-Loop fixen
- `isUpdatingFromParent`-Flag überprüfen und optimieren
- Tiefe Kopien vermeiden, wo nicht nötig
- Watch `deep: true` nur für benötigte Properties

### Strategie 3: Formular-Struktur anpassen
- Tag-Adding-Bereich außerhalb des `<form>`-Elements platzieren
- Separate Event-Handling für Tags

### Strategie 4: State Management verbessern
- Tags als separates Prop/Event behandeln
- `v-model` für Tags anstelle von `formData`-Integration

## Implementierungsplan

### Phase 1: Debugging und Validierung
1. Konsolen-Logs hinzufügen, um Datenfluss zu verfolgen
2. Prüfen, welche Felder genau geleert werden
3. Browser-DevTools verwenden, um Event-Propagation zu überwachen

### Phase 2: Minimaler Fix
1. In `HackathonForm.vue`:
   - `addTag()`-Funktion: `event.preventDefault()` hinzufügen
   - Button: `@click.prevent="addTag"` setzen
   - `watch(formData)`-Logik überprüfen

2. In `create/hackathon.vue`:
   - Überflüssiges `newTag` Ref entfernen
   - `addTag`-Funktion entfernen (wird nicht verwendet)

### Phase 3: Erweiterte Korrekturen
1. Formular-Struktur überarbeiten:
   - Tags-Bereich in separate Komponente auslagern
   - Eigenes `v-model` für Tags implementieren

2. Reactivity optimieren:
   - `watch`-Tiefe auf notwendige Properties beschränken
   - `nextTick()` für Updates verwenden

### Phase 4: Testing
1. Manuelles Testen des Flows:
   - Tag hinzufügen, ohne dass andere Felder geleert werden
   - Formular-Submit funktioniert weiterhin
   - Reset-Button funktioniert korrekt

2. Edge Cases testen:
   - Mehrere Tags hintereinander hinzufügen
   - Tags entfernen
   - Formular mit Daten füllen, dann Tag hinzufügen

## Code-Änderungen

### Änderung 1: HackathonForm.vue
```vue
<!-- Button-Anpassung -->
<Button
  type="button"
  @click.prevent="addTag"
  variant="primary"
  class="rounded-l-none"
  :disabled="disabled || !newTag.trim()"
>
  {{ t('create.hackathonForm.fields.add') }}
</Button>

<!-- addTag-Funktion -->
const addTag = (event?: Event) => {
  if (event) event.preventDefault()
  console.log('addTag called, newTag:', newTag.value)
  if (newTag.value.trim() && !formData.value.tags.includes(newTag.value.trim())) {
    console.log('Adding tag:', newTag.value.trim())
    // Immutable update
    const updatedTags = [...formData.value.tags, newTag.value.trim()]
    formData.value = {
      ...formData.value,
      tags: updatedTags
    }
    newTag.value = ''
    console.log('Tags after add:', formData.value.tags)
  }
}
```

### Änderung 2: create/hackathon.vue
```vue
<!-- Entferne überflüssiges newTag Ref -->
// Entferne: const newTag = ref('')
// Entferne: addTag-Funktion (wird nicht verwendet)
```

### Änderung 3: Watch-Optimierung
```vue
// Statt deep watch auf formData, spezifische Properties beobachten
watch(() => [...formData.value.tags], (newTags, oldTags) => {
  if (isUpdatingFromParent) return
  if (JSON.stringify(newTags) !== JSON.stringify(oldTags)) {
    emit('update:modelValue', { ...formData.value, tags: newTags })
  }
})
```

## Risiken und Abhängigkeiten
1. **Risiko**: Änderungen an der Reactivity könnten andere Formular-Funktionen beeinträchtigen
2. **Abhängigkeit**: Vue 3 Reactivity-System muss korrekt funktionieren
3. **Testing**: Manuelles Testing erforderlich, da keine automatisierten Tests vorhanden

## Erfolgskriterien
- [ ] Tag hinzufügen leert nur das Tag-Input-Feld
- [ ] Andere Formularfelder bleiben unverändert
- [ ] Formular-Submit funktioniert weiterhin
- [ ] Reset-Button funktioniert korrekt
- [ ] Keine Konsolen-Fehler oder Warnungen

## Zeitplan
1. **Phase 1 (Debugging)**: 30 Minuten
2. **Phase 2 (Minimaler Fix)**: 45 Minuten
3. **Phase 3 (Erweiterte Korrekturen)**: 60 Minuten
4. **Phase 4 (Testing)**: 30 Minuten

## Notfallplan
Falls der Fix nicht funktioniert:
1. Zurück zu ursprünglichem Code
2. Alternative Implementierung: Tags als separate Komponente
3. Externes State Management (Pinia) für Formulardaten

## Dokumentation
- Änderungen in CHANGELOG.md dokumentieren
- Code-Kommentare hinzufügen, um Reactivity-Logik zu erklären
- Team über Fix informieren