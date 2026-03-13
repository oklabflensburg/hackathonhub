# Email-Infrastruktur Konsolidierungs- und Erweiterungsplan

## Überblick
Basierend auf der umfassenden Analyse aller Service-Dateien identifizieren wir vier Hauptbereiche für Verbesserungen:
1. Schließen von Lücken in Bestätigungs-Emails
2. Vollständige Konsolidierung auf den `email_orchestrator`
3. Erweiterung der Template-Registry
4. Integration von Hackathon-spezifischen Emails

## 1. Schließen von Lücken in Bestätigungs-Emails

### 1.1 Email-Verifikations-Bestätigung
**Problem**: Nach erfolgreicher Email-Verifikation erhält der Nutzer keine Bestätigung.
**Lösung**: Implementiere `send_verification_confirmation_email` im `EmailVerificationService`.

**Aktionsschritte**:
1. Erstelle Template `verification_confirmed` in der Registry
2. Füge Methode in `email_verification_service.py` hinzu:
   ```python
   def send_verification_confirmation_email(
       self, db: Session, user_id: int, language: str = "en"
   ) -> bool:
       # Ruft email_orchestrator.send_template mit template_name="verification_confirmed" auf
   ```
3. Rufe diese Methode in `verify_email_token` nach erfolgreicher Verifikation auf

### 1.2 Password-Reset-Bestätigung
**Problem**: Nach erfolgreichem Password-Reset keine Bestätigungs-Email.
**Lösung**: Erweitere `reset_password` in `EmailAuthService`.

**Aktionsschritte**:
1. Erstelle Template `password_reset_confirmed` in der Registry
2. Modifiziere `reset_password`-Methode:
   ```python
   def reset_password(self, db: Session, token: str, new_password: str) -> bool:
       # Existierende Logik...
       if success:
           self.email_orchestrator.send_template(
               db=db,
               template_name="password_reset_confirmed",
               context=EmailContext(user_id=reset_token.user_id, ...),
               variables={"user_name": user.name}
           )
       return success
   ```

### 1.3 Passwortänderungs-Benachrichtigung
**Problem**: Bei manueller Passwortänderung (`change_password`) keine Sicherheitsbenachrichtigung.
**Lösung**: Erweitere `change_password` in `EmailAuthService`.

**Aktionsschritte**:
1. Erstelle Template `password_changed` in der Registry
2. Modifiziere `change_password`-Methode:
   ```python
   def change_password(self, db: Session, user_id: int, ...) -> bool:
       # Existierende Logik...
       if success:
           self.email_orchestrator.send_template(
               db=db,
               template_name="password_changed",
               context=EmailContext(user_id=user_id, ...),
               variables={"timestamp": datetime.utcnow().isoformat()}
           )
       return success
   ```

### 1.4 Newsletter-Abmeldungsbestätigung
**Problem**: Keine Bestätigung bei Newsletter-Abmeldung.
**Lösung**: Erweitere `unsubscribe` in `NewsletterService`.

**Aktionsschritte**:
1. Erstelle Template `newsletter_unsubscribed` in der Registry
2. Modifiziere `unsubscribe`-Methode:
   ```python
   def unsubscribe(self, db: Session, email: str) -> Optional[Dict]:
       # Existierende Logik...
       if subscription:
           self.email_orchestrator.send_template(
               db=db,
               template_name="newsletter_unsubscribed",
               context=EmailContext(user_email=email, ...),
               variables={"email": email}
           )
       return result
   ```

## 2. Vollständige Konsolidierung auf den `email_orchestrator`

### 2.1 Migration von `notification_service.py`
**Problem**: Verwendet `email_service` statt `email_orchestrator`.
**Lösung**: Ersetze `EmailService` durch `EmailOrchestrator`.

**Aktionsschritte**:
1. Ändere Import in `notification_service.py`:
   ```python
   from app.services.email_orchestrator import EmailOrchestrator, EmailContext
   ```
2. Ändere `__init__`:
   ```python
   def __init__(self):
       self.email_orchestrator = EmailOrchestrator()
       # statt self.email_service = EmailService()
   ```
3. Überarbeite `send_multi_channel_notification`:
   - Ersetze `self.email_service.send_email()` durch `self.email_orchestrator.send_template()`
   - Passe Parameter an (benötigt `db`, `template_name`, `context`, `variables`)
   - Verwende existierende Template-Map für `template_name`

### 2.2 Migration von `newsletter_service.py`
**Problem**: Verwendet `email_service.send_newsletter_welcome()`.
**Lösung**: Ersetze durch `email_orchestrator.send_template()`.

**Aktionsschritte**:
1. Ändere Import:
   ```python
   from app.services.email_orchestrator import EmailOrchestrator, EmailContext
   ```
2. Ändere `__init__`:
   ```python
   def __init__(self):
       self.repository = NewsletterRepository()
       self.email_orchestrator = EmailOrchestrator()
   ```
3. Überarbeite `subscribe`-Methode:
   ```python
   # Statt email_service.send_newsletter_welcome()
   context = EmailContext(user_email=email_lower, language="en", category="newsletter")
   self.email_orchestrator.send_template(
       db=db,
       template_name="newsletter_welcome",
       context=context,
       variables={"email": email_lower}
   )
   ```

### 2.3 Migration von `email_service.py` (Deprecation-Plan)
**Langfristige Lösung**: `email_service.py` sollte nur noch von `email_orchestrator` verwendet werden.
**Aktionsschritte**:
1. Markiere `email_service` als interne Komponente (nicht direkt von anderen Services aufrufen)
2. Aktualisiere Dokumentation
3. Entferne direkte Importe aus anderen Services (außer `email_orchestrator`)

## 3. Erweiterung der Template-Registry

### 3.1 Aktuelle Template-Übersicht
Aus `template_registry.py` müssen folgende neue Templates hinzugefügt werden:

**Fehlende Templates**:
1. `verification_confirmed` - Bestätigung erfolgreicher Email-Verifikation
2. `password_reset_confirmed` - Bestätigung erfolgreichen Password-Resets
3. `password_changed` - Benachrichtigung bei Passwortänderung
4. `newsletter_unsubscribed` - Bestätigung Newsletter-Abmeldung
5. `security_login_new_device` - Sicherheitsbenachrichtigung bei Login von neuem Gerät
6. `settings_changed` - Benachrichtigung bei Änderung sensibler Einstellungen

### 3.2 Template-Registry-Erweiterung
**Aktionsschritte**:
1. Öffne `backend/app/utils/template_registry.py`
2. Füge neue Templates zur `TEMPLATE_REGISTRY` hinzu:
   ```python
   TEMPLATE_REGISTRY = {
       # Existierende Templates...
       
       # Neue Bestätigungs-Templates
       "verification_confirmed": EmailTemplate(
           name="verification_confirmed",
           category="verification",
           required_variables=["user_name"],
           optional_variables=["verification_date"],
           description="Confirmation email after successful email verification"
       ),
       "password_reset_confirmed": EmailTemplate(
           name="password_reset_confirmed",
           category="security",
           required_variables=["user_name"],
           optional_variables=["reset_date", "ip_address"],
           description="Confirmation email after successful password reset"
       ),
       "password_changed": EmailTemplate(
           name="password_changed",
           category="security",
           required_variables=["user_name", "change_date"],
           optional_variables=["ip_address", "device_info"],
           description="Security notification when password is changed"
       ),
       "newsletter_unsubscribed": EmailTemplate(
           name="newsletter_unsubscribed",
           category="newsletter",
           required_variables=["email"],
           optional_variables=["unsubscribe_date"],
           description="Confirmation email after unsubscribing from newsletter"
       ),
       "security_login_new_device": EmailTemplate(
           name="security_login_new_device",
           category="security",
           required_variables=["user_name", "login_time", "device_info", "location"],
           optional_variables=["ip_address", "browser_info"],
           description="Security alert for login from new device/location"
       ),
       "settings_changed": EmailTemplate(
           name="settings_changed",
           category="settings",
           required_variables=["user_name", "changed_setting", "change_time"],
           optional_variables=["ip_address", "device_info"],
           description="Notification when sensitive account settings are changed"
       ),
   }
   ```

### 3.3 Template-Dateien erstellen
**Aktionsschritte**:
1. Erstelle Verzeichnisstruktur für neue Templates:
   ```
   backend/templates/emails/verification_confirmed/
     - en.html
     - de.html
     - subject.txt
   backend/templates/emails/password_reset_confirmed/
     - en.html
     - de.html
     - subject.txt
   # usw. für alle neuen Templates
   ```
2. Erstelle HTML- und Subject-Dateien mit entsprechendem Inhalt
3. Teste Template-Rendering mit `template_engine.render_email()`

## 4. Integration von Hackathon-spezifischen Emails

### 4.1 Analyse des `hackathon_service.py`
**Aktueller Status**: Keine Email-Funktionalität vorhanden.
**Erforderliche Emails**:
1. `hackathon_registered` - Bestätigung der Hackathon-Registrierung
2. `hackathon_start_reminder` - Erinnerung vor Hackathon-Start
3. `hackathon_started` - Benachrichtigung bei Hackathon-Start
4. `hackathon_updates` - Updates während des Hackathons

### 4.2 Implementierungsstrategie
**Option A**: Direkte Integration in `hackathon_service.py`
**Option B**: Nutzung von `notification_service` mit entsprechenden Notification-Types

**Empfehlung**: Option B (konsistent mit bestehendem System)

### 4.3 Aktionsschritte
1. **Erweitere Notification-Types** in `notification_preference_service.py`:
   ```python
   NOTIFICATION_TYPES = [
       # Existierende Types...
       {
           "type_key": "hackathon_registered",
           "category": "hackathon",
           "default_channels": "email,in_app",
           "description": "When you register for a hackathon"
       },
       {
           "type_key": "hackathon_start_reminder",
           "category": "hackathon",
           "default_channels": "email,push",
           "description": "Reminder before hackathon starts"
       },
       {
           "type_key": "hackathon_started",
           "category": "hackathon",
           "default_channels": "email,push,in_app",
           "description": "When a hackathon you registered for starts"
       },
   ]
   ```

2. **Erweitere Template-Map** in `notification_service.py`:
   ```python
   template_map = {
       # Existierende Mappings...
       "hackathon_registered": "hackathon/registered",
       "hackathon_start_reminder": "hackathon/start_reminder",
       "hackathon_started": "hackathon/started",
   }
   ```

3. **Integriere in `hackathon_service.py`**:
   ```python
   from app.services.notification_service import NotificationService
   
   class HackathonService:
       def __init__(self):
           self.notification_service = NotificationService()
       
       def register_for_hackathon(self, db: Session, user_id: int, hackathon_id: int):
           # Existierende Registrierungslogik...
           
           # Sende Bestätigungs-Email
           self.notification_service.send_multi_channel_notification(
               db=db,
               notification_type="hackathon_registered",
               user_id=user_id,
               title="Hackathon Registration Confirmed",
               message=f"You have successfully registered for {hackathon.name}",
               variables={
                   "hackathon_name": hackathon.name,
                   "start_date": hackathon.start_date,
                   "registration_date": datetime.utcnow().isoformat()
               }
           )
   ```

4. **Erstelle fehlende Hackathon-Templates**:
   - `hackathon/start_reminder/` (neu)
   - `hackathon/registered/` (existiert bereits)
   - `hackathon/started/` (existiert bereits)

## 5. Implementierungsreihenfolge und Zeitplan

### Phase 1: Template-Infrastruktur (1-2 Tage)
1. Erweitere Template-Registry mit neuen Templates
2. Erstelle Template-Dateien (HTML, Subject)
3. Teste Template-Rendering

### Phase 2: Bestätigungs-Emails (2-3 Tage)
1. Implementiere `verification_confirmed` in `EmailVerificationService`
2. Implementiere `password_reset_confirmed` in `EmailAuthService`
3. Implementiere `password_changed` in `EmailAuthService`
4. Implementiere `newsletter_unsubscribed` in `NewsletterService`

### Phase 3: Konsolidierung (2-3 Tage)
1. Migriere `notification_service` zu `email_orchestrator`
2. Migriere `newsletter_service` zu `email_orchestrator`
3. Aktualisiere alle betroffenen Tests

### Phase 4: Hackathon-Emails (1-2 Tage)
1. Erweitere Notification-Types
2. Integriere Email-Sendungen in `hackathon_service`
3. Erstelle fehlende Hackathon-Templates

### Phase 5: Testing und Deployment (1-2 Tage)
1. Integrationstests für alle neuen Email-Flows
2. E2E-Tests mit realen Email-Sendungen
3. Deployment und Monitoring

## 6. Qualitätssicherung und Testing

### 6.1 Unit Tests
- Teste jede neue Email-Methode isoliert
- Mocke `email_orchestrator` und `db` Session
- Teste Template-Variable-Validierung

### 6.2 Integration Tests
- Teste komplette Email-Flows (Registrierung → Verifikation → Bestätigung)
- Teste Fehlerbehandlung (z.B. fehlgeschlagene Email-Sendung)
- Teste Sprachwechsel (en/de)

### 6.3 E2E Tests
- Teste mit realem SMTP-Server (Test-Konto)
- Überprüfe Email-Inhalte und Formatierung
- Teste Mobile-Responsiveness der HTML-Emails

## 7. Monitoring und Logging

### 7.1 Erfolgsmetriken
- Email-Sendungsrate pro Template-Typ
- Öffnungs- und Klickraten (wenn Tracking verfügbar)
- Fehlerraten bei Email-Sendungen

### 7.2 Logging-Erweiterungen
- Detaillierte Logs für jede Email-Sendung
- Template-Rendering-Fehler
- User-Präferenz-Checks (wenn Email nicht gesendet werden soll)

## 8. Rollback-Plan

### 8.1 Risikominimierung
- Schrittweise Einführung (Feature-Flags)
- Canary-Deployment für neue Email-Templates
- Monitoring von Fehlerraten nach jedem Schritt

### 8.2 Rollback-Szenarien
1. **Template-Rendering-Fehler**: Deaktiviere betroffenes Template, fallback zu generischer Email
2. **Performance-Probleme**: Rate-Limiting für Email-Sendungen
3. **User-Beschwerden**: Temporäres Abschalten bestimmter Email-Typen

## 9. Erfolgskriterien

### 9.1 Technische Kriterien
- ✅ Alle Services verwenden `email_orchestrator` (keine direkten `email_service`-Aufrufe)
- ✅ Template-Registry enthält alle benötigten Templates
- ✅ 100% Test-Abdeckung für neue Email-Methoden
- ✅ Keine Regression in bestehenden Email-Flows

### 9.2 Business-Kriterien
- ✅ Nutzer erhalten Bestätigungs-Emails für alle kritischen Aktionen
- ✅ Sicherheitsbenachrichtigungen für verdächtige Aktivitäten
- ✅ Konsistente User-Experience über alle Email-Typen hinweg
- ✅ Reduzierte Support-Anfragen zu "Habe ich meine Email verifiziert?"

## 10. Nächste Schritte

1. **Genehmigung des Plans** durch Product Owner/Technical Lead
2. **Aufteilung in konkrete Tasks** für Entwicklungsteam
3. **Priorisierung** basierend auf Business-Impact
4. **Start der Implementierung** mit Phase 1 (Template-Infrastruktur)

---

**Letzte Aktualisierung**: 2026-03-13  
**Verantwortlicher**: Technical Architect  
**Status**: Zur Überprüfung