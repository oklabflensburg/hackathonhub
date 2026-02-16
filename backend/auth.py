from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

import crud
import schemas
from database import get_db

load_dotenv()

# JWT configuration
SECRET_KEY = os.getenv(
    "SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security warning for default secret key
if SECRET_KEY == "your-secret-key-here-change-in-production":
    import warnings
    warnings.warn(
        "Using default SECRET_KEY. This is insecure for production. "
        "Set the SECRET_KEY environment variable.",
        UserWarning
    )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception


def refresh_access_token(token: str):
    """Refresh an access token if it's still valid or within grace period"""
    try:
        # Decode without verification to check expiration
        payload = jwt.decode(token, SECRET_KEY, algorithms=[
                             ALGORITHM], options={"verify_exp": False})
        username_or_email: str = payload.get("sub")
        if username_or_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Check if token is expired but within grace period (e.g., 5 minutes)
        exp = payload.get("exp")
        if exp:
            current_time = datetime.utcnow().timestamp()
            # If token expired more than 5 minutes ago, require re-login
            if current_time > exp + 300:  # 5 minutes grace period
                raise HTTPException(
                    status_code=401,
                    detail="Token expired, please login again")

        # Create new token with username (not email)
        # We need to get the actual username from database
        # For simplicity, we'll use the same value for now
        # In production, you might want to look up the user to get username
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_token = create_access_token(
            data={"sub": username_or_email}, expires_delta=access_token_expires
        )
        return new_token
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    # Try to find user by username (stored in token sub field)
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        # Fallback: try to find by email (for backward compatibility)
        user = crud.get_user_by_email(db, email=token_data.username)
        if user is None:
            raise credentials_exception
    return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user)
):
    # For now, all users are considered active
    # You could add logic to check if user is disabled, etc.
    return current_user

# GitHub OAuth helper functions


async def authenticate_github_user(code: str, db: Session):
    """
    Authenticate user via GitHub OAuth
    
    This function implements the complete GitHub OAuth flow:
    1. Exchange code for access token with GitHub
    2. Use access token to get user info from GitHub API
    3. Create or update user in database
    4. Return JWT token for the application
    
    Args:
        code: The OAuth authorization code from GitHub
        db: Database session
    
    Returns:
        Dictionary with access_token, token_type, and user info
    """
    # Use the actual GitHub OAuth implementation
    from github_oauth import authenticate_with_github
    return await authenticate_with_github(code, db)
