"""
Cookie-Hilfsfunktionen für HTTP-Only Authentifizierung.

Dieses Modul stellt Funktionen zum Setzen und Löschen von HTTP-Only Cookies
für die Authentifizierung bereit, um SSR-kompatible Authentifizierung zu
ermöglichen.
"""

from typing import Optional
from fastapi import Response
from app.core.config import settings


# Cookie-Konfiguration
AUTH_TOKEN_COOKIE_NAME = "auth_token"
REFRESH_TOKEN_COOKIE_NAME = "refresh_token"
COOKIE_MAX_AGE = 30 * 24 * 60 * 60  # 30 Tage in Sekunden
COOKIE_PATH = "/"
COOKIE_DOMAIN = None  # None = aktueller Domain
COOKIE_SECURE = not settings.DEBUG  # Nur über HTTPS (in Produktion)
COOKIE_HTTP_ONLY = True  # Nicht zugänglich via JavaScript
COOKIE_SAME_SITE = "lax"  # Schutz vor CSRF


def set_auth_cookies(
    response: Response,
    auth_token: str,
    refresh_token: str,
    persistent: bool = True,
    max_age: Optional[int] = None,
    secure: Optional[bool] = None,
    domain: Optional[str] = None,
) -> None:
    """
    Setzt HTTP-Only Cookies für Authentifizierungstokens.
    
    Args:
        response: FastAPI Response-Objekt
        auth_token: JWT Access Token
        refresh_token: JWT Refresh Token
        persistent: Ob Cookies persistent sein sollen (default: True)
        max_age: Cookie-Lebensdauer in Sekunden 
                 (default: 30 Tage wenn persistent, sonst None)
        secure: Nur über HTTPS (default: True in Produktion)
        domain: Cookie-Domain (default: None = aktuelle Domain)
    """
    if max_age is None:
        max_age = COOKIE_MAX_AGE if persistent else None
    
    if secure is None:
        # Secure=True in Produktion, Secure=False in Entwicklung
        # basierend auf DEBUG-Einstellung
        secure = not settings.DEBUG
    
    # Auth-Token Cookie setzen
    response.set_cookie(
        key=AUTH_TOKEN_COOKIE_NAME,
        value=auth_token,
        max_age=max_age,
        path=COOKIE_PATH,
        domain=domain or COOKIE_DOMAIN,
        secure=secure,
        httponly=COOKIE_HTTP_ONLY,
        samesite=COOKIE_SAME_SITE,
    )
    
    # Refresh-Token Cookie setzen
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        max_age=max_age,
        path=COOKIE_PATH,
        domain=domain or COOKIE_DOMAIN,
        secure=secure,
        httponly=COOKIE_HTTP_ONLY,
        samesite=COOKIE_SAME_SITE,
    )


def clear_auth_cookies(response: Response) -> None:
    """
    Löscht die Authentifizierungs-Cookies.
    
    Args:
        response: FastAPI Response-Objekt
    """
    # Cookies mit abgelaufener Max-Age löschen
    response.delete_cookie(
        key=AUTH_TOKEN_COOKIE_NAME,
        path=COOKIE_PATH,
        domain=COOKIE_DOMAIN,
    )
    
    response.delete_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        path=COOKIE_PATH,
        domain=COOKIE_DOMAIN,
    )


def get_auth_token_from_cookies(request) -> Optional[str]:
    """
    Holt den Auth-Token aus den Cookies der Request.
    
    Args:
        request: FastAPI Request-Objekt
        
    Returns:
        Auth-Token oder None wenn nicht vorhanden
    """
    return request.cookies.get(AUTH_TOKEN_COOKIE_NAME)


def get_refresh_token_from_cookies(request) -> Optional[str]:
    """
    Holt den Refresh-Token aus den Cookies der Request.
    
    Args:
        request: FastAPI Request-Objekt
        
    Returns:
        Refresh-Token oder None wenn nicht vorhanden
    """
    return request.cookies.get(REFRESH_TOKEN_COOKIE_NAME)


def has_auth_cookies(request) -> bool:
    """
    Prüft ob Auth-Cookies in der Request vorhanden sind.
    
    Args:
        request: FastAPI Request-Objekt
        
    Returns:
        True wenn beide Cookies vorhanden sind
    """
    auth_token = get_auth_token_from_cookies(request)
    refresh_token = get_refresh_token_from_cookies(request)
    return auth_token is not None and refresh_token is not None