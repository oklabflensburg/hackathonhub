"""
i18n helper functions for HTTP exceptions with translation support.
Provides convenient functions to raise HTTPException with localized messages.
"""

from fastapi import HTTPException, status
from typing import Any, Optional

from .translations import get_translation


def raise_i18n_http_exception(
    locale: str,
    status_code: int,
    translation_key: str,
    **kwargs: Any
) -> None:
    """
    Raise an HTTPException with i18n support.
    
    Args:
        locale: Language code (e.g., 'en', 'de')
        status_code: HTTP status code (use FastAPI status constants)
        translation_key: Translation key in format "category.subkey"
        **kwargs: Format arguments for the translation string
    
    Raises:
        HTTPException: With localized detail message
    """
    detail = get_translation(translation_key, locale, **kwargs)
    raise HTTPException(status_code=status_code, detail=detail)


def raise_not_found(locale: str, entity: str, **kwargs: Any) -> None:
    """
    Raise a 404 Not Found exception with localized message.
    
    Args:
        locale: Language code
        entity: Entity name (e.g., 'project', 'user', 'team')
        **kwargs: Additional format arguments
    
    Raises:
        HTTPException: 404 Not Found with localized message
    """
    return raise_i18n_http_exception(
        locale=locale,
        status_code=status.HTTP_404_NOT_FOUND,
        translation_key=f"errors.{entity}_not_found",
        **kwargs
    )


def raise_forbidden(
    locale: str,
    action: Optional[str] = None,
    **kwargs: Any
) -> None:
    """
    Raise a 403 Forbidden exception with localized message.
    
    Args:
        locale: Language code
        action: Optional specific action for more precise error messages
        **kwargs: Additional format arguments
    
    Raises:
        HTTPException: 403 Forbidden with localized message
    """
    if action:
        translation_key = f"errors.forbidden_{action}"
    else:
        translation_key = "errors.forbidden"
    
    return raise_i18n_http_exception(
        locale=locale,
        status_code=status.HTTP_403_FORBIDDEN,
        translation_key=translation_key,
        **kwargs
    )


def raise_unauthorized(
    locale: str,
    reason: Optional[str] = None,
    **kwargs: Any
) -> None:
    """
    Raise a 401 Unauthorized exception with localized message.
    
    Args:
        locale: Language code
        reason: Optional specific reason for unauthorized access
        **kwargs: Additional format arguments
    
    Raises:
        HTTPException: 401 Unauthorized with localized message
    """
    if reason:
        translation_key = f"errors.unauthorized_{reason}"
    else:
        translation_key = "errors.unauthorized"
    
    return raise_i18n_http_exception(
        locale=locale,
        status_code=status.HTTP_401_UNAUTHORIZED,
        translation_key=translation_key,
        **kwargs
    )


def raise_bad_request(
    locale: str,
    validation_key: Optional[str] = None,
    **kwargs: Any
) -> None:
    """
    Raise a 400 Bad Request exception with localized message.
    
    Args:
        locale: Language code
        validation_key: Optional specific validation error key
        **kwargs: Additional format arguments
    
    Raises:
        HTTPException: 400 Bad Request with localized message
    """
    if validation_key:
        translation_key = f"errors.validation_{validation_key}"
    else:
        translation_key = "errors.validation_error"
    
    return raise_i18n_http_exception(
        locale=locale,
        status_code=status.HTTP_400_BAD_REQUEST,
        translation_key=translation_key,
        **kwargs
    )


def raise_internal_server_error(
    locale: str,
    component: Optional[str] = None,
    **kwargs: Any
) -> None:
    """
    Raise a 500 Internal Server Error exception with localized message.
    
    Args:
        locale: Language code
        component: Optional component name for more specific error
        **kwargs: Additional format arguments
    
    Raises:
        HTTPException: 500 Internal Server Error with localized message
    """
    if component:
        translation_key = f"errors.server_{component}"
    else:
        translation_key = "errors.server_error"
    
    return raise_i18n_http_exception(
        locale=locale,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        translation_key=translation_key,
        **kwargs
    )


def get_locale_from_request(request) -> str:
    """
    Extract locale from request state.
    
    Args:
        request: FastAPI request object
    
    Returns:
        Language code (defaults to 'en' if not found)
    """
    # Try to get locale from request state (set by middleware)
    locale = request.state.get("locale", "en")
    return locale


# Convenience function for common validation errors
def raise_validation_error(
    locale: str,
    field: Optional[str] = None,
    error_type: Optional[str] = None,
    **kwargs: Any
) -> None:
    """
    Raise a validation error with localized message.
    
    Args:
        locale: Language code
        field: Optional field name
        error_type: Type of validation error (e.g., 'required', 'invalid')
        **kwargs: Additional format arguments
    
    Raises:
        HTTPException: 400 Bad Request with localized validation message
    """
    if field and error_type:
        translation_key = f"validation.{field}_{error_type}"
    elif error_type:
        translation_key = f"validation.{error_type}"
    else:
        translation_key = "errors.validation_error"
    
    return raise_i18n_http_exception(
        locale=locale,
        status_code=status.HTTP_400_BAD_REQUEST,
        translation_key=translation_key,
        **kwargs
    )