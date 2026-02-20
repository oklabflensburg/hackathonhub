from fastapi import FastAPI, Depends, HTTPException, Header, Query, Request, Body
from fastapi import File, UploadFile
from sqlalchemy.orm import Session
from typing import List
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

from database import get_db
import models
import schemas
import crud
import auth
import email_service
import email_auth
import google_oauth
import file_upload

from i18n.middleware import LocaleMiddleware
from i18n.translations import get_translation

# Load environment variables
load_dotenv()

# Create database tables (commented out for Alembic migrations)
# models.Base.metadata.create_all(bind=engine)
# Note: Use Alembic for database migrations: alembic upgrade head

app = FastAPI(
    title="Hackathon Dashboard API",
    description="Backend API for Hackathon Dashboard with GitHub OAuth",
    version="1.0.0"
)

# Add i18n middleware
app.add_middleware(LocaleMiddleware)

# Serve static files (uploaded images)
# Use UPLOAD_DIR from environment or default to "uploads"
upload_dir = os.getenv("UPLOAD_DIR", "uploads")
upload_path = Path(upload_dir)

# Create directory if it doesn't exist
upload_path.mkdir(parents=True, exist_ok=True)

app.mount("/static/uploads", StaticFiles(directory=str(upload_path)), name="uploads")


@app.get("/")
async def root():
    return {"message": "Welcome to Hackathon Dashboard API"}


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "hackathon-dashboard-api"}


@app.post("/api/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    type: str = Query("project", enum=["project", "hackathon", "avatar"]),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Upload a file and return its path"""
    try:
        file_path = await file_upload.file_upload_service.save_upload_file(
            file, type
        )
        relative_url = file_upload.file_upload_service.get_file_url(file_path)
        # If relative_url is empty (file doesn't exist), construct default
        if not relative_url:
            relative_url = f"/static{file_path}"
        # Convert to absolute URL using request base URL
        if relative_url.startswith(('http://', 'https://')):
            absolute_url = relative_url
        else:
            # Ensure no double slashes
            base_url = str(request.base_url).rstrip('/')
            absolute_url = f"{base_url}{relative_url}"
        return {
            "file_path": file_path,
            "url": absolute_url,
            "filename": file.filename,
            "message": "File uploaded successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}"
        )


@app.get("/api/projects", response_model=List[schemas.Project])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    search: str = Query(None, description="Search query for full-text search"),
    db: Session = Depends(get_db)
):
    """Get all hackathon projects with optional full-text search"""
    projects = crud.get_projects(db, skip=skip, limit=limit, search=search)
    return projects


@app.post("/api/projects", response_model=schemas.Project)
async def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Create a new hackathon project"""
    return crud.create_project(db=db, project=project, user_id=current_user.id)


@app.get("/api/projects/{project_id}", response_model=schemas.Project)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    request: Request = None
):
    """Get a specific project by ID"""
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        locale = getattr(request.state, 'locale', 'en') if request else 'en'
        detail = get_translation("errors.project_not_found", locale)
        raise HTTPException(status_code=404, detail=detail)
    return project


@app.post("/api/projects/{project_id}/view")
async def increment_project_view(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Increment view count for a project"""
    project = crud.increment_project_view_count(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "message": "View count incremented",
        "view_count": project.view_count
    }


@app.put("/api/projects/{project_id}", response_model=schemas.Project)
async def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Update a project (only owner or team members can update)"""
    # Get the project
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if user is the owner
    if project.owner_id != current_user.id:
        # Check if user is a team member of the project's hackathon
        if project.hackathon_id:
            # Check if user is a team member in any team for this hackathon
            team_member = db.query(models.TeamMember).join(models.Team).filter(
                models.TeamMember.user_id == current_user.id,
                models.Team.hackathon_id == project.hackathon_id
            ).first()

            if not team_member:
                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Only the project owner or hackathon team members "
                        "can update this project"
                    )
                )
        else:
            raise HTTPException(
                status_code=403,
                detail="Only the project owner can update this project"
            )

    # Update the project
    updated_project = crud.update_project(
        db=db,
        project_id=project_id,
        project_update=project_update
    )

    if updated_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return updated_project


@app.delete("/api/projects/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Delete a project (only owner can delete)"""
    # Get the project
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if user is the owner
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the project owner can delete the project"
        )

    # Delete the project
    deleted = crud.delete_project(db, project_id=project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"message": "Project deleted successfully"}


# Vote endpoints
@app.post("/api/projects/{project_id}/vote")
async def vote_for_project(
    project_id: int,
    vote_data: dict,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Vote for a project (upvote or downvote)"""
    # Check if project exists
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get vote type from request data
    vote_type = vote_data.get('vote_type', '')

    # Map 'up'/'down' to 'upvote'/'downvote'
    if vote_type == 'up':
        vote_type = 'upvote'
    elif vote_type == 'down':
        vote_type = 'downvote'

    # Validate vote type
    if vote_type not in ['upvote', 'downvote']:
        raise HTTPException(
            status_code=400,
            detail="Invalid vote type. Must be 'upvote' or 'downvote'"
        )

    # Create vote data
    vote_create = schemas.VoteCreate(
        project_id=project_id,
        vote_type=vote_type
    )

    # Create vote
    vote = crud.create_vote(db=db, vote=vote_create, user_id=current_user.id)

    # Get updated project stats
    project = crud.get_project(db, project_id=project_id)
    db.refresh(project)  # Ensure we have latest values

    return {
        "vote": vote,
        "project_stats": {
            "project_id": project_id,
            "upvotes": project.upvote_count,
            "downvotes": project.downvote_count,
            "total_score": project.vote_score,
            "user_vote": vote.vote_type if vote else None
        }
    }


@app.delete("/api/projects/{project_id}/vote")
async def remove_vote(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Remove user's vote from a project"""
    # Check if project exists
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Delete vote
    vote = crud.delete_vote(
        db=db, user_id=current_user.id, project_id=project_id)

    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")

    # Get updated project stats
    project = crud.get_project(db, project_id=project_id)
    db.refresh(project)  # Ensure we have latest values

    return {
        "message": "Vote removed successfully",
        "project_stats": {
            "project_id": project_id,
            "upvotes": project.upvote_count,
            "downvotes": project.downvote_count,
            "total_score": project.vote_score,
            "user_vote": None
        }
    }


@app.get("/api/projects/{project_id}/vote-stats")
async def get_project_vote_stats(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get vote statistics for a project (public endpoint)"""
    # Check if project exists
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Note: user_vote will always be None for this public endpoint
    # The frontend should handle user-specific votes separately

    # Use getattr with default values in case columns don't exist yet
    # (e.g., before migration runs)
    upvotes = getattr(project, 'upvote_count', 0)
    downvotes = getattr(project, 'downvote_count', 0)
    vote_score = getattr(project, 'vote_score', 0)

    return {
        "project_id": project_id,
        "upvotes": upvotes,
        "downvotes": downvotes,
        "total_score": vote_score,
        "user_vote": None
    }


# Comment endpoints
@app.get("/api/projects/{project_id}/comments",
         response_model=List[schemas.Comment])
async def get_project_comments(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get comments for a project"""
    # Check if project exists
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    comments = crud.get_comments_by_project(
        db, project_id=project_id, skip=skip, limit=limit
    )
    return comments


@app.post("/api/projects/{project_id}/comments",
          response_model=schemas.Comment)
async def create_project_comment(
    project_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Create a comment on a project"""
    # Check if project exists
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Create the comment
    db_comment = crud.create_comment(
        db=db,
        comment=comment,
        user_id=current_user.id,
        project_id=project_id
    )

    # Update project comment count
    project.comment_count = (project.comment_count or 0) + 1
    db.commit()

    return db_comment


@app.put("/api/comments/{comment_id}", response_model=schemas.Comment)
async def update_comment(
    comment_id: int,
    comment_update: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Update a comment (only author can update)"""
    # Get the comment
    comment = crud.get_comment(db, comment_id=comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Check if user is the author
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the comment author can update this comment"
        )

    # Update the comment
    updated_comment = crud.update_comment(
        db=db,
        comment_id=comment_id,
        comment_update=comment_update
    )

    if updated_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return updated_comment


@app.delete("/api/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Delete a comment (only author can delete)"""
    # Get the comment
    comment = crud.get_comment(db, comment_id=comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Check if user is the author
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the comment author can delete this comment"
        )

    # Delete the comment
    deleted_comment = crud.delete_comment(db, comment_id=comment_id)

    if deleted_comment:
        # Update project comment count
        project = crud.get_project(db, project_id=comment.project_id)
        if project:
            project.comment_count = max(0, (project.comment_count or 1) - 1)
            db.commit()

    return {"message": "Comment deleted successfully"}


@app.post("/api/comments/{comment_id}/vote")
async def vote_for_comment(
    comment_id: int,
    vote: schemas.CommentVoteCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Vote on a comment (upvote/downvote)"""
    # Check if comment exists
    comment = crud.get_comment(db, comment_id=comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Create or update vote
    crud.create_comment_vote(
        db=db,
        vote=vote,
        user_id=current_user.id,
        comment_id=comment_id
    )

    return {
        "message": "Vote recorded successfully",
        "comment_id": comment_id,
        "vote_type": vote.vote_type,
        "upvote_count": comment.upvote_count or 0,
        "downvote_count": comment.downvote_count or 0
    }


@app.delete("/api/comments/{comment_id}/vote")
async def remove_comment_vote(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Remove vote from a comment"""
    # Check if comment exists
    comment = crud.get_comment(db, comment_id=comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Delete vote
    deleted_vote = crud.delete_comment_vote(
        db=db,
        comment_id=comment_id,
        user_id=current_user.id
    )

    if deleted_vote:
        return {
            "message": "Vote removed successfully",
            "comment_id": comment_id,
            "upvote_count": comment.upvote_count or 0,
            "downvote_count": comment.downvote_count or 0
        }
    else:
        raise HTTPException(
            status_code=404,
            detail="No vote found for this comment"
        )


@app.get("/api/users/me/votes")
async def get_user_votes(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Get all votes by the current user with project details"""
    votes = crud.get_user_votes(db, user_id=current_user.id)

    # Enrich votes with project details
    enriched_votes = []
    for vote in votes:
        # Get project details
        project = crud.get_project(db, project_id=vote.project_id)
        if project:
            # Get hackathon name if exists
            hackathon_name = None
            if project.hackathon:
                hackathon_name = project.hackathon.name

            # Get technologies as array
            technologies = []
            if project.technologies:
                tech_list = project.technologies.split(',')
                technologies = [
                    tech.strip() for tech in tech_list if tech.strip()
                ]

            # Calculate total votes
            total_votes = project.upvote_count + project.downvote_count

            # Prepare vote data
            vote_data = {
                "id": vote.id,
                "project_id": vote.project_id,
                "vote_type": vote.vote_type,
                "created_at": vote.created_at,
                "project_name": project.title,
                "project_description": project.description,
                "project_image": project.image_path,
                "project_technologies": technologies,
                "project_vote_count": total_votes,
                "project_comment_count": project.comment_count,
                "project_view_count": project.view_count,
                "hackathon_name": hackathon_name
            }

            # Add author name if available
            if project.owner:
                vote_data["project_author"] = project.owner.name
            else:
                vote_data["project_author"] = "Unknown"

            enriched_votes.append(vote_data)

    return enriched_votes


@app.get("/api/users/me/projects", response_model=List[schemas.Project])
async def get_user_projects(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Get all projects owned by the current user"""
    projects = crud.get_projects_by_user(db, user_id=current_user.id)
    return projects


@app.get("/api/users/me/stats")
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Get user statistics"""
    # Count user's projects
    projects_count = db.query(models.Project).filter(
        models.Project.owner_id == current_user.id
    ).count()

    # Count user's hackathons (where user is owner)
    hackathons_count = db.query(models.Hackathon).filter(
        models.Hackathon.owner_id == current_user.id
    ).count()

    # Count user's votes
    votes_count = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id
    ).count()

    return {
        "hackathonsCreated": hackathons_count,
        "projectsSubmitted": projects_count,
        "totalVotes": votes_count
    }


@app.get("/api/hackathons", response_model=List[schemas.Hackathon])
async def get_hackathons(
    skip: int = 0,
    limit: int = 100,
    search: str = Query(None, description="Search query for full-text search"),
    db: Session = Depends(get_db)
):
    """Get all hackathons with optional full-text search"""
    hackathons = crud.get_hackathons(db, skip=skip, limit=limit, search=search)
    return hackathons


@app.post("/api/hackathons", response_model=schemas.Hackathon)
async def create_hackathon(
    hackathon: schemas.HackathonCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Create a new hackathon"""
    # Geocode the location if not already provided
    if hackathon.location and not (hackathon.latitude and hackathon.longitude):
        from geocoding import geocode_address
        coordinates = await geocode_address(hackathon.location)
        if coordinates:
            hackathon.latitude, hackathon.longitude = coordinates

    return crud.create_hackathon(
        db=db, hackathon=hackathon, owner_id=current_user.id
    )


@app.get("/api/hackathons/{hackathon_id}", response_model=schemas.Hackathon)
async def get_hackathon(
    hackathon_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific hackathon by ID"""
    hackathon = crud.get_hackathon(db, hackathon_id=hackathon_id)
    if hackathon is None:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    return hackathon


@app.put("/api/hackathons/{hackathon_id}", response_model=schemas.Hackathon)
async def update_hackathon(
    hackathon_id: int,
    hackathon_update: schemas.HackathonUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Update a hackathon (only owner can update)"""
    # Get the hackathon
    hackathon = crud.get_hackathon(db, hackathon_id=hackathon_id)
    if hackathon is None:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    # Check if user is the owner
    if hackathon.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the hackathon owner can update this hackathon"
        )

    # Geocode the location if it's being updated and coordinates not provided
    if (hackathon_update.location is not None and
            not (hackathon_update.latitude and hackathon_update.longitude)):
        from geocoding import geocode_address
        coordinates = await geocode_address(hackathon_update.location)
        if coordinates:
            hackathon_update.latitude, hackathon_update.longitude = coordinates

    # Update the hackathon
    updated_hackathon = crud.update_hackathon(
        db=db,
        hackathon_id=hackathon_id,
        hackathon_update=hackathon_update
    )

    if updated_hackathon is None:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    return updated_hackathon


@app.get(
    "/api/hackathons/{hackathon_id}/registrations",
    response_model=List[schemas.HackathonRegistration]
)
async def get_hackathon_registrations(
    hackathon_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Get all registrations for a hackathon"""
    # Check if hackathon exists
    hackathon = crud.get_hackathon(db, hackathon_id=hackathon_id)
    if hackathon is None:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    registrations = crud.get_hackathon_participants(
        db, hackathon_id=hackathon_id)
    return registrations


@app.get(
    "/api/hackathons/{hackathon_id}/participants",
    response_model=List[schemas.HackathonParticipant]
)
async def get_hackathon_participants(
    hackathon_id: int,
    db: Session = Depends(get_db)
):
    """Get all participants for a hackathon with user details"""
    # Check if hackathon exists
    hackathon = crud.get_hackathon(db, hackathon_id=hackathon_id)
    if hackathon is None:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    participants = crud.get_hackathon_participants_with_users(
        db, hackathon_id=hackathon_id)
    return participants


@app.get(
    "/api/me/registrations",
    response_model=List[schemas.HackathonRegistration]
)
async def get_my_registrations(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Get current user's hackathon registrations"""
    registrations = crud.get_user_hackathon_registrations(
        db, user_id=current_user.id)
    return registrations


@app.post("/api/hackathons/{hackathon_id}/register")
async def register_for_hackathon(
    hackathon_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Register current user for a hackathon"""
    # Check if hackathon exists
    hackathon = crud.get_hackathon(db, hackathon_id=hackathon_id)
    if hackathon is None:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    # Check if user is already registered
    existing = crud.get_user_registration_for_hackathon(
        db, user_id=current_user.id, hackathon_id=hackathon_id)
    if existing:
        return {
            "registration": existing,
            "is_new": False,
            "message": "You are already registered for this hackathon"
        }

    # Create registration
    registration_data = schemas.HackathonRegistrationCreate(
        hackathon_id=hackathon_id,
        status="registered"
    )

    registration = crud.create_hackathon_registration(
        db=db,
        registration=registration_data,
        user_id=current_user.id
    )
    return {
        "registration": registration,
        "is_new": True,
        "message": "Successfully registered for the hackathon!"
    }


@app.delete("/api/hackathons/{hackathon_id}/unregister")
async def unregister_from_hackathon(
    hackathon_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Unregister current user from a hackathon"""
    # Check if registration exists
    registration = crud.get_user_registration_for_hackathon(
        db, user_id=current_user.id, hackathon_id=hackathon_id
    )

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    crud.delete_hackathon_registration(db, registration_id=registration.id)
    return {"message": "Successfully unregistered from hackathon"}


@app.get("/api/auth/github")
async def github_auth(redirect_url: str = Query(None)):
    """Initiate GitHub OAuth flow"""
    client_id = os.getenv("GITHUB_CLIENT_ID")
    scope = "user:email"

    # Validate that we're using a GitHub client ID, not a Google client ID
    if not client_id:
        raise HTTPException(
            status_code=500,
            detail="GitHub OAuth is not configured. Please set GITHUB_CLIENT_ID in .env file."
        )
    
    # Check if client_id looks like a Google client ID (common mistake)
    if "apps.googleusercontent.com" in client_id:
        raise HTTPException(
            status_code=500,
            detail="Configuration error: GitHub client ID appears to be a Google client ID. "
                   "Please check your .env file and ensure GITHUB_CLIENT_ID is set to a valid GitHub OAuth client ID."
        )

    # Build authorization URL with state parameter containing redirect URL
    authorization_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={client_id}&scope={scope}"
    )

    # Add state parameter if redirect_url is provided
    if redirect_url:
        import urllib.parse
        encoded_state = urllib.parse.quote(redirect_url)
        authorization_url += f"&state={encoded_state}"

    return {"authorization_url": authorization_url}


@app.get("/api/auth/github/callback")
async def github_callback(
    code: str,
    state: str = Query(None),
    db: Session = Depends(get_db)
):
    """Handle GitHub OAuth callback and redirect to frontend"""
    try:
        from github_oauth import authenticate_with_github
        result = await authenticate_with_github(code, db)

        # Redirect to frontend with token in query parameter
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        import urllib.parse
        token = urllib.parse.quote(result["access_token"])

        # Use state (redirect URL) if provided, otherwise redirect to home
        if state:
            # Decode the state (which contains the original redirect URL)
            decoded_state = urllib.parse.unquote(state)
            # Ensure redirect URL is within our frontend domain for security
            if decoded_state.startswith('/'):
                # It's a path within our frontend
                redirect_url = (
                    f"{frontend_url}{decoded_state}"
                    f"?token={token}&source=github"
                )
            else:
                # Fallback to home if state is malformed
                redirect_url = f"{frontend_url}/?token={token}&source=github"
        else:
            redirect_url = f"{frontend_url}/?token={token}&source=github"

        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=redirect_url)
    except Exception as e:
        # On error, redirect to frontend with error
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        import urllib.parse
        error_msg = urllib.parse.quote(str(e))

        # Use state for error redirect if available
        if state:
            decoded_state = urllib.parse.unquote(state)
            if decoded_state.startswith('/'):
                redirect_url = (
                    f"{frontend_url}{decoded_state}"
                    f"?error={error_msg}&source=github"
                )
            else:
                redirect_url = (
                    f"{frontend_url}/?error={error_msg}&source=github"
                )
        else:
            redirect_url = f"{frontend_url}/?error={error_msg}&source=github"

        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=redirect_url)


@app.post("/api/auth/register")
async def register_user(
    user_data: schemas.UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user with email/password"""
    try:
        # Register user
        result = email_auth.register_user(db, user_data)

        # Send verification email
        email_auth.send_verification_email(
            db, result["user"].id, result["user"].email
        )

        return {
            "message": "User registered successfully. "
                       "Please check your email for verification.",
            "user": result["user"],
            "requires_verification": True
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )


@app.post("/api/auth/login")
async def login_user(
    credentials: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    """Login with email/password"""
    try:
        result = email_auth.authenticate_user(
            db, credentials.email, credentials.password
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Login failed: {str(e)}"
        )


@app.post("/api/auth/verify-email")
async def verify_email(
    token: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """Verify email address using verification token"""
    try:
        from email_verification import verify_email_token
        user = verify_email_token(db, token)
        return {
            "message": "Email verified successfully",
            "user": schemas.User.from_orm(user)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Email verification failed: {str(e)}"
        )


@app.get("/api/auth/google")
async def google_auth(redirect_url: str = Query(None)):
    """Initiate Google OAuth flow"""
    try:
        auth_url = google_oauth.get_google_auth_url(redirect_url)
        return {"authorization_url": auth_url}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate Google OAuth URL: {str(e)}"
        )


@app.get("/api/auth/google/callback")
async def google_callback(
    code: str,
    state: str = Query(None),
    db: Session = Depends(get_db)
):
    """Handle Google OAuth callback and redirect to frontend"""
    try:
        result = await google_oauth.authenticate_with_google(code, db)

        # Redirect to frontend with token in query parameter
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        import urllib.parse
        token = urllib.parse.quote(result["access_token"])

        # Use state (redirect URL) if provided, otherwise redirect to home
        if state:
            decoded_state = urllib.parse.unquote(state)
            if decoded_state.startswith('/'):
                redirect_url = (
                    f"{frontend_url}{decoded_state}"
                    f"?token={token}&source=google"
                )
            else:
                redirect_url = f"{frontend_url}/?token={token}&source=google"
        else:
            redirect_url = f"{frontend_url}/?token={token}&source=google"

        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=redirect_url)
    except Exception as e:
        # On error, redirect to frontend with error
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        import urllib.parse
        error_msg = urllib.parse.quote(str(e))

        if state:
            decoded_state = urllib.parse.unquote(state)
            if decoded_state.startswith('/'):
                redirect_url = (
                    f"{frontend_url}{decoded_state}"
                    f"?error={error_msg}&source=google"
                )
            else:
                redirect_url = (
                    f"{frontend_url}/?error={error_msg}&source=google"
                )
        else:
            redirect_url = f"{frontend_url}/?error={error_msg}&source=google"

        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=redirect_url)


@app.post("/api/auth/refresh")
async def refresh_token(
    authorization: str = Header(None, alias="Authorization"),
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header"
        )

    token = authorization.replace("Bearer ", "")

    try:
        # Use refresh_tokens which handles token rotation
        result = auth.refresh_tokens(token, db)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Token refresh failed: {str(e)}"
        )


@app.post("/api/newsletter/subscribe")
async def subscribe_to_newsletter(
    subscription: schemas.NewsletterSubscriptionCreate,
    db: Session = Depends(get_db)
):
    """Subscribe to newsletter"""
    try:
        # Create subscription in database
        db_subscription = crud.create_newsletter_subscription(
            db=db,
            email=subscription.email,
            source=subscription.source
        )

        # Send welcome email
        email_sent = email_service.send_newsletter_welcome(
            subscription.email
        )

        return {
            "message": "Successfully subscribed to newsletter",
            "email": subscription.email,
            "subscribed_at": db_subscription.subscribed_at,
            "welcome_email_sent": email_sent
        }

    except Exception as e:
        # Check if it's a duplicate email error
        if "UNIQUE constraint failed" in str(e):
            # Check if already subscribed
            existing = crud.get_newsletter_subscription(db, subscription.email)
            if existing and existing.is_active:
                return {
                    "message": "Already subscribed to newsletter",
                    "email": subscription.email,
                    "already_subscribed": True
                }

        raise HTTPException(
            status_code=400,
            detail=f"Failed to subscribe: {str(e)}"
        )


@app.post("/api/newsletter/unsubscribe")
async def unsubscribe_from_newsletter(
    email: str,
    db: Session = Depends(get_db)
):
    """Unsubscribe from newsletter"""
    subscription = crud.unsubscribe_newsletter(db, email)

    if subscription:
        return {
            "message": "Successfully unsubscribed from newsletter",
            "email": email,
            "unsubscribed_at": subscription.unsubscribed_at
        }
    else:
        raise HTTPException(
            status_code=404,
            detail="Email not found in newsletter subscriptions"
        )


@app.get("/api/me", response_model=schemas.User)
async def get_current_user(
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Get current authenticated user"""
    return current_user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
