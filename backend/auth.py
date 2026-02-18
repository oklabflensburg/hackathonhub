from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
import uuid
from dotenv import load_dotenv

import crud
import schemas
from database import get_db

load_dotenv()

# JWT configuration
SECRET_KEY = os.getenv(
    "SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Security warning for default secret key
if SECRET_KEY == "your-secret-key-here-change-in-production":
    import warnings
    warnings.warn(
        "Using default SECRET_KEY. This is insecure for production. "
        "Set the SECRET_KEY environment variable.",
        UserWarning
    )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create a JWT token with expiration"""
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
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception


def create_tokens(user_id: int, username: str):
    """Create access and refresh token pair"""
    # Access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": username,
            "user_id": user_id,
            "type": "access"
        },
        expires_delta=access_token_expires
    )
    
    # Refresh token with unique ID
    refresh_token_id = str(uuid.uuid4())
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_access_token(
        data={
            "sub": username,
            "user_id": user_id,
            "type": "refresh",
            "jti": refresh_token_id
        },
        expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "refresh_token_id": refresh_token_id,
        "access_token_expires": access_token_expires,
        "refresh_token_expires": refresh_token_expires
    }


def verify_refresh_token(token: str, db: Session):
    """Verify a refresh token and return user info"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check token type
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        # Check token ID (jti)
        token_id = payload.get("jti")
        if not token_id:
            raise HTTPException(
                status_code=401, detail="Invalid refresh token")
        
        # Check if token is revoked in database
        refresh_token = crud.get_refresh_token(db, token_id)
        if not refresh_token or refresh_token.revoked:
            raise HTTPException(
                status_code=401, detail="Refresh token revoked")
        
        # Check expiration
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=401, detail="Refresh token expired")
        
        # Get user info
        username = payload.get("sub")
        user_id = payload.get("user_id")
        
        if not username or not user_id:
            raise HTTPException(
                status_code=401, detail="Invalid token payload")
        
        return {
            "username": username,
            "user_id": user_id,
            "token_id": token_id
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


def refresh_tokens(refresh_token: str, db: Session):
    """Refresh access token using a valid refresh token"""
    # Verify the refresh token
    token_info = verify_refresh_token(refresh_token, db)
    
    # Get user from database
    user = crud.get_user(db, token_info["user_id"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Revoke the old refresh token
    crud.revoke_refresh_token(db, token_info["token_id"])
    
    # Create new tokens
    new_tokens = create_tokens(user.id, user.username)
    
    # Store new refresh token in database
    crud.create_refresh_token(
        db,
        user_id=user.id,
        token_id=new_tokens["refresh_token_id"],
        expires_at=datetime.utcnow() + new_tokens["refresh_token_expires"]
    )
    
    return {
        "access_token": new_tokens["access_token"],
        "refresh_token": new_tokens["refresh_token"],
        "token_type": "bearer",
        "user": schemas.User.from_orm(user)
    }


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get current user from access token"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode token to check type
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type = payload.get("type")
        
        # Only accept access tokens
        if token_type != "access":
            raise credentials_exception
        
        # Use existing verify_token for backward compatibility
        token_data = verify_token(token, credentials_exception)
        
        # Try to find user by username (stored in token sub field)
        user = crud.get_user_by_username(db, username=token_data.username)
        if user is None:
            # Fallback: try to find by email (for backward compatibility)
            user = crud.get_user_by_email(db, email=token_data.username)
            if user is None:
                raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


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
