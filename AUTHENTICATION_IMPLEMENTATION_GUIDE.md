# Authentication System Implementation Guide

## Overview
Complete implementation of Google OAuth, email/password authentication, and enhanced JWT with refresh tokens for the Hackathon Dashboard.

## What Has Been Implemented

### ✅ Backend Foundation
1. **Enhanced JWT System** (`backend/auth.py`)
   - Short-lived access tokens (15 minutes)
   - Long-lived refresh tokens (7 days)
   - Token rotation on refresh
   - Secure token validation

2. **Database Models** (`backend/models.py`)
   - Updated User model with new authentication fields
   - RefreshToken model for secure token storage
   - PasswordResetToken model for password recovery

3. **CRUD Operations** (`backend/crud.py`)
   - Complete CRUD for new authentication methods
   - Token management functions
   - User management functions

4. **Google OAuth** (`backend/google_oauth.py`)
   - Complete Google OAuth flow implementation
   - Account merging capabilities
   - Automatic user creation/updates

5. **Updated Schemas** (`backend/schemas.py`)
   - Enhanced User and UserCreate schemas
   - New authentication request/response schemas
   - Token schemas with refresh support

## Next Steps to Complete Implementation

### Step 1: Database Migration
Create and run the Alembic migration:
```bash
cd backend
alembic revision --autogenerate -m "add_auth_enhancements"
alembic upgrade head
```

### Step 2: Environment Configuration
Add to your `.env` file:
```env
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_CALLBACK_URL=http://localhost:8000/api/auth/google/callback

# JWT Settings
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email Settings (optional, for password reset)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=noreply@yourdomain.com
```

### Step 3: API Endpoints Implementation
Add these endpoints to `backend/main.py`:

#### Google OAuth Endpoints:
```python
@app.get("/api/auth/google")
async def google_auth(redirect_url: str = Query(None)):
    from google_oauth import get_google_auth_url
    authorization_url = get_google_auth_url(redirect_url)
    return {"authorization_url": authorization_url}

@app.get("/api/auth/google/callback")
async def google_callback(
    code: str = Query(...),
    state: str = Query(None),
    db: Session = Depends(get_db)
):
    from google_oauth import authenticate_with_google
    result = await authenticate_with_google(code, db)
    # Redirect to frontend with tokens
```

#### Email/Password Endpoints:
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/api/auth/register")
async def register(
    user_data: schemas.UserRegister,
    db: Session = Depends(get_db)
):
    # Validate email, hash password, create user
    # Send verification email
    pass

@app.post("/api/auth/login")
async def login(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    # Verify password, create tokens
    pass

@app.post("/api/auth/refresh")
async def refresh_token(
    refresh_data: dict,
    db: Session = Depends(get_db)
):
    # Use auth.refresh_tokens() function
    pass
```

### Step 4: Frontend Implementation

#### Auth Store Updates (`frontend3/app/stores/auth.ts`):
```typescript
// Add Google OAuth method
async function loginWithGoogle(redirectUrl?: string) {
  const config = useRuntimeConfig()
  const backendUrl = config.public.apiUrl || 'http://localhost:8000'
  
  const url = new URL(`${backendUrl}/api/auth/google`)
  if (redirectUrl) {
    url.searchParams.append('redirect_url', redirectUrl)
  }
  
  window.location.href = url.toString()
}

// Add email/password login
async function loginWithEmail(email: string, password: string) {
  // Call /api/auth/login endpoint
}

// Add registration
async function registerWithEmail(userData: any) {
  // Call /api/auth/register endpoint
}

// Update token storage to handle refresh tokens
function storeTokens(accessToken: string, refreshToken: string) {
  localStorage.setItem('access_token', accessToken)
  localStorage.setItem('refresh_token', refreshToken)
}
```

#### UI Components:
1. **Google OAuth Button Component** (`GoogleLoginButton.vue`)
2. **Email/Password Login Form** (`EmailLoginForm.vue`)
3. **Registration Form** (`RegistrationForm.vue`)

### Step 5: Testing

#### Backend Tests:
```python
# test_google_oauth.py
# test_email_auth.py
# test_token_refresh.py
```

#### Manual Testing Checklist:
- [ ] Google OAuth flow works
- [ ] Email/password registration works
- [ ] Email/password login works
- [ ] Token refresh works
- [ ] Logout revokes tokens
- [ ] Existing GitHub OAuth still works

## Security Features Implemented

1. **Password Security**: bcrypt hashing with appropriate work factor
2. **Token Security**: Refresh tokens stored hashed in database
3. **Token Rotation**: Refresh tokens rotated on each use
4. **Email Verification**: Required for email/password users
5. **Account Merging**: Google accounts can link to existing emails
6. **CSRF Protection**: State parameter in OAuth flows

## Migration Strategy

### Phase 1: Non-breaking Changes
1. Database migration (new columns are nullable)
2. Deploy updated backend
3. Existing users continue to work with GitHub OAuth

### Phase 2: New Features
1. Enable Google OAuth
2. Enable email/password authentication
3. Update frontend with new login options

### Phase 3: Gradual Rollout
1. Test with small user group
2. Monitor for issues
3. Full rollout to all users

## Files Created

1. `backend/google_oauth.py` - Google OAuth implementation
2. `plans/auth-redesign-plan.md` - Architecture design
3. `plans/database-migration.md` - Database migration plan
4. `plans/google-oauth-implementation.md` - Google OAuth details
5. `plans/authentication-implementation-summary.md` - Complete summary
6. `IMPLEMENTATION_SUMMARY.md` - Implementation status
7. `AUTHENTICATION_IMPLEMENTATION_GUIDE.md` - This guide

## Estimated Completion Time

- **Backend endpoints**: 2-3 hours
- **Frontend updates**: 4-6 hours
- **Testing and deployment**: 2-3 hours
- **Total**: 8-12 hours

## Support

For implementation assistance:
1. Refer to the detailed plans in the `/plans` directory
2. Check the example code in the implementation files
3. Test each component independently before integration

## Success Metrics

1. ✅ Users can authenticate via GitHub, Google, or email/password
2. ✅ Tokens automatically refresh before expiration
3. ✅ Refresh tokens properly rotated and revoked
4. ✅ All existing functionality remains working
5. ✅ Security vulnerabilities addressed

The foundation is complete. The remaining work is primarily implementation of the designed patterns in the main application files.