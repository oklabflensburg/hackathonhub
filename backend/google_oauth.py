import httpx
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
from datetime import datetime

import crud
import schemas
import auth

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_CALLBACK_URL = os.getenv("GOOGLE_CALLBACK_URL")
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]


def validate_google_config():
    """Validate that Google OAuth credentials are configured"""
    default_client_id = "your-google-client-id-here"
    default_client_secret = "your-google-client-secret-here"
    
    if not GOOGLE_CLIENT_ID or GOOGLE_CLIENT_ID == default_client_id:
        raise ValueError(
            "Google OAuth is not configured. Please set GOOGLE_CLIENT_ID "
            "in .env file. See backend/.env for instructions."
        )
    if (not GOOGLE_CLIENT_SECRET or 
            GOOGLE_CLIENT_SECRET == default_client_secret):
        raise ValueError(
            "Google OAuth is not configured. Please set GOOGLE_CLIENT_SECRET "
            "in .env file. See backend/.env for instructions."
        )
    if not GOOGLE_CALLBACK_URL:
        raise ValueError(
            "Google OAuth callback URL is not configured. "
            "Please set GOOGLE_CALLBACK_URL in .env file."
        )


def get_google_auth_url(redirect_url: str = None):
    """Generate Google OAuth authorization URL"""
    # Validate configuration before generating URL
    validate_google_config()
    
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_CALLBACK_URL,
        "response_type": "code",
        "scope": " ".join(GOOGLE_SCOPES),
        "access_type": "offline",  # Get refresh token
        "prompt": "select_account"  # Force account selection
    }
    
    if redirect_url:
        params["state"] = redirect_url
    
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"


async def exchange_code_for_token(code: str):
    """Exchange Google OAuth code for access token"""
    # Validate configuration before making API call
    validate_google_config()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            headers={"Accept": "application/json"},
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": GOOGLE_CALLBACK_URL
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to exchange code: {response.text}")
        
        return response.json()


async def get_google_user_info(access_token: str):
    """Get user info from Google API using access token"""
    async with httpx.AsyncClient() as client:
        # Get user info
        user_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
        )
        
        if user_response.status_code != 200:
            raise Exception(f"Failed to get user info: {user_response.text}")
        
        user_data = user_response.json()
        
        return {
            "google_id": user_data["id"],
            "email": user_data["email"],
            "email_verified": user_data.get("verified_email", False),
            "username": user_data.get("email", "").split("@")[0],
            "name": user_data.get("name", ""),
            "avatar_url": user_data.get("picture", ""),
            "locale": user_data.get("locale", "en"),
            "given_name": user_data.get("given_name", ""),
            "family_name": user_data.get("family_name", "")
        }


async def authenticate_with_google(code: str, db: Session):
    """Complete Google OAuth authentication flow"""
    # Exchange code for access token
    token_data = await exchange_code_for_token(code)
    access_token = token_data.get("access_token")
    
    if not access_token:
        raise Exception("No access token received from Google")
    
    # Get user info from Google
    google_user = await get_google_user_info(access_token)
    
    # Check if user exists by Google ID
    db_user = crud.get_user_by_google_id(db, google_user["google_id"])
    
    if not db_user:
        # Check if user exists by email (merge accounts)
        db_user = crud.get_user_by_email(db, google_user["email"])
        
        if db_user:
            # Update existing user with Google ID
            db_user = crud.update_user_google_id(
                db, db_user.id, google_user["google_id"])
        else:
            # Create new user
            user_create = schemas.UserCreate(
                google_id=google_user["google_id"],
                username=google_user["username"],
                email=google_user["email"],
                name=google_user["name"],
                avatar_url=google_user["avatar_url"],
                auth_method="google",
                email_verified=google_user["email_verified"]
            )
            db_user = crud.create_user(db, user_create)
    else:
        # Update existing user with latest info
        db_user = crud.update_user_last_login(db, db_user.id)
    
    # Create JWT tokens
    tokens = auth.create_tokens(db_user.id, db_user.username)
    
    # Store refresh token in database
    try:
        crud.create_refresh_token(
            db,
            user_id=db_user.id,
            token_id=tokens["refresh_token_id"],
            expires_at=datetime.utcnow() + tokens["refresh_token_expires"]
        )
    except Exception as e:
        # Log the error but don't fail the authentication
        # This allows Google OAuth to work even if refresh token storage fails
        import logging
        logging.error(f"Failed to store refresh token: {e}")
        # Continue without storing refresh token
    
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer",
        "user": schemas.User.from_orm(db_user)
    }