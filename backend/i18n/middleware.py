"""
Middleware for language detection and localization in FastAPI.
"""

from fastapi import Request
from fastapi.middleware import Middleware


def get_locale(request: Request) -> str:
    """
    Extract locale from Accept-Language header or default to 'en'.
    
    Args:
        request: FastAPI request object
    
    Returns:
        Language code ('en' or 'de')
    """
    accept_language = request.headers.get("Accept-Language", "en")
    
    # Parse Accept-Language header (e.g., "en-US,en;q=0.9,de;q=0.8")
    languages = accept_language.split(",")
    for lang in languages:
        # Extract language code (e.g., "en" from "en-US" or "en;q=0.9")
        lang_code = lang.split(";")[0].strip().split("-")[0].lower()
        
        # Check if it's a supported language
        if lang_code in ["en", "de"]:
            return lang_code
    
    # Default to English
    return "en"


class LocaleMiddleware:
    """
    Middleware to add locale to request state.
    """
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        # Create request object to access headers
        request = Request(scope, receive)
        locale = get_locale(request)
        
        # Add locale to request state
        scope["state"] = scope.get("state", {})
        scope["state"]["locale"] = locale
        
        await self.app(scope, receive, send)


def create_i18n_middleware() -> Middleware:
    """
    Create i18n middleware for FastAPI.
    
    Returns:
        FastAPI Middleware instance
    """
    return Middleware(LocaleMiddleware)


def get_locale_from_request(request: Request) -> str:
    """
    Get locale from request state (for use in dependencies).
    
    Args:
        request: FastAPI request object
    
    Returns:
        Language code
    """
    return request.state.get("locale", "en")