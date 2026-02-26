# UPLOAD_DIR Fix - Implementierungs-TODO

## Phase 1: Diagnose (Sofort durchführbar)

### [ ] 1.1 Diagnose-Skript erstellen und ausführen
- **Datei**: `backend/check_upload_config.py`
- **Ziel**: Aktuelle Konfiguration und Berechtigungen prüfen
- **Aktion**: Skript in Code-Modus erstellen und ausführen

### [ ] 1.2 Umgebungsvariablen prüfen
- Prüfen, welche `.env`-Datei geladen wird
- `UPLOAD_DIR` in aktueller Umgebung überprüfen
- Prozessumgebung analysieren

### [ ] 1.3 Verzeichnisberechtigungen testen
- Existenz von `/opt/git/hackathonhub/backend/uploads`
- Schreibrechte für aktuellen Benutzer/Prozess
- Alternative: `./uploads` im Backend-Verzeichnis

## Phase 2: Konfiguration korrigieren

### [ ] 2.1 `.env`-Datei aktualisieren
- `UPLOAD_DIR=/opt/git/hackathonhub/backend/uploads` hinzufügen
- Oder alternativen Pfad konfigurieren
- Entwicklung vs. Produktion unterscheiden

### [ ] 2.2 Verzeichnis erstellen und Berechtigungen setzen
```bash
mkdir -p /opt/git/hackathonhub/backend/uploads
chmod 755 /opt/git/hackathonhub/backend/uploads
# Ggf. Benutzer anpassen: chown www-data:www-data ...
```

### [ ] 2.3 Docker/Container-Konfiguration prüfen
- Volumes in docker-compose.yml
- Environment variables in Container
- Mount-Points korrekt gesetzt

## Phase 3: Code-Konsistenz herstellen

### [ ] 3.1 FileUploadService auf settings umstellen
- **Datei**: `backend/app/utils/file_upload.py`
- **Änderung**: `os.getenv("UPLOAD_DIR")` durch `settings.UPLOAD_DIR` ersetzen
- **Import**: `from app.core.config import settings` hinzufügen

### [ ] 3.2 Logging verbessern
- `print` durch `logger.warning` ersetzen
- Detaillierte Fehlermeldungen hinzufügen
- Konfigurationsvalidierung beim Start

### [ ] 3.3 Fallback-Logik optional verbessern
- Mehrere Fallback-Optionen
- Bessere Diagnose-Informationen
- Konfigurations-Validation

## Phase 4: Testing und Validierung

### [ ] 4.1 Unit Test für FileUploadService
- Test für verschiedene Konfigurationen
- Test für Berechtigungsfehler
- Test für Fallback-Logik

### [ ] 4.2 Integrationstest für Upload
- Datei-Upload über API testen
- Verifizieren, dass Datei im korrekten Verzeichnis landet
- Statischer Zugriff testen

### [ ] 4.3 Manueller Test in Entwicklung
- Anwendung neu starten
- Upload durchführen
- Log auf Warnungen prüfen

## Phase 5: Deployment

### [ ] 5.1 Änderungen in Git committen
- Code-Änderungen
- Konfigurations-Änderungen
- Dokumentation aktualisieren

### [ ] 5.2 Produktions-Deployment vorbereiten
- Environment variables in Produktion setzen
- Verzeichnis auf Produktionsserver erstellen
- Berechtigungen anpassen

### [ ] 5.3 Monitoring einrichten
- Logs auf weitere Warnungen überwachen
- Upload-Verzeichnis-Größe monitorieren
- Fehler-Alerts konfigurieren

## Kurzanleitung für schnelle Lösung

### Option A: Einfachste Lösung (wenn Verzeichnis existiert)
1. `.env`-Datei öffnen und hinzufügen:
   ```
   UPLOAD_DIR=/opt/git/hackathonhub/backend/uploads
   ```
2. Anwendung neu starten

### Option B: Wenn Verzeichnis nicht existiert
1. Verzeichnis erstellen:
   ```bash
   sudo mkdir -p /opt/git/hackathonhub/backend/uploads
   sudo chown -R $(whoami):$(whoami) /opt/git/hackathonhub/backend/uploads
   ```
2. `.env`-Datei wie oben aktualisieren
3. Anwendung neu starten

### Option C: Temporäre Lösung (Fallback akzeptieren)
1. `/tmp/uploads` als legitimes Verzeichnis akzeptieren
2. Symbolic Link einrichten:
   ```bash
   ln -sf /opt/git/hackathonhub/backend/uploads /tmp/uploads
   ```

## Dringlichkeitsreihenfolge

1. **KRITISCH**: Diagnose durchführen (warum wird Fallback verwendet?)
2. **HOCH**: `.env`-Datei korrigieren
3. **HOCH**: Verzeichnisberechtigungen prüfen
4. **MITTEL**: Code-Konsistenz herstellen
5. **NIEDRIG**: Logging verbessern

## Erfolgsmetriken
- [ ] Keine "Using fallback upload directory" Warnungen im Log
- [ ] Uploads werden im korrekten Verzeichnis (`/opt/git/hackathonhub/backend/uploads/`) gespeichert
- [ ] Statische Dateien sind unter `http://domain/static/uploads/` erreichbar
- [ ] Berechtigungsfehler werden korrekt geloggt

## Risiko-Mitigation
- **Vor Änderungen**: Backup der aktuellen Upload-Dateien
- **Testing**: In Entwicklungsumgebung zuerst testen
- **Rollback**: Bereit sein, Änderungen rückgängig zu machen
- **Monitoring**: Nach Deployment Logs genau beobachten

## Notizen
- Der aktuelle Code verwendet zwei verschiedene Konfigurationsquellen (settings vs os.getenv)
- Das Problem tritt wahrscheinlich in der Produktionsumgebung auf
- Möglicherweise läuft der Prozess unter einem anderen Benutzer (www-data, nginx)
- Docker-Container könnten andere Pfade haben