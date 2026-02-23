"""
GitHub OAuth service for authentication with GitHub accounts.
"""
import httpx
from sqlalchemy.orm import Session
from datetime import datetime
import os
from dotenv import load_dotenv

from app.domain.schemas.user import UserCreate, UserUpdate
from app.repositories.user_repository import (
    UserRepository, RefreshTokenRepository
)
from app.core.auth import create_tokens

load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_CALLBACK_URL = os.getenv("GITHUB_CALLBACK_URL")


class GitHubOAuthService:
    """Service for GitHub OAuth authentication operations."""

    def __init__(self):
        self.user_repository = UserRepository()
        self.refresh_token_repository = RefreshTokenRepository()

    @staticmethod
    def validate_github_config():
        """Validate that GitHub OAuth credentials are configured correctly."""
        if not GITHUB_CLIENT_ID:
            raise ValueError(
                "GitHub OAuth is not configured. Please set GITHUB_CLIENT_ID "
                "in .env file."
            )

        # Check if client_id looks like a Google client ID (common mistake)
        if "apps.googleusercontent.com" in GITHUB_CLIENT_ID:
            raise ValueError(
                "Configuration error: GitHub client ID appears to be a "
                "Google client ID. Please check your .env file and ensure "
                "GITHUB_CLIENT_ID is set to a valid GitHub OAuth client ID."
            )

        if not GITHUB_CLIENT_SECRET:
            raise ValueError(
                "GitHub OAuth is not configured. Please set "
                "GITHUB_CLIENT_SECRET in .env file."
            )

        if not GITHUB_CALLBACK_URL:
            raise ValueError(
                "GitHub OAuth callback URL is not configured. "
                "Please set GITHUB_CALLBACK_URL in .env file."
            )

    @staticmethod
    async def exchange_code_for_token(code: str) -> dict:
        """Exchange GitHub OAuth code for access token."""
        # Validate configuration before making API call
        GitHubOAuthService.validate_github_config()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": GITHUB_CLIENT_ID,
                    "client_secret": GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": GITHUB_CALLBACK_URL
                }
            )

            if response.status_code != 200:
                raise Exception(f"Failed to exchange code: {response.text}")

            return response.json()

    @staticmethod
    async def get_github_user_info(access_token: str) -> dict:
        """Get user info from GitHub API using access token."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"token {access_token}",
                    "Accept": "application/json"
                }
            )

            if response.status_code != 200:
                raise Exception(f"Failed to get user info: {response.text}")

            user_data = response.json()

            # Get user emails
            email_response = await client.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"token {access_token}",
                    "Accept": "application/json"
                }
            )

            if email_response.status_code == 200:
                emails = email_response.json()
            else:
                emails = []
            primary_email = next(
                (email["email"] for email in emails if email["primary"]), None)

            return {
                "github_id": user_data["id"],
                "username": user_data["login"],
                "email": primary_email or user_data.get("email", ""),
                "name": user_data.get("name", ""),
                "avatar_url": user_data.get("avatar_url", ""),
                "bio": user_data.get("bio", ""),
                "location": user_data.get("location", ""),
                "company": user_data.get("company", ""),
                "blog": user_data.get("blog", ""),
                "twitter_username": user_data.get("twitter_username", "")
            }

    async def authenticate_with_github(
        self,
        code: str,
        db: Session,
        current_user_id: int = None
    ) -> dict:
        """Complete GitHub OAuth authentication flow.

        Args:
            code: GitHub OAuth code
            db: Database session
            current_user_id: Optional ID of the user trying to link
                            GitHub account. If provided and GitHub account
                            is already associated with a different user,
                            raises an exception.
        """
        # Validate configuration before starting OAuth flow
        self.validate_github_config()

        # Exchange code for access token
        token_data = await self.exchange_code_for_token(code)
        access_token = token_data.get("access_token")

        if not access_token:
            raise Exception("No access token received from GitHub")

        # Get user info from GitHub
        github_user = await self.get_github_user_info(access_token)

        # Check if user exists in database
        db_user = self.user_repository.get_by_github_id(
            db, github_user["github_id"])

        # If current_user_id is provided (user trying to link GitHub account)
        if current_user_id is not None:
            if db_user:
                # GitHub account is already associated with a user
                if db_user.id != current_user_id:
                    # GitHub account belongs to a different user
                    error_msg = (
                        "github_account_already_linked: GitHub account is "
                        "already associated with another user "
                        f"(username: {db_user.username})"
                    )
                    raise Exception(error_msg)
                else:
                    # GitHub account already belongs to the current user
                    # This is fine - they're already connected
                    pass
            else:
                # GitHub account is not associated with any user
                # We should link it to the current user
                # Update current user with GitHub info
                current_user = self.user_repository.get(db, current_user_id)
                if current_user:
                    # Update user with GitHub info
                    user_update = UserUpdate(
                        github_id=github_user["github_id"],
                        avatar_url=github_user["avatar_url"] or
                        current_user.avatar_url,
                        bio=github_user["bio"] or current_user.bio,
                        location=github_user["location"] or
                        current_user.location,
                        company=github_user["company"] or current_user.company
                    )
                    db_user = self.user_repository.update_from_schema(
                        db, current_user_id, user_update)
                else:
                    raise Exception("Current user not found")

        # Normal flow (login/registration)
        else:
            if not db_user:
                # Create new user
                user_create = UserCreate(
                    github_id=github_user["github_id"],
                    username=github_user["username"],
                    email=github_user["email"],
                    name=github_user["name"],
                    avatar_url=github_user["avatar_url"],
                    bio=github_user["bio"],
                    location=github_user["location"],
                    company=github_user["company"],
                    access_token=access_token
                )
                db_user = self.user_repository.create_from_schema(
                    db, user_create)
            else:
                # Update existing user with latest info
                # (In a real app, you might want to update some fields)
                pass

        # Create tokens using the new JWT system with refresh tokens
        tokens = create_tokens(db_user.id, db_user.username)

        # Store refresh token in database
        self.refresh_token_repository.create_token(
            db,
            user_id=db_user.id,
            token_id=tokens["refresh_token_id"],
            expires_at=datetime.utcnow() + tokens["refresh_token_expires"]
        )

        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer",
            "user": db_user
        }


# Global GitHub OAuth service instance
github_oauth = GitHubOAuthService()