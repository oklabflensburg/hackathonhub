# OAuth Refresh Token Fix - Implementierungsdokumentation

## Problembeschreibung

Bei der Authentifizierung mit Google oder GitHub OAuth wurden nur `access_token` an das Frontend gesendet, nicht aber `refresh_token`. Dies führte dazu, dass die Token-Refresh-Logik nicht funktionierte, da das Frontend keinen Refresh-Token hatte, um neue Access-Tokens anzufordern.

## Ursache

1. **Backend**: Die Callback-Routen (`google_callback` und `github_callback`) in `backend/app/api/v1/auth/routes.py` gaben nur den `access_token` im Query-Parameter weiter.
2. **Frontend**: Die `initializeAuth` Funktion in `frontend3/app/stores/auth.ts` setzte den `refresh_token` auf einen leeren String, wenn der Token aus der URL kam.

## Lösung

Implementierung der Query-Parameter-Lösung, bei der beide Tokens (`access_token` und `refresh_token`) als Query-Parameter an das Frontend gesendet werden.

### Backend-Änderungen

**Datei**: `backend/app/api/v1/auth/routes.py`

#### Google OAuth Callback (Zeilen 167-217)
- **Vorher**: `?token={token}&source=google`
- **Nachher**: `?access_token={access_token}&refresh_token={refresh_token}&source=google`

#### GitHub OAuth Callback (Zeilen 368-440)
- **Vorher**: `?token={token}&source=github`
- **Nachher**: `?access_token={access_token}&refresh_token={refresh_token}&source=github`

### Frontend-Änderungen

**Datei**: `frontend3/app/stores/auth.ts`

#### `initializeAuth` Funktion (Zeilen 552-612)
- **Vorher**: Liest nur `token` Parameter aus der URL
- **Nachher**: Liest sowohl `access_token` als auch `refresh_token` Parameter aus der URL
- **Vorher**: Setzt `refresh_token` auf leeren String: `preferences.auth.setTokens(urlToken, '')`
- **Nachher**: Setzt beide Tokens korrekt: `preferences.auth.setTokens(accessToken, refreshTokenParam || '')`

## Technische Details

### URL-Encoding
Beide Tokens werden URL-encoded, um Sonderzeichen sicher zu übertragen:
```python
access_token = urllib.parse.quote(result["access_token"])
refresh_token = urllib.parse.quote(result.get("refresh_token", ""))
```

### Abwärtskompatibilität
Die Lösung behält den `source` Parameter bei, um die Quelle der Authentifizierung (google/github) zu identifizieren.

### Sicherheitsaspekte
- **Aktuelle Lösung**: Tokens werden in Query-Parametern übertragen (in Browser-History sichtbar)
- **Empfohlene Verbesserung**: Später auf Fragment-Identifier oder Token-Austausch-Endpunkt umstellen

## Testen

Die Änderungen wurden mit einem Testskript validiert, das folgende Aspekte überprüft:
1. Korrekte URL-Generierung mit beiden Tokens
2. Korrektes URL-Encoding und -Decoding
3. Korrekte Parameter-Parsing im Frontend

## Auswirkungen

### Positive Auswirkungen
1. **Funktionierende Token-Refresh-Logik**: Das Frontend kann jetzt Refresh-Tokens verwenden, um abgelaufene Access-Tokens zu erneuern
2. **Bessere Benutzererfahrung**: Benutzer bleiben länger angemeldet, ohne sich neu authentifizieren zu müssen
3. **Konsistenz**: OAuth-Logins verhalten sich jetzt wie Email-Logins (beide geben Refresh-Tokens zurück)

### Zu beachtende Punkte
1. **Sicherheit**: Tokens sind in der Browser-History sichtbar (wie zuvor auch)
2. **URL-Länge**: Längere URLs durch zusätzliche Parameter

## Zukünftige Verbesserungen

1. **Fragment-Identifier**: Tokens im URL-Fragment (`#`) statt Query-Parametern übertragen
2. **Token-Austausch-Endpunkt**: Backend-Endpunkt, der Tokens gegen einen einmaligen Code austauscht
3. **HTTP-Only Cookies**: Tokens als sichere HTTP-Only Cookies setzen

## Rollback-Anleitung

Falls Probleme auftreten, können die Änderungen wie folgt rückgängig gemacht werden:

### Backend-Rollback
1. In `backend/app/api/v1/auth/routes.py` die Callback-Routen auf die ursprüngliche Version zurücksetzen
2. `?token={token}&source=...` statt `?access_token=...&refresh_token=...&source=...` verwenden

### Frontend-Rollback
1. In `frontend3/app/stores/auth.ts` die `initializeAuth` Funktion auf die ursprüngliche Version zurücksetzen
2. `urlParams.get('token')` statt `urlParams.get('access_token')` verwenden
3. `preferences.auth.setTokens(urlToken, '')` beibehalten

## Verantwortliche Dateien

1. `backend/app/api/v1/auth/routes.py` - Backend Callback-Routen
2. `frontend3/app/stores/auth.ts` - Frontend Auth Store
3. `backend/app/services/google_oauth_service.py` - Google OAuth Service (unverändert, gab bereits beide Tokens zurück)
4. `backend/app/services/github_oauth_service.py` - GitHub OAuth Service (unverändert, gab bereits beide Tokens zurück)

## Autor

Implementiert als Teil der Task: "when user authenticates with google or github do the same as login with email in case no access_token and refresh_token is sent to frontend"

**Datum**: 25. Februar 2026
**Status**: Implementiert und getestet