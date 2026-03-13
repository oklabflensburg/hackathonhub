"""
Jinja2-based template engine for rendering email templates.
Replaces the custom template engine with full Jinja2 feature support.
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.exceptions import TemplateNotFound

from app.i18n.translations import get_translation

logger = logging.getLogger(__name__)


class Jinja2TemplateEngine:
    """Jinja2-based template engine for email rendering."""

    def __init__(self, template_dir: str = "templates/emails"):
        """
        Initialize Jinja2 template engine.

        Args:
            template_dir: Directory containing email templates
        """
        self.template_dir = template_dir
        self.env = self._create_jinja2_environment()
        self.base_template = self._load_base_template()

    def _create_jinja2_environment(self) -> Environment:
        """Create Jinja2 environment with custom filters and globals."""
        # Convert template_dir to absolute path
        abs_template_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            self.template_dir
        )

        env = Environment(
            loader=FileSystemLoader(abs_template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Add custom filters
        env.filters['truncate'] = self._truncate_filter
        env.filters['date_format'] = self._date_format_filter

        # Add global functions
        env.globals['get_translation'] = get_translation
        env.globals['current_year'] = datetime.now().year

        return env

    def _load_base_template(self) -> Optional[str]:
        """Load base template content."""
        try:
            base_path = os.path.join(self.template_dir, "base.html")
            with open(base_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Base template not found: {base_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading base template: {e}")
            return None

    @staticmethod
    @staticmethod
    def _truncate_filter(text: str, length: int = 100,
                         end: str = "...") -> str:
        """Truncate text to specified length."""
        if len(text) <= length:
            return text
        return text[:length - len(end)] + end

    @staticmethod
    def _date_format_filter(date_str: str,
                            format_str: str = "%Y-%m-%d") -> str:
        """Format date string."""
        try:
            if isinstance(date_str, str):
                # Try to parse the date string
                from datetime import datetime as dt
                date_obj = dt.fromisoformat(date_str.replace('Z', '+00:00'))
                return date_obj.strftime(format_str)
        except (ValueError, AttributeError):
            pass
        return date_str

    def render_email(
        self,
        template_name: str,
        language: str = "en",
        variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Render email template with given variables using Jinja2.

        Args:
            template_name: Name of template directory (e.g., "verification")
            language: Language code (e.g., "en", "de")
            variables: Dictionary of template variables

        Returns:
            Dictionary with "subject", "html", and "text" keys

        Raises:
            ValueError: If template not found
            TemplateSyntaxError: If template has syntax errors
        """
        if variables is None:
            variables = {}

        # Add current year if not provided
        if "current_year" not in variables:
            variables["current_year"] = datetime.now().year

        # Try to load language-specific template
        template_path = f"{template_name}/{language}.html"

        try:
            template = self.env.get_template(template_path)
        except TemplateNotFound:
            # Fallback to English if language-specific template not found
            if language != "en":
                logger.warning(
                    f"Template {template_name}/{language}.html not found, "
                    f"falling back to English"
                )
                template_path = f"{template_name}/en.html"
                template = self.env.get_template(template_path)
            else:
                raise ValueError(
                    f"Template {template_name} not found for "
                    f"language {language}"
                )

        # Get subject from translations
        subject_key_map = {
            "verification": "email.verification_subject",
            "password_reset": "email.password_reset_subject",
            "newsletter_welcome": "email.newsletter_welcome_subject",
            "team/invitation_sent": "email.team_invitation_subject",
            "team/invitation_accepted":
                "email.team_invitation_accepted_subject",
            "team/member_added": "email.team_member_added_subject",
            "team/created": "email.team_created_subject",
            "project/created": "email.project_created_subject",
            "project/commented": "email.project_commented_subject",
            "hackathon/registered": "email.hackathon_registered_subject",
            "hackathon/started": "email.hackathon_started_subject"
        }

        subject_key = subject_key_map.get(template_name)
        if subject_key:
            try:
                # Use Jinja2 to render subject with variables
                subject_template = get_translation(subject_key, language)
                # Create a simple Jinja2 environment for subject rendering
                subject_env = Environment()
                subject_template_parsed = subject_env.from_string(
                    subject_template
                )
                subject = subject_template_parsed.render(**variables)
            except KeyError:
                subject = "Email from Hackathon Dashboard"
        else:
            subject = "Email from Hackathon Dashboard"

        # Get title from translations
        title_key_map = {
            "verification": "email.verification_title",
            "password_reset": "email.password_reset_title",
            "newsletter_welcome": "email.newsletter_welcome_title",
            "team/invitation_sent": "email.team_invitation_title",
            "team/invitation_accepted": "email.team_invitation_accepted_title",
            "team/member_added": "email.team_member_added_title",
            "team/created": "email.team_created_title",
            "project/created": "email.project_created_title",
            "project/commented": "email.project_commented_title",
            "hackathon/registered": "email.hackathon_registered_title",
            "hackathon/started": "email.hackathon_started_title"
        }

        title_key = title_key_map.get(template_name)
        if title_key:
            try:
                title = get_translation(title_key, language)
            except KeyError:
                title = self._get_title(template_name, language)
        else:
            title = self._get_title(template_name, language)

        # Add common variables
        variables.update({
            "subject": subject,
            "title": title,
            "lang": language
        })

        # Render content using Jinja2
        rendered_content = template.render(**variables)

        # Generate plain text version
        text_content = self._html_to_text(rendered_content)

        return {
            "subject": subject,
            "html": rendered_content,
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
            },
            "team/invitation_sent": {
                "en": "Team Invitation",
                "de": "Teameinladung"
            },
            "team/invitation_accepted": {
                "en": "Invitation Accepted",
                "de": "Einladung angenommen"
            },
            "team/member_added": {
                "en": "Team Member Added",
                "de": "Teammitglied hinzugefügt"
            },
            "team/created": {
                "en": "Team Created",
                "de": "Team erstellt"
            },
            "project/created": {
                "en": "New Project",
                "de": "Neues Projekt"
            },
            "project/commented": {
                "en": "New Project Comment",
                "de": "Neuer Projekt-Kommentar"
            },
            "hackathon/registered": {
                "en": "Hackathon Registration",
                "de": "Hackathon-Registrierung"
            },
            "hackathon/started": {
                "en": "Hackathon Started",
                "de": "Hackathon gestartet"
            }
        }

        if template_name in titles and language in titles[template_name]:
            return titles[template_name][language]

        # Fallback
        fallback_titles = {
            "verification": "Verify Your Email",
            "password_reset": "Reset Password",
            "newsletter_welcome": "Welcome"
        }

        return fallback_titles.get(
            template_name, "Email from Hackathon Dashboard"
        )

    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text (simplified)."""
        import re

        # Remove HTML tags but keep line breaks for paragraphs
        text = re.sub(r'<br\s*/?>', '\n', html)
        text = re.sub(r'<p.*?>', '\n', text)
        text = re.sub(r'</p>', '\n\n', text)
        text = re.sub(r'<[^>]+>', '', text)

        # Replace common HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&', '&')
        text = text.replace('<', '<')
        text = text.replace('>', '>')
        text = text.replace('"', '"')

        # Collapse multiple whitespace and newlines
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)

        # Trim
        text = text.strip()

        return text

    def get_template_variables(self, template_name: str,
                               language: str = "en") -> Dict:
        """
        Get available variables for a template by analyzing it.

        Args:
            template_name: Name of template
            language: Language code

        Returns:
            Dictionary with variable information
        """
        try:
            template_path = f"{template_name}/{language}.html"
            template_source = self.env.loader.get_source(
                self.env, template_path
            )[0]

            # Simple extraction of variable names from {{ variable }} patterns
            import re
            variables = set()

            # Find all {{ variable }} patterns
            pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}'
            matches = re.findall(pattern, template_source)
            variables.update(matches)

            # Find all {{ variable|filter }} patterns
            pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\|'
            matches = re.findall(pattern, template_source)
            variables.update(matches)

            return {
                "template_name": template_name,
                "language": language,
                "variables": sorted(list(variables))
            }

        except Exception as e:
            logger.error(f"Failed to analyze template variables: {e}")
            return {
                "template_name": template_name,
                "language": language,
                "variables": []
            }


# Global Jinja2 template engine instance
jinja2_template_engine = Jinja2TemplateEngine()
