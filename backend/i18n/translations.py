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
            "invalid_token": "Invalid token",
            "token_expired": "Token expired, please login again",
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
            "oauth_failed": "OAuth failed"
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
            "newsletter_welcome_body": "Thanks for subscribing"
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
            "invalid_token": "Ungültiges Token",
            "token_expired": "Token abgelaufen",
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
            "oauth_failed": "OAuth fehlgeschlagen"
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
            "newsletter_welcome_body": "Danke fürs Abonnieren"
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