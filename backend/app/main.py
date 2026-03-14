"""
Main FastAPI application entry point.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.config import settings
from app.i18n.middleware import LocaleMiddleware

# Import routers
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.users.routes import router as users_router
from app.api.v1.projects.routes import router as projects_router
from app.api.v1.hackathons.routes import router as hackathons_router
from app.api.v1.teams.routes import router as teams_router
from app.api.v1.notifications.routes import router as notifications_router
from app.api.v1.notifications.preferences_routes import (
    router as notification_preferences_router,
)
from app.api.v1.me.routes import router as me_router
from app.api.v1.comments.routes import router as comments_router
from app.api.v1.newsletter.routes import router as newsletter_router
from app.api.v1.notification_types.routes import (
    router as notification_types_router
)
from app.api.v1.uploads.routes import router as uploads_router
from app.api.v1.compatibility.routes import router as compatibility_router
from app.api.v1.push.routes import router as push_router
from app.api.v1.settings.routes import router as settings_router
from app.api.v1.admin.routes import router as admin_router
from app.api.v1.team_reports.routes import router as team_reports_router
from app.api.v1.reports.routes import router as reports_router

logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Hackathon Dashboard",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Configure CORS
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add i18n middleware for language detection
app.add_middleware(LocaleMiddleware)

# Mount static files for uploaded images
upload_dir = Path(settings.UPLOAD_DIR)
upload_dir.mkdir(parents=True, exist_ok=True)
app.mount(
    "/static/uploads",
    StaticFiles(directory=str(upload_dir)),
    name="uploads"
)

# Include routers
app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["auth"]
)
app.include_router(
    users_router,
    prefix="/api/users",
    tags=["users"]
)
app.include_router(
    projects_router,
    prefix="/api/projects",
    tags=["projects"]
)
app.include_router(
    hackathons_router,
    prefix="/api/hackathons",
    tags=["hackathons"]
)
app.include_router(
    teams_router,
    prefix="/api/teams",
    tags=["teams"]
)
app.include_router(
    notification_preferences_router,
    prefix="/api/notifications",
    tags=["notification-preferences"]
)
app.include_router(
    notifications_router,
    prefix="/api/notifications",
    tags=["notifications"]
)
app.include_router(
    me_router,
    prefix="/api",
    tags=["me"]
)
app.include_router(
    comments_router,
    prefix="/api/comments",
    tags=["comments"]
)
app.include_router(
    uploads_router,
    prefix="/api",
    tags=["uploads"]
)
app.include_router(
    newsletter_router,
    prefix="/api/newsletter",
    tags=["newsletter"]
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
app.include_router(
    settings_router,
    prefix="/api/settings",
    tags=["settings"]
)
app.include_router(
    admin_router,
    prefix="/api/admin",
    tags=["admin"]
)
app.include_router(
    team_reports_router,
    prefix="/api/team-reports",
    tags=["team-reports"]
)
app.include_router(
    reports_router,
    prefix="/api/reports",
    tags=["reports"]
)

# Debug: verify router inclusion
logger.debug(f"Push router included: {push_router}")
logger.debug(f"Settings router included: {settings_router}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": f"Welcome to {settings.APP_NAME}"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.APP_NAME}


# Initialize notification types (should run in all environments)
@app.on_event("startup")
async def initialize_notification_types():
    """Initialize notification types in the database."""
    from app.services.notification_preference_service import (
        notification_preference_service
    )
    from app.core.database import SessionLocal

    db = SessionLocal()
    try:
        notification_preference_service.initialize_notification_types(db)
        logger.info("Notification types initialized")
    except Exception as e:
        logger.error(f"Failed to initialize notification types: {e}")
    finally:
        db.close()
