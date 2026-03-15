"""
Translation dictionaries for backend messages.
Supports English (en) and German (de) languages.
"""

from typing import Dict, Any

TRANSLATIONS: Dict[str, Dict[str, Any]] = {
    "en": {
        "errors": {
            "project_not_found": "Project not found",
            "hackathon_not_found": "Hackathon not found",
            "comment_not_found": "Comment not found",
            "vote_not_found": "Vote not found",
            "registration_not_found": "Registration not found",
            "user_not_found": "User not found",
            "unauthorized": "Not authorized to perform this action",
            "forbidden": "Access forbidden",
            "forbidden_email_verification": (
                "Email not verified. Please check your email."
            ),
            "invalid_token": "Invalid token",
            "token_expired": "Token expired, please login again",
            "token_already_used": "Verification link already used.",
            "invalid_vote_type": "Invalid vote type",
            "missing_auth_header": "Missing Authorization header",
            "token_refresh_failed": "Token refresh failed",
            "only_owner_can_update": "Only owner can update",
            "only_owner_can_delete": "Only owner can delete",
            "only_owner_or_team_can_update": "Only owner or team can update",
            "only_comment_author_can_update": "Only author can update comment",
            "only_comment_author_can_delete": "Only author can delete comment",
            "only_hackathon_owner_can_update": (
                "Only hackathon owner can update"
            ),
            "already_registered": "Already registered",
            "email_already_subscribed": "Already subscribed",
            "email_not_found": "Email not found",
            "failed_to_subscribe": "Failed to subscribe",
            "validation_error": "Validation error",
            "server_error": "Internal server error",
            "geocoding_failed": "Geocoding failed",
            "github_auth_failed": "GitHub auth failed",
            "oauth_failed": "OAuth failed",
            "team_not_found": "Team not found",
            "notification_not_found": "Notification not found",
            "preference_not_found": "Preference not found",
            "subscription_not_found": "Subscription not found",
            "invitation_not_found": "Invitation not found",
            "member_not_found": "Member not found",
            "file_too_large": "File too large. Max size is {max_size}MB",
            "file_type_not_allowed": (
                "File type not allowed. Allowed types: {types}"
            ),
            "invalid_file_type": (
                "Invalid file type. Allowed types: {allowed_types}"
            ),
            "failed_to_save_file": "Failed to save file: {error}",
            "cannot_upload_for_another_user": (
                "Cannot upload avatar for another user"
            ),
            "not_authorized_to_update": (
                "Not authorized to update this {entity}"
            ),
            "not_authorized_to_delete": (
                "Not authorized to delete this {entity}"
            ),
            "only_creator_can_delete": "Only creator can delete the {entity}",
            "only_owners_or_admins_can_add_members": (
                "Only team owners or admins can add members"
            ),
            "user_already_member": "User is already a member of this team",
            "cannot_remove_yourself": (
                "Cannot remove yourself from team. Use leave team instead."
            ),
            "validation_remove_self": (
                "Cannot remove yourself from team. Use leave team instead."
            ),
            "validation_already_member": (
                "User is already a member of this team"
            ),
            "validation_invitation_exists": (
                "Invitation already exists for this user"
            ),
            "validation_vote_type_invalid": "Invalid vote type",
            "validation_vote_type_must_be": (
                "Vote type must be '{option1}' or '{option2}'"
            ),
            "validation_registration": "Registration failed",
            "validation_email_verification": "Email verification failed",
            "validation_Two-factor authentication not set up": (
                "Two-factor authentication not set up"
            ),
            "validation_Invalid verification code": (
                "Invalid verification code"
            ),
            "only_owner_can_remove_another_owner": (
                "Only team owner can remove another owner"
            ),
            "sole_owner_cannot_leave": (
                "Cannot leave team as the sole owner. "
                "Transfer ownership or delete team."
            ),
            "validation_sole_owner_cannot_leave": (
                "Cannot leave team as the sole owner. "
                "Transfer ownership or delete team."
            ),
            "only_owners_or_admins_can_create_invitations": (
                "Only team owners or admins can create invitations"
            ),
            "invitation_already_exists": (
                "Invitation already exists for this user"
            ),
            "cannot_accept_for_another_user": (
                "Cannot accept invitation for another user"
            ),
            "cannot_decline_for_another_user": (
                "Cannot decline invitation for another user"
            ),
            "invitation_already_processed": (
                "Invitation is already {status}"
            ),
            "registration_closed": "Registration is closed for this hackathon",
            "already_registered_for_hackathon": (
                "Already registered for this hackathon"
            ),
            "failed_to_delete": "Failed to delete {entity}",
            "failed_to_update": "Failed to update {entity}",
            "vote_type_must_be": (
                "Vote type must be '{option1}' or '{option2}'"
            ),
            "incorrect_email_or_password": "Incorrect email or password",
            "email_not_verified": "Email not verified",
            "invalid_refresh_token": "Invalid refresh token",
            "refresh_token_revoked_or_expired": (
                "Refresh token revoked or expired"
            ),
            "invalid_token_payload": "Invalid token payload",
            "invalid_token_type": "Invalid token type",
            "not_authenticated": "Not authenticated",
            "could_not_validate_credentials": "Could not validate credentials",
            "failed_to_process_password_reset": (
                "Failed to process password reset request"
            ),
            "invalid_or_expired_reset_token": "Invalid or expired reset token",
            "failed_to_reset_password": "Failed to reset password",
            "failed_to_generate_oauth_url": (
                "Failed to generate OAuth URL: {error}"
            ),
            "oauth_not_configured": (
                "{provider} OAuth is not configured. "
                "Please set {env_var} in .env file."
            ),
            "configuration_error": "Configuration error: {details}",
            "email_verification_failed": "Email verification failed: {error}",
            "comment_voting_not_implemented": (
                "Comment voting not yet implemented"
            ),
            "push_notifications_not_implemented": (
                "Push notifications not yet implemented"
            ),
            "unauthorized_comment": "Please log in to post a reply",
            "unauthorized_credentials": "Invalid credentials"
        },
        "success": {
            "project_created": "Project created",
            "project_updated": "Project updated",
            "project_deleted": "Project deleted",
            "view_count_incremented": "View count incremented",
            "vote_recorded": "Vote recorded",
            "vote_removed": "Vote removed",
            "comment_created": "Comment created",
            "comment_updated": "Comment updated",
            "comment_deleted": "Comment deleted",
            "hackathon_created": "Hackathon created",
            "hackathon_updated": "Hackathon updated",
            "registration_successful": "Registration successful",
            "unregistration_successful": "Unregistration successful",
            "newsletter_subscribed": "Newsletter subscribed",
            "newsletter_unsubscribed": "Newsletter unsubscribed",
            "welcome": "Welcome to API",
            "health_check": "Service healthy"
        },
        "validation": {
            "required_field": "Field required",
            "invalid_email": "Invalid email",
            "invalid_url": "Invalid URL",
            "string_too_short": "Too short",
            "string_too_long": "Too long",
            "number_too_small": "Number too small",
            "number_too_large": "Number too large"
        },
        "email": {
            "newsletter_welcome_subject": "Welcome to Newsletter",
            "newsletter_welcome_body": "Thanks for subscribing",
            "verification_subject": (
                "Verify Your Email Address - Hackathon Dashboard"
            ),
            "password_reset_subject": (
                "Reset Your Password - Hackathon Dashboard"
            ),
            "verification_title": "Verify Your Email Address",
            "password_reset_title": "Reset Your Password",
            "newsletter_welcome_title": "Welcome to Hackathon Hub!",
            "team_invitation_subject": (
                "You've been invited to join a team - Hackathon Dashboard"
            ),
            "team_invitation_accepted_subject": (
                "Your team invitation has been accepted - Hackathon Dashboard"
            ),
            "team_member_added_subject": (
                "You've been added to a team - Hackathon Dashboard"
            ),
            "project_created_subject": (
                "New project created - Hackathon Dashboard"
            ),
            "hackathon_registered_subject": (
                "You're registered for {hackathon_name} - Hackathon Dashboard"
            ),
            "hackathon_started_subject": (
                "{hackathon_name} has started! - Hackathon Dashboard"
            ),
            "project_commented_subject": (
                "New comment on your project - Hackathon Dashboard"
            ),
            "team_created_subject": (
                "Your team has been created! - Hackathon Dashboard"
            ),
            "verification_confirmed_subject": (
                "Your email has been verified - Hackathon Dashboard"
            ),
            "password_reset_confirmed_subject": (
                "Your password reset was completed - Hackathon Dashboard"
            ),
            "password_changed_subject": (
                "Your password was changed - Hackathon Dashboard"
            ),
            "newsletter_unsubscribed_subject": (
                "You have been unsubscribed - Hackathon Dashboard"
            ),
            "security_login_new_device_subject": (
                "New device sign-in detected - Hackathon Dashboard"
            ),
            "settings_changed_subject": (
                "Your account settings were changed - Hackathon Dashboard"
            ),
            "hackathon_start_reminder_subject": (
                "{hackathon_name} starts in {days_until_start} day(s) - Hackathon Dashboard"
            ),
            "team_invitation_title": "Team Invitation",
            "team_invitation_accepted_title": "Invitation Accepted",
            "team_member_added_title": "Team Member Added",
            "project_created_title": "New Project",
            "hackathon_registered_title": "Hackathon Registration",
            "hackathon_started_title": "Hackathon Started",
            "project_commented_title": "New Project Comment",
            "team_created_title": "Team Created",
            "verification_confirmed_title": "Email Verified",
            "password_reset_confirmed_title": "Password Reset Confirmed",
            "password_changed_title": "Password Changed",
            "newsletter_unsubscribed_title": "Newsletter Unsubscribed",
            "security_login_new_device_title": "New Device Sign-In",
            "settings_changed_title": "Settings Changed",
            "hackathon_start_reminder_title": "Hackathon Reminder"
        },
        "notifications": {
            "help_text.team_invitation": "Alerts you when another participant invites you to a team so you can accept, decline, or react before collaboration starts without you.",
            "help_text.team_invitation_accepted": "Lets you know that an invited member has joined, so you can assign roles, share context, and continue coordination without checking manually.",
            "help_text.team_invitation_declined": "Informs you when an invitation is declined, so you can quickly invite someone else or rebalance the team before deadlines get closer.",
            "help_text.team_member_added": "Notifies you that you were added to a team, including cases where active project work already depends on your participation.",
            "help_text.team_created": "Confirms team creation and keeps newly created collaboration spaces visible when you manage multiple teams or hackathons.",
            "help_text.project_created": "Tells you when a new project appears in your team so you can review ownership, scope, and next steps early.",
            "help_text.project_commented": "Highlights new project discussion so feedback, review requests, and blockers are not missed.",
            "help_text.hackathon_registered": "Confirms successful registration and keeps event-related communication attached to the hackathon you joined.",
            "help_text.hackathon_started": "Signals the official event start so you can join on time and avoid missing kickoff, submissions, or early announcements.",
            "help_text.hackathon_start_reminder": "Sends a reminder shortly before kickoff so you have time to prepare teammates, devices, and submission materials.",
            "help_text.comment_reply": "Keeps threaded conversations visible when someone answers your comment and expects follow-up or clarification.",
            "help_text.vote_received": "Shows engagement with your project inside the app without creating unnecessary email or push noise by default.",
            "help_text.system_announcement": "Covers platform-wide announcements, maintenance information, and operational updates relevant to your account.",
            "help_text.security_alert": "Reserved for security-sensitive events that may require immediate action, such as suspicious access or account changes.",
            "help_text.verification_confirmed": "Confirms that your email address is verified and your account is ready for features that require a verified identity.",
            "help_text.password_reset_confirmed": "Confirms that a password reset was completed so you can spot unexpected account recovery activity.",
            "help_text.password_changed": "Warns you whenever the account password changes, which is critical for detecting unauthorized access quickly.",
            "help_text.newsletter_unsubscribed": "Records newsletter subscription changes so you have a clear audit trail of marketing preference updates.",
            "help_text.security_login_new_device": "Notifies you about sign-ins from new devices to help detect account takeover attempts and react immediately.",
            "help_text.settings_changed": "Confirms sensitive account setting changes so you can verify that profile or security updates were intentional."
        }
    },
    "de": {
        "errors": {
            "project_not_found": "Projekt nicht gefunden",
            "hackathon_not_found": "Hackathon nicht gefunden",
            "comment_not_found": "Kommentar nicht gefunden",
            "vote_not_found": "Stimme nicht gefunden",
            "registration_not_found": "Registrierung nicht gefunden",
            "user_not_found": "Benutzer nicht gefunden",
            "unauthorized": "Nicht autorisiert",
            "forbidden": "Zugriff verboten",
            "forbidden_email_verification": (
                "E-Mail nicht verifiziert. Bitte überprüfen Sie Ihre E-Mails."
            ),
            "invalid_token": "Ungültiges Token",
            "token_expired": "Token abgelaufen",
            "token_already_used": "Verifizierungslink bereits verwendet.",
            "invalid_vote_type": "Ungültiger Stimmentyp",
            "missing_auth_header": "Authorization-Header fehlt",
            "token_refresh_failed": "Token-Aktualisierung fehlgeschlagen",
            "only_owner_can_update": "Nur Besitzer kann aktualisieren",
            "only_owner_can_delete": "Nur Besitzer kann löschen",
            "only_owner_or_team_can_update": (
                "Nur Besitzer oder Team kann aktualisieren"
            ),
            "only_comment_author_can_update": (
                "Nur Autor kann Kommentar aktualisieren"
            ),
            "only_comment_author_can_delete": (
                "Nur Autor kann Kommentar löschen"
            ),
            "only_hackathon_owner_can_update": (
                "Nur Hackathon-Besitzer kann aktualisieren"
            ),
            "already_registered": "Bereits registriert",
            "email_already_subscribed": "Bereits abonniert",
            "email_not_found": "E-Mail nicht gefunden",
            "failed_to_subscribe": "Abonnement fehlgeschlagen",
            "validation_error": "Validierungsfehler",
            "server_error": "Serverfehler",
            "geocoding_failed": "Geocoding fehlgeschlagen",
            "github_auth_failed": "GitHub-Auth fehlgeschlagen",
            "oauth_failed": "OAuth fehlgeschlagen",
            "team_not_found": "Team nicht gefunden",
            "notification_not_found": "Benachrichtigung nicht gefunden",
            "preference_not_found": "Präferenz nicht gefunden",
            "subscription_not_found": "Abonnement nicht gefunden",
            "invitation_not_found": "Einladung nicht gefunden",
            "member_not_found": "Mitglied nicht gefunden",
            "file_too_large": (
                "Datei zu groß. Maximale Größe ist {max_size}MB"
            ),
            "file_type_not_allowed": (
                "Dateityp nicht erlaubt. Erlaubte Typen: {types}"
            ),
            "invalid_file_type": (
                "Ungültiger Dateityp. Erlaubte Typen: {allowed_types}"
            ),
            "failed_to_save_file": "Fehler beim Speichern der Datei: {error}",
            "cannot_upload_for_another_user": (
                "Kann kein Avatar für einen anderen Benutzer hochladen"
            ),
            "not_authorized_to_update": (
                "Nicht berechtigt, dieses {entity} zu aktualisieren"
            ),
            "not_authorized_to_delete": (
                "Nicht berechtigt, dieses {entity} zu löschen"
            ),
            "only_creator_can_delete": (
                "Nur Ersteller kann das {entity} löschen"
            ),
            "only_owners_or_admins_can_add_members": (
                "Nur Team-Besitzer oder Admins können Mitglieder hinzufügen"
            ),
            "user_already_member": (
                "Benutzer ist bereits Mitglied dieses Teams"
            ),
            "cannot_remove_yourself": (
                "Kann sich nicht selbst entfernen. "
                "Verwende stattdessen 'Team verlassen'."
            ),
            "validation_remove_self": (
                "Kann sich nicht selbst entfernen. "
                "Verwende stattdessen 'Team verlassen'."
            ),
            "validation_already_member": (
                "Benutzer ist bereits Mitglied dieses Teams"
            ),
            "validation_invitation_exists": (
                "Einladung für diesen Benutzer existiert bereits"
            ),
            "validation_vote_type_invalid": "Ungültiger Stimmentyp",
            "validation_vote_type_must_be": (
                "Stimmentyp muss '{option1}' oder '{option2}' sein"
            ),
            "validation_registration": "Registrierung fehlgeschlagen",
            "validation_email_verification": (
                "E-Mail-Verifizierung fehlgeschlagen"
            ),
            "validation_Two-factor authentication not set up": (
                "Zwei-Faktor-Authentifizierung nicht eingerichtet"
            ),
            "validation_Invalid verification code": (
                "Ungültiger Verifizierungscode"
            ),
            "only_owner_can_remove_another_owner": (
                "Nur Team-Besitzer kann einen anderen Besitzer entfernen"
            ),
            "sole_owner_cannot_leave": (
                "Kann Team nicht verlassen als einziger Besitzer. "
                "Übertrage Besitz oder lösche das Team."
            ),
            "validation_sole_owner_cannot_leave": (
                "Kann Team nicht verlassen als einziger Besitzer. "
                "Übertrage Besitz oder lösche das Team."
            ),
            "only_owners_or_admins_can_create_invitations": (
                "Nur Team-Besitzer oder Admins können Einladungen erstellen"
            ),
            "invitation_already_exists": (
                "Einladung für diesen Benutzer existiert bereits"
            ),
            "cannot_accept_for_another_user": (
                "Kann keine Einladung für einen anderen Benutzer annehmen"
            ),
            "cannot_decline_for_another_user": (
                "Kann keine Einladung für einen anderen Benutzer ablehnen"
            ),
            "invitation_already_processed": (
                "Einladung ist bereits {status}"
            ),
            "registration_closed": (
                "Registrierung für diesen Hackathon ist geschlossen"
            ),
            "already_registered_for_hackathon": (
                "Bereits für diesen Hackathon registriert"
            ),
            "failed_to_delete": "Fehler beim Löschen von {entity}",
            "failed_to_update": "Fehler beim Aktualisieren von {entity}",
            "vote_type_must_be": (
                "Stimmentyp muss '{option1}' oder '{option2}' sein"
            ),
            "incorrect_email_or_password": "Falsche E-Mail oder Passwort",
            "email_not_verified": "E-Mail nicht verifiziert",
            "invalid_refresh_token": "Ungültiges Aktualisierungstoken",
            "refresh_token_revoked_or_expired": (
                "Aktualisierungstoken widerrufen oder abgelaufen"
            ),
            "invalid_token_payload": "Ungültige Token-Nutzlast",
            "invalid_token_type": "Ungültiger Tokentyp",
            "not_authenticated": "Nicht authentifiziert",
            "could_not_validate_credentials": (
                "Anmeldedaten konnten nicht validiert werden"
            ),
            "failed_to_process_password_reset": (
                "Fehler bei der Verarbeitung der Passwort-Reset-Anfrage"
            ),
            "invalid_or_expired_reset_token": (
                "Ungültiges oder abgelaufenes Reset-Token"
            ),
            "failed_to_reset_password": (
                "Fehler beim Zurücksetzen des Passworts"
            ),
            "failed_to_generate_oauth_url": (
                "Fehler beim Generieren der OAuth-URL: {error}"
            ),
            "oauth_not_configured": (
                "{provider} OAuth ist nicht konfiguriert. "
                "Bitte setze {env_var} in der .env-Datei."
            ),
            "configuration_error": "Konfigurationsfehler: {details}",
            "email_verification_failed": (
                "E-Mail-Verifizierung fehlgeschlagen: {error}"
            ),
            "comment_voting_not_implemented": (
                "Kommentar-Abstimmung noch nicht implementiert"
            ),
            "push_notifications_not_implemented": (
                "Push-Benachrichtigungen noch nicht implementiert"
            ),
            "unauthorized_comment": (
                "Bitte melde dich an, um eine Antwort zu posten"
            ),
            "unauthorized_credentials": "Ungültige Anmeldedaten"
        },
        "success": {
            "project_created": "Projekt erstellt",
            "project_updated": "Projekt aktualisiert",
            "project_deleted": "Projekt gelöscht",
            "view_count_incremented": "Aufrufzähler erhöht",
            "vote_recorded": "Stimme erfasst",
            "vote_removed": "Stimme entfernt",
            "comment_created": "Kommentar erstellt",
            "comment_updated": "Kommentar aktualisiert",
            "comment_deleted": "Kommentar gelöscht",
            "hackathon_created": "Hackathon erstellt",
            "hackathon_updated": "Hackathon aktualisiert",
            "registration_successful": "Registrierung erfolgreich",
            "unregistration_successful": "Abmeldung erfolgreich",
            "newsletter_subscribed": "Newsletter abonniert",
            "newsletter_unsubscribed": "Newsletter abgemeldet",
            "welcome": "Willkommen bei API",
            "health_check": "Service gesund"
        },
        "validation": {
            "required_field": "Feld erforderlich",
            "invalid_email": "Ungültige E-Mail",
            "invalid_url": "Ungültige URL",
            "string_too_short": "Zu kurz",
            "string_too_long": "Zu lang",
            "number_too_small": "Zahl zu klein",
            "number_too_large": "Zahl zu groß"
        },
        "email": {
            "newsletter_welcome_subject": "Willkommen beim Newsletter",
            "newsletter_welcome_body": "Danke fürs Abonnieren",
            "verification_subject": (
                "Bestätigen Sie Ihre E-Mail-Adresse - Hackathon Dashboard"
            ),
            "password_reset_subject": (
                "Setzen Sie Ihr Passwort zurück - Hackathon Dashboard"
            ),
            "verification_title": "Bestätigen Sie Ihre E-Mail-Adresse",
            "password_reset_title": "Setzen Sie Ihr Passwort zurück",
            "newsletter_welcome_title": "Willkommen beim Hackathon Hub!",
            "team_invitation_subject": (
                "Sie wurden zu einem Team eingeladen - Hackathon Dashboard"
            ),
            "team_invitation_accepted_subject": (
                "Ihre Teameinladung wurde angenommen - Hackathon Dashboard"
            ),
            "team_member_added_subject": (
                "Sie wurden einem Team hinzugefügt - Hackathon Dashboard"
            ),
            "project_created_subject": (
                "Neues Projekt erstellt - Hackathon Dashboard"
            ),
            "hackathon_registered_subject": (
                "Du bist für {hackathon_name} registriert! - "
                "Hackathon Dashboard"
            ),
            "hackathon_started_subject": (
                "{hackathon_name} hat begonnen! - Hackathon Dashboard"
            ),
            "project_commented_subject": (
                "Neuer Kommentar zu deinem Projekt - Hackathon Dashboard"
            ),
            "team_created_subject": (
                "Dein Team wurde erstellt! - Hackathon Dashboard"
            ),
            "verification_confirmed_subject": (
                "Deine E-Mail wurde verifiziert - Hackathon Dashboard"
            ),
            "password_reset_confirmed_subject": (
                "Dein Passwort-Reset wurde abgeschlossen - Hackathon Dashboard"
            ),
            "password_changed_subject": (
                "Dein Passwort wurde geändert - Hackathon Dashboard"
            ),
            "newsletter_unsubscribed_subject": (
                "Du wurdest vom Newsletter abgemeldet - Hackathon Dashboard"
            ),
            "security_login_new_device_subject": (
                "Anmeldung von neuem Gerät erkannt - Hackathon Dashboard"
            ),
            "settings_changed_subject": (
                "Deine Kontoeinstellungen wurden geändert - Hackathon Dashboard"
            ),
            "hackathon_start_reminder_subject": (
                "{hackathon_name} startet in {days_until_start} Tag(en) - Hackathon Dashboard"
            ),
            "team_invitation_title": "Teameinladung",
            "team_invitation_accepted_title": "Einladung angenommen",
            "team_member_added_title": "Teammitglied hinzugefügt",
            "project_created_title": "Neues Projekt",
            "hackathon_registered_title": "Hackathon-Registrierung",
            "hackathon_started_title": "Hackathon gestartet",
            "project_commented_title": "Neuer Projekt-Kommentar",
            "team_created_title": "Team erstellt",
            "verification_confirmed_title": "E-Mail verifiziert",
            "password_reset_confirmed_title": "Passwort-Reset bestätigt",
            "password_changed_title": "Passwort geändert",
            "newsletter_unsubscribed_title": "Newsletter abgemeldet",
            "security_login_new_device_title": "Neues Gerät erkannt",
            "settings_changed_title": "Einstellungen geändert",
            "hackathon_start_reminder_title": "Hackathon-Erinnerung"
        },
        "notifications": {
            "help_text.team_invitation": "Informiert dich, wenn dich jemand in ein Team einlädt, damit du rechtzeitig annehmen, ablehnen oder reagieren kannst, bevor die Zusammenarbeit ohne dich startet.",
            "help_text.team_invitation_accepted": "Zeigt dir, dass ein eingeladener Nutzer beigetreten ist, damit du Rollen vergeben, Kontext teilen und die Zusammenarbeit direkt fortsetzen kannst.",
            "help_text.team_invitation_declined": "Informiert dich, wenn eine Einladung abgelehnt wurde, damit du schnell andere Personen einladen oder das Team neu ausbalancieren kannst.",
            "help_text.team_member_added": "Benachrichtigt dich, wenn du zu einem Team hinzugefügt wurdest, auch in Fällen, in denen bereits laufende Projektarbeit von deiner Teilnahme abhängt.",
            "help_text.team_created": "Bestätigt die Teamerstellung und hält neue Kollaborationsräume sichtbar, wenn du mehrere Teams oder Hackathons verwaltest.",
            "help_text.project_created": "Informiert dich, wenn in deinem Team ein neues Projekt angelegt wurde, damit du Zuständigkeiten, Umfang und nächste Schritte früh prüfen kannst.",
            "help_text.project_commented": "Hebt neue Diskussionen am Projekt hervor, damit Feedback, Review-Anfragen und Blocker nicht untergehen.",
            "help_text.hackathon_registered": "Bestätigt deine erfolgreiche Anmeldung und bündelt wichtige Kommunikationspunkte zum Hackathon, an dem du teilnimmst.",
            "help_text.hackathon_started": "Signalisiert den offiziellen Start des Events, damit du Kickoff, Einreichungen und frühe Ankündigungen nicht verpasst.",
            "help_text.hackathon_start_reminder": "Erinnert dich kurz vor dem Start, damit du Team, Geräte und Einreichungsunterlagen rechtzeitig vorbereiten kannst.",
            "help_text.comment_reply": "Hält Kommentar-Threads sichtbar, wenn jemand auf deinen Beitrag antwortet und eine Rückmeldung oder Klärung erwartet.",
            "help_text.vote_received": "Zeigt Interaktionen mit deinem Projekt in der App an, ohne standardmäßig unnötige E-Mail- oder Push-Benachrichtigungen zu erzeugen.",
            "help_text.system_announcement": "Umfasst plattformweite Ankündigungen, Wartungshinweise und betriebliche Updates, die für dein Konto relevant sind.",
            "help_text.security_alert": "Ist für sicherheitsrelevante Ereignisse reserviert, bei denen möglicherweise sofortiges Handeln nötig ist, etwa bei verdächtigen Zugriffen oder Kontoänderungen.",
            "help_text.verification_confirmed": "Bestätigt, dass deine E-Mail-Adresse verifiziert wurde und dein Konto für Funktionen mit verifizierter Identität bereit ist.",
            "help_text.password_reset_confirmed": "Bestätigt den Abschluss eines Passwort-Resets, damit dir unerwartete Kontowiederherstellungen auffallen.",
            "help_text.password_changed": "Warnt dich bei jeder Passwortänderung, was wichtig ist, um unbefugten Zugriff schnell zu erkennen.",
            "help_text.newsletter_unsubscribed": "Dokumentiert Änderungen an deinen Newsletter-Einstellungen, damit du einen klaren Verlauf deiner Marketing-Präferenzen hast.",
            "help_text.security_login_new_device": "Benachrichtigt dich über Anmeldungen von neuen Geräten, damit du mögliche Kontoübernahmen früh erkennst und sofort reagieren kannst.",
            "help_text.settings_changed": "Bestätigt sensible Änderungen an Kontoeinstellungen, damit du prüfen kannst, ob Profil- oder Sicherheitsänderungen beabsichtigt waren."
        }
    }
}


def get_translation(key: str, locale: str = "en", **kwargs) -> str:
    """
    Get a translated message for the given key and locale.

    Args:
        key: Translation key in format "category.subkey"
        locale: Language code (default: "en")
        **kwargs: Format arguments for the translation string

    Returns:
        Translated string with formatted arguments
    """
    if locale not in TRANSLATIONS:
        locale = "en"

    # Split key into category and subkey
    parts = key.split(".", 1)
    if len(parts) != 2:
        raise KeyError(f"Invalid translation key format: {key}")

    category, subkey = parts

    # Navigate through translation dictionary
    category_dict = TRANSLATIONS[locale].get(category)
    if not category_dict:
        raise KeyError(f"Translation category not found: {category}")

    translation = category_dict.get(subkey)
    if translation is None:
        # Try to find a generic fallback for common error patterns
        # For forbidden_{action} keys, fall back to generic "forbidden"
        if subkey.startswith("forbidden_") and category == "errors":
            generic_translation = TRANSLATIONS[locale].get(
                "errors", {}
            ).get("forbidden")
            if generic_translation:
                # Include action in kwargs for context if available
                action = subkey.replace("forbidden_", "")
                kwargs_with_action = {"action": action, **kwargs}
                try:
                    return generic_translation.format(**kwargs_with_action)
                except KeyError:
                    # If formatting fails, return generic translation
                    # without action
                    return generic_translation

        # For unauthorized_{reason} keys, fall back to generic "unauthorized"
        if subkey.startswith("unauthorized_") and category == "errors":
            generic_translation = TRANSLATIONS[locale].get(
                "errors", {}
            ).get("unauthorized")
            if generic_translation:
                # Include reason in kwargs for context if available
                reason = subkey.replace("unauthorized_", "")
                kwargs_with_reason = {"reason": reason, **kwargs}
                try:
                    return generic_translation.format(**kwargs_with_reason)
                except KeyError:
                    # If formatting fails, return generic translation
                    # without reason
                    return generic_translation

        # Fallback to English if translation not found
        if locale != "en":
            try:
                return get_translation(key, "en", **kwargs)
            except KeyError:
                pass

        raise KeyError(f"Translation key not found: {key}")

    # Format the translation with provided arguments
    if kwargs:
        try:
            return translation.format(**kwargs)
        except KeyError as e:
            raise KeyError(
                f"Missing format argument {e} for translation: {key}"
            ) from e

    return translation
