# Google OAuth Setup Guide

## Problem
When trying to authenticate with Google, you get a 400 error: "Die Anfrage kann vom Server nicht verarbeitet werden, da sie fehlerhaft ist."

## Root Cause
The Google OAuth credentials are not configured in the `.env` file. When the application tries to generate a Google OAuth URL, it uses `client_id=None` and `redirect_uri=None`, which Google's servers reject with a 400 error.

## Solution Implemented

### 1. Updated `.env` file
Added Google OAuth configuration with clear instructions:
```env
# Google OAuth - REQUIRED for Google login
# 1. Create a project at https://console.cloud.google.com/
# 2. Enable Google OAuth API
# 3. Create OAuth 2.0 credentials
# 4. Add authorized redirect URI: http://localhost:8000/api/auth/google/callback
# 5. Copy Client ID and Client Secret here
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
GOOGLE_CALLBACK_URL=http://localhost:8000/api/auth/google/callback
```

### 2. Added validation in `google_oauth.py`
Added a `validate_google_config()` function that checks if Google OAuth credentials are properly configured before generating URLs or making API calls.

### 3. Improved error messages
Instead of generating invalid URLs with `client_id=None`, the application now returns clear error messages:
```
{
  "detail": "Failed to generate Google OAuth URL: Google OAuth is not configured. Please set GOOGLE_CLIENT_ID in .env file. See backend/.env for instructions."
}
```

## Steps to Enable Google OAuth

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the "Google OAuth 2.0 API"

### Step 2: Configure OAuth Consent Screen
1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" user type
3. Fill in required information:
   - App name: "Hackathon Dashboard"
   - User support email: your email
   - Developer contact information: your email
4. Add scopes: `.../auth/userinfo.email`, `.../auth/userinfo.profile`, `openid`
5. Add test users (optional for testing)

### Step 3: Create OAuth 2.0 Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Web application"
4. Add authorized redirect URIs:
   - For development: `http://localhost:8000/api/auth/google/callback`
   - For production: `https://api.yourdomain.com/api/auth/google/callback`
5. Click "Create"
6. Copy the Client ID and Client Secret

### Step 4: Update `.env` file
Replace the placeholder values in `backend/.env`:
```env
GOOGLE_CLIENT_ID=your-actual-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-actual-client-secret
GOOGLE_CALLBACK_URL=http://localhost:8000/api/auth/google/callback
```

### Step 5: Restart the backend
```bash
cd backend
# If using uvicorn directly
uvicorn main:app --reload

# Or using the startup script
./start.sh
```

## Testing
1. Go to the frontend login page
2. Click "Sign in with Google"
3. You should be redirected to Google's authentication page
4. After authentication, you should be redirected back to the application with a valid JWT token

## Troubleshooting

### Error: "Invalid redirect_uri"
Make sure the redirect URI in your Google Cloud Console matches exactly the `GOOGLE_CALLBACK_URL` in your `.env` file.

### Error: "Client ID not found"
Verify that the Client ID is correctly copied from Google Cloud Console.

### Error: "The OAuth client was deleted"
Check if the OAuth credentials were accidentally deleted in Google Cloud Console.

### Error: "redirect_uri_mismatch"
The redirect URI in the authorization request doesn't match the authorized redirect URIs in Google Cloud Console. Update the authorized redirect URIs to include:
- `http://localhost:8000/api/auth/google/callback` (development)
- `https://api.yourdomain.com/api/auth/google/callback` (production)

## Production Deployment
For production, update the environment variables:
```env
GOOGLE_CALLBACK_URL=https://api.yourdomain.com/api/auth/google/callback
FRONTEND_URL=https://yourdomain.com
```

Also update the authorized redirect URIs in Google Cloud Console to include your production callback URL.

## Security Notes
1. Never commit actual Client IDs or Client Secrets to version control
2. Use environment variables or secret management in production
3. Regularly rotate Client Secrets
4. Monitor authentication logs for suspicious activity