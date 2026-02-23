"""
Internationalization module for Hackathon Dashboard backend.
Provides translation support for error messages, success messages,
and other user-facing strings.
"""

from .translations import TRANSLATIONS, get_translation
from .middleware import get_locale, LocaleMiddleware

__all__ = [
    "TRANSLATIONS",
    "get_translation",
    "get_locale",
    "LocaleMiddleware"
]