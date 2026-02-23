"""
Main FastAPI application entry point.
"""
import importlib
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import engine
from app.domain.models.base import Base

# Import routers
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.users.routes import router as users_router
from app.api.v1.projects.routes import router as projects_router
from app.api.v1.hackathons.routes import router as hackathons_router
from app.api.v1.teams.routes import router as teams_router
from app.api.v1.notifications.routes import router as notifications_router
from app.api.v1.me.routes import router as me_router
from app.api.v1.comments.routes import router as comments_router
from app.api.v1.newsletter.routes import router as newsletter_router
from app.api.v1.notification_types.routes import (
    router as notification_types_router
)
from app.api.v1.compatibility.routes import router as compatibility_router
from app.api.v1.push.routes import router as push_router

logger = logging.getLogger(__name__)

# Uploads router is optional for backward compatibility
# Try to import dynamically to avoid breaking if module doesn't exist
UPLOADS_AVAILABLE = False
uploads_router = None
try:
    # Try to import the uploads module
    uploads_module = importlib.import_module('app.api.v1.uploads.routes')
    uploads_router = uploads_module.router
    UPLOADS_AVAILABLE = True
except ImportError:
    logger.warning(
        "Uploads module not available. File upload functionality disabled."
    )


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Hackathon Dashboard",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Mount static files for uploaded images
upload_dir = Path(settings.UPLOAD_DIR)
upload_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static/uploads",
          StaticFiles(directory=str(upload_dir)), name="uploads")

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(projects_router, prefix="/api/projects", tags=["projects"])
app.include_router(
    hackathons_router, prefix="/api/hackathons", tags=["hackathons"]
)
app.include_router(teams_router, prefix="/api/teams", tags=["teams"])
app.include_router(
    notifications_router,
    prefix="/api/notifications",
    tags=["notifications"]
)
app.include_router(me_router, prefix="/api", tags=["me"])
app.include_router(comments_router, prefix="/api/comments", tags=["comments"])
# Include uploads router only if available
if UPLOADS_AVAILABLE:
    app.include_router(uploads_router, prefix="/api", tags=["uploads"])
app.include_router(
    newsletter_router, prefix="/api/newsletter", tags=["newsletter"]
)
app.include_router(
    notification_types_router,
    prefix="/api/notification-types",
    tags=["notification-types"]
)
app.include_router(
    compatibility_router,
    prefix="/api",
    tags=["compatibility"]
)
app.include_router(
    push_router,
    prefix="/api/push",
    tags=["push"]
)

# Debug: verify router inclusion
logger.debug(f"Push router included: {push_router}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": f"Welcome to {settings.APP_NAME}"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.APP_NAME}


# Create database tables (for development)
# In production, use Alembic migrations instead
if settings.DEBUG:
    @app.on_event("startup")
    async def startup_event():
        """Create database tables on startup in debug mode."""
        Base.metadata.create_all(bind=engine)
