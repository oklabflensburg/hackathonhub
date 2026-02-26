# UPLOAD_DIR Fallback Problem - Lösungsplan

## Problembeschreibung
Das Log zeigt: `WARNING: Using fallback upload directory: /tmp/uploads`

Die Anwendung verwendet `/tmp/uploads` anstatt des konfigurierten Verzeichnisses `/opt/git/hackathonhub/backend/uploads`.

## Root Cause Analyse

### 1. Inkonsistente Konfigurationsquellen
- **`main.py`**: Verwendet `settings.UPLOAD_DIR` (aus Pydantic Settings)
- **`FileUploadService`**: Verwendet `os.getenv("UPLOAD_DIR")` (direkt aus Prozessumgebung)

### 2. Umgebungsvariable nicht korrekt gesetzt
- `UPLOAD_DIR` muss in der `.env`-Datei gesetzt sein
- Pydantic lädt `.env`, aber `os.getenv` benötigt die Variable im Prozess-Environment
- Mögliche Unterschiede zwischen Entwicklung und Produktion

### 3. Berechtigungsprobleme
- Verzeichnis `/opt/git/hackathonhub/backend/uploads` existiert nicht
- Prozessbenutzer hat keine Schreibrechte
- Parent-Verzeichnis nicht beschreibbar

### 4. Code-Review-Ergebnisse
- `FileUploadService.__init__` (Zeilen 14-30):
  ```python
  default_dir = "./uploads"
  upload_dir = os.getenv("UPLOAD_DIR", default_dir)
  # Wenn upload_dir leer oder nicht beschreibbar → Fallback zu /tmp/uploads
  ```
- `main.py` (Zeile 59):
  ```python
  upload_dir = Path(settings.UPLOAD_DIR)  # Verwendet settings
  ```

## Lösungsstrategie

### Phase 1: Diagnose (Sofort)
1. **Umgebungsprüfung**: Testskript zur Überprüfung von:
   - `os.getenv("UPLOAD_DIR")`
   - `settings.UPLOAD_DIR`
   - Verzeichnisexistenz und -berechtigungen
   - Aktuelles Arbeitsverzeichnis

2. **Log-Analyse**: 
   - Welche `.env`-Datei wird geladen?
   - Welcher Benutzer führt den Prozess aus?
   - Vollständiger Pfad des verwendeten Verzeichnisses

### Phase 2: Konfigurationskonsistenz
1. **Einheitliche Konfigurationsquelle**:
   - Option A: `FileUploadService` auf `settings.UPLOAD_DIR` umstellen
   - Option B: Sicherstellen, dass `UPLOAD_DIR` in Prozessumgebung gesetzt ist

2. **`.env`-Datei validieren**:
   - `UPLOAD_DIR=/opt/git/hackathonhub/backend/uploads` hinzufügen
   - Absolute vs. relative Pfade klären
   - Entwicklung vs. Produktion unterscheiden

### Phase 3: Verzeichnisbereitstellung
1. **Verzeichnis erstellen** (falls nicht existent):
   ```bash
   sudo mkdir -p /opt/git/hackathonhub/backend/uploads
   ```

2. **Berechtigungen setzen**:
   ```bash
   sudo chown -R $(whoami):$(whoami) /opt/git/hackathonhub/backend/uploads
   sudo chmod -R 755 /opt/git/hackathonhub/backend/uploads
   ```

3. **Prozessbenutzer berücksichtigen**:
   - Wenn Dienst als `www-data` oder `nginx` läuft
   - Gruppenberechtigungen entsprechend setzen

### Phase 4: Code-Verbesserungen
1. **`FileUploadService` refactoren**:
   ```python
   # Statt os.getenv("UPLOAD_DIR")
   from app.core.config import settings
   upload_dir = settings.UPLOAD_DIR
   ```

2. **Bessere Fehlerbehandlung**:
   - Detaillierte Logging statt `print`
   - Spezifische Fehlermeldungen für verschiedene Fehlerursachen
   - Konfigurationsvalidierung beim Start

3. **Fallback-Logik verbessern**:
   - Mehrere Fallback-Optionen (z.B. `./uploads`, `$HOME/uploads`)
   - Bessere Diagnose-Informationen im Log

### Phase 5: Testing und Validierung
1. **Unit Tests** für `FileUploadService`
2. **Integrationstest** für Upload-Funktionalität
3. **Konfigurationstest** für verschiedene Umgebungen

## Detaillierte Implementierungsschritte

### Schritt 1: Diagnose-Skript erstellen
```python
# backend/check_upload_config.py
import os
from pathlib import Path
from app.core.config import settings

def diagnose():
    print("UPLOAD_DIR Diagnosis:")
    print(f"os.getenv('UPLOAD_DIR'): {os.getenv('UPLOAD_DIR')}")
    print(f"settings.UPLOAD_DIR: {settings.UPLOAD_DIR}")
    
    # Check directory
    dir_path = Path(settings.UPLOAD_DIR)
    print(f"Directory: {dir_path.absolute()}")
    print(f"Exists: {dir_path.exists()}")
    
    # Check writable
    try:
        test_file = dir_path / ".test"
        test_file.touch()
        test_file.unlink()
        print("Writable: YES")
    except Exception as e:
        print(f"Writable: NO - {e}")
```

### Schritt 2: Konfiguration vereinheitlichen
**Datei**: `backend/app/utils/file_upload.py`
```python
from app.core.config import settings  # Am Anfang hinzufügen

class FileUploadService:
    def __init__(self):
        # Verwende settings.UPLOAD_DIR statt os.getenv
        upload_dir = settings.UPLOAD_DIR
        
        # Rest der Logik bleibt gleich
        upload_path = Path(upload_dir)
        # ...
```

### Schritt 3: `.env`-Datei aktualisieren
Zur `.env`-Datei hinzufügen:
```
UPLOAD_DIR=/opt/git/hackathonhub/backend/uploads
```

### Schritt 4: Verzeichnis und Berechtigungen
```bash
# Verzeichnis erstellen
mkdir -p /opt/git/hackathonhub/backend/uploads

# Berechtigungen setzen (anpassen an Prozessbenutzer)
sudo chown -R $USER:$USER /opt/git/hackathonhub/backend/uploads
chmod -R 755 /opt/git/hackathonhub/backend/uploads
```

### Schritt 5: Logging verbessern
```python
import logging
logger = logging.getLogger(__name__)

class FileUploadService:
    def __init__(self):
        # ...
        if not upload_dir or not self._is_writable(upload_path):
            tmp_upload = Path("/tmp/uploads")
            tmp_upload.mkdir(parents=True, exist_ok=True)
            upload_dir = str(tmp_upload)
            logger.warning(
                f"Using fallback upload directory: {upload_dir}. "
                f"Configured directory {settings.UPLOAD_DIR} is not writable or not set."
            )
```

## Prioritätsreihenfolge

1. **Hoch**: Diagnose durchführen (warum wird Fallback verwendet?)
2. **Hoch**: `.env`-Datei korrigieren und Umgebungsvariable setzen
3. **Mittel**: Verzeichnisberechtigungen prüfen und korrigieren
4. **Mittel**: Code-Konsistenz herstellen (settings statt os.getenv)
5. **Niedrig**: Logging und Fehlerbehandlung verbessern

## Erfolgskriterien
- Keine "Using fallback upload directory" Warnungen im Log
- Uploads werden im korrekten Verzeichnis gespeichert
- Statische Dateien sind unter `/static/uploads/` erreichbar
- Konfiguration ist konsistent zwischen Entwicklung und Produktion

## Risiken und Mitigation
- **Risiko**: Brechende Änderungen für bestehende Uploads
  - **Mitigation**: Migration bestehender Dateien oder symlink einrichten
- **Risiko**: Berechtigungsprobleme in Produktion
  - **Mitigation**: Docker-Volumes korrekt konfigurieren
- **Risiko**: Unterschiedliche Pfade in verschiedenen Umgebungen
  - **Mitigation**: Environment-spezifische `.env`-Dateien verwenden

## Notfall-Fallback
Falls das Problem nicht sofort gelöst werden kann:
1. Temporär `/tmp/uploads` als legitimes Verzeichnis akzeptieren
2. Cron-Job einrichten, der Dateien regelmäßig ins richtige Verzeichnis verschiebt
3. Symbolic Link von `/tmp/uploads` zum gewünschten Verzeichnis

## Nächste Schritte
1. Diagnose-Skript ausführen
2. Ergebnisse analysieren
3. Spezifische Korrektur basierend auf Diagnose implementieren
4. Testing in Entwicklungsumgebung
5. Deployment in Produktion