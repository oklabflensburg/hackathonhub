"""
Template engine for rendering email templates with i18n support.
"""
import os
import re
from datetime import datetime
from typing import Dict, Any, Optional
import logging

from i18n.translations import get_translation

logger = logging.getLogger(__name__)


class TemplateEngine:
    """Engine for loading and rendering email templates."""
    
    def __init__(self, template_dir: str = "templates/emails"):
        """
        Initialize template engine.
        
        Args:
            template_dir: Directory containing email templates
        """
        self.template_dir = template_dir
        self.base_template = self._load_template("base.html")
        
    def _load_template(self, template_path: str) -> Optional[str]:
        """Load template file from disk."""
        full_path = os.path.join(self.template_dir, template_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Template not found: {full_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading template {full_path}: {e}")
            return None
    
    def _render_template(self, template: str,
                         variables: Dict[str, Any]) -> str:
        """Render template with variable substitution."""
        if not template:
            return ""
        
        # Simple variable substitution: {{ variable_name }}
        result = template
        for key, value in variables.items():
            placeholder = f"{{{{ {key} }}}}"
            if isinstance(value, str):
                result = result.replace(placeholder, value)
            else:
                result = result.replace(placeholder, str(value))
        
        return result
    
    def render_email(
        self,
        template_name: str,
        language: str = "en",
        variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Render email template with given variables.
        
        Args:
            template_name: Name of template directory (e.g., "verification")
            language: Language code (e.g., "en", "de")
            variables: Dictionary of template variables
            
        Returns:
            Dictionary with "subject", "html", and "text" keys
        """
        if variables is None:
            variables = {}
        
        # Add current year if not provided
        if "current_year" not in variables:
            variables["current_year"] = datetime.now().year
        
        # Try to load language-specific template
        template_path = f"{template_name}/{language}.html"
        content_template = self._load_template(template_path)
        
        # Fallback to English if language-specific template not found
        if not content_template and language != "en":
            msg = f"Template {template_name}/{language}.html not found, "
            msg += "falling back to English"
            logger.warning(msg)
            template_path = f"{template_name}/en.html"
            content_template = self._load_template(template_path)
        
        if not content_template:
            msg = f"Template {template_name} not found for language {language}"
            raise ValueError(msg)
        
        # Get subject from translations
        subject_key_map = {
            "verification": "email.verification_subject",
            "password_reset": "email.password_reset_subject",
            "newsletter_welcome": "email.newsletter_welcome_subject",
            "team/invitation_sent": "email.team_invitation_subject",
            "team/invitation_accepted": (
                "email.team_invitation_accepted_subject"
            ),
            "team/member_added": "email.team_member_added_subject",
            "project/created": "email.project_created_subject"
        }
        
        subject_key = subject_key_map.get(template_name)
        if subject_key:
            try:
                subject = get_translation(subject_key, language)
            except KeyError:
                subject = "Email from Hackathon Dashboard"
        else:
            subject = "Email from Hackathon Dashboard"
        
        # Render content
        rendered_content = self._render_template(content_template, variables)
        
        # Get title from translations
        title_key_map = {
            "verification": "email.verification_title",
            "password_reset": "email.password_reset_title",
            "newsletter_welcome": "email.newsletter_welcome_title",
            "team/invitation_sent": "email.team_invitation_title",
            "team/invitation_accepted": "email.team_invitation_accepted_title",
            "team/member_added": "email.team_member_added_title",
            "project/created": "email.project_created_title"
        }
        
        title_key = title_key_map.get(template_name)
        if title_key:
            try:
                title = get_translation(title_key, language)
            except KeyError:
                title = self._get_title(template_name, language)
        else:
            title = self._get_title(template_name, language)
        
        # Render full HTML using base template
        base_variables = {
            "subject": subject,
            "title": title,
            "content": rendered_content,
            "current_year": variables.get("current_year", datetime.now().year),
            "lang": language
        }
        
        html_content = self._render_template(
            self.base_template, base_variables
        )
        
        # Generate plain text version (simple conversion)
        text_content = self._html_to_text(rendered_content)
        
        return {
            "subject": base_variables["subject"],
            "html": html_content,
            "text": text_content
        }
    
    def _get_title(self, template_name: str, language: str) -> str:
        """Get email title based on template name and language."""
        titles = {
            "verification": {
                "en": "Verify Your Email Address",
                "de": "Bestätigen Sie Ihre E-Mail-Adresse"
            },
            "password_reset": {
                "en": "Reset Your Password",
                "de": "Setzen Sie Ihr Passwort zurück"
            },
            "newsletter_welcome": {
                "en": "Welcome to Hackathon Hub!",
                "de": "Willkommen beim Hackathon Hub!"
            }
        }
        
        if template_name in titles and language in titles[template_name]:
            return titles[template_name][language]
        
        # Fallback
        return {
            "verification": "Verify Your Email",
            "password_reset": "Reset Password",
            "newsletter_welcome": "Welcome"
        }.get(template_name, "Email from Hackathon Dashboard")
    
    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text (simplified)."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        
        # Replace common HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&', '&')
        text = text.replace('<', '<')
        text = text.replace('>', '>')
        text = text.replace('"', '"')
        
        # Collapse multiple whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Trim
        text = text.strip()
        
        return text


# Global template engine instance
template_engine = TemplateEngine()