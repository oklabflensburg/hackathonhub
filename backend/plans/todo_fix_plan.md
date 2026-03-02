# Plan zur Behebung von TODOs im Backend

## Analyseergebnisse

### Gefundene TODOs
1. **Explizites TODO** in [`backend/app/api/v1/projects/routes.py:113`](backend/app/api/v1/projects/routes.py:113):
   - `# TODO: Move permission logic to service layer`
   - Betrifft die `update_project`-Route, die direkt `ProjectRepository` importiert, um Besitz zu prüfen
   - Gleiches Problem existiert in `delete_project` (ohne explizites TODO)

2. **Architektur-TODOs** (aus `BACKEND_REFACTORING_SUMMARY.md`):
   - Phase 2A: API-Routen sollten Service-Klassen statt Repositories verwenden
   - Phase 2B: Legacy-Code-Bereinigung
   - Phase 2C: Finale Integration
   - Phase 3: Erweiterte Features
   - Phase 4: Performance-Optimierung

3. **Repository-Direktimporte** in folgenden Dateien:
   - `projects/routes.py` (mehrfach)
   - `teams/routes.py`
   - `hackathons/routes.py`
   - `users/routes.py`
   - `me/routes.py`
   - `notifications/routes.py`
   - `comments/routes.py`
   - `compatibility/routes.py`
   - `notification_types/routes.py`

## Priorisierte Aktionspunkte

### Hochpriorität (unmittelbare Code-Korrekturen)

#### 1. Berechtigungslogik in Service-Schicht verschieben
**Datei**: `backend/app/api/v1/projects/routes.py`
**Betroffene Funktionen**:
- `update_project` (Zeile 97-125)
- `delete_project` (Zeile 128-151)

**Lösungsansatz**:
- Berechtigungsprüfung in `project_service.py` hinzufügen
- Service-Methoden `update_project` und `delete_project` um `user_id`-Parameter erweitern
- Service prüft Besitz und wirft entsprechende Exceptions
- Routen rufen Service mit `current_user.id` auf

**Erforderliche Änderungen**:
1. `app/services/project_service.py`:
   - `update_project` um `user_id` erweitern
   - `delete_project` um `user_id` erweitern
   - Besitzprüfung vor Operation durchführen
   - `ForbiddenError` oder ähnliche Exception werfen

2. `app/api/v1/projects/routes.py`:
   - Repository-Importe entfernen (Zeilen 114-115, 138-139)
   - Direkte Repository-Aufrufe durch Service-Aufrufe ersetzen
   - Exception-Handling anpassen

#### 2. Konsistente Service-Nutzung in allen Routen
**Ziel**: Alle API-Routen sollen Services statt Repositories verwenden

**Vorgehen**:
1. Inventarisierung aller Repository-Importe in Routen
2. Prüfen, ob entsprechende Service-Methoden existieren
3. Fehlende Service-Methoden implementieren
4. Routen auf Service-Aufrufe umstellen

### Mittelpriorität (Architektur-Verbesserungen)

#### 3. Phase 2A aus BACKEND_REFACTORING_SUMMARY.md umsetzen
- API-Routen auf Service-Klassen umstellen
- `auth_service.py` Facade für konsolidierte Authentifizierung erstellen
- Sicherstellen, dass alle Geschäftslogik in Service-Schicht liegt

#### 4. Phase 2B: Legacy-Code-Bereinigung
- Alte `crud.py`, `models.py`, `schemas.py` Dateien entfernen
- Alte Service-Importe aktualisieren
- Testdateien auf neue Struktur umstellen

### Niedrigpriorität (Langfristige Verbesserungen)

#### 5. Phase 2C, 3, 4
- Finale Integration
- WebSocket für Echtzeit-Benachrichtigungen
- Caching, Rate Limiting, Performance-Optimierung

## Detaillierter Implementierungsplan für Hochpriorität

### Schritt 1: Project Service erweitern

**Datei**: `app/services/project_service.py`

```python
def update_project(self, db: Session, project_id: int, project_update: ProjectUpdate, user_id: int) -> Optional[Project]:
    """Update a project with ownership check."""
    project = self.project_repository.get(db, project_id)
    if not project:
        return None
    
    # Check ownership
    if project.owner_id != user_id:
        raise ForbiddenError("Not authorized to update this project")
    
    # Update logic...
    return updated_project

def delete_project(self, db: Session, project_id: int, user_id: int) -> bool:
    """Delete a project with ownership check."""
    project = self.project_repository.get(db, project_id)
    if not project:
        return False
    
    # Check ownership
    if project.owner_id != user_id:
        raise ForbiddenError("Not authorized to delete this project")
    
    # Delete logic...
    return True
```

### Schritt 2: Project Routes anpassen

**Datei**: `app/api/v1/projects/routes.py`

```python
# Entfernen:
# from app.repositories.project_repository import ProjectRepository
# project_repo = ProjectRepository()

# In update_project:
updated_project = project_service.update_project(
    db, project_id, project_update, current_user.id
)

# In delete_project:
success = project_service.delete_project(db, project_id, current_user.id)
```

### Schritt 3: Exception-Handling

**Option**: Bestehende `raise_forbidden`-Funktion verwenden oder Service-spezifische Exception einführen.

## Zeitplan und Aufwand

**Hochpriorität (1-2 Tage)**:
- Project Service und Routes anpassen
- Tests aktualisieren

**Mittelpriorität (3-5 Tage)**:
- Alle anderen Routen auf Services umstellen
- Legacy-Code bereinigen

**Niedrigpriorität (1-2 Wochen)**:
- Langfristige Architekturverbesserungen

## Risiken und Abhängigkeiten

1. **Bestehende Tests**: Müssen angepasst werden
2. **Frontend-Kompatibilität**: API-Schnittstellen bleiben gleich
3. **Datenbank-Schema**: Keine Änderungen erforderlich
4. **Team-Koordination**: Andere Entwickler müssen über Änderungen informiert werden

## Erfolgskriterien

- [ ] Explizites TODO in `projects/routes.py` behoben
- [ ] Alle Repository-Importe in Routen durch Service-Aufrufe ersetzt
- [ ] Bestehende Tests passieren
- [ ] Keine Regression in API-Endpoints
- [ ] Code-Coverage bleibt gleich oder verbessert sich

## Nächste Schritte

1. Benutzer-Feedback zu diesem Plan einholen
2. Bei Zustimmung in Code-Mode wechseln
3. Implementierung Schritt für Schritt durchführen
4. Tests nach jedem Schritt ausführen
5. Dokumentation aktualisieren