# 2FA-Architektur-Diagramm

## System-Übersicht

```mermaid
graph TB
    subgraph "Frontend (Vue 3 / Nuxt 3)"
        subgraph "Settings Page"
            S1[SettingsContent.vue]
            S2[TwoFactorSetup Molecule]
            S3[TwoFactorDisable Molecule]
            S4[TwoFactorStatus Molecule]
            S5[Modal Component]
        end
        
        subgraph "Authentication Flow"
            A1[Login Page]
            A2[Verify-2FA Page]
            A3[Auth Store]
        end
        
        subgraph "Component Hierarchy"
            C1[Atoms: Button, Input, Toggle]
            C2[Molecules: TwoFactorSetup, TwoFactorDisable]
            C3[Organisms: SettingsContent, TwoFactorVerification]
            C4[Templates: SettingsPageTemplate]
            C5[Pages: settings.vue, verify-2fa.vue]
        end
    end
    
    subgraph "Backend (FastAPI / Python)"
        subgraph "API Endpoints"
            B1[POST /api/settings/security/2fa/enable]
            B2[POST /api/settings/security/2fa/verify]
            B3[POST /api/settings/security/2fa/disable]
            B4[GET /api/settings/security]
            B5[POST /api/auth/verify-2fa]
        end
        
        subgraph "Services"
            B6[Settings Service]
            B7[Email Auth Service]
            B8[Two Factor Service]
        end
        
        subgraph "Data Layer"
            B9[User Model with 2FA fields]
            B10[Database: PostgreSQL]
        end
    end
    
    subgraph "External Services"
        E1[Authenticator Apps: Google Authenticator, Authy]
        E2[Email Service for backup]
        E3[Push Notification Service]
    end
    
    %% Connections
    S1 --> S2
    S1 --> S3
    S1 --> S4
    S1 --> S5
    
    A1 --> A2
    A2 --> A3
    
    C1 --> C2
    C2 --> C3
    C3 --> C4
    C4 --> C5
    
    S2 --> B1
    S3 --> B3
    A2 --> B5
    
    B1 --> B6
    B5 --> B7
    B6 --> B8
    B8 --> B9
    B9 --> B10
    
    B8 --> E1
    B7 --> E2
    B8 --> E3
```

## 2FA-Einrichtungs-Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend as Settings Page
    participant Backend as API
    participant DB as Database
    participant AuthApp as Authenticator App
    
    User->>Frontend: Klickt "2FA aktivieren"
    Frontend->>Backend: POST /api/settings/security/2fa/enable
    Backend->>DB: Generiert 2FA Secret
    Backend->>Backend: Generiert QR Code
    Backend-->>Frontend: Returns secret + QR code
    Frontend-->>User: Zeigt QR Code an
    
    User->>AuthApp: Scannt QR Code mit Authenticator App
    AuthApp-->>User: Generiert 6-stelligen Code
    
    User->>Frontend: Gibt Verifizierungscode ein
    Frontend->>Backend: POST /api/settings/security/2fa/verify
    Backend->>Backend: Validiert TOTP Code
    Backend->>DB: Speichert 2FA aktiviert
    Backend-->>Frontend: Returns success + backup codes
    Frontend-->>User: Zeigt Backup Codes an
    
    User->>Frontend: Speichert Backup Codes
    Frontend-->>User: Bestätigung der Einrichtung
```

## 2FA-Login-Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend as Login Page
    participant Backend as Auth API
    participant DB as Database
    participant AuthApp as Authenticator App
    
    User->>Frontend: Gibt Email/Passwort ein
    Frontend->>Backend: POST /api/auth/login
    Backend->>DB: Validiert Credentials
    
    alt 2FA deaktiviert
        Backend-->>Frontend: Returns access_token
        Frontend-->>User: Redirect zu Dashboard
    else 2FA aktiviert
        Backend->>Backend: Generiert temp_token
        Backend-->>Frontend: Returns requires_2fa: true, temp_token
        Frontend-->>User: Redirect zu /verify-2fa
        
        User->>AuthApp: Holt 6-stelligen Code
        User->>Frontend: Gibt 2FA Code ein
        Frontend->>Backend: POST /api/auth/verify-2fa
        Backend->>Backend: Validiert TOTP Code
        Backend->>DB: Aktualisiert Login-Zeitpunkt
        Backend-->>Frontend: Returns access_token
        Frontend-->>User: Redirect zu Dashboard
    end
```

## Komponenten-Hierarchie (Atomic Design)

```mermaid
graph TD
    subgraph "Atoms (Grundbausteine)"
        A1[Button]
        A2[Input Field]
        A3[Toggle Switch]
        A4[Icon]
        A5[Badge]
        A6[Modal]
    end
    
    subgraph "Molecules (Kombinationen)"
        M1[TwoFactorSetup]
        M2[TwoFactorDisable]
        M3[TwoFactorStatus]
        M4[QRCodeDisplay]
        M5[BackupCodeList]
    end
    
    subgraph "Organisms (Komplexe Komponenten)"
        O1[SettingsContent]
        O2[TwoFactorVerification]
        O3[SecuritySettings]
    end
    
    subgraph "Templates (Layouts)"
        T1[SettingsPageTemplate]
        T2[AuthPageTemplate]
    end
    
    subgraph "Pages (Vollständige Seiten)"
        P1[settings.vue]
        P2[verify-2fa.vue]
        P3[login.vue]
    end
    
    %% Connections
    A1 --> M1
    A2 --> M1
    A3 --> M3
    A4 --> M3
    A5 --> M3
    A6 --> M1
    
    M1 --> O1
    M2 --> O1
    M3 --> O1
    M4 --> M1
    M5 --> M1
    
    O1 --> T1
    O2 --> T2
    
    T1 --> P1
    T2 --> P2
    T2 --> P3
```

## Datenfluss bei 2FA-Operationen

```mermaid
flowchart TD
    Start[User Action] --> ActionType{Action Type}
    
    ActionType -->|Enable 2FA| EnableFlow
    ActionType -->|Disable 2FA| DisableFlow
    ActionType -->|Login with 2FA| LoginFlow
    ActionType -->|View Backup Codes| BackupFlow
    
    subgraph EnableFlow[2FA Activation Flow]
        E1[User clicks Enable] --> E2[API: Generate Secret]
        E2 --> E3[Frontend: Show QR Code]
        E3 --> E4[User scans with Auth App]
        E4 --> E5[User enters verification code]
        E5 --> E6[API: Verify TOTP]
        E6 --> E7[DB: Store 2FA enabled]
        E7 --> E8[Frontend: Show backup codes]
        E8 --> E9[Success]
    end
    
    subgraph DisableFlow[2FA Deactivation Flow]
        D1[User clicks Disable] --> D2[Frontend: Password confirmation]
        D2 --> D3[API: Verify password]
        D3 --> D4[DB: Remove 2FA data]
        D4 --> D5[Frontend: Success message]
        D5 --> D6[Success]
    end
    
    subgraph LoginFlow[2FA Login Flow]
        L1[User enters credentials] --> L2[API: Check 2FA status]
        L2 -->|2FA enabled| L3[API: Return temp_token]
        L3 --> L4[Frontend: Redirect to verify-2fa]
        L4 --> L5[User enters 2FA code]
        L5 --> L6[API: Verify code with temp_token]
        L6 --> L7[API: Issue access_token]
        L7 --> L8[Frontend: Redirect to dashboard]
        L8 --> L9[Success]
        
        L2 -->|2FA disabled| L10[API: Issue access_token directly]
        L10 --> L8
    end
    
    subgraph BackupFlow[Backup Code Management]
        B1[User clicks View Backup Codes] --> B2[Frontend: Show modal]
        B2 --> B3[User can copy/download]
        B3 --> B4[Frontend: Close modal]
        B4 --> B5[Success]
    end
    
    EnableFlow --> End[Operation Complete]
    DisableFlow --> End
    LoginFlow --> End
    BackupFlow --> End
```

## Sicherheits-Architektur

```mermaid
graph LR
    subgraph "Client-Side Security"
        CS1[HTTPS only]
        CS2[No 2FA secret storage]
        CS3[Secure cookie handling]
        CS4[XSS protection]
        CS5[CSRF tokens]
    end
    
    subgraph "Server-Side Security"
        SS1[TOTP validation]
        SS2[Rate limiting]
        SS3[Secure secret generation]
        SS4[Encrypted backup codes]
        SS5[Audit logging]
    end
    
    subgraph "Data Security"
        DS1[Encrypted 2FA secrets]
        DS2[Hashed backup codes]
        DS3[Secure session management]
        DS4[Regular security audits]
    end
    
    subgraph "Recovery Mechanisms"
        RM1[Backup codes]
        RM2[Email recovery]
        RM3[Admin override]
        RM4[Time-based lockout]
    end
    
    CS1 --> SS1
    CS2 --> SS3
    CS3 --> DS3
    CS4 --> SS4
    CS5 --> SS2
    
    SS1 --> DS1
    SS2 --> DS4
    SS3 --> DS2
    SS4 --> RM1
    SS5 --> DS4
    
    DS1 --> RM2
    DS2 --> RM3
    DS3 --> RM4
```

Diese Diagramme zeigen die vollständige Architektur der 2FA-Implementierung, von der Benutzeroberfläche bis zur Datenbank, einschließlich aller Sicherheitsaspekte und Wiederherstellungsmechanismen.