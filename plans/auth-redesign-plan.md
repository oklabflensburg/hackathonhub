# Authentication System Redesign Plan

## Current System Analysis

The current authentication system uses:
1. **GitHub OAuth** - Working implementation with JWT tokens
2. **JWT tokens** - 30-minute access tokens with refresh endpoint
3. **Frontend auth store** - Token management with auto-refresh on 401
4. **Database** - Users stored with GitHub ID, username, email, etc.

## Requirements
1. Add Google OAuth alongside existing GitHub OAuth
2. Add email/password authentication
3. Implement proper refresh token system with auto-refresh
4. Maintain backward compatibility

## Architecture Design

### 1. Google OAuth Integration

**Backend Flow:**
```
Frontend → /api/auth/google → Google OAuth → /api/auth/google/callback → JWT
```

**Environment Variables Needed:**
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_CALLBACK_URL`

**Implementation Approach:**
- Create `google_oauth.py` similar to `github_oauth.py`
- Use Google People API for user info
- Store `google_id` in users table alongside `github_id`

### 2. Email/Password Authentication

**Database Changes:**
- Add `password_hash` column to users table (nullable)
- Add `email_verified` boolean column
- Add `auth_method` enum (github, google, email)

**Endpoints:**
- `POST /api/auth/register` - Create user with email/password
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/verify-email` - Email verification
- `POST /api/auth/forgot-password` - Password reset request
- `POST /api/auth/reset-password` - Password reset

**Security:**
- Use bcrypt for password hashing
- Implement email verification flow
- Rate limiting on login attempts

### 3. Enhanced JWT System

**Current Issue:** Single token with refresh endpoint but no proper refresh token storage

**Proposed Solution:**
```
Access Token: Short-lived (15 minutes)
Refresh Token: Long-lived (7 days), stored in database
```

**Token Structure:**
```python
# Access Token Payload
{
  "sub": "user_id",
  "type": "access",
  "exp": 1234567890
}

# Refresh Token Payload  
{
  "sub": "user_id",
  "type": "refresh",
  "jti": "unique_token_id",
  "exp": 1234567890
}
```

**Database Table:**
```sql
CREATE TABLE refresh_tokens (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  token_id VARCHAR(64) UNIQUE,  -- jti from JWT
  device_info TEXT,
  created_at TIMESTAMP,
  expires_at TIMESTAMP,
  revoked BOOLEAN DEFAULT FALSE
);
```

### 4. Auto-Refresh Implementation

**Frontend Strategy:**
1. Intercept 401 responses
2. Attempt refresh with stored refresh token
3. Retry original request with new access token
4. If refresh fails, logout user

**Refresh Token Rotation:**
- Issue new refresh token on each refresh
- Revoke old refresh token
- Prevent token reuse

## Implementation Plan

### Phase 1: Database Migration
1. Add new columns to users table
2. Create refresh_tokens table
3. Create migration script

### Phase 2: Backend Authentication
1. Implement Google OAuth
2. Implement email/password endpoints
3. Update JWT generation with refresh tokens
4. Add token refresh endpoint with rotation

### Phase 3: Frontend Updates
1. Update auth store for multiple login methods
2. Add Google OAuth button
3. Add email/password login/register forms
4. Implement auto-refresh interceptor

### Phase 4: Security & Testing
1. Add rate limiting
2. Implement email verification
3. Test all authentication flows
4. Update documentation

## Database Schema Changes

### Users Table Additions:
```sql
ALTER TABLE users ADD COLUMN password_hash VARCHAR(255);
ALTER TABLE users ADD COLUMN google_id INTEGER UNIQUE;
ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN auth_method VARCHAR(20) DEFAULT 'github';
ALTER TABLE users ADD COLUMN last_login TIMESTAMP;
```

### New Refresh Tokens Table:
```sql
CREATE TABLE refresh_tokens (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_id VARCHAR(64) UNIQUE NOT NULL,
  device_info TEXT,
  ip_address INET,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
  revoked BOOLEAN DEFAULT FALSE,
  revoked_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_token_id ON refresh_tokens(token_id);
CREATE INDEX idx_refresh_tokens_expires ON refresh_tokens(expires_at);
```

## API Endpoints

### Authentication Endpoints:
```
GET    /api/auth/github           # Existing - Initiate GitHub OAuth
GET    /api/auth/github/callback  # Existing - GitHub callback
GET    /api/auth/google           # New - Initiate Google OAuth  
GET    /api/auth/google/callback  # New - Google callback
POST   /api/auth/register         # New - Email/password registration
POST   /api/auth/login            # New - Email/password login
POST   /api/auth/refresh          # Enhanced - Refresh tokens with rotation
POST   /api/auth/logout           # New - Logout (revoke refresh token)
POST   /api/auth/verify-email     # New - Verify email address
POST   /api/auth/forgot-password  # New - Request password reset
POST   /api/auth/reset-password   # New - Reset password with token
```

## Security Considerations

1. **Password Security:**
   - Use bcrypt with appropriate work factor
   - Minimum password length: 8 characters
   - Password strength validation

2. **Token Security:**
   - Store refresh tokens hashed in database
   - Implement token blacklisting on logout
   - Short access token lifetime (15 minutes)

3. **Rate Limiting:**
   - Login attempts: 5 per 15 minutes per IP
   - Registration: 3 per hour per IP
   - Password reset: 3 per hour per email

4. **Email Verification:**
   - Send verification email on registration
   - Require verification for full access
   - Resend verification email option

## Frontend Changes

### Auth Store Updates:
- Add methods for Google OAuth
- Add methods for email/password login
- Update token storage to handle refresh tokens
- Enhance auto-refresh logic

### UI Components:
- Google OAuth button component
- Email/password login form
- Registration form
- Password reset flow

## Migration Strategy

1. **Backward Compatibility:**
   - Existing GitHub OAuth continues to work
   - Current JWT tokens still valid until expiry
   - Gradual migration to new token system

2. **Data Migration:**
   - Add nullable columns first
   - Migrate existing users gradually
   - Set default values for new fields

## Testing Plan

1. **Unit Tests:**
   - Password hashing/verification
   - Token generation/validation
   - OAuth flow mocks

2. **Integration Tests:**
   - Complete OAuth flows
   - Email/password registration/login
   - Token refresh rotation

3. **End-to-End Tests:**
   - User registration flow
   - Login with all methods
   - Token expiration and refresh
   - Logout and token revocation

## Dependencies

### Backend:
- `python-jose[cryptography]` - JWT handling (already installed)
- `bcrypt` - Password hashing
- `httpx` - HTTP client (already installed)
- `email-validator` - Email validation

### Frontend:
- `@nuxtjs/google-auth` or custom implementation
- Password strength meter component

## Timeline & Priority

**High Priority (Week 1):**
1. Database migrations
2. Google OAuth implementation
3. Basic email/password authentication

**Medium Priority (Week 2):**
1. Enhanced JWT with refresh tokens
2. Frontend auth store updates
3. Auto-refresh implementation

**Low Priority (Week 3):**
1. Email verification
2. Password reset flow
3. Advanced security features

## Success Metrics

1. Users can authenticate via GitHub, Google, or email/password
2. Tokens automatically refresh before expiration
3. Refresh tokens properly rotated and revoked
4. All existing functionality remains working
5. Security vulnerabilities addressed

## Risk Mitigation

1. **Data Loss:** Backup database before migrations
2. **Downtime:** Deploy during low-traffic periods
3. **Security:** Thorough security review before production
4. **Compatibility:** Maintain API compatibility for existing clients