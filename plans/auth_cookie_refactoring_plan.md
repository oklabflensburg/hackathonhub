# Authentifizierungs-Refactoring: HTTP-Only Cookies für SSR

## Problemstellung
Die aktuelle Authentifizierung verwendet JWT-Tokens, die im Frontend in `localStorage` gespeichert werden. Dies führt zu:
1. **Hydration-Mismatches**: Der Auth-Store kann auf dem Server nicht auf `localStorage` zugreifen, daher ist `isAuthenticated` auf dem Server `false`, auf dem Client möglicherweise `true`.
2. **Geschützte Seiten werden kurz gerendert**: Nicht authentifizierte Benutzer sehen geschützte Seiten kurz, bevor die clientseitige Umleitung erfolgt.
3. **SSR-Inkompatibilität**: Server-seitiges Rendering kann den Authentifizierungszustand nicht korrekt bestimmen.

## Lösung
Verwendung von **HTTP-Only Cookies** für die Authentifizierung:
- Tokens werden vom Backend als HTTP-Only Cookies gesetzt.
- Cookies werden automatisch mit jeder Request an das Backend gesendet.
- Der Frontend kann Cookies auf dem Server lesen (via `useCookie`).
- Keine Hydration-Mismatches, da Server und Client den gleichen Authentifizierungszustand sehen.

## Backend-Änderungen

### 1. Cookie-Hilfsfunktionen
Erstelle eine neue Datei `backend/app/utils/cookies.py`:
```python
from fastapi import Response
from datetime import datetime, timedelta

def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
    max_age_access: int = 3600,  # 1 hour
    max_age_refresh: int = 604800  # 7 days
):
    """Set HTTP-only cookies for authentication tokens."""
    response.set_cookie(
        key="auth_token",
        value=access_token,
        max_age=max_age_access,
        httponly=True,
        secure=True,  # In production
        samesite="lax",
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=max_age_refresh,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )

def clear_auth_cookies(response: Response):
    """Clear authentication cookies."""
    response.delete_cookie(key="auth_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")
```

### 2. Login-Routen anpassen
Ändere `backend/app/api/v1/auth/routes.py`:
- Importiere `set_auth_cookies`
- Ändere die Login-Endpoints, um Cookies zu setzen und dennoch JSON zu retournieren (für Abwärtskompatibilität).

```python
from app.utils.cookies import set_auth_cookies, clear_auth_cookies

@router.post("/login", response_model=TokenWithRefresh)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale),
    response: Response = None  # FastAPI injects Response
):
    # ... existing authentication logic ...
    
    # Create response with tokens
    token_response = TokenWithRefresh(
        access_token=auth_result.get("access_token", ""),
        refresh_token=auth_result.get("refresh_token", ""),
        token_type=auth_result.get("token_type", "bearer")
    )
    
    # Set HTTP-only cookies
    set_auth_cookies(
        response,
        access_token=auth_result.get("access_token", ""),
        refresh_token=auth_result.get("refresh_token", "")
    )
    
    return token_response
```

### 3. Logout-Route anpassen
```python
@router.post("/logout")
async def logout(response: Response):
    clear_auth_cookies(response)
    return {"message": "Logged out successfully"}
```

### 4. Token-Validierung über Cookies
Optional: Ändere die `oauth2_scheme`-Abhängigkeit, um Tokens aus Cookies zu lesen, falls der Authorization-Header fehlt.

## Frontend-Änderungen

### 1. Auth-Store anpassen (`frontend3/app/stores/auth.ts`)
- Ändere `initializeAuth()`, um Tokens aus Cookies zu lesen (via `useCookie`).
- Speichere Tokens weiterhin in `localStorage` für Abwärtskompatibilität.
- Entferne die client-seitige Token-Logik aus URLs (OAuth-Callback).

### 2. Preferences-Store anpassen (`frontend3/app/stores/preferences.ts`)
- Ändere `SSRStorage`, um Auth-Tokens aus Cookies zu lesen/schreiben.
- Verwende `useCookie` für `auth_token` und `refresh_token`.

### 3. Middleware anpassen (`frontend3/app/middleware/auth.ts`)
- Verwende `useCookie` auf Server und Client, um den Authentifizierungszustand zu prüfen.
- Entferne die client-seitige Einschränkung (`process.server`-Check).

### 4. API-Client anpassen
- Stelle sicher, dass Tokens nicht manuell in Headers gesetzt werden (Cookies werden automatisch gesendet).
- Falls nötig, füge Fallback-Logik für `localStorage`-Tokens hinzu.

## Migrationsstrategie
1. **Phase 1**: Backend setzt Cookies zusätzlich zu JSON-Response (abwärtskompatibel).
2. **Phase 2**: Frontend liest Tokens primär aus Cookies, fallback auf `localStorage`.
3. **Phase 3**: Frontend speichert Tokens nicht mehr in `localStorage`.
4. **Phase 4**: Backend validiert Tokens nur noch aus Cookies (optional).

## Testing
1. **Login/Logout Flow**: Teste, ob Cookies gesetzt/gelöscht werden.
2. **Geschützte Seiten**: Teste SSR mit authentifizierten/nicht authentifizierten Benutzern.
3. **Hydration**: Überprüfe, dass keine Hydration-Warnungen mehr auftreten.
4. **Cross-Tab Synchronisation**: Cookies sind automatisch synchronisiert.

## Risiken und Abwärtskompatibilität
- **Risiko**: Ältere Clients, die keine Cookies unterstützen, können sich nicht authentifizieren.
- **Lösung**: Behalte JSON-Response bei und verwende Hybrid-Ansatz.
- **CSRF-Schutz**: HTTP-Only Cookies sind gegen XSS sicher, benötigen aber CSRF-Token für state-changing Requests.
- **CORS**: Cookies erfordern korrekte CORS-Konfiguration (`credentials: 'include'`).

## Zeitplan
1. Backend-Änderungen: 2-3 Stunden
2. Frontend-Änderungen: 2-3 Stunden
3. Testing und Bugfixing: 1-2 Stunden
4. Deployment und Monitoring: 1 Stunde

## Erfolgskriterien
- Keine Hydration-Warnungen bei Login/Logout oder geschützten Seiten.
- Geschützte Seiten werden auf dem Server nicht gerendert für nicht authentifizierte Benutzer.
- Authentifizierungsfluss funktioniert weiterhin (Login, Logout, Token-Refresh).
- Abwärtskompatibilität mit bestehenden Clients gewährleistet.