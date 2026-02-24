"""
Dependencies for i18n support in FastAPI routes.
Provides locale extraction from request for use in route functions.
"""

from fastapi import Request
from typing import Optional

from .middleware import get_locale_from_request


async def get_locale(request: Request) -> str:
    """
    Dependency to get locale from request.
    
    Args:
        request: FastAPI request object
    
    Returns:
        Language code (e.g., 'en', 'de')
    """
    return get_locale_from_request(request)


async def get_locale_or_default(
    request: Request,
    default: str = "en"
) -> str:
    """
    Dependency to get locale from request with fallback default.
    
    Args:
        request: FastAPI request object
        default: Default locale if not found in request
    
    Returns:
        Language code
    """
    locale = getattr(request.state, "locale", None)
    if locale is None:
        return default
    return locale


async def get_locale_with_fallback(
    request: Request,
    preferred: Optional[str] = None
) -> str:
    """
    Dependency to get locale with preferred fallback.
    
    Args:
        request: FastAPI request object
        preferred: Preferred locale if not found in request
    
    Returns:
        Language code
    """
    locale = getattr(request.state, "locale", None)
    if locale is None:
        if preferred is not None:
            return preferred
        return "en"
    return locale