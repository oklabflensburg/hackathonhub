# 2FA Integration Testing Documentation

## Übersicht

Diese Dokumentation beschreibt die vollständige Integration der Zwei-Faktor-Authentifizierung (2FA) in die Hackathon Hub Platform. Die Implementierung umfasst sowohl die Verwaltung von 2FA-Einstellungen als auch den Login-Flow mit 2FA.

## Implementierte Komponenten

### 1. Backend-API-Erweiterungen

#### Neue Endpunkte:
- `POST /api/auth/verify-2fa` - Verifiziert 2FA-Code nach initialem Login
- `POST /api/auth/verify-2fa-backup` - Verifiziert Backup-Code nach initialem Login

#### Erweiterte Endpunkte:
- `POST /api/auth/login` - Gibt jetzt `temp_token` zurück, wenn 2FA aktiviert ist

#### Neue Schemas:
- `TwoFactorLoginVerifyRequest` - Request für 2FA-Code-Verifizierung
- `TwoFactorBackupVerifyRequest` - Request für Backup-Code-Verifizierung
- `TwoFactorLoginResponse` - Response für erfolgreiche 2FA-Verifizierung

### 2. Frontend-Komponenten

#### Neue Komponenten:
- `TwoFactorStatus.vue` - Molekül-Komponente für 2FA-Statusanzeige
- `verify-2fa.vue` - Seite für 2FA-Verifizierung während Login

#### Erweiterte Komponenten:
- `SettingsContent.vue` - Integrierte 2FA-Verwaltung mit Modals
- `auth.ts` Store - Erweiterte Auth-Methoden für 2FA-Login

### 3. Service-Layer-Erweiterungen

#### EmailAuthService:
- `login_user()` - Generiert temporäre Tokens für 2FA-Login
- `verify_2fa_and_login()` - Verifiziert 2FA-Code mit temporärem Token
- `verify_2fa_backup_code()` - Verifiziert Backup-Code mit temporärem Token
- `_decode_temp_token()` - Hilfsfunktion für Token-Validierung

#### AuthService (Facade):
- `verify_2fa_and_login()` - Konsolidierte Methode für 2FA-Verifizierung
- `verify_2fa_backup_code()` - Konsolidierte Methode für Backup-Code-Verifizierung

## Test-Szenarien

### Szenario 1: 2FA-Einrichtung in den Einstellungen
1. Benutzer navigiert zu `/settings`
2. Wechselt zum Tab "Sicherheit"
3. Klickt auf "Zwei-Faktor-Authentifizierung aktivieren"
4. Scannt QR-Code mit Authenticator-App
5. Gibt 6-stelligen Code ein
6. Speichert Backup-Codes
7. 2FA ist jetzt aktiviert

### Szenario 2: Login mit 2FA
1. Benutzer gibt Email/Passwort ein
2. Backend erkennt 2FA ist aktiviert
3. Frontend erhält `requires_2fa: true` mit `temp_token`
4. Benutzer wird zu `/verify-2fa` weitergeleitet
5. Benutzer gibt 6-stelligen Code ein
6. Backend verifiziert Code mit `temp_token`
7. Login wird abgeschlossen, Session-Tokens werden gesetzt

### Szenario 3: Login mit Backup-Code
1. Benutzer hat keinen Zugriff auf Authenticator-App
2. Nach Schritt 3 oben klickt Benutzer auf "Backup-Code verwenden"
3. Benutzer gibt einen der gespeicherten Backup-Codes ein
4. Backend verifiziert Backup-Code
5. Verwendeter Backup-Code wird aus der Liste entfernt
6. Login wird abgeschlossen

### Szenario 4: 2FA-Deaktivierung
1. Benutzer navigiert zu Sicherheitseinstellungen
2. Klickt auf "Zwei-Faktor-Authentifizierung deaktivieren"
3. Gibt Passwort zur Bestätigung ein
4. 2FA wird deaktiviert, Backup-Codes werden ungültig

## API-Testfälle

### Testfall 1: Login mit 2FA-aktiviertem Benutzer
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Erwartete Antwort (2FA aktiviert):**
```json
{
  "requires_2fa": true,
  "user_id": 123,
  "temp_token": "eyJ1c2VyX2lkIjoxMjMsImVtYWlsIjoidXNlckBleGFtcGxlLmNvbSIs...",
  "message": "Two-factor authentication required"
}
```

### Testfall 2: 2FA-Code-Verifizierung
```http
POST /api/auth/verify-2fa
Content-Type: application/json

{
  "code": "123456",
  "temp_token": "eyJ1c2VyX2lkIjoxMjMsImVtYWlsIjoidXNlckBleGFtcGxlLmNvbSIs...",
  "remember_device": false
}
```

**Erwartete Antwort:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 123,
  "requires_2fa": false
}
```

### Testfall 3: Backup-Code-Verifizierung
```http
POST /api/auth/verify-2fa-backup
Content-Type: application/json

{
  "backup_code": "ABCD1234EFGH",
  "temp_token": "eyJ1c2VyX2lkIjoxMjMsImVtYWlsIjoidXNlckBleGFtcGxlLmNvbSIs..."
}
```

**Erwartete Antwort:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 123,
  "requires_2fa": false,
  "remaining_backup_codes": 9
}
```

## Sicherheitsaspekte

### Temporäre Tokens
- Gültig für 10 Minuten
- Enthalten User-ID, Email und Ablaufzeit
- Base64-urlsafe-kodiertes JSON
- Werden nach erfolgreicher Verifizierung ungültig

### Backup-Codes
- Werden bei Verwendung aus der Datenbank entfernt
- Großbuchstaben und Zahlen, 8-12 Zeichen
- Werden bei 2FA-Deaktivierung ungültig

### Rate Limiting
- Empfohlen: Maximal 5 Versuche pro Temp-Token
- Nach 5 Fehlversuchen: Temp-Token wird ungültig
- Benutzer muss Login-Prozess neu starten

## Frontend-Integrationstests

### Test 1: Settings-Integration
1. Navigiere zu `/settings`
2. Überprüfe, dass 2FA-Status korrekt angezeigt wird
3. Teste Setup/Disable-Modals
4. Verifiziere, dass Backup-Codes korrekt angezeigt werden

### Test 2: Login-Flow-Integration
1. Versuche Login mit 2FA-aktiviertem Benutzer
2. Überprüfe Weiterleitung zu `/verify-2fa`
3. Teste Code-Eingabe und Verifizierung
4. Teste Backup-Code-Alternative
5. Verifiziere, dass nach erfolgreicher Verifizierung zur Startseite weitergeleitet wird

## Bekannte Einschränkungen

1. **Device Remembering**: Die "Gerät merken" Funktion ist implementiert, aber die Device-Tokens werden noch nicht persistent gespeichert.
2. **Trusted Devices**: Die Anzeige vertrauenswürdiger Geräte in der Status-Komponente verwendet Platzhalterdaten.
3. **Push-Benachrichtigungen**: Bei 2FA-Login werden noch keine Push-Benachrichtigungen versendet.

## Nächste Schritte

1. **Device-Token-Speicherung**: Implementierung einer Datenbanktabelle für Device-Tokens
2. **Push-Benachrichtigungen**: Integration von Login-Benachrichtigungen bei 2FA
3. **Rate Limiting**: Implementierung von Rate-Limiting für 2FA-Versuche
4. **Recovery-Optionen**: Implementierung von Account-Recovery bei Verlust aller 2FA-Methoden

## Erfolgskriterien

- [x] 2FA kann in den Einstellungen aktiviert/deaktiviert werden
- [x] Login-Flow mit 2FA funktioniert korrekt
- [x] Backup-Codes können verwendet werden
- [x] Temporäre Tokens sind sicher und ablaufend
- [x] Frontend-Komponenten folgen Atomic Design Principles
- [x] API-Endpunkte sind dokumentiert und getestet
- [ ] E2E-Tests für kompletten 2FA-Flow
- [ ] Performance-Tests unter Last