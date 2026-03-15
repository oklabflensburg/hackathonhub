"""
Enhanced email translations with dynamic language resolution.
Provides comprehensive translation support for all email templates.
"""
from typing import Dict, Optional
import logging

from .translations import get_translation, SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)


class EmailTranslationManager:
    """Manager for email-specific translations with enhanced features."""

    # Email translation keys mapping
    EMAIL_TRANSLATION_KEYS = {
        # Subject translations
        "verification": "email.verification_subject",
        "password_reset": "email.password_reset_subject",
        "newsletter_welcome": "email.newsletter_welcome_subject",
        "team/invitation_sent": "email.team_invitation_subject",
        "team/invitation_accepted": "email.team_invitation_accepted_subject",
        "team/member_added": "email.team_member_added_subject",
        "team/created": "email.team_created_subject",
        "project/created": "email.project_created_subject",
        "project/commented": "email.project_commented_subject",
        "hackathon/registered": "email.hackathon_registered_subject",
        "hackathon/started": "email.hackathon_started_subject",
        "verification_confirmed": "email.verification_confirmed_subject",
        "password_reset_confirmed": "email.password_reset_confirmed_subject",
        "password_changed": "email.password_changed_subject",
        "newsletter_unsubscribed": "email.newsletter_unsubscribed_subject",
        "security_login_new_device": "email.security_login_new_device_subject",
        "settings_changed": "email.settings_changed_subject",
        "hackathon/start_reminder": "email.hackathon_start_reminder_subject",

        # Title translations
        "verification_title": "email.verification_title",
        "password_reset_title": "email.password_reset_title",
        "newsletter_welcome_title": "email.newsletter_welcome_title",
        "team_invitation_title": "email.team_invitation_title",
        "team_invitation_accepted_title":
            "email.team_invitation_accepted_title",
        "team_member_added_title": "email.team_member_added_title",
        "team_created_title": "email.team_created_title",
        "project_created_title": "email.project_created_title",
        "project_commented_title": "email.project_commented_title",
        "hackathon_registered_title": "email.hackathon_registered_title",
        "hackathon_started_title": "email.hackathon_started_title",
        "verification_confirmed_title": "email.verification_confirmed_title",
        "password_reset_confirmed_title": "email.password_reset_confirmed_title",
        "password_changed_title": "email.password_changed_title",
        "newsletter_unsubscribed_title": "email.newsletter_unsubscribed_title",
        "security_login_new_device_title": "email.security_login_new_device_title",
        "settings_changed_title": "email.settings_changed_title",
        "hackathon_start_reminder_title": "email.hackathon_start_reminder_title",

        # Common email phrases
        "greeting": "email.greeting",
        "closing": "email.closing",
        "signature": "email.signature",
        "footer_notice": "email.footer_notice",
        "unsubscribe_link": "email.unsubscribe_link",
        "contact_support": "email.contact_support"
    }

    def __init__(self):
        self.cache: Dict[str, Dict[str, str]] = {}

    def get_email_translation(
        self,
        key: str,
        language: str = "en",
        fallback_language: str = "en",
        variables: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Get email translation with variable interpolation.

        Args:
            key: Translation key
            language: Target language
            fallback_language: Fallback language if translation not found
            variables: Variables to interpolate into translation

        Returns:
            Translated string with variables interpolated
        """
        if variables is None:
            variables = {}

        # Try to get translation
        translation = get_translation(key, language)

        # If not found, try fallback language
        if translation == key and language != fallback_language:
            translation = get_translation(key, fallback_language)

        # If still not found, return the key as last resort
        if translation == key:
            logger.warning(f"Translation not found for key: {key}")
            return key

        # Interpolate variables
        try:
            return translation.format(**variables)
        except KeyError as e:
            logger.error(f"Missing variable {e} in translation {key}")
            return translation
        except Exception as e:
            logger.error(f"Error interpolating translation {key}: {e}")
            return translation

    def get_email_subject(
        self,
        template_name: str,
        language: str = "en",
        variables: Optional[Dict[str, str]] = None
    ) -> str:
        """Get email subject for a template."""
        key = self.EMAIL_TRANSLATION_KEYS.get(template_name)
        if not key:
            # Try to construct key from template name
            if "/" in template_name:
                # Convert "team/invitation_sent" to "team_invitation_sent"
                key_name = template_name.replace("/", "_")
                key = f"email.{key_name}_subject"
            else:
                key = f"email.{template_name}_subject"

        return self.get_email_translation(key, language, variables=variables)

    def get_email_title(
        self,
        template_name: str,
        language: str = "en",
        variables: Optional[Dict[str, str]] = None
    ) -> str:
        """Get email title for a template."""
        # Map template name to title key
        title_key_map = {
            "verification": "verification_title",
            "password_reset": "password_reset_title",
            "newsletter_welcome": "newsletter_welcome_title",
            "team/invitation_sent": "team_invitation_title",
            "team/invitation_accepted": "team_invitation_accepted_title",
            "team/member_added": "team_member_added_title",
            "team/created": "team_created_title",
            "project/created": "project_created_title",
            "project/commented": "project_commented_title",
            "hackathon/registered": "hackathon_registered_title",
            "hackathon/started": "hackathon_started_title",
            "verification_confirmed": "verification_confirmed_title",
            "password_reset_confirmed": "password_reset_confirmed_title",
            "password_changed": "password_changed_title",
            "newsletter_unsubscribed": "newsletter_unsubscribed_title",
            "security_login_new_device": "security_login_new_device_title",
            "settings_changed": "settings_changed_title",
            "hackathon/start_reminder": "hackathon_start_reminder_title",
        }

        key_name = title_key_map.get(template_name)
        if key_name:
            key = self.EMAIL_TRANSLATION_KEYS.get(key_name)
        else:
            # Try to construct key
            if "/" in template_name:
                key_name = template_name.replace("/", "_") + "_title"
                key = f"email.{key_name}"
            else:
                key = f"email.{template_name}_title"

        return self.get_email_translation(key, language, variables=variables)

    def get_common_email_phrase(
        self,
        phrase_key: str,
        language: str = "en",
        variables: Optional[Dict[str, str]] = None
    ) -> str:
        """Get common email phrase translation."""
        key = self.EMAIL_TRANSLATION_KEYS.get(phrase_key)
        if not key:
            key = f"email.{phrase_key}"

        return self.get_email_translation(key, language, variables=variables)

    def validate_language_support(
        self,
        template_name: str,
        language: str = "en"
    ) -> bool:
        """Validate that a template has translations for the given language."""
        # Check if language is supported
        if language not in SUPPORTED_LANGUAGES:
            logger.warning(f"Language {language} not in SUPPORTED_LANGUAGES")
            return False

        # Get subject key
        subject_key = self.EMAIL_TRANSLATION_KEYS.get(template_name)
        if not subject_key:
            # Try to construct key
            if "/" in template_name:
                key_name = template_name.replace("/", "_")
                subject_key = f"email.{key_name}_subject"
            else:
                subject_key = f"email.{template_name}_subject"

        # Check if translation exists
        translation = get_translation(subject_key, language)
        if translation == subject_key:
            # Translation not found
            logger.warning(
                f"Translation not found for {subject_key} in {language}"
            )
            return False

        return True

    def get_available_languages(self, template_name: str) -> list:
        """Get list of languages available for a template."""
        available_languages = []

        for language in SUPPORTED_LANGUAGES:
            if self.validate_language_support(template_name, language):
                available_languages.append(language)

        return available_languages

    def get_template_translation_report(self) -> Dict[str, Dict[str, list]]:
        """Generate report of translation coverage for all templates."""
        report = {
            "fully_translated": [],
            "partially_translated": [],
            "missing_translations": []
        }

        # Get all template names from translation keys
        template_names = set()
        for key in self.EMAIL_TRANSLATION_KEYS:
            if key.endswith("_subject"):
                # Extract template name from key
                if key.startswith("email."):
                    template_part = key[6:]  # Remove "email."
                    if template_part.endswith("_subject"):
                        template_name = template_part[:-8]  # Remove "_subject"
                        # Convert back to path format if needed
                        if "_" in template_name and "/" not in template_name:
                            # Check if this is a compound name
                            # like "team_invitation_sent"
                            # We'll keep it as is for now
                            pass
                        template_names.add(template_name)

        # Check each template
        for template_name in template_names:
            available_languages = self.get_available_languages(template_name)

            if len(available_languages) == len(SUPPORTED_LANGUAGES):
                report["fully_translated"].append(template_name)
            elif available_languages:
                report["partially_translated"].append({
                    "template": template_name,
                    "languages": available_languages
                })
            else:
                report["missing_translations"].append(template_name)

        return report


# Global instance
email_translation_manager = EmailTranslationManager()


# Convenience functions
def get_email_subject(
    template_name: str,
    language: str = "en",
    variables: Optional[Dict[str, str]] = None
) -> str:
    """Convenience function to get email subject."""
    return email_translation_manager.get_email_subject(
        template_name, language, variables
    )


def get_email_title(
    template_name: str,
    language: str = "en",
    variables: Optional[Dict[str, str]] = None
) -> str:
    """Convenience function to get email title."""
    return email_translation_manager.get_email_title(
        template_name, language, variables
    )


def validate_email_translations(
    template_name: str, language: str = "en"
) -> bool:
    """Convenience function to validate email translations."""
    return email_translation_manager.validate_language_support(
        template_name, language
    )
