# Google OAuth Implementation Plan

## Overview
Implement Google OAuth authentication alongside existing GitHub OAuth. The implementation will follow a similar pattern to the GitHub OAuth flow.

## File Structure

### New Files:
1. `backend/google_oauth.py` - Google OAuth logic
2. `backend/auth_utils.py` - Shared authentication utilities (optional)

### Modified Files:
1. `backend/main.py` - Add Google OAuth endpoints
2. `backend/models.py` - Add Google OAuth fields
3. `backend/schemas.py` - Add Google OAuth schemas
4. `backend/crud.py` - Add Google OAuth user operations

## Implementation Details

### 1. Google OAuth Configuration

**Environment Variables:**
```python
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_CALLBACK_URL = os.getenv("GOOGLE_CALLBACK_URL", "http://localhost:8000/api/auth/google/callback")
```

**OAuth Scopes:**
```python
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]
```

### 2. Google OAuth Flow

```
1. Frontend → GET /api/auth/google?redirect_url=...
2. Backend → Returns Google authorization URL
3. Frontend → Redirects user to Google
4. Google → Redirects to /api/auth/google/callback with code
5. Backend → Exchanges code for tokens, gets user info
6. Backend → Creates/updates user, returns JWT
7. Backend → Redirects to frontend with token
```

### 3. Google OAuth Implementation (`google_oauth.py`)

```python
import httpx
from sqlalchemy.orm import Session
from datetime import timedelta
import os
from dotenv import load_dotenv
from urllib.parse import urlencode

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

def get_google_auth_url(redirect_url: str = None):
    """Generate Google OAuth authorization URL"""
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
            "username": user_data.get("email", "").split("@")[0],  # Use email prefix as username
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
            db_user = crud.update_user_google_id(db, db_user.id, google_user["google_id"])
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
    
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer",
        "user": schemas.User.from_orm(db_user)
    }
```

### 4. Updated CRUD Operations (`crud.py`)

Add these functions:

```python
def get_user_by_google_id(db: Session, google_id: str):
    return db.query(models.User).filter(models.User.google_id == google_id).first()

def update_user_google_id(db: Session, user_id: int, google_id: str):
    user = get_user(db, user_id)
    if user:
        user.google_id = google_id
        user.auth_method = "google"
        db.commit()
        db.refresh(user)
    return user

def update_user_last_login(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
    return user
```

### 5. Updated Auth Module (`auth.py`)

Add enhanced token creation with refresh tokens:

```python
from datetime import datetime, timedelta
import uuid

# Update token expiration times
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Reduced from 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_tokens(user_id: int, username: str):
    """Create access and refresh token pair"""
    # Access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username, "user_id": user_id, "type": "access"},
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
```

### 6. API Endpoints (`main.py`)

Add these endpoints:

```python
@app.get("/api/auth/google")
async def google_auth(redirect_url: str = Query(None)):
    """Initiate Google OAuth flow"""
    from google_oauth import get_google_auth_url
    
    authorization_url = get_google_auth_url(redirect_url)
    return {"authorization_url": authorization_url}

@app.get("/api/auth/google/callback")
async def google_callback(
    code: str = Query(...),
    state: str = Query(None),
    db: Session = Depends(get_db)
):
    """Google OAuth callback endpoint"""
    try:
        from google_oauth import authenticate_with_google
        result = await authenticate_with_google(code, db)
        
        # Store refresh token in database
        from crud import create_refresh_token
        create_refresh_token(
            db,
            user_id=result["user"].id,
            token_id=result["refresh_token_id"],
            expires_at=datetime.utcnow() + result["refresh_token_expires"]
        )
        
        # Redirect to frontend
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        import urllib.parse
        
        # Encode tokens for URL
        access_token = urllib.parse.quote(result["access_token"])
        refresh_token = urllib.parse.quote(result["refresh_token"])
        
        # Build redirect URL
        if state:
            try:
                decoded_state = urllib.parse.unquote(state)
                redirect_url = f"{frontend_url}{decoded_state}"
            except:
                redirect_url = f"{frontend_url}/"
        else:
            redirect_url = f"{frontend_url}/"
        
        # Add tokens to URL
        redirect_url += f"?access_token={access_token}&refresh_token={refresh_token}&source=google"
        
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        logger.error(f"Google OAuth error: {e}")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        error_url = f"{frontend_url}/login?error=google_auth_failed"
        return RedirectResponse(url=error_url)
```

### 7. Frontend Integration

**Auth Store Updates:**
```typescript
async function loginWithGoogle(redirectUrl?: string) {
  // Similar to loginWithGitHub but calls /api/auth/google
}

function handleGoogleCallback() {
  // Parse tokens from URL, store them
  // Use refresh token for auto-refresh
}
```

**UI Component:**
```vue
<template>
  <button @click="loginWithGoogle" class="google-login-btn">
    <GoogleIcon /> Sign in with Google
  </button>
</template>
```

## Testing Strategy

### Unit Tests:
1. `test_google_oauth.py` - Test OAuth flow functions
2. `test_google_user_info.py` - Test user info parsing

### Integration Tests:
1. Test complete OAuth flow with mock Google API
2. Test account merging (email already exists)
3. Test token creation and validation

### Manual Testing:
1. Register Google OAuth app in Google Cloud Console
2. Test complete flow from frontend to backend
3. Test token refresh functionality

## Security Considerations

1. **State Parameter:** Use state parameter to prevent CSRF
2. **PKCE:** Consider implementing PKCE for enhanced security
3. **Token Storage:** Store refresh tokens securely in database
4. **Scope Limitation:** Request minimal scopes needed
5. **Email Verification:** Trust Google's email verification

## Error Handling

1. **Invalid Code:** Return 400 with descriptive error
2. **Network Issues:** Retry logic with exponential backoff
3. **User Cancels:** Redirect to login page with cancellation message
4. **Account Already Exists:** Merge accounts or show error

## Deployment Checklist

1. [ ] Register application in Google Cloud Console
2. [ ] Configure OAuth consent screen
3. [ ] Add authorized redirect URIs
4. [ ] Set environment variables in production
5. [ ] Test in staging environment
6. [ ] Monitor logs for authentication errors

## Migration from GitHub OAuth

The Google OAuth implementation is designed to work alongside GitHub OAuth:
- Users can have both GitHub and Google IDs
- `auth_method` field tracks primary authentication method
- Email addresses must remain unique across providers

## Performance Considerations

1. **Token Caching:** Cache Google API responses where appropriate
2. **Database Indexes:** Ensure indexes on google_id and email fields
3. **Connection Pooling:** Use HTTP connection pooling for Google API calls

## Monitoring and Logging

1. Log successful/failed authentication attempts
2. Track authentication method usage statistics
3. Monitor token refresh rates
4. Alert on authentication failure spikes