# Backend-API-Erweiterungen für /settings Seite

## Übersicht
Dieses Dokument beschreibt die erforderlichen Backend-API-Erweiterungen für die vollständige /settings Seite.

## Bestehende API-Endpoints

### Benutzer-API (`/api/v1/users`)
- `GET /users/me` - Aktuelles Benutzerprofil
- `PATCH /users/me` - Profil aktualisieren (username, email, name, avatar_url, bio, location, company)

### Benachrichtigungs-API (`/api/v1/notifications`)
- `GET /notifications/preferences` - Benachrichtigungseinstellungen abrufen
- `PUT /notifications/preferences` - Benachrichtigungseinstellungen aktualisieren

### Upload-API (`/api/v1/uploads`)
- `POST /uploads/avatar` - Avatar hochladen

## Erforderliche Neue API-Endpoints

### 1. Erweiterte Benutzer-Einstellungen (`/api/v1/users/settings`)

#### `GET /users/me/settings`
**Beschreibung**: Alle Benutzereinstellungen abrufen
**Response**:
```json
{
  "profile": {
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe",
    "avatar_url": "https://...",
    "bio": "Software developer",
    "location": "Berlin, Germany",
    "company": "Tech Corp"
  },
  "security": {
    "two_factor_enabled": false,
    "active_sessions": [
      {
        "id": "session_123",
        "device": "Chrome on Windows",
        "location": "Berlin, DE",
        "last_active": "2024-01-15T10:30:00Z",
        "current": true
      }
    ]
  },
  "privacy": {
    "profile_visibility": "public",
    "email_visibility": "private",
    "show_online_status": true,
    "allow_messages_from": "all_users"
  },
  "platform": {
    "theme": "dark",
    "language": "en",
    "timezone": "Europe/Berlin",
    "date_format": "DD/MM/YYYY",
    "notifications_sound": true,
    "reduce_animations": false
  },
  "notifications": {
    "email_enabled": true,
    "push_enabled": true,
    "in_app_enabled": true,
    "categories": {
      "project_updates": true,
      "team_invitations": true,
      "hackathon_announcements": true,
      "comment_replies": true,
      "vote_notifications": true
    }
  },
  "connections": {
    "github": {
      "connected": true,
      "username": "johndoe",
      "avatar_url": "https://..."
    },
    "google": {
      "connected": false
    }
  }
}
```

#### `PUT /users/me/settings`
**Beschreibung**: Alle oder teilweise Einstellungen aktualisieren
**Request Body**:
```json
{
  "profile": {
    "name": "Updated Name",
    "bio": "Updated bio"
  },
  "privacy": {
    "profile_visibility": "friends_only"
  },
  "platform": {
    "theme": "light"
  }
}
```
**Response**: Aktualisierte Einstellungen (wie GET)

#### `PATCH /users/me/settings/{section}`
**Beschreibung**: Spezifischen Einstellungsbereich aktualisieren
**Path Parameter**: `section` (profile, security, privacy, platform, notifications, connections)
**Request Body**: Bereichsspezifisches Update-Objekt

### 2. Sicherheits-API (`/api/v1/users/security`)

#### `POST /users/me/security/password`
**Beschreibung**: Passwort ändern
**Request Body**:
```json
{
  "current_password": "oldPassword123",
  "new_password": "newPassword456"
}
```

#### `POST /users/me/security/two-factor/enable`
**Beschreibung**: 2FA aktivieren
**Response**:
```json
{
  "qr_code": "data:image/png;base64,...",
  "secret": "JBSWY3DPEHPK3PXP",
  "backup_codes": ["code1", "code2", ...]
}
```

#### `POST /users/me/security/two-factor/disable`
**Beschreibung**: 2FA deaktivieren
**Request Body**:
```json
{
  "password": "userPassword123"
}
```

#### `GET /users/me/security/sessions`
**Beschreibung**: Aktive Sitzungen abrufen

#### `DELETE /users/me/security/sessions/{session_id}`
**Beschreibung**: Spezifische Sitzung beenden

#### `DELETE /users/me/security/sessions/other`
**Beschreibung**: Alle anderen Sitzungen beenden

### 3. OAuth-Verbindungen (`/api/v1/users/connections`)

#### `GET /users/me/connections`
**Beschreibung**: Alle OAuth-Verbindungen abrufen

#### `DELETE /users/me/connections/{provider}`
**Beschreibung**: OAuth-Verbindung trennen (provider: github, google)
**Request Body** (optional):
```json
{
  "password": "userPassword123"
}
```

### 4. Datenschutz-API (`/api/v1/users/privacy`)

#### `GET /users/me/privacy`
**Beschreibung**: Datenschutzeinstellungen abrufen

#### `PUT /users/me/privacy`
**Beschreibung**: Datenschutzeinstellungen aktualisieren

#### `POST /users/me/privacy/export`
**Beschreibung**: Datenexport anfordern
**Response**:
```json
{
  "request_id": "export_123",
  "status": "pending",
  "estimated_completion": "2024-01-16T10:30:00Z"
}
```

#### `DELETE /users/me/privacy/account`
**Beschreibung**: Account löschen anfordern
**Request Body**:
```json
{
  "password": "userPassword123",
  "confirmation": "DELETE MY ACCOUNT"
}
```

### 5. Platform-Einstellungen (`/api/v1/users/preferences`)

#### `GET /users/me/preferences`
**Beschreibung**: Platform-Einstellungen abrufen

#### `PUT /users/me/preferences`
**Beschreibung**: Platform-Einstellungen aktualisieren

## Datenbank-Erweiterungen

### Neue Tabellen

#### `user_settings` (Erweiterung der user Tabelle)
```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS (
  theme VARCHAR(20) DEFAULT 'system',
  language VARCHAR(10) DEFAULT 'en',
  timezone VARCHAR(50) DEFAULT 'UTC',
  date_format VARCHAR(20) DEFAULT 'YYYY-MM-DD',
  notifications_sound BOOLEAN DEFAULT TRUE,
  reduce_animations BOOLEAN DEFAULT FALSE,
  profile_visibility VARCHAR(20) DEFAULT 'public',
  email_visibility VARCHAR(20) DEFAULT 'private',
  show_online_status BOOLEAN DEFAULT TRUE,
  allow_messages_from VARCHAR(20) DEFAULT 'all_users',
  two_factor_secret VARCHAR(32),
  two_factor_backup_codes TEXT,
  two_factor_enabled BOOLEAN DEFAULT FALSE,
  data_export_requested_at TIMESTAMP,
  account_deletion_requested_at TIMESTAMP
);
```

#### `user_sessions`
```sql
CREATE TABLE IF NOT EXISTS user_sessions (
  id VARCHAR(64) PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  device_info TEXT,
  user_agent TEXT,
  ip_address INET,
  location VARCHAR(100),
  last_active TIMESTAMP NOT NULL DEFAULT NOW(),
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at);
```

#### `notification_preferences` (bereits vorhanden, möglicherweise erweitern)
```sql
-- Bereits vorhanden, sicherstellen dass alle benötigten Felder existieren
```

## Pydantic Schemas

### Neue Schemas in `backend/app/domain/schemas/user.py`

```python
class UserSettings(BaseModel):
    profile: ProfileSettings
    security: SecuritySettings
    privacy: PrivacySettings
    platform: PlatformPreferences
    notifications: NotificationSettings
    connections: OAuthConnections

class ProfileSettings(BaseModel):
    username: str
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None

class SecuritySettings(BaseModel):
    two_factor_enabled: bool = False
    active_sessions: List[UserSession] = []

class PrivacySettings(BaseModel):
    profile_visibility: Literal["public", "friends_only", "private"] = "public"
    email_visibility: Literal["public", "friends_only", "private"] = "private"
    show_online_status: bool = True
    allow_messages_from: Literal["all_users", "friends_only", "none"] = "all_users"

class PlatformPreferences(BaseModel):
    theme: Literal["light", "dark", "system"] = "system"
    language: str = "en"
    timezone: str = "UTC"
    date_format: str = "YYYY-MM-DD"
    notifications_sound: bool = True
    reduce_animations: bool = False

class NotificationSettings(BaseModel):
    email_enabled: bool = True
    push_enabled: bool = True
    in_app_enabled: bool = True
    categories: NotificationCategories

class NotificationCategories(BaseModel):
    project_updates: bool = True
    team_invitations: bool = True
    hackathon_announcements: bool = True
    comment_replies: bool = True
    vote_notifications: bool = True

class OAuthConnections(BaseModel):
    github: Optional[OAuthConnection] = None
    google: Optional[OAuthConnection] = None

class OAuthConnection(BaseModel):
    connected: bool = False
    username: Optional[str] = None
    avatar_url: Optional[str] = None

class UserSession(BaseModel):
    id: str
    device: str
    location: Optional[str] = None
    last_active: datetime
    current: bool = False
```

## Service-Layer Erweiterungen

### Neue Methoden in `UserService`

```python
class UserService:
    def get_user_settings(self, db: Session, user_id: int) -> UserSettings:
        """Alle Benutzereinstellungen abrufen"""
        
    def update_user_settings(self, db: Session, user_id: int, 
                           settings_update: UserSettingsUpdate) -> UserSettings:
        """Benutzereinstellungen aktualisieren"""
        
    def change_password(self, db: Session, user_id: int, 
                       current_password: str, new_password: str) -> bool:
        """Passwort ändern"""
        
    def enable_two_factor(self, db: Session, user_id: int) -> TwoFactorSetup:
        """2FA aktivieren"""
        
    def disable_two_factor(self, db: Session, user_id: int, password: str) -> bool:
        """2FA deaktivieren"""
        
    def get_active_sessions(self, db: Session, user_id: int) -> List[UserSession]:
        """Aktive Sitzungen abrufen"""
        
    def revoke_session(self, db: Session, user_id: int, session_id: str) -> bool:
        """Sitzung beenden"""
        
    def revoke_other_sessions(self, db: Session, user_id: int, 
                            current_session_id: str) -> int:
        """Alle anderen Sitzungen beenden"""
        
    def request_data_export(self, db: Session, user_id: int) -> ExportRequest:
        """Datenexport anfordern"""
        
    def request_account_deletion(self, db: Session, user_id: int, 
                               password: str) -> bool:
        """Account-Löschung anfordern"""
```

## Sicherheitsüberlegungen

### Authentifizierung
- Alle Endpoints erfordern Authentifizierung
- Sensitive Operationen (Passwortänderung, 2FA, Account-Löschung) erfordern zusätzliche Passwortbestätigung

### Validierung
- Passwortstärke-Validierung
- Email-Format-Validierung
- Theme/Language/Visibility Enum-Validierung

### Rate Limiting
- Sensitive Endpoints (Passwortänderung, 2FA) sollten rate-limited sein
- Datenexport/Account-Löschung erfordern Cooldown-Perioden

### Audit Logging
- Alle Einstellungsänderungen protokollieren
- Sicherheitsrelevante Aktionen (Passwortänderung, 2FA, Sitzungsbeendigung) detailliert protokollieren

## Migrations

### Alembic Migration erstellen
```python
# migrations/versions/add_user_settings_tables.py
def upgrade():
    # user_settings Spalten hinzufügen
    # user_sessions Tabelle erstellen
    # Indizes erstellen
    pass

def downgrade():
    # Änderungen rückgängig machen
    pass
```

## Testing

### Testabdeckung
- Unit Tests für alle neuen Service-Methoden
- Integration Tests für API-Endpoints
- Sicherheitstests für sensitive Operationen
- Validierungstests für alle Schemas

## Deployment-Plan

### Phase 1: Datenbank-Migration
1. Migration-Skript erstellen und testen
2. Migration in Staging-Umgebung durchführen
3. Datenkonsistenz überprüfen

### Phase 2: Backend-API
1. Neue Endpoints implementieren
2. Service-Layer-Logik implementieren
3. Tests schreiben und durchführen

### Phase 3: Frontend-Integration
1. Frontend kann neue APIs nutzen
2. Fallback für alte APIs bereitstellen
3. Graduelle Migration

## Next Steps
1. Frontend-Seitenstruktur und Routing planen
2. Datenmodelle und Validierungsschemata finalisieren
3. UI/UX-Design detaillieren
4. Implementierungsplan erstellen